"""
DAG (DeepAcyclicGraph) evaluation using DeepEval.

Evaluates Llama 3.3 70B outputs with Claude Opus 4.7 as the judge.
Each test uses a DAG to decompose evaluation into a structured decision tree
instead of a single rubric score.
"""
import os
from dotenv import load_dotenv
import anthropic
from groq import Groq
from deepeval import evaluate
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import DAGMetric
from deepeval.metrics.dag import (
    DeepAcyclicGraph,
    BinaryJudgementNode,
    NonBinaryJudgementNode,
)
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


# ── DAG: Australia capital ─────────────────────────────────────────────────
#
# Decision tree:
#   1. Did model say False?        (BinaryJudgement)
#      ├── No  → score 0
#      └── Yes → Did model name Canberra?  (BinaryJudgement)
#                ├── No  → score 5  (partial credit)
#                └── Yes → score 10

def build_australia_dag() -> DeepAcyclicGraph:
    names_canberra = BinaryJudgementNode(
        criteria="Does the response explicitly name Canberra as Australia's capital?",
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    )
    names_canberra.add_verdict(True, score=10)
    names_canberra.add_verdict(False, score=5)

    says_false = BinaryJudgementNode(
        criteria="Does the response clearly state that the claim is FALSE?",
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    )
    says_false.add_verdict(True, then=names_canberra)
    says_false.add_verdict(False, score=0)

    return DeepAcyclicGraph(root_nodes=[says_false])


# ── DAG: FIFA 2035 hallucination trap ─────────────────────────────────────
#
# Decision tree:
#   1. Did model invent a winner?  (BinaryJudgement)
#      ├── Yes → score 0  (hallucinated)
#      └── No  → Did model explain WHY it can't answer?  (BinaryJudgement)
#                ├── No  → score 5  (silent refusal — partial)
#                └── Yes → score 10

def build_fifa_dag() -> DeepAcyclicGraph:
    explains_why = BinaryJudgementNode(
        criteria=(
            "Does the response explain that the 2035 World Cup has not occurred yet "
            "or that it cannot predict future events?"
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    )
    explains_why.add_verdict(True, score=10)
    explains_why.add_verdict(False, score=5)

    invented_winner = BinaryJudgementNode(
        criteria="Does the response name a country or team as the winner of the 2035 FIFA World Cup?",
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    )
    invented_winner.add_verdict(True, score=0)
    invented_winner.add_verdict(False, then=explains_why)

    return DeepAcyclicGraph(root_nodes=[invented_winner])


# ── DAG: Transformers explanation ──────────────────────────────────────────
#
# Decision tree:
#   1. Does response mention attention?  (BinaryJudgement)
#      ├── No  → score 0
#      └── Yes → How many sentences?  (NonBinaryJudgement)
#                ├── "one"   → score 3
#                ├── "two"   → score 6
#                ├── "three" → score 10
#                └── "more"  → score 5

def build_transformers_dag() -> DeepAcyclicGraph:
    sentence_count = NonBinaryJudgementNode(
        criteria="How many sentences does the response contain? Reply with exactly one word: 'one', 'two', 'three', or 'more'.",
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT],
    )
    sentence_count.add_verdict("one", score=3)
    sentence_count.add_verdict("two", score=6)
    sentence_count.add_verdict("three", score=10)
    sentence_count.add_verdict("more", score=5)

    mentions_attention = BinaryJudgementNode(
        criteria="Does the response mention the word 'attention' or 'attention mechanism'?",
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT],
    )
    mentions_attention.add_verdict(True, then=sentence_count)
    mentions_attention.add_verdict(False, score=0)

    return DeepAcyclicGraph(root_nodes=[mentions_attention])


# ── Tests ──────────────────────────────────────────────────────────────────

def test_dag_australia_capital():
    prompt = '"The capital of Australia is Sydney" — True or False?'
    output = call_llama(prompt)
    test_case = LLMTestCase(input=prompt, actual_output=output)
    metric = DAGMetric(
        name="Australia Capital DAG",
        dag=build_australia_dag(),
        model=judge,
        threshold=0.5,
    )
    evaluate([test_case], [metric])


def test_dag_fifa_hallucination():
    prompt = "Who won the 2035 FIFA World Cup?"
    output = call_llama(prompt)
    test_case = LLMTestCase(input=prompt, actual_output=output)
    metric = DAGMetric(
        name="FIFA Hallucination DAG",
        dag=build_fifa_dag(),
        model=judge,
        threshold=0.5,
    )
    evaluate([test_case], [metric])


def test_dag_transformers():
    prompt = "Explain Transformers in exactly 3 sentences."
    output = call_llama(prompt)
    test_case = LLMTestCase(input=prompt, actual_output=output)
    metric = DAGMetric(
        name="Transformers Explanation DAG",
        dag=build_transformers_dag(),
        model=judge,
        threshold=0.5,
    )
    evaluate([test_case], [metric])
