#!/usr/bin/env python3
"""Generate aligned URDF visual & collision STL meshes for the ReBot Soft Gripper.

Reads Seeed's official CAD STEP files fetched by ros2_ws/scripts/setup_deps.sh:
  - third_party/reBot-DevArm/hardware/reBot_B601_DM/3D_Printed_Parts/Soft_Gripper/Soft_Gripper_Mount.step
  - third_party/reBot-DevArm/hardware/reBot_B601_DM/3D_Printed_Parts/Soft_Gripper/Soft_Gripper_Finger.step

Exact rigid-body CAD alignment (in mm, scaled by 0.001 to URDF meters):
  1. Soft_Gripper_Finger -> Soft_Gripper_Mount:
     Matched via the asymmetric 3-bolt L-pattern (20.0 mm x 14.0 mm, z in [-14.25, +14.25]):
       p_mount = (x_f - 94.209, 141.126 - y_f, -z_f)
     which places the finger base flush on the mount pocket floor (y_mount = -9.100 mm).
  2. Soft_Gripper_Mount -> finger_left_link (URDF end_link / finger_left_link frame):
     Matched via the 4-bolt M3 linear carriage pattern (10.0 mm x 15.0 mm on mating plane
     x_urdf = -64.809 mm, y_urdf in {+14.800, +24.800} mm, z_urdf in {-7.500, +7.500} mm):
       p_left_mm = (y_mount - 49.809, -x_mount + 19.650, z_mount)
     placing the mount inner face at y = +5.150 mm (flush with the left carriage) and
     extending the Fin-Ray fingertip to x = +28.581 mm (+0.02858 m ahead of the hard finger tip).
  3. finger_left_link -> finger_right_link:
     180-degree proper rigid rotation about +x:
       p_right = (x_left, -y_left, -z_left)
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import re
import struct

import numpy as np
from scipy.interpolate import BSpline
from scipy.spatial import ConvexHull


def _split_top_level(s: str) -> list[str]:
    out: list[str] = []
    depth = 0
    in_str = False
    cur: list[str] = []
    for ch in s:
        if ch == "'":
            in_str = not in_str
            cur.append(ch)
        elif not in_str:
            if ch == "(":
                depth += 1
                cur.append(ch)
            elif ch == ")":
                depth -= 1
                cur.append(ch)
            elif ch == "," and depth == 0:
                out.append("".join(cur).strip())
                cur = []
            else:
                cur.append(ch)
        else:
            cur.append(ch)
    if cur:
        out.append("".join(cur).strip())
    return out


def _ref(s: str) -> int:
    m = re.search(r"#(\d+)", s)
    if not m:
        raise ValueError(f"Expected STEP entity ref in {s!r}")
    return int(m.group(1))


def _refs(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"#(\d+)", s)]


def _nums(s: str) -> list[float]:
    return [
        float(x)
        for x in re.findall(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[Ee][+-]?\d+)?", s)
    ]


class StepModel:
    def __init__(self, path: Path) -> None:
        txt = path.read_text(encoding="utf-8", errors="ignore")
        txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
        self.ents: dict[int, tuple[str, list[str]]] = {}
        for m in re.finditer(r"#(\d+)\s*=\s*([A-Z0-9_]+)\((.*?)\)\s*;", txt, flags=re.S):
            eid = int(m.group(1))
            etype = m.group(2)
            raw_args = m.group(3).replace("\n", " ").replace("\r", " ")
            self.ents[eid] = (etype, _split_top_level(raw_args))

    def point(self, eid: int) -> np.ndarray:
        t, a = self.ents[eid]
        if t == "VERTEX_POINT":
            return self.point(_ref(a[1]))
        return np.array(_nums(a[1])[:3], dtype=np.float64)

    def direction(self, eid: int) -> np.ndarray:
        _, a = self.ents[eid]
        v = np.array(_nums(a[1])[:3], dtype=np.float64)
        return v / np.linalg.norm(v)

    def axis2(self, eid: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        _, a = self.ents[eid]
        origin = self.point(_ref(a[1]))
        z_ax = (
            self.direction(_ref(a[2]))
            if len(a) > 2 and "#" in a[2]
            else np.array([0.0, 0.0, 1.0])
        )
        if len(a) > 3 and "#" in a[3]:
            x_raw = self.direction(_ref(a[3]))
        else:
            x_raw = (
                np.array([1.0, 0.0, 0.0])
                if abs(z_ax[0]) < 0.9
                else np.array([0.0, 1.0, 0.0])
            )
        x_ax = x_raw - np.dot(x_raw, z_ax) * z_ax
        x_ax /= np.linalg.norm(x_ax)
        y_ax = np.cross(z_ax, x_ax)
        return origin, x_ax, y_ax, z_ax

    def sample_edge_curve(self, edge_id: int, orient: bool) -> np.ndarray:
        _, a = self.ents[edge_id]
        p1 = self.point(_ref(a[1]))
        p2 = self.point(_ref(a[2]))
        curve_id = _ref(a[3])
        same_sense = a[4].strip() == ".T."
        ct, ca = self.ents[curve_id]

        if ct == "LINE":
            pts = np.vstack([p1, p2])
        elif ct == "CIRCLE":
            origin, x_ax, y_ax, _ = self.axis2(_ref(ca[1]))
            radius = float(ca[2])
            d1 = p1 - origin
            d2 = p2 - origin
            th1 = math.atan2(float(np.dot(d1, y_ax)), float(np.dot(d1, x_ax)))
            th2 = math.atan2(float(np.dot(d2, y_ax)), float(np.dot(d2, x_ax)))
            closed_v = np.linalg.norm(p1 - p2) < 1e-6
            if same_sense:
                dth = (th2 - th1) % (2.0 * math.pi)
                if dth < 1e-6 and closed_v:
                    dth = 2.0 * math.pi
            else:
                dth = -((th1 - th2) % (2.0 * math.pi))
                if abs(dth) < 1e-6 and closed_v:
                    dth = -2.0 * math.pi
            n_seg = max(2, int(math.ceil(abs(dth) / (math.pi / 12.0))))
            thetas = np.linspace(th1, th1 + dth, n_seg + 1)
            pts = (
                origin[None, :]
                + radius * np.cos(thetas)[:, None] * x_ax[None, :]
                + radius * np.sin(thetas)[:, None] * y_ax[None, :]
            )
            pts[0] = p1
            pts[-1] = p2
        elif ct == "B_SPLINE_CURVE_WITH_KNOTS":
            deg = int(ca[1])
            ctrl = np.array([self.point(cid) for cid in _refs(ca[2])], dtype=np.float64)
            mults = [int(x) for x in re.findall(r"\d+", ca[6])]
            knots = _nums(ca[7])
            full_knots: list[float] = []
            for k, m in zip(knots, mults):
                full_knots.extend([k] * m)
            spl = BSpline(np.array(full_knots, dtype=np.float64), ctrl, deg)
            u_grid = np.linspace(knots[0], knots[-1], 200)
            eval_grid = spl(u_grid)
            u1 = float(u_grid[int(np.argmin(np.linalg.norm(eval_grid - p1, axis=1)))])
            u2 = float(u_grid[int(np.argmin(np.linalg.norm(eval_grid - p2, axis=1)))])
            if abs(u2 - u1) < 1e-9:
                u1, u2 = (knots[0], knots[-1]) if same_sense else (knots[-1], knots[0])
            pts = spl(np.linspace(u1, u2, 17))
            pts[0] = p1
            pts[-1] = p2
        else:
            raise ValueError(f"Unsupported STEP curve entity {ct}")

        return pts if orient else pts[::-1].copy()

    def sample_loop(self, loop_id: int) -> np.ndarray:
        _, a = self.ents[loop_id]
        chunks = []
        for oe_id in _refs(a[1]):
            _, oa = self.ents[oe_id]
            pts = self.sample_edge_curve(_ref(oa[3]), oa[4].strip() == ".T.")
            chunks.append(pts[:-1])
        ring = np.vstack(chunks)
        cleaned = [ring[0]]
        for p in ring[1:]:
            if np.linalg.norm(p - cleaned[-1]) > 1e-5:
                cleaned.append(p)
        if len(cleaned) > 1 and np.linalg.norm(cleaned[0] - cleaned[-1]) <= 1e-5:
            cleaned.pop()
        return np.array(cleaned, dtype=np.float64)


def _signed_area_2d(poly: np.ndarray) -> float:
    x = poly[:, 0]
    y = poly[:, 1]
    return 0.5 * float(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


def _pt_in_tri(p: np.ndarray, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> bool:
    v0 = c - a
    v1 = b - a
    v2 = p - a
    dot00 = float(np.dot(v0, v0))
    dot01 = float(np.dot(v0, v1))
    dot02 = float(np.dot(v0, v2))
    dot11 = float(np.dot(v1, v1))
    dot12 = float(np.dot(v1, v2))
    denom = dot00 * dot11 - dot01 * dot01
    if abs(denom) < 1e-16:
        return False
    inv = 1.0 / denom
    u = (dot11 * dot02 - dot01 * dot12) * inv
    v = (dot00 * dot12 - dot01 * dot02) * inv
    return u > 1e-9 and v > 1e-9 and (u + v) < 1.0 - 1e-9


def _segments_properly_intersect(
    a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray
) -> bool:
    def ccw(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
        return float((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]))

    c1 = ccw(a, b, c)
    c2 = ccw(a, b, d)
    c3 = ccw(c, d, a)
    c4 = ccw(c, d, b)
    return (c1 * c2 < -1e-14) and (c3 * c4 < -1e-14)


def _point_in_poly_2d(pt: np.ndarray, ring: np.ndarray) -> bool:
    inside = False
    n = len(ring)
    for i in range(n):
        a, b = ring[i], ring[(i + 1) % n]
        if (a[1] > pt[1]) != (b[1] > pt[1]):
            x_int = a[0] + (pt[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x_int > pt[0]:
                inside = not inside
    return inside


def _bridge_holes(
    outer_2d: np.ndarray,
    outer_3d: np.ndarray,
    holes_2d: list[np.ndarray],
    holes_3d: list[np.ndarray],
) -> tuple[np.ndarray, np.ndarray]:
    poly_2d = outer_2d.copy()
    poly_3d = outer_3d.copy()
    order = sorted(
        range(len(holes_2d)),
        key=lambda i: float(np.max(holes_2d[i][:, 0])),
        reverse=True,
    )
    remaining = set(order)
    for idx in order:
        remaining.remove(idx)
        h2 = holes_2d[idx]
        h3 = holes_3d[idx]
        m_idx = int(np.argmax(h2[:, 0]))
        m_pt = h2[m_idx]

        best_vi = -1
        best_dist = float("inf")
        n_p = len(poly_2d)
        for vi in range(n_p):
            cand = poly_2d[vi]
            if np.linalg.norm(cand - m_pt) < 1e-8:
                best_vi = vi
                break
            blocked = False
            for ei in range(n_p):
                ej = (ei + 1) % n_p
                if np.linalg.norm(poly_2d[ei] - cand) < 1e-8 or np.linalg.norm(poly_2d[ej] - cand) < 1e-8:
                    continue
                if _segments_properly_intersect(m_pt, cand, poly_2d[ei], poly_2d[ej]):
                    blocked = True
                    break
            if blocked:
                continue
            for hi in range(len(h2)):
                hj = (hi + 1) % len(h2)
                if hi == m_idx or hj == m_idx:
                    continue
                if _segments_properly_intersect(m_pt, cand, h2[hi], h2[hj]):
                    blocked = True
                    break
            if blocked:
                continue
            for other_idx in remaining:
                oh2 = holes_2d[other_idx]
                for oi in range(len(oh2)):
                    oj = (oi + 1) % len(oh2)
                    if _segments_properly_intersect(m_pt, cand, oh2[oi], oh2[oj]):
                        blocked = True
                        break
                if blocked:
                    break
            if blocked:
                continue
            mid = 0.5 * (m_pt + cand)
            if not _point_in_poly_2d(mid, poly_2d):
                continue
            if any(_point_in_poly_2d(mid, holes_2d[oi]) for oi in remaining):
                continue
            dist = float(np.linalg.norm(cand - m_pt))
            if dist < best_dist:
                best_dist = dist
                best_vi = vi

        if best_vi < 0:
            best_vi = int(np.argmin(np.linalg.norm(poly_2d - m_pt, axis=1)))

        h2_rot = np.vstack([h2[m_idx:], h2[:m_idx], h2[m_idx : m_idx + 1]])
        h3_rot = np.vstack([h3[m_idx:], h3[:m_idx], h3[m_idx : m_idx + 1]])
        poly_2d = np.vstack([poly_2d[: best_vi + 1], h2_rot, poly_2d[best_vi:]])
        poly_3d = np.vstack([poly_3d[: best_vi + 1], h3_rot, poly_3d[best_vi:]])
    return poly_2d, poly_3d


def _ear_clip(poly_2d: np.ndarray) -> list[tuple[int, int, int]]:
    idxs = list(range(len(poly_2d)))
    tris: list[tuple[int, int, int]] = []
    eps = 1e-11
    guard = 0
    max_guard = len(idxs) * 6 + 50
    while len(idxs) > 3 and guard < max_guard:
        guard += 1
        ear_found = False
        best_k = -1
        best_diag = float("inf")
        m = len(idxs)
        for k in range(m):
            i0 = idxs[(k - 1) % m]
            i1 = idxs[k]
            i2 = idxs[(k + 1) % m]
            a, b, c = poly_2d[i0], poly_2d[i1], poly_2d[i2]
            if np.linalg.norm(b - a) < 1e-9 or np.linalg.norm(c - b) < 1e-9:
                idxs.pop(k)
                ear_found = True
                break
            cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            if cross <= eps:
                continue
            diag = float(np.linalg.norm(c - a))
            if diag >= best_diag:
                continue
            contains = False
            for j in idxs:
                if j in (i0, i1, i2):
                    continue
                pj = poly_2d[j]
                if (
                    np.linalg.norm(pj - a) < 1e-6
                    or np.linalg.norm(pj - b) < 1e-6
                    or np.linalg.norm(pj - c) < 1e-6
                ):
                    continue
                if _pt_in_tri(pj, a, b, c):
                    contains = True
                    break
            if not contains:
                best_diag = diag
                best_k = k
        if best_k >= 0 and not ear_found:
            i0 = idxs[(best_k - 1) % m]
            i1 = idxs[best_k]
            i2 = idxs[(best_k + 1) % m]
            tris.append((i0, i1, i2))
            idxs.pop(best_k)
            ear_found = True
        if not ear_found:
            # Clip sharpest locally convex ear if numerical sliver blocks strict check
            best_k = -1
            best_cross = -float("inf")
            for k in range(len(idxs)):
                i0 = idxs[(k - 1) % len(idxs)]
                i1 = idxs[k]
                i2 = idxs[(k + 1) % len(idxs)]
                a, b, c = poly_2d[i0], poly_2d[i1], poly_2d[i2]
                cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
                if cross > best_cross:
                    best_cross = cross
                    best_k = k
            if best_k >= 0:
                i0 = idxs[(best_k - 1) % len(idxs)]
                i1 = idxs[best_k]
                i2 = idxs[(best_k + 1) % len(idxs)]
                tris.append((i0, i1, i2))
                idxs.pop(best_k)
            else:
                break
    if len(idxs) == 3:
        tris.append((idxs[0], idxs[1], idxs[2]))
    return tris


def tessellate_step(path: Path) -> np.ndarray:
    model = StepModel(path)
    all_tris: list[np.ndarray] = []
    for _, (etype, args) in model.ents.items():
        if etype != "ADVANCED_FACE":
            continue
        bound_ids = _refs(args[1])
        surf_id = _ref(args[2])
        same_sense = args[3].strip() == ".T."
        st, sa = model.ents[surf_id]

        outer_3d = None
        holes_3d = []
        for bid in bound_ids:
            bt, ba = model.ents[bid]
            loop_3d = model.sample_loop(_ref(ba[1]))
            if bt == "FACE_OUTER_BOUND" and outer_3d is None:
                outer_3d = loop_3d
            else:
                holes_3d.append(loop_3d)
        if outer_3d is None:
            outer_3d = holes_3d.pop(0)

        if st == "PLANE":
            origin, x_ax, _, z_ax = model.axis2(_ref(sa[1]))
            n_out = z_ax if same_sense else -z_ax
            u_ax = x_ax
            v_ax = np.cross(n_out, u_ax)

            def proj(pts3: np.ndarray) -> np.ndarray:
                d = pts3 - origin[None, :]
                return np.column_stack([d @ u_ax, d @ v_ax])

            outer_2d = proj(outer_3d)
            if _signed_area_2d(outer_2d) < 0:
                outer_2d = outer_2d[::-1].copy()
                outer_3d = outer_3d[::-1].copy()
            holes_2d = []
            fixed_holes_3d = []
            for h3 in holes_3d:
                h2 = proj(h3)
                if _signed_area_2d(h2) > 0:
                    h2 = h2[::-1].copy()
                    h3 = h3[::-1].copy()
                holes_2d.append(h2)
                fixed_holes_3d.append(h3)

            if holes_2d:
                poly_2d, poly_3d = _bridge_holes(
                    outer_2d, outer_3d, holes_2d, fixed_holes_3d
                )
            else:
                poly_2d, poly_3d = outer_2d, outer_3d

            for i0, i1, i2 in _ear_clip(poly_2d):
                t3 = np.array([poly_3d[i0], poly_3d[i1], poly_3d[i2]])
                if np.linalg.norm(np.cross(t3[1] - t3[0], t3[2] - t3[0])) > 1e-10:
                    all_tris.append(t3)

        elif st in ("CYLINDRICAL_SURFACE", "CONICAL_SURFACE"):
            origin, x_ax, y_ax, z_ax = model.axis2(_ref(sa[1]))
            r_ref = float(sa[2])
            d = outer_3d - origin[None, :]
            s_vals = d @ z_ax
            raw_th = np.arctan2(d @ y_ax, d @ x_ax)
            th = np.empty_like(raw_th)
            th[0] = raw_th[0]
            for i in range(1, len(raw_th)):
                diff = math.atan2(
                    math.sin(raw_th[i] - th[i - 1]),
                    math.cos(raw_th[i] - th[i - 1]),
                )
                th[i] = th[i - 1] + diff
            poly_2d = np.column_stack([max(r_ref, 1.0) * th, s_vals])
            poly_3d = outer_3d.copy()
            if _signed_area_2d(poly_2d) < 0:
                poly_2d = poly_2d[::-1].copy()
                poly_3d = poly_3d[::-1].copy()
            for i0, i1, i2 in _ear_clip(poly_2d):
                t3 = (
                    np.array([poly_3d[i0], poly_3d[i1], poly_3d[i2]])
                    if same_sense
                    else np.array([poly_3d[i0], poly_3d[i2], poly_3d[i1]])
                )
                if np.linalg.norm(np.cross(t3[1] - t3[0], t3[2] - t3[0])) > 1e-10:
                    all_tris.append(t3)
        else:
            raise ValueError(f"Unsupported STEP surface entity {st}")
    return np.array(all_tris, dtype=np.float64)


def load_binary_stl(path: Path) -> np.ndarray:
    data = path.read_bytes()
    count = struct.unpack("<I", data[80:84])[0]
    dt = np.dtype([("normal", "<f4", (3,)), ("verts", "<f4", (3, 3)), ("attr", "<u2")])
    return np.frombuffer(data, dtype=dt, offset=84, count=count)["verts"].astype(np.float64)


def write_binary_stl(tris_m: np.ndarray, path: Path, header_note: str) -> None:
    triangles = tris_m.astype(np.float32)
    normals = np.cross(
        triangles[:, 1] - triangles[:, 0],
        triangles[:, 2] - triangles[:, 0],
    )
    norms = np.linalg.norm(normals, axis=1)
    normals /= np.maximum(norms[:, None], 1e-12)
    records = np.zeros(
        len(triangles),
        dtype=[("normal", "<f4", (3,)), ("vertices", "<f4", (3, 3)), ("attribute", "<u2")],
    )
    records["normal"] = normals
    records["vertices"] = triangles
    path.parent.mkdir(parents=True, exist_ok=True)
    header = header_note.encode("ascii", errors="ignore")[:80].ljust(80, b"\0")
    path.write_bytes(header + struct.pack("<I", len(records)) + records.tobytes())


def _convex_hull_tris(points_m: np.ndarray) -> np.ndarray:
    hull = ConvexHull(points_m)
    pts = hull.points
    centroid = pts.mean(axis=0)
    tris = []
    for simplex in hull.simplices:
        a, b, c = pts[simplex[0]], pts[simplex[1]], pts[simplex[2]]
        n = np.cross(b - a, c - a)
        if np.dot(n, a - centroid) < 0:
            b, c = c, b
        tris.append([a, b, c])
    return np.array(tris, dtype=np.float64)


def _mount_to_left_m(pts_mm: np.ndarray) -> np.ndarray:
    # p_left_mm = (y_mount - 49.809, -x_mount + 19.650, z_mount), det = +1
    out = np.empty_like(pts_mm)
    out[..., 0] = (pts_mm[..., 1] - 49.809) * 0.001
    out[..., 1] = (-pts_mm[..., 0] + 19.650) * 0.001
    out[..., 2] = pts_mm[..., 2] * 0.001
    return out


def _finger_to_mount_mm(pts_mm: np.ndarray) -> np.ndarray:
    # p_mount_mm = (x_f - 94.209, 141.126 - y_f, -z_f), det = +1 (180 deg about X)
    out = np.empty_like(pts_mm)
    out[..., 0] = pts_mm[..., 0] - 94.209
    out[..., 1] = 141.126 - pts_mm[..., 1]
    out[..., 2] = -pts_mm[..., 2]
    return out


def _left_to_right_m(pts_m: np.ndarray) -> np.ndarray:
    # 180 deg proper rotation about +X: diag(1, -1, -1), det = +1
    out = pts_m.copy()
    out[..., 1] *= -1.0
    out[..., 2] *= -1.0
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    ws_default = Path(__file__).resolve().parents[3]
    parser.add_argument(
        "--devarm-dir",
        type=Path,
        default=ws_default / "third_party" / "reBot-DevArm",
        help="Path to third_party/reBot-DevArm",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "meshes" / "soft_gripper",
        help="Output mesh directory",
    )
    args = parser.parse_args()

    cad_dir = (
        args.devarm_dir
        / "hardware"
        / "reBot_B601_DM"
        / "3D_Printed_Parts"
        / "Soft_Gripper"
    )
    dm_meshes = args.devarm_dir / "Rebot_Arm_description" / "DM" / "meshes"

    mount_tris_mm = tessellate_step(cad_dir / "Soft_Gripper_Mount.step")
    finger_tris_mm = tessellate_step(cad_dir / "Soft_Gripper_Finger.step")

    left_mount_m = _mount_to_left_m(mount_tris_mm)
    left_finger_m = _mount_to_left_m(_finger_to_mount_mm(finger_tris_mm))
    right_mount_m = _left_to_right_m(left_mount_m)
    right_finger_m = _left_to_right_m(left_finger_m)

    # Build lightweight compound convex collision meshes (carriage + mount + soft finger)
    left_carriage_m = load_binary_stl(
        dm_meshes / "shared" / "colored_left_finger_carriage_grey.stl"
    )
    left_rack_m = load_binary_stl(
        dm_meshes / "visual" / "colored_left_finger_rack_metal.stl"
    )
    left_coll_m = np.vstack(
        [
            _convex_hull_tris(left_carriage_m.reshape(-1, 3)),
            _convex_hull_tris(left_rack_m.reshape(-1, 3)),
            _convex_hull_tris(left_mount_m.reshape(-1, 3)),
            _convex_hull_tris(left_finger_m.reshape(-1, 3)),
        ]
    )
    right_coll_m = _left_to_right_m(left_coll_m)

    note = "Derived from Seeed reBot-DevArm Soft_Gripper STEP; CERN-OHL-W-2.0"
    outputs = {
        args.out_dir / "visual" / "left_soft_mount.stl": left_mount_m,
        args.out_dir / "visual" / "left_soft_finger.stl": left_finger_m,
        args.out_dir / "visual" / "right_soft_mount.stl": right_mount_m,
        args.out_dir / "visual" / "right_soft_finger.stl": right_finger_m,
        args.out_dir / "collision" / "left_soft_finger_collision.stl": left_coll_m,
        args.out_dir / "collision" / "right_soft_finger_collision.stl": right_coll_m,
    }
    for path, tris in outputs.items():
        write_binary_stl(tris, path, note)
        v = tris.reshape(-1, 3)
        print(
            f"Wrote {path.relative_to(args.out_dir)} ({len(tris)} tris) | "
            f"min={np.round(v.min(0), 5)} max={np.round(v.max(0), 5)}"
        )


if __name__ == "__main__":
    main()
