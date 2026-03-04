"""
AlignED Report 4 — Analysis
Reads scored outputs and produces summary statistics and JSON data
files for the report charts.

Usage: python analyse.py
"""

import json
from pathlib import Path
from collections import defaultdict

SCORES_DIR = Path("data")
OUTPUT_DIR = Path("outputs")


def load_scores():
    """Load the scored results."""
    with open(SCORES_DIR / "scores.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_outputs():
    """Load the raw model outputs for qualitative display."""
    with open(OUTPUT_DIR / "all_results.json", "r", encoding="utf-8") as f:
        return json.load(f)


def analyse():
    """
    Run all analyses and save chart-ready JSON data.
    """
    scores = load_scores()
    outputs = load_outputs()

    # Filter out any error scores
    valid_scores = [s for s in scores if s["output_score"] >= 0]

    # --- Analysis 1: Condition effect ---
    # Mean output score by condition across all models
    condition_scores = defaultdict(list)
    for s in valid_scores:
        condition_scores[s["condition"]].append(s["output_score"])

    condition_means = {}
    for condition, score_list in condition_scores.items():
        condition_means[condition] = {
            "mean": round(sum(score_list) / len(score_list), 2),
            "scores": score_list,
            "n": len(score_list)
        }

    # --- Analysis 2: Model x Condition breakdown ---
    model_condition = defaultdict(lambda: defaultdict(list))
    for s in valid_scores:
        model_condition[s["model_name"]][s["condition"]].append(s["output_score"])

    model_condition_summary = {}
    for model, conditions in model_condition.items():
        model_condition_summary[model] = {}
        for condition, score_list in conditions.items():
            model_condition_summary[model][condition] = {
                "mean": round(sum(score_list) / len(score_list), 2),
                "scores": score_list
            }

    # --- Analysis 3: Output-Trace concordance ---
    concordance = {"high_high": 0, "high_low": 0, "low_high": 0, "low_low": 0}
    for s in valid_scores:
        trace = s["trace_score"]
        if not isinstance(trace, (int, float)) or trace < 0:
            continue
        output_high = s["output_score"] >= 2
        trace_high = trace >= 1
        if output_high and trace_high:
            concordance["high_high"] += 1
        elif output_high and not trace_high:
            concordance["high_low"] += 1
        elif not output_high and trace_high:
            concordance["low_high"] += 1
        else:
            concordance["low_low"] += 1

    # --- Analysis 4: Trace scores by condition ---
    trace_by_condition = defaultdict(list)
    for s in valid_scores:
        trace = s["trace_score"]
        if isinstance(trace, (int, float)) and trace >= 0:
            trace_by_condition[s["condition"]].append(trace)

    trace_means = {}
    for condition, score_list in trace_by_condition.items():
        trace_means[condition] = {
            "mean": round(sum(score_list) / len(score_list), 2),
            "scores": score_list,
            "n": len(score_list)
        }

    # --- Compile chart-ready data ---
    chart_data = {
        "metadata": {
            "report": "AlignED Report 4",
            "task": "Worked example fading (two-step linear equations)",
            "models": list(model_condition.keys()),
            "conditions": ["A_unprompted", "B_general_clt", "C_specific_fading"],
            "n_per_cell": 1,
            "temperature": "N/A for all models (incompatible with thinking/reasoning modes)",
        },
        "condition_effect": condition_means,
        "model_condition": model_condition_summary,
        "concordance": concordance,
        "trace_by_condition": trace_means,
        "raw_scores": valid_scores,
    }

    # Save
    with open(SCORES_DIR / "analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(chart_data, f, indent=2, ensure_ascii=False)

    # --- Print summary ---
    print("=" * 60)
    print("AlignED Report 4 — Analysis Summary")
    print("=" * 60)

    print("\n--- Analysis 1: Condition Effect (mean output score) ---\n")
    for condition in ["A_unprompted", "B_general_clt", "C_specific_fading"]:
        if condition in condition_means:
            data = condition_means[condition]
            print(f"  {condition}: {data['mean']:.2f} (n={data['n']}, scores={data['scores']})")

    print("\n--- Analysis 2: Model x Condition ---\n")
    for model, conditions in model_condition_summary.items():
        print(f"  {model}:")
        for condition in ["A_unprompted", "B_general_clt", "C_specific_fading"]:
            if condition in conditions:
                data = conditions[condition]
                print(f"    {condition}: {data['mean']:.2f} (scores={data['scores']})")

    print("\n--- Analysis 3: Output-Trace Concordance ---\n")
    print(f"  Applied + Reasoned:     {concordance['high_high']}")
    print(f"  Applied + No reasoning: {concordance['high_low']}")
    print(f"  Not applied + Reasoned: {concordance['low_high']}")
    print(f"  Not applied + No reasoning: {concordance['low_low']}")

    print("\n--- Analysis 4: Trace Scores by Condition ---\n")
    for condition in ["A_unprompted", "B_general_clt", "C_specific_fading"]:
        if condition in trace_means:
            data = trace_means[condition]
            print(f"  {condition}: {data['mean']:.2f} (n={data['n']}, scores={data['scores']})")

    print(f"\nResults saved to {SCORES_DIR}/analysis_results.json")


if __name__ == "__main__":
    analyse()
