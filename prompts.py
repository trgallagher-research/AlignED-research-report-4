"""
AlignED Report 4 — Prompt Definitions
Pilot study: Do LLMs apply the worked example fading effect?

Three conditions (A, B, C) testing whether frontier models apply
the fading effect from cognitive load theory when asked to create
worked examples for two-step linear equations.
"""

# Condition A: Unprompted (no mention of CLT)
# Note: "set" used instead of "sequence" to avoid priming CLT associations
# ("worked example sequence" is a CLT term of art).
CONDITION_A = (
    "You are an experienced mathematics teacher. Create a set of "
    "4 worked examples teaching Year 8 students how to solve two-step "
    "linear equations (e.g., 3x + 5 = 20). Each worked example should "
    "present a problem and its full worked solution."
)

# Condition B: General CLT (mentions CLT but not fading specifically)
CONDITION_B = (
    "You are an experienced mathematics teacher. Create a set of "
    "4 worked examples teaching Year 8 students how to solve two-step "
    "linear equations (e.g., 3x + 5 = 20). Each worked example should "
    "present a problem and its full worked solution. Apply cognitive "
    "load theory principles in your design."
)

# Condition C: Specific principle (names and defines fading)
CONDITION_C = (
    "You are an experienced mathematics teacher. Create a set of "
    "4 worked examples teaching Year 8 students how to solve two-step "
    "linear equations (e.g., 3x + 5 = 20). Apply the worked example "
    "fading effect from cognitive load theory: systematically remove "
    "solution steps across the sequence so that learners gradually "
    "take over more of the problem-solving process."
)

# All conditions in a list for iteration
CONDITIONS = {
    "A_unprompted": CONDITION_A,
    "B_general_clt": CONDITION_B,
    "C_specific_fading": CONDITION_C,
}

# Scoring rubric prompt for LLM-as-judge
# NOTE: The task context is deliberately neutral — it describes the task
# without naming what we are looking for. The scoring criteria define the
# scale; the judge must determine which level matches the output.
SCORING_RUBRIC = """You are scoring a model's response to an educational design task.

## Task context
The model was asked to create a set of 4 worked examples teaching Year 8 students to solve two-step linear equations.

## The model's output
{output}

## The model's reasoning trace (chain of thought)
{trace}

## Score the response on two dimensions.

### Dimension 1: Output Structure (0-2)

Score the structural design of the worked example set:

- **0 (Uniform):** All four examples have the same structure — every solution step is fully completed by the model in all four examples. The examples may vary in difficulty but not in how much work the student does.
- **1 (Some variation):** There is some structural variation across examples — later examples may have shorter explanations, or slightly different formatting — but all solution steps are still completed by the model. No steps are left for the student to complete.
- **2 (Progressive scaffolding removal):** Solution steps are progressively removed across the set. At least one example is partially completed (some steps left blank, marked with "?", or explicitly left for the student), and the final example requires the student to complete most or all steps independently.

Key distinctions:
- Harder equations with all steps shown = 0 or 1, not scaffolding removal.
- Less narration but all steps present = 1, not scaffolding removal.
- Steps left for the student to complete = 2.

### Dimension 2: Reasoning Trace Content (0-2)

Score what the model's reasoning trace discusses about instructional design:

- **0 (No design reasoning):** The trace does not discuss how the examples should be structured for learning purposes, or only discusses surface choices (which equations to pick, formatting).
- **1 (Informal design logic):** The trace discusses structuring the examples for learning without using formal terminology. Examples: "I should have them do more of the work in later ones," "gradually reduce the support," "let the student try the last steps."
- **2 (Formal pedagogical reference):** The trace explicitly references a named pedagogical theory, principle, or researcher related to instructional design of worked examples.

If no reasoning trace is available, score Dimension 2 as "N/A".

## Output format
Respond with ONLY a JSON object:
{{"output_score": <0-2>, "trace_score": <0-2 or "N/A">, "output_reasoning": "<brief explanation for output score>", "trace_reasoning": "<brief explanation for trace score>"}}
"""
