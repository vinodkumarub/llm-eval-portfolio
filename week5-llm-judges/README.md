# Week 5 — Calibrating the Judge

Module 5 of the 12-week AI Eval Testing plan. You have been trusting Claude to
grade. This week you check whether that trust is earned.

> **Scaffold — topic not final.** Weeks 4–12 were sketched from the course arc
> in the root `README.md`. Rewrite this file as you decide what you actually want
> to build, and check each tool is installed and authenticated before designing
> around it.

---

## Why this week

Every `model_graded_qa` and `llm-rubric` result from Weeks 2–4 rests on an
unmeasured assumption: that the judge agrees with you. A judge that is 80%
aligned with your intent turns a 90% pass rate into a number nobody can act on.
Judge calibration is the least glamorous and most load-bearing skill in this
course.

---

## What you'll build

| Artifact | What it is |
|---|---|
| `gold/labels.jsonl` | 50–100 outputs you labelled by hand, before seeing any judge score |
| `judge_agreement.py` | Judge vs your labels — agreement rate, Cohen's kappa, confusion matrix |
| `prompt_variants/` | 3+ judge prompts: bare rubric, rubric + examples, chain-of-thought |
| `bias_probes.py` | Position bias, verbosity bias, self-preference |
| `JUDGE-CARD.md` | The judge's own scorecard: what it is reliable for, and where it is not |

---

## How to approach it

1. Pull real outputs from your Week 2–4 logs. Label them yourself first — this is the one step you cannot delegate.
2. Measure raw agreement, then kappa. Raw agreement looks great when one class dominates; kappa is what survives review.
3. Read the disagreements one at a time. Often the rubric is ambiguous, not the judge.
4. Probe for bias deliberately: swap A/B order, pad one answer with filler, have the judge grade its own family's output.
5. Iterate the judge prompt, then re-measure on the same labels. Changing the labels to match the judge defeats the purpose.

---

## What "done" looks like

- [ ] 50+ hand labels recorded before any judge comparison
- [ ] Agreement and kappa reported, not just agreement
- [ ] All three bias probes run with numbers attached
- [ ] Best and worst judge prompt variants compared on identical data
- [ ] `JUDGE-CARD.md` states the judge's reliable range in plain language

---

## Questions to answer in your own words

1. What is your judge's kappa, and would you ship a decision based on it?
2. Which rubric wording changes moved agreement most?
3. Did self-preference show up? Quantify it rather than asserting it.
4. Knowing this, which Week 2–4 conclusions would you now restate more cautiously?
