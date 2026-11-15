"""Cut one object out of a splat trained on a phone video and scale it to metres.

  ../teleoperation/.venv/bin/python tools/crop_object_splat.py splats/towel/splat.ply \
      --object splats/towel/object.json --out splats/towel_object.ply

The splat comes from hf_jobs/train_splat.sh on a video that circles one object on a
table (prepare_splat_dataset.py --standalone --object ...). nerfstudio has already
put z roughly up and the cameras' centre near the origin, so the object sits near
the z axis. Steps:

1. fit the table plane (RANSAC, normal within 35 deg of +z) and level it;
2. find the object: the densest blob just above the table near the axis;
3. measure its length (height if upright, longest horizontal extent if lying),
   then scale so that it matches object.json;
4. keep the gaussians in a box around it, in the object's frame: origin on the
   table under its centre, z up, x along its length if lying. Units are metres.

Positions, orientations, sizes and the view-dependent colour (SH) are all
transformed, so the result renders correctly in any 3DGS viewer. It also writes
<out>.json (the measured size and the transform) and <out>.png (top and side
views with a 1 cm grid) to check the crop.
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np

# ---------------------------------------------------------------- ply io

_PLY_TYPES = {"float": "f4", "float32": "f4", "double": "f8", "uchar": "u1",
              "uint8": "u1", "int": "i4", "int32": "i4", "uint": "u4", "short": "i2"}


def read_ply(path):
    with open(path, "rb") as f:
        header = []
        while True:
            line = f.readline().decode("ascii").strip()
            header.append(line)
            if line == "end_header":
                break
        if "format binary_little_endian 1.0" not in header:
            raise SystemExit(f"{path}: only binary little-endian ply is supported")
        n = next(int(h.split()[2]) for h in header if h.startswith("element vertex"))
        props = [(h.split()[2], "<" + _PLY_TYPES[h.split()[1]])
                 for h in header if h.startswith("property")]
        return np.fromfile(f, dtype=np.dtype(props), count=n)


def write_ply(path, v):
    names = {"f4": "float", "f8": "double", "u1": "uchar", "i4": "int", "u4": "uint",
             "i2": "short"}
    lines = ["ply", "format binary_little_endian 1.0", f"element vertex {len(v)}"]
    lines += [f"property {names[v.dtype[k].str[1:]]} {k}" for k in v.dtype.names]
    lines.append("end_header")
    with open(path, "wb") as f:
        f.write(("\n".join(lines) + "\n").encode("ascii"))
        v.tofile(f)


# ---------------------------------------------------------------- math

def _sh_basis(d):
    """Real SH basis up to degree 3, exactly as 3DGS / gsplat evaluate it."""
    x, y, z = d[:, 0], d[:, 1], d[:, 2]
    xx, yy, zz = x * x, y * y, z * z
    c1, c2, c3 = 0.4886025119029199, [1.0925484305920792, -1.0925484305920792,
                                      0.31539156525252005, -1.0925484305920792,
                                      0.5462742152960396], \
        [-0.5900435899266435, 2.890611442640554, -0.4570457994644658,
         0.3731763325901154, -0.4570457994644658, 1.445305721320277, -0.5900435899266435]
    return np.stack([
        -c1 * y, c1 * z, -c1 * x,
        c2[0] * x * y, c2[1] * y * z, c2[2] * (2 * zz - xx - yy), c2[3] * x * z,
        c2[4] * (xx - yy),
        c3[0] * y * (3 * xx - yy), c3[1] * x * y * z, c3[2] * y * (4 * zz - xx - yy),
        c3[3] * z * (2 * zz - 3 * xx - 3 * yy), c3[4] * x * (4 * zz - xx - yy),
        c3[5] * z * (xx - yy), c3[6] * x * (xx - 3 * yy)], axis=1)


def sh_rotation(R, n_coef):
    """Matrix M with c_new = M @ c_old for the non-DC SH coefficients of a
    gaussian rotated by R (fitted on random directions; exact for real SH)."""
    rng = np.random.default_rng(0)
    d = rng.normal(size=(500, 3))
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    A, B = _sh_basis(d)[:, :n_coef], _sh_basis(d @ R)[:, :n_coef]  # B = Y(R^T d)
    return np.linalg.lstsq(A, B, rcond=None)[0]


def quat_from_matrix(R):
    w = np.sqrt(max(0.0, 1 + np.trace(R))) / 2
    x = np.copysign(np.sqrt(max(0.0, 1 + R[0, 0] - R[1, 1] - R[2, 2])) / 2, R[2, 1] - R[1, 2])
    y = np.copysign(np.sqrt(max(0.0, 1 - R[0, 0] + R[1, 1] - R[2, 2])) / 2, R[0, 2] - R[2, 0])
    z = np.copysign(np.sqrt(max(0.0, 1 - R[0, 0] - R[1, 1] + R[2, 2])) / 2, R[1, 0] - R[0, 1])
    return np.array([w, x, y, z])


def quat_mul(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b.T
    return np.stack([aw * bw - ax * bx - ay * by - az * bz,
                     aw * bx + ax * bw + ay * bz - az * by,
                     aw * by - ax * bz + ay * bw + az * bx,
                     aw * bz + ax * by - ay * bx + az * bw], axis=1)


def frame_from_normal(n):
    """Rotation whose rows are an orthonormal frame with z = n."""
    a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
    x = np.cross(a, n)
    x /= np.linalg.norm(x)
    return np.stack([x, np.cross(n, x), n])


# ---------------------------------------------------------------- finding the object

def fit_table(p, w, rng, iters=3000, tol=0.006):
    """RANSAC plane over opaque gaussians near the axis; normal close to +z."""
    near = np.linalg.norm(p[:, :2], axis=1) < 1.0
    q, qw = p[near], w[near]
    best, best_score = None, -1
    for _ in range(iters):
        a, b, c = q[rng.choice(len(q), 3, replace=False)]
        n = np.cross(b - a, c - a)
        if np.linalg.norm(n) < 1e-9:
            continue
        n /= np.linalg.norm(n)
        if n[2] < 0:
            n = -n
        if n[2] < np.cos(np.radians(35)):
            continue
        score = qw[np.abs((q - a) @ n) < tol].sum()
        if score > best_score:
            best, best_score = (n, a), score
    n, a = best
    inl = q[np.abs((q - a) @ n) < tol]
    c = inl.mean(0)
    n = np.linalg.svd(inl - c)[2][2]
    if n[2] < 0:
        n = -n
    return n, c, len(inl)


def find_centre(xy, w, start=(0.0, 0.0), bw=0.12, steps=30):
    """Weighted mean shift in the table plane."""
    c = np.array(start, float)
    for _ in range(steps):
        k = w * np.exp(-np.sum((xy - c) ** 2, 1) / (2 * bw * bw))
        c = (xy * k[:, None]).sum(0) / k.sum()
    return c


def top_of_column(h, gap):
    """Highest height reached from the table without a gap > `gap`."""
    h = np.sort(h[h > 0])
    if len(h) == 0:
        return 0.0
    jumps = np.nonzero(np.diff(h) > gap)[0]
    top = h[jumps[0]] if len(jumps) else h[-1]
    below = h[h <= top]
    return float(np.percentile(below, 99.5))


def extent(v, lo=0.5, hi=99.5):
    return np.percentile(v, lo), np.percentile(v, hi)


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ply")
    p.add_argument("--object", required=True, help="object.json from the dataset")
    p.add_argument("--out", required=True)
    p.add_argument("--min-opacity", type=float, default=0.3)
    p.add_argument("--margin", type=float, default=0.15,
                   help="extra room around the object, as a fraction of its size")
    p.add_argument("--table", type=float, default=0.004,
                   help="keep this much table under the object, metres (0 = none)")
    args = p.parse_args()

    meta = json.loads(Path(args.object).read_text())
    L, D, pose = meta["length"], meta["diameter"], meta["pose"]
    v = read_ply(args.ply)
    P = np.stack([v["x"], v["y"], v["z"]], 1).astype(np.float64)
    alpha = 1 / (1 + np.exp(-v["opacity"].astype(np.float64)))
    size = np.exp(np.stack([v[f"scale_{i}"] for i in range(3)], 1)).max(1)
    good = (alpha > args.min_opacity) & np.isfinite(P).all(1)
    good &= size <= np.percentile(size[good], 95)
    rng = np.random.default_rng(0)

    # 1. table plane -> levelled frame (z = height above the table)
    n, c0, n_in = fit_table(P[good], alpha[good], rng)
    F = frame_from_normal(n)
    Q = (P - c0) @ F.T
    print(f"table: {n_in} gaussians on the plane, tilt {np.degrees(np.arccos(n[2])):.1f} deg")

    # 2. object: blob just above the table near the axis
    g = good & (Q[:, 2] > 0.01) & (Q[:, 2] < 1.0)
    origin_xy = (-c0 @ F.T)[:2]
    cxy = find_centre(Q[g, :2], alpha[g], start=origin_xy)
    r = np.linalg.norm(Q[:, :2] - cxy, axis=1)

    # 3. measure the length in splat units
    if pose == "upright":
        col = good & (r < 0.08)
        top = top_of_column(Q[col, 2], gap=0.03)
        for _ in range(2):  # refine the column radius from the expected aspect ratio
            rad = 0.6 * top * D / L * 1.3
            col = good & (r < rad) & (Q[:, 2] > 0)
            cxy = np.average(Q[col, :2], axis=0, weights=alpha[col])
            r = np.linalg.norm(Q[:, :2] - cxy, axis=1)
            top = top_of_column(Q[col & (r < rad), 2], gap=0.03)
        measured = top
        Rz = np.eye(3)
        lo, hi = extent(np.linalg.norm(Q[col, :2] - cxy, axis=1), 0, 90)
        measured_d = 2 * hi
    else:
        blob = good & (r < 0.5) & (Q[:, 2] > 0.01) & (Q[:, 2] < 0.3)
        xy = Q[blob, :2] - cxy
        axis = np.linalg.svd(xy - xy.mean(0), full_matrices=False)[2][0]
        perp = np.array([-axis[1], axis[0]])
        u = xy @ axis
        a0, a1 = extent(u[np.abs(xy @ perp) < 0.15], 1, 99)
        measured = a1 - a0
        mid = (a0 + a1) / 2
        cxy = cxy + axis * mid
        Rz = np.array([[axis[0], axis[1], 0], [perp[0], perp[1], 0], [0, 0, 1]])
        sel = good & (np.abs((Q[:, :2] - cxy) @ axis) < measured / 2) & \
            (np.abs((Q[:, :2] - cxy) @ perp) < measured * D / L)
        measured_d = top_of_column(Q[sel, 2], gap=0.02)
    s = L / measured
    print(f"{meta['object']}: length {measured:.3f} splat units -> {L * 100:g} cm "
          f"(scale {s:.4f} m/unit); diameter then {measured_d * s * 100:.1f} cm "
          f"(given {D * 100:g} cm)")

    # 4. object frame in metres: X = s * Rz F (P - c0) - [cx, cy, 0]
    R = Rz @ F
    t = np.array([cxy[0], cxy[1], 0.0]) @ Rz.T
    X = s * (P - c0) @ R.T - s * t
    half = (np.array([L, D, D]) / 2 if pose == "lying" else np.array([D, D, L]) / 2)
    half = half * (1 + args.margin) + 0.01
    if pose == "upright":
        zlo, zhi = -args.table, L * (1 + args.margin)
        box = (np.abs(X[:, 0]) < half[0]) & (np.abs(X[:, 1]) < half[1])
    else:
        zlo, zhi = -args.table, D * (1 + 2 * args.margin) + 0.01
        box = (np.abs(X[:, 0]) < half[0]) & (np.abs(X[:, 1]) < half[1])
    keep = box & (X[:, 2] > zlo) & (X[:, 2] < zhi) & np.isfinite(X).all(1)

    out = v[keep].copy()
    for i, k in enumerate("xyz"):
        out[k] = X[keep, i]
    for k in ("nx", "ny", "nz"):
        if k in out.dtype.names:
            out[k] = 0
    for i in range(3):
        out[f"scale_{i}"] = out[f"scale_{i}"] + np.log(s)
    q = np.stack([out[f"rot_{i}"] for i in range(4)], 1).astype(np.float64)
    q = quat_mul(quat_from_matrix(R), q / np.linalg.norm(q, axis=1, keepdims=True))
    for i in range(4):
        out[f"rot_{i}"] = q[:, i]
    rest = sorted((k for k in out.dtype.names if k.startswith("f_rest_")),
                  key=lambda k: int(k.split("_")[-1]))
    if rest:
        m = len(rest) // 3
        M = sh_rotation(R, m)
        for ch in range(3):
            ks = rest[ch * m:(ch + 1) * m]
            C = np.stack([out[k] for k in ks], 1).astype(np.float64)
            C = C @ M.T
            for j, k in enumerate(ks):
                out[k] = C[:, j]

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    write_ply(outp, out)
    info = {"object": meta["object"], "pose": pose, "given": meta,
            "measured_length_units": measured, "scale_m_per_unit": s,
            "measured_diameter_m": measured_d * s, "n_gaussians": int(keep.sum()),
            "frame": "origin on the table under the object's centre, z up, "
                     "x along the length when lying; metres",
            "splat_to_object": {"scale": s, "R": R.tolist(), "p0": c0.tolist(),
                                "t": (s * t).tolist(),
                                "formula": "X = scale * R @ (p - p0) - t"}}
    outp.with_suffix(".json").write_text(json.dumps(info, indent=2) + "\n")
    preview(out, outp.with_suffix(".png"), meta["object"])
    print(f"wrote {outp} ({keep.sum()} gaussians), .json and .png")


def preview(v, path, title, px_per_cm=12):
    """Top (x-y) and side (x-z) views: gaussian centres in their base colour."""
    X = np.stack([v["x"], v["y"], v["z"]], 1)
    a = 1 / (1 + np.exp(-v["opacity"]))
    rgb = np.clip(0.5 + 0.28209479177387814 *
                  np.stack([v["f_dc_0"], v["f_dc_1"], v["f_dc_2"]], 1), 0, 1)
    order = np.argsort(a)
    panels = []
    for (i, j), name in (((0, 1), "top (x right, y up)"), ((0, 2), "side (x right, z up)")):
        lo, hi = X[:, [i, j]].min(0) - 0.01, X[:, [i, j]].max(0) + 0.01
        W, H = ((hi - lo) * 100 * px_per_cm).astype(int) + 1
        img = np.full((H, W, 3), 255, np.uint8)
        for k in range(int(np.ceil(lo[0] * 100)), int(hi[0] * 100) + 1):
            x = int((k / 100 - lo[0]) * 100 * px_per_cm)
            cv2.line(img, (x, 0), (x, H - 1), (200, 200, 200) if k % 5 else (150, 150, 150), 1)
        for k in range(int(np.ceil(lo[1] * 100)), int(hi[1] * 100) + 1):
            y = H - 1 - int((k / 100 - lo[1]) * 100 * px_per_cm)
            cv2.line(img, (0, y), (W - 1, y), (200, 200, 200) if k % 5 else (150, 150, 150), 1)
        uv = ((X[order][:, [i, j]] - lo) * 100 * px_per_cm).astype(int)
        uv[:, 1] = H - 1 - uv[:, 1]
        col = (rgb[order][:, ::-1] * 255).astype(np.uint8)
        ok = (a[order] > 0.2)
        img[uv[ok, 1].clip(0, H - 1), uv[ok, 0].clip(0, W - 1)] = col[ok]
        cv2.putText(img, name, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        panels.append(img)
    h = max(p.shape[0] for p in panels)
    panels = [cv2.copyMakeBorder(p, 0, h - p.shape[0], 0, 10, cv2.BORDER_CONSTANT,
                                 value=(255, 255, 255)) for p in panels]
    img = np.hstack(panels)
    img = cv2.copyMakeBorder(img, 26, 0, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    cv2.putText(img, f"{title}: grid 1 cm (dark every 5 cm)", (6, 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1)
    cv2.imwrite(str(path), img)


if __name__ == "__main__":
    main()
