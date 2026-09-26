# promptfoo vs Inspect AI

_Author: Vinod Kumar · Week 3 · after shipping a real suite in each (Week 2 promptfoo, Week 3 Inspect)._

Both run prompts across models and score the output. They differ in **who writes
the logic and how much control you get** — YAML declarations vs. Python objects.

| Axis | promptfoo (Week 2) | Inspect AI (Week 3) |
|---|---|---|
| Config style | YAML-first, declarative | Python-first, composable |
| Sweet spot | CI gating, fast prompt/model regression | Safety, multi-step, research-grade evals |
| Assertions / scoring | `assert` list (`contains`, `is-json`, `llm-rubric`) | Reusable `Scorer` objects + custom Python graders |
| Multi-step / tools / agents | Limited | First-class (solvers, `react`, tool loops) |
| Multi-turn conversations | Awkward to express | Native — a `Sample.input` is a list of chat messages |
| Logs & debugging | Pass/fail table + web view | Per-sample transcripts, scores, grader rationale via `inspect view` |
| Reusability of scoring | Per-test `assert` blocks | One scorer applies to any matching sample |
| Red-team built-ins | Strong (OWASP plugin suite) | Via the `inspect_evals` companion benchmarks |
| Governance | OpenAI-owned since Mar 2026 (still MIT) | UK AISI — public-sector credibility |
| **When I choose it** | "Gate the merge." | "Prove it's safe / evaluate the hard stuff." |

## What the build actually showed

- **Multi-turn is the clearest divide.** The sycophancy eval is a three-message
  conversation (question → correct answer → confident pushback). In Inspect that's
  just a list of `ChatMessage`s in `Sample.input`. In promptfoo the same test would
  fight the YAML.
- **One scorer, many cases.** `instruction_following.py` uses a single
  `constraint_scorer` that dispatches on `metadata["rule"]` — nine constraint types,
  one grader. In promptfoo each case carries its own `assert` block.
- **The logs are the product.** `inspect view` shows the grader's *reasoning* per
  sample, not just green/red. That's what lets you catch the judge being wrong — the
  seed for Week 4 judge calibration.
- **promptfoo is still faster for the simple gate.** For "did this prompt regress
  across three models," the Week 2 YAML + `ci-gate.mjs` is less code and runs in CI
  with no Python driver.

## Selection rule

> For CI gates and side-by-side prompt regression, use **promptfoo**. For
> safety-critical, multi-step, or research-grade evaluation — anything needing
> custom solvers, tool loops, or reusable scorers — use **Inspect AI**.
