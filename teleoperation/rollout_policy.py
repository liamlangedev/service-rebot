#!/usr/bin/env python3
"""Run a trained LeRobot policy (ACT, SmolVLA, ...) on the real reBot B601 through the 200 Hz MIT loop.

The policy runs at --fps (the dataset fps, 30) and produces joint-position targets. The 200 Hz control thread
interpolates between them and drives the motors with the same gains and feed-forward used while recording,
so the arm behaves like it did under teleoperation. No Leap is needed.

  # 1. check the model on this machine, no robot, no motion
  python rollout_policy.py --policy niru-5/act_rebot_sort_v1 --dry-run

  # 2. run it
  python rollout_policy.py --port /dev/tty.usbmodem00000000050C1 --policy niru-5/act_rebot_sort_v1 \
      --task "pickup the keys and put it in the designated bin" --duration 30

Keys: Right = start the run / stop it early, Esc = quit, S = stop in place, G = resume, H = go to ready.
Each run starts from the ready pose and returns to it afterwards.
"""
import argparse
import json
import threading
import time
from dataclasses import fields
from pathlib import Path

import cv2
import numpy as np
import torch
from pynput import keyboard

from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.configs.policies import PreTrainedConfig
from lerobot.policies.factory import get_policy_class, make_pre_post_processors
from lerobot.policies.utils import build_inference_frame, make_robot_action
from lerobot.robots.rebot_b601_follower import RebotB601Follower, RebotB601FollowerRobotConfig
from lerobot.robots.rebot_b601_follower.motor_family import MOTOR_PROFILES, GripperControlMode, MotorFamily
from lerobot.utils.feature_utils import hw_to_dataset_features

from record_episodes import CAMERAS_FILE, _retrying
from teleop import gripper_limits
from teleop.fast_loop import FastLoop
from teleop.mit_ff import MitFF, MitParams
from teleop.ready_move import move_to_ready
from teleop.rebot_real import JOINT_NAMES, READY_QPOS, q_to_action

# Gains used while recording the dataset (see REAL_ARM.md); the policy must see the same dynamics.
RECORDING_MIT = dict(kp_scale=3.0, kd_scale=3.0, wrist_scale=0.4, friction_scale=1.3)
ALL_NAMES = [*JOINT_NAMES, "gripper"]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--policy", required=True,
                   help="Hub repo or local folder, e.g. niru-5/act_rebot_sort_v1. For an intermediate checkpoint use "
                        "--subfolder checkpoints/010500/pretrained_model")
    p.add_argument("--subfolder", default=None)
    p.add_argument("--port", default=None, help="arm serial port (not needed with --dry-run)")
    p.add_argument("--task", default="pickup the keys and put it in the designated bin",
                   help="language prompt; used by SmolVLA/VLAs, ignored by ACT. Use the exact training wording")
    p.add_argument("--device", default="auto", help="auto (cuda > mps > cpu), cuda, mps or cpu")
    p.add_argument("--dtype", choices=["float32", "bfloat16"], default=None,
                   help="override the policy dtype (pi0/pi0.5: bfloat16 is faster on MPS/CUDA)")
    p.add_argument("--num-inference-steps", type=int, default=None,
                   help="flow-matching denoising steps (pi0/pi0.5 default 10); fewer = faster, slightly less precise")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--duration", type=float, default=30.0, help="seconds per run")
    p.add_argument("--runs", type=int, default=0, help="stop after this many runs (0 = until Esc)")
    p.add_argument("--n-action-steps", type=int, default=None,
                   help="actions executed per policy call (default: the model's chunk, ACT 100 / SmolVLA 50). "
                        "Smaller = more reactive, more inference calls")
    p.add_argument("--max-step-deg", type=float, default=4.0,
                   help="largest change of any joint target per policy step (deg); 4 deg x 30 Hz = 120 deg/s")
    p.add_argument("--max-gripper-step-deg", type=float, default=40.0)
    p.add_argument("--cameras-file", default=str(CAMERAS_FILE))
    p.add_argument("--cam-width", type=int, default=None,
                   help="image width fed to the policy; must match training (default: save_width of cameras.json)")
    p.add_argument("--cam-height", type=int, default=None,
                   help="image height fed to the policy (default: save_height of cameras.json)")
    p.add_argument("--capture-width", type=int, default=None, help="camera capture width (default: width of cameras.json)")
    p.add_argument("--capture-height", type=int, default=None, help="camera capture height (default: height of cameras.json)")
    p.add_argument("--gripper-torque-ratio", type=float, default=0.03)
    p.add_argument("--park", choices=["ask", "yes", "no"], default="ask")
    p.add_argument("--yes", action="store_true", help="skip the Enter prompt before the first ready move")
    p.add_argument("--dry-run", action="store_true", help="load the policy and run it on a fake observation; no robot")
    for f in fields(MitParams):
        d = RECORDING_MIT.get(f.name, getattr(MitParams(), f.name))
        p.add_argument(f"--mit.{f.name}", dest=f"mit_{f.name}", type=type(d), default=d)
    return p.parse_args()


def pick_device(name: str) -> str:
    if name != "auto":
        return name
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_policy(args, device: str):
    """Returns (policy, preprocessor, postprocessor). The processors restore the exact normalization and
    camera renaming saved with the checkpoint."""
    kw = {"subfolder": args.subfolder} if args.subfolder else {}
    cfg = PreTrainedConfig.from_pretrained(args.policy, **kw)
    cfg.pretrained_path = args.policy if not args.subfolder else str(Path(args.policy) / args.subfolder)
    cfg.device = device
    if args.subfolder and not Path(args.policy).exists():
        from huggingface_hub import snapshot_download
        local = snapshot_download(args.policy, allow_patterns=[f"{args.subfolder}/*"])
        cfg.pretrained_path = str(Path(local) / args.subfolder)
        cfg = PreTrainedConfig.from_pretrained(cfg.pretrained_path)
        cfg.pretrained_path, cfg.device = Path(local) / args.subfolder, device
    cls = get_policy_class(cfg.type)
    if args.dtype and hasattr(cfg, "dtype"):
        cfg.dtype = getattr(torch, args.dtype)
    if args.num_inference_steps and hasattr(cfg, "num_inference_steps"):
        cfg.num_inference_steps = args.num_inference_steps
    # The policy's __init__ randomly initialises billions of weights on the CPU (~100 s for pi0/pi0.5) and
    # from_pretrained then overwrites them; building directly on the target device takes seconds.
    with torch.device(device):
        policy = cls.from_pretrained(cfg.pretrained_path, config=cfg)
    policy.to(device)
    policy.eval()
    if args.n_action_steps:
        if args.n_action_steps > cfg.chunk_size:
            raise SystemExit(f"--n-action-steps {args.n_action_steps} exceeds the model's chunk size {cfg.chunk_size}")
        policy.config.n_action_steps = args.n_action_steps
    pre, post = make_pre_post_processors(
        policy_cfg=cfg, pretrained_path=cfg.pretrained_path,
        preprocessor_overrides={"device_processor": {"device": device}})
    policy.reset()
    return policy, pre, post, cfg


def feature_names(cfg):
    return sorted(k for k, v in cfg.input_features.items() if "image" in k)


class PolicyDriver:
    """Step function of the 200 Hz thread: linearly interpolates between successive policy targets."""

    def __init__(self, q0_deg: np.ndarray, period: float):
        self.cur = np.asarray(q0_deg, dtype=float).copy()
        self.start, self.goal, self.t0, self.period = self.cur.copy(), self.cur.copy(), time.perf_counter(), period
        self.lock = threading.Lock()

    def set_goal(self, goal_deg: np.ndarray):
        with self.lock:
            self.start, self.goal, self.t0 = self.cur.copy(), np.asarray(goal_deg, float), time.perf_counter()

    def resync(self, joints_deg: dict):
        with self.lock:
            self.cur = np.array([joints_deg[f"{n}.pos"] for n in ALL_NAMES], dtype=float)
            self.start, self.goal, self.t0 = self.cur.copy(), self.cur.copy(), time.perf_counter()

    def step(self, dt: float) -> dict:
        with self.lock:
            a = min(1.0, (time.perf_counter() - self.t0) / self.period)
            self.cur = self.start + (self.goal - self.start) * a
            cur = self.cur.copy()
        action = {f"{n}.pos": float(v) for n, v in zip(ALL_NAMES, cur)}
        return action


class Keys:
    def __init__(self):
        self.go, self.quit = threading.Event(), threading.Event()
        keyboard.Listener(on_press=self._on_press).start()

    def _on_press(self, key):
        if key == keyboard.Key.right:
            self.go.set()
        elif key == keyboard.Key.esc:
            self.quit.set()


def dry_run(args, device):
    policy, pre, post, cfg = load_policy(args, device)
    print(f"policy {cfg.type}: chunk {cfg.chunk_size}, n_action_steps {policy.config.n_action_steps}, device {device}")
    print("expects:", {k: tuple(v.shape) for k, v in cfg.input_features.items()})
    h, w = args.cam_height, args.cam_width
    rng = np.random.default_rng(0)
    ready = np.degrees(READY_QPOS)
    obs = {f"{n}.pos": float(v) for n, v in zip(JOINT_NAMES, ready)}
    obs["gripper.pos"] = -200.0
    for name in ("front_wide", "gripper", "high_oblique"):
        obs[name] = rng.integers(0, 255, (h, w, 3), dtype=np.uint8)

    class _Fake:  # only the feature declarations are needed here
        observation_features = {**{f"{n}.pos": float for n in ALL_NAMES},
                                **{n: (h, w, 3) for n in ("front_wide", "gripper", "high_oblique")}}
        action_features = {f"{n}.pos": float for n in ALL_NAMES}
        robot_type = "rebot_b601_follower"

    ds_features = {**hw_to_dataset_features(_Fake.action_features, "action"),
                   **hw_to_dataset_features(_Fake.observation_features, "observation")}
    for i in range(3):
        t = time.perf_counter()
        with torch.inference_mode():
            frame = build_inference_frame(dict(obs), torch.device(device), ds_features, args.task, _Fake.robot_type)
            act = make_robot_action(post(policy.select_action(pre(frame))), ds_features)
        print(f"call {i}: {1000 * (time.perf_counter() - t):.0f} ms  first action [deg]:",
              {k[:-4]: round(v, 1) for k, v in act.items()})
        policy.reset()
    print("ready pose [deg]:", {n: round(float(v), 1) for n, v in zip(JOINT_NAMES, ready)})
    print("OK: the policy loads and produces 7-dim joint targets. (Fake images, so the values are not meaningful.)")


def main():
    args = parse_args()
    cam_file = json.loads(Path(args.cameras_file).read_text())
    # Same path as record_episodes.py: capture at the 16:9 mode, then downscale to the saved size
    cap_w, cap_h = args.capture_width or cam_file["width"], args.capture_height or cam_file["height"]
    args.cam_width = args.cam_width or cam_file.get("save_width", cap_w)
    args.cam_height = args.cam_height or cam_file.get("save_height", cap_h)
    device = pick_device(args.device)
    if args.dry_run:
        return dry_run(args, device)
    if not args.port:
        raise SystemExit("--port is required (or use --dry-run)")
    limits = gripper_limits.load()
    if limits is None:
        raise SystemExit(f"Gripper range not measured. Run: python tools/measure_gripper.py --port {args.port}")
    g_lo, g_hi = gripper_limits.bounds(limits)
    params = MitParams(**{f.name: getattr(args, f"mit_{f.name}") for f in fields(MitParams)})

    policy, pre, post, cfg = load_policy(args, device)
    print(f"policy {cfg.type} on {device}: chunk {cfg.chunk_size}, n_action_steps {policy.config.n_action_steps}")

    cameras = {n: OpenCVCameraConfig(index_or_path=i, width=cap_w, height=cap_h, fps=args.fps,
                                     warmup_s=3, fourcc=cam_file.get("fourcc"))
               for n, i in cam_file["cameras"].items()}
    print("cameras:", {n: c.index_or_path for n, c in cameras.items()},
          f"capture {cap_w}x{cap_h}@{args.fps} -> policy {args.cam_width}x{args.cam_height}")
    rcfg = RebotB601FollowerRobotConfig(port=args.port, cameras=cameras, disable_torque_on_disconnect=False,
                                        gripper_torque_ratio=args.gripper_torque_ratio)
    rcfg.joint_limits["gripper"] = (g_lo, g_hi)
    rcfg.gripper_control_mode = GripperControlMode.MIT if params.grip_mode == "mit" else GripperControlMode.FORCE_POS
    robot = RebotB601Follower(rcfg)
    for cam in robot.cameras.values():
        cam.connect = _retrying(cam.connect, cam)

    ds_features = {**hw_to_dataset_features(robot.action_features, "action"),
                   **hw_to_dataset_features(robot.observation_features, "observation")}
    # Same joint limits the IK used while recording, with a margin
    lim = MOTOR_PROFILES[MotorFamily.DM].joint_limits
    lo = np.array([lim[n][0] + 3 for n in JOINT_NAMES] + [g_lo])
    hi = np.array([lim[n][1] - 3 for n in JOINT_NAMES] + [g_hi])
    max_step = np.array([args.max_step_deg] * 6 + [args.max_gripper_step_deg])

    keys = Keys()
    robot.connect()
    loop = FastLoop(robot, rate=200.0, mit=MitFF(robot, params))
    runs = 0
    try:
        if not loop.gravity_check():
            raise SystemExit("gravity feed-forward check failed")
        if not move_to_ready(robot, speed=params.ready_speed, confirm=not args.yes):
            raise SystemExit("arm did not reach the ready pose")
        obs0 = robot.get_observation()
        driver = PolicyDriver([obs0[f"{n}.pos"] for n in ALL_NAMES], 1.0 / args.fps)
        loop.start(driver.step)
        period = 1.0 / args.fps

        while not keys.quit.is_set() and (args.runs == 0 or runs < args.runs):
            keys.go.clear()
            print(f"\n[run {runs + 1}] Ready. Press -> to start the policy (Esc to quit).")
            while not keys.go.is_set() and not keys.quit.is_set():
                time.sleep(0.02)
            if keys.quit.is_set():
                break
            keys.go.clear()
            policy.reset()
            print(f"  running for {args.duration:.0f} s.  -> stop early | S stop in place | Esc quit")
            t_end, next_tick, n, lat = time.perf_counter() + args.duration, time.perf_counter(), 0, []
            was_active = True
            while time.perf_counter() < t_end and not keys.go.is_set() and not keys.quit.is_set():
                if loop._mode != "teleop":  # stopped (S) or returning (H): do not fight it
                    was_active = False
                    time.sleep(0.02)
                    next_tick = time.perf_counter()
                    continue
                if not was_active:
                    policy.reset()  # drop the old action queue; the driver was re-synced by the loop
                    was_active = True
                t_inf = time.perf_counter()
                obs = robot.get_observation()
                for name in cameras:
                    if obs[name].shape[:2] != (args.cam_height, args.cam_width):
                        obs[name] = cv2.resize(obs[name], (args.cam_width, args.cam_height), interpolation=cv2.INTER_AREA)
                with torch.inference_mode():
                    frame = build_inference_frame(obs, torch.device(device), ds_features, args.task, getattr(robot, "robot_type", robot.name))
                    act = make_robot_action(post(policy.select_action(pre(frame))), ds_features)
                lat.append(time.perf_counter() - t_inf)
                goal = np.array([act[f"{n}.pos"] for n in ALL_NAMES], dtype=float)
                with driver.lock:
                    ref = driver.goal.copy()
                goal = np.clip(ref + np.clip(goal - ref, -max_step, max_step), lo, hi)  # rate and range limits
                driver.set_goal(goal)
                n += 1
                next_tick += period
                sleep = next_tick - time.perf_counter()
                if sleep > 0:
                    time.sleep(sleep)
                else:
                    next_tick = time.perf_counter()
            runs += 1
            if lat:
                print(f"  {n} policy steps, inference per step: median {1000 * np.median(lat):.0f} ms, "
                      f"max {1000 * max(lat):.0f} ms (a call every chunk is the slow one)")
            print("  returning to ready")
            loop.return_to_ready()
            time.sleep(0.2)
            t0 = time.time()
            while loop._mode == "returning" and time.time() - t0 < 20.0:
                time.sleep(0.05)
    finally:
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
        robot.disconnect()


if __name__ == "__main__":
    main()
