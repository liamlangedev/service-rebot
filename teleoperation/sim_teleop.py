#!/usr/bin/env python3
"""Teleoperate the reBot Arm B601 in MuJoCo.

  uv run sim_teleop.py --input quest            # Quest over USB
  uv run sim_teleop.py --input quest --ip 192.168.1.42   # Quest over Wi-Fi ADB
  uv run sim_teleop.py --input mouse            # no headset: drag the green target
  uv run sim_teleop.py --input demo             # scripted controller motion

Quest controls (right hand by default):
  grip (hold)   clutch: the arm follows your hand while held
  trigger       close the gripper
  A             send the arm home
  B             toggle orientation tracking (position-only is easier at first)

Keyboard in the viewer (all modes): Up/Down arrow opens/closes the gripper
(mouse/demo modes), Home key sends the arm home.
In mouse mode: double-click the green target, then Ctrl + right-drag to move it,
Ctrl + left-drag to rotate it.
"""
import argparse
import time

import mujoco
import mujoco.viewer
import numpy as np

from teleop.ik import DiffIK
from teleop.quest_input import ClutchTeleop, DemoSource, QuestSource
from teleop.rebot_model import ARM_JOINTS, GRIPPER_MAX, HOME_QPOS, TCP_SITE, RebotSim

KEY_UP, KEY_DOWN, KEY_HOME = 265, 264, 268


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", choices=["quest", "mouse", "demo"], default="quest")
    p.add_argument("--hand", choices=["r", "l"], default="r")
    p.add_argument("--ip", default=None, help="Quest IP for wireless ADB (default: USB)")
    p.add_argument("--scale", type=float, default=1.0, help="hand-to-robot motion scale")
    p.add_argument("--no-rotation", action="store_true", help="track position only")
    p.add_argument("--rate", type=float, default=100.0, help="control rate [Hz]")
    p.add_argument("--max-joint-vel", type=float, default=2.0, help="[rad/s]")
    p.add_argument("--headless", action="store_true", help="no viewer (for tests)")
    p.add_argument("--duration", type=float, default=None, help="stop after N seconds")
    p.add_argument("--record", default=None, help="save the session to this .npz")
    return p.parse_args()


def main():
    args = parse_args()
    sim = RebotSim()
    m, d = sim.model, sim.data
    ik = DiffIK(m, TCP_SITE, ARM_JOINTS, q_rest=HOME_QPOS,
                max_joint_vel=args.max_joint_vel)
    teleop = ClutchTeleop(pos_scale=args.scale, track_rotation=not args.no_rotation)

    if args.input == "quest":
        source = QuestSource(hand=args.hand, ip_address=args.ip)
    elif args.input == "demo":
        source = DemoSource()
    else:
        source = None  # the mocap target itself is the input

    dt = 1.0 / args.rate
    n_sub = max(1, round(dt / m.opt.timestep))
    home_pos, home_rot = ik.fk(HOME_QPOS)

    state = dict(q_cmd=HOME_QPOS.copy(), gripper=GRIPPER_MAX,
                 target=(home_pos, home_rot), go_home=False)
    log = {k: [] for k in ["t", "q_cmd", "q_meas", "target_pos", "target_rot", "gripper"]}

    def key_callback(key):
        if key == KEY_UP:
            state["gripper"] = min(GRIPPER_MAX, state["gripper"] + 0.005)
        elif key == KEY_DOWN:
            state["gripper"] = max(0.0, state["gripper"] - 0.005)
        elif key == KEY_HOME:
            state["go_home"] = True

    viewer = None
    if not args.headless:
        viewer = mujoco.viewer.launch_passive(m, d, key_callback=key_callback)
        viewer.cam.lookat[:] = [0.25, 0.0, 0.3]
        viewer.cam.distance = 1.3

    t_start = time.perf_counter()
    next_tick = t_start
    last_print = 0.0
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
                target_pos, target_rot = teleop.update(s, target_pos, target_rot)
                if s.valid and args.input == "quest":
                    state["gripper"] = GRIPPER_MAX * (1.0 - np.clip(s.trigger, 0, 1))
                elif args.input == "demo":
                    state["gripper"] = GRIPPER_MAX * (1.0 - s.trigger)
            else:
                target_pos, target_rot = sim.get_target()  # dragged by the mouse

            if state["go_home"]:
                state["go_home"] = False
                target_pos, target_rot = home_pos.copy(), home_rot.copy()
                print("[teleop] going home")
            state["target"] = (target_pos, target_rot)

            # ---- 2. IK -> joint command -------------------------------------
            track_rot = None if (args.no_rotation or not teleop.track_rotation) else target_rot
            q_cmd, pos_err, rot_err = ik.solve(state["q_cmd"], target_pos, track_rot, dt)
            state["q_cmd"] = q_cmd
            sim.command(q_cmd, state["gripper"])

            # Show the target; in mouse mode the mocap is the input, so leave it.
            if source is not None:
                sim.set_target(target_pos, target_rot)

            # ---- 3. physics + viewer ----------------------------------------
            for _ in range(n_sub):
                mujoco.mj_step(m, d)
            if viewer is not None:
                viewer.sync()

            if args.record:
                log["t"].append(now)
                log["q_cmd"].append(q_cmd)
                log["q_meas"].append(sim.q_arm)
                log["target_pos"].append(target_pos)
                log["target_rot"].append(target_rot)
                log["gripper"].append(state["gripper"])

            if now - last_print > 0.5:
                last_print = now
                tcp, _ = sim.tcp_pose()
                engaged = "ENGAGED" if teleop.engaged else "idle   "
                print(f"[{now:6.1f}s] {engaged} target={np.round(target_pos, 3)} "
                      f"tcp={np.round(tcp, 3)} ik_err={pos_err * 1000:5.1f}mm/"
                      f"{np.degrees(rot_err):4.1f}deg grip={state['gripper'] * 1000:4.1f}mm")

            # ---- 4. keep real time -------------------------------------------
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
        if viewer is not None:
            viewer.close()
        if args.record:
            np.savez(args.record, **{k: np.array(v) for k, v in log.items()})
            print(f"saved {len(log['t'])} samples to {args.record}")


if __name__ == "__main__":
    main()
