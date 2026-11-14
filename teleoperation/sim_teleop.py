#!/usr/bin/env python3
"""Teleoperate the reBot Arm B601 in MuJoCo and optionally record a LeRobot dataset.

  uv run sim_teleop.py --input quest            # Quest via the WebXR relay (start it first)
  uv run sim_teleop.py --input oculus           # Quest via OculusReader (APK + ADB)
  uv run sim_teleop.py --input oculus --ip 192.168.1.42  # OculusReader over Wi-Fi ADB
  uv run sim_teleop.py --input mouse            # no headset: drag the arm
  uv run sim_teleop.py --input demo             # scripted controller motion

  # record episodes (needs: uv sync --extra lerobot)
  uv run sim_teleop.py --input mouse --record --task "pick up the red cube"

  # drive the REAL arm (LeRobot driver); the sim mirrors the measured pose
  uv run sim_teleop.py --input quest --robot real --port /dev/ttyACM0

Quest controls (right hand by default):
  grip (hold)       clutch: the arm follows your hand while held
  trigger           close the gripper
  A                 send the arm home
  B                 toggle orientation tracking (position-only is easier at first)
  joystick click    start / save a recording episode

Mouse controls: double-click any part of the arm (it gets highlighted), then
  Ctrl + right-drag   move the gripper
  Ctrl + left-drag    rotate the gripper

Keyboard (in the viewer window):
  Up / Down   open / close the gripper (mouse and demo modes)
  Home        send the arm home
  End         start / save a recording episode
  Delete      discard the episode being recorded
"""
import argparse
import os
import sys
import time
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np

from teleop.ik import DiffIK
from teleop.mouse_input import MouseDragTeleop
from teleop.quest_input import ClutchTeleop, DemoSource, make_quest_source
from teleop.rebot_model import ARM_JOINTS, GRIPPER_MAX, HOME_QPOS, TCP_SITE, RebotSim

KEY_UP, KEY_DOWN, KEY_HOME, KEY_END, KEY_DELETE = 265, 264, 268, 269, 261
VIEWER_HZ = 50.0


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", choices=["quest", "oculus", "mouse", "demo"], default="quest",
                   help="quest = WebXR relay, oculus = OculusReader")
    p.add_argument("--hand", choices=["r", "l"], default="r")
    p.add_argument("--relay", default="ws://127.0.0.1:8443/ws", help="WebXR relay WebSocket")
    p.add_argument("--ip", default=None, help="Quest IP for wireless ADB (oculus only)")
    p.add_argument("--scale", type=float, default=1.0, help="hand-to-robot motion scale")
    p.add_argument("--no-rotation", action="store_true", help="track position only")
    p.add_argument("--rate", type=int, default=None, help="control rate [Hz] (sim 100, real 50)")
    p.add_argument("--max-joint-vel", type=float, default=None,
                   help="[rad/s] (sim 2.0, real 0.5)")
    p.add_argument("--headless", action="store_true", help="no viewer (for tests)")
    p.add_argument("--duration", type=float, default=None, help="stop after N seconds")
    r = p.add_argument_group("real arm (LeRobot rebot_b601_follower)")
    r.add_argument("--robot", choices=["sim", "real"], default="sim")
    r.add_argument("--port", default="/dev/ttyACM0", help="Damiao serial bridge")
    r.add_argument("--robot-id", default="follower", help="calibration file name")
    r.add_argument("--calibration-dir", default=str(Path(__file__).resolve().parents[1]),
                   help="folder with <robot-id>.json (default: repo root)")
    r.add_argument("--max-step-deg", type=float, default=5.0,
                   help="LeRobot max_relative_target per command [deg]")
    g = p.add_argument_group("LeRobot recording")
    g.add_argument("--record", action="store_true", help="record a LeRobot dataset")
    g.add_argument("--task", default="pick up the red cube", help="episode instruction")
    g.add_argument("--repo-id", default="steel_team/rebot_sim_teleop")
    g.add_argument("--dataset-root", default=None,
                   help="output folder (default: datasets/<repo-id name>_<timestamp>)")
    g.add_argument("--fps", type=int, default=25, help="dataset fps (must divide --rate)")
    g.add_argument("--cameras", default="front,wrist,overhead_rgb")
    g.add_argument("--autostart", action="store_true",
                   help="start recording immediately (headless demo / tests)")
    return p.parse_args()


def main():
    args = parse_args()
    real_mode = args.robot == "real"
    if args.rate is None:
        args.rate = 50 if real_mode else 100
    if args.max_joint_vel is None:
        args.max_joint_vel = 0.5 if real_mode else 2.0
    if real_mode and args.record:
        sys.exit("--record renders the simulated cameras; record the real arm with lerobot-record.")
    if args.record and args.rate % args.fps:
        sys.exit(f"--fps {args.fps} must divide --rate {args.rate}")

    sim = RebotSim()
    m, d = sim.model, sim.data
    ik = DiffIK(m, TCP_SITE, ARM_JOINTS, q_rest=HOME_QPOS,
                max_joint_vel=args.max_joint_vel)
    teleop = ClutchTeleop(pos_scale=args.scale, track_rotation=not args.no_rotation)
    mouse = MouseDragTeleop(m)

    if args.input in ("quest", "oculus"):
        source = make_quest_source("webxr" if args.input == "quest" else "oculus",
                                   args.hand, args.ip, args.relay)
    elif args.input == "demo":
        source = DemoSource()
    else:
        source = None  # the viewer's mouse drag is the input

    recorder = None
    if args.record:
        from teleop.lerobot_recorder import LeRobotRecorder
        root = args.dataset_root or os.path.join(
            "datasets", f"{args.repo_id.split('/')[-1]}_{time.strftime('%Y%m%d_%H%M%S')}")
        recorder = LeRobotRecorder(m, args.repo_id, root, args.fps, args.task,
                                   cameras=args.cameras.split(","))
        if args.autostart:
            recorder.start()

    dt = 1.0 / args.rate
    n_sub = max(1, round(dt / m.opt.timestep))
    record_every = args.rate // args.fps if recorder else 0
    sync_every = max(1, round(args.rate / VIEWER_HZ))
    home_pos, home_rot = ik.fk(HOME_QPOS)

    state = dict(q_cmd=HOME_QPOS.copy(), gripper=GRIPPER_MAX,
                 target=(home_pos, home_rot), go_home=False, episode_key=None,
                 prev_rec_button=False)

    real = None
    if real_mode:
        from teleop.real_robot import RealRebot
        real = RealRebot(args.port, args.robot_id, args.calibration_dir, args.max_step_deg)
        q_meas, finger = real.read()
        print(f"[real] connected, measured q = {np.round(np.degrees(q_meas), 1)} deg")
        # Start from where the arm is: nothing moves until you engage.
        state.update(q_cmd=q_meas.copy(), gripper=finger, target=ik.fk(q_meas))
        sim.mirror(q_meas, finger)

    def key_callback(key):
        if key == KEY_UP:
            state["gripper"] = min(GRIPPER_MAX, state["gripper"] + 0.005)
        elif key == KEY_DOWN:
            state["gripper"] = max(0.0, state["gripper"] - 0.005)
        elif key == KEY_HOME:
            state["go_home"] = True
        elif key in (KEY_END, KEY_DELETE):
            state["episode_key"] = key

    def reset_scene():
        sim.reset()
        state.update(q_cmd=HOME_QPOS.copy(), gripper=GRIPPER_MAX,
                     target=(home_pos.copy(), home_rot.copy()))

    def toggle_episode(discard=False):
        if recorder is None:
            print("[record] not recording; start with --record")
        elif discard:
            if recorder.recording:
                recorder.discard()
                reset_scene()
        elif recorder.recording:
            recorder.save()
            reset_scene()
        else:
            recorder.start()

    viewer = None
    if not args.headless:
        viewer = mujoco.viewer.launch_passive(m, d, key_callback=key_callback)
        viewer.cam.lookat[:] = [0.25, 0.0, 0.3]
        viewer.cam.distance = 1.3

    t_start = time.perf_counter()
    next_tick = t_start
    last_print = 0.0
    tick = 0
    try:
        while viewer is None or viewer.is_running():
            now = time.perf_counter() - t_start
            if args.duration is not None and now > args.duration:
                break

            # ---- 1. read the operator -> TCP target --------------------------
            target_pos, target_rot = state["target"]
            if source is not None:
                s = source.read()
                if s.reset:
                    state["go_home"] = True
                if s.record and not state["prev_rec_button"]:
                    toggle_episode()
                state["prev_rec_button"] = s.record
                target_pos, target_rot = teleop.update(s, target_pos, target_rot)
                if s.valid and args.input in ("quest", "oculus"):
                    state["gripper"] = GRIPPER_MAX * (1.0 - np.clip(s.trigger, 0, 1))
                elif args.input == "demo":
                    state["gripper"] = GRIPPER_MAX * (1.0 - s.trigger)
            elif viewer is not None:
                with viewer.lock():
                    target_pos, target_rot = mouse.update(viewer.perturb, target_pos, target_rot)

            if state["episode_key"] is not None:
                toggle_episode(discard=state["episode_key"] == KEY_DELETE)
                state["episode_key"] = None
                target_pos, target_rot = state["target"]

            if state["go_home"]:
                state["go_home"] = False
                target_pos, target_rot = home_pos.copy(), home_rot.copy()
                print("[teleop] going home")
            state["target"] = (target_pos, target_rot)
            sim.set_target(target_pos, target_rot)

            # ---- 2. IK -> joint command -------------------------------------
            track_rot = None if (args.no_rotation or not teleop.track_rotation) else target_rot
            q_cmd, pos_err, rot_err = ik.solve(state["q_cmd"], target_pos, track_rot, dt)
            state["q_cmd"] = q_cmd
            sim.command(q_cmd, state["gripper"])

            # ---- 3. physics (or the real arm) + viewer -----------------------
            if real is not None:
                real.send(q_cmd, state["gripper"])
                sim.mirror(*real.read())
            else:
                for _ in range(n_sub):
                    mujoco.mj_step(m, d)
            if viewer is not None and tick % sync_every == 0:
                viewer.sync()
                mouse.cancel_forces(d)  # the drag moves the target, not the links

            # ---- 4. record --------------------------------------------------
            if recorder is not None and recorder.recording and tick % record_every == 0:
                recorder.add_frame(d, sim.q_arm, sim.gripper, q_cmd, state["gripper"])

            if now - last_print > 0.5:
                last_print = now
                tcp, _ = sim.tcp_pose()
                engaged = "ENGAGED" if (teleop.engaged or mouse.engaged) else "idle   "
                rec = f" REC {recorder.n_frames:4d}" if recorder and recorder.recording else ""
                print(f"[{now:6.1f}s] {engaged} target={np.round(target_pos, 3)} "
                      f"tcp={np.round(tcp, 3)} ik_err={pos_err * 1000:5.1f}mm/"
                      f"{np.degrees(rot_err):4.1f}deg grip={state['gripper'] * 1000:4.1f}mm{rec}")

            # ---- 5. keep real time -------------------------------------------
            tick += 1
            next_tick += dt
            sleep = next_tick - time.perf_counter()
            if sleep > 0:
                time.sleep(sleep)
            else:
                next_tick = time.perf_counter()
    except KeyboardInterrupt:
        pass
    finally:
        if source is not None:
            source.close()
        if real is not None:
            real.close()
        if recorder is not None:
            recorder.close()
        if viewer is not None:
            # MuJoCo's passive viewer can segfault while shutting down GLFW;
            # everything is saved by now, so skip interpreter teardown.
            sys.stdout.flush()
            os._exit(0)


if __name__ == "__main__":
    main()
