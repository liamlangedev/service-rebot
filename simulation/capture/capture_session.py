"""Guided capture session on the real setup.

  cd simulation
  uv run --project ../teleoperation python -m capture.capture_session --name s1
  uv run --project ../teleoperation python -m capture.capture_session --name test --fake --pause 5 --yes

What it does (the arm holds every pose with torque on, commands streamed at 50 Hz):
  1. moves the arm to the ready pose (gripper down) and captures a full-res frame
     from every camera plus the measured joint angles
  2. PAUSE (default 3 min) for your phone video / photos of the scene (Gaussian
     splat capture). The arm holds still. Enter ends the pause early.
  3. captures again (checks that nothing moved), then visits a few more poses
     and captures at each
  4. compares every frame with the sim at the measured joints (compare/*.jpg:
     real | sim | real with the sim robot's outline) and, if the ChArUco board
     lies on the table (`charuco` in real_setup.json), solves:
       - each fixed camera's pose (from the board)
       - the wrist camera's mount on the gripper (board + arm kinematics)
       - consistency: spread across captures (moved camera / joint errors)
     --write puts the fitted cameras into real_setup.json (old one backed up).

Output: captures/<name>/ (session.json, frames/, compare/, phone/ for your media).
Prerequisites: capture/devices.json from the device UI; the arm's follower.json
calibration and teleoperation/config/gripper_limits.json (as for teleop).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import threading
import time
from pathlib import Path

import cv2
import mujoco
import numpy as np

from capture.calib import (CV_TO_MJ, fixed_camera_entry, fovy_from_K, load_intrinsics,
                           mean_rotation, rot_angle_deg, wrist_camera_entry)
from capture.devices import (DEVICES_FILE, FULL_RES, ROLES, SIM_DIR, SimCameraHub,
                             load_devices, open_streams, resolve)
from rebot_sim import DEFAULT_CONFIG, RealSetupEnv, load_config
from rebot_sim.charuco import BoardSpec, detect, draw, solve_pose

from teleop import gripper_limits  # noqa: E402  (path set by rebot_sim)
from teleop.rebot_model import GRIPPER_MAX  # noqa: E402
from teleop.rebot_real import (JOINT_NAMES, READY_QPOS, joint_space_path, obs_to_q,  # noqa: E402
                               q_to_action)

REPO_ROOT = SIM_DIR.parent
# Extra poses, relative to the ready pose (rad): small moves that keep the
# gripper over the table in front of the robot, where the board lies.
POSES = {
    "ready": np.zeros(6),
    "pan_left": np.array([0.25, 0, 0, 0, 0, 0]),
    "pan_right": np.array([-0.25, 0, 0, 0, 0, 0]),
    "reach": np.array([0, 0.15, 0.10, -0.12, 0, 0]),
    "roll": np.array([0, 0, 0, 0, 0, 0.5]),
}

PHONE_GUIDE = """
  PHONE CAPTURE for the Gaussian splat (the arm holds still; Enter ends early)
  - Take the can/cup off the table. Leave the ChArUco board where it is.
  - Lock exposure and focus (long-press on the phone screen). Landscape, 4K or 1080p.
  - Video: walk slowly around the open side in 3 loops: high (looking down from
    ~60 cm), mid (~30 cm), low (table level). Then close-ups of the table under the
    gripper and inside both bin compartments. Move slowly (no motion blur).
    Or ~200 photos with lots of overlap.
  - Don't touch the cameras, the board or the bin.
  - Afterwards, copy the files into  {phone_dir}
"""


# ----------------------------------------------------------------- arm
class Arm:
    """Streams hold commands at `rate` Hz so the motors stay stiff; moves are
    joint-space trajectories fed through the same stream."""

    def __init__(self, robot, open_deg: float, rate: float = 50.0):
        self.robot, self.rate, self.grip = robot, rate, open_deg
        obs = robot.get_observation()
        self._action = q_to_action(obs_to_q(obs), open_deg)
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while not self._stop.is_set():
            with self._lock:
                action = dict(self._action)
            try:
                self.robot.send_action(action)
            except Exception as exc:  # noqa: BLE001
                print(f"\n[arm] send failed: {exc}")
            time.sleep(1.0 / self.rate)

    def measured(self, n: int = 5):
        qs, gs = [], []
        for _ in range(n):
            obs = self.robot.get_observation()
            qs.append(obs_to_q(obs))
            gs.append(obs["gripper.pos"])
            time.sleep(0.02)
        return np.mean(qs, axis=0), float(np.mean(gs))

    def move_to(self, q_target: np.ndarray, speed: float = 0.5, settle: float = 1.5) -> float:
        q0, _ = self.measured(1)
        for q in joint_space_path(q0, q_target, speed, self.rate):
            with self._lock:
                self._action = q_to_action(q, self.grip)
            time.sleep(1.0 / self.rate)
        time.sleep(settle)
        q, _ = self.measured()
        return float(np.degrees(np.max(np.abs(q - q_target))))

    def close(self):
        self._stop.set()
        self._thread.join(timeout=1.0)
        self.robot.disconnect()


def connect_arm(args, devices):
    from lerobot.robots.rebot_b601_follower import RebotB601FollowerRobotConfig
    limits = gripper_limits.load()
    if limits is None and not args.fake:
        sys.exit("gripper range not measured: run teleoperation/tools/measure_gripper.py first")
    limits = limits or (-270.0, 0.0)
    lo, hi = gripper_limits.bounds(limits)
    calib_dir = Path(args.calibration_dir)
    port = args.port or (resolve(devices["arm"]) if devices and devices.get("arm") else None)
    if not args.fake:
        if not port:
            sys.exit("no arm port: pick it in the device UI or pass --port")
        if not (calib_dir / f"{args.robot_id}.json").exists():
            sys.exit(f"{calib_dir / (args.robot_id + '.json')} missing: not connecting "
                     "(lerobot would start re-zeroing the motors)")
    config = RebotB601FollowerRobotConfig(
        port=port or "fake", id=args.robot_id, calibration_dir=calib_dir,
        joint_limits={"gripper": (lo, hi)}, max_relative_target=args.max_step_deg,
        control_mode="pos_vel", pos_vel_velocity=60.0, disable_torque_on_disconnect=False)
    if args.fake:
        from teleop.fake_rebot import FakeRebotFollower
        robot = FakeRebotFollower(config, limits)
    else:
        from lerobot.robots.rebot_b601_follower import RebotB601Follower
        robot = RebotB601Follower(config)
    robot.connect(calibrate=False)
    open_deg = limits[0]  # (open_deg, closed_deg)
    return Arm(robot, open_deg), limits


# ----------------------------------------------------------------- session
class Session:
    def __init__(self, args):
        self.args = args
        self.out = SIM_DIR / "captures" / args.name
        if self.out.exists() and not args.overwrite:
            sys.exit(f"{self.out} exists (use another --name or --overwrite)")
        for d in ("frames", "compare", "phone"):
            (self.out / d).mkdir(parents=True, exist_ok=True)
        self.cfg = load_config()
        self.board = BoardSpec.from_config(self.cfg.get("charuco"))
        self.board_on_table = bool((self.cfg.get("charuco") or {}).get("enabled")
                                   and self.board.near_left)
        self.captures = []
        self.hub = None
        if args.fake:  # sim cameras showing the board, rendered at the measured joints
            fcfg = json.loads(json.dumps(self.cfg))
            fcfg["charuco"] = {**(fcfg.get("charuco") or {}), "enabled": True,
                               "near_left": self.board.near_left or [0.48, 0.175]}
            if not self.board_on_table:
                self.cfg, self.board, self.board_on_table = fcfg, BoardSpec.from_config(
                    fcfg["charuco"]), True
            self.cam_env = RealSetupEnv(fcfg, objects=False)
            self.cam_env.hide_markers()
            self.hub = SimCameraHub(self.cam_env, ROLES)
            self.streams = {r: self.hub.stream(r) for r in ROLES}
            self.devices = {"cameras": {r: {"key": f"sim:{r}"} for r in ROLES}, "arm": None}
        else:
            self.devices = load_devices()
            if not self.devices:
                sys.exit(f"{DEVICES_FILE} missing: run the device UI first "
                         "(python -m capture.device_ui)")
            self.streams = open_streams(self.devices)
        # The sim the frames are compared with (the calibrated model, board drawn if used).
        self.env = RealSetupEnv(self.cfg, objects=False)
        self.env.hide_markers()
        self.robot_geoms = _robot_geoms(self.env.model)
        self.renderer = mujoco.Renderer(self.env.model, height=FULL_RES[1], width=FULL_RES[0])
        self.arm = None

    # -- capture -------------------------------------------------------
    def capture(self, tag: str):
        if self.arm is not None:
            q, grip = self.arm.measured()
        else:
            q, grip = None, None
        finger = GRIPPER_MAX if grip is None else _deg_to_finger(grip, self.limits)
        if self.hub is not None and q is not None:
            with self.hub.lock:
                self.cam_env.mirror(q, finger)
        t0 = time.time()
        frames = {}
        for role, s in self.streams.items():
            frames[role] = s.read(fresh_after=t0 + 0.05)
        (self.out / "frames" / tag).mkdir(exist_ok=True)
        if q is not None:
            self.env.mirror(q, finger)
        rec = {"tag": tag, "time": time.strftime("%H:%M:%S"),
               "joints_deg": None if q is None else dict(zip(JOINT_NAMES, np.degrees(q).round(3).tolist())),
               "gripper_deg": grip, "cameras": {}}
        panels = []
        for role, img in frames.items():
            cv2.imwrite(str(self.out / "frames" / tag / f"{role}.png"), img)
            det = detect(self.board, img) if self.board_on_table else None
            if det is not None and not det.spans_2d(self.board):
                det = None  # e.g. a single row of corners: no usable pose
            sim, mask = self._render(role, img.shape[1], img.shape[0])
            panels.append(_panel(role, img, sim, mask, det))
            rec["cameras"][role] = {"file": f"frames/{tag}/{role}.png",
                                    "size": [img.shape[1], img.shape[0]],
                                    "board_corners": 0 if det is None else len(det)}
            if det is not None:
                rec["cameras"][role]["_det"] = det
                if role == "wrist":
                    ee = self.env.data.body("end_link")
                    rec["cameras"][role]["_ee"] = (ee.xmat.reshape(3, 3).copy(), ee.xpos.copy())
        cv2.imwrite(str(self.out / "compare" / f"{tag}.jpg"), np.vstack(panels),
                    [cv2.IMWRITE_JPEG_QUALITY, 85])
        self.captures.append(rec)
        corners = ", ".join(f"{r} {c['board_corners']}" for r, c in rec["cameras"].items())
        print(f"[capture] {tag}: saved {len(frames)} frames"
              + (f" (board corners: {corners})" if self.board_on_table else ""))

    def _render(self, role, w, h):
        cam = role
        self.renderer.update_scene(self.env.data, camera=cam)
        rgb = self.renderer.render()
        self.renderer.enable_segmentation_rendering()
        self.renderer.update_scene(self.env.data, camera=cam)
        seg = self.renderer.render()
        self.renderer.disable_segmentation_rendering()
        mask = (seg[..., 1] == mujoco.mjtObj.mjOBJ_GEOM) & np.isin(seg[..., 0], self.robot_geoms)
        sim = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        if (w, h) != FULL_RES:
            sim = cv2.resize(sim, (w, h))
            mask = cv2.resize(mask.astype(np.uint8), (w, h), interpolation=cv2.INTER_NEAREST) > 0
        return sim, mask

    # -- pause ---------------------------------------------------------
    def pause(self, seconds: float):
        print(PHONE_GUIDE.format(phone_dir=self.out / "phone"))
        done = threading.Event()

        def wait_enter():
            try:
                input()
            except EOFError:
                return
            done.set()
        threading.Thread(target=wait_enter, daemon=True).start()
        t_end = time.time() + seconds
        while not done.is_set() and time.time() < t_end:
            left = int(t_end - time.time())
            print(f"\r  >>> capture time left: {left // 60}:{left % 60:02d}  (Enter = done) ",
                  end="", flush=True)
            done.wait(1.0)
        print("\n  pause over")

    # -- analysis ------------------------------------------------------
    def analyse(self):
        result = {"fixed_cameras": {}, "wrist_camera": None}
        if not self.board_on_table:
            print("[calib] no ChArUco board on the table (charuco.enabled/near_left in "
                  "real_setup.json): only the visual comparisons were made")
            return result
        ws = self.env.ws
        for role in [r for r in ROLES if r != "wrist" and r in self.streams]:
            poses = []
            for rec in self.captures:
                c = rec["cameras"].get(role, {})
                if "_det" not in c:
                    continue
                det = c["_det"]
                K, dist, src = load_intrinsics(role, tuple(c["size"]),
                                               self.env.model.cam_fovy[self.env.model.camera(role).id])
                world = np.array([ws.world(*p) for p in self.board.to_workspace(det.obj)])
                try:
                    R_cv, C, rms = solve_pose(det, world, K, dist)
                except Exception as exc:  # noqa: BLE001
                    print(f"[calib] {role} {rec['tag']}: pose solve failed ({exc})")
                    continue
                poses.append((R_cv @ CV_TO_MJ, C, rms, rec["tag"]))
            if not poses:
                print(f"[calib] {role}: board not seen")
                continue
            R = mean_rotation([p[0] for p in poses])
            C = np.mean([p[1] for p in poses], axis=0)
            spread_mm = max(np.linalg.norm(p[1] - C) for p in poses) * 1000
            spread_deg = max(rot_angle_deg(p[0], R) for p in poses)
            fovy = fovy_from_K(K, tuple(c["size"]))
            old = self.env.data.cam(role)
            moved_mm = np.linalg.norm(C - old.xpos) * 1000
            turned = rot_angle_deg(R, old.xmat.reshape(3, 3))
            entry = fixed_camera_entry(ws, R, C, fovy)
            result["fixed_cameras"][role] = {
                "entry": entry, "intrinsics": src, "captures": len(poses),
                "rms_px": round(float(np.mean([p[2] for p in poses])), 2),
                "spread_mm": round(spread_mm, 1), "spread_deg": round(spread_deg, 2),
                "vs_sim_mm": round(moved_mm, 1), "vs_sim_deg": round(turned, 2)}
            print(f"[calib] {role}: board fit {result['fixed_cameras'][role]['rms_px']} px "
                  f"({src}); vs current sim {moved_mm:.0f} mm / {turned:.1f} deg; "
                  f"spread over {len(poses)} captures {spread_mm:.1f} mm / {spread_deg:.2f} deg")
            if spread_mm > 5 or spread_deg > 0.5:
                print(f"         WARNING: {role} or the board moved during the session")
        # Wrist camera: T_ee_cam = T_world_ee^-1 * T_world_cam, per capture.
        samples = []
        for rec in self.captures:
            c = rec["cameras"].get("wrist", {})
            if "_det" not in c:
                continue
            det = c["_det"]
            K, dist, src = load_intrinsics("wrist", tuple(c["size"]),
                                           self.env.model.cam_fovy[self.env.model.camera("wrist").id])
            world = np.array([ws.world(*p) for p in self.board.to_workspace(det.obj)])
            try:
                R_cv, C, rms = solve_pose(det, world, K, dist)
            except Exception as exc:  # noqa: BLE001
                print(f"[calib] wrist {rec['tag']}: pose solve failed ({exc})")
                continue
            R_ee, p_ee = c["_ee"]
            samples.append((R_ee.T @ (R_cv @ CV_TO_MJ), R_ee.T @ (C - p_ee), rms, rec["tag"]))
        if samples:
            R = mean_rotation([s[0] for s in samples])
            t = np.mean([s[1] for s in samples], axis=0)
            spread_mm = max(np.linalg.norm(s[1] - t) for s in samples) * 1000
            spread_deg = max(rot_angle_deg(s[0], R) for s in samples)
            entry = wrist_camera_entry(R, t, fovy_from_K(K, tuple(c["size"])))
            result["wrist_camera"] = {"entry": entry, "intrinsics": src, "captures": len(samples),
                                      "rms_px": round(float(np.mean([s[2] for s in samples])), 2),
                                      "spread_mm": round(spread_mm, 1),
                                      "spread_deg": round(spread_deg, 2)}
            print(f"[calib] wrist: mount {np.round(t * 1000, 1)} mm in end_link, "
                  f"{len(samples)} poses agree within {spread_mm:.1f} mm / {spread_deg:.2f} deg")
            if spread_mm > 8 or spread_deg > 1.5:
                print("         WARNING: wrist poses disagree. The sim's joint angles/zeros or "
                      "link lengths likely differ from the real arm (check compare/*.jpg).")
        else:
            print("[calib] wrist: board not seen in any pose")
        return result

    def write_config(self, result):
        path = Path(DEFAULT_CONFIG)
        cfg = json.loads(path.read_text())
        shutil.copy(path, self.out / "real_setup.before.json")
        for cam in cfg["cameras"]:
            r = result["fixed_cameras"].get(cam["name"])
            if r:
                cam.update(r["entry"])
                cam.pop("fov_diagonal_deg", None)
                cam["_calibrated"] = f"ChArUco board, capture session {self.args.name}"
        if result["wrist_camera"]:
            cfg["wrist_camera"].pop("fov_diagonal_deg", None)
            cfg["wrist_camera"].update(result["wrist_camera"]["entry"])
            cfg["wrist_camera"]["_calibrated"] = f"ChArUco hand-eye, capture session {self.args.name}"
        path.write_text(json.dumps(cfg, indent=2) + "\n")
        print(f"[calib] updated {path} (previous version: {self.out / 'real_setup.before.json'})")

    def save(self, result, extra):
        clean = []
        for rec in self.captures:
            r = json.loads(json.dumps({k: v for k, v in rec.items() if k != "cameras"}))
            r["cameras"] = {role: {k: v for k, v in c.items() if not k.startswith("_")}
                            for role, c in rec["cameras"].items()}
            clean.append(r)
        board = None
        if self.board_on_table:
            board = {k: getattr(self.board, k) for k in
                     ("squares_x", "squares_y", "square", "marker", "dictionary", "near_left")}
        data = {"name": self.args.name, "fake": self.args.fake, "devices": self.devices,
                "scene_version": self.cfg.get("version"), "board": board,
                "captures": clean, "calibration": result, **extra}
        (self.out / "session.json").write_text(json.dumps(data, indent=2, default=_json) + "\n")
        print(f"[session] {self.out / 'session.json'}")

    def close(self):
        for s in self.streams.values():
            s.close()
        if self.hub:
            self.hub.close()
        self.renderer.close()


# ----------------------------------------------------------------- helpers
def _robot_geoms(model) -> np.ndarray:
    root = model.body("base_link").id
    ids = []
    for g in range(model.ngeom):
        b = model.geom_bodyid[g]
        while b not in (0, root):
            b = model.body_parentid[b]
        if b == root:
            ids.append(g)
    return np.array(ids)


def _deg_to_finger(deg, limits):
    open_deg, closed_deg = limits
    closing = (deg - open_deg) / (closed_deg - open_deg)
    return GRIPPER_MAX * (1.0 - float(np.clip(closing, 0.0, 1.0)))


def _panel(role, real, sim, mask, det, width=640):
    h = int(width * real.shape[0] / real.shape[1])
    a = cv2.resize(draw(real, det), (width, h))
    b = cv2.resize(sim, (width, h))
    c = a.copy()
    m = cv2.resize(mask.astype(np.uint8), (width, h), interpolation=cv2.INTER_NEAREST)
    contours, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(c, contours, -1, (0, 255, 0), 2)
    for im, label in ((a, f"real {role}"), (b, "sim"), (c, "real + sim robot outline")):
        cv2.putText(im, label, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    return np.hstack([a, b, c])


def _json(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    return str(o)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name", default=time.strftime("session_%Y%m%d_%H%M%S"))
    p.add_argument("--pause", type=float, default=180, help="phone capture pause [s]")
    p.add_argument("--poses", default="pan_left,pan_right,reach,roll",
                   help=f"extra poses after the pause, from {list(POSES)} ('' = none)")
    p.add_argument("--speed", type=float, default=0.4, help="arm joint speed [rad/s]")
    p.add_argument("--write", action="store_true", help="update real_setup.json from the board")
    p.add_argument("--no-arm", action="store_true", help="cameras only")
    p.add_argument("--fake", action="store_true", help="simulated cameras and arm")
    p.add_argument("--yes", action="store_true", help="don't ask before moving the arm")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--port", default=None, help="arm port (default: from devices.json)")
    p.add_argument("--robot-id", default="follower")
    p.add_argument("--calibration-dir", default=str(REPO_ROOT))
    p.add_argument("--max-step-deg", type=float, default=5.0)
    args = p.parse_args()
    poses = [s for s in args.poses.split(",") if s]
    for s in poses:
        if s not in POSES:
            sys.exit(f"unknown pose {s}; choose from {list(POSES)}")

    sess = Session(args)
    sess.limits = gripper_limits.load() or (-270.0, 0.0)
    extra = {}
    try:
        if not args.no_arm:
            print("=" * 72 + "\n ARM: torque stays on and it moves between poses. Clear the "
                  "table,\n keep a hand near the power switch.\n" + "=" * 72)
            sess.arm, sess.limits = connect_arm(args, sess.devices)
            if not args.yes:
                input("Enter to move to the ready pose... ")
            err = sess.arm.move_to(READY_QPOS, args.speed)
            print(f"[arm] ready pose reached (max error {err:.1f} deg)")
        sess.capture("ready")
        if args.pause > 0:
            sess.pause(args.pause)
            sess.capture("after_pause")
        if sess.arm is not None:
            for name in poses:
                err = sess.arm.move_to(READY_QPOS + POSES[name], args.speed)
                print(f"[arm] {name} (max error {err:.1f} deg)")
                sess.capture(name)
            sess.arm.move_to(READY_QPOS, args.speed)
        result = sess.analyse()
        if args.write and (result["fixed_cameras"] or result["wrist_camera"]):
            sess.write_config(result)
        sess.save(result, extra)
        phone = list((sess.out / "phone").iterdir())
        print(f"\nDone. Compare images: {sess.out / 'compare'}")
        print(f"Phone media in {sess.out / 'phone'}: {len(phone)} file(s)"
              + ("" if phone else " (copy your video/photos there, then run "
                 "python -m capture.prepare_splat_dataset " + args.name + ")"))
    finally:
        if sess.arm is not None:
            if not args.yes and not args.fake:
                try:
                    input("\nSupport the arm, then Enter to release it (motors may go limp)... ")
                except EOFError:
                    pass
            sess.arm.close()
        sess.close()


if __name__ == "__main__":
    main()
