"""Provider selection.

Only the selected backend's package is imported, so a Gemini-only install does not
need ``openai`` and a local run does not need ``google-genai``.
"""

from __future__ import annotations

from typing import Sequence

from ..config import VLMSettings
from ..types import ToolSchema
from .base import ChatSession


def make_session(settings: VLMSettings, system_prompt: str, tools: Sequence[ToolSchema],
                 api_key: str | None = None) -> ChatSession:
    provider = settings.provider
    if provider == "gemini":
        from .gemini import GeminiSession

        return GeminiSession(settings, system_prompt, tools, api_key=api_key)
    if provider == "openai":
        from .openai_compat import OpenAISession

        return OpenAISession(settings, system_prompt, tools, api_key=api_key)
    if provider == "mock":
        from .mock import MockSession

        return MockSession(settings, system_prompt, tools)
    raise ValueError(f"unknown VLM provider {provider!r}: use gemini | openai | mock")
