"""Provider selection.

Only the selected backend's package is imported, so a Gemini-only install does not
need ``openai`` and a local run does not need ``google-genai``.
"""

from __future__ import annotations

import json
import urllib.request
from typing import Sequence

from ..config import VLMSettings
from ..types import ToolSchema
from .base import ChatSession

_DEFAULT_MODELS: dict[str, list[str]] = {
    "gemini": ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-2.5-pro"],
    "openai": ["gpt-4o", "gpt-4o-mini"],
    "anthropic": ["claude-sonnet-4-20250514", "claude-3-7-sonnet-20250219", "claude-3-5-haiku-20241022"],
    "mock": ["mock"],
}


def _fetch_json(url: str, headers: dict[str, str] | None = None, timeout_s: float = 3.0) -> dict:
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return json.loads(resp.read().decode("utf-8"))


def list_provider_models(
    provider: str,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout_s: float = 3.0,
) -> list[str]:
    """Query the provider's live models API, falling back to defaults on error."""
    if provider == "mock":
        return ["mock"]
    try:
        if provider == "gemini" and api_key:
            data = _fetch_json(
                f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
                timeout_s=timeout_s,
            )
            models = [
                str(m["name"]).removeprefix("models/")
                for m in data.get("models", [])
                if "generateContent" in m.get("supportedGenerationMethods", [])
            ]
            if models:
                return models

        elif provider == "openai" and (api_key or base_url):
            root = (base_url or "https://api.openai.com/v1").rstrip("/")
            data = _fetch_json(
                f"{root}/models",
                headers={"Authorization": f"Bearer {api_key or 'not-needed'}"},
                timeout_s=timeout_s,
            )
            ids = [str(m["id"]) for m in data.get("data", []) if m.get("id")]
            if not base_url:
                prefixes = ("gpt-", "o1", "o3", "o4", "chatgpt-")
                skip = ("instruct", "realtime", "audio", "transcribe", "tts", "search", "image")
                ids = [i for i in ids if i.startswith(prefixes) and not any(s in i for s in skip)]
            if ids:
                return sorted(ids)

        elif provider == "anthropic" and api_key:
            data = _fetch_json(
                "https://api.anthropic.com/v1/models",
                headers={"x-api-key": api_key, "anthropic-version": "2023-06-01"},
                timeout_s=timeout_s,
            )
            models = [str(m["id"]) for m in data.get("data", []) if m.get("id")]
            if models:
                return models
    except Exception:
        pass
    return list(_DEFAULT_MODELS.get(provider, []))


def make_session(settings: VLMSettings, system_prompt: str, tools: Sequence[ToolSchema],
                 api_key: str | None = None) -> ChatSession:
    provider = settings.provider
    if provider == "gemini":
        from .gemini import GeminiSession

        return GeminiSession(settings, system_prompt, tools, api_key=api_key)
    if provider == "openai":
        from .openai_compat import OpenAISession

        return OpenAISession(settings, system_prompt, tools, api_key=api_key)
    if provider == "anthropic":
        from .anthropic import AnthropicSession

        return AnthropicSession(settings, system_prompt, tools, api_key=api_key)
    if provider == "mock":
        from .mock import MockSession

        return MockSession(settings, system_prompt, tools)
    raise ValueError(f"unknown VLM provider {provider!r}: use gemini | openai | anthropic | mock")
