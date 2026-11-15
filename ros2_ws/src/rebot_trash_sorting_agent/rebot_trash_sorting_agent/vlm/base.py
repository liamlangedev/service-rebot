"""Planner backends.

One interface, three implementations:

* :mod:`gemini` - Google ``google-genai`` (default: ``gemini-3.8-flash``)
* :mod:`openai_compat` - any OpenAI-compatible endpoint (vLLM, Ollama, LM Studio)
* :mod:`mock` - no network, no key; deterministic script for smoke tests

A session owns its own conversation, because the providers disagree about how tool
results are represented. The orchestrator only ever does::

    response = session.send([text, image])
    ...run response.tool_calls[0]...
    session.submit_tool_results(response, [result])
"""

from __future__ import annotations

import json
from typing import Any, Protocol, Sequence, runtime_checkable

from ..types import ImagePart, LLMResponse, TextPart, ToolResult, ToolSchema

Part = TextPart | ImagePart


@runtime_checkable
class ChatSession(Protocol):
    name: str
    model: str

    def send(self, parts: Sequence[Part]) -> LLMResponse:
        """Send a user turn and get the next planner turn."""

    def submit_tool_results(self, response: LLMResponse, results: Sequence[ToolResult]) -> None:
        """Record what the executed tool returned, for the next send()."""


def jsonable(payload: Any) -> Any:
    """Round-trip through JSON so every provider sees plain data."""
    return json.loads(json.dumps(payload, default=str))
