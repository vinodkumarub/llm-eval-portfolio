# Week 2 — Automated Evals, Red Teaming & a CI Gate

Module 2 of the 12-week AI Eval Testing plan. Week 1 was manual: you read every
output yourself. Week 2 is about making the machine read them — **promptfoo** for
declarative assertions, **DeepEval** for judge-based metrics, and a CI gate that
fails a build when defenses regress.

Three tools here on purpose, because they answer different questions:

| Tool | Question it answers |
|---|---|
| promptfoo | Does this prompt still satisfy its assertions, across N providers? |
| promptfoo redteam | Does the model hold up against adversarial probes? |
| DeepEval | How good is this output, when "good" needs a judge rather than a regex? |

---

## What's here

| File | What it is |
|---|---|
| `promptfooconfig.yaml` | 5 Week-1 prompts turned into declarative assertions, 4 providers |
| `redteam.yaml` | OWASP LLM Top 10 red team — 12 plugins × 5 tests, jailbreak + prompt-injection strategies |
| `test_week2.py` | DeepEval: `AnswerRelevancyMetric` + `GEval`, Claude as judge over Groq outputs |
| `test_dag.py` | DeepEval `DAGMetric` — evaluation as a decision tree instead of one rubric score |
| `ci-gate.mjs` | Reads promptfoo JSON, exits 1 if the defense rate drops below `PASS_THRESHOLD` (default 0.90) |

---

## Setup

Keys are read from the repo-root `.env` (`envFile: ../.env` in the promptfoo
config), so you should not need to export anything for promptfoo. The Python
tests load the same `.env` via `python-dotenv`.

```bash
source venv/bin/activate
```

Confirm promptfoo and DeepEval are actually installed before designing around
them — `promptfoo --version` and `python -c "import deepeval"`.

---

## Run it

```bash
# 1. the assertion suite (4 providers)
cd week2-promptfoo
promptfoo eval

# 2. browse results — pass/fail per assertion, side by side per provider
promptfoo view

# 3. DeepEval judge metrics
python test_week2.py
python test_dag.py
```

### Red team + gate

```bash
promptfoo redteam run -c redteam.yaml -o results.json
node ci-gate.mjs results.json

# stricter gate
PASS_THRESHOLD=0.95 node ci-gate.mjs results.json
```

The gate is a plain script, not yet wired to a GitHub Actions workflow — there is
no `.github/` in this repo. Wiring it up is the open item below.

---

## Assertion types used, and why

| Assertion | Used for | Trade-off |
|---|---|---|
| `equals` | The 17 × 24 × 8 = 3264 answer | Exact and cheap; breaks on any formatting the model adds |
| `icontains` / `not-icontains` | Canberra vs Sydney | Catches presence, not meaning — a model can contain "Canberra" and still be wrong |
| `javascript` | Sentence count, one-word output | Best tool for a mechanical rule |
| `llm-rubric` | The 2035 World Cup trap | Needed when "did it invent a winner?" is a judgement |

Note the 2035 test pairs a cheap `not-icontains "won the"` with the rubric. That
is the pattern to internalize: **deterministic check first, judge only for what
the check cannot see.** Week 3 formalizes this split.

---

## Red team coverage

12 plugins, 5 tests each, run through `jailbreak` and `prompt-injection`
strategies against Claude Opus 4.7:

| Area | Plugins |
|---|---|
| Injection & extraction | `indirect-prompt-injection`, `prompt-extraction`, `ascii-smuggling` |
| Leakage | `cross-session-leak`, `divergent-repetition`, `debug-access` |
| Agency | `excessive-agency`, `overreliance` |
| Truthfulness | `hallucination` |
| Harm | `harmful:hate`, `harmful:harassment-bullying`, `harmful:cybercrime` |

---

## Known rough edges

| Item | Why it matters |
|---|---|
| `description: "My eval"` in `promptfooconfig.yaml` | Still the generated default — name it so results are identifiable later |
| Baseline model drift | Week 1 recorded Claude Opus 4.6; Weeks 2–3 use `claude-opus-4-7`. Cross-week comparisons need this noted explicitly |
| Only 5 of the 10 Week-1 prompts are automated | Prompts 3, 6, 7, 9, 10 have no assertions yet — decide which are worth automating and which genuinely need a human |
| Gate not in CI | The threshold means nothing until something enforces it on a push |

---

## What "done" looks like

- [ ] `promptfoo eval` green across all 4 providers, results viewed in the UI
- [ ] Red team run, defense rate recorded per plugin category
- [ ] Gate demonstrated both ways — passing, then failing with `PASS_THRESHOLD=1.0`
- [ ] DeepEval judge metrics run; judge rationale read, not just the score
- [ ] A written note on where the assertions disagreed with your Week 1 manual verdict

---

## Questions to answer in your own words

1. Which Week 1 failures did the automated assertions **miss**? That gap is the real lesson of this week.
2. Did any assertion fail on an output you would have passed by hand? Was the assertion wrong, or your intuition?
3. Where is 0.90 the right defense threshold, and where would you set it higher?
4. `GEval` vs `DAGMetric` on the same output — did decomposing the rubric change the verdict, and was it worth the extra calls?

---

## Reference

- Config guide — https://promptfoo.dev/docs/configuration/guide
- Assertions & metrics — https://promptfoo.dev/docs/configuration/expected-outputs
- Red team — https://promptfoo.dev/docs/red-team
- DeepEval metrics — https://deepeval.com/docs/metrics-introduction
