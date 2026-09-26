"""Confirm Inspect AI runs one sample end-to-end against Groq's free tier."""
from inspect_ai import Task, eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.scorer import includes
from inspect_ai.solver import generate

task = Task(
    dataset=[Sample(input="Reply with exactly the word: READY", target="READY")],
    plan=generate(),
    scorer=includes(),
)

if __name__ == "__main__":
    inspect_eval(task, model="groq/llama-3.3-70b-versatile")
    print("Inspect is working. Run `inspect view` to see the log.")
