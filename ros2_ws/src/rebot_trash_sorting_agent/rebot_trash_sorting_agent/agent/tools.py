"""The planner's tool surface.

One tool call per step. Everything the model can do to
the robot is here, which also means this is the whole safety surface.
"""

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
            "description": "Optional short object names discovered in the image, e.g. can, bottle, paper cup, wrapper. Extends baseline classes, not an assertion that objects exist. Omit to keep the current vocabulary.",
        },
    },
    "additionalProperties": False,
}

TOOLS: list[ToolSchema] = [
    ToolSchema(
        name="detect_objects",
        description="Run local detection/segmentation without moving the arm. Suggest classes from the camera image on the first call. Returns pixel boxes/masks, calibrated positions and front-view heights when available, and publishes overlays.",
        parameters=_DETECTION_PARAMETERS,
    ),
    ToolSchema(
        name="list_objects",
        description=(
            "Look at the table and return the objects that are visible now, with their "
            "position in the robot base frame (metres, x is straight ahead of the arm, "
            "y is to the arm's left). Call this before the first pick and after any move "
            "that could have changed the scene."
        ),
        parameters=_DETECTION_PARAMETERS,
    ),
    ToolSchema(
        name="move_above_object",
        description="Move only to a pre-grasp pose above one uniquely detected object. Do not descend, grasp, open or close the gripper. Use when asked to hover or go above an object, not pick it up.",
        parameters={
            "type": "object",
            "properties": {
                "object": {"type": "string", "description": "Visible detector label returned by detect_objects"},
                "clearance_m": {
                    "type": "number",
                    "minimum": 0.02,
                    "maximum": 0.25,
                    "description": "Minimum clearance above measured top, in metres; default 0.10",
                },
            },
            "required": ["object"],
            "additionalProperties": False,
        },
    ),
    ToolSchema(
        name="move_to_pose",
        description="Move only the tool to an explicit pose in base_link: XYZ in metres, yaw/tilt in degrees (default zero, tool down). Does not operate the gripper. Use only supplied coordinates or measured tool results, never guessed coordinates from image pixels. IK and configured tool limits are checked.",
        parameters={
            "type": "object",
            "properties": {
                "x": {"type": "number"},
                "y": {"type": "number"},
                "z": {"type": "number"},
                "yaw_deg": {"type": "number"},
                "tilt_deg": {"type": "number"},
            },
            "required": ["x", "y", "z"],
            "additionalProperties": False,
        },
    ),
    ToolSchema(
        name="grasp_object",
        description="Approach and grasp one detected object, verify hold, and optionally lift (default true). Keeps holding the object; does not place it or return home. Set lift=false when asked only to close on the object without lifting.",
        parameters={
            "type": "object",
            "properties": {
                "object": {"type": "string"},
                "lift": {"type": "boolean"},
            },
            "required": ["object"],
            "additionalProperties": False,
        },
    ),
    ToolSchema(
        name="place_object",
        description="Place and release the currently held object at a destination, then retreat. Requires a previous successful grasp/close; the held state persists between user tasks. Does not pick another object.",
        parameters={
            "type": "object",
            "properties": {
                "destination": {
                    "type": "string",
                    "description": "Configured bin name or table; omitted means a free spot",
                },
            },
            "additionalProperties": False,
        },
    ),
    ToolSchema(
        name="open_gripper",
        description="Open the gripper without moving the arm. Releases any held object at the current position; use only when explicitly requested or intended by the task.",
        parameters={"type": "object", "properties": {}, "additionalProperties": False},
    ),
    ToolSchema(
        name="close_gripper",
        description="Close the gripper at the current pose without moving the arm. Returns measured holding state; does not establish the identity of an untracked object.",
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
