# Week 6 — Evaluating Agents and Tool Use

Module 6 of the 12-week AI Eval Testing plan. Grade the trajectory, not only the
final answer.

> **Scaffold — topic not final.** Weeks 4–12 were sketched from the course arc
> in the root `README.md`. Rewrite this file as you decide what you actually want
> to build, and check each tool is installed and authenticated before designing
> around it.

---

## Why this week

An agent can reach the right answer through a wrong path — three redundant tool
calls, a hallucinated argument, a retry that silently masked an error. Final-answer
scoring hides all of it, and the hidden parts are what break in production, where
each wasted call costs money and latency.

---

## What you'll build

| Artifact | What it is |
|---|---|
| `tools/` | 3–5 mock tools with deterministic responses, so failures are the agent's |
| `tasks.jsonl` | Tasks with a known-good tool sequence recorded for each |
| `evals/tool_selection.py` | Right tool, right arguments, right order |
| `evals/trajectory.py` | Step count, redundant calls, recovery after an error |
| `evals/task_success.py` | End-state correctness — the outcome, not the transcript |
| `FAILURE-MODES.md` | Agent-specific failure classes, extending the Week 3 taxonomy |

---

## How to approach it

1. Mock the tools. Real APIs make failures ambiguous — was that the agent or a 503?
2. For each task, write the ideal call sequence before you run anything.
3. Score outcome and trajectory separately, then look at the cells where they disagree. Right answer / bad path is the interesting quadrant.
4. Inject tool failures deliberately — timeouts, empty results, malformed responses — and score recovery.
5. Cap the step budget. An agent that succeeds in 40 calls has failed a real requirement.

---

## What "done" looks like

- [ ] Mock tools with recorded ideal sequences per task
- [ ] Outcome and trajectory scored as separate metrics
- [ ] Error-injection cases included and scored for recovery
- [ ] Step/cost budget enforced and reported
- [ ] At least three agent-specific failure modes added to the taxonomy

---

## Questions to answer in your own words

1. How often did right answer coincide with wrong path?
2. What did a tool error actually do to the agent — retry, give up, or fabricate the result?
3. Which trajectory metric would you put in a CI gate, and what threshold?
4. Does the Week 3 taxonomy still hold for agents, or did it need new top-level classes?
