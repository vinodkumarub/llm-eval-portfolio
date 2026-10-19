# Week 7 — A Domain-Specific Eval Suite

Module 7 of the 12-week AI Eval Testing plan. Pick one real use case and build
the suite you would hand to the team that owns it.

> **Scaffold — topic not final.** Weeks 4–12 were sketched from the course arc
> in the root `README.md`. Rewrite this file as you decide what you actually want
> to build, and check each tool is installed and authenticated before designing
> around it.

---

## Why this week

Generic evals measure generic capability. No team ships on that. A domain suite
forces the harder work: deciding what quality means *for one use case*, with
criteria someone who is not an eval engineer can read and argue with.

Pick a domain you can judge yourself — support replies, code review comments,
SQL generation, clinical summarization. If you cannot tell good from bad by eye,
you cannot write the criteria.

---

## What you'll build

| Artifact | What it is |
|---|---|
| `DOMAIN.md` | The use case, its users, and what failure costs them |
| `RUBRIC.md` | Quality dimensions with concrete pass/fail language and examples |
| `dataset.jsonl` | 40+ realistic cases, including the awkward ones a demo would skip |
| `evals/` | One scorer per dimension, deterministic where the rule allows |
| `SCORECARD.md` | Model comparison on this domain, with a recommendation |

---

## How to approach it

1. Write `DOMAIN.md` first, including what a failure costs. Severity drives thresholds later.
2. Decompose quality into 3–5 dimensions. If you cannot name them, the rubric is still vibes.
3. For each dimension, write one clear pass and one clear fail example before any scorer code.
4. Build the dataset from real-shaped inputs: edge cases, ambiguous asks, out-of-scope requests.
5. Keep the deterministic/judge split from Week 3, and the calibration from Week 5 — judge dimensions need agreement numbers here too.

---

## What "done" looks like

- [ ] Domain and cost-of-failure documented
- [ ] 3–5 dimensions, each with pass/fail examples
- [ ] 40+ cases including out-of-scope and ambiguous inputs
- [ ] Every judged dimension has a measured agreement rate
- [ ] A scorecard with an explicit model recommendation and its caveats

---

## Questions to answer in your own words

1. Which dimension mattered most, and would the domain's actual users agree?
2. What did your generic Week 1–3 evals say about these models, and does the domain suite agree?
3. Which failures are tolerable here and which are not, and who decides?
4. What would you have to add before a team could gate a release on this suite?
