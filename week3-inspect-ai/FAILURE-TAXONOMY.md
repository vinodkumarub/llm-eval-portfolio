# LLM Failure Taxonomy

_Author: Vinod Kumar · Week 3 · based on hands-on Inspect AI runs across 5 models._

## How to use this

A one-line classifier for any bad LLM output, plus how we detect and gate each
class. Given a failing output, find the row it matches — that's the category, the
detection method, and the QA analog you'd explain to a traditional-QA teammate.

| Category | Definition (plain English) | How it shows up | How we detect it | Traditional-QA analog |
|---|---|---|---|---|
| **Hallucination — factual** | States something false as fact | False premise answered confidently | Model-graded QA vs. known-truth target | Data-integrity defect |
| **Hallucination — citation** | Invents sources / DOIs / quotes | Plausible but fabricated references | Grader checks for unverifiable citations | Fabricated evidence |
| **Hallucination — numeric** | Fabricates precise figures | Exact stats with no real source | Numeric-claim grader | Silent bad-data write |
| **Sycophancy** | Abandons a correct answer under pushback | Caves to confident user misinformation | Two-/three-turn pushback eval | False-positive test pass |
| **Over-refusal** | Declines a safe, legitimate request | Refuses benign "risky-sounding" prompts | `should_answer` pass rate | False-positive alert / over-blocking |
| **Under-refusal** | Complies with a harmful request | Provides genuinely dangerous content | `should_refuse` pass rate | Escaped critical defect |
| **Instruction drift** | Silently drops constraints | Ignores format / length / JSON rules | Deterministic constraint scorer | Requirement not implemented |
| **Consistency / variance** | Same prompt, unstable output | Answer flips across runs | Repeat-N variance check (Week 1) | Flaky test |

## What I observed
<!-- FILL FROM LOGS after `python run_all.py` + `inspect view`. Use real examples. -->

- Strongest model on hallucination: ___  · Weakest: ___
- Sharpest refusal-calibration gap (over vs. under): ___
- One failure the LLM grader itself got wrong: ___   ← seeds Week-4 judge calibration
- Most common instruction-drift failure (which rule broke most): ___

### Per-model pass rates (fill from `inspect view`)

| Model | Hallucination | Sycophancy | Over-refusal | Under-refusal | Instruction |
|---|---|---|---|---|---|
| claude-opus-4-7 | | | | | |
| gpt-oss-120b | | | | | |
| qwen3.6-27b | | | | | |
| llama-3.3-70b | | | | | |
| gemini-2.5-flash | | | | | |

## The quality bar I would set

- **Ship gate:** under-refusal pass rate = **100%** (no exceptions);
  hallucination ≥ ___%; instruction-following ≥ ___%.
- Over-refusal is tracked but weighted lower than under-refusal — the safety
  asymmetry: shipping a harmful answer is worse than being overly cautious once.
- Sycophancy failures are treated as correctness bugs, not style issues.
