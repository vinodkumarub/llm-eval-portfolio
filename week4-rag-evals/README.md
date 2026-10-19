# Week 4 — RAG Evaluation: Faithfulness vs Retrieval

Module 4 of the 12-week AI Eval Testing plan. Evaluate a retrieval pipeline, not
just a model.

> **Scaffold — topic not final.** Weeks 4–12 were sketched from the course arc
> in the root `README.md`. Rewrite this file as you decide what you actually want
> to build, and check each tool is installed and authenticated before designing
> around it.

---

## Why this week

Weeks 1–3 evaluated a model answering from its own weights. Most real systems
answer from retrieved context, which splits failure into two independent
questions: **did retrieval find the right chunks**, and **did the model stay
faithful to what it found**. A single accuracy number cannot tell those apart,
and fixing the wrong one wastes a sprint.

---

## What you'll build

| Artifact | What it is |
|---|---|
| `corpus/` | A small, closed document set you fully understand — 20–50 chunks, not a scraped pile |
| `build_index.py` | Chunk + embed + index, with chunk size as a variable you can sweep |
| `evals/faithfulness.py` | Is every claim in the answer supported by the retrieved context? |
| `evals/context_relevance.py` | Did retrieval return what was needed? Precision and recall @k |
| `evals/answer_correctness.py` | Ground-truth comparison, separate from faithfulness |
| `FINDINGS.md` | Which failures were retrieval's fault vs generation's fault |

---

## How to approach it

1. Build the corpus first and write 20 question/ground-truth pairs **before** indexing anything.
2. Include questions whose answer is **not** in the corpus. A RAG system that answers those is hallucinating, and most suites never test it.
3. Index, then measure retrieval alone — no generation. If recall@5 is poor, generation metrics are noise.
4. Add generation and score faithfulness against the *retrieved* context, not against the ground truth. Those are different metrics.
5. Sweep one variable (chunk size or k) and show the effect on each metric separately.

---

## What "done" looks like

- [ ] 20+ question/ground-truth pairs, written before the index existed
- [ ] At least 3 unanswerable questions in the set
- [ ] Retrieval scored independently of generation
- [ ] Faithfulness and correctness reported as separate numbers
- [ ] One swept parameter, with the trade-off written up

---

## Questions to answer in your own words

1. For each failure you found: retrieval or generation? How do you know?
2. What did the model do with the unanswerable questions — refuse, hedge, or invent?
3. Can an answer be faithful and still wrong? Find a real example in your logs.
4. Which Week 3 scorer patterns transferred here unchanged, and which needed the context passed in?
