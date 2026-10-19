# Week 11 — Cost, Latency, Quality: The Real Selection Problem

Module 11 of the 12-week AI Eval Testing plan. Best model on the benchmark is
rarely the right model to ship.

> **Scaffold — topic not final.** Weeks 4–12 were sketched from the course arc
> in the root `README.md`. Rewrite this file as you decide what you actually want
> to build, and check each tool is installed and authenticated before designing
> around it.

---

## Why this week

Every number so far has been quality-only. Nobody selects on quality alone: they
select under a latency budget and a cost ceiling. A model 2 points better at 6×
the price and 3× the latency loses most real decisions, and being able to say so
with numbers is what separates an eval engineer from a benchmark reader.

---

## What you'll build

| Artifact | What it is |
|---|---|
| `measure.py` | Per-call cost, p50/p95/p99 latency, tokens in/out, alongside quality |
| `frontier.py` | Quality-vs-cost Pareto frontier — which models are dominated |
| `routing.py` | Cheap model first, escalate on low confidence; measure what it saves |
| `MODEL-CARD.md` | Card for your recommended model: strengths, limits, measured numbers |
| `RECOMMENDATION.md` | The decision, its constraints, and what would change it |

---

## How to approach it

1. Instrument cost and latency on the suite you already have — do not build a new one.
2. Report p95 and p99, not the mean. Users feel the tail.
3. Plot the frontier and identify dominated models explicitly: worse *and* more expensive is a finding worth stating.
4. Try a routing strategy and measure the real saving, including the escalation overhead you added.
5. State the recommendation with its constraints. "Best" without a budget is not an answer.

---

## What "done" looks like

- [ ] Cost, p50/p95/p99 latency, and quality in one table
- [ ] Pareto frontier with dominated models named
- [ ] A routing experiment with measured savings and quality impact
- [ ] Model card with measured numbers, not marketing claims
- [ ] A recommendation that states its budget and latency assumptions

---

## Questions to answer in your own words

1. At your quality bar, which model is actually cheapest?
2. How much quality would you trade for halving p95 latency, and who should make that call?
3. Did routing pay off, or did the escalation overhead eat the saving?
4. What would change your recommendation — a price cut, a new release, a different traffic mix?
