"""World model: fuses 2D detections from the fixed cameras into 3D objects on the table.

* Seen by >= 2 scene cameras: the rays are triangulated (gives height too).
* Seen by 1 camera: the ray is intersected with the table plane at half the default
  object height. The wrist camera corrects the remaining x/y error before grasping.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field

import numpy as np

from autonomy.geometry import ray_plane_z, triangulate_rays
from autonomy.perception import Detection, label_matches


@dataclass
class Zone:
    name: str
    center: tuple[float, float]
    size: tuple[float, float]          # full x / y extent [m]
    drop_height: float = 0.02          # release height above the zone surface [m]

    def contains(self, xy, margin: float = 0.0) -> bool:
        return (abs(xy[0] - self.center[0]) <= self.size[0] / 2 + margin and
                abs(xy[1] - self.center[1]) <= self.size[1] / 2 + margin)


@dataclass
class Obj:
    id: str
    label: str
    pos: np.ndarray                    # approx. centre [m]
    height: float
    yaw: float | None = None           # long axis direction in the table plane [rad]
    width: float | None = None         # short side [m] (what the gripper closes on)
    length: float | None = None
    views: list[str] = field(default_factory=list)
    score: float = 1.0

    def summary(self) -> dict:
        return {"id": self.id, "label": self.label, "xyz_m": np.round(self.pos, 3).tolist(),
                "height_m": round(self.height, 3),
                "width_m": None if self.width is None else round(self.width, 3),
                "seen_by": self.views}


@dataclass
class WorldConfig:
    table_z: float = 0.03
    table_region: tuple = (0.10, -0.30, 0.75, 0.30)     # x0, y0, x1, y1 accepted area
    default_height: float = 0.05
    max_tri_residual: float = 0.03
    merge_radius: float = 0.04
    max_object_size: float = 0.15      # larger blobs are background (floor, mats, bins)


class WorldModel:
    def __init__(self, rig, detector, cfg: WorldConfig, zones: list[Zone]):
        self.rig, self.detector, self.cfg = rig, detector, cfg
        self.zones = {z.name: z for z in zones}
        self.objects: list[Obj] = []
        self.handled: set[str] = set()
        self.last_images: dict[str, np.ndarray] = {}
        self._next_id = 0

    # ---- perception ---------------------------------------------------------------
    def look(self, queries: list[str] | None = None) -> list[Obj]:
        """Grabs the scene cameras and rebuilds the object list (ids stay stable)."""
        images = self.rig.grab(self.rig.scene)
        self.last_images.update(images)
        cams = {n: self.rig.model(n) for n in self.rig.scene}
        dets: dict[str, list[Detection]] = {}
        primary = self.rig.scene[0]
        dets[primary] = self.detector.detect(images[primary], queries, primary)
        # Ask the other views for the same names so labels line up across cameras.
        names = queries or sorted({d.label for d in dets[primary]}) or None
        for n in self.rig.scene[1:]:
            dets[n] = self.detector.detect(images[n], names, n)
        objs = self._keep_ids(self._fuse(dets, cams))
        if queries:
            # A focused look only re-measures the asked-for objects: keep the others.
            keep = [o for o in self.objects
                    if not any(label_matches(q, o.label) > 0 for q in queries)
                    and all(np.linalg.norm(o.pos[:2] - n.pos[:2]) > self.cfg.merge_radius for n in objs)]
            objs += keep
        self.objects = objs
        return self.objects

    def _point_on_table(self, cam, uv, height):
        o, d = cam.ray(uv)
        return ray_plane_z(o, d, self.cfg.table_z + height / 2)

    def _in_region(self, p) -> bool:
        x0, y0, x1, y1 = self.cfg.table_region
        return p is not None and x0 <= p[0] <= x1 and y0 <= p[1] <= y1

    def _fuse(self, dets, cams) -> list[Obj]:
        h0 = self.cfg.default_height
        cand = []                 # (det, cam, single-view table point)
        for n, ds in dets.items():
            for d in ds:
                p = self._point_on_table(cams[n], d.uv, h0)
                if self._in_region(p):
                    cand.append((d, cams[n], p))
        used = set()
        objs = []
        # Pair detections of the same label from different cameras by triangulation.
        pairs = []
        for (i, a), (j, b) in itertools.combinations(enumerate(cand), 2):
            if a[1].name == b[1].name or label_matches(a[0].label, b[0].label) < 0.99:
                continue
            p, res = triangulate_rays(*zip(a[1].ray(a[0].uv), b[1].ray(b[0].uv)))
            if res < self.cfg.max_tri_residual and self._in_region(p) and p[2] > self.cfg.table_z - 0.01:
                pairs.append((res, i, j, p))
        for res, i, j, p in sorted(pairs, key=lambda t: t[0]):
            if i in used or j in used:
                continue
            used |= {i, j}
            h = float(np.clip(2 * (p[2] - self.cfg.table_z), 0.01, 0.30))
            p = np.array([p[0], p[1], self.cfg.table_z + h / 2])
            objs.append(self._make(cand[i], p, h, [cand[i][1].name, cand[j][1].name]))
        for k, c in enumerate(cand):
            if k in used:
                continue
            p = c[2]
            if any(label_matches(c[0].label, o.label) > 0.99 and np.linalg.norm(o.pos[:2] - p[:2]) < self.cfg.merge_radius for o in objs):
                continue          # same object, already triangulated
            objs.append(self._make(c, np.array(p), h0, [c[1].name]))
        return [o for o in objs if o.width is None or o.width <= self.cfg.max_object_size]

    def _make(self, cand, pos, height, views) -> Obj:
        d, cam, _ = cand
        yaw = width = length = None
        if d.angle is not None:
            yaw = self._image_angle_to_yaw(cam, d.uv, d.angle, pos[2])
        if d.size_px is not None:
            depth = np.linalg.norm(pos - cam.center)
            f = cam.K[0, 0]
            length, width = d.size_px[0] * depth / f, d.size_px[1] * depth / f
        elif d.bbox is not None:
            depth = np.linalg.norm(pos - cam.center)
            bw, bh = d.bbox[2] - d.bbox[0], d.bbox[3] - d.bbox[1]
            length, width = max(bw, bh) * depth / cam.K[0, 0], min(bw, bh) * depth / cam.K[0, 0]
        return Obj(id="", label=d.label, pos=pos, height=height, yaw=yaw, width=width,
                   length=length, views=views, score=d.score)

    @staticmethod
    def _image_angle_to_yaw(cam, uv, angle, z):
        """Direction of an image-plane line through uv, mapped onto the plane at height z."""
        uv = np.asarray(uv, float)
        step = 15.0 * np.array([np.cos(angle), np.sin(angle)])
        a, b = (ray_plane_z(*cam.ray(uv - step), z), ray_plane_z(*cam.ray(uv + step), z))
        if a is None or b is None:
            return None
        v = b - a
        return float(np.arctan2(v[1], v[0]))

    def _keep_ids(self, objs: list[Obj]) -> list[Obj]:
        """Re-uses the id of the nearest previous object with the same label."""
        old = list(self.objects)
        for o in objs:
            best = min((p for p in old if p.label == o.label),
                       key=lambda p: np.linalg.norm(p.pos[:2] - o.pos[:2]), default=None)
            if best is not None and np.linalg.norm(best.pos[:2] - o.pos[:2]) < 0.15:
                o.id = best.id
                old.remove(best)
            else:
                o.id = f"obj{self._next_id}"
                self._next_id += 1
        return objs

    # ---- queries ------------------------------------------------------------------
    def find(self, query: str, exclude: set[str] | None = None) -> Obj | None:
        """Object by id ('obj3') or by name ('red cube'); best word match wins."""
        exclude = exclude or set()
        for o in self.objects:
            if o.id == query.strip():
                return o
        scored = [(label_matches(query, o.label), o.score, o) for o in self.objects if o.id not in exclude]
        scored = [s for s in scored if s[0] > 0]
        if not scored:
            return None
        return max(scored, key=lambda s: (s[0], s[1]))[2]

    def zone_of(self, xy) -> str | None:
        for z in self.zones.values():
            if z.contains(xy):
                return z.name
        return None

    def find_zone(self, query: str) -> Zone | None:
        best = max(self.zones.values(), key=lambda z: label_matches(query, z.name), default=None)
        return best if best is not None and label_matches(query, best.name) > 0 else None

    def free_spot(self, zone: Zone, footprint: float, reachable) -> np.ndarray | None:
        """A point in the zone that is clear of known objects and reachable, preferring
        the middle of the zone."""
        cx, cy = zone.center
        sx, sy = zone.size
        best = None
        for x in np.linspace(cx - sx / 2 + footprint, cx + sx / 2 - footprint, 9):
            for y in np.linspace(cy - sy / 2 + footprint, cy + sy / 2 - footprint, 7):
                p = np.array([x, y])
                if any(np.linalg.norm(o.pos[:2] - p) < footprint + 0.035 for o in self.objects):
                    continue
                if not reachable(p):
                    continue
                score = np.linalg.norm(p - np.asarray(zone.center))   # prefer the middle
                if best is None or score < best[0]:
                    best = (score, p)
        return None if best is None else best[1]

    def describe(self) -> str:
        lines = [f"- {o.id}: {o.label} at x={o.pos[0]:.2f} y={o.pos[1]:.2f} m, "
                 f"~{o.height * 100:.0f} cm tall, in zone: {self.zone_of(o.pos[:2]) or 'none'}"
                 for o in self.objects]
        zones = [f"- {z.name}: centre ({z.center[0]:.2f}, {z.center[1]:.2f}) m, size "
                 f"{z.size[0]:.2f} x {z.size[1]:.2f} m" for z in self.zones.values()]
        return ("Objects on the table:\n" + ("\n".join(lines) or "- (none detected)") +
                "\nNamed zones / bins:\n" + ("\n".join(zones) or "- (none)"))
