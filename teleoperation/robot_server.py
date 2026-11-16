#!/usr/bin/env python3
"""Long-running robot server: loads the policy and the arm once, then runs skills on request over HTTP.

  python robot_server.py --port /dev/tty.usbmodem00000000050C1 --policy RoboCrafty/smolvla_rebot_merged_V2_15000 \
      --device mps --cam-height 360

  # inference on the GPU Space instead of this machine (--policy picks one of the Space's models; default XVLA)
  python robot_server.py --port /dev/ttyACM0 --cameras-file config/cameras_linux.json \
      --remote-url https://niru-5-rebot-policy-server.hf.space --policy RoboCrafty/smolvla_rebot_merged_V2

  GET  /skills            skill names the orchestrator may use
  GET  /status            {"state": "idle|running|stopping", "skill": ..., "elapsed": ...}
  POST /run   {"skill": "towel"}      start a skill (409 if busy); the arm returns to ready when it ends
  POST /stop[?reason=done|stuck|...]  end the running skill, back to ready; the reason is reported in /status "last"
  GET  /frame?camera=front_wide       current camera image (JPEG)

Extra flags: --http-port 8000 --host 127.0.0.1 (all other options are those of rollout_policy.py).

Only skills from config/skills.json can be run, with their exact training prompt. The keys S / G / H of the 200 Hz loop
still work (S stops the arm in place). Ctrl-C shuts the server down and parks the arm (see --park).

--fake runs the HTTP layer without arm, cameras or model, to test the orchestrator.
"""
import argparse
import json
import sys
import threading
import time
from pathlib import Path

import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

SKILLS_FILE = Path(__file__).resolve().parent / "config" / "skills.json"


class RunRequest(BaseModel):
    skill: str


class Runner:
    """Owns the arm, cameras and policy. One skill at a time, executed on a worker thread."""

    def __init__(self, args):
        self.args = args
        self.skills = json.loads(SKILLS_FILE.read_text())["skills"]
        self.state, self.skill, self.t0, self.last = "idle", None, 0.0, {}
        self.stop_reason, self.motion = None, 0.0  # motion: largest arm-joint travel [deg] over the last 3 s
        self.stop_flag = threading.Event()
        self.lock = threading.Lock()
        self.fake = args.fake
        if not self.fake:
            self._setup_real()

    # ---- setup (real hardware) -----------------------------------------------------------------------------
    def _setup_real(self):
        import torch
        import rollout_policy as rp
        from dataclasses import fields
        from lerobot.cameras.opencv import OpenCVCameraConfig
        from lerobot.robots.rebot_b601_follower import RebotB601Follower, RebotB601FollowerRobotConfig
        from lerobot.robots.rebot_b601_follower.motor_family import MOTOR_PROFILES, GripperControlMode, MotorFamily
        from record_episodes import _retrying
        from teleop import gripper_limits
        from teleop.fast_loop import FastLoop
        from teleop.mit_ff import MitFF, MitParams
        from teleop.ready_move import move_to_ready

        a = self.args
        self.torch, self.rp = torch, rp
        cam_file = json.loads(Path(a.cameras_file).read_text())
        cap_w, cap_h = a.capture_width or cam_file["width"], a.capture_height or cam_file["height"]
        self.w = a.cam_width or cam_file.get("save_width", cap_w)
        self.h = a.cam_height or cam_file.get("save_height", cap_h)
        self.device = rp.pick_device(a.device)
        limits = gripper_limits.load()
        if limits is None:
            raise SystemExit(f"Gripper range not measured. Run: python tools/measure_gripper.py --port {a.port}")
        g_lo, g_hi = gripper_limits.bounds(limits)
        params = MitParams(**{f.name: getattr(a, f"mit_{f.name}") for f in fields(MitParams)})

        # Local checkpoint or the remote GPU server (--remote-url, e.g. the HF Space); same interface either way.
        # sizes: robot camera -> (h, w) the policy was trained on (undoes camera renaming such as camera1).
        self.pol, self.sizes = rp.make_policy(a, self.device)

        cameras = {n: OpenCVCameraConfig(index_or_path=i, width=cap_w, height=cap_h, fps=a.fps, warmup_s=3,
                                         fourcc=cam_file.get("fourcc")) for n, i in cam_file["cameras"].items()}
        rcfg = RebotB601FollowerRobotConfig(port=a.port, cameras=cameras, disable_torque_on_disconnect=False,
                                            gripper_torque_ratio=a.gripper_torque_ratio)
        rcfg.joint_limits["gripper"] = (g_lo, g_hi)
        rcfg.gripper_control_mode = GripperControlMode.MIT if params.grip_mode == "mit" else GripperControlMode.FORCE_POS
        self.robot = RebotB601Follower(rcfg)
        for cam in self.robot.cameras.values():
            cam.connect = _retrying(cam.connect, cam)
        self.camera_names = list(cameras)
        missing = set(self.sizes) - set(self.camera_names)
        if missing:
            raise SystemExit(f"policy expects cameras {sorted(self.sizes)}, {sorted(missing)} missing from {a.cameras_file}")
        lim = MOTOR_PROFILES[MotorFamily.DM].joint_limits
        self.lo = np.array([lim[n][0] + 3 for n in rp.JOINT_NAMES] + [g_lo])
        self.hi = np.array([lim[n][1] - 3 for n in rp.JOINT_NAMES] + [g_hi])
        self.max_step = np.array([a.max_step_deg] * 6 + [a.max_gripper_step_deg])

        # S / G / H: pynput needs X11; under Wayland read them from this terminal (--keys, see teleop/term_keys.py)
        self.key_backend = rp.pick_key_backend(a.keys)
        FastLoop.key_backend = self.key_backend
        print(f"keys: {self.key_backend}" + (" (S / G / H are read from THIS terminal; keep it focused)"
                                              if self.key_backend == "terminal" else ""))
        self.robot.connect()
        self.loop = FastLoop(self.robot, rate=200.0, mit=MitFF(self.robot, params))
        if not self.loop.gravity_check():
            raise SystemExit("gravity feed-forward check failed")
        if not move_to_ready(self.robot, speed=params.ready_speed, confirm=not a.yes):
            raise SystemExit("arm did not reach the ready pose")
        obs0 = self.robot.get_observation()
        self.driver = rp.PolicyDriver([obs0[f"{n}.pos"] for n in rp.ALL_NAMES], 1.0 / a.fps)
        self.loop.start(self.driver.step)
        print("robot ready.")

    # ---- API ------------------------------------------------------------------------------------------------
    def status(self):
        el = time.time() - self.t0 if self.state != "idle" else 0.0
        return {"state": self.state, "skill": self.skill, "elapsed": round(el, 1),
                "motion_deg_3s": round(self.motion, 1), "last": self.last}

    def start(self, skill: str):
        if skill not in self.skills:
            raise KeyError(skill)
        with self.lock:
            if self.state != "idle":
                raise RuntimeError(f"busy ({self.state}: {self.skill})")
            self.state, self.skill, self.t0 = "running", skill, time.time()
            self.stop_flag.clear()
            self.stop_reason, self.motion = None, 0.0
        threading.Thread(target=self._run, args=(skill,), daemon=True).start()

    def stop(self, reason: str | None = None):
        if self.state == "running":
            self.stop_reason = reason
            self.state = "stopping"
            self.stop_flag.set()

    def frame_jpeg(self, camera: str) -> bytes:
        if self.fake:
            img = np.full((self.args.cam_height or 360, self.args.cam_width or 640, 3), 90, np.uint8)
            cv2.putText(img, f"fake {camera}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        else:
            if camera not in self.camera_names:
                raise KeyError(camera)
            img = self.robot.get_observation()[camera]  # RGB
            img = cv2.resize(img, (self.w, self.h), interpolation=cv2.INTER_AREA)
        ok, buf = cv2.imencode(".jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 85])
        return buf.tobytes()

    # ---- skill execution ------------------------------------------------------------------------------------
    def _run(self, skill: str):
        spec = self.skills[skill]
        ok, note = True, ""
        try:
            if self.fake:
                t_end = time.time() + 40
                while time.time() < t_end and not self.stop_flag.is_set():
                    self.motion = 6.0
                    time.sleep(0.1)
            else:
                note = self._run_policy(spec["prompt"], float(spec.get("duration", 45)))
        except Exception as e:  # keep the server alive; the arm is held by the 200 Hz loop
            ok, note = False, f"error: {e!r}"
            print(note)
        finally:
            self.last = {"skill": skill, "finished": ok, "stopped_early": self.stop_flag.is_set(),
                         "reason": self.stop_reason, "note": note}
            if not self.fake:
                self._return_to_ready()
            self.state, self.skill = "idle", None

    def _run_policy(self, prompt: str, duration: float) -> str:
        rp, a = self.rp, self.args
        self.pol.reset()
        period, n, lat = 1.0 / a.fps, 0, []
        hist = []  # (time, arm joints) for the motion measure
        t_end, next_tick, was_active = time.perf_counter() + duration, time.perf_counter(), True
        while time.perf_counter() < t_end and not self.stop_flag.is_set():
            if self.loop._mode != "teleop":  # S (stop) or H (ready) pressed: do not fight it
                was_active = False
                time.sleep(0.02)
                next_tick = time.perf_counter()
                continue
            if not was_active:
                self.pol.reset()
                was_active = True
            obs = self.robot.get_observation()
            now = time.time()
            hist.append((now, np.array([obs[f"{n}.pos"] for n in rp.JOINT_NAMES])))
            while hist and now - hist[0][0] > 3.0:
                hist.pop(0)
            q = np.array([h[1] for h in hist])
            self.motion = float(np.max(q.max(0) - q.min(0)))
            obs = rp.resize_to_policy(obs, self.sizes)
            t_inf = time.perf_counter()
            act = self.pol.select_action(obs, prompt)
            lat.append(time.perf_counter() - t_inf)
            goal = np.array([act[f"{n}.pos"] for n in rp.ALL_NAMES], dtype=float)
            with self.driver.lock:
                ref = self.driver.goal.copy()
            goal = np.clip(ref + np.clip(goal - ref, -self.max_step, self.max_step), self.lo, self.hi)
            self.driver.set_goal(goal)
            n += 1
            next_tick += period
            sleep = next_tick - time.perf_counter()
            if sleep > 0:
                time.sleep(sleep)
            else:
                next_tick = time.perf_counter()
        return f"{n} steps, inference median {1000 * float(np.median(lat)) if lat else 0:.0f} ms"

    def _return_to_ready(self):
        self.loop.return_to_ready()
        time.sleep(0.2)
        t0 = time.time()
        while self.loop._mode == "returning" and time.time() - t0 < 20.0:
            time.sleep(0.05)

    def shutdown(self):
        if self.fake:
            return
        if self.key_backend == "terminal":
            from teleop.term_keys import TerminalKeys
            TerminalKeys.get().stop()  # give the terminal back to input()
        # No move to the folded rest pose (its path can hit things behind the arm): release torque in place.
        release = self.args.park == "yes"
        if self.args.park == "ask":
            try:
                input("\nThe arm is being held. Put a hand under it, then press Enter to release torque and exit "
                      "(the arm will drop where it is; Ctrl-C: exit without releasing)... ")
                release = True
            except (KeyboardInterrupt, EOFError):
                print("\nexiting without releasing torque: support the arm, then switch off the power")
        if release:
            self.loop.release_in_place(warn_s=3.0)
        self.robot.disconnect()


def make_app(runner: Runner) -> FastAPI:
    app = FastAPI(title="reBot robot server")

    @app.get("/skills")
    def skills():
        return {k: v["prompt"] for k, v in runner.skills.items()}

    @app.get("/status")
    def status():
        return runner.status()

    @app.post("/run")
    def run(req: RunRequest):
        try:
            runner.start(req.skill)
        except KeyError:
            raise HTTPException(404, f"unknown skill {req.skill!r}; known: {list(runner.skills)}")
        except RuntimeError as e:
            raise HTTPException(409, str(e))
        return runner.status()

    @app.post("/stop")
    def stop(reason: str | None = None):
        runner.stop(reason)
        return runner.status()

    @app.get("/frame")
    def frame(camera: str = "front_wide"):
        try:
            return Response(runner.frame_jpeg(camera), media_type="image/jpeg")
        except KeyError:
            raise HTTPException(404, f"unknown camera {camera!r}")

    return app


def main():
    fake = "--fake" in sys.argv
    argv_rest = [a for a in sys.argv[1:] if a not in ("--fake",)]
    host, http_port = "127.0.0.1", 8000
    clean = []
    it = iter(argv_rest)
    for a in it:
        if a == "--http-port":
            http_port = int(next(it))
        elif a == "--host":
            host = next(it)
        else:
            clean.append(a)
    sys.argv = [sys.argv[0]] + clean
    if fake and "--policy" not in clean:
        sys.argv += ["--policy", "fake"]
    import rollout_policy as rp
    args = rp.parse_args()
    args.fake = fake
    # (--cam-width/--cam-height stay unset unless given: the policy's own training size is used, see make_policy)
    if not fake and not args.port:
        raise SystemExit("--port is required (or use --fake)")

    runner = Runner(args)
    try:
        uvicorn.run(make_app(runner), host=host, port=http_port, log_level="warning")
    finally:
        runner.stop_flag.set()
        runner.shutdown()


if __name__ == "__main__":
    main()
