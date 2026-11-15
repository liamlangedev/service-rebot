"""Google Gemini planner backend (``google-genai`` SDK).

Default model: ``gemini-3.8-flash`` - GA, 1M-token context, image input, native
function calling and structured output, with thinking levels ``low|medium|high``.
``low`` is right for a one-tool-per-step loop: the planning is short, the latency
and the bill are not.

The key is read from the environment (``GEMINI_API_KEY``); the node loads a
gitignored ``.env`` first. It is never logged.
"""

from __future__ import annotations

import os
import time
from typing import Any, Sequence

from ..config import VLMSettings
from ..types import ImagePart, LLMResponse, TextPart, ToolCall, ToolResult, ToolSchema
from .base import Part, jsonable

_TRANSIENT = ("429", "500", "502", "503", "504", "deadline", "timeout", "unavailable", "overloaded")


class GeminiSession:
    name = "gemini"

    def __init__(self, settings: VLMSettings, system_prompt: str, tools: Sequence[ToolSchema],
                 api_key: str | None = None) -> None:
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:  # pragma: no cover - dependency is optional
            raise RuntimeError(
                "gemini provider needs the google-genai package: pip install google-genai "
                "(or run scripts/setup_agent.sh)"
            ) from exc

        self._types = types
        self.model = settings.model
        self._settings = settings
        self._tool_mode = settings.tool_mode
        self._pending: list[Any] = []

        key = api_key or os.environ.get(settings.api_key_env) or os.environ.get("GOOGLE_API_KEY")
        if not key:
            raise RuntimeError(
                f"no Gemini API key: set {settings.api_key_env} (e.g. in ros2_ws/.env)"
            )

        http_options = None
        try:
            http_options = types.HttpOptions(timeout=int(settings.timeout_s * 1000))
        except Exception:  # noqa: BLE001 - older SDKs take timeout differently
            http_options = None
        self._client = genai.Client(api_key=key, **({"http_options": http_options} if http_options else {}))

        prompt = system_prompt
        if self._tool_mode == "json":
            from .json_tools import tool_prompt

            prompt = f"{system_prompt}\n\n{tool_prompt(tools)}"

        config_kwargs: dict[str, Any] = {
            "system_instruction": prompt,
            "temperature": settings.temperature,
            "max_output_tokens": settings.max_output_tokens,
        }
        if self._tool_mode == "native":
            config_kwargs["tools"] = [self._tool(tools)]
        if settings.thinking_level:
            try:
                config_kwargs["thinking_config"] = types.ThinkingConfig(thinking_level=settings.thinking_level)
            except Exception:  # noqa: BLE001 - not every model/SDK has thinking levels
                pass
        try:
            config = types.GenerateContentConfig(**config_kwargs)
        except TypeError:
            config_kwargs.pop("thinking_config", None)
            config = types.GenerateContentConfig(**config_kwargs)
        self._config = config
        self._chat = self._client.chats.create(model=self.model, config=config)

    # ------------------------------------------------------------------ SDK glue
    def _tool(self, tools: Sequence[ToolSchema]) -> Any:
        types = self._types
        declarations = []
        for tool in tools:
            try:
                declarations.append(
                    types.FunctionDeclaration(
                        name=tool.name,
                        description=tool.description,
                        parameters_json_schema=tool.parameters,
                    )
                )
            except TypeError:  # older google-genai: build a Schema by hand
                declarations.append(
                    types.FunctionDeclaration(
                        name=tool.name,
                        description=tool.description,
                        parameters=types.Schema(**tool.parameters),
                    )
                )
        return types.Tool(function_declarations=declarations)

    def _part(self, part: Part) -> Any:
        types = self._types
        if isinstance(part, ImagePart):
            return types.Part.from_bytes(data=part.data, mime_type=part.mime_type)
        return types.Part.from_text(text=part.text)

    # ------------------------------------------------------------------ protocol
    def send(self, parts: Sequence[Part]) -> LLMResponse:
        message = [*self._pending, *(self._part(p) for p in parts)]
        self._pending = []
        response = self._with_retries(lambda: self._chat.send_message(message))

        text = getattr(response, "text", None) or ""
        calls: list[ToolCall] = []
        for call in (getattr(response, "function_calls", None) or []):
            calls.append(ToolCall(name=str(call.name), arguments=dict(call.args or {}), call_id=getattr(call, "id", None)))
        if not calls and self._tool_mode == "json":
            from .json_tools import parse_tool_call

            parsed = parse_tool_call(text)
            if parsed is not None:
                calls = [parsed]

        usage = {}
        meta = getattr(response, "usage_metadata", None)
        if meta is not None:
            for field, key in (("prompt_token_count", "input"), ("candidates_token_count", "output"),
                               ("total_token_count", "total"), ("thoughts_token_count", "thoughts")):
                value = getattr(meta, field, None)
                if value:
                    usage[key] = int(value)

        return LLMResponse(
            text=text,
            tool_calls=calls,
            model=self.model,
            usage=usage,
            request_id=getattr(response, "response_id", None),
            raw=response,
        )

    def submit_tool_results(self, response: LLMResponse, results: Sequence[ToolResult]) -> None:
        types = self._types
        by_index = {i: r for i, r in enumerate(results)}
        parts = []
        for index, call in enumerate(response.tool_calls):
            result = by_index.get(index)
            payload = jsonable(result.payload) if result is not None else {"error": "not executed"}
            if result is not None and result.is_error:
                payload = {"error": payload}
            parts.append(types.Part.from_function_response(name=call.name, response={"result": payload}))
        self._pending = parts

    # ------------------------------------------------------------------ plumbing
    def _with_retries(self, call):
        last: Exception | None = None
        for attempt in range(self._settings.retries + 1):
            try:
                return call()
            except Exception as exc:  # noqa: BLE001 - SDK error types vary by version
                last = exc
                text = str(exc).lower()
                if attempt >= self._settings.retries or not any(t in text for t in _TRANSIENT):
                    raise RuntimeError(f"gemini request failed: {_short(exc)}") from exc
                time.sleep(min(2.0 * (attempt + 1), 8.0))
        raise RuntimeError(f"gemini request failed: {_short(last)}") from last


def _short(exc: Exception | None) -> str:
    text = str(exc or "").strip().replace("\n", " ")
    return (text[:300] + "...") if len(text) > 300 else text
