"""Image preparation and the prompted-JSON tool protocol.

``tool_mode: json`` exists for vision models that are fine at seeing but unreliable
at native function calling. The tools are described in the system prompt and the
model must answer with a single JSON object; the parser is deliberately forgiving
about code fences and extra prose, strict about the payload.
"""

from __future__ import annotations

import json
import re
from typing import Any, Sequence

from ..types import ToolCall, ToolSchema

_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def encode_jpeg(bgr: Any, max_side: int = 1024, quality: int = 85) -> bytes:
    """Encode an HxWx3 BGR array as JPEG, downscaling the longest side."""
    import cv2
    import numpy as np

    image = np.asarray(bgr)
    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    height, width = image.shape[:2]
    scale = min(1.0, float(max_side) / max(height, width))
    if scale < 1.0:
        image = cv2.resize(image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)
    ok, buffer = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), int(quality)])
    if not ok:
        raise RuntimeError("JPEG encoding failed")
    return buffer.tobytes()


def tool_prompt(tools: Sequence[ToolSchema]) -> str:
    """The block appended to the system prompt in JSON tool mode."""
    lines = [
        "TOOLS",
        "Reply with exactly one JSON object and nothing else:",
        '{"tool": "<tool name>", "arguments": { ... }}',
        "Call exactly one tool per step. The tool result arrives in the next message.",
        "",
    ]
    for tool in tools:
        lines.append(f"- {tool.name}: {tool.description}")
        lines.append(f"  arguments (JSON Schema): {json.dumps(tool.parameters, separators=(',', ':'))}")
    lines.append("")
    lines.append('When the task is finished, call task_done with success and a short summary.')
    return "\n".join(lines)


def parse_tool_call(text: str, tools: Sequence[ToolSchema] | None = None) -> ToolCall | None:
    """Extract the first well-formed tool call from a model reply."""
    if not text:
        return None
    known = {t.name for t in tools} if tools else None
    for candidate in _candidates(text):
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        call = _as_call(data, known)
        if call is not None:
            return call
    return None


def _candidates(text: str) -> list[str]:
    out: list[str] = []
    for match in _FENCE.finditer(text):
        out.append(match.group(1).strip())
    stripped = text.strip()
    out.append(stripped)
    # balanced-brace scan for a JSON object embedded in prose
    for start, char in enumerate(text):
        if char != "{":
            continue
        depth, in_string, escape = 0, False, False
        for index in range(start, len(text)):
            current = text[index]
            if in_string:
                if escape:
                    escape = False
                elif current == "\\":
                    escape = True
                elif current == '"':
                    in_string = False
                continue
            if current == '"':
                in_string = True
            elif current == "{":
                depth += 1
            elif current == "}":
                depth -= 1
                if depth == 0:
                    out.append(text[start : index + 1])
                    break
    return out


def _as_call(data: Any, known: set[str] | None) -> ToolCall | None:
    if not isinstance(data, dict):
        return None
    name = data.get("tool") or data.get("name") or data.get("tool_name")
    args = data.get("arguments", data.get("args", data.get("parameters", {})))
    if not isinstance(name, str):
        return None
    if not isinstance(args, dict):
        try:
            args = json.loads(args)
        except (TypeError, json.JSONDecodeError):
            return None
    if known is not None and name not in known:
        # "arguments" nested one level down happens with some small models
        nested = args.get("tool")
        if isinstance(nested, str) and nested in known:
            return ToolCall(name=nested, arguments=args.get("arguments") or {})
        return None
    return ToolCall(name=name, arguments=args)
