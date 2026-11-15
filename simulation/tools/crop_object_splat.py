"""Cut one object out of a splat trained on a phone video and scale it to metres.

  ../teleoperation/.venv/bin/python tools/crop_object_splat.py splats/towel/splat.ply \
      --object splats/towel/object.json --out splats/towel_object.ply

The splat comes from hf_jobs/train_splat.sh on a video that circles one object
(prepare_splat_dataset.py --standalone --object ...). It is in nerfstudio's
training frame; transforms.json next to it (and dataparser_transforms.json, if
present) give the cameras. Steps:

1. normalise with the cameras: origin where their optical axes meet (the object),
   z along their mean up vector, unit = their median distance to that point;
2. segment the object: dense voxels near the origin, the connected component
   closest to it (a textureless table only gives a diffuse cloud, so it is not
   used);
3. its principal axis is its length: vertical if upright, along the table if
   lying. Measure the length there and scale it to object.json;
4. keep the gaussians in a box around it, in the object's frame: origin at the
   centre of its base, z up, x along its length if lying. Units are metres.

Positions, orientations, sizes and the view-dependent colour (SH) are all
transformed, so the result renders correctly in any 3DGS viewer. It also writes
<out>.json (the measured sizes and the transform) and <out>.png (top and side
views on a 1 cm grid) to check the crop.
"""
import argparse
import json
from collections import deque
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


# ---------------------------------------------------------------- cameras

def _rotation_between(a, b):
    """nerfstudio's rotation_matrix(a, b): the rotation taking a onto b."""
    a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
    v, c = np.cross(a, b), a @ b
    k = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + k + k @ k * ((1 - c) / (v @ v + 1e-8))


def dataparser_transform(T):
    """The splat is trained (and exported) in nerfstudio's dataparser frame, not the
    transforms.json frame. Recompute it as nerfstudio does with its defaults
    (orientation_method=up, center_method=poses, auto_scale_poses): returns (3x4, scale)."""
    R = _rotation_between(T[:, :3, 1].mean(0), np.array([0.0, 0, 1]))
    M = np.c_[R, R @ -T[:, :3, 3].mean(0)]
    pos = T[:, :3, 3] @ R.T + M[:, 3]
    return M, 1.0 / np.abs(pos).max()


def camera_rig(transforms, dataparser=None):
    """Cameras from nerfstudio transforms.json (OpenGL: look along -z, +y up), moved
    into the splat's frame: the point nearest to all optical axes, the mean up vector
    and the median camera distance to that point."""
    T = np.array([f["transform_matrix"] for f in transforms["frames"]], float)
    if dataparser:
        M, scale = np.array(dataparser["transform"], float), dataparser["scale"]
    else:
        M, scale = dataparser_transform(T)
    T = np.einsum("ij,njk->nik", M[:, :3], T[:, :3, :4])
    T[:, :3, 3] = (T[:, :3, 3] + M[:, 3]) * scale
    C, fwd, up = T[:, :3, 3], -T[:, :3, 2], T[:, :3, 1]
    A, b = np.zeros((3, 3)), np.zeros(3)
    for c, f in zip(C, fwd):
        M = np.eye(3) - np.outer(f, f)
        A += M
        b += M @ c
    o = np.linalg.solve(A, b)
    up = up.mean(0)
    return o, up / np.linalg.norm(up), float(np.median(np.linalg.norm(C - o, axis=1)))




def segment(P, voxel=0.02, radius=0.9, near=0.4):
    """Indices of the object: dense voxels inside `radius`, 26-connected, the largest
    component whose centre is within `near` of the origin (normalised units)."""
    idx = np.nonzero(np.linalg.norm(P, axis=1) < radius)[0]
    keys = np.floor(P[idx] / voxel).astype(np.int64)
    uniq, inv, counts = np.unique(keys, axis=0, return_inverse=True, return_counts=True)
    inv = inv.ravel()
    dense = counts >= max(3, np.percentile(counts, 60))
    cell = {tuple(k): i for i, k in enumerate(uniq) if dense[i]}
    label, comps = {}, []
    offs = [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)]
    for start in cell:
        if start in label:
            continue
        label[start] = len(comps)
        members, q = [], deque([start])
        while q:
            k = q.popleft()
            members.append(cell[k])
            for o in offs:
                nb = (k[0] + o[0], k[1] + o[1], k[2] + o[2])
                if nb in cell and nb not in label:
                    label[nb] = len(comps)
                    q.append(nb)
        comps.append(members)
    best, best_n = None, 0
    for members in comps:
        n = counts[members].sum()
        centre = (uniq[members].mean(0) + 0.5) * voxel
        if np.linalg.norm(centre) < near and n > best_n:
            best, best_n = members, n
    if best is None:
        raise SystemExit("no object found near the cameras' focus")
    return idx[np.isin(inv, best)]


def extent(v, lo=0.5, hi=99.5):
    return np.percentile(v, lo), np.percentile(v, hi)


def principal_axis(d):
    return np.linalg.svd(d, full_matrices=False)[2][0]


def grow_column(P, seed, up, unit, binw=0.02, gap=0.2, rel=0.15, iters=4):
    """An upright object from its dense seed (e.g. a bottle's cap and label): walk
    along its axis in bins of `binw` while bins are dense, bridging sparse runs up
    to `gap` (transparent glass), then refit the axis and repeat. Lengths are in
    units of `unit` (the camera orbit). Returns (centre, axis, points)."""
    c, axis = np.median(seed, axis=0), up.copy()
    d = seed - c
    rad = np.linalg.norm(d - np.outer(d @ axis, axis), axis=1)
    rc = max(0.05 * unit, 1.25 * np.percentile(rad, 95))
    for _ in range(iters):
        d = P - c
        t = d @ axis
        rad = np.linalg.norm(d - np.outer(t, axis), axis=1)
        sel = np.nonzero((rad < rc) & (np.abs(t) < 1.2 * unit))[0]
        b = np.floor(t[sel] / (binw * unit)).astype(int)
        b0 = b.min()
        counts = np.bincount(b - b0)
        dense = counts >= rel * np.percentile(counts[counts > 0], 90)
        start = int(np.clip(-b0, 0, len(counts) - 1))
        start = np.nonzero(dense)[0][np.argmin(np.abs(np.nonzero(dense)[0] - start))]
        ends = []
        for step in (1, -1):
            k = end = start
            miss = 0
            while 0 <= k + step < len(counts) and miss <= gap / binw:
                k += step
                if dense[k]:
                    end, miss = k, 0
                else:
                    miss += 1
            ends.append(end)
        hi, lo = ends
        pts = P[sel[(b - b0 >= lo) & (b - b0 <= hi)]]
        c = np.median(pts, axis=0)
        axis = principal_axis(pts - c)
        axis *= np.sign(axis @ up)
    return c, axis, pts


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ply")
    p.add_argument("--object", required=True, help="object.json from the dataset")
    p.add_argument("--out", required=True)
    p.add_argument("--transforms", help="camera poses (default: transforms.json next to the ply)")
    p.add_argument("--min-opacity", type=float, default=0.3)
    p.add_argument("--margin", type=float, default=0.1,
                   help="extra room around the object, as a fraction of its size")
    args = p.parse_args()

    meta = json.loads(Path(args.object).read_text())
    L, D, pose = meta["length"], meta["diameter"], meta["pose"]
    v = read_ply(args.ply)
    P0 = np.stack([v["x"], v["y"], v["z"]], 1).astype(np.float64)
    alpha = 1 / (1 + np.exp(-v["opacity"].astype(np.float64)))
    good = (alpha > args.min_opacity) & np.isfinite(P0).all(1)

    # 1. normalise with the cameras
    tf = Path(args.transforms) if args.transforms else Path(args.ply).with_name("transforms.json")
    dp = tf.with_name("dataparser_transforms.json")
    o, up, orbit = camera_rig(json.loads(tf.read_text()),
                              json.loads(dp.read_text()) if dp.exists() else None)
    P = (P0 - o) @ frame_from_normal(up).T / orbit
    print(f"cameras: focus {o.round(3)}, orbit radius {orbit:.3f} units")

    # 2. segment the object: a dense seed; an upright object then grows along its axis
    gi = np.nonzero(good)[0]
    seed = gi[segment(P[gi])]
    if pose == "upright":
        m, axis, Po = grow_column(P0[good], P0[seed], up, orbit)
    else:
        Po = P0[seed]
        m = np.median(Po, axis=0)
        axis = principal_axis(Po - m)
    print(f"object: {len(Po)} gaussians (seed {len(seed)})")

    # 3. principal axis = length; object frame rows R (x, y, z) in splat coordinates
    if pose == "upright":
        R = frame_from_normal(axis)
        tilt = np.degrees(np.arccos(np.clip(axis @ up, -1, 1)))
    else:
        z = up - (up @ axis) * axis
        z /= np.linalg.norm(z)
        R = np.stack([axis, np.cross(z, axis), z])
        tilt = 90 - np.degrees(np.arccos(np.clip(abs(axis @ up), -1, 1)))
    Q = (Po - m) @ R.T
    if pose == "upright":
        lo, hi = extent(Q[:, 2])
        measured = hi - lo
        measured_d = 2 * np.percentile(np.linalg.norm(Q[:, :2] - np.median(Q[:, :2], 0), axis=1), 90)
        base = np.r_[np.median(Q[:, :2], 0), lo]
    else:
        lo, hi = extent(Q[:, 0])
        measured = hi - lo
        zlo, zhi = extent(Q[:, 2])
        measured_d = zhi - zlo
        base = np.array([(lo + hi) / 2, np.median(Q[:, 1]), zlo])
    s = L / measured
    print(f"{meta['object']}: length {measured:.4f} units = {L * 100:g} cm -> scale {s:.4f} m/unit; "
          f"axis {tilt:.1f} deg off {'vertical' if pose == 'upright' else 'horizontal'}")
    print(f"  diameter then measures {measured_d * s * 100:.1f} cm (given {D * 100:g} cm)")

    # 4. object frame in metres: X = s * R (P0 - p0); p0 = centre of the base
    p0 = m + base @ R
    X = s * (P0 - p0) @ R.T
    d = max(D, measured_d * s)
    if pose == "upright":
        half, zr = np.array([d, d]) / 2, (L, L)
    else:
        half, zr = np.array([L, d]) / 2, (d, d)
    half = half * (1 + args.margin) + 0.01
    gsize = s * np.exp(np.stack([v[f"scale_{i}"] for i in range(3)], 1).astype(np.float64)).max(1)
    keep = ((np.abs(X[:, :2]) < half).all(1) & (X[:, 2] > -0.003) &
            (X[:, 2] < zr[1] * (1 + args.margin) + 0.01) & (gsize < 0.5 * d) &
            np.isfinite(X).all(1))

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
        n_coef = len(rest) // 3
        M = sh_rotation(R, n_coef)
        for ch in range(3):
            ks = rest[ch * n_coef:(ch + 1) * n_coef]
            C = np.stack([out[k] for k in ks], 1).astype(np.float64) @ M.T
            for j, k in enumerate(ks):
                out[k] = C[:, j]

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    write_ply(outp, out)
    info = {"object": meta["object"], "pose": pose, "given": meta,
            "measured_length_units": measured, "scale_m_per_unit": s,
            "measured_diameter_m": measured_d * s, "axis_tilt_deg": tilt,
            "n_gaussians": int(keep.sum()),
            "frame": "origin at the centre of the object's base, z up, x along the "
                     "length when lying; metres",
            "splat_to_object": {"scale": s, "R": R.tolist(), "p0": p0.tolist(),
                                "formula": "X = scale * R @ (p - p0)"}}
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
