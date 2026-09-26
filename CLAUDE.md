# CLAUDE.md — llm-eval-portfolio

Vinod's hands-on **12-week AI Eval Testing course** and portfolio. The goal is that
Vinod *learns* the craft, so this repo is a learning space, not a delivery project.

---

## How to work here

| Rule | What it means |
|---|---|
| **Coach, don't do** | Scaffold and explain. Vinod runs the evals, reads results (`inspect view`, `promptfoo view`), and writes analysis/taxonomies in his own words. Never write finished deliverables for him. |
| **Explain the how** | When a step says "do X" and X is new, briefly explain how and why — teacher voice, concise, no finished answer. |
| **Steps ≠ files** | "Explain / give steps / how do I" → text only. Create or edit files only when asked to create/write/add something, and keep scope to exactly that. |
| **Ask before installing** | No `pip`/`brew`/`npm`/`npx` without an explicit yes (a global hook blocks these anyway). |
| **Readable markdown** | Tables, headings, whitespace. No dense nested lists. |
| **No flattery** | End on substance: status, next step, or a real question. |

---

## Layout

| Path | Contents |
|---|---|
| `observations/` | Week 1 prompts, expected results, raw outputs, failure notes |
| `scripts/` | `verify_setup.py` (API keys), `verify_tracing.py` (LangSmith) |
| `week2-promptfoo/` | promptfoo config, red-team config, pytest/DeepEval tests, CI gate |
| `week3-inspect-ai/` | Inspect AI evals (hallucination, sycophancy, refusal, instruction-following), `run_all.py`, failure taxonomy |
| `reports/` | Polished write-ups (mostly empty so far) |

New weeks go in a `weekN-<topic>/` folder at the repo root with their own `README.md`.

---

## Environment

| Item | Value |
|---|---|
| Python | `venv/` at repo root — `source venv/bin/activate` |
| Secrets | `.env` (gitignored) — Anthropic, Groq, LangSmith keys |
| Baseline model | Claude (Anthropic API) |
| Candidate models | Groq: `openai/gpt-oss-120b`, `qwen/qwen3.6-27b`, `llama-3.3-70b-versatile` |
| Tools | promptfoo, Inspect AI, DeepEval, LangSmith |

Check that a tool is actually installed/authenticated before designing around it.
