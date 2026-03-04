# AlignED Report 4 — Methodological Plan (Pilot Study)

## Do LLMs Apply the Worked Example Fading Effect? A Pilot Study

### Research Question

When asked to create worked examples for a common educational task, do frontier LLMs apply the fading effect from cognitive load theory — and do they reason about it in their chain of thought?

### Framing

This is a pilot study testing a single CLT principle (fading) across three frontier models. It tests whether a methodology based on examining both outputs and reasoning traces can reveal how models reason about pedagogical theory. The findings will inform whether a larger multi-principle study is warranted.

### Why Fading?

"Create worked examples for [topic]" is one of the most natural ways teachers use LLMs for instructional design. The worked example fading effect — progressively removing solution steps so learners take over the problem-solving process — is well-established in CLT research. If models produce four fully worked examples when best practice says they should fade, that has direct implications for how teachers use AI-generated materials.

---

## 1. Study Design

### Overview

- **1 task**: Create a set of worked examples (fading principle)
- **3 conditions**: unprompted, general CLT, specific principle named
- **3 models** with accessible reasoning traces
- **1 run** per condition × model (pilot)
- **Temperature**: N/A for all three models (incompatible with thinking/reasoning modes)
- **Total: 9 API calls** (plus 9 scoring calls)

### Models

| Model | Provider | Reasoning trace | Access |
|-------|----------|----------------|--------|
| Claude Opus 4.6 | Anthropic | Extended thinking (enabled, 8K budget) | Anthropic API |
| GPT-5.2 Pro | OpenAI | Reasoning tokens (effort: high) | OpenAI API |
| Gemini 3.1 Pro | Google | Thinking traces (8K budget) | Google AI API |

### What We Measure

Each response is scored on two dimensions:

1. **Output structure** (0–2): Did the model produce a fading sequence?
2. **Reasoning trace content** (0–2): Did the chain of thought reference fading or its underlying logic?

---

## 2. Prompts

### The CLT Principle Being Tested

The worked example fading effect holds that instructional sequences should begin with fully worked examples, then progressively remove solution steps until the learner solves problems independently. This is distinct from simply increasing difficulty — fading means removing scaffolding, not making equations harder.

### Condition A (Unprompted)

> You are an experienced mathematics teacher. Create a set of 4 worked examples teaching Year 8 students how to solve two-step linear equations (e.g., 3x + 5 = 20). Each worked example should present a problem and its full worked solution.

### Condition B (General CLT)

> You are an experienced mathematics teacher. Create a set of 4 worked examples teaching Year 8 students how to solve two-step linear equations (e.g., 3x + 5 = 20). Each worked example should present a problem and its full worked solution. Apply cognitive load theory principles in your design.

### Condition C (Specific Principle)

> You are an experienced mathematics teacher. Create a set of 4 worked examples teaching Year 8 students how to solve two-step linear equations (e.g., 3x + 5 = 20). Apply the worked example fading effect from cognitive load theory: systematically remove solution steps across the sequence so that learners gradually take over more of the problem-solving process.

### Design Notes

**Why "full worked solution" in Condition A?** This is the natural phrasing a teacher would use. It creates a tension: the prompt asks for "full worked solutions" but CLT best practice says to fade. Does the model default to literal compliance or apply pedagogical judgement? This tension is the core of what we're testing.

**Why the role frame?** "You are an experienced mathematics teacher" is consistent across all conditions and reflects how teachers actually prompt models. It cannot explain between-condition differences.

---

## 3. Hypotheses

**H1 (Fading is rare unprompted):** In Condition A, models will produce four fully worked examples with no fading. The prompt asks for "full worked solutions," and models default to compliance. Expected: most or all models score 0.

**H2 (General CLT activates some fading):** In Condition B, some models will introduce a gradient (increasing difficulty, reduced explanation) but may not achieve true structural fading (removing solution steps). Expected rate: moderate.

**H3 (Specific principle produces fading):** In Condition C, most runs will produce a correctly faded sequence because the prompt defines the structure explicitly. The interesting variation is whether the fading is mechanically applied or whether the reasoning trace explains *why* each stage reduces support. Expected rate: high.

**H4 (Prompting gradient):** Output scores will follow the pattern C > B > A.

**H5 (Traces mirror outputs):** When models produce a faded sequence, their reasoning traces will more often reference fading or its logic than when they produce four complete examples.

**H6 (Difficulty ≠ fading):** Some Condition B responses will increase equation difficulty across examples without fading solution steps — conflating "harder problems" with "reduced scaffolding." This is the most common near-miss.

---

## 4. Scoring Rubric

### Dimension 1: Output Structure (0–2)

| Score | Label | Criteria |
|-------|-------|----------|
| 0 | Uniform | All four examples have the same structure — every solution step is fully completed by the model in all four examples. The examples may vary in difficulty but not in how much work the student does. |
| 1 | Some variation | There is some structural variation across examples — later examples may have shorter explanations, or slightly different formatting — but all solution steps are still completed by the model. No steps are left for the student to complete. |
| 2 | Progressive scaffolding removal | Solution steps are progressively removed across the set. At least one example is partially completed (some steps left blank, marked with "?", or explicitly left for the student), and the final example requires the student to complete most or all steps independently. |

### Key Scoring Distinctions

- **Difficulty increase alone = 0 or 1.** Harder equations with fully worked solutions is not fading.
- **Reduced explanation alone = 1.** Less narration ("Step 1: subtract 5") vs. more narration ("Step 1: To isolate x, we first subtract 5 from both sides") is a change in explanation depth, not fading.
- **Steps left for the student to complete = 2.** This is the defining feature. Fading means the learner takes over steps that were previously shown.

### Dimension 2: Reasoning Trace Reference (0–2)

| Score | Label | Criteria |
|-------|-------|----------|
| 0 | Absent | Trace does not reference fading, scaffolding removal, or the logic of gradually shifting work to the learner. |
| 1 | Implicit logic | Trace references the underlying logic without CLT terminology. Examples: "I'll make the last one have fewer steps shown so students try on their own," "gradually have them do more of the work," "reduce the support across examples." |
| 2 | Explicit reference | Trace explicitly names: fading, the worked example effect, the completion problem effect, cognitive load theory, or Sweller. |

### Scoring Process

- Each model's outputs are scored by a **different** model (to avoid self-scoring bias):
  - Claude outputs → scored by GPT-5.2 Pro
  - GPT-5.2 Pro outputs → scored by Gemini 3.1 Pro
  - Gemini outputs → scored by Claude Opus 4.6
- Pilot uses single scoring per output. A larger follow-up study would include inter-rater reliability checks.

---

## 5. Data Analysis Plan

### Data Structure

Each row: Model × Condition. Columns:
- `model_id`, `condition` (A/B/C)
- `output_score` (0–2), `trace_score` (0–2), `notes`

9 rows total (pilot — 1 run per cell).

### Analyses

**Analysis 1: Condition effect (central finding).**
Mean output score by condition, averaged across models. Present as a bar chart with three bars (A, B, C). This is the main figure.

**Analysis 2: Model × condition breakdown.**
A 3 × 3 table (models × conditions) showing output scores. One score per cell (pilot).

**Analysis 3: Output–trace concordance.**
For each of the 9 responses, plot output score against trace score. Look for:
- High output + high trace = reasoned and applied
- High output + low trace = applied without articulating why
- Low output + high trace = reasoned but didn't execute
- Low output + low trace = neither

**Analysis 4: The difficulty-vs-fading distinction.**
Of the responses scoring 0 or 1, how many increased equation difficulty without fading? This tests H6 and reveals the most common near-miss pattern.

### Reporting

No inferential statistics (n = 9 is too small). All findings are descriptive. All 9 outputs and traces published as supplementary data.

---

## 6. Interpretability Disclaimer

Chain-of-thought traces are generated text, not a direct window into model computation. A trace that references CLT may reflect patterns in training data rather than something analogous to human reasoning about pedagogy. We analyse traces as artefacts — evidence of what the model articulated during processing — not as claims about internal understanding.

This framing is analogous to analysing a teacher's written lesson plan rationale. We examine the reasoning they articulated and whether it aligns with the evidence base, without claiming to know everything that influenced their decisions.

---

## 7. Limitations

**L1: One task, one principle.** This pilot tests fading only. Performance on fading does not generalise to CLT knowledge broadly. A follow-up study with multiple principles would be needed.

**L2: Three models is a small sample.** Findings describe these three models at this point in time, not LLMs in general.

**L3: The prompt asks for "full worked solutions."** This creates a deliberate tension with fading but may suppress fading even in models that "know" the principle. A model that complies literally with the prompt instruction is not necessarily ignorant of fading — it may be prioritising instruction-following over pedagogical judgement. This is noted as an interpretation consideration, not a flaw: the tension is part of what we are testing.

**L4: Single-turn only.** A teacher might follow up with "can you make these progressively harder?" or "can you fade the scaffolding?" This study captures only the first-pass response.

**L5: No human baseline.** We don't know how human teachers or instructional designers would respond to these prompts. Without this, we cannot say whether model performance is good or poor in absolute terms.

**L6: No temperature control.** All three providers' thinking/reasoning modes are incompatible with temperature settings. Temperature is omitted for all calls, meaning outputs may vary across runs. This pilot prioritises access to reasoning traces over strict reproducibility.

**L7: LLM judges share training biases.** Cross-model scoring mitigates but does not eliminate this. The pilot framing acknowledges this as an open methodological question.

---

## 8. Practical Implementation

### API Calls

- 3 conditions × 3 models × 1 run = **9 calls**
- Scoring: 9 outputs scored by cross-model judges = **9 scoring calls**
- **Total: 18 API calls**

### Estimated Cost

| Component | Estimated cost |
|-----------|---------------|
| Model runs (9 calls with thinking) | $2–5 |
| LLM judge scoring (9 calls) | $1–3 |
| **Total** | **$3–8** |

### Timeline

| Phase | Time |
|-------|------|
| Pre-pilot (1 prompt × 3 models, verify trace capture) | 1–2 hours |
| Data collection (18 calls, automated) | 1–2 hours |
| Scoring (automated + review) | Half day |
| Analysis | Half day |
| Report (static HTML site) | 2–3 days |
| **Total** | **~4–5 days** |

### Implementation

Claude Code writes:
1. `prompts.py` — three prompt variants as constants
2. `run_models.py` — API calls to Anthropic, OpenAI, Google; captures output + reasoning traces; saves as JSON
3. `score_outputs.py` — cross-model LLM judge scoring with rubric
4. `analyse.py` — aggregates scores, outputs JSON for charts
5. Static HTML site following AlignED design system

### Pre-Pilot Checklist

- [ ] Verify API access to all three models
- [ ] Verify reasoning trace capture works for each provider
- [ ] Run Condition A once per model to check output format and confirm API configurations work
- [ ] Test LLM judge scoring on the 3 pre-pilot outputs to calibrate rubric

---

## 9. Report Structure

Following the AlignED series format:

1. **Abstract** — Pilot study, three frontier models, one CLT principle, key finding
2. **Introduction** — Teachers use LLMs to create worked examples; CLT says those examples should fade; do models know this?
3. **Methods** — This document condensed; full prompts in appendices
4. **Results** — Condition effect chart, model × condition table, concordance plot, example outputs
5. **Discussion** — What the pilot found, implications for teacher AI use, what a larger study should test
6. **Appendices** — All three prompts, scoring rubric, raw outputs and traces, scoring data

### Potential Title Options

- "Do LLMs Fade Worked Examples? A Pilot Study of Pedagogical Reasoning in AI"
- "Cognitive Load Theory and LLM Instructional Design: A Pilot Study of the Fading Effect"
- "When Teachers Ask AI for Worked Examples: Do Models Apply the Fading Effect?"
