import os
from dotenv import load_dotenv

load_dotenv()

# Fail loudly and early if a key is missing
for key in ["ANTHROPIC_API_KEY", "GROQ_API_KEY"]:
    if not os.getenv(key):
        raise SystemExit(f"Missing {key} in .env")

from anthropic import Anthropic
from groq import Groq

PROMPT = "Say hello in one line."

claude = Anthropic()
msg = claude.messages.create(
    model="claude-sonnet-5",
    max_tokens=200,
    messages=[{"role": "user", "content": PROMPT}],
)
print("CLAUDE:", msg.content[0].text)

groq = Groq()
resp = groq.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": PROMPT}],
)
print("GROQ:", resp.choices[0].message.content)
