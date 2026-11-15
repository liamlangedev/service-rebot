"""The plan-act loop: one tool call per step, with the camera and the scene in front.

Shape taken from the WRC pipeline, which got this right: a fresh image and a
compact scene summary every step, exactly one tool call per turn, the tool's JSON
result fed straight back, and a hard step budget. The model never gets to narrate
several actions and then watch them drift.
"""

from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any, Callable, Sequence

from ..types import ImagePart, LLMResponse, TextPart, TaskResult, ToolCall, ToolResult, ToolSchema
from ..vlm.base import ChatSession
from .events import EventLog
from .tools import TOOL_NAMES

ToolRunner = Callable[[str, dict[str, Any]], ToolResult]
SceneProvider = Callable[[], str]
Capture = Callable[[], bytes | None]


@dataclass
class OrchestratorSettings:
    max_steps: int = 12
    timeout_s: float = 240.0
    max_consecutive_errors: int = 3


class Orchestrator:
    def __init__(self, session: ChatSession, tools: Sequence[ToolSchema], runner: ToolRunner,
                 events: EventLog, settings: OrchestratorSettings, scene: SceneProvider,
                 capture: Capture | None = None) -> None:
        self._session = session
        self._tools = list(tools)
        self._runner = runner
        self._events = events
        self._settings = settings
        self._scene = scene
        self._capture = capture
        self._cancelled = False
        self._current_call: str | None = None

    # ------------------------------------------------------------------ control
    def cancel(self) -> None:
        self._cancelled = True

    @property
    def busy(self) -> bool:
        return self._current_call is not None

    # ------------------------------------------------------------------ loop
    def run(self, task: str) -> TaskResult:
        task = (task or "").strip()
        if not task:
            return TaskResult(task="", success=False, summary="empty task", steps=0, error="empty task")

        started = time.monotonic()
        self._events.bind(task=task)
        self._events.emit("task_start", scene=self._scene())

        steps = 0
        errors = 0
        last_summary = ""
        try:
            while steps < self._settings.max_steps:
                if self._cancelled:
                    return TaskResult(task, False, last_summary or "stopped", steps, stopped=True)
                if time.monotonic() - started > self._settings.timeout_s:
                    return TaskResult(task, False, last_summary, steps, error="task timeout")

                parts = self._turn_parts(task, steps)
                turn_started = time.monotonic()
                response = self._session.send(parts)
                self._events.emit(
                    "planner_turn",
                    step=steps,
                    latency_s=round(time.monotonic() - turn_started, 3),
                    text=_short(response.text),
                    tool_calls=[c.name for c in response.tool_calls],
                    usage=response.usage,
                    model=response.model,
                )

                call = response.first_call
                if call is None:
                    # JSON mode can fail to produce a call; ask once more, then stop.
                    errors += 1
                    self._events.emit("planner_no_call", step=steps, text=_short(response.text))
                    if errors >= self._settings.max_consecutive_errors:
                        return TaskResult(task, False, "planner returned no tool call", steps,
                                          error="no tool call")
                    self._session.submit_tool_results(
                        response, [ToolResult("planner", {"error": "reply with one tool call"}, True)]
                    )
                    continue

                if call.name == "task_done":
                    args = call.arguments or {}
                    success = bool(args.get("success", False))
                    last_summary = str(args.get("summary", "")).strip()
                    self._events.emit("task_done", step=steps, success=success, summary=last_summary)
                    return TaskResult(task, success, last_summary or ("done" if success else "failed"), steps + 1)

                self._current_call = call.name
                result = self._execute(call)
                self._current_call = None
                steps += 1

                if result.is_error:
                    errors += 1
                else:
                    errors = 0
                self._events.emit(
                    "tool_result",
                    step=steps,
                    tool=result.name,
                    ok=not result.is_error,
                    result=result.payload,
                )
                if isinstance(result.payload.get("summary"), str):
                    last_summary = result.payload["summary"]

                self._session.submit_tool_results(response, [result])
                if errors >= self._settings.max_consecutive_errors:
                    return TaskResult(task, False, last_summary or "too many tool errors", steps,
                                      error=f"{errors} consecutive tool errors")

            return TaskResult(task, False, last_summary or "step limit reached", steps, error="step limit")
        except Exception as exc:  # noqa: BLE001 - the node must survive any planner/tool failure
            self._current_call = None
            self._events.emit("task_error", error=str(exc))
            return TaskResult(task, False, last_summary, steps, error=str(exc))

    # ------------------------------------------------------------------ helpers
    def _turn_parts(self, task: str, step: int) -> list[TextPart | ImagePart]:
        scene = self._scene()
        if step == 0:
            text = f"Task: {task}\n\nScene now:\n{scene}"
        else:
            text = f"Scene now:\n{scene}"
        parts: list[TextPart | ImagePart] = [TextPart(text)]
        if self._capture is not None:
            try:
                image = self._capture()
            except Exception as exc:  # noqa: BLE001 - a dead camera must not abort the task
                image = None
                self._events.emit("camera_error", error=str(exc))
            if image:
                self._events.save_image(f"step{step:02d}.jpg", image)
                parts.append(ImagePart(image))
        return parts

    def _execute(self, call: ToolCall) -> ToolResult:
        if call.name not in TOOL_NAMES:
            return ToolResult(call.name, {"error": f"unknown tool {call.name!r}"}, True)
        started = time.monotonic()
        try:
            result = self._runner(call.name, dict(call.arguments or {}))
        except Exception as exc:  # noqa: BLE001 - surface tool failures to the planner as data
            result = ToolResult(call.name, {"error": str(exc)}, True)
        duration = round(time.monotonic() - started, 3)
        self._events.emit("tool_call", tool=call.name, arguments=dict(call.arguments or {}), duration_s=duration)
        return result


def _short(text: str | None, limit: int = 400) -> str:
    text = (text or "").strip().replace("\n", " ")
    return (text[:limit] + "...") if len(text) > limit else text


__all__ = ["Orchestrator", "OrchestratorSettings", "LLMResponse"]
