# Reasoning Trace Analysis — AlignED Report 4 Pilot

## Overview

This document records what the reasoning traces (chain of thought) reveal
about how Claude Opus 4.6 and Gemini 3.1 Pro approach educational design
tasks across three prompting conditions.

---

## Condition A: Unprompted

### Claude Opus 4.6 — Trace

> "I need to create 4 worked examples for Year 8 students on solving
> two-step linear equations. I'll make them progressively more challenging
> and cover different variations, including positive and negative numbers,
> and different operations."

**What this tells us:** Claude's reasoning is purely about content coverage
and surface variation (positive/negative, different operations). There is
no design reasoning — no consideration of how much the student should do,
how to structure for learning, or any pedagogical framework. The model
treats this as a content generation task, not an instructional design task.

### Gemini 3.1 Pro — Trace

> "To cover a good range of examples, I'll vary the equations. Example one
> will be a straightforward addition and multiplication problem... Example
> three will include division... finally, to challenge them slightly and
> reinforce understanding that equations work both ways, Example four will
> involve... the variable on the right side."

**What this tells us:** Gemini's reasoning is also about content variety
and difficulty sequencing. It thinks about which equation types to include
for coverage, considers age-appropriate language, and plans formatting.
Like Claude, it treats this as curriculum coverage, not learning design.
The trace mentions "reinforce understanding" but in the sense of covering
different formats, not scaffolding removal.

### Condition A finding
Neither model spontaneously reasons about fading, scaffolding, or how
much work the student should do. Without prompting, the models frame
"worked examples" as "show the student how to do it" — not as an
instructional sequence designed to transfer responsibility.

---

## Condition B: General CLT

### Claude Opus 4.6 — Trace

> "Cognitive load theory principles relevant here:
> 1. Intrinsic load management — sequence from simple to complex
> 2. Extraneous load reduction — clear, consistent formatting
> 3. Germane load optimization — use consistent solution structure
> 4. Worked example effect — provide complete, step-by-step solutions
> 5. Element interactivity — start with low element interactivity"

**What this tells us:** Claude retrieves formal CLT terminology accurately.
It lists five distinct CLT constructs by name. Critically, it interprets
the "worked example effect" as providing *complete* solutions — which is
technically correct (the worked example effect says studying worked examples
is better than problem-solving for novices). But it does NOT retrieve the
fading effect. The model knows CLT well enough to cite sub-constructs but
selects the ones that justify keeping all steps complete. The output even
lists "completion problems (fading worked examples)" as a *future next step*,
confirming the model knows fading exists but deliberately chose not to apply
it here.

### Gemini 3.1 Pro — Trace

> "I'll lean heavily on the Worked Example Effect. This means providing
> complete solutions with annotations... I'll also incorporate 'fading'
> by starting with simpler equations and gradually increasing complexity,
> but maintaining a similar format."

**What this tells us:** Gemini explicitly names "fading" but immediately
redefines it as difficulty progression ("starting with simpler equations
and gradually increasing complexity"). This is the most revealing trace
in the dataset. The model has the term "fading" in its repertoire but
maps it to the wrong mechanism. It conflates increasing difficulty with
removing scaffolding — the exact near-miss predicted by hypothesis H6.

### Condition B finding
Both models retrieve formal CLT terminology when prompted. Both know
the phrase "fading." But neither applies it correctly:
- Claude knows fading but deliberately excludes it, prioritising the
  worked example effect (complete solutions).
- Gemini names fading but redefines it as difficulty progression.

This suggests the models have CLT knowledge in their training data but
do not reliably distinguish between related constructs when the prompt
says "apply CLT" without specifying which principle.

---

## Condition C: Specific Fading

### Claude Opus 4.6 — Trace

> "The worked example fading effect involves:
> 1. First example: Complete worked example (all steps shown)
> 2. Second example: Most steps shown, one step removed
> 3. Third example: More steps removed, students complete more
> 4. Fourth example: Most/all steps removed, students solve independently"

**What this tells us:** When the prompt defines fading, Claude restates it
in practical terms and implements it precisely. The trace is relatively
brief — it treats this as execution rather than deliberation. The formal
citations (Sweller & Cooper, 1985; Renkl, Atkinson & Maier, 2002) appear
in the output's teacher notes, not in the trace. This suggests the model
retrieves references during output generation, not during planning.

### Gemini 3.1 Pro — Trace

> "We're using the worked example fading effect here, also known as
> backward fading, and this is based on cognitive load theory... The
> fading should be: Example 1, 100% teacher. Example 2, 75% teacher,
> 25% student. Example 3, 25% teacher, 75% student. And Example 4:
> 0% teacher, 100% student."

**What this tells us:** Gemini names the technique ("backward fading"),
identifies it as CLT-based, and plans a specific percentage allocation
for each example. The trace shows genuine design planning — calculating
how much responsibility to shift per example. This is the richest
pedagogical reasoning in any trace across the dataset.

### Condition C finding
Both models implement fading correctly when told exactly what it is.
The traces show they can plan the fading structure before generating.
Gemini's trace is notably more detailed — it plans ratios and names
the specific variant (backward fading).

---

## Cross-Cutting Findings

### 1. The knowledge-application gap (Condition B)
The most important finding across all traces: both models *know* about
fading (it appears in their Condition B reasoning) but neither applies
it unless specifically instructed. Claude actively chooses against it;
Gemini misapplies it. This is not an absence of knowledge — it is a
failure to correctly select and apply the right principle from a set of
known principles.

### 2. How models interpret "apply CLT"
When told to "apply cognitive load theory," both models default to:
- Clear formatting (extraneous load reduction)
- Consistent structure (schema building)
- Complete solutions (worked example effect)
- Difficulty progression (element interactivity)

They do NOT default to fading. This suggests that in training data,
CLT is most frequently associated with presentation clarity and worked
examples, not with scaffolding removal.

### 3. Reasoning depth varies by condition
- Condition A traces are shallow: content selection and formatting only.
- Condition B traces are rich: formal terminology, multiple principles.
- Condition C traces are practical: implementation planning.

The general CLT prompt (B) produces the most *reasoning about theory*.
The specific prompt (C) produces the most *correct implementation*.

### 4. Difficulty ≠ fading confusion
Both models, unprompted, equate "progression" with "harder equations."
Gemini in Condition B explicitly equates "fading" with "increasing
complexity." This is the most common near-miss and confirms H6.

---

## Scores Summary

| Model | Condition | Output (0-2) | Trace (0-2) |
|-------|-----------|:---:|:---:|
| Claude | A (unprompted) | 0 | 0 |
| Claude | B (general CLT) | 0 | 2 |
| Claude | C (specific fading) | 2 | 1 |
| Gemini | A (unprompted) | 0 | 0 |
| Gemini | B (general CLT) | 1 | 2 |
| Gemini | C (specific fading) | 2 | 2 |

Scores assigned by Opus 4.6 (Claude outputs) and Sonnet 4.6 (Gemini
outputs) review agents, verified against rubric.

---

*Generated: March 2026*
*Study: AlignED Report 4 Pilot*
