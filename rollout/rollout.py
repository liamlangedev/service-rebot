#!/usr/bin/env python3
"""Roll out policies on the real reBot B601, with safety limits. See rollout/README.md.

Modes
-----
  full       full-task policy (ACT / SmolVLA on rebot_sort_v1) from the ready pose
  grasp-abs  grasp-only ACT (absolute): drive slowly to a dataset clip's start pose,
             then grasp; stops once gripped and lifted
  grasp-rel  grasp-only ACT (relative): place the arm above the keys by hand (torque off),
             lock it, then grasp; stops once gripped and lifted

Keys (terminal, no Enter): a = start   space/s = stop and hold   q = quit
                           h = torque off/on for hand placement (grasp-rel, before start)

Every stop holds the arm where it is (torque on). Quit leaves torque on as well: support
the arm before switching the power off.
"""

from __future__ import annotations

import argparse
import json
import threading
import time
from pathlib import Path

import numpy as np

import robot_io
from keys import Keys
from robot_io import READY_DEG, Fk, connect_robot, set_torque, state_of, to_action
from safety import GripperUnits, LagWatch, SafetyFilter, SafetyLimits

RATE = 30.0
DT = 1.0 / RATE
DEFAULT_POLICY = {
    "full": "niru-5/act_rebot_sort_v1",
    "grasp-abs": "niru-5/act_rebot_grasp_keys_abs",
    "grasp-rel": "niru-5/act_rebot_grasp_keys_rel",
}
#: the abs grasp run stopped at step ~2.1k without pushing a final model (training/RUNS.md);
#: its last checkpoint lives only in this subfolder
DEFAULT_SUBFOLDER = {"grasp-abs": "checkpoints/002000/pretrained_model"}
SMOLVLA_CAMERAS = {"camera1": "front_wide", "camera2": "gripper", "camera3": "high_oblique"}


# ---------------------------------------------------------------------------- helpers
class Session:
    """Robot + cameras + safety + keys + log, shared by all modes."""

    def __init__(self, args, needed_cams: list[str]):
        self.args = args
        self.keys = Keys()
        cams = dict(c.split("=", 1) for c in (args.cam or []))
        missing = [c for c in needed_cams if c not in cams]
        if missing and not args.fake_hardware:
            raise SystemExit(f"policy needs cameras {missing}: add --cam NAME=/dev/videoN")
        self.robot, limits = connect_robot(args, {c: cams[c] for c in needed_cams if c in cams})
        self.grip = GripperUnits(robot_open=limits[0], robot_closed=limits[1])
        self.fk = Fk()
        self.limits = SafetyLimits(max_speed_deg_s=args.max_speed, max_offset_deg=args.max_offset,
                                   min_tcp_z=args.min_tcp_z, max_reach_m=args.max_reach,
                                   max_lag_deg=args.max_lag_deg)
        self.safety = SafetyFilter(self.limits, RATE, fk=self.fk)
        self.fake_cams = None
        if args.fake_hardware and needed_cams:
            self.fake_cams = robot_io.FakeCameras(args.fake_images_repo, args.fake_images_root,
                                                  args.fake_episode, args.fake_start_frame,
                                                  needed_cams)
        self.log: list[dict] = []
        self.events: list[str] = []
        self.t0 = time.monotonic()

    def observe(self) -> tuple[np.ndarray, dict[str, np.ndarray]]:
        obs = self.robot.get_observation()
        images = self.fake_cams.read() if self.fake_cams else {
            k: v for k, v in obs.items() if isinstance(v, np.ndarray) and v.ndim == 3}
        return state_of(obs), images

    def state(self) -> np.ndarray:
        return state_of(self.robot.get_observation())

    def send(self, cmd7: np.ndarray) -> None:
        self.robot.send_action(to_action(cmd7))

    def event(self, msg: str) -> None:
        stamp = f"[{time.monotonic() - self.t0:6.1f}s] {msg}"
        print(stamp, flush=True)
        self.events.append(stamp)

    def hold(self, until_quit: bool = True) -> None:
        """Stream hold commands at the current pose (motors may go limp without commands)."""
        target = self.state()
        self.event("holding" + ("; press q to quit" if until_quit and self.keys.enabled else ""))
        t_end = time.monotonic() + (1e9 if until_quit and self.keys.enabled else 1.0)
        while time.monotonic() < t_end:
            self.send(target)
            if self.keys.poll() == "q":
                break
            time.sleep(DT)

    def wait_key(self, prompt: str, allowed: str = "aq") -> str:
        """Hold the pose while waiting for one of `allowed` (auto 'a' with --auto-start)."""
        if self.args.auto_start or not self.keys.enabled:
            if not self.args.auto_start:
                raise SystemExit("no terminal for keys: run in a terminal or pass --auto-start")
            return "a"
        print(prompt, flush=True)
        target = self.state()
        while True:
            self.send(target)
            k = self.keys.poll()
            if k and k in allowed:
                return k
            time.sleep(DT)

    def move_to(self, target7: np.ndarray, seconds: float, label: str) -> bool:
        """Smooth joint-space move (gripper included) under the speed, workspace and lag checks."""
        start = self.state()
        why = self.safety.check_pose(target7)
        if why:
            self.event(f"refusing to move to {label}: {why}")
            return False
        dist = float(np.max(np.abs(target7[:6] - start[:6])))
        seconds = max(seconds, dist / self.limits.max_speed_deg_s)
        n = max(2, int(seconds * RATE))
        self.event(f"moving to {label} over {seconds:.1f} s (max joint change {dist:.0f} deg); "
                   "space = stop")
        lag = LagWatch(self.limits)
        t0 = time.monotonic()
        prev = start
        for i in range(1, n + int(RATE) + 1):  # + 1 s to settle
            s = min(i / n, 1.0)
            s = s * s * (3 - 2 * s)
            cmd = start + s * (target7 - start)
            why = self.safety.check_pose(cmd, from_q=prev)  # may rise out of a low pose
            if why:
                self.event(f"STOP: {why}")
                return False
            self.send(cmd)
            prev = cmd
            k = self.keys.poll()
            if k in (" ", "s", "q"):
                self.event("stopped by key")
                return False
            why = lag.update(time.monotonic(), cmd, self.state())
            if why:
                self.event(f"STOP: {why}")
                return False
            sleep = t0 + i * DT - time.monotonic()
            if sleep > 0:
                time.sleep(sleep)
        err = float(np.max(np.abs(self.state()[:6] - target7[:6])))
        self.event(f"at {label} (residual {err:.1f} deg)")
        return err < self.args.arrive_tol_deg

    def save(self, mode: str, summary: dict) -> Path:
        out = Path(self.args.log_dir)
        out.mkdir(parents=True, exist_ok=True)
        stem = out / f"{time.strftime('%Y%m%d_%H%M%S')}_{mode}"
        if self.log:
            np.savez_compressed(stem.with_suffix(".npz"), **{
                k: np.array([row[k] for row in self.log]) for k in self.log[0]})
        stem.with_suffix(".json").write_text(json.dumps(
            {**summary, "events": self.events, "args": vars(self.args)}, indent=2, default=str))
        print(f"log: {stem}.json / .npz")
        return stem


def load_runner(args, mode: str):
    from rebot_trash_sorting_agent.grasp_policy.runner import PolicyRunner, RunnerConfig
    policy = args.policy or DEFAULT_POLICY[mode]
    sub = args.policy_subfolder if args.policy_subfolder is not None else (
        DEFAULT_SUBFOLDER.get(mode) if not args.policy else None)
    rel = mode == "grasp-rel"
    task = args.task or ("pickup the keys and put it in the designated bin" if mode == "full"
                         else "grasp the keys and lift them")
    use_cams = tuple(args.use_cams) if args.use_cams else None
    if args.remote:
        # inference on a remote GPU (rollout/remote/): the server downloads the model
        from remote_runner import RemoteRunner
        runner = RemoteRunner(args.remote, policy, sub, "relative" if rel else "absolute",
                              task, use_cams, args.max_offset or 180.0)
    else:
        if sub:
            from huggingface_hub import snapshot_download
            policy = str(Path(snapshot_download(policy, allow_patterns=[f"{sub}/*"])) / sub)
        print(f"loading {policy} ({'relative' if rel else 'absolute'}, {args.device})")
        runner = PolicyRunner(RunnerConfig(policy_path=policy, mode="relative" if rel else "absolute",
                                           device=args.device, task=task,
                                           max_offset_deg=args.max_offset or 180.0,
                                           use_cameras=use_cams))
    cam_map = {n: SMOLVLA_CAMERAS.get(n, n) for n in runner.camera_names}
    for pair in args.camera_map or []:
        k, v = pair.split("=", 1)
        cam_map[k] = v
    print("policy cameras:", cam_map)
    return runner, cam_map


# ---------------------------------------------------------------------------- policy loop
def run_policy(sess: Session, runner, cam_map: dict[str, str], grasp: bool) -> dict:
    """Run the policy until done / timeout / key / safety, then return a summary (the
    caller holds the arm).

    Default (streaming): inference runs in a thread on the latest observation, and each
    30 Hz tick executes the action of the newest chunk that belongs to "now". It needs
    inference faster than a chunk.

    --sync (slow policies, e.g. SmolVLA on a CPU): hold still -> infer on the current
    observation -> play the chunk from its first action -> repeat. The arm waits during
    inference, so the observation the chunk was planned from stays valid. --timeout then
    counts only the time spent moving.
    """
    from rebot_trash_sorting_agent.grasp_policy.done import DoneConfig, GraspDone

    args = sess.args
    state, images = sess.observe()
    anchor_data = state.copy()
    anchor_data[6] = sess.grip.to_data(state[6])
    runner.start(anchor_data)
    sess.safety.set_anchor(state)
    done = GraspDone(DoneConfig(lift_m=args.lift_m)) if grasp else None
    lag = LagWatch(sess.limits)
    ctx = {"prev_cmd": state.copy(), "t_start": time.monotonic(), "moving_s": 0.0}
    infer_ms: list[float] = []

    def predict(st, imgs):
        st_data = st.copy()
        st_data[6] = sess.grip.to_data(st[6])
        pimgs = {pname: imgs[src] for pname, src in cam_map.items()}
        tic = time.monotonic()
        acts, _ = runner.predict(st_data, pimgs, n=runner.chunk_size)
        infer_ms.append((time.monotonic() - tic) * 1000)
        return acts

    def apply(a, st, now) -> str | None:
        """Safety-filter and send one policy action; returns a stop reason or None."""
        cmd = np.r_[a[:6], sess.grip.to_robot(float(a[6]))]
        v = sess.safety.filter(cmd, ctx["prev_cmd"])
        if v.stop:
            return f"safety: {v.stop}"
        sess.send(v.command)
        ctx["prev_cmd"] = v.command
        why = lag.update(now, v.command, st)
        if why:
            return f"safety: {why}"
        tcp = sess.fk(st)
        sess.log.append({"t": now - ctx["t_start"], "state": st, "policy_action": a,
                         "command": v.command, "tcp": np.array(tcp),
                         "clipped": ",".join(v.clipped)})
        if done is not None:
            closing = sess.grip.opening_data(float(a[6])) < 0.3
            finger = sess.grip.opening_robot(st[6]) * 0.05  # metre-equivalent
            if done.update(closing, finger, tcp[2]):
                return f"gripped and lifted {done.lifted_m * 100:.1f} cm"
        return None

    def key_stop() -> bool:
        return sess.keys.poll() in (" ", "s", "q")

    sess.event("policy running" + (" (sync: infer, then play the chunk)" if args.sync else "")
               + "; space = stop")
    reason = "timeout"
    if args.sync:
        reason = _loop_sync(sess, predict, apply, key_stop, ctx, args)
    else:
        reason = _loop_streaming(sess, predict, apply, key_stop, ctx, args)

    summary = {"reason": reason, "duration_s": round(time.monotonic() - ctx["t_start"], 2),
               "moving_s": round(ctx["moving_s"], 2), "sync": bool(args.sync),
               "ticks": len(sess.log), "inferences": len(infer_ms),
               "infer_ms_median": round(float(np.median(infer_ms)), 1) if infer_ms else None,
               "clipped_ticks": sum(1 for r in sess.log if r["clipped"])}
    if done is not None:
        summary.update(gripped=done.gripped, lifted_m=round(done.lifted_m, 4))
    sess.event(f"policy stopped: {reason}")
    return summary


def _loop_streaming(sess, predict, apply, key_stop, ctx, args) -> str:
    state, images = sess.observe()
    shared = {"obs": (state, images, time.monotonic()), "plan": None, "error": None}
    lock = threading.Lock()
    running = threading.Event()
    running.set()

    def infer_loop():
        while running.is_set():
            with lock:
                st, imgs, t_obs = shared["obs"]
            try:
                acts = predict(st, imgs)
                with lock:
                    shared["plan"] = (t_obs, acts)
            except Exception as exc:  # noqa: BLE001 - surfaced in the control loop
                shared["error"] = exc
                return

    threading.Thread(target=infer_loop, daemon=True).start()
    starved_plan = None
    try:
        while True:
            now = time.monotonic()
            if now - ctx["t_start"] > args.timeout:
                return "timeout"
            if shared["error"] is not None:
                return f"inference error: {shared['error']}"
            if key_stop():
                return "stopped by key"
            state, images = sess.observe()
            with lock:
                shared["obs"] = (state, images, now)
                plan = shared["plan"]
            if plan is None:  # first inference not ready yet: hold
                sess.send(ctx["prev_cmd"])
                time.sleep(DT)
                continue
            t_obs, acts = plan
            i = int(round((now - t_obs) / DT))
            if i >= len(acts):
                if starved_plan is not t_obs:
                    sess.event("chunk ran out before the next inference; repeating its last "
                               "action (slow policy? use --sync)")
                    starved_plan = t_obs
                i = len(acts) - 1
            why = apply(acts[i], state, now)
            if why:
                return why
            ctx["moving_s"] = now - ctx["t_start"]
            sleep = now + DT - time.monotonic()
            if sleep > 0:
                time.sleep(sleep)
    finally:
        running.clear()


def _loop_sync(sess, predict, apply, key_stop, ctx, args) -> str:
    n_play = args.sync_steps
    while True:
        if ctx["moving_s"] >= args.timeout:
            return "timeout"
        # 1. infer on the current observation while holding still
        state, images = sess.observe()
        box: dict = {}

        def work(st=state, imgs=images):
            try:
                box["acts"] = predict(st, imgs)
            except Exception as exc:  # noqa: BLE001
                box["error"] = exc

        th = threading.Thread(target=work, daemon=True)
        th.start()
        tic = time.monotonic()
        while th.is_alive():
            sess.send(ctx["prev_cmd"])          # hold
            if key_stop():
                return "stopped by key"
            time.sleep(DT)
        if "error" in box:
            return f"inference error: {box['error']}"
        sess.event(f"inference {time.monotonic() - tic:.1f} s; playing "
                   f"{min(n_play or len(box['acts']), len(box['acts']))} actions")
        # 2. play the chunk from its first action
        acts = box["acts"][: n_play or None]
        t0 = time.monotonic()
        for i, a in enumerate(acts):
            if key_stop():
                return "stopped by key"
            now = time.monotonic()
            state = sess.state()
            why = apply(a, state, now)
            if why:
                return why
            ctx["moving_s"] += DT
            sleep = t0 + (i + 1) * DT - time.monotonic()
            if sleep > 0:
                time.sleep(sleep)


# ---------------------------------------------------------------------------- modes
def dataset_start(args) -> tuple[np.ndarray, dict]:
    """First state of a clip of niru-5/rebot_grasp_keys_abs (dataset degrees)."""
    import glob

    import pandas as pd
    from huggingface_hub import snapshot_download

    root = snapshot_download(args.start_dataset, repo_type="dataset",
                             allow_patterns=["meta/*", "meta/**", "data/**"])
    df = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{root}/data/*/*.parquet"))])
    ep = df[df["episode_index"] == args.start_episode].sort_values("frame_index")
    if ep.empty:
        raise SystemExit(f"episode {args.start_episode} not in {args.start_dataset}")
    info = {}
    clips = Path(root) / "meta" / "grasp_clips.json"
    if clips.exists():
        g = json.loads(clips.read_text())
        src = g["train_source_episodes"] + g["holdout_source_episodes"]
        if args.start_episode < len(src):
            info["source_episode"] = src[args.start_episode]
            info["held_out"] = src[args.start_episode] in g["holdout_source_episodes"]
    return np.array(ep.iloc[0]["observation.state"], dtype=np.float64), info


def mode_full(sess: Session, runner, cam_map) -> dict:
    ready = np.r_[READY_DEG, sess.grip.robot_open]
    if not sess.move_to(ready, sess.args.approach_s, "ready pose"):
        return {"reason": "did not reach the ready pose"}
    if sess.wait_key("Ready. Press a to start the policy, q to quit.") == "q":
        return {"reason": "quit before start"}
    return run_policy(sess, runner, cam_map, grasp=False)


def mode_grasp_abs(sess: Session, runner, cam_map) -> dict:
    start_data, info = dataset_start(sess.args)
    start = start_data.copy()
    start[6] = sess.grip.robot_open
    x, y, z = sess.fk(start)
    print(f"clip {sess.args.start_episode} of {sess.args.start_dataset} {info}")
    print(f"  start joints [deg]: {np.round(start[:6], 1)}")
    print(f"  TCP at start: x={x:.3f} y={y:+.3f} m (base frame), {z * 100:.1f} cm site height")
    print("  place the object under the gripper there, as in that episode")
    ready = np.r_[READY_DEG, sess.grip.robot_open]
    if sess.args.via_ready and not sess.move_to(ready, 5.0, "ready pose"):
        return {"reason": "did not reach the ready pose", **info}
    if not sess.move_to(start, sess.args.approach_s, "dataset start pose"):
        return {"reason": "did not reach the start pose", **info}
    if sess.wait_key("At the start pose. Press a to grasp, q to quit.") == "q":
        return {"reason": "quit before start", **info}
    return {**run_policy(sess, runner, cam_map, grasp=True), **info,
            "start_state": start.tolist()}


def mode_grasp_rel(sess: Session, runner, cam_map) -> dict:
    ready = np.r_[READY_DEG, sess.grip.robot_open]
    if sess.args.via_ready and not sess.move_to(ready, 5.0, "ready pose"):
        return {"reason": "did not reach the ready pose"}
    print("Place the gripper ~5 cm above the keys, wrist camera looking at them:\n"
          "  h = torque OFF (SUPPORT THE ARM, it will drop) / h again = torque ON and hold here\n"
          "  a = start the grasp from the current pose   q = quit")
    if sess.args.auto_start or not sess.keys.enabled:
        sess.wait_key("")
    else:
        torque_on, target = True, sess.state()
        while True:
            if torque_on:
                sess.send(target)
            k = sess.keys.poll()
            if k == "h":
                torque_on = not torque_on
                if torque_on:
                    target = sess.state()
                    target[6] = sess.grip.robot_open
                    set_torque(sess.robot, True)
                    sess.send(target)
                    sess.event("torque ON, holding here")
                else:
                    sess.event("torque OFF: move the arm by hand, h to lock")
                    set_torque(sess.robot, False)
            elif k == "a":
                if not torque_on:
                    print("lock the arm first (h)")
                    continue
                break
            elif k == "q":
                if not torque_on:
                    set_torque(sess.robot, True)
                return {"reason": "quit before start"}
            time.sleep(DT)
    here = sess.state()
    why = sess.safety.check_pose(here, from_q=here)  # a low start only forbids going lower
    if why:
        return {"reason": f"start pose outside the workspace: {why}"}
    return run_policy(sess, runner, cam_map, grasp=True)


# ---------------------------------------------------------------------------- main
def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["full", "grasp-abs", "grasp-rel"])
    p.add_argument("--policy", help="Hub repo or local pretrained_model dir (default per mode)")
    p.add_argument("--policy-subfolder",
                   help="model folder inside the repo, e.g. checkpoints/004000/pretrained_model")
    p.add_argument("--task", help="language task (SmolVLA)")
    p.add_argument("--device", default="cpu")
    p.add_argument("--remote", metavar="URL",
                   help="run inference on a remote policy server (rollout/remote/), e.g. the "
                        "URL printed by rollout/remote/start_server.sh")
    p.add_argument("--cam", action="append", metavar="NAME=DEVICE",
                   help="camera by dataset name: front_wide, gripper, high_oblique")
    p.add_argument("--use-cams", nargs="+", metavar="POLICY_CAM",
                   help="feed only these policy cameras, e.g. --use-cams camera2 for a SmolVLA "
                        "trained on the wrist camera only (its config still lists camera1-3)")
    p.add_argument("--camera-map", action="append", metavar="POLICY=DATASET",
                   help="policy camera -> dataset camera (SmolVLA camera1..3 are mapped already)")
    # robot
    p.add_argument("--port", default="/dev/ttyACM0")
    p.add_argument("--robot-id", default="follower")
    p.add_argument("--calibration-dir", default=str(robot_io.REPO))
    p.add_argument("--fake-hardware", action="store_true", help="MuJoCo stand-in, no arm")
    # safety
    p.add_argument("--max-speed", type=float, default=45.0, help="joint speed cap [deg/s]")
    p.add_argument("--max-offset", type=float, default=None,
                   help="max arm joint change from the start [deg] (grasp modes default 30)")
    p.add_argument("--min-tcp-z", type=float, default=0.120, help="tcp site floor [m]")
    p.add_argument("--max-reach", type=float, default=0.55, help="horizontal reach cap [m]")
    p.add_argument("--max-lag-deg", type=float, default=25.0)
    p.add_argument("--arrive-tol-deg", type=float, default=5.0,
                   help="max joint error after a slow move, else stop")
    p.add_argument("--max-step-deg", type=float, default=8.0,
                   help="driver max_relative_target for the arm joints [deg per command]")
    p.add_argument("--max-gripper-step-deg", type=float, default=40.0,
                   help="driver max_relative_target for the gripper [deg per command]")
    p.add_argument("--gripper-torque-ratio", type=float, default=0.03,
                   help="FORCE_POS gripper force limit (as in teleoperation/rollout_policy.py)")
    p.add_argument("--motor-vel-deg", type=float, default=60.0, help="driver pos_vel speed [deg/s]")
    p.add_argument("--timeout", type=float, default=None,
                   help="policy time limit [s] (with --sync: time spent moving)")
    p.add_argument("--sync", action="store_true",
                   help="slow policies: hold while inferring, then play the chunk from its start")
    p.add_argument("--sync-steps", type=int, default=0,
                   help="with --sync: actions played per inference (0 = the whole chunk)")
    # grasp
    p.add_argument("--lift-m", type=float, default=0.05)
    p.add_argument("--approach-s", type=float, default=5.0, help="duration of the slow approach")
    p.add_argument("--start-dataset", default="niru-5/rebot_grasp_keys_abs")
    p.add_argument("--start-episode", type=int, default=27, help="clip index (27-29 held out)")
    p.add_argument("--no-via-ready", dest="via_ready", action="store_false")
    p.add_argument("--auto-start", action="store_true", help="no key presses (dry runs)")
    # dry-run images
    p.add_argument("--fake-images-repo", default="RoboCrafty/rebot_sort_v1")
    p.add_argument("--fake-images-root", default=None)
    p.add_argument("--fake-episode", type=int, default=32)
    p.add_argument("--fake-start-frame", type=int, default=0)
    p.add_argument("--log-dir", default=str(robot_io.REPO / "rollout" / "logs"))
    args = p.parse_args()

    grasp = args.mode != "full"
    if args.max_offset is None and grasp:
        args.max_offset = 30.0
    if args.timeout is None:
        args.timeout = 10.0 if grasp else 40.0
    if args.auto_start and not args.fake_hardware:
        p.error("--auto-start is only allowed with --fake-hardware")

    runner, cam_map = load_runner(args, args.mode)
    print("=" * 72)
    print(f" ROLLOUT {args.mode}" + (" (FAKE HARDWARE)" if args.fake_hardware else ""))
    print("  clear the workspace, hand near the power switch")
    print("  space/s = stop and hold   q = quit   (torque stays on)")
    print("=" * 72)
    sess = Session(args, needed_cams=sorted(set(cam_map.values())))
    summary: dict = {}
    with sess.keys:
        try:
            summary = {"grasp-abs": mode_grasp_abs, "grasp-rel": mode_grasp_rel,
                       "full": mode_full}[args.mode](sess, runner, cam_map)
        except KeyboardInterrupt:
            summary = {"reason": "Ctrl-C"}
        finally:
            try:
                sess.hold(until_quit=True)
            finally:
                sess.save(args.mode, summary)
                print(json.dumps(summary, indent=2, default=str))
                sess.robot.disconnect()


if __name__ == "__main__":
    main()
