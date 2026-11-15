"""Anthropic Claude planner backend using the Messages REST API."""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Sequence

from ..config import VLMSettings
from ..types import ImagePart, LLMResponse, TextPart, ToolCall, ToolResult, ToolSchema
from .base import Part, jsonable

_DEFAULT_URL = "https://api.anthropic.com/v1/messages"
_TRANSIENT = ("429", "500", "502", "503", "504", "529", "timeout", "temporarily", "overloaded")


class AnthropicSession:
    name = "anthropic"

    def __init__(self, settings: VLMSettings, system_prompt: str, tools: Sequence[ToolSchema],
                 api_key: str | None = None) -> None:
        key = (
            api_key
            or os.environ.get("ANTHROPIC_API_KEY")
            or os.environ.get("CLAUDE_API_KEY")
            or os.environ.get(settings.api_key_env)
        )
        if not key:
            raise RuntimeError("anthropic provider needs ANTHROPIC_API_KEY or CLAUDE_API_KEY")

        self.model = settings.model
        self._settings = settings
        self._api_key = key
        self._system_prompt = system_prompt
        self._tools = list(tools)
        self._base_url = (settings.base_url or _DEFAULT_URL).rstrip("/")
        self._messages: list[dict[str, Any]] = []

    def send(self, parts: Sequence[Part]) -> LLMResponse:
        self._messages.append({"role": "user", "content": self._content(parts)})
        data = self._with_retries(self._post_messages)

        blocks = data.get("content") or []
        text_parts: list[str] = []
        calls: list[ToolCall] = []
        for block in blocks:
            if not isinstance(block, dict):
                continue
            btype = block.get("type")
            if btype == "text":
                text_parts.append(str(block.get("text") or ""))
            elif btype == "tool_use":
                calls.append(
                    ToolCall(
                        name=str(block.get("name") or ""),
                        arguments=dict(block.get("input") or {}),
                        call_id=block.get("id"),
                    )
                )

        self._messages.append({"role": "assistant", "content": blocks})

        raw_usage = data.get("usage") or {}
        in_tok = int(raw_usage.get("input_tokens") or 0)
        out_tok = int(raw_usage.get("output_tokens") or 0)
        usage = {"input": in_tok, "output": out_tok, "total": in_tok + out_tok} if raw_usage else {}

        return LLMResponse(
            text="".join(text_parts),
            tool_calls=calls,
            model=self.model,
            usage=usage,
            request_id=data.get("id"),
            raw=data,
        )

    def submit_tool_results(self, response: LLMResponse, results: Sequence[ToolResult]) -> None:
        by_index = {i: r for i, r in enumerate(results)}
        content: list[dict[str, Any]] = []
        for index, call in enumerate(response.tool_calls):
            result = by_index.get(index)
            payload = jsonable(result.payload) if result is not None else {"error": "not executed"}
            is_error = bool(result is not None and result.is_error)
            if is_error:
                payload = {"error": payload}
            content.append(
                {
                    "type": "tool_result",
                    "tool_use_id": call.call_id or f"call_{index}",
                    "content": json.dumps(payload, default=str),
                    "is_error": is_error,
                }
            )
        self._messages.append({"role": "user", "content": content})

    def _post_messages(self) -> dict[str, Any]:
        body: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self._settings.max_output_tokens or 4096,
            "system": self._system_prompt,
            "messages": self._messages,
        }
        if self._settings.temperature is not None:
            body["temperature"] = self._settings.temperature
        if self._tools:
            body["tools"] = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.parameters,
                }
                for t in self._tools
            ]

        req = urllib.request.Request(
            self._base_url,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "x-api-key": self._api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self._settings.timeout_s) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"anthropic HTTP {exc.code}: {detail}") from exc

    @staticmethod
    def _content(parts: Sequence[Part]) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for part in parts:
            if isinstance(part, TextPart):
                out.append({"type": "text", "text": part.text})
            elif isinstance(part, ImagePart):
                out.append(
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": part.mime_type,
                            "data": base64.b64encode(part.data).decode("ascii"),
                        },
                    }
                )
        return out

    @staticmethod
    def _with_retries(fn: Any) -> Any:
        delay = 1.0
        for attempt in range(3):
            try:
                return fn()
            except Exception as exc:
                msg = str(exc).lower()
                if attempt == 2 or not any(tok in msg for tok in _TRANSIENT):
                    raise
                time.sleep(delay)
                delay *= 2.0
