"""OpenAI-compatible planner backend (OpenAI, vLLM, Ollama, LM Studio, ...).

Point ``vlm.base_url`` at anything that speaks ``/v1/chat/completions`` and set
``vlm.model`` to what that server calls the model. Vision is sent as a data-URL
image; tool calling uses the standard ``tools``/``tool_calls`` fields, or the JSON
protocol when ``tool_mode: json`` (small local models often need that).
"""

from __future__ import annotations

import base64
import os
import time
from typing import Any, Sequence

from ..config import VLMSettings
from ..types import ImagePart, LLMResponse, TextPart, ToolCall, ToolResult, ToolSchema
from .base import Part, jsonable

_TRANSIENT = ("429", "500", "502", "503", "504", "timeout", "temporarily", "overloaded")


class OpenAISession:
    name = "openai"

    def __init__(self, settings: VLMSettings, system_prompt: str, tools: Sequence[ToolSchema],
                 api_key: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - dependency is optional
            raise RuntimeError(
                "openai provider needs the openai package: pip install openai"
            ) from exc

        self.model = settings.model
        self._settings = settings
        self._tool_mode = settings.tool_mode
        self._tools = list(tools)
        key = api_key or os.environ.get(settings.api_key_env) or "not-needed"

        prompt = system_prompt
        if self._tool_mode == "json":
            from .json_tools import tool_prompt

            prompt = f"{system_prompt}\n\n{tool_prompt(tools)}"
        self._messages: list[dict[str, Any]] = [{"role": "system", "content": prompt}]
        self._client = OpenAI(
            api_key=key,
            base_url=settings.base_url or None,
            timeout=settings.timeout_s,
        )

    # ------------------------------------------------------------------ protocol
    def send(self, parts: Sequence[Part]) -> LLMResponse:
        self._messages.append({"role": "user", "content": self._content(parts)})
        response = self._with_retries(lambda: self._client.chat.completions.create(**self._request()))
        message = response.choices[0].message
        text = message.content or ""
        calls: list[ToolCall] = []
        for call in (getattr(message, "tool_calls", None) or []):
            arguments = call.function.arguments
            if isinstance(arguments, str):
                import json

                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}
            calls.append(ToolCall(name=str(call.function.name), arguments=dict(arguments or {}), call_id=call.id))
        if not calls and self._tool_mode == "json":
            from .json_tools import parse_tool_call

            parsed = parse_tool_call(text, self._tools)
            if parsed is not None:
                calls = [parsed]

        # Keep the assistant turn in history so tool results have something to answer.
        assistant: dict[str, Any] = {"role": "assistant", "content": text or None}
        if calls:
            assistant["tool_calls"] = [
                {
                    "id": call.call_id or f"call_{index}",
                    "type": "function",
                    "function": {"name": call.name, "arguments": _dumps(call.arguments)},
                }
                for index, call in enumerate(calls)
            ]
        self._messages.append(assistant)

        usage = {}
        if getattr(response, "usage", None) is not None:
            usage = {
                "input": int(getattr(response.usage, "prompt_tokens", 0) or 0),
                "output": int(getattr(response.usage, "completion_tokens", 0) or 0),
                "total": int(getattr(response.usage, "total_tokens", 0) or 0),
            }
        return LLMResponse(text=text, tool_calls=calls, model=self.model, usage=usage,
                           request_id=getattr(response, "id", None), raw=response)

    def submit_tool_results(self, response: LLMResponse, results: Sequence[ToolResult]) -> None:
        by_index = {i: r for i, r in enumerate(results)}
        for index, call in enumerate(response.tool_calls):
            result = by_index.get(index)
            payload = jsonable(result.payload) if result is not None else {"error": "not executed"}
            if result is not None and result.is_error:
                payload = {"error": payload}
            self._messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.call_id or f"call_{index}",
                    "name": call.name,
                    "content": _dumps({"result": payload}),
                }
            )

    # ------------------------------------------------------------------ plumbing
    def _request(self) -> dict[str, Any]:
        request: dict[str, Any] = {
            "model": self.model,
            "messages": self._messages,
            "temperature": self._settings.temperature,
            "max_tokens": self._settings.max_output_tokens,
        }
        if self._tool_mode == "native":
            request["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
                for tool in self._tools
            ]
            request["tool_choice"] = "auto"
        return request

    @staticmethod
    def _content(parts: Sequence[Part]) -> list[dict[str, Any]]:
        content: list[dict[str, Any]] = []
        for part in parts:
            if isinstance(part, ImagePart):
                encoded = base64.b64encode(part.data).decode("ascii")
                content.append(
                    {"type": "image_url", "image_url": {"url": f"data:{part.mime_type};base64,{encoded}"}}
                )
            else:
                content.append({"type": "text", "text": part.text})
        return content

    def _with_retries(self, call):
        last: Exception | None = None
        for attempt in range(self._settings.retries + 1):
            try:
                return call()
            except Exception as exc:  # noqa: BLE001 - SDK error types vary by version
                last = exc
                text = str(exc).lower()
                if attempt >= self._settings.retries or not any(t in text for t in _TRANSIENT):
                    raise RuntimeError(f"openai-compatible request failed: {_short(exc)}") from exc
                time.sleep(min(2.0 * (attempt + 1), 8.0))
        raise RuntimeError(f"openai-compatible request failed: {_short(last)}") from last


def _dumps(value: Any) -> str:
    import json

    return json.dumps(value, separators=(",", ":"), default=str)


def _short(exc: Exception | None) -> str:
    text = str(exc or "").strip().replace("\n", " ")
    return (text[:300] + "...") if len(text) > 300 else text


__all__ = ["OpenAISession", "TextPart"]
