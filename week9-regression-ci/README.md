# Week 9 — Regression Testing and CI Enforcement

Module 9 of the 12-week AI Eval Testing plan. Turn the suite into something that
blocks a bad change.

> **Scaffold — topic not final.** Weeks 4–12 were sketched from the course arc
> in the root `README.md`. Rewrite this file as you decide what you actually want
> to build, and check each tool is installed and authenticated before designing
> around it.

---

## Why this week

An eval suite nobody runs is documentation. The value shows up when a prompt
edit, a model upgrade, or a dependency bump fails a check before it reaches
users. Week 2 produced a gate script; this week makes it a real pipeline with
thresholds you can defend.

---

## What you'll build

| Artifact | What it is |
|---|---|
| `golden/` | Frozen dataset + recorded baseline scores, version-controlled |
| `.github/workflows/evals.yml` | CI job: fast tier on every PR, full tier nightly |
| `compare_to_baseline.py` | Per-category deltas vs the golden baseline |
| `thresholds.yaml` | Severity-weighted gates — safety stricter than style |
| `RUNBOOK.md` | What to do when the gate fails, and who decides to override |

---

## How to approach it

1. Freeze the golden set and commit the baseline scores. An unversioned baseline means a silent drift becomes the new normal.
2. Tier the suite: a cheap deterministic tier that can run on every PR, and an expensive judged tier that runs nightly.
3. Set thresholds per category by severity, not one global number. A safety regression and a formatting regression are not the same event.
4. Prove the gate fails. A gate that has never failed has never been tested.
5. Write the override path down. Undocumented overrides become routine overrides.

---

## What "done" looks like

- [ ] Golden set and baseline scores committed
- [ ] CI runs the fast tier on PRs in a defensible amount of time
- [ ] Per-category deltas, not just a global pass rate
- [ ] A deliberately broken prompt caught by CI, with a link to the failing run
- [ ] Runbook covering failure triage and overrides

---

## Questions to answer in your own words

1. Which checks earned a place in the per-PR tier, and why those?
2. What is your false-alarm rate — how often does the gate fail on a harmless change?
3. When a judged check fails, how do you tell a real regression from judge noise?
4. Who can override the gate, and what do they have to write down?
