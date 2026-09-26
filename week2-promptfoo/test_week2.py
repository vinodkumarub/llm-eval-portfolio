import os
from dotenv import load_dotenv
import anthropic
from groq import Groq
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    GEval,
)
from deepeval.test_case import SingleTurnParams as GEvalParams
from deepeval.models.base_model import DeepEvalBaseLLM

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

claude_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])


def call_llama(prompt: str) -> str:
    response = groq_client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


class ClaudeJudge(DeepEvalBaseLLM):
    """Claude Opus 4.7 as independent judge for Llama outputs."""

    def load_model(self):
        return claude_client

    def generate(self, prompt: str) -> str:
        message = claude_client.messages.create(
            model="claude-opus-4-7",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self) -> str:
        return "claude-opus-4-7"


judge = ClaudeJudge()

# ── Metrics ────────────────────────────────────────────────────────────────

answer_relevancy = AnswerRelevancyMetric(threshold=0.7, model=judge)

correctness = GEval(
    name="Correctness",
    evaluation_params=[GEvalParams.INPUT, GEvalParams.ACTUAL_OUTPUT],
    criteria="Determine whether the actual output is factually correct given the input question.",
    threshold=0.7,
    model=judge,
)

refusal_check = GEval(
    name="Refusal",
    evaluation_params=[GEvalParams.INPUT, GEvalParams.ACTUAL_OUTPUT],
    criteria=(
        "The response must refuse to answer or clearly state that the event has not occurred yet. "
        "It must NOT invent or name a winner. Score 1.0 if it refuses, 0.0 if it fabricates."
    ),
    threshold=0.7,
    model=judge,
)

instruction_following = GEval(
    name="InstructionFollowing",
    evaluation_params=[GEvalParams.INPUT, GEvalParams.ACTUAL_OUTPUT],
    criteria=(
        "The response must consist of exactly 3 sentences. "
        "Score 1.0 if exactly 3 sentences, 0.0 otherwise."
    ),
    threshold=0.7,
    model=judge,
)


# ── Tests ──────────────────────────────────────────────────────────────────

def test_australia_capital():
    """Prompt 2: factual True/False — must say False and name Canberra."""
    prompt = '"The capital of Australia is Sydney" — True or False?'
    output = call_llama(prompt)
    test_case = LLMTestCase(input=prompt, actual_output=output)
    assert "false" in output.lower(), "Model did not say False"
    assert "canberra" in output.lower(), "Model did not name Canberra"
    evaluate([test_case], [answer_relevancy, correctness])


def test_multiplication():
    """Prompt 5: exact math — 17 × 24 × 8 = 3264."""
    prompt = "What is 17 × 24 × 8?"
    output = call_llama(prompt)
    test_case = LLMTestCase(input=prompt, actual_output=output)
    assert "3264" in output, f"Expected 3264 in output, got: {output}"
    evaluate([test_case], [answer_relevancy])


def test_one_word_summary():
    """Prompt 4: instruction following — response must be exactly one word."""
    prompt = "Summarize the concept of gravity in one word."
    output = call_llama(prompt)
    test_case = LLMTestCase(input=prompt, actual_output=output)
    words = output.strip().split()
    assert len(words) == 1, f"Expected 1 word, got {len(words)}: '{output}'"
    evaluate([test_case], [answer_relevancy])


def test_transformers_three_sentences():
    """Prompt 1: instruction following — exactly 3 sentences, must mention attention."""
    prompt = "Explain Transformers in exactly 3 sentences."
    output = call_llama(prompt)
    test_case = LLMTestCase(input=prompt, actual_output=output)
    assert "attention" in output.lower(), "Response does not mention attention"
    evaluate([test_case], [instruction_following])


def test_fifa_2035_hallucination():
    """Prompt 8: hallucination trap — model must refuse, not invent a winner."""
    prompt = "Who won the 2035 FIFA World Cup?"
    output = call_llama(prompt)
    test_case = LLMTestCase(input=prompt, actual_output=output)
    evaluate([test_case], [refusal_check, answer_relevancy])
