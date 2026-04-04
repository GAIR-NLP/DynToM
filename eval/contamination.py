"""
DynToM Data Contamination Detection

Adapted CoDeC (Contamination Detection via Context) for API-based LLMs.
Compares model accuracy on DynToM questions with and without in-context
examples from other DynToM trials. If accuracy drops with context, it
suggests the model may have memorized the benchmark data.

Reference: Zawalski et al., "Detecting Data Contamination in LLMs via
In-Context Learning" (arXiv:2510.27055)

Usage:
    python contamination.py --model gpt-5.4 --num-samples 50
    python contamination.py --model all --num-samples 30
"""

import argparse
import json
import logging
import os
import random

import numpy as np
from tqdm import tqdm

from config import DATA_DIR, RESULTS_DIR, MODELS, REQUIRE_PROMPT
from run_eval import construct_prompt, call_model, parse_json_response, validate_answers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(RESULTS_DIR, "contamination.log")),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

CONTAMINATION_FILE = os.path.join(RESULTS_DIR, "contamination.json")


def load_ground_truth(trial_id):
    """Load ground truth answers for a trial."""
    path = os.path.join(DATA_DIR, f"trial{trial_id}", "question_new.json")
    with open(path, encoding="UTF-8") as f:
        truth = json.load(f)
    if "questions" in truth:
        truth = truth["questions"]
    return truth


def trial_accuracy(answers, truth):
    """Compute accuracy for a single trial (only counting answered questions)."""
    if not answers:
        return None
    answered = 0
    correct = 0
    for q_id in truth:
        model_answer = answers.get(q_id, "")
        if not model_answer or not str(model_answer).strip():
            continue
        answered += 1
        if model_answer == truth[q_id]["true answer"]:
            correct += 1
    if answered == 0:
        return None
    return correct / answered


def construct_context_example(trial_id):
    """Build an in-context demonstration from a trial's data.

    Returns the example text with story, questions, and correct answers.
    """
    story_path = os.path.join(DATA_DIR, f"trial{trial_id}", "story.json")
    question_path = os.path.join(DATA_DIR, f"trial{trial_id}", "question_new.json")

    with open(story_path, encoding="UTF-8") as f:
        script = json.load(f)
    with open(question_path, encoding="UTF-8") as f:
        questions = json.load(f)

    if "questions" in questions:
        questions = questions["questions"]

    story = script["story"]
    for key, value in story.items():
        value.pop("background", None)

    questions_stripped = {}
    for q_id, q_data in questions.items():
        questions_stripped[q_id] = {
            "question": q_data["question"],
            "options": q_data["options"],
        }

    correct_answers = {q_id: q["true answer"] for q_id, q in questions.items()}
    characters = script["characters information"]

    example = (
        f"Example:\n"
        f"{characters}\n{story}\n{questions_stripped}\n"
        f"Correct answers: {json.dumps(correct_answers)}"
    )
    return example


def run_codec_trial(model_name, trial_id, context_trial_id, delay=3, use_cached=True):
    """Run baseline and context inference for a single trial.

    If use_cached is True and a cached answer file exists for the baseline,
    reuse it instead of calling the API again.

    Returns dict with baseline/context accuracies and delta, or None on failure.
    """
    truth = load_ground_truth(trial_id)

    # --- Baseline ---
    cached_path = os.path.join(RESULTS_DIR, model_name, f"trial{trial_id}_answers.json")
    baseline_answers = None

    if use_cached and os.path.exists(cached_path):
        try:
            with open(cached_path, encoding="UTF-8") as f:
                baseline_answers = json.load(f)
            if not validate_answers(baseline_answers):
                baseline_answers = None
        except (json.JSONDecodeError, OSError):
            baseline_answers = None

    if baseline_answers is None:
        system_msg, user_msg = construct_prompt(trial_id)
        raw = call_model(model_name, system_msg, user_msg, delay=delay)
        if raw is None:
            return None
        baseline_answers = parse_json_response(raw)
        if not validate_answers(baseline_answers):
            logger.warning("Trial %d [%s]: baseline had insufficient answers", trial_id, model_name)
            return None

    baseline_acc = trial_accuracy(baseline_answers, truth)
    if baseline_acc is None:
        return None

    # --- With context ---
    context_example = construct_context_example(context_trial_id)
    target_prompt, _ = construct_prompt(trial_id)
    augmented_system = f"{context_example}\n\nNow answer these questions:\n{target_prompt}"

    raw = call_model(model_name, augmented_system, REQUIRE_PROMPT, delay=delay)
    if raw is None:
        return None
    context_answers = parse_json_response(raw)
    if not validate_answers(context_answers):
        logger.warning("Trial %d [%s]: context run had insufficient answers", trial_id, model_name)
        return None

    context_acc = trial_accuracy(context_answers, truth)
    if context_acc is None:
        return None

    delta = context_acc - baseline_acc

    logger.info(
        "Trial %d [%s]: baseline=%.1f%%, context=%.1f%%, delta=%+.1f%%",
        trial_id, model_name, baseline_acc * 100, context_acc * 100, delta * 100,
    )

    return {
        "trial_id": trial_id,
        "context_trial_id": context_trial_id,
        "baseline_accuracy": round(baseline_acc, 4),
        "context_accuracy": round(context_acc, 4),
        "delta": round(delta, 4),
        "contaminated": delta < 0,
    }


def compute_codec_score(model_name, num_samples=50, delay=3, seed=42,
                        start=50, end=1150, use_cached=True):
    """Compute CoDeC contamination score for a model on DynToM.

    Returns dict with overall score and per-trial details.
    """
    random.seed(seed)

    trial_ids = [
        t for t in range(start, end)
        if os.path.exists(os.path.join(DATA_DIR, f"trial{t}", "question_new.json"))
    ]

    if not trial_ids:
        return None

    sampled = random.sample(trial_ids, min(num_samples, len(trial_ids)))

    results = []
    for trial_id in tqdm(sampled, desc=f"CoDeC {model_name}"):
        context_id = random.choice([t for t in trial_ids if t != trial_id])
        result = run_codec_trial(model_name, trial_id, context_id,
                                 delay=delay, use_cached=use_cached)
        if result is not None:
            results.append(result)

    if not results:
        return None

    contaminated = sum(1 for r in results if r["contaminated"])
    score = contaminated / len(results)

    return {
        "codec_score": round(score * 100, 1),
        "num_samples": len(results),
        "num_contaminated": contaminated,
        "avg_baseline_acc": round(np.mean([r["baseline_accuracy"] for r in results]) * 100, 1),
        "avg_context_acc": round(np.mean([r["context_accuracy"] for r in results]) * 100, 1),
        "avg_delta": round(np.mean([r["delta"] for r in results]) * 100, 1),
    }


def load_contamination_results():
    """Load previously saved contamination results."""
    if os.path.exists(CONTAMINATION_FILE):
        with open(CONTAMINATION_FILE, encoding="UTF-8") as f:
            return json.load(f)
    return {}


def save_contamination_results(all_results):
    """Save contamination results, merging with any existing data."""
    existing = load_contamination_results()
    existing.update(all_results)
    with open(CONTAMINATION_FILE, "w", encoding="UTF-8") as f:
        json.dump(existing, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="DynToM Contamination Detection (CoDeC)")
    parser.add_argument("--model", required=True, help="Model name or 'all'")
    parser.add_argument("--num-samples", type=int, default=50,
                        help="Number of trials to sample (default: 50)")
    parser.add_argument("--delay", type=float, default=3,
                        help="Seconds between API calls (default: 3)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--start", type=int, default=50)
    parser.add_argument("--end", type=int, default=1150)
    parser.add_argument("--no-cache", action="store_true",
                        help="Don't use cached baseline results")
    args = parser.parse_args()

    os.makedirs(RESULTS_DIR, exist_ok=True)

    if args.model == "all":
        model_names = list(MODELS.keys())
    else:
        if args.model not in MODELS:
            print(f"Unknown model: {args.model}. Available: {', '.join(MODELS.keys())}")
            return
        model_names = [args.model]

    all_results = {}
    for model_name in model_names:
        logger.info("=== CoDeC for %s ===", model_name)
        result = compute_codec_score(
            model_name,
            num_samples=args.num_samples,
            delay=args.delay,
            seed=args.seed,
            start=args.start,
            end=args.end,
            use_cached=not args.no_cache,
        )
        if result is None:
            print(f"\n{model_name}: FAILED (no successful trials)")
            continue

        all_results[model_name] = result
        print(f"\n{model_name}:")
        print(f"  CoDeC Score: {result['codec_score']}%")
        print(f"  Samples: {result['num_samples']}")
        print(f"  Contaminated: {result['num_contaminated']}")
        print(f"  Avg Baseline Accuracy: {result['avg_baseline_acc']}%")
        print(f"  Avg Context Accuracy: {result['avg_context_acc']}%")
        print(f"  Avg Delta: {result['avg_delta']}%")

    if all_results:
        save_contamination_results(all_results)
        print(f"\nResults saved to {CONTAMINATION_FILE}")


if __name__ == "__main__":
    main()
