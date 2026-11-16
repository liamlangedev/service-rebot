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

  # XVLA (merged V2 dataset, 640x360 images)
  python rollout_policy.py --port /dev/ttyACM0 --policy niru-5/xvla_rebot_merged_V2 \
      --task "pick up the bottle and put it in the designated bin" --duration 60

  # same, but inference on a GPU server (remote_inference/, e.g. a Hugging Face Space); no model on this machine
  python rollout_policy.py --port /dev/ttyACM0 --remote-url https://niru-5-rebot-policy-server.hf.space \
      --task "pick up the bottle and put it in the designated bin" --duration 60

Cameras capture at the cameras.json mode (16:9) and frames are downscaled to the image size the policy was
trained on (read from the checkpoint / server), like record_episodes.py.

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
from teleop.term_keys import TerminalKeys
from teleop.term_keys import pick_backend as pick_key_backend

# Gains used while recording the dataset (see REAL_ARM.md); the policy must see the same dynamics.
RECORDING_MIT = dict(kp_scale=3.0, kd_scale=3.0, wrist_scale=0.4, friction_scale=1.3)
ALL_NAMES = [*JOINT_NAMES, "gripper"]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--policy", default=None,
                   help="Hub repo or local folder, e.g. niru-5/act_rebot_sort_v1. For an intermediate checkpoint use "
                        "--subfolder checkpoints/010500/pretrained_model")
    p.add_argument("--subfolder", default=None)
    p.add_argument("--remote-url", default=None,
                   help="run inference on a remote server (remote_inference/app.py, e.g. https://<user>-<space>.hf.space) "
                        "instead of loading --policy here. Private Spaces use your HF token (hf auth login / HF_TOKEN)")
    p.add_argument("--remote-timeout", type=float, default=30.0)
    p.add_argument("--port", default=None, help="arm serial port (not needed with --dry-run)")
    p.add_argument("--task", default="pickup the keys and put it in the designated bin",
                   help="language prompt; used by SmolVLA/VLAs, ignored by ACT. Use the exact training wording")
    p.add_argument("--device", default="auto", help="auto (cuda > mps > cpu), cuda, mps or cpu")
    p.add_argument("--dtype", choices=["float32", "bfloat16"], default=None,
                   help="override the policy dtype (pi0/pi0.5: bfloat16 is faster on MPS/CUDA)")
    p.add_argument("--num-inference-steps", type=int, default=None,
                   help="flow-matching denoising steps (pi0/pi0.5/XVLA default 10); fewer = faster, slightly less precise")
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
                   help="image width fed to the policy; must match training (default: the policy's training size)")
    p.add_argument("--cam-height", type=int, default=None,
                   help="image height fed to the policy (default: the policy's training size)")
    p.add_argument("--capture-width", type=int, default=None, help="camera capture width (default: width of cameras.json)")
    p.add_argument("--capture-height", type=int, default=None, help="camera capture height (default: height of cameras.json)")
    p.add_argument("--gripper-torque-ratio", type=float, default=0.03)
    p.add_argument("--park", choices=["ask", "yes", "no"], default="ask")
    p.add_argument("--yes", action="store_true", help="skip the Enter prompt before the first ready move")
    p.add_argument("--dry-run", action="store_true", help="load the policy and run it on a fake observation; no robot")
    p.add_argument("--keys", choices=["auto", "pynput", "terminal"], default="auto",
                   help="where Right/Esc/S/G/H are read from. pynput needs an X11 session; terminal works under Wayland "
                        "but only while this terminal has focus. auto = terminal under Wayland, else pynput")
    p.add_argument("--dry-run-image", default=None,
                   help="with --dry-run: use this image (any size) for every camera instead of random noise")
    for f in fields(MitParams):
        d = RECORDING_MIT.get(f.name, getattr(MitParams(), f.name))
        p.add_argument(f"--mit.{f.name}", dest=f"mit_{f.name}", type=type(d), default=d)
    args = p.parse_args()
    if not args.policy and not args.remote_url:
        p.error("--policy or --remote-url is required")
    return args


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
    for attr in ("num_inference_steps", "num_denoising_steps"):  # pi0/SmolVLA name, XVLA name
        if args.num_inference_steps and hasattr(cfg, attr):
            setattr(cfg, attr, args.num_inference_steps)
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


def policy_image_sizes(cfg) -> dict:
    """camera name -> (height, width) the policy was trained on, from input_features shape (C, H, W)."""
    out = {}
    for k, v in cfg.input_features.items():
        if k.startswith("observation.images."):
            _, h, w = tuple(v.shape)
            out[k.removeprefix("observation.images.")] = (int(h), int(w))
    return out


def resize_to_policy(obs: dict, sizes: dict) -> dict:
    """Downscale camera frames to the policy's input size, the same way record_episodes.py does (INTER_AREA)."""
    for name, (h, w) in sizes.items():
        img = obs.get(name)
        if img is not None and img.shape[:2] != (h, w):
            obs[name] = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    return obs


class LocalPolicy:
    """Policy loaded on this machine, behind the same interface as teleop.remote_policy.RemotePolicy."""

    def __init__(self, args, device: str):
        self.policy, self.pre, self.post, self.cfg = load_policy(args, device)
        self.device = torch.device(device)
        self.image_sizes = policy_image_sizes(self.cfg)
        act = {f"{n}.pos": float for n in ALL_NAMES}
        obs = {**act, **{n: (h, w, 3) for n, (h, w) in self.image_sizes.items()}}
        self.ds_features = {**hw_to_dataset_features(act, "action"), **hw_to_dataset_features(obs, "observation")}
        print(f"policy {self.cfg.type} on {device}: chunk {self.cfg.chunk_size}, "
              f"n_action_steps {self.policy.config.n_action_steps}")

    def reset(self):
        self.policy.reset()

    def select_action(self, obs: dict, task: str) -> dict:
        with torch.inference_mode():
            frame = build_inference_frame(obs, self.device, self.ds_features, task, "rebot_b601_follower")
            return make_robot_action(self.post(self.policy.select_action(self.pre(frame))), self.ds_features)


def make_policy(args, device: str):
    """Returns (policy, {camera: (h, w)} fed to it). --cam-width/--cam-height override the training size."""
    if args.remote_url:
        from teleop.remote_policy import RemotePolicy
        pol = RemotePolicy(args.remote_url, n_action_steps=args.n_action_steps, timeout=args.remote_timeout)
        i = pol.info
        print(f"remote policy {i['type']} ({i['policy']}) on {i.get('gpu') or i['device']} {i.get('dtype', '')} "
              f"at {args.remote_url}: chunk {pol.chunk_size}, n_action_steps {pol.n_action_steps}")
    else:
        pol = LocalPolicy(args, device)
    sizes = dict(pol.image_sizes)
    if args.cam_width and args.cam_height:
        sizes = {n: (args.cam_height, args.cam_width) for n in sizes}
    return pol, sizes


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
    """Right = go, Esc = quit. backend "pynput" (X11) or "terminal" (teleop/term_keys.py, works under Wayland;
    the terminal must have focus). With the terminal backend, keys are read once FastLoop.start() runs."""

    def __init__(self, backend: str = "pynput"):
        self.go, self.quit = threading.Event(), threading.Event()
        if backend == "terminal":
            from teleop.term_keys import TerminalKeys
            TerminalKeys.get().add_callback(self._on_name)
        else:
            from pynput import keyboard
            self._kb = keyboard
            keyboard.Listener(on_press=self._on_press).start()

    def _on_name(self, name: str):
        if name == "right":
            self.go.set()
        elif name == "esc":
            self.quit.set()

    def _on_press(self, key):
        if key == self._kb.Key.right:
            self.go.set()
        elif key == self._kb.Key.esc:
            self.quit.set()


def dry_run(args, device, cap_w, cap_h):
    pol, sizes = make_policy(args, device)
    cams = list(sizes) or ["front_wide", "gripper", "high_oblique"]
    print("policy input cameras [HxW]:", sizes)
    rng = np.random.default_rng(0)
    ready = np.degrees(READY_QPOS)
    obs = {f"{n}.pos": float(v) for n, v in zip(JOINT_NAMES, ready)}
    obs["gripper.pos"] = -200.0
    img = None
    if args.dry_run_image:
        img = cv2.cvtColor(cv2.imread(args.dry_run_image), cv2.COLOR_BGR2RGB)
        cap_h, cap_w = img.shape[:2]
    for name in cams:  # fake frames at capture size, then resized like on the robot
        obs[name] = img.copy() if img is not None else rng.integers(0, 255, (cap_h, cap_w, 3), dtype=np.uint8)
    obs = resize_to_policy(obs, sizes)
    print("images:", {n: obs[n].shape for n in cams}, f"(captured {cap_w}x{cap_h})")
    for i in range(3):
        pol.reset()
        t = time.perf_counter()
        act = pol.select_action(dict(obs), args.task)
        ms = getattr(pol, "last_ms", None)
        ms = f" (round trip {ms['rtt']:.0f} ms, server inference {ms['infer']:.0f} ms)" if ms else ""
        print(f"call {i}: {1000 * (time.perf_counter() - t):.0f} ms{ms}  first action [deg]:",
              {k[:-4]: round(v, 1) for k, v in act.items()})
    print("ready pose [deg]:", {n: round(float(v), 1) for n, v in zip(JOINT_NAMES, ready)})
    print("OK: the policy loads and produces 7-dim joint targets. (Fake images, so the values are not meaningful.)")


def main():
    args = parse_args()
    cam_file = json.loads(Path(args.cameras_file).read_text())
    # Same path as record_episodes.py: capture at the 16:9 mode, then downscale to the saved size
    cap_w, cap_h = args.capture_width or cam_file["width"], args.capture_height or cam_file["height"]
    device = pick_device(args.device)
    if args.dry_run:
        return dry_run(args, device, cap_w, cap_h)
    if not args.port:
        raise SystemExit("--port is required (or use --dry-run)")
    limits = gripper_limits.load()
    if limits is None:
        raise SystemExit(f"Gripper range not measured. Run: python tools/measure_gripper.py --port {args.port}")
    g_lo, g_hi = gripper_limits.bounds(limits)
    params = MitParams(**{f.name: getattr(args, f"mit_{f.name}") for f in fields(MitParams)})

    pol, sizes = make_policy(args, device)
    missing = set(sizes) - set(cam_file["cameras"])
    if missing:
        raise SystemExit(f"policy expects cameras {sorted(sizes)}, {sorted(missing)} missing from {args.cameras_file}")

    cameras = {n: OpenCVCameraConfig(index_or_path=i, width=cap_w, height=cap_h, fps=args.fps,
                                     warmup_s=3, fourcc=cam_file.get("fourcc"))
               for n, i in cam_file["cameras"].items()}
    print("cameras:", {n: c.index_or_path for n, c in cameras.items()},
          f"capture {cap_w}x{cap_h}@{args.fps} -> policy", {n: f"{w}x{h}" for n, (h, w) in sizes.items()})
    rcfg = RebotB601FollowerRobotConfig(port=args.port, cameras=cameras, disable_torque_on_disconnect=False,
                                        gripper_torque_ratio=args.gripper_torque_ratio)
    rcfg.joint_limits["gripper"] = (g_lo, g_hi)
    rcfg.gripper_control_mode = GripperControlMode.MIT if params.grip_mode == "mit" else GripperControlMode.FORCE_POS
    robot = RebotB601Follower(rcfg)
    for cam in robot.cameras.values():
        cam.connect = _retrying(cam.connect, cam)

    # Same joint limits the IK used while recording, with a margin
    lim = MOTOR_PROFILES[MotorFamily.DM].joint_limits
    lo = np.array([lim[n][0] + 3 for n in JOINT_NAMES] + [g_lo])
    hi = np.array([lim[n][1] - 3 for n in JOINT_NAMES] + [g_hi])
    max_step = np.array([args.max_step_deg] * 6 + [args.max_gripper_step_deg])

    key_backend = pick_key_backend(args.keys)
    FastLoop.key_backend = key_backend
    print(f"keys: {key_backend}" + (" (keep THIS terminal focused: -> / Esc / S / G / H are read from it)"
                                     if key_backend == "terminal" else ""))
    keys = Keys(key_backend)
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
            pol.reset()
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
                    pol.reset()  # drop the old action queue; the driver was re-synced by the loop
                    was_active = True
                t_inf = time.perf_counter()
                obs = resize_to_policy(robot.get_observation(), sizes)
                act = pol.select_action(obs, args.task)
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
        if key_backend == "terminal":
            TerminalKeys.get().stop()  # give the terminal back to input()
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
