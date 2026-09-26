from dotenv import load_dotenv

load_dotenv()

from langsmith import traceable
from anthropic import Anthropic

claude = Anthropic()

@traceable
def ask_claude(prompt: str) -> str:
    msg = claude.messages.create(
        model="claude-sonnet-5",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text

print(ask_claude("Say hello in one line."))
