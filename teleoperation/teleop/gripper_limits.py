"""Measured physical gripper range (degrees in lerobot's public frame).

Created by tools/measure_gripper.py. Nothing in the real-arm path moves the
gripper without it, because the open/closed ends differ per build.
"""
import json
from pathlib import Path

LIMITS_FILE = Path(__file__).resolve().parents[1] / "config" / "gripper_limits.json"
MARGIN_DEG = 5.0  # commands stay this far inside the measured ends


def load(path: Path = LIMITS_FILE):
    """Returns (open_deg, closed_deg) or None if not measured yet."""
    if not path.exists():
        return None
    d = json.loads(path.read_text())
    return float(d["open_deg"]), float(d["closed_deg"])


def save(open_deg: float, closed_deg: float, path: Path = LIMITS_FILE) -> None:
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({"open_deg": open_deg, "closed_deg": closed_deg}, indent=2))


def bounds(limits) -> tuple[float, float]:
    """(lo, hi) allowed command range, inside the physical ends."""
    lo, hi = sorted(limits)
    return lo + MARGIN_DEG, hi - MARGIN_DEG
