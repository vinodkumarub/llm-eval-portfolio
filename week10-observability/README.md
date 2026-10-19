# Week 10 — Production Observability and Online Evals

Module 10 of the 12-week AI Eval Testing plan. Evaluate real traffic, not your
own test set.

> **Scaffold — topic not final.** Weeks 4–12 were sketched from the course arc
> in the root `README.md`. Rewrite this file as you decide what you actually want
> to build, and check each tool is installed and authenticated before designing
> around it.

---

## Why this week

Your dataset reflects what you thought users would ask. Production reflects what
they actually ask, and the gap is where incidents live. Online evals sample live
traffic, score it continuously, and alert on drift — a different discipline from
offline benchmarking.

LangSmith is already wired up in this repo (`scripts/verify_tracing.py`), so this
week builds on tracing you have rather than new infrastructure.

---

## What you'll build

| Artifact | What it is |
|---|---|
| `trace_schema.md` | What every trace must carry: inputs, outputs, scores, cost, latency, version |
| `online_sampler.py` | Sample a slice of live traffic for scoring |
| `drift_monitor.py` | Input distribution drift and output quality drift over time |
| `feedback_loop.py` | Route thumbs-down traffic into the next offline dataset |
| `ALERTS.md` | What pages a human, at what threshold, and what they do about it |

---

## How to approach it

1. Decide what a trace must contain before you start sampling. Missing fields cannot be backfilled after an incident.
2. Sample rather than score everything — pick a rate that gives a usable signal at a cost you would actually approve.
3. Separate input drift from quality drift. New kinds of questions and worse answers to the same questions need different responses.
4. Close the loop: failures found online become offline cases, so the suite grows from reality.
5. Write alert thresholds with a named owner and an action. An alert with no action is a notification.

---

## What "done" looks like

- [ ] Trace schema defined and enforced in at least one script
- [ ] Online sampling running with a justified rate and cost estimate
- [ ] Input and quality drift tracked separately
- [ ] A real production-shaped failure promoted into the offline dataset
- [ ] Alert thresholds with owners and actions

---

## Questions to answer in your own words

1. What is in your traces that you would need during an incident, and what did you nearly leave out?
2. What sampling rate did you pick, and what does it cost per month at your traffic assumption?
3. Would your offline suite have caught the production failures you found?
4. How quickly would a quality regression be noticed today — hours, days, or never?
