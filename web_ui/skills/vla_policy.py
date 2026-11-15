"""Pluggable VLA policy client for manipulation tasks (ROS-free)."""

from __future__ import annotations

import threading
from typing import Any

import numpy as np


class VLAError(RuntimeError):
    """The VLA policy failed or is not configured."""


class VLAPolicyClient:
    """Base interface for calling a trained VLA policy on live camera frames."""

    def __init__(self, cfg: dict[str, Any] | None = None) -> None:
        self.cfg = dict(cfg or {})
        self.backend = str(self.cfg.get("backend", "stub"))
        self.checkpoint = str(self.cfg.get("checkpoint", "") or "")
        self.timeout_s = float(self.cfg.get("timeout_s", 60.0))
        self._cancel = threading.Event()

    def cancel(self) -> None:
        self._cancel.set()

    def reset(self) -> None:
        self._cancel.clear()

    def execute(
        self,
        instruction: str,
        frames: dict[str, np.ndarray],
        *,
        target: str | None = None,
        destination: str | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Run the VLA policy for ``instruction`` using the latest camera frames.

        Replace or subclass this method when wiring in the trained VLA model.
        """
        if self._cancel.is_set():
            raise VLAError("VLA policy cancelled")
        cam_names = sorted(frames.keys())
        if dry_run:
            return {
                "success": True,
                "executed": False,
                "backend": self.backend,
                "instruction": instruction,
                "target": target,
                "destination": destination,
                "cameras": cam_names,
                "summary": f"dry run: would run VLA policy for {instruction!r}",
            }
        if self.backend == "stub":
            raise VLAError(
                "VLA policy backend is 'stub'; wire a trained VLA policy in web_ui/skills/vla_policy.py"
            )
        raise VLAError(f"unsupported VLA backend: {self.backend!r}")
