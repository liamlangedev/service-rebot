#!/usr/bin/env python3
"""Calibration for the real setup (3 cameras + arm). Run the steps in order, once;
afterwards do not move the cameras or the table.

  1. python -m autonomy.calibrate list-cameras                       # which /dev/video index is which
  2. python -m autonomy.calibrate make-sheet                          # print aruco_sheet.png at 100 %
  3. python -m autonomy.calibrate intrinsics --camera top --fov-deg 70   (quick)  or
     python -m autonomy.calibrate intrinsics --camera top --board 9x6 --square 0.025  (better)
     ... for every camera (top, side, wrist)
  4. python -m autonomy.calibrate markers   --config autonomy/config/real.json
        tape the sheet to the table, jog the gripper tip onto each marker centre, press Enter
        -> marker positions in the robot frame + table height
  5. python -m autonomy.calibrate extrinsics --config ...   # fixed cameras: pose from the markers
  6. python -m autonomy.calibrate wrist      --config ...   # wrist camera mount from 5 hover poses
  7. python -m autonomy.calibrate check      --config ...   # reprojection error + overlay images

Everything is written to the "calibration" file named in the config
(default autonomy/config/calibration.json).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DICT = "DICT_4X4_50"


def _aruco():
    import cv2
    d = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, DICT))
    return cv2, d, cv2.aruco.ArucoDetector(d, cv2.aruco.DetectorParameters())


def detect_markers(image_rgb) -> dict[int, np.ndarray]:
    """marker id -> centre pixel."""
    cv2, _, det = _aruco()
    corners, ids, _ = det.detectMarkers(cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY))
    if ids is None:
        return {}
    return {int(i): c.reshape(4, 2).mean(0) for i, c in zip(ids.ravel(), corners)}


def solve_extrinsics(world_pts, img_pts, K, dist):
    """World points (N>=4) + pixels -> T_world_cam (4x4), RMS reprojection error [px]."""
    import cv2
    wp = np.asarray(world_pts, np.float64)
    ip = np.asarray(img_pts, np.float64)
    ok, rvec, tvec = cv2.solvePnP(wp, ip, K, dist, flags=cv2.SOLVEPNP_ITERATIVE if len(wp) >= 6 else cv2.SOLVEPNP_SQPNP)
    if not ok:
        raise RuntimeError("solvePnP failed")
    rvec, tvec = cv2.solvePnPRefineLM(wp, ip, K, dist, rvec, tvec)
    R_cw, _ = cv2.Rodrigues(rvec)              # world -> camera
    proj, _ = cv2.projectPoints(wp, rvec, tvec, K, dist)
    rms = float(np.sqrt(np.mean(np.sum((proj.reshape(-1, 2) - ip) ** 2, axis=1))))
    T = np.eye(4)
    T[:3, :3] = R_cw.T
    T[:3, 3] = (-R_cw.T @ tvec).ravel()
    return T, rms


def average_transforms(Ts) -> np.ndarray:
    """Mean of rigid transforms (rotation via SVD projection)."""
    R = sum(T[:3, :3] for T in Ts)
    U, _, Vt = np.linalg.svd(R)
    Rm = U @ np.diag([1, 1, np.linalg.det(U @ Vt)]) @ Vt
    out = np.eye(4)
    out[:3, :3] = Rm
    out[:3, 3] = np.mean([T[:3, 3] for T in Ts], axis=0)
    return out


# ---- helpers using the configured hardware ---------------------------------------
def _load(cfg_path):
    cfg = json.loads(Path(cfg_path).read_text())
    cal_path = HERE.parent / cfg.get("calibration", "autonomy/config/calibration.json")
    cal = json.loads(cal_path.read_text()) if cal_path.exists() else {"cameras": {}}
    return cfg, cal_path, cal


def _save(cal_path, cal):
    cal_path.parent.mkdir(parents=True, exist_ok=True)
    cal_path.write_text(json.dumps(cal, indent=2))
    print(f"saved {cal_path}")


def _hardware(cfg_path):
    from autonomy.app import build
    ns = argparse.Namespace(robot=None, viewer=False, detector="color")
    return build(json.loads(Path(cfg_path).read_text()), ns)


def _key():
    import termios
    import tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def jog(arm, prompt="") -> np.ndarray | None:
    """Keyboard jog of the fingertips, gripper pointing down. Returns the tip position on Enter."""
    from autonomy.arm import TIP_OFFSET
    from autonomy.geometry import top_down_rotation
    R = top_down_rotation(np.pi / 2)
    tcp, rot = arm.fk()
    if np.degrees(np.arccos(np.clip(-rot[2, 0], -1, 1))) > 5 or tcp[0] < 0.15:
        tcp = np.array([0.30, 0.0, arm.safety.table_z + 0.20])    # start above the table
        arm.move_tcp(tcp, R)
    step = 0.01
    print(f"{prompt}\n  w/s: +x/-x  a/d: +y/-y  r/f: up/down  1/2/3: step 1/5/20 mm  Enter: record  q: skip")
    while True:
        k = _key()
        delta = {"w": (1, 0, 0), "s": (-1, 0, 0), "a": (0, 1, 0), "d": (0, -1, 0), "r": (0, 0, 1), "f": (0, 0, -1)}.get(k)
        if k in "123":
            step = {"1": 0.001, "2": 0.005, "3": 0.02}[k]
        elif delta is not None:
            target = tcp + step * np.array(delta)
            try:
                arm.move_tcp(target, R, linear=True, speed=0.3)
                tcp = target
            except Exception as e:  # unreachable or safety: stay put
                print(f"\r  blocked: {e}")
            tip = tcp + TIP_OFFSET * R[:, 0]
            print(f"\r  tip = {np.round(tip, 4)}  step {step * 1000:.0f} mm   ", end="", flush=True)
        elif k in ("\r", "\n"):
            print()
            return tcp + TIP_OFFSET * R[:, 0]
        elif k in ("q", "\x03"):
            print()
            return None


# ---- commands ----------------------------------------------------------------------
def cmd_list_cameras(a):
    import cv2
    out = HERE.parent / "runs" / "camera_probe"
    out.mkdir(parents=True, exist_ok=True)
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():
            continue
        ok, frame = cap.read()
        if ok:
            cv2.imwrite(str(out / f"device_{i}.jpg"), frame)
            print(f"device {i}: {frame.shape[1]}x{frame.shape[0]} -> {out / f'device_{i}.jpg'}")
        cap.release()


def cmd_make_sheet(a):
    cv2, d, _ = _aruco()
    px_per_mm = 300 / 25.4                       # 300 dpi
    size = int(a.marker_mm * px_per_mm)
    W, H = int(277 * px_per_mm), int(190 * px_per_mm)   # A4 landscape, 1 cm margins
    sheet = np.full((H, W), 255, np.uint8)
    for k in range(6):
        r, c = divmod(k, 3)
        x = int((20 + c * 90) * px_per_mm)
        y = int((25 + r * 95) * px_per_mm)
        sheet[y:y + size, x:x + size] = cv2.aruco.generateImageMarker(d, k, size)
        cv2.putText(sheet, f"id {k}", (x, y + size + 60), cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 4)
    path = HERE.parent / "aruco_sheet.png"
    cv2.imwrite(str(path), sheet)
    print(f"wrote {path}: print at 100 % (300 dpi), {a.marker_mm} mm markers, ids 0-5")


def cmd_intrinsics(a):
    import cv2
    cfg, cal_path, cal = _load(a.config)
    spec = next(c for c in cfg["cameras"] if c["name"] == a.camera)
    cap = cv2.VideoCapture(spec["device"])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, spec.get("width", 1280))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, spec.get("height", 720))
    ok, frame = cap.read()
    if not ok:
        sys.exit(f"camera {a.camera} gives no frames")
    h, w = frame.shape[:2]
    if a.fov_deg:
        from autonomy.geometry import intrinsics_from_fovy
        K, dist, rms = intrinsics_from_fovy(a.fov_deg, w, h), np.zeros(5), None
        print("approximate intrinsics from the vertical field of view (use --board for accuracy)")
    else:
        cols, rows = map(int, a.board.split("x"))
        objp = np.zeros((rows * cols, 3), np.float32)
        objp[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2) * a.square
        obj_pts, img_pts = [], []
        print(f"show the {a.board} chessboard at different angles/distances; collecting {a.views} views...")
        import time
        last = 0.0
        while len(img_pts) < a.views:
            ok, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            found, corners = cv2.findChessboardCorners(gray, (cols, rows))
            if found and time.time() - last > 1.0:
                corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                           (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-3))
                obj_pts.append(objp)
                img_pts.append(corners)
                last = time.time()
                print(f"  view {len(img_pts)}/{a.views}")
        rms, K, dist, _, _ = cv2.calibrateCamera(obj_pts, img_pts, (w, h), None, None)
        dist = dist.ravel()[:5]
        print(f"RMS reprojection error {rms:.2f} px (good: < 0.5)")
    cap.release()
    cam = cal["cameras"].setdefault(a.camera, {})
    cam.update({"K": np.asarray(K).tolist(), "dist": np.asarray(dist).tolist(), "width": w, "height": h,
                "intrinsics_rms_px": rms})
    _save(cal_path, cal)


def cmd_markers(a):
    cfg, cal_path, cal = _load(a.config)
    ctx = _hardware(a.config)
    arm = ctx.arm
    pts = {}
    try:
        for k in range(a.count):
            tip = jog(arm, f"\nMarker id {k}: touch its CENTRE with the closed fingertips")
            if tip is not None:
                pts[str(k)] = tip.tolist()
                print(f"  marker {k} at {np.round(tip, 4)}")
                arm.move_tcp(arm.fk()[0] + [0, 0, 0.03], arm.fk()[1], linear=True, speed=0.3)
    finally:
        arm.observe_pose()
        arm.close()
    if len(pts) < 4:
        sys.exit("need at least 4 markers")
    cal["markers"] = pts
    cal["table_z"] = float(np.mean([p[2] for p in pts.values()]))
    print(f"table_z = {cal['table_z']:.4f} m -> also put it in the config's world.table_z")
    _save(cal_path, cal)


def cmd_extrinsics(a):
    cfg, cal_path, cal = _load(a.config)
    ctx = _hardware(a.config)
    rig, arm = ctx.world.rig, ctx.arm
    try:
        arm.observe_pose()
        imgs = rig.grab(rig.scene)
    finally:
        arm.close()
    world = {int(k): np.array(v) for k, v in cal.get("markers", {}).items()}
    for name in rig.scene:
        seen = detect_markers(imgs[name])
        ids = [i for i in seen if i in world]
        if len(ids) < 4:
            print(f"{name}: only {len(ids)} known markers visible, skipped")
            continue
        c = cal["cameras"][name]
        T, rms = solve_extrinsics([world[i] for i in ids], [seen[i] for i in ids],
                                  np.array(c["K"]), np.array(c.get("dist", [0] * 5)))
        c.update({"T_world_cam": T.tolist(), "extrinsics_rms_px": rms})
        print(f"{name}: {len(ids)} markers, RMS {rms:.2f} px, camera at {np.round(T[:3, 3], 3)} m")
    _save(cal_path, cal)


def cmd_wrist(a):
    from autonomy.geometry import grasp_rotation, make_T, tilted_approach
    cfg, cal_path, cal = _load(a.config)
    ctx = _hardware(a.config)
    rig, arm = ctx.world.rig, ctx.arm
    world = {int(k): np.array(v) for k, v in cal.get("markers", {}).items()}
    center = np.mean(list(world.values()), axis=0)
    c = cal["cameras"][rig.wrist]
    K, dist = np.array(c["K"]), np.array(c.get("dist", [0] * 5))
    samples = []
    try:
        for dx, dy, tilt in [(0, 0, 0), (0.04, 0, 10), (-0.04, 0, 0), (0, 0.04, 10), (0, -0.04, 0)]:
            p = center + [dx, dy, 0.25]
            az = np.arctan2(p[1], p[0])
            R = grasp_rotation(tilted_approach(az, np.radians(tilt)), [-np.sin(az), np.cos(az), 0])
            arm.move_tcp(p, R)
            img = rig.grab([rig.wrist])[rig.wrist]
            seen = detect_markers(img)
            ids = [i for i in seen if i in world]
            if len(ids) < 4:
                print(f"  pose {len(samples)}: {len(ids)} markers visible, skipped")
                continue
            T_wc, rms = solve_extrinsics([world[i] for i in ids], [seen[i] for i in ids], K, dist)
            m, d = arm.sim.model, arm.sim.data
            b = m.body("end_link").id
            T_we = make_T(d.xmat[b].reshape(3, 3), d.xpos[b])
            samples.append(np.linalg.inv(T_we) @ T_wc)
            print(f"  pose {len(samples)}: {len(ids)} markers, RMS {rms:.2f} px")
    finally:
        arm.observe_pose()
        arm.close()
    if len(samples) < 2:
        sys.exit("not enough wrist views; check that the sheet is under the arm")
    T = average_transforms(samples)
    spread = max(np.linalg.norm(s[:3, 3] - T[:3, 3]) for s in samples)
    c["T_endlink_cam"] = T.tolist()
    print(f"wrist mount: {np.round(T[:3, 3], 4)} m from end_link, spread {spread * 1000:.1f} mm")
    _save(cal_path, cal)


def cmd_check(a):
    import cv2
    cfg, cal_path, cal = _load(a.config)
    ctx = _hardware(a.config)
    rig = ctx.world.rig
    world = {int(k): np.array(v) for k, v in cal.get("markers", {}).items()}
    out = HERE.parent / "runs" / "calibration_check"
    out.mkdir(parents=True, exist_ok=True)
    try:
        ctx.arm.observe_pose()
        imgs = rig.grab(rig.scene)
    finally:
        ctx.arm.close()
    for name in rig.scene:
        cam = rig.model(name)
        seen = detect_markers(imgs[name])
        img = cv2.cvtColor(imgs[name], cv2.COLOR_RGB2BGR)
        errs = []
        for i, p in world.items():
            uv = cv2.projectPoints(p.reshape(1, 3), cv2.Rodrigues(cam.R.T)[0], -cam.R.T @ cam.center, cam.K, cam.dist)[0].ravel()
            cv2.circle(img, tuple(int(v) for v in uv), 8, (0, 0, 255), 2)
            if i in seen:
                errs.append(np.linalg.norm(seen[i] - uv))
        cv2.imwrite(str(out / f"{name}.jpg"), img)
        print(f"{name}: mean marker error {np.mean(errs) if errs else float('nan'):.1f} px over {len(errs)} markers -> {out / (name + '.jpg')}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list-cameras")
    s = sub.add_parser("make-sheet")
    s.add_argument("--marker-mm", type=float, default=50)
    for name in ("intrinsics", "markers", "extrinsics", "wrist", "check"):
        s = sub.add_parser(name)
        s.add_argument("--config", default=str(HERE / "config" / "real.json"))
        if name == "intrinsics":
            s.add_argument("--camera", required=True)
            s.add_argument("--fov-deg", type=float, default=None, help="vertical FOV for a quick estimate")
            s.add_argument("--board", default="9x6", help="inner corners, cols x rows")
            s.add_argument("--square", type=float, default=0.025, help="square size [m]")
            s.add_argument("--views", type=int, default=15)
        if name == "markers":
            s.add_argument("--count", type=int, default=6)
    a = p.parse_args(argv)
    {"list-cameras": cmd_list_cameras, "make-sheet": cmd_make_sheet, "intrinsics": cmd_intrinsics,
     "markers": cmd_markers, "extrinsics": cmd_extrinsics, "wrist": cmd_wrist, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    main()
