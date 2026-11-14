#!/usr/bin/env python3
"""One-shot Quest end-effector teleop of the reBot Arm B601 in MuJoCo.

Plug in the Quest (USB, developer mode, USB debugging allowed), put it on,
pick up the RIGHT controller, then:

  uv run quest_ee_teleop.py                    # Quest over USB ADB
  uv run quest_ee_teleop.py --ip 172.24.1.43   # Quest over Wi-Fi ADB
  uv run quest_ee_teleop.py --demo             # no headset: scripted controller

The script installs/launches the OculusReader app on the headset over ADB and
opens the MuJoCo viewer. Controls (right controller):

  A                 start mimicking: the gripper follows your hand position AND
                    rotation, relative to where your hand was when you pressed A
  B                 stop mimicking: the arm holds its pose (press A again to
                    resume from where your hand is now, like lifting a mouse)
  thumbstick left   close the gripper (hold; push further = faster)
  thumbstick right  open the gripper

Keyboard in the viewer: Home = send the arm home, Up/Down = open/close gripper.
"""
import argparse
import os
import sys
import time

import mujoco
import mujoco.viewer
import numpy as np

from teleop.ik import DiffIK
from teleop.quest_input import ClutchTeleop, ControllerSample
from teleop.rebot_model import ARM_JOINTS, GRIPPER_MAX, HOME_QPOS, TCP_SITE, RebotSim

KEY_UP, KEY_DOWN, KEY_HOME = 265, 264, 268
VIEWER_HZ = 50.0


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ip", default=None, help="Quest IP for Wi-Fi ADB (default: USB)")
    p.add_argument("--hand", choices=["r", "l"], default="r",
                   help="controller to use (l uses X = start, Y = stop)")
    p.add_argument("--scale", type=float, default=1.0, help="hand-to-robot motion scale")
    p.add_argument("--grip-speed", type=float, default=0.06,
                   help="gripper speed at full thumbstick [m/s] (0.05 m = full travel)")
    p.add_argument("--deadzone", type=float, default=0.3, help="thumbstick deadzone")
    p.add_argument("--rate", type=int, default=100, help="control rate [Hz]")
    p.add_argument("--max-joint-vel", type=float, default=2.0, help="[rad/s]")
    p.add_argument("--demo", action="store_true", help="scripted controller, no headset")
    p.add_argument("--headless", action="store_true", help="no viewer (for tests)")
    p.add_argument("--duration", type=float, default=None, help="stop after N seconds")
    return p.parse_args()


class DemoController:
    """Fake right controller: presses A, waves and twists, works the gripper, presses B."""

    def __init__(self):
        self.t0 = time.time()

    def read(self) -> ControllerSample:
        t = time.time() - self.t0
        w = 2 * np.pi / 6.0
        pos = np.array([0.05 * np.sin(w * t), 0.08 * np.sin(w * t), 0.06 * np.sin(2 * w * t)])
        a = 0.4 * np.sin(w * t)  # roll about the forward axis
        rot = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
        stick_x = -1.0 if 3.0 < t % 8 < 4.0 else (1.0 if 6.0 < t % 8 < 7.0 else 0.0)
        return ControllerSample(valid=True, pos=pos, rot=rot,
                                reset=0.5 < t < 0.6,                 # A
                                toggle_rot=10.0 < t < 10.1,          # B
                                joystick=(stick_x, 0.0), stamp=time.time())

    def close(self):
        pass


def open_quest(hand: str, ip: str | None):
    """Connects over ADB, installs + launches the OculusReader app, returns the source."""
    from teleop.quest_input import OculusSource
    try:
        src = OculusSource(hand=hand, ip_address=ip)
    except Exception as e:  # no device, unauthorized, adb server down, ...
        sys.exit(f"[quest] could not connect over ADB: {e}\n"
                 "  - is the Quest plugged in and listed as 'device' by `adb devices`?\n"
                 "  - put the headset on and accept 'Allow USB debugging' if asked")
    print("[quest] connected; OculusReader app launched on the headset")
    return src


def wait_for_controller(src, hand: str, timeout: float = 30.0):
    """Blocks until the controller pose streams (headset awake, app in front)."""
    t0, last_msg = time.time(), 0.0
    while time.time() - t0 < timeout:
        if src.read().valid:
            print("[quest] controller tracked")
            return True
        if time.time() - last_msg > 3.0:
            last_msg = time.time()
            print(f"[quest] waiting for the {'right' if hand == 'r' else 'left'} controller... "
                  "(headset on, green grid app in front, press a button on the controller)")
        time.sleep(0.05)
    print("[quest] no controller yet; starting anyway, it will pick up when tracked")
    return False


def main():
    args = parse_args()
    start_btn, stop_btn = ("A", "B") if args.hand == "r" else ("X", "Y")

    source = DemoController() if args.demo else open_quest(args.hand, args.ip)
    if not args.demo:
        wait_for_controller(source, args.hand)

    sim = RebotSim()
    m, d = sim.model, sim.data
    ik = DiffIK(m, TCP_SITE, ARM_JOINTS, q_rest=HOME_QPOS, max_joint_vel=args.max_joint_vel)
    # The ClutchTeleop "clutch" is driven by our latched A/B state, not the grip.
    mapper = ClutchTeleop(pos_scale=args.scale, track_rotation=True)

    dt = 1.0 / args.rate
    n_sub = max(1, round(dt / m.opt.timestep))
    sync_every = max(1, round(args.rate / VIEWER_HZ))
    home_pos, home_rot = ik.fk(HOME_QPOS)
    state = dict(q_cmd=HOME_QPOS.copy(), gripper=GRIPPER_MAX, target=(home_pos, home_rot),
                 following=False, go_home=False, prev_a=False, prev_b=False)

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

    print(f"[teleop] ready: press {start_btn} to start mimicking, {stop_btn} to stop, "
          "thumbstick left/right = close/open gripper")
    t_start = time.perf_counter()
    next_tick, last_print, tick = t_start, 0.0, 0
    try:
        while viewer is None or viewer.is_running():
            now = time.perf_counter() - t_start
            if args.duration is not None and now > args.duration:
                break

            # ---- 1. controller -> follow state, TCP target, gripper ---------
            s = source.read()
            a_pressed, b_pressed = s.reset, s.toggle_rot  # A/B (X/Y on the left hand)
            if a_pressed and not state["prev_a"] and not state["following"]:
                state["following"] = True
                print(f"[teleop] {start_btn}: mimicking ON")
            if b_pressed and not state["prev_b"] and state["following"]:
                state["following"] = False
                print(f"[teleop] {stop_btn}: mimicking OFF (arm holds its pose)")
            state["prev_a"], state["prev_b"] = a_pressed, b_pressed

            # Feed the mapper a sample whose clutch is our latched follow state;
            # toggle_rot is cleared so B does not also flip rotation tracking.
            follow_sample = ControllerSample(valid=s.valid, pos=s.pos, rot=s.rot,
                                             clutch=state["following"], stamp=s.stamp)
            target_pos, target_rot = mapper.update(follow_sample, *state["target"])

            if s.valid:
                x = s.joystick[0]
                if abs(x) > args.deadzone:
                    # left (x < 0) closes, right (x > 0) opens; speed grows with deflection
                    mag = (abs(x) - args.deadzone) / (1.0 - args.deadzone)
                    state["gripper"] = float(np.clip(
                        state["gripper"] + np.sign(x) * mag * args.grip_speed * dt,
                        0.0, GRIPPER_MAX))

            if state["go_home"]:
                state["go_home"] = False
                state["following"] = False
                target_pos, target_rot = home_pos.copy(), home_rot.copy()
                print("[teleop] going home (mimicking OFF)")
            state["target"] = (target_pos, target_rot)
            sim.set_target(target_pos, target_rot)

            # ---- 2. IK -> joints -> physics --------------------------------
            q_cmd, pos_err, rot_err = ik.solve(state["q_cmd"], target_pos, target_rot, dt)
            state["q_cmd"] = q_cmd
            sim.command(q_cmd, state["gripper"])
            for _ in range(n_sub):
                mujoco.mj_step(m, d)
            if viewer is not None and tick % sync_every == 0:
                viewer.sync()

            if now - last_print > 0.5:
                last_print = now
                tcp, _ = sim.tcp_pose()
                mode = "FOLLOW " if state["following"] else "paused "
                track = "" if s.valid else " (controller not tracked)"
                print(f"[{now:6.1f}s] {mode} target={np.round(target_pos, 3)} "
                      f"tcp={np.round(tcp, 3)} ik_err={pos_err * 1000:5.1f}mm/"
                      f"{np.degrees(rot_err):4.1f}deg grip={state['gripper'] * 1000:4.1f}mm"
                      f"{track}")

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
        source.close()
        # MuJoCo's passive viewer can segfault while shutting down GLFW, and the
        # OculusReader logcat thread is not a daemon: exit hard.
        sys.stdout.flush()
        os._exit(0)


if __name__ == "__main__":
    main()
