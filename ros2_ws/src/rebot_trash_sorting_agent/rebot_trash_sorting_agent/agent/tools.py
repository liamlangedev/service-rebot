"""The planner's tool surface.

Deliberately small: four tools, one call per step. Everything the model can do to
the robot is here, which also means this is the whole safety surface.
"""

from __future__ import annotations

from typing import Any

from ..types import ToolSchema

TOOLS: list[ToolSchema] = [
    ToolSchema(
        name="list_objects",
        description=(
            "Look at the table and return the objects that are visible now, with their "
            "position in the robot base frame (metres, x is straight ahead of the arm, "
            "y is to the arm's left). Call this before the first pick and after any move "
            "that could have changed the scene."
        ),
        parameters={"type": "object", "properties": {}, "additionalProperties": False},
    ),
    ToolSchema(
        name="pick_and_place",
        description=(
            "Pick up one visible object and put it down. Runs the whole sequence: move "
            "above the object, descend, close the gripper, lift, move to the destination, "
            "release, retreat. Pass the detector's label exactly as list_objects returned it."
        ),
        parameters={
            "type": "object",
            "properties": {
                "object": {"type": "string", "description": "detector label of the object to pick"},
                "destination": {
                    "type": "string",
                    "description": (
                        "optional release target: a bin compartment name from the scene notes, "
                        "or 'table'. Omit for a free spot on the table."
                    ),
                },
            },
            "required": ["object"],
            "additionalProperties": False,
        },
    ),
    ToolSchema(
        name="move_home",
        description="Move the arm to its folded home pose, clear of the table. Use it to retreat.",
        parameters={"type": "object", "properties": {}, "additionalProperties": False},
    ),
    ToolSchema(
        name="task_done",
        description=(
            "Finish the task. Call it exactly once, as the last step, whatever the outcome. "
            "success must reflect what the tools actually did."
        ),
        parameters={
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "summary": {"type": "string", "description": "one or two sentences for the operator"},
            },
            "required": ["success", "summary"],
            "additionalProperties": False,
        },
    ),
]

TOOL_NAMES = frozenset(t.name for t in TOOLS)


def destination_arg(arguments: dict[str, Any]) -> str | None:
    value = arguments.get("destination")
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def object_arg(arguments: dict[str, Any]) -> str:
    value = arguments.get("object")
    if value is None:
        raise ValueError("pick_and_place needs an 'object' argument")
    text = str(value).strip()
    if not text:
        raise ValueError("pick_and_place got an empty object name")
    return text
