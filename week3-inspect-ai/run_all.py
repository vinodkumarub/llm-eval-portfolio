"""Run every Week-3 eval across every model and drop logs in ./logs.

`eval()` accepts a list of tasks and a list of models and runs the full matrix,
writing one .eval log per (task x model). Browse the results with:

    inspect view --log-dir ./logs
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from inspect_ai import eval

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # so `evals` package imports work from any cwd

# Provider keys live in the repo-root .env (one level up from week3-inspect-ai/).
load_dotenv(HERE.parent / ".env")

from evals.hallucination import hallucination          # noqa: E402
from evals.sycophancy import sycophancy                # noqa: E402
from evals.refusal import refusal                      # noqa: E402
from evals.instruction_following import instruction_following  # noqa: E402

# Model IDs mirror the Week 2 promptfoo config. Confirm current IDs in the
# provider consoles if a run fails with an unknown-model error.
MODELS = [
    "anthropic/claude-opus-4-7",       # baseline / reference grader
    "groq/openai/gpt-oss-120b",
    "groq/qwen/qwen3.6-27b",
    "groq/llama-3.3-70b-versatile",
]

# Gemini only runs if its key is present, so the matrix works before the key
# is added and automatically includes Gemini once GOOGLE_API_KEY is set.
if os.getenv("GOOGLE_API_KEY"):
    MODELS.append("google/gemini-2.5-flash")
else:
    print("[run_all] GOOGLE_API_KEY not set — skipping google/gemini-2.5-flash")

TASKS = [hallucination(), sycophancy(), refusal(), instruction_following()]

if __name__ == "__main__":
    print(f"[run_all] {len(TASKS)} tasks x {len(MODELS)} models "
          f"= {len(TASKS) * len(MODELS)} runs")
    eval(TASKS, model=MODELS, log_dir=str(HERE / "logs"))
    print("[run_all] done. Browse with: inspect view --log-dir ./logs")
