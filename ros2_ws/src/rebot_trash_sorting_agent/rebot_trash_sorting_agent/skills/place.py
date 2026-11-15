"""Where to put an object down.

Two destinations exist:

* a **bin compartment** - the tool cannot reach the bin straight down (measured:
  no IK solution at any release height), so the release pose leans towards +y over
  the rim. 40 deg reaches both compartments, 50 deg is the fallback for the far one.
* a **free spot on the table** - chosen from a grid so the object lands clear of the
  walls, the bin and the other objects, and only where the arm can actually reach.
"""

from __future__ import annotations

import math
from typing import Callable, Iterable, Sequence

from ..types import PlaceTarget, WorldObject
from .poses import ToolPose

IkCheck = Callable[[ToolPose], bool]


def bin_target(name: str, places: dict, motion: dict) -> PlaceTarget:
    compartments = dict((places.get("bin") or {}).get("compartments") or {})
    if name not in compartments:
        raise KeyError(f"unknown bin compartment {name!r}; have {sorted(compartments)}")
    rim_z = float((places.get("bin") or {}).get("rim_z", 0.108))
    cfg = dict(motion.get("place") or {})
    clearance = float(cfg.get("bin_release_clearance", 0.05))
    tilt = float(cfg.get("bin_tilt_deg", 40.0))
    spot = compartments[name]
    return PlaceTarget(
        name=name,
        x=float(spot["x"]),
        y=float(spot["y"]),
        z=rim_z + clearance,
        kind="bin",
        tilt_deg=tilt,
    )


def bin_targets(name: str, places: dict, motion: dict) -> list[PlaceTarget]:
    """The primary leaning release plus the configured tilt fallbacks."""
    primary = bin_target(name, places, motion)
    fallbacks = [float(t) for t in (motion.get("place") or {}).get("bin_tilt_fallbacks_deg", [])]
    out = [primary]
    for tilt in fallbacks:
        if abs(tilt - primary.tilt_deg) > 1e-6:
            out.append(PlaceTarget(primary.name, primary.x, primary.y, primary.z, "bin", tilt))
    return out


def table_spot(objects: Iterable[WorldObject], places: dict, motion: dict,
               ik_check: IkCheck | None = None, target_objects: Sequence[str] = ()) -> PlaceTarget:
    """Best free spot on the table, nearest to the arm first."""
    table_z = float((places.get("table") or {}).get("z", -0.012))
    cfg = dict(motion.get("place") or {})
    release = float(cfg.get("table_release_height", 0.06))
    clearance = float(cfg.get("spot_clearance", 0.06))
    grid = dict(cfg.get("free_spots") or {})
    ws = dict((places.get("workspace") or {}))
    xs = [float(v) for v in grid.get("x", [0.18, 0.22, 0.26, 0.30])]
    ys = [float(v) for v in grid.get("y", [-0.16, -0.08, 0.0, 0.08, 0.16])]
    if ws.get("x"):
        xs = [x for x in xs if ws["x"][0] <= x <= ws["x"][1]] or xs
    if ws.get("y"):
        ys = [y for y in ys if ws["y"][0] <= y <= ws["y"][1]] or ys

    obstacles = [o for o in objects if o.label not in target_objects]
    bin_boxes = [box for box in ((places.get("bin") or {}).get("boxes") or {}).values()]
    wall_boxes = list((places.get("walls") or {}).values())

    scored: list[tuple[float, float, float]] = []
    for x in xs:
        for y in ys:
            if _inside_any(x, y, bin_boxes) or _near_any(x, y, wall_boxes, clearance):
                continue
            clear = min((math.dist((x, y), o.xy) for o in obstacles), default=1.0)
            if clear < clearance:
                continue
            # Prefer spots in front of the arm and far from everything else.
            score = clear - 0.25 * math.dist((x, y), (0.24, 0.0))
            scored.append((score, x, y))
    scored.sort(reverse=True)

    for _, x, y in scored:
        target = PlaceTarget(name="table", x=x, y=y, z=table_z + release, kind="table")
        if ik_check is None or ik_check(ToolPose(x, y, target.z)):
            return target
    # Nothing was clear: fall back to the grid centre so the caller gets a real goal
    # and MoveIt/IK can reject it with a useful message.
    return PlaceTarget(name="table", x=0.24, y=0.0, z=table_z + release, kind="table")


def resolve_place(name: str | None, places: dict, motion: dict, objects: Iterable[WorldObject] = (),
                  ik_check: IkCheck | None = None) -> list[PlaceTarget]:
    """Ordered release targets for a tool argument.

    ``None`` / ``"table"`` -> a free table spot, then nothing else.
    A bin name            -> the bin, then its tilt fallbacks, then a table spot.
    """
    objects = list(objects)
    if name and name in dict((places.get("bin") or {}).get("compartments") or {}):
        return [*bin_targets(name, places, motion), table_spot(objects, places, motion, ik_check)]
    return [table_spot(objects, places, motion, ik_check)]


def _inside_any(x: float, y: float, boxes: Iterable[Sequence[float]]) -> bool:
    for box in boxes:
        x0, x1, y0, y1 = float(box[0]), float(box[1]), float(box[2]), float(box[3])
        if x0 <= x <= x1 and y0 <= y <= y1:
            return True
    return False


def _near_any(x: float, y: float, boxes: Iterable[Sequence[float]], margin: float) -> bool:
    for box in boxes:
        x0, x1, y0, y1 = float(box[0]), float(box[1]), float(box[2]), float(box[3])
        if x0 - margin <= x <= x1 + margin and y0 - margin <= y <= y1 + margin:
            return True
    return False
