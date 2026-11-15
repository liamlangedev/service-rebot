#!/usr/bin/env python3
"""Record LeRobot episodes of the reBot B601 teleoperated with the Leap (200 Hz MIT control).

Same flow as the PAROL6 record script:
    -> (Right)  start recording an episode, and again to save it
    <- (Left)   discard the episode being recorded
    Esc         finish and write the dataset
--resume appends to an existing dataset; --episodes is then the TOTAL to reach.
After every episode the arm returns to the ready pose by itself, then waits for the next ->.
Episodes are encoded while recording (streaming encoding), so saving is near-instant.
Other keys (global): S stop in place, G resume, H go to the ready pose.

  python record_episodes.py --port /dev/tty.usbmodem00000000050C1 \
    --repo-id RoboCrafty/rebot_sort_v1 --task "put the sock in the box" \
    --episodes 50 --fps 30 [--resume] --max-episode-s 30
"""
import argparse
import json
import shutil
import threading
import time
from dataclasses import fields
from pathlib import Path

import cv2
import numpy as np
from pynput import keyboard

from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.robots.rebot_b601_follower import RebotB601Follower, RebotB601FollowerRobotConfig
from lerobot.robots.rebot_b601_follower.motor_family import GripperControlMode
from lerobot.utils.constants import HF_LEROBOT_HOME
from lerobot.utils.feature_utils import build_dataset_frame, hw_to_dataset_features

from teleop import gripper_limits
from teleop.fast_loop import FastLoop
from teleop.lerobot_leap import LeapIK, LeapIKConfig
from teleop.mit_ff import MitFF, MitParams
from teleop.ready_move import move_to_ready


CAMERAS_FILE = Path(__file__).resolve().parent / "config" / "cameras.json"


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", required=True)
    p.add_argument("--repo-id", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--camera", action="append", default=[], metavar="NAME=INDEX",
                   help="override config/cameras.json, repeatable, e.g. --camera gripper=2 --camera front_wide=1")
    p.add_argument("--cameras-file", default=str(CAMERAS_FILE))
    p.add_argument("--cam-width", type=int, default=None, help="default: from the cameras file")
    p.add_argument("--cam-height", type=int, default=None)
    p.add_argument("--save-width", type=int, default=None, help="recorded image width (default: from the cameras file)")
    p.add_argument("--save-height", type=int, default=None)
    p.add_argument("--cam-fourcc", default=None, help="e.g. MJPG: compressed USB stream, much less bandwidth")
    p.add_argument("--episodes", type=int, default=50)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--max-episode-s", type=float, default=30.0)
    p.add_argument("--root", default=None, help="local dataset directory (default: lerobot cache)")
    p.add_argument("--resume", action="store_true", help="append to an existing dataset")
    p.add_argument("--push-to-hub", action="store_true", help="upload when finished")
    p.add_argument("--gripper-torque-ratio", type=float, default=0.03, help="force_pos gripper squeeze")
    p.add_argument("--park", choices=["ask", "yes", "no"], default="ask",
                   help="at exit: lower the arm to the folded rest pose and release torque (ask = wait for Enter)")
    p.add_argument("--yes", action="store_true", help="skip the Enter prompt before the first ready move")
    t = LeapIKConfig()
    p.add_argument("--teleop.scale", dest="t_scale", type=float, default=1.5)
    p.add_argument("--teleop.smoothing", dest="t_smoothing", type=float, default=t.smoothing)
    p.add_argument("--teleop.track_rotation", dest="t_rot", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--teleop.yaw_offset_deg", dest="t_yaw", type=float, default=t.yaw_offset_deg)
    p.add_argument("--teleop.max_joint_vel", dest="t_vel", type=float, default=t.max_joint_vel)
    p.add_argument("--teleop.max_wrist_vel", dest="t_wvel", type=float, default=t.max_wrist_vel)
    p.add_argument("--teleop.max_rot_vel", dest="t_rvel", type=float, default=t.max_rot_vel)
    p.add_argument("--teleop.gripper_vel", dest="t_gvel", type=float, default=2000.0)
    for f in fields(MitParams):
        d = getattr(MitParams(), f.name)
        p.add_argument(f"--mit.{f.name}", dest=f"mit_{f.name}", type=type(d), default=d)
    return p.parse_args()


class Keys:
    def __init__(self):
        self.toggle, self.discard, self.quit = threading.Event(), threading.Event(), threading.Event()
        keyboard.Listener(on_press=self._on_press).start()

    def _on_press(self, key):
        if key == keyboard.Key.right:
            self.toggle.set()
        elif key == keyboard.Key.left:
            self.discard.set()
        elif key == keyboard.Key.esc:
            self.quit.set()

    def clear(self):
        self.toggle.clear()
        self.discard.clear()


def _retrying(connect, cam, attempts: int = 4):
    def wrapper(*a, **kw):
        for i in range(1, attempts + 1):
            try:
                return connect(*a, **kw)
            except (TimeoutError, ConnectionError) as e:
                print(f"[camera] {cam} failed to start (attempt {i}/{attempts}): {e}")
                if i == attempts:
                    raise
                time.sleep(1.5)
    return wrapper


def main():
    args = parse_args()
    limits = gripper_limits.load()
    if limits is None:
        raise SystemExit(f"Gripper range not measured. Run: python tools/measure_gripper.py --port {args.port}")
    g_lo, g_hi = gripper_limits.bounds(limits)
    params = MitParams(**{f.name: getattr(args, f"mit_{f.name}") for f in fields(MitParams)})

    cam_file = json.loads(Path(args.cameras_file).read_text())
    specs = dict(cam_file["cameras"])
    for spec in args.camera:
        name, _, idx = spec.partition("=")
        specs[name] = int(idx) if idx.isdigit() else idx
    width, height = args.cam_width or cam_file["width"], args.cam_height or cam_file["height"]
    fourcc = args.cam_fourcc or cam_file.get("fourcc")
    cameras = {name: OpenCVCameraConfig(index_or_path=idx, width=width, height=height, fps=args.fps,
                                        warmup_s=3, fourcc=fourcc)
               for name, idx in specs.items()}
    save_w, save_h = args.save_width or cam_file.get("save_width", width), args.save_height or cam_file.get("save_height", height)
    print("cameras:", {n: c.index_or_path for n, c in cameras.items()}, f"capture {width}x{height}@{args.fps} -> saved {save_w}x{save_h}")
    cfg = RebotB601FollowerRobotConfig(
        port=args.port, cameras=cameras, disable_torque_on_disconnect=False,
        gripper_torque_ratio=args.gripper_torque_ratio)
    cfg.joint_limits["gripper"] = (g_lo, g_hi)  # lerobot's default (-270..0) is wrong for this arm
    if params.grip_mode == "mit":
        cfg.gripper_control_mode = GripperControlMode.MIT
    else:
        cfg.gripper_control_mode = GripperControlMode.FORCE_POS
    robot = RebotB601Follower(cfg)
    for cam in robot.cameras.values():
        cam.connect = _retrying(cam.connect, cam)  # a camera that times out at startup is retried
    teleop = LeapIK(LeapIKConfig(
        scale=args.t_scale, smoothing=args.t_smoothing, track_rotation=args.t_rot, yaw_offset_deg=args.t_yaw,
        max_joint_vel=args.t_vel, max_wrist_vel=args.t_wvel, max_rot_vel=args.t_rvel, gripper_vel=args.t_gvel))

    features = {
        **hw_to_dataset_features(robot.action_features, "action"),
        **hw_to_dataset_features(robot.observation_features, "observation"),
    }
    for key, ft in features.items():
        if key.startswith("observation.images.") and ft["dtype"] in ("video", "image"):
            ft["shape"] = (save_h, save_w, ft["shape"][2])
    n_cams = len(cameras)
    root = Path(args.root) if args.root else HF_LEROBOT_HOME / args.repo_id
    exists = (root / "meta" / "info.json").exists()
    has_data = exists and any((root / "data").glob("**/*.parquet"))
    if exists and not has_data:
        shutil.rmtree(root)  # leftover of a run that saved nothing
        exists = False
    if exists and not args.resume:
        raise SystemExit(f"{root} already holds a dataset. Add --resume to append to it, or use a new --repo-id.")
    if args.resume and not exists:
        print("No existing dataset, creating a new one.")
        args.resume = False
    if args.resume:
        dataset = LeRobotDataset.resume(
            args.repo_id, root=root,
            image_writer_threads=4 * n_cams, streaming_encoding=True)
        if dataset.fps != args.fps or any(k not in dataset.features for k in features):
            raise SystemExit("Existing dataset has different features/fps; use a new --repo-id.")
        print(f"Resuming {args.repo_id}: {dataset.meta.total_episodes} episodes already recorded")
    else:
        dataset = LeRobotDataset.create(
            args.repo_id, args.fps, root=args.root, robot_type=getattr(robot, "robot_type", robot.name),
            features=features, use_videos=True, image_writer_threads=4 * n_cams,
            streaming_encoding=True)  # encode while recording so save_episode() is near-instant

    keys = Keys()
    robot.connect()
    mit = MitFF(robot, params)
    loop = FastLoop(robot, rate=200.0, mit=mit)
    base = dataset.meta.total_episodes if args.resume else 0
    saved = 0
    try:
        if not loop.gravity_check():
            raise SystemExit("gravity feed-forward check failed")
        if not move_to_ready(robot, speed=params.ready_speed, confirm=not args.yes):
            raise SystemExit("arm did not reach the ready pose")
        teleop.connect()
        loop.start(teleop.step)  # the 200 Hz thread drives the arm from now on

        def go_home():
            loop.return_to_ready()
            t0 = time.time()
            time.sleep(0.2)
            while loop._mode == "returning" and time.time() - t0 < 20.0:
                time.sleep(0.05)

        while base + saved < args.episodes and not keys.quit.is_set():
            keys.clear()
            print(f"\n[{base + saved}/{args.episodes}] Ready. Press -> to start recording (Esc to finish).")
            while not keys.toggle.is_set() and not keys.quit.is_set():
                time.sleep(0.02)
            if keys.quit.is_set():
                break
            keys.clear()

            print("  recording...  -> save | <- discard")
            period = 1.0 / args.fps
            t_end = time.perf_counter() + args.max_episode_s
            next_tick = time.perf_counter()
            n, first, moved = 0, None, False
            while not (keys.toggle.is_set() or keys.discard.is_set() or keys.quit.is_set()):
                if time.perf_counter() > t_end:
                    print("  max episode length reached")
                    break
                obs = robot.get_observation()
                for cam_key in cameras:
                    img = obs[cam_key]
                    if img.shape[:2] != (save_h, save_w):
                        obs[cam_key] = cv2.resize(img, (save_w, save_h), interpolation=cv2.INTER_AREA)
                action = loop.latest_action()
                if action is None:
                    continue
                action = dict(action)
                action["gripper.pos"] = float(np.clip(action["gripper.pos"], g_lo, g_hi))
                state = [obs[k] for k in robot.action_features]
                first = state if first is None else first
                moved = moved or max(abs(a - b) for a, b in zip(state, first)) > 0.5
                dataset.add_frame({
                    **build_dataset_frame(dataset.features, obs, "observation"),
                    **build_dataset_frame(dataset.features, action, "action"),
                    "task": args.task,
                })
                n += 1
                next_tick += period
                sleep = next_tick - time.perf_counter()
                if sleep > 0:
                    time.sleep(sleep)
                else:
                    next_tick = time.perf_counter()

            if keys.discard.is_set() or keys.quit.is_set() or n == 0:
                dataset.clear_episode_buffer()
                print("  discarded")
            elif not moved:
                dataset.clear_episode_buffer()
                print("  DISCARDED: joints never moved (is the clutch engaged?)")
            else:
                print(f"  saving {n} frames ({n / args.fps:.1f}s)...")
                t_save = time.perf_counter()
                dataset.save_episode()
                print(f"  saved in {time.perf_counter() - t_save:.1f} s")
                saved += 1

            if not keys.quit.is_set():
                print("  returning to ready")
                t_home = time.perf_counter()
                go_home()
                print(f"  back at ready in {time.perf_counter() - t_home:.1f} s")
    finally:
        # The control thread keeps holding the arm while the (slow) dataset finalization runs.
        print(f"\nFinalizing dataset with {saved} new episodes -> {dataset.root}")
        try:
            dataset.finalize()
            if args.push_to_hub and saved:
                dataset.push_to_hub()
        except Exception as e:
            print(f"dataset finalize failed: {e!r}")
        teleop.disconnect()
        park = args.park == "yes"
        if args.park == "ask":
            try:
                input("\nThe arm is being held. Clear the path to the folded rest pose, then press Enter to lower it "
                      "and release torque (Ctrl-C: exit now, the arm will go limp)... ")
                park = True
            except (KeyboardInterrupt, EOFError):
                print("\nexiting without parking")
        if park:
            loop.park_and_release()
        robot.disconnect()  # patched by FastLoop: stops the thread, saves the log


if __name__ == "__main__":
    main()
