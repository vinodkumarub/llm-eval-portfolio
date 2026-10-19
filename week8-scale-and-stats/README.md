# Week 8 — Scale and Statistics: Is That Difference Real?

Module 8 of the 12-week AI Eval Testing plan. Run hundreds of cases, then prove
the gap between two models is not noise.

> **Scaffold — topic not final.** Weeks 4–12 were sketched from the course arc
> in the root `README.md`. Rewrite this file as you decide what you actually want
> to build, and check each tool is installed and authenticated before designing
> around it.

---

## Why this week

Every pass rate you have reported so far came from a small sample with no error
bar. "Model A scored 84%, model B 79%" is not a finding until you can say how
often that ordering would flip on a re-run. This week is where eval work stops
being anecdotal.

---

## What you'll build

| Artifact | What it is |
|---|---|
| `runner.py` | Parallel runner with retries, caching, and resumable progress |
| `stats.py` | Bootstrap confidence intervals, paired significance tests, power estimate |
| `variance.py` | Same case × N runs — per-model output variance at fixed temperature |
| `DASHBOARD.md` | Model comparison table where every number carries an interval |

---

## How to approach it

1. Make the runner resumable and cached before scaling up — a crash 400 calls in should cost nothing.
2. Estimate sample size *first*: to detect a 5-point difference reliably, how many cases do you need? That number usually surprises people.
3. Use paired tests. Same prompts to both models means paired data, and paired tests are far more sensitive than unpaired.
4. Bootstrap the confidence interval rather than assuming normality — it is a few lines and makes no distributional claim.
5. Separate the two variance sources: model nondeterminism and judge nondeterminism. Measure each.

---

## What "done" looks like

- [ ] 300+ cases run, resumably, with cost and wall-clock recorded
- [ ] Every pass rate reported with a confidence interval
- [ ] A paired test between the top two models, with the p-value and what it does and does not mean
- [ ] Judge variance measured separately from model variance
- [ ] At least one earlier "finding" re-examined and, if warranted, withdrawn

---

## Questions to answer in your own words

1. Which earlier conclusions survive once intervals are attached?
2. How many cases do you actually need for a 5-point difference, and what does that cost in API spend?
3. How much of your total variance is the judge rather than the model?
4. What would you tell a stakeholder who asks for one number?
