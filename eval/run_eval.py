"""
DynToM Evaluation Runner

Runs inference on the DynToM benchmark for specified models.
Prompt construction exactly replicates the original llm_api/prompt.py (commit 8e435482).

Usage:
    python eval/run_eval.py --model gpt-4-turbo
    python eval/run_eval.py --model gpt-5.4 --start 50 --end 100
    python eval/run_eval.py --model all
"""

import argparse
import json
import logging
import os
import time
import unicodedata

from tqdm import tqdm

from config import DATA_DIR, RESULTS_DIR, REQUIRE_PROMPT, MODELS, get_api_key

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(RESULTS_DIR, "eval.log")),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Prompt construction (exact replica of old llm_api/prompt.py)
# ---------------------------------------------------------------------------

def construct_prompt(trial_id, information_type="level1"):
    """Construct the evaluation prompt for a given trial.

    Exactly replicates the logic from llm_api/prompt.py (commit 8e435482):
    - Loads story.json and question_new.json
    - For level1: removes 'background' key from each scenario
    - Strips questions to only 'question' and 'options' fields
    - Returns (system_prompt_string, require_prompt_string)
    """
    story_path = os.path.join(DATA_DIR, f"trial{trial_id}", "story.json")
    question_path = os.path.join(DATA_DIR, f"trial{trial_id}", "question_new.json")

    with open(story_path, encoding="UTF-8") as f:
        script = json.load(f)
    with open(question_path, encoding="UTF-8") as f:
        questions = json.load(f)

    story = script["story"]

    if information_type == "level1":
        # Remove background from each scenario (dialogue only)
        for key, value in story.items():
            value.pop("background", None)

    # Handle nested "questions" key if present
    if "questions" in questions:
        questions = questions["questions"]

    # Strip questions to only question + options (remove true answer, option reasons, etc.)
    questions_new = {}
    for key, value in questions.items():
        questions_new[key] = {
            "question": value["question"],
            "options": value["options"],
        }

    characters_information = script["characters information"]
    system_prompt = f"Answer all the {len(questions_new)} questions based on the story"
    full_prompt = f"{system_prompt}\n{characters_information}\n{story}\n{questions_new}\n{system_prompt}"

    return full_prompt, REQUIRE_PROMPT


# ---------------------------------------------------------------------------
# Response parsing (exact replica of old convert_to_json from model_chat.py)
# ---------------------------------------------------------------------------

def parse_json_response(raw_text):
    """Parse model response text into a dict of {question_id: answer_letter}.

    Replicates the convert_to_json logic from model_chat.py (commit 8e435482).
    """
    if not raw_text:
        return {}

    content = unicodedata.normalize("NFKC", raw_text)

    # Strip markdown code fences
    if "```json" in content:
        content = content[content.find("```json") + 7:]
    if "```" in content:
        content = content[:content.find("```")]

    content = content.strip()

    # Extract JSON object
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1 or end <= start:
        logger.error("No JSON object found in response")
        return {}

    content = content[start:end + 1]

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        logger.error("JSON decode error. Raw content:\n%s", content[:500])
        return {}

    # Normalize answer values to single lowercase letters
    result = {}
    for q_id, answer in parsed.items():
        if isinstance(answer, str) and len(answer) >= 1:
            result[q_id] = answer.strip().lower()[0]
        else:
            result[q_id] = str(answer).strip().lower()[:1] if answer else ""

    return result


# ---------------------------------------------------------------------------
# Model API calls
# ---------------------------------------------------------------------------

def call_openai_chat(model_id, system_msg, user_msg):
    """Call OpenAI Chat Completions API (for GPT-4-Turbo reference)."""
    from openai import OpenAI
    client = OpenAI(api_key=get_api_key("openai_chat"))
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.0,
    )
    return completion.choices[0].message.content


def call_openai_responses(model_id, system_msg, user_msg):
    """Call OpenAI Responses API (for GPT-5.4, GPT-5.4 Pro)."""
    from openai import OpenAI
    client = OpenAI(api_key=get_api_key("openai_responses"))
    response = client.responses.create(
        model=model_id,
        instructions=system_msg,
        input=user_msg,
    )
    return response.output_text


def call_anthropic(model_id, system_msg, user_msg):
    """Call Anthropic Messages API (for Claude Opus 4.6)."""
    import anthropic
    client = anthropic.Anthropic(api_key=get_api_key("anthropic"))
    message = client.messages.create(
        model=model_id,
        max_tokens=8192,
        system=system_msg,
        messages=[{"role": "user", "content": user_msg}],
    )
    return message.content[0].text


def call_google(model_id, system_msg, user_msg):
    """Call Google GenAI API (for Gemini 3.1 Pro)."""
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=get_api_key("google"))
    response = client.models.generate_content(
        model=model_id,
        config=types.GenerateContentConfig(system_instruction=system_msg),
        contents=user_msg,
    )
    return response.text


PROVIDER_FUNCTIONS = {
    "openai_chat": call_openai_chat,
    "openai_responses": call_openai_responses,
    "anthropic": call_anthropic,
    "google": call_google,
}


def validate_answers(answers, expected=71):
    """Check that answers dict has sufficient non-empty responses.

    Returns True if at least `expected` questions have non-empty answers.
    """
    if not answers:
        return False
    answered = sum(1 for v in answers.values() if v and str(v).strip())
    return answered >= expected


def call_model(model_name, system_msg, user_msg, max_retries=5, delay=2):
    """Call the appropriate model API with retry logic and rate limiting.

    Retries on exceptions AND on empty/incomplete responses (e.g. Gemini
    returning nothing when rate-limited instead of raising an error).
    """
    provider, model_id = MODELS[model_name]
    call_fn = PROVIDER_FUNCTIONS[provider]

    for attempt in range(max_retries):
        try:
            result = call_fn(model_id, system_msg, user_msg)
            # Rate limiting: pause between calls to avoid 429s
            if delay > 0:
                time.sleep(delay)
            # Check for empty/None responses (some providers fail silently)
            if not result or not result.strip():
                wait = 10 * (2 ** attempt)
                logger.warning(
                    "Attempt %d/%d for %s returned empty response. Retrying in %ds...",
                    attempt + 1, max_retries, model_name, wait,
                )
                if attempt < max_retries - 1:
                    time.sleep(wait)
                    continue
                else:
                    logger.error("All retries exhausted for %s (empty responses)", model_name)
                    return None
            return result
        except Exception as e:
            wait = 10 * (2 ** attempt)  # 10s, 20s, 40s, 80s, 160s
            logger.warning(
                "Attempt %d/%d failed for %s: %s. Retrying in %ds...",
                attempt + 1, max_retries, model_name, str(e)[:200], wait,
            )
            if attempt < max_retries - 1:
                time.sleep(wait)
            else:
                logger.error("All retries exhausted for %s", model_name)
                return None


# ---------------------------------------------------------------------------
# Main evaluation loop
# ---------------------------------------------------------------------------

def get_answer_path(model_name, trial_id):
    model_dir = os.path.join(RESULTS_DIR, model_name)
    os.makedirs(model_dir, exist_ok=True)
    return os.path.join(model_dir, f"trial{trial_id}_answers.json")


def run_single_trial(model_name, trial_id, delay=2, resume=True):
    """Run inference for a single trial. Returns True if successful."""
    answer_path = get_answer_path(model_name, trial_id)
    if resume and os.path.exists(answer_path):
        # Check that existing file has valid answers
        try:
            with open(answer_path, encoding="UTF-8") as f:
                existing = json.load(f)
            if validate_answers(existing):
                return True  # Already done with valid answers
            else:
                logger.info("Trial %d [%s]: existing file has no valid answers, re-running", trial_id, model_name)
                os.remove(answer_path)
        except (json.JSONDecodeError, OSError):
            logger.info("Trial %d [%s]: existing file is corrupt, re-running", trial_id, model_name)
            os.remove(answer_path)

    # Check trial data exists
    story_path = os.path.join(DATA_DIR, f"trial{trial_id}", "story.json")
    question_path = os.path.join(DATA_DIR, f"trial{trial_id}", "question_new.json")
    if not os.path.exists(story_path) or not os.path.exists(question_path):
        logger.warning("Trial %d missing data files, skipping", trial_id)
        return False

    system_msg, user_msg = construct_prompt(trial_id, information_type="level1")
    raw_response = call_model(model_name, system_msg, user_msg, delay=delay)

    if raw_response is None:
        logger.warning("Trial %d [%s]: no response after retries, skipping", trial_id, model_name)
        return False

    answers = parse_json_response(raw_response)

    if not validate_answers(answers):
        answered = sum(1 for v in answers.values() if v and str(v).strip())
        logger.warning(
            "Trial %d [%s]: only %d/71 valid answers, not saving",
            trial_id, model_name, answered,
        )
        return False

    logger.info(
        "Trial %d [%s]: %d/%d questions answered",
        trial_id, model_name, len(answers), 71,
    )

    with open(answer_path, "w", encoding="UTF-8") as f:
        json.dump(answers, f, indent=2)

    return True


def main():
    parser = argparse.ArgumentParser(description="Run DynToM evaluation")
    parser.add_argument("--model", required=True, help="Model name or 'all'")
    parser.add_argument("--start", type=int, default=50, help="Start trial ID (inclusive)")
    parser.add_argument("--end", type=int, default=1150, help="End trial ID (exclusive)")
    parser.add_argument("--delay", type=float, default=2, help="Seconds between API calls (rate limiting)")
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True,
                        help="Resume from previous runs, skipping completed trials (default: True)")
    args = parser.parse_args()

    os.makedirs(RESULTS_DIR, exist_ok=True)

    if args.model == "all":
        model_names = list(MODELS.keys())
    else:
        if args.model not in MODELS:
            print(f"Unknown model: {args.model}")
            print(f"Available: {', '.join(MODELS.keys())}")
            return
        model_names = [args.model]

    trial_ids = list(range(args.start, args.end))

    for model_name in model_names:
        logger.info("=== Starting evaluation for %s ===", model_name)
        # Filter to trials that actually exist
        valid_trials = [
            t for t in trial_ids
            if os.path.exists(os.path.join(DATA_DIR, f"trial{t}", "question_new.json"))
        ]
        logger.info("Found %d valid trials in range %d-%d", len(valid_trials), args.start, args.end)

        for trial_id in tqdm(valid_trials, desc=model_name):
            run_single_trial(model_name, trial_id, delay=args.delay, resume=args.resume)

        logger.info("=== Finished %s ===", model_name)


if __name__ == "__main__":
    main()
