# Week 1 — Foundations: Manual Evaluation & Failure Hunting

Module 1 of the 12-week AI Eval Testing plan. Week 1 has no `week1-*` folder —
its artifacts live here in `observations/`, because the deliverable *is* the
observation record.

The point of Week 1 is the discipline, not the tooling: **write the pass
criterion before you see the output.** Everything automated in Weeks 2–3 is only
trustworthy if you have already done it by hand once and know what a failure
looks like.

---

## What's here

| File | What it is |
|---|---|
| `Week1-expected-results.md` | Pass/fail criterion for each of the 10 prompts, written *before* any run |
| `week1-raw-outputs.md` | Verbatim outputs — 10 prompts × 4 models, Session 3 |
| `week1-failures.md` | Session 4: targeted failure hunting across 4 categories |

Supporting scripts live at the repo root in `scripts/`:

| Script | What it proves |
|---|---|
| `scripts/verify_setup.py` | Anthropic + Groq keys work and both models reply |
| `scripts/verify_tracing.py` | LangSmith tracing is live and a trace appears in the project |

---

## Models under test

| Slot | Model |
|---|---|
| BASE | Claude Opus 4.6 (Anthropic) — the fixed reference point |
| A | `openai/gpt-oss-120b` (Groq) |
| B | `qwen/qwen3.6-27b` (Groq) |
| C | `llama-3.3-70b-versatile` (Groq) |

One baseline, held constant across every comparison. Changing the baseline
mid-course invalidates every earlier comparison.

---

## The four failure categories

`week1-failures.md` probes each one deliberately rather than waiting for failures
to show up:

| Category | The probe |
|---|---|
| 🔴 Hallucination | Fake citations, a fictional study, a false premise, an obscure number |
| 🟠 Sycophancy | Assert confident misinformation and push back — does the model cave? |
| 🟡 Instruction drift | Stack multiple constraints — which one gets quietly dropped? |
| 🟢 Consistency / variance | Same prompt 5× per model — how stable is the output? |

---

## Run rules

These are the rules the record depends on. Breaking one makes the file
unciteable later:

1. Criterion first, output second. No post-hoc criteria.
2. Paste outputs **verbatim** — no trimming, no tidying, no paraphrase.
3. Same prompt text to every model, character for character.
4. Log anomalies even when they aren't failures. Odd-but-passing is a finding.
5. Observation stays in `observations/`; conclusions go to `reports/`.

---

## What "done" looks like

- [x] Setup and tracing verified
- [x] Pass criteria written for all 10 prompts
- [x] 10 prompts × 4 models recorded verbatim
- [x] Failure hunting across all 4 categories
- [ ] Per-category pass rates tallied into a table
- [ ] A short written verdict in `reports/` — which model failed how, and would you ship any of them

---

## Questions to answer in your own words

Write these up in `reports/`, not here. They are the thing an interviewer will
actually ask about.

1. Which category produced the most failures, and is that about the models or about your probes?
2. Where did the baseline fail too? A baseline that never fails means your probes are too easy.
3. Which of your 10 pass criteria turned out to be ambiguous once you saw real output?
4. Which failures could a deterministic check catch, and which need a judge? (This answer becomes your Week 3 scorer split.)
