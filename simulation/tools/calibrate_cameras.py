"""Fit the external cameras' poses and focal lengths to real frames.

Hand-picked correspondences between scene landmarks (in workspace coordinates,
see real_setup.json) and pixels in reference_photos/cameras/*.jpeg are fitted
with a pinhole model (MuJoCo's camera model: principal point at the image
centre, square pixels, no distortion). Points give point-to-point residuals;
straight edges (wall/table junctions, the bin's bottom edge) give
point-to-line residuals, so their end points needn't be visible.
The base plate's size was never measured, so it is fitted too (shared by
both cameras).

  uv run --project ../teleoperation tools/calibrate_cameras.py           # fit + report
  uv run --project ../teleoperation tools/calibrate_cameras.py --write   # update real_setup.json
  uv run --project ../teleoperation tools/calibrate_cameras.py --overlay out/  # draw on photos
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

SIM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SIM))
from rebot_sim.scene import DEFAULT_CONFIG  # noqa: E402

W, H = 1920, 1080  # real frame size of the cameras

# The gripper camera sees no fixed landmarks, so it was matched by rendering
# candidate mounts next to reference_photos/cameras/gripper_camera_view.jpeg
# (fingers entering from the bottom corners, tips at mid-height). end_link frame:
# +x along the fingers (tips at 0), +y finger travel, +z away from the finger plane.
WRIST = {"pos": [-0.09, 0.0, 0.03], "look_at": [0.02, 0.0, -0.012], "fovy": 67.0,
         "aspect": [16, 9],
         "_calibrated": "matched by eye to reference_photos/cameras/gripper_camera_view.jpeg"}

# Robot base axis (workspace coords); the plate is centred left-right on it and
# flush with the near wall.
ROBOT_L = 0.60


def plate(cfg_lr, cfg_nf, corner: str, top: bool):
    """Plate corner from its (fitted) size. corner in {ne, nw, fe, fw}."""
    l = ROBOT_L + (cfg_lr / 2 if corner[1] == "e" else -cfg_lr / 2)
    n = 0.0 if corner[0] == "n" else cfg_nf
    return (l, n, 0.012 if top else 0.0)


# ----------------------------------------------------------------- observations
# Points: (label, workspace (from_left, from_near, height) or plate spec, pixel)
# Lines:  (label, [3D sample points along the edge], two pixels on the image line)
CAMERAS = {
    "cam_far": dict(
        photo="center_camera_view.jpeg",
        init=dict(pos=(0.36, 0.84, 0.30), look=(0.45, 0.30, 0.0), f=900.0),
        points=[
            ("table corner at near/right walls", (0.98, 0.0, 0.0), (805, 241)),
            ("bin far-from-cam top corner", (0.25, 0.15, 0.12), (1472, 281)),
            ("bin far-from-cam bottom corner", (0.25, 0.15, 0.0), (1400, 426)),
            ("bin near-to-cam bottom corner", (0.25, 0.55, 0.0), (1343, 822)),
            ("plate far-west corner (bottom)", ("plate", "fw", False), (1174, 364)),
            ("plate near-west corner (top)", ("plate", "nw", True), (1203, 307)),
        ],
        lines=[
            ("table / right wall", [(0.98, n, 0.0) for n in np.linspace(0.05, 0.6, 6)],
             ((123, 562), (799, 240))),
            ("table / near wall", [(l, 0.0, 0.0) for l in np.linspace(0.3, 0.9, 6)],
             ((1300, 343), (1421, 360))),
        ],
    ),
    "cam_corner": dict(
        photo="corner_camera_view.jpeg",
        # Nearly all landmarks lie on the table plane, so focal length and distance
        # trade off; pin f to the C920's spec (43.3 deg vertical at 1080p).
        init=dict(pos=(0.98, 0.84, 0.60), look=(0.5, 0.3, 0.0), f=540 / np.tan(np.radians(43.3 / 2)),
                  f_weight=200.0),
        points=[
            ("plate near-east corner (top)", ("plate", "ne", True), (401, 297)),
            ("plate far-east corner (bottom)", ("plate", "fe", False), (525, 443)),
            ("plate far-west corner (top)", ("plate", "fw", True), (836, 277)),
            ("plate near-west corner (top)", ("plate", "nw", True), (728, 161)),
            ("bin far-east bottom corner", (0.25, 0.55, 0.0), (1638, 640)),
        ],
        lines=[
            ("bin east side on the table", [(0.25, n, 0.0) for n in np.linspace(0.2, 0.55, 6)],
             ((1638, 640), (1530, 540))),
            ("table / near wall", [(l, 0.0, 0.0) for l in np.linspace(0.75, 0.98, 6)],
             ((0, 460), (401, 297))),
        ],
    ),
}


# ----------------------------------------------------------------- camera model
def rodrigues(r):
    th = np.linalg.norm(r)
    if th < 1e-12:
        return np.eye(3)
    k = r / th
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * K @ K


def lookat_R(pos, target):
    """Camera-to-workspace rotation (MuJoCo convention: looks along -z, y up)."""
    z = np.asarray(pos, float) - np.asarray(target, float)
    z /= np.linalg.norm(z)
    x = np.cross([0, 0, 1], z)
    x /= np.linalg.norm(x)
    return np.column_stack([x, np.cross(z, x), z])


def to_xyz(p):
    """Workspace coords (from_left, from_near, height) already form a right-handed
    frame: x east (towards the right wall), y north (towards the far edge), z up."""
    return np.array(p, float)


def project(R, C, f, P):
    pc = R.T @ (to_xyz(P) - C)
    return np.array([W / 2 + f * pc[0] / -pc[2], H / 2 - f * pc[1] / -pc[2]]), -pc[2]


# ----------------------------------------------------------------- fitting
def unpack(x, names):
    cams = {}
    for i, n in enumerate(names):
        c = x[7 * i:7 * i + 7]
        cams[n] = (c[0:3], c[3:6], np.exp(c[6]))  # focal length as log(f) stays > 0
    lr, nf = x[-2:]
    return cams, lr, nf


def resolve(P, lr, nf):
    if isinstance(P[0], str):
        return plate(lr, nf, P[1], P[2])
    return P


def residuals(x, names, R0):
    cams, lr, nf = unpack(x, names)
    out = []
    for n in names:
        C, r, f = cams[n]
        R = R0[n] @ rodrigues(r)
        obs = CAMERAS[n]
        for _, P, px in obs["points"]:
            uv, depth = project(R, C, f, resolve(P, lr, nf))
            out.extend(uv - px if depth > 0 else [1e3, 1e3])
        for _, samples, (a, b) in obs["lines"]:
            a, b = np.array(a, float), np.array(b, float)
            nrm = np.array([-(b - a)[1], (b - a)[0]]) / np.linalg.norm(b - a)
            for P in samples:
                uv, depth = project(R, C, f, P)
                out.append(0.5 * (uv - a) @ nrm if depth > 0 else 1e3)  # 6 samples ~ 3 points
    # Weak priors: plate size near the photo estimate, cameras at their measured
    # heights (only matters if the points can't decide).
    out.append(50 * (lr - 0.19))
    out.append(50 * (nf - 0.15))
    for n in names:
        ini = CAMERAS[n]["init"]
        out.append(20 * (cams[n][0][2] - ini["pos"][2]))
        if "f_weight" in ini:  # focal length known from the spec sheet
            out.append(ini["f_weight"] * np.log(cams[n][2] / ini["f"]))
    return np.array(out)


def fit(names):
    R0, x0 = {}, []
    for n in names:
        ini = CAMERAS[n]["init"]
        C = to_xyz(ini["pos"])
        R0[n] = lookat_R(C, to_xyz(ini["look"]))
        x0 += [*C, 0, 0, 0, np.log(ini["f"])]
    x = np.array(x0 + [0.19, 0.15], float)
    lam = 1e-2
    r = residuals(x, names, R0)
    for _ in range(300):  # Levenberg-Marquardt, numeric Jacobian
        J = np.empty((r.size, x.size))
        for j in range(x.size):
            d = np.zeros_like(x)
            d[j] = 1e-6 * max(1.0, abs(x[j]))
            J[:, j] = (residuals(x + d, names, R0) - r) / d[j]
        A = J.T @ J
        g = J.T @ r
        while True:
            step = np.linalg.solve(A + lam * np.diag(np.diag(A) + 1e-9), -g)
            r_new = residuals(x + step, names, R0)
            if r_new @ r_new < r @ r:
                x, r, lam = x + step, r_new, lam * 0.3
                break
            lam *= 10
            if lam > 1e12:
                break
        if np.linalg.norm(step) < 1e-10 or lam > 1e12:
            break
    return x, R0


def summary(x, names, R0):
    cams, lr, nf = unpack(x, names)
    res = {}
    for n in names:
        C, r, f = cams[n]
        R = R0[n] @ rodrigues(r)
        pos_ws = tuple(C)
        # A look-at point: where the optical axis hits the table (or 0.5 m ahead).
        d = -R[:, 2]
        t = -C[2] / d[2] if d[2] < -1e-6 else 0.5
        hit = C + t * d
        look_ws = (hit[0], hit[1], max(hit[2], 0.0))
        fovy = np.degrees(2 * np.arctan(H / 2 / f))
        fovd = np.degrees(2 * np.arctan(np.hypot(W, H) / 2 / f))
        # Roll about the optical axis, relative to a level camera (image up =
        # world up) looking at the same point; scene.py applies it the same way.
        L = lookat_R(C, hit)
        roll = np.degrees(np.arctan2(R[:, 0] @ L[:, 1], R[:, 0] @ L[:, 0]))
        errs = []
        for label, P, px in CAMERAS[n]["points"]:
            uv, _ = project(R, C, f, resolve(P, lr, nf))
            errs.append((label, np.linalg.norm(uv - px)))
        res[n] = dict(pos=pos_ws, look=look_ws, fovy=fovy, fov_diag=fovd, roll=roll,
                      errs=errs, R=R, C=C, f=f)
    return res, lr, nf


def overlay(res, lr, nf, out: Path):
    import cv2
    out.mkdir(parents=True, exist_ok=True)
    for n, r in res.items():
        im = cv2.imread(str(SIM / "reference_photos" / "cameras" / CAMERAS[n]["photo"]))
        for label, P, px in CAMERAS[n]["points"]:
            uv, _ = project(r["R"], r["C"], r["f"], resolve(P, lr, nf))
            cv2.circle(im, tuple(int(v) for v in px), 9, (0, 0, 255), 2)
            cv2.drawMarker(im, tuple(int(v) for v in uv), (0, 255, 0), cv2.MARKER_CROSS, 22, 2)
        for _, samples, (a, b) in CAMERAS[n]["lines"]:
            cv2.line(im, a, b, (0, 0, 255), 2)
            pts = [project(r["R"], r["C"], r["f"], P)[0] for P in samples]
            for p, q in zip(pts, pts[1:]):
                cv2.line(im, tuple(int(v) for v in p), tuple(int(v) for v in q), (0, 255, 0), 2)
        cv2.imwrite(str(out / f"{n}_fit.jpg"), im)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--write", action="store_true", help="update real_setup.json")
    p.add_argument("--overlay", default=None, help="folder for photos with the fit drawn on")
    args = p.parse_args()

    names = list(CAMERAS)
    x, R0 = fit(names)
    res, lr, nf = summary(x, names, R0)
    print(f"base plate: {lr * 100:.1f} cm (left-right) x {nf * 100:.1f} cm (near-far)")
    for n, r in res.items():
        print(f"\n{n}: pos (from_left, from_near, height) = "
              f"({r['pos'][0]:.3f}, {r['pos'][1]:.3f}, {r['pos'][2]:.3f}) m")
        print(f"  looks at ({r['look'][0]:.3f}, {r['look'][1]:.3f}, {r['look'][2]:.3f}),"
              f" roll {r['roll']:+.1f} deg")
        print(f"  fovy {r['fovy']:.1f} deg (diagonal {r['fov_diag']:.1f} deg at 16:9)")
        for label, e in r["errs"]:
            print(f"    {e:5.1f} px  {label}")
    if args.overlay:
        overlay(res, lr, nf, Path(args.overlay))
        print(f"\noverlays -> {args.overlay} (red = picked, green = fitted)")
    if args.write:
        path = DEFAULT_CONFIG
        cfg = json.loads(path.read_text())
        for cam in cfg["cameras"]:
            r = res[cam["name"]]
            cam["from_left"], cam["from_near"], cam["height"] = (round(v, 3) for v in r["pos"])
            cam["look_at"] = [round(v, 3) for v in r["look"]]
            cam["roll_deg"] = round(r["roll"], 1)
            cam.pop("fov_diagonal_deg", None)
            cam["_comment"] = cam.get("_comment", "").split(";")[0] + "; pose and fovy fitted to the real frame"
            cam["fovy"] = round(r["fovy"], 1)
            cam["aspect"] = [16, 9]
            cam["_calibrated"] = "tools/calibrate_cameras.py against reference_photos/cameras"
        cfg["wrist_camera"].pop("fov_diagonal_deg", None)
        cfg["wrist_camera"].update(WRIST)
        cfg["base_plate"]["size_left_right"] = round(lr, 3)
        cfg["base_plate"]["size_near_far"] = round(nf, 3)
        # Keep the plate's near edge on the wall (the fit assumes it).
        cfg["base_plate"]["center_offset_near_far"] = round(nf / 2 - cfg["robot"]["from_near"], 4)
        path.write_text(json.dumps(cfg, indent=2) + "\n")
        print(f"updated {path}")


if __name__ == "__main__":
    main()
