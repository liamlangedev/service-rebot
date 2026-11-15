"""Fit the external cameras' poses and focal lengths to real frames.

Evidence, in workspace coordinates (see real_setup.json), fitted with a pinhole
model (MuJoCo's camera model: principal point at the image centre, square
pixels, no distortion):

* hand-picked landmarks in reference_photos/cameras/*.jpeg: base-plate and bin
  corners (points) and wall/table junctions and the bin's bottom edge (lines,
  point-to-line residuals, so their end points needn't be visible);
* for cam_corner (the C920), the table homography measured on the real arm in the
  classic_real branch (ros2_ws/.../config/calibration.yaml: 5 marks touched with
  the closed gripper and read from forward kinematics, 2.48 mm error). It maps
  1280x720 pixels to base_link metres on the table, so it pins the camera to the
  arm itself. It is turned into a grid of point correspondences over the area
  the marks covered.

The base plate is part of the robot's mesh (20 x 14 x 1.4 cm, centred on joint 1).

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

_CFG = json.loads(Path(DEFAULT_CONFIG).read_text())
ROBOT_L = _CFG["robot"]["from_left"]   # joint-1 axis, workspace coords
ROBOT_N = _CFG["robot"]["from_near"]
_BIN = _CFG["bin"]
BIN_E = _BIN["from_left"] + _BIN["size_left_right"]   # bin side towards the robot
BIN_NEAR, BIN_FAR = _BIN["from_near"], _BIN["from_near"] + _BIN["size_near_far"]
BIN_TOP = _BIN["height"]

# Base plate = robot mesh `base_link_matte_black` (measured from the mesh).
PLATE_HALF_LR, PLATE_HALF_NF, PLATE_T = 0.10, 0.07, 0.014

# Table homography from the real arm (classic_real branch, 2026-11-15T07:32):
# [x, y, 1] ~ H @ [u, v, 1], pixels of the C920 at 1280x720 -> base_link metres.
TABLE_H = np.array([0.0004667, 0.00115046, -0.42378476,
                    0.00075495, -0.0006639, -0.17915145,
                    -0.00020751, 0.00100864, 1.0]).reshape(3, 3)
TABLE_H_SIZE = (1280, 720)
TABLE_H_REGION = dict(x=(0.15, 0.45), y=(-0.20, 0.20))  # where the marks were

# The gripper camera sees no fixed landmarks, so it was matched by rendering
# candidate mounts next to reference_photos/cameras/gripper_camera_view.jpeg
# (fingers entering from the bottom corners, tips at mid-height). end_link frame:
# +x along the fingers (tips at 0), +y finger travel, +z away from the finger plane.
WRIST = {"pos": [-0.09, 0.0, 0.03], "look_at": [0.02, 0.0, -0.012], "fovy": 67.0,
         "aspect": [16, 9],
         "_calibrated": "matched by eye to reference_photos/cameras/gripper_camera_view.jpeg"}


def plate(corner: str, top: bool):
    """Base-plate corner, corner in {ne, nw, fe, fw} (near/far, east/west)."""
    l = ROBOT_L + (PLATE_HALF_LR if corner[1] == "e" else -PLATE_HALF_LR)
    n = ROBOT_N + (-PLATE_HALF_NF if corner[0] == "n" else PLATE_HALF_NF)
    return (l, n, PLATE_T if top else 0.0)


def homography_points(n: int = 5):
    """Grid of (workspace point, 1920x1080 pixel) pairs from the table homography."""
    Hinv = np.linalg.inv(TABLE_H)
    s = W / TABLE_H_SIZE[0]
    out = []
    for x in np.linspace(*TABLE_H_REGION["x"], n):
        for y in np.linspace(*TABLE_H_REGION["y"], n):
            p = Hinv @ np.array([x, y, 1.0])
            px = (p[0] / p[2] * s, p[1] / p[2] * s)
            out.append((f"table map ({x:.2f}, {y:+.2f})",
                        (ROBOT_L - y, ROBOT_N + x, 0.0), px))
    return out


# ----------------------------------------------------------------- observations
# Points: (label, workspace (from_left, from_near, height), pixel)
# Lines:  (label, [3D sample points along the edge], two pixels on the image line)
CAMERAS = {
    "cam_far": dict(
        photo="center_camera_view.jpeg",
        init=dict(pos=(0.36, 0.84, 0.30), look=(0.45, 0.30, 0.0), f=900.0),
        points=[
            ("table corner at near/right walls", (0.98, 0.0, 0.0), (805, 241)),
            ("bin far-from-cam top corner", (BIN_E, BIN_NEAR, BIN_TOP), (1472, 281)),
            ("bin far-from-cam bottom corner", (BIN_E, BIN_NEAR, 0.0), (1400, 426)),
            ("bin near-to-cam bottom corner", (BIN_E, BIN_FAR, 0.0), (1343, 822)),
            ("plate far-west corner (bottom)", plate("fw", False), (1174, 364)),
            ("plate near-west corner (top)", plate("nw", True), (1203, 307)),
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
        # The table map makes f observable, but keep it near the C920's spec
        # (43.3 deg vertical at 16:9).
        init=dict(pos=(0.85, 0.59, 0.55), look=(0.5, 0.3, 0.0),
                  f=540 / np.tan(np.radians(43.3 / 2)), f_weight=50.0),
        points=[
            ("plate near-east corner (top)", plate("ne", True), (401, 297)),
            ("plate far-east corner (bottom)", plate("fe", False), (525, 443)),
            ("plate far-west corner (top)", plate("fw", True), (836, 277)),
            ("plate near-west corner (top)", plate("nw", True), (728, 161)),
            ("bin far-east bottom corner", (BIN_E, BIN_FAR, 0.0), (1638, 640)),
        ] + homography_points(),
        lines=[
            ("bin east side on the table",
             [(BIN_E, n, 0.0) for n in np.linspace(BIN_NEAR + 0.05, BIN_FAR, 6)],
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
    return cams


def residuals(x, names, R0):
    cams = unpack(x, names)
    out = []
    for n in names:
        C, r, f = cams[n]
        R = R0[n] @ rodrigues(r)
        obs = CAMERAS[n]
        for _, P, px in obs["points"]:
            uv, depth = project(R, C, f, P)
            out.extend(uv - px if depth > 0 else [1e3, 1e3])
        for _, samples, (a, b) in obs["lines"]:
            a, b = np.array(a, float), np.array(b, float)
            nrm = np.array([-(b - a)[1], (b - a)[0]]) / np.linalg.norm(b - a)
            for P in samples:
                uv, depth = project(R, C, f, P)
                out.append(0.5 * (uv - a) @ nrm if depth > 0 else 1e3)  # 6 samples ~ 3 points
        # Weak priors: measured height, spec focal length (only matter if the
        # observations can't decide).
        ini = obs["init"]
        out.append(20 * (C[2] - ini["pos"][2]))
        if "f_weight" in ini:
            out.append(ini["f_weight"] * np.log(f / ini["f"]))
    return np.array(out)


def fit(names):
    R0, x0 = {}, []
    for n in names:
        ini = CAMERAS[n]["init"]
        C = to_xyz(ini["pos"])
        R0[n] = lookat_R(C, to_xyz(ini["look"]))
        x0 += [*C, 0, 0, 0, np.log(ini["f"])]
    x = np.array(x0, float)
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
    cams = unpack(x, names)
    res = {}
    for n in names:
        C, r, f = cams[n]
        R = R0[n] @ rodrigues(r)
        # A look-at point: where the optical axis hits the table (or 0.5 m ahead).
        d = -R[:, 2]
        t = -C[2] / d[2] if d[2] < -1e-6 else 0.5
        hit = C + t * d
        fovy = np.degrees(2 * np.arctan(H / 2 / f))
        fovd = np.degrees(2 * np.arctan(np.hypot(W, H) / 2 / f))
        # Roll about the optical axis, relative to a level camera (image up =
        # world up) looking at the same point; scene.py applies it the same way.
        L = lookat_R(C, hit)
        roll = np.degrees(np.arctan2(R[:, 0] @ L[:, 1], R[:, 0] @ L[:, 0]))
        errs = [(label, np.linalg.norm(project(R, C, f, P)[0] - px))
                for label, P, px in CAMERAS[n]["points"]]
        res[n] = dict(pos=tuple(C), look=(hit[0], hit[1], max(hit[2], 0.0)), fovy=fovy,
                      fov_diag=fovd, roll=roll, errs=errs, R=R, C=C, f=f)
    return res


def overlay(res, out: Path):
    import cv2
    out.mkdir(parents=True, exist_ok=True)
    for n, r in res.items():
        im = cv2.imread(str(SIM / "reference_photos" / "cameras" / CAMERAS[n]["photo"]))
        for label, P, px in CAMERAS[n]["points"]:
            uv, _ = project(r["R"], r["C"], r["f"], P)
            color = (255, 160, 0) if label.startswith("table map") else (0, 0, 255)
            cv2.circle(im, tuple(int(v) for v in px), 9, color, 2)
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
    res = summary(x, names, R0)
    for n, r in res.items():
        print(f"\n{n}: pos (from_left, from_near, height) = "
              f"({r['pos'][0]:.3f}, {r['pos'][1]:.3f}, {r['pos'][2]:.3f}) m")
        print(f"  looks at ({r['look'][0]:.3f}, {r['look'][1]:.3f}, {r['look'][2]:.3f}),"
              f" roll {r['roll']:+.1f} deg")
        print(f"  fovy {r['fovy']:.1f} deg (diagonal {r['fov_diag']:.1f} deg at 16:9)")
        tm = [e for label, e in r["errs"] if label.startswith("table map")]
        for label, e in r["errs"]:
            if not label.startswith("table map"):
                print(f"    {e:5.1f} px  {label}")
        if tm:
            print(f"    table map: {len(tm)} points, mean {np.mean(tm):.1f} px, max {np.max(tm):.1f} px")
    if args.overlay:
        overlay(res, Path(args.overlay))
        print(f"\noverlays -> {args.overlay} (red = picked, blue = table map, green = fitted)")
    if args.write:
        path = DEFAULT_CONFIG
        cfg = json.loads(path.read_text())
        for cam in cfg["cameras"]:
            r = res[cam["name"]]
            cam["from_left"], cam["from_near"], cam["height"] = (round(v, 3) for v in r["pos"])
            cam["look_at"] = [round(v, 3) for v in r["look"]]
            cam["roll_deg"] = round(r["roll"], 1)
            cam.pop("fov_diagonal_deg", None)
            cam["fovy"] = round(r["fovy"], 1)
            cam["aspect"] = [16, 9]
            cam["_calibrated"] = ("tools/calibrate_cameras.py: reference_photos/cameras"
                                  + (" + the real arm's table homography (classic_real)"
                                     if cam["name"] == "cam_corner" else ""))
        cfg["wrist_camera"].pop("fov_diagonal_deg", None)
        cfg["wrist_camera"].update(WRIST)
        path.write_text(json.dumps(cfg, indent=2) + "\n")
        print(f"updated {path}")


if __name__ == "__main__":
    main()
