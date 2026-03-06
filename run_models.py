"""
AlignED Report 4 — Model Runner
Sends the 3 prompt conditions to 3 frontier models, captures outputs
and reasoning traces, saves results as JSON.

Usage: python run_models.py
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import openai
import requests
from dotenv import load_dotenv

from prompts import CONDITIONS

# Load API keys from .env
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Validate API keys at startup
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

# Output directory
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def call_claude(prompt, model_id="claude-opus-4-6"):
    """
    Call Claude Opus 4.6 with extended thinking enabled.
    Returns a dict with 'output' and 'trace' keys.

    Note: Thinking mode is incompatible with the temperature parameter.
    The API rejects the request if temperature is set alongside thinking.
    We use type="enabled" with an 8K token thinking budget.
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Extended thinking — temperature cannot be set when thinking is enabled
    response = client.messages.create(
        model=model_id,
        max_tokens=16000,
        thinking={
            "type": "enabled",
            "budget_tokens": 8000
        },
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract output text and thinking trace
    output_text = ""
    trace_text = ""
    for block in response.content:
        if block.type == "thinking":
            trace_text += block.thinking
        elif block.type == "text":
            output_text += block.text

    return {
        "output": output_text,
        "trace": trace_text,
        "model": model_id,
        "temperature": "N/A (incompatible with thinking mode)",
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }


def call_openai(prompt, model_id="gpt-5.2-pro"):
    """
    Call OpenAI GPT-5.2 Pro (frontier reasoning model).
    Returns a dict with 'output' and 'trace' keys.

    Note: GPT-5.2-pro supports extended thinking via reasoning_effort.
    Temperature is not supported when reasoning effort is set (only
    works with reasoning.effort = "none"). We omit temperature entirely.
    """
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # Reasoning models: temperature not supported with reasoning effort
    response = client.chat.completions.create(
        model=model_id,
        max_completion_tokens=16000,
        reasoning={"effort": "high"},
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract output and reasoning trace
    output_text = response.choices[0].message.content or ""
    trace_text = ""

    # Access reasoning tokens if available (check multiple possible fields)
    if hasattr(response.choices[0].message, "reasoning_content"):
        trace_text = response.choices[0].message.reasoning_content or ""
    elif hasattr(response.choices[0].message, "reasoning"):
        trace_text = response.choices[0].message.reasoning or ""

    if not trace_text:
        print("  -> WARNING: No reasoning trace found in OpenAI response")

    return {
        "output": output_text,
        "trace": trace_text,
        "model": model_id,
        "temperature": "N/A (not supported with reasoning effort)",
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
    }


def call_gemini(prompt, model_id="gemini-3.1-pro-preview"):
    """
    Call Gemini 3.1 Pro via REST API with thinking enabled.
    Returns a dict with 'output' and 'trace' keys.
    """
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model_id}:generateContent?key={GOOGLE_API_KEY}"
    )

    # includeThoughts: true is required to get thinking traces in the response
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 16000,
            "thinkingConfig": {
                "thinkingBudget": 8000,
                "includeThoughts": True
            }
        }
    }

    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    # Extract output and thinking trace from Gemini response
    output_text = ""
    trace_text = ""

    if "candidates" in data and len(data["candidates"]) > 0:
        parts = data["candidates"][0].get("content", {}).get("parts", [])
        for part in parts:
            if part.get("thought", False):
                # This is a thinking/reasoning part
                trace_text += part.get("text", "")
            elif "text" in part:
                # This is a regular output part
                output_text += part["text"]

    if not trace_text:
        print("  -> WARNING: No thinking trace found in Gemini response")

    # Token usage
    usage = data.get("usageMetadata", {})

    return {
        "output": output_text,
        "trace": trace_text,
        "model": model_id,
        "temperature": "N/A (omitted with thinkingConfig)",
        "input_tokens": usage.get("promptTokenCount", 0),
        "output_tokens": usage.get("candidatesTokenCount", 0),
    }


# Map of model names to their call functions
# OpenAI GPT-5.2 Pro not available on this account — pilot runs with 2 models
MODELS = {
    "claude_opus_4_6": call_claude,
    "gemini_3_1_pro": call_gemini,
}


def run_all():
    """
    Run all 9 combinations (3 models x 3 conditions) and save results.
    Skips any model/condition pair that already has a saved output file.
    """
    results = []
    total_calls = len(MODELS) * len(CONDITIONS)
    call_num = 0

    for model_name, call_fn in MODELS.items():
        for condition_name, prompt in CONDITIONS.items():
            call_num += 1
            filename = f"{model_name}_{condition_name}.json"
            output_path = OUTPUT_DIR / filename

            # Skip if already completed
            if output_path.exists():
                print(f"[{call_num}/{total_calls}] {model_name} / {condition_name} -> SKIPPING (already exists)")
                with open(output_path, "r", encoding="utf-8") as f:
                    results.append(json.load(f))
                continue

            print(f"[{call_num}/{total_calls}] {model_name} / {condition_name}...")

            try:
                result = call_fn(prompt)
                result["condition"] = condition_name
                result["model_name"] = model_name
                result["timestamp"] = datetime.now(timezone.utc).isoformat()
                result["status"] = "success"
                results.append(result)

                # Save individual result immediately (crash-safe)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"  -> OK ({result['output_tokens']} output tokens)")

            except Exception as e:
                error_result = {
                    "model_name": model_name,
                    "condition": condition_name,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "error",
                    "error": str(e),
                    "output": "",
                    "trace": "",
                }
                results.append(error_result)
                print(f"  -> ERROR: {e}")

            # Brief pause between calls to avoid rate limits
            time.sleep(2)

    # Save combined results
    with open(OUTPUT_DIR / "all_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(results)} results saved to {OUTPUT_DIR}/")

    # Summary
    successes = sum(1 for r in results if r["status"] == "success")
    errors = sum(1 for r in results if r["status"] == "error")
    print(f"Successes: {successes}, Errors: {errors}")


if __name__ == "__main__":
    run_all()
