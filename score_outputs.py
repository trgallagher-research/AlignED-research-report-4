"""
AlignED Report 4 — Scoring Pipeline
Uses cross-model LLM-as-judge scoring:
  - Claude outputs scored by GPT-5.2 Pro
  - OpenAI outputs scored by Gemini 3.1 Pro
  - Gemini outputs scored by Claude Opus 4.6

Each output is scored on two dimensions:
  1. Output Structure (0-2): Did the model remove scaffolding?
  2. Reasoning Trace Content (0-2): Did the trace discuss design logic?

Usage: python score_outputs.py
"""

import json
import os
import sys
from pathlib import Path

import anthropic
import openai
import requests
from dotenv import load_dotenv

from prompts import SCORING_RUBRIC

# Load API keys
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Validate keys
missing_keys = []
if not ANTHROPIC_API_KEY:
    missing_keys.append("ANTHROPIC_API_KEY")
if not OPENAI_API_KEY:
    missing_keys.append("OPENAI_API_KEY")
if not GOOGLE_API_KEY:
    missing_keys.append("GOOGLE_API_KEY")
if missing_keys:
    print(f"ERROR: Missing API keys in .env: {', '.join(missing_keys)}")
    sys.exit(1)

OUTPUT_DIR = Path("outputs")
SCORES_DIR = Path("data")
SCORES_DIR.mkdir(exist_ok=True)

# Cross-model judge assignments (no model scores its own output)
JUDGE_ASSIGNMENTS = {
    "claude_opus_4_6": "openai_gpt_5_2_pro",    # Claude scored by GPT-5.2 Pro
    "openai_gpt_5_2_pro": "gemini_3_1_pro",     # OpenAI scored by Gemini
    "gemini_3_1_pro": "claude_opus_4_6",         # Gemini scored by Claude
}


def call_judge_claude(prompt):
    """Call Claude as a judge (no thinking needed for scoring)."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1000,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def call_judge_openai(prompt):
    """Call GPT-5.2 Pro as a judge (no reasoning needed for scoring)."""
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-5.2-pro",
        max_completion_tokens=1000,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def call_judge_gemini(prompt):
    """Call Gemini 3.1 Pro as a judge."""
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-3.1-pro-preview:generateContent"
        f"?key={GOOGLE_API_KEY}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0, "maxOutputTokens": 1000}
    }
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    # Safely extract text from response
    candidates = data.get("candidates", [])
    if not candidates:
        return "(empty response from Gemini judge)"
    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts:
        return "(no parts in Gemini judge response)"
    return parts[0].get("text", "(no text in Gemini judge response)")


# Map judge model names to their call functions
JUDGE_FUNCTIONS = {
    "claude_opus_4_6": call_judge_claude,
    "openai_gpt_5_2_pro": call_judge_openai,
    "gemini_3_1_pro": call_judge_gemini,
}


def parse_judge_response(judge_response):
    """
    Parse JSON from judge response, handling markdown code blocks
    and other formatting quirks.
    """
    json_text = judge_response.strip()

    # Handle markdown code blocks
    if "```" in json_text:
        # Extract content between first pair of backticks
        parts = json_text.split("```")
        if len(parts) >= 2:
            json_text = parts[1]
            # Remove optional language label (e.g., "json")
            if json_text.startswith("json"):
                json_text = json_text[4:]
            json_text = json_text.strip()

    # Try to find JSON object if there's surrounding text
    if not json_text.startswith("{"):
        start = json_text.find("{")
        end = json_text.rfind("}") + 1
        if start >= 0 and end > start:
            json_text = json_text[start:end]

    return json.loads(json_text)


def score_single_output(result):
    """
    Score a single model output using the assigned cross-model judge.
    Returns a dict with scores and judge info.
    """
    model_name = result["model_name"]
    judge_name = JUDGE_ASSIGNMENTS[model_name]
    judge_fn = JUDGE_FUNCTIONS[judge_name]

    # Build the scoring prompt
    trace_text = result.get("trace", "")
    if not trace_text:
        trace_text = "(No reasoning trace available)"

    scoring_prompt = SCORING_RUBRIC.format(
        output=result["output"],
        trace=trace_text
    )

    # Call the judge
    judge_response = judge_fn(scoring_prompt)

    # Parse the JSON response
    try:
        scores = parse_judge_response(judge_response)
    except (json.JSONDecodeError, IndexError, ValueError):
        scores = {
            "output_score": -1,
            "trace_score": -1,
            "output_reasoning": "PARSE_ERROR: " + judge_response[:500],
            "trace_reasoning": "PARSE_ERROR"
        }

    return {
        "model_name": model_name,
        "condition": result["condition"],
        "judge": judge_name,
        "output_score": scores.get("output_score", -1),
        "trace_score": scores.get("trace_score", -1),
        "output_reasoning": scores.get("output_reasoning", ""),
        "trace_reasoning": scores.get("trace_reasoning", ""),
        "raw_judge_response": judge_response,
    }


def score_all():
    """
    Score all outputs and save results.
    """
    # Load all results
    results_file = OUTPUT_DIR / "all_results.json"
    if not results_file.exists():
        print("No results found. Run run_models.py first.")
        return

    with open(results_file, "r", encoding="utf-8") as f:
        results = json.load(f)

    # Filter to successful results only
    results = [r for r in results if r.get("status") == "success"]
    print(f"Scoring {len(results)} outputs...\n")

    all_scores = []
    for i, result in enumerate(results):
        model = result["model_name"]
        condition = result["condition"]
        judge = JUDGE_ASSIGNMENTS[model]
        print(f"[{i+1}/{len(results)}] Scoring {model} / {condition} (judge: {judge})...")

        try:
            score = score_single_output(result)
            all_scores.append(score)
            print(f"  -> Output: {score['output_score']}, Trace: {score['trace_score']}")
        except Exception as e:
            print(f"  -> ERROR: {e}")
            all_scores.append({
                "model_name": model,
                "condition": condition,
                "judge": judge,
                "output_score": -1,
                "trace_score": -1,
                "output_reasoning": f"ERROR: {e}",
                "trace_reasoning": f"ERROR: {e}",
                "raw_judge_response": "",
            })

    # Save scores
    with open(SCORES_DIR / "scores.json", "w", encoding="utf-8") as f:
        json.dump(all_scores, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(all_scores)} scores saved to {SCORES_DIR}/scores.json")

    # Print summary table
    print("\n--- RESULTS SUMMARY ---\n")
    print(f"{'Model':<25} {'Condition':<20} {'Output':>8} {'Trace':>8}")
    print("-" * 65)
    for s in all_scores:
        print(f"{s['model_name']:<25} {s['condition']:<20} {s['output_score']:>8} {s['trace_score']:>8}")


if __name__ == "__main__":
    score_all()
