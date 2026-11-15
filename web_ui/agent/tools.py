"""Planner tool surface for VLA-backed manipulation (ROS-free)."""

from __future__ import annotations

from typing import Any

from ..types import ToolSchema

_DETECTION_PARAMETERS = {
    "type": "object",
    "properties": {
        "classes": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 32,
            "description": (
                "Optional short object names discovered in the image, e.g. can, bottle, paper cup, wrapper. "
                "Extends baseline classes. Omit to keep the current vocabulary."
            ),
        },
    },
    "additionalProperties": False,
}

TOOLS: list[ToolSchema] = [
    ToolSchema(
        name="detect_objects",
        description=(
            "Run local detection/segmentation on the table camera without moving the arm. "
            "Returns pixel boxes/masks and object labels."
        ),
        parameters=_DETECTION_PARAMETERS,
    ),
    ToolSchema(
        name="list_objects",
        description=(
            "Look at the table and return visible and remembered objects. "
            "Call this before manipulation and after a VLA policy rollout to verify the scene."
        ),
        parameters=_DETECTION_PARAMETERS,
    ),
    ToolSchema(
        name="run_vla_policy",
        description=(
            "Execute the trained VLA manipulation policy for one clear natural-language instruction "
            "(for example, 'pick up the aluminum can and place it in the bin'). "
            "The policy consumes the live camera feeds directly."
        ),
        parameters={
            "type": "object",
            "properties": {
                "instruction": {
                    "type": "string",
                    "description": "Clear single-step manipulation instruction for the VLA policy.",
                },
                "object": {
                    "type": "string",
                    "description": "Optional target object label from list_objects.",
                },
                "destination": {
                    "type": "string",
                    "description": "Optional destination (e.g. bin name or table).",
                },
            },
            "required": ["instruction"],
            "additionalProperties": False,
        },
    ),
    ToolSchema(
        name="task_done",
        description=(
            "Finish the user's request and report what happened. "
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
