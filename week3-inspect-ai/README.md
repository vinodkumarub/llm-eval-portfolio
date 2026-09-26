# Week 3 — Safety Evals & Failure Taxonomy with Inspect AI

Module 3 of the 12-week AI Eval Testing plan. Learn **Inspect AI** (UK AISI's
evaluation framework) and produce a **failure taxonomy** a team can classify against.

Where Weeks 1–2 covered *running* evals, Week 3 covers *defining what quality means*:
four failure categories, each turned into a real, logged Inspect eval, run across
five models.

---

## What's here

| File | What it is |
|---|---|
| `scripts/verify_inspect.py` | Smoke test — one sample end-to-end against Groq |
| `evals/hallucination.py` | Factual / citation / numeric fabrication (model-graded) |
| `evals/sycophancy.py` | Does the model cave under confident pushback? (model-graded) |
| `evals/refusal.py` | Over-refusal **and** under-refusal, scored separately |
| `evals/instruction_following.py` | Format/constraint compliance (deterministic scorer) |
| `run_all.py` | Runs every eval × every model into `logs/` |
| `FAILURE-TAXONOMY.md` | 1-page taxonomy of LLM failure classes |
| `PROMPTFOO-VS-INSPECT.md` | 1-page framework comparison + selection rule |

---

## Setup

```bash
cd ~/"AI Learning/llm-eval-portfolio"
source venv/bin/activate
pip install inspect-ai google-genai      # google-genai only needed for Gemini
```

Provider keys are read from the repo-root `.env` (`ANTHROPIC_API_KEY`,
`GROQ_API_KEY`, and `GOOGLE_API_KEY` for Gemini). For CLI runs, load them into the
shell; `run_all.py` loads `.env` automatically via `python-dotenv`.

```bash
set -a; source .env; set +a
```

---

## Run it

```bash
# 1. smoke test
python week3-inspect-ai/scripts/verify_inspect.py

# 2. the full matrix (4 tasks × up to 5 models)
cd week3-inspect-ai
python run_all.py

# 3. browse transcripts, scores, and grader rationale
inspect view --log-dir ./logs
```

`run_all.py` auto-skips Gemini if `GOOGLE_API_KEY` isn't set, so the other four
models run regardless.

---

## The four failure categories

| Eval | Scoring | Why this scorer |
|---|---|---|
| **Hallucination** | `model_graded_qa` (Claude) | "Did it fabricate?" is a judgement call — needs an LLM grader |
| **Sycophancy** | `model_graded_qa` (Claude) | "Did it hold its answer?" across a multi-turn exchange |
| **Refusal calibration** | `model_graded_qa` (Claude), tagged by direction | Over- vs under-refusal need separate pass rates |
| **Instruction following** | custom deterministic Python scorer | The rule is checkable in code — no judge needed |

The split is the point: **model-graded where meaning matters, deterministic where
the rule is mechanical.**

---

## Model IDs

Mirror the Week 2 promptfoo config: `anthropic/claude-opus-4-7`,
`groq/openai/gpt-oss-120b`, `groq/qwen/qwen3.6-27b`,
`groq/llama-3.3-70b-versatile`, `google/gemini-2.5-flash`. IDs drift — confirm in
the provider consoles if a run fails with an unknown-model error.

---

## Status

- [ ] Smoke test passing
- [ ] All four evals run across ≥3 models, logged
- [ ] Over- and under-refusal measured as separate pass rates
- [ ] `FAILURE-TAXONOMY.md` filled from real logs
- [ ] `PROMPTFOO-VS-INSPECT.md` complete
