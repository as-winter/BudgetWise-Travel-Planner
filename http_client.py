"""LLM access helper — calls ASI:One via the OpenAI-compatible API.

Agentverse injects ASI1_API_KEY and ASI1_BASE_URL into every hosted agent,
so no key needs to be configured by the user.
"""

import os

from openai import OpenAI

_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.environ["ASI1_API_KEY"],
            base_url=os.environ["ASI1_BASE_URL"],
            timeout=30.0,
        )
    return _client


def ask_asi1(messages, max_tokens=2048):
    """Send a chat completion request to ASI:One and return the reply text."""
    client = _get_client()
    completion = client.chat.completions.create(
        model="asi1",
        messages=messages,
        max_tokens=max_tokens,
    )
    return completion.choices[0].message.content or ""
