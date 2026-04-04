"""
DynToM Results Analyzer

Computes accuracy and Table 3 breakdown from stored answer files.
Question-to-mental-state mappings replicate analysis/analysis_question.py (commit 8e435482).

Usage:
    python eval/analyze.py --model gpt-4-turbo
    python eval/analyze.py --model all
"""

import argparse
import json
import os

from config import DATA_DIR, RESULTS_DIR, MODELS

# ---------------------------------------------------------------------------
# Question-to-category mappings (from analysis/analysis_question.py)
# ---------------------------------------------------------------------------

# Understanding (U) questions per mental state
U_QUESTIONS = {
    "belief": [f"type_a_what_{i}" for i in range(1, 6)],
    "emotion": [f"type_a_what_{i}" for i in range(6, 11)],
    "intention": [f"type_a_what_{i}" for i in range(11, 16)],
    "action": [f"type_a_what_{i}" for i in range(16, 21)],
}

# Transformation (T) questions per mental state (type_d_why + type_d_whether)
T_QUESTIONS = {
    "belief": (
        [f"type_d_why_{i}" for i in range(1, 5)]
        + [f"type_d_whether_{i}" for i in range(1, 5)]
    ),
    "emotion": (
        [f"type_d_why_{i}" for i in range(5, 9)]
        + [f"type_d_whether_{i}" for i in range(5, 9)]
    ),
    "intention": (
        [f"type_d_why_{i}" for i in range(9, 13)]
        + [f"type_d_whether_{i}" for i in range(9, 13)]
    ),
    "action": (
        [f"type_d_why_{i}" for i in range(13, 17)]
        + [f"type_d_whether_{i}" for i in range(13, 17)]
    ),
}

# All question IDs (71 per trial)
ALL_U = []
for qs in U_QUESTIONS.values():
    ALL_U.extend(qs)

ALL_T_PER_STATE = []
for qs in T_QUESTIONS.values():
    ALL_T_PER_STATE.extend(qs)

# type_c and type_d_how questions (included in AVG but not in per-state U/T)
TYPE_C = [f"type_c_how_{i}" for i in range(1, 16)]
TYPE_D_HOW = [f"type_d_how_{i}" for i in range(1, 5)]


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def load_trial_results(model_name, trial_id):
    """Load model answers and ground truth for a trial.

    Returns (answers_dict, truth_dict) or (None, None) if files missing.
    """
    answer_path = os.path.join(RESULTS_DIR, model_name, f"trial{trial_id}_answers.json")
    truth_path = os.path.join(DATA_DIR, f"trial{trial_id}", "question_new.json")

    if not os.path.exists(answer_path) or not os.path.exists(truth_path):
        return None, None

    with open(answer_path, encoding="UTF-8") as f:
        answers = json.load(f)
    with open(truth_path, encoding="UTF-8") as f:
        truth = json.load(f)

    if "questions" in truth:
        truth = truth["questions"]

    return answers, truth


def compute_accuracy(answers, truth, question_ids):
    """Compute accuracy for a subset of question IDs.

    Only counts questions where the model provided a non-empty answer.
    Returns (correct_count, total_count).
    """
    correct = 0
    total = 0
    for q_id in question_ids:
        if q_id not in truth:
            continue
        model_answer = answers.get(q_id, "")
        # Skip questions with no answer provided
        if not model_answer or not str(model_answer).strip():
            continue
        total += 1
        true_answer = truth[q_id]["true answer"]
        if model_answer == true_answer:
            correct += 1
    return correct, total


def analyze_model(model_name, start=50, end=1150):
    """Compute Table 3 breakdown for a model across all trials.

    Returns a dict with per-category accuracy.
    """
    # Accumulators: {category: [correct, total]}
    categories = {}
    for state in ["belief", "emotion", "intention", "action"]:
        categories[f"{state}_U"] = [0, 0]
        categories[f"{state}_T"] = [0, 0]
    categories["all"] = [0, 0]

    context_count = 0
    trial_ids = range(start, end)

    for trial_id in trial_ids:
        answers, truth = load_trial_results(model_name, trial_id)
        if answers is None:
            continue

        context_count += 1

        # Per-state U and T
        for state in ["belief", "emotion", "intention", "action"]:
            c, t = compute_accuracy(answers, truth, U_QUESTIONS[state])
            categories[f"{state}_U"][0] += c
            categories[f"{state}_U"][1] += t

            c, t = compute_accuracy(answers, truth, T_QUESTIONS[state])
            categories[f"{state}_T"][0] += c
            categories[f"{state}_T"][1] += t

        # Overall (all 71 questions)
        all_q_ids = list(truth.keys())
        c, t = compute_accuracy(answers, truth, all_q_ids)
        categories["all"][0] += c
        categories["all"][1] += t

    # Compute percentages
    results = {"context_count": context_count}
    for cat, (correct, total) in categories.items():
        if total > 0:
            results[cat] = round(100.0 * correct / total, 1)
        else:
            results[cat] = 0.0
        results[f"{cat}_correct"] = correct
        results[f"{cat}_total"] = total

    return results


def load_contamination_results():
    """Load CoDeC contamination results if available."""
    path = os.path.join(RESULTS_DIR, "contamination.json")
    if os.path.exists(path):
        with open(path, encoding="UTF-8") as f:
            return json.load(f)
    return {}


def format_table(all_results):
    """Format results as a markdown table matching Table 3 from the paper."""
    contamination = load_contamination_results()

    header = (
        "| Model | Contexts | Belief U | Belief T | Emotion U | Emotion T | "
        "Intention U | Intention T | Action U | Action T | AVG | CoDeC |"
    )
    sep = "|" + "|".join(["---"] * 12) + "|"

    # Paper reference values
    paper_ref = {
        "Human": "1100 | 83.8 | 77.6 | 89.5 | 78.7 | 79.0 | 73.8 | 76.7 | 76.3 | 77.7 | -",
        "GPT-4o (paper)": "1100 | 80.9 | 44.5 | 91.7 | 45.8 | 87.5 | 51.9 | 95.1 | 55.6 | 64.0 | -",
        "GPT-4-Turbo (paper)": "1100 | 63.5 | 32.3 | 74.7 | 33.9 | 71.3 | 35.5 | 80.5 | 36.2 | 47.6 | -",
    }

    lines = [header, sep]
    for name, vals in paper_ref.items():
        lines.append(f"| {name} | {vals} |")

    lines.append(sep)

    for model_name, results in all_results.items():
        codec = contamination.get(model_name, {})
        codec_str = f"{codec['codec_score']}" if "codec_score" in codec else "-"

        row = (
            f"| {model_name} "
            f"| {results['context_count']} "
            f"| {results['belief_U']} | {results['belief_T']} "
            f"| {results['emotion_U']} | {results['emotion_T']} "
            f"| {results['intention_U']} | {results['intention_T']} "
            f"| {results['action_U']} | {results['action_T']} "
            f"| {results['all']} | {codec_str} |"
        )
        lines.append(row)
        if model_name == "gpt-4-turbo":
            lines.append(sep)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze DynToM evaluation results")
    parser.add_argument("--model", required=True, help="Model name or 'all'")
    parser.add_argument("--start", type=int, default=50)
    parser.add_argument("--end", type=int, default=1150)
    parser.add_argument("--output", default=None, help="Output JSON path")
    args = parser.parse_args()

    if args.model == "all":
        model_names = list(MODELS.keys())
    else:
        model_names = [args.model]

    all_results = {}
    for model_name in model_names:
        results = analyze_model(model_name, args.start, args.end)
        all_results[model_name] = results
        print(f"\n--- {model_name} ({results['context_count']} contexts) ---")
        print(f"  Belief    U: {results['belief_U']}%  T: {results['belief_T']}%")
        print(f"  Emotion   U: {results['emotion_U']}%  T: {results['emotion_T']}%")
        print(f"  Intention U: {results['intention_U']}%  T: {results['intention_T']}%")
        print(f"  Action    U: {results['action_U']}%  T: {results['action_T']}%")
        print(f"  AVG: {results['all']}%")

    print("\n\n=== Table 3 Comparison ===\n")
    print(format_table(all_results))

    if args.output:
        with open(args.output, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
