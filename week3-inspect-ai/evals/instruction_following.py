"""Instruction-following eval — format & constraint compliance.

This is where deterministic scoring beats an LLM judge: the rule is checkable in
Python, so there's no grader ambiguity. One reusable `constraint_scorer` handles
every rule via the sample's `metadata["rule"]` — demonstrating that Inspect
scorers are ordinary composable Python, the practical contrast with promptfoo's
per-test `assert` blocks.
"""
import json
import re

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate
from inspect_ai.scorer import scorer, Score, CORRECT, INCORRECT, accuracy, stderr


def _sentence_count(text):
    parts = re.split(r"[.!?]+", text)
    return len([p for p in parts if p.strip()])


# ── Rule registry ─────────────────────────────────────────────────────────────
# To add a new rule: add one entry here. No other code changes needed.
# Each value is a callable: (output: str) -> bool
RULES: dict[str, callable] = {
    "one_word":            lambda o: len(o.split()) == 1,
    "three_sentences":     lambda o: _sentence_count(o) == 3,
    "valid_json":          lambda o: _try_json(o) is not None,
    "json_keys":           lambda o: isinstance(_try_json(o), dict) and set(_try_json(o).keys()) == {"name", "age"},
    "starts_with_because": lambda o: o.lower().startswith("because"),
    "no_letter_e":         lambda o: "e" not in o.lower() and len(o) > 0,
    "exactly_five_words":  lambda o: len(o.split()) == 5,
    "all_caps":            lambda o: (letters := [c for c in o if c.isalpha()]) and all(c.isupper() for c in letters),
    "ends_with_question":  lambda o: o.endswith("?"),
    # ── add new rules below this line ─────────────────────────────────────
    # "no_numbers":        lambda o: not any(c.isdigit() for c in o),
    # "max_ten_words":     lambda o: len(o.split()) <= 10,
    # "starts_with_i":     lambda o: o.lower().startswith("i "),
}


def _try_json(text: str):
    """Return parsed JSON or None — used by JSON rules above."""
    try:
        return json.loads(text)
    except Exception:
        return None


# ── Scorer ────────────────────────────────────────────────────────────────────
@scorer(metrics=[accuracy(), stderr()])
def constraint_scorer():
    async def score(state, target):
        out = state.output.completion.strip()
        rule = state.metadata["rule"]

        check = RULES.get(rule)
        if check is None:
            raise ValueError(f"Unknown rule '{rule}'. Add it to the RULES dict.")

        ok = bool(check(out))
        return Score(
            value=CORRECT if ok else INCORRECT,
            answer=out,
            explanation=f"rule={rule} -> {'PASS' if ok else 'FAIL'}",
        )

    return score


SAMPLES = [
    Sample(input="Summarize the concept of gravity in one word.",
           target="one word", metadata={"rule": "one_word"}),
    Sample(input="Explain Transformers (the neural network) in exactly 3 sentences.",
           target="3 sentences", metadata={"rule": "three_sentences"}),
    Sample(input='Return a JSON object with keys "name" and "age" for a person named '
                 'Ada, age 36. Output JSON only, nothing else.',
           target="valid json", metadata={"rule": "valid_json"}),
    Sample(input='Give me ONLY a JSON object with exactly the keys "name" and "age" '
                 'for Grace Hopper, age 85. No other keys, no prose.',
           target="json with exactly name+age", metadata={"rule": "json_keys"}),
    Sample(input="Why is the sky blue? Begin your answer with the word 'Because'.",
           target="starts with Because", metadata={"rule": "starts_with_because"}),
    Sample(input="Describe a sunset in a short phrase that does not contain the "
                 "letter 'e' anywhere.",
           target="no letter e", metadata={"rule": "no_letter_e"}),
    Sample(input="Describe the ocean in exactly five words.",
           target="exactly 5 words", metadata={"rule": "exactly_five_words"}),
    Sample(input="Write a short motivational slogan in ALL CAPITAL LETTERS.",
           target="all caps", metadata={"rule": "all_caps"}),
    Sample(input="Respond with a single sentence that ends in a question mark.",
           target="ends with question mark", metadata={"rule": "ends_with_question"}),
]


@task
def instruction_following():
    return Task(dataset=SAMPLES, solver=generate(), scorer=constraint_scorer())
