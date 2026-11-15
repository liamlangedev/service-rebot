"""Grasp pose generation from an RGB detection.

The object is a vertical-ish thing standing on the table plane, so a top-down
pinch is the starting point. Nothing here has a per-class size table: the width and
the orientation come from the mask's bottom edge, measured through the table
homography by :meth:`TableMap.footprint`.

* **orientation** - the jaw closes perpendicular to the visible bottom edge, so a
  box is taken across its depth instead of its long side. The measured yaw is
  candidate one; yaw + 90 deg is the fallback if that orientation has no IK.
* **height** - the object's height is not observable with one RGB view and a plane
  homography, so pinch heights are a short ladder (low first). If the jaws close on
  nothing, the skill opens, retreats and tries the next rung; that is also how a
  person recovers from grabbing too low.
* **width** - the projected bottom edge is an upper bound on the jaw opening. It is
  used to warn, not to refuse: the jaw stalls on the object anyway.

All of this is pure geometry; the ROS side turns the poses into MoveGroup goals.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..types import GraspCandidate, WorldObject
from .poses import ToolPose


@dataclass
class GraspPlan:
    label: str
    pre_grasp: ToolPose
    grasp: ToolPose
    lift: ToolPose
    candidates: list[GraspCandidate] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def best(self) -> GraspCandidate | None:
        return self.candidates[0] if self.candidates else None

    @property
    def feasible(self) -> bool:
        return bool(self.candidates)

    def offset(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0) -> "GraspPlan":
        """Shift all three poses together (wrist view correction)."""
        return GraspPlan(
            label=self.label,
            pre_grasp=self.pre_grasp.offset(dx=dx, dy=dy, dz=dz),
            grasp=self.grasp.offset(dx=dx, dy=dy, dz=dz),
            lift=self.lift.offset(dx=dx, dy=dy, dz=dz),
            candidates=list(self.candidates),
            notes=list(self.notes),
        )

    def summary(self) -> dict:
        best = self.best
        return {
            "label": self.label,
            "grasp": self.grasp.summary(),
            "pre_grasp": self.pre_grasp.summary(),
            "width_m": round(best.width_m, 4) if best else None,
            "yaw_deg": round(best.yaw_deg, 1) if best else None,
            "pinch_m": round(best.pinch_m, 4) if best else None,
            "candidates": [c.summary() for c in self.candidates],
            "notes": self.notes,
        }


def plan_grasp(obj: WorldObject, motion: dict, table_z: float) -> GraspPlan:
    """Turn one detection into ordered grasp candidates in the base frame."""
    cfg = dict(motion.get("grasp") or {})
    tcp_below = float(cfg.get("tcp_below_pinch", 0.020))
    pre_clear = float(cfg.get("pre_grasp_clearance", 0.12))
    lift_clear = float(cfg.get("lift_clearance", 0.10))
    max_open = float(cfg.get("max_open_width_m", 0.095))
    margin = float(cfg.get("min_width_margin_m", 0.005))
    assumed_width = float(cfg.get("assumed_width_m", 0.04))
    pinches = [float(p) for p in (cfg.get("pinch_heights_m") or [cfg.get("pinch_height", 0.035)])]

    notes: list[str] = []
    width = float(obj.width_m) if obj.width_m > 0.005 else assumed_width
    if obj.width_m <= 0.005:
        notes.append(
            f"{obj.label}: bottom edge too short to measure; assuming "
            f"{assumed_width * 100:.1f} cm wide"
        )
    usable = max_open - margin
    fits = width <= usable
    if not fits:
        notes.append(
            f"{obj.label}: visible edge {width * 100:.1f} cm, jaw is "
            f"{max_open * 100:.1f} cm (usable {usable * 100:.1f} cm) - close across "
            "the narrow side or the grasp will slip"
        )
    elif width > 0.8 * usable:
        notes.append(f"{obj.label}: close to the jaw limit ({width * 100:.1f} cm)")

    yaw0 = _normalise_deg(float(obj.yaw_deg))
    offsets = [float(v) for v in (cfg.get("yaw_candidates_deg") or [0.0, 90.0])]
    yaws = [_normalise_deg(yaw0 + offset) for offset in offsets]

    candidates: list[GraspCandidate] = []
    index = 0
    for pinch in pinches:
        tcp_z = table_z + pinch - tcp_below
        floor = table_z + 0.002
        if tcp_z < floor:
            notes.append(
                f"pinch {pinch * 100:.1f} cm would put the fingertip in the table; "
                f"raised to {floor + tcp_below - table_z:.3f} m"
            )
            tcp_z = floor
        actual_pinch = tcp_z + tcp_below - table_z
        for yaw in yaws:
            score = 1.0 - 0.05 * index
            if not fits:
                score -= 0.5
            candidates.append(
                GraspCandidate(
                    x=float(obj.x),
                    y=float(obj.y),
                    z=tcp_z,
                    yaw_deg=yaw,
                    width_m=width,
                    score=max(score, 0.0),
                    label=obj.label,
                    pinch_m=actual_pinch,
                )
            )
            index += 1

    best = candidates[0]
    grasp_pose = ToolPose(best.x, best.y, best.z, best.yaw_deg)
    return GraspPlan(
        label=obj.label,
        pre_grasp=ToolPose(best.x, best.y, best.z + pre_clear, best.yaw_deg),
        grasp=grasp_pose,
        lift=ToolPose(best.x, best.y, best.z + lift_clear, best.yaw_deg),
        candidates=candidates,
        notes=notes,
    )


def _normalise_deg(angle: float) -> float:
    """Map an orientation onto (-90, 90] degrees: a line has no direction."""
    return ((float(angle) + 90.0) % 180.0) - 90.0
