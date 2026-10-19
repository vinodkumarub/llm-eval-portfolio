# Week 12 — Capstone: The Portfolio Report

Module 12 of the 12-week AI Eval Testing plan. Turn eleven weeks of logs into one
document a hiring manager or a stakeholder can read in ten minutes.

> **Scaffold — topic not final.** Weeks 4–12 were sketched from the course arc
> in the root `README.md`. Rewrite this file as you decide what you actually want
> to build, and check each tool is installed and authenticated before designing
> around it.

---

## Why this week

Nobody will read your logs. The portfolio artifact is a written argument:
here is what I measured, here is how, here is what I found, here is what I would
do with it — and here is where my own method is weak. That last part is what
makes the rest credible.

---

## What you'll build

| Artifact | What it is |
|---|---|
| `REPORT.md` | The main write-up — methodology, findings, recommendation, limitations |
| `METHODOLOGY.md` | Reproducible detail: datasets, models, scorers, judge calibration |
| `figures/` | A handful of charts that each make one point |
| `EXEC-SUMMARY.md` | One page for someone who will not read the report |
| Updated root `README.md` | The repo as a portfolio front door, not a course log |

---

## How to approach it

1. Write the findings first, in one sentence each. If a finding needs a paragraph to state, it is not one finding.
2. Build the report around those sentences; methodology belongs in its own file for the reader who wants to check you.
3. One chart per point. A chart that needs explaining is doing the reader's work badly.
4. Write the limitations section honestly — sample sizes, judge agreement, model drift, what you did not test. Reviewers look for this section first.
5. Rewrite the root README last, for a reader who has never heard of this course.

---

## What "done" looks like

- [ ] Every finding stated in one sentence, with a pointer to the evidence
- [ ] Methodology detailed enough for someone else to reproduce a run
- [ ] Limitations section naming specific weaknesses, not generic hedges
- [ ] Executive summary that stands alone on one page
- [ ] Root README rewritten as a portfolio entry point

---

## Questions to answer in your own words

1. What are your three strongest findings, and what is the evidence for each?
2. Which of your own conclusions are you least confident in, and why?
3. If you had four more weeks, what would you test that you did not?
4. What would you do differently if you started this course again?
