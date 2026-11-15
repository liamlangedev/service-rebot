"""Keyless planner for smoke tests and CI.

It is not clever on purpose: list the scene, pick the first visible object (a can
if one is there), put it in the near bin compartment, finish. That is enough to
exercise perception, MoveIt, the gripper and the trace end to end with no network
and no API key:

    ros2 launch rebot_trash_sorting_agent agent.launch.py provider:=mock
"""

from __future__ import annotations

from typing import Sequence

from ..types import LLMResponse, ToolCall, ToolResult, ToolSchema
from .base import Part


class MockSession:
    name = "mock"

    def __init__(self, settings=None, system_prompt: str = "", tools: Sequence[ToolSchema] = ()) -> None:
        self.model = getattr(settings, "model", "mock") or "mock"
        self._last: ToolResult | None = None
        self._history: list[ToolResult] = []
        self.turns = 0

    def send(self, parts: Sequence[Part]) -> LLMResponse:
        self.turns += 1
        call = self._decide()
        return LLMResponse(text=f"[mock] {call.name}", tool_calls=[call], model=self.model,
                           usage={"input": 0, "output": 0})

    def submit_tool_results(self, response: LLMResponse, results: Sequence[ToolResult]) -> None:
        self._last = results[0] if results else None
        self._history.extend(results)

    # ------------------------------------------------------------------ policy
    def _decide(self) -> ToolCall:
        last = self._last
        if last is None or last.name == "list_objects":
            if last is None:
                return ToolCall(name="list_objects", arguments={})
            visible = [o for o in last.payload.get("objects", []) if o.get("state") == "visible"]
            if not visible:
                return ToolCall(name="task_done", arguments={"success": False, "summary": "no objects visible"})
            chosen = next((o for o in visible if "can" in str(o.get("label", ""))), visible[0])
            return ToolCall(
                name="pick_and_place",
                arguments={"object": chosen.get("label"), "destination": "bin_0"},
            )
        if last.name == "pick_and_place":
            if last.payload.get("success"):
                return ToolCall(
                    name="task_done",
                    arguments={"success": True, "summary": f"placed {last.payload.get('object', 'object')}"},
                )
            return ToolCall(name="task_done", arguments={"success": False, "summary": "pick failed"})
        return ToolCall(name="task_done", arguments={"success": False, "summary": "nothing left to do"})
