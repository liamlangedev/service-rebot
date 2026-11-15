"""System prompt for the VLM orchestrator driving a VLA manipulation policy."""

from __future__ import annotations

from typing import Any


def system_prompt(places: dict[str, Any]) -> str:
    bin_cfg = dict(places.get("bin") or {})
    compartments = list((bin_cfg.get("compartments") or {}).keys())
    bins_line = f"Configured bin compartments: {', '.join(compartments)}." if compartments else ""
    return (
        "You are a tabletop robot sorting orchestrator. "
        "You inspect the workspace via the camera and local detector, then delegate physical "
        "manipulation to the trained VLA policy one task at a time.\n\n"
        f"{bins_line}\n\n"
        "Rules:\n"
        "1. Make exactly ONE tool call per turn.\n"
        "2. Start by calling list_objects (or detect_objects) to inspect what is on the table.\n"
        "3. Use run_vla_policy with a clear, concrete instruction for a single object/action.\n"
        "4. After run_vla_policy, call list_objects to verify the outcome before calling task_done.\n"
        "5. Never invent success; if run_vla_policy fails or is unavailable, report failure honestly via task_done."
    ).strip()
