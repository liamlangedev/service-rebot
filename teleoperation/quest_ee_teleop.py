#!/usr/bin/env python3
"""One-shot Quest end-effector teleop of the reBot Arm B601 in MuJoCo.

Plug in the Quest (USB, developer mode, USB debugging allowed), put it on,
pick up the RIGHT controller, then:

  uv run quest_ee_teleop.py                    # Quest over USB ADB
  uv run quest_ee_teleop.py --ip 172.24.1.43   # Quest over Wi-Fi ADB
  uv run quest_ee_teleop.py --demo             # no headset: scripted controller
  uv run quest_ee_teleop.py --vr               # see the MuJoCo scene IN the headset
  uv run quest_ee_teleop.py --passthrough      # see-through headset, watch the PC screen

The script installs/launches the OculusReader app on the headset over ADB and
opens the MuJoCo viewer. With --vr it instead opens a WebXR page in the Quest
browser (over USB, via adb reverse) that draws the live simulation around you
and streams the controllers back; press "Enter VR" (or "Start AR" for
passthrough) on that page. Controls (right controller):

  A                    arm robot control
  B                    stop and disarm
  hold grip            move the arm with your hand (position, and rotation unless
                       --no-hand-rotation); release it and the arm holds its pose,
                       so you can re-centre your hand, like lifting a mouse
  thumbstick up/down   open / close the gripper (push further = faster)
  thumbstick l/r       rotate (roll) the gripper left / right
  index trigger        precision mode: hand motion and stick rates scaled down

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
from teleop.rebot_model import ARM_JOINTS, GRASP_SITE, GRIPPER_MAX, HOME_QPOS, RebotSim

KEY_UP, KEY_DOWN, KEY_HOME = 265, 264, 268
VIEWER_HZ = 50.0


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ip", default=None, help="Quest IP for Wi-Fi ADB (default: USB)")
    p.add_argument("--hand", choices=["r", "l"], default="r",
                   help="controller to use (l uses X = arm, Y = disarm)")
    p.add_argument("--scale", type=float, default=1.0, help="hand-to-robot motion scale")
    p.add_argument("--precision-scale", type=float, default=0.25,
                   help="motion / stick-rate factor while the index trigger is held")
    p.add_argument("--grip-speed", type=float, default=0.06,
                   help="gripper speed at full thumbstick [m/s] (0.05 m = full travel)")
    p.add_argument("--roll-speed", type=float, default=1.5,
                   help="gripper roll speed at full thumbstick [rad/s]")
    p.add_argument("--no-hand-rotation", action="store_true",
                   help="hand moves position only; orientation changes only via the stick roll")
    p.add_argument("--deadzone", type=float, default=0.3, help="thumbstick deadzone")
    p.add_argument("--rate", type=int, default=100, help="control rate [Hz]")
    p.add_argument("--max-joint-vel", type=float, default=2.0, help="[rad/s]")
    p.add_argument("--strict-rotation", action="store_true",
                   help="never trade orientation for position (by default the tool tilts "
                        "a little when your hand's orientation is out of reach, e.g. "
                        "holding it level close to the table)")
    p.add_argument("--demo", action="store_true", help="scripted controller, no headset")
    p.add_argument("--vr", action="store_true",
                   help="show the simulation in the headset (WebXR page, USB) and read "
                        "the controllers from it instead of the OculusReader app")
    p.add_argument("--passthrough", action="store_true",
                   help="like --vr, but the headset draws nothing: it is see-through, so "
                        "you watch the MuJoCo window on the PC screen while the "
                        "controllers drive the sim")
    p.add_argument("--vr-port", type=int, default=8765, help="port of the VR page server")
    p.add_argument("--no-viewer", action="store_true",
                   help="skip the desktop MuJoCo window (e.g. with --vr)")
    p.add_argument("--headless", action="store_true", help="no viewer (for tests)")
    p.add_argument("--duration", type=float, default=None, help="stop after N seconds")
    return p.parse_args()


def _rodrigues(v):
    """Rotation matrix of the axis-angle vector v."""
    a = np.linalg.norm(v)
    if a < 1e-12:
        return np.eye(3)
    k = v / a
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K


def _rotvec(R):
    """Axis-angle vector of the rotation matrix R."""
    quat, vel = np.empty(4), np.empty(3)
    mujoco.mju_mat2Quat(quat, np.ascontiguousarray(R).reshape(-1))
    mujoco.mju_quat2Vel(vel, quat, 1.0)
    return vel


def _rot_x(a):
    return np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])


class GripClutchMapper:
    """Grip-clutched, incremental hand -> TCP-target mapping.

    While moving, every tick adds the hand's motion since the previous tick
    (times `gain`) to the target, so changing the gain (precision mode) or
    releasing the grip never makes the target jump.
    """

    def __init__(self, workspace: ClutchTeleop, track_rotation: bool = True,
                 smoothing: float = 0.3):
        self.workspace = workspace
        self.track_rotation = track_rotation
        self.smoothing = smoothing
        self._prev = None  # (filtered hand position, hand rotation) of the last tick

    def update(self, s: ControllerSample, moving: bool, gain: float, target_pos, target_rot):
        if not (s.valid and moving):
            self._prev = None
            return target_pos, target_rot
        if self._prev is None:  # grip just pressed: anchor here, no motion yet
            self._prev = (s.pos.copy(), s.rot.copy())
            return target_pos, target_rot
        p_prev, R_prev = self._prev
        p_f = self.smoothing * p_prev + (1 - self.smoothing) * s.pos
        pos = self.workspace.clamp(np.asarray(target_pos) + gain * (p_f - p_prev))
        rot = np.asarray(target_rot)
        if self.track_rotation:
            dR = s.rot @ R_prev.T
            if gain != 1.0:
                dR = _rodrigues(gain * _rotvec(dR))
            rot = dR @ rot
        self._prev = (p_f, s.rot.copy())
        return pos, rot


class DemoController:
    """Fake right controller: arms, moves with the grip held (part of it in
    precision mode), works the gripper and the roll with the stick, disarms."""

    def __init__(self):
        self.t0 = time.time()

    def read(self) -> ControllerSample:
        t = time.time() - self.t0
        w = 2 * np.pi / 6.0
        pos = np.array([0.05 * np.sin(w * t), 0.08 * np.sin(w * t), 0.06 * np.sin(2 * w * t)])
        stick_y = -1.0 if 3.0 < t < 4.0 else (1.0 if 6.0 < t < 7.0 else 0.0)  # close, open
        stick_x = 1.0 if 8.0 < t < 8.5 else 0.0                                # roll right
        return ControllerSample(valid=True, pos=pos, rot=_rot_x(0.3 * np.sin(w * t)),
                                reset=0.5 < t < 0.6,          # A: arm
                                toggle_rot=10.0 < t < 10.1,   # B: disarm
                                clutch=1.0 < t < 9.5,         # grip held
                                trigger=1.0 if 4.5 < t < 5.5 else 0.0,  # precision
                                joystick=(stick_x, stick_y), stamp=time.time())

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


def wait_for_controller(src, hand: str, timeout: float = 30.0, hint: str | None = None):
    """Blocks until the controller pose streams (headset awake, app in front)."""
    t0, last_msg = time.time(), 0.0
    while time.time() - t0 < timeout:
        if src.read().valid:
            print("[quest] controller tracked")
            return True
        if time.time() - last_msg > 3.0:
            last_msg = time.time()
            print(f"[quest] waiting for the {'right' if hand == 'r' else 'left'} controller... "
                  f"({hint or 'headset on, green grid app in front, press a button on the controller'})")
        time.sleep(0.05)
    print("[quest] no controller yet; starting anyway, it will pick up when tracked")
    return False


def main():
    args = parse_args()
    start_btn, stop_btn = ("A", "B") if args.hand == "r" else ("X", "Y")

    sim = RebotSim()
    m, d = sim.model, sim.data

    bridge = None
    if args.vr or args.passthrough:
        from teleop.vr_view import VRBridge, open_on_headset
        bridge = VRBridge(m, port=args.vr_port, extra_sites=[GRASP_SITE])
        bridge.start()
        open_on_headset(args.vr_port, "view=passthrough" if args.passthrough else "")
    if args.demo:
        source = DemoController()
    elif bridge is not None:
        # Don't block: the page needs the live scene before you can enter VR.
        source = bridge.source(args.hand)
        print("[vr] on the headset page press "
              + ("'Start AR' (see-through)" if args.passthrough
                 else "'Enter VR' (or 'Start AR' for passthrough)"))
    else:
        source = open_quest(args.hand, args.ip)
        wait_for_controller(source, args.hand)
    # Control the point between the fingertips, so the fingers go where your hand goes.
    ik = DiffIK(m, GRASP_SITE, ARM_JOINTS, q_rest=HOME_QPOS, max_joint_vel=args.max_joint_vel,
                min_rot_weight=None if args.strict_rotation else 0.05)
    mapper = GripClutchMapper(ClutchTeleop(), track_rotation=not args.no_hand_rotation)

    dt = 1.0 / args.rate
    n_sub = max(1, round(dt / m.opt.timestep))
    sync_every = max(1, round(args.rate / VIEWER_HZ))
    home_pos, home_rot = ik.fk(HOME_QPOS)
    state = dict(q_cmd=HOME_QPOS.copy(), gripper=GRIPPER_MAX, target=(home_pos, home_rot),
                 armed=False, moving=False, precise=False, go_home=False,
                 prev_a=False, prev_b=False)

    def stick(v):
        """Thumbstick value past the deadzone, rescaled to 0..1 with its sign."""
        if abs(v) <= args.deadzone:
            return 0.0
        return float(np.sign(v) * (abs(v) - args.deadzone) / (1.0 - args.deadzone))

    def status_text():
        if not state["armed"]:
            return f"DISARMED - press {start_btn}"
        if not state["moving"]:
            return "ARMED - hold grip to move"
        return "MOVING" + (" (precision)" if state["precise"] else "")

    def key_callback(key):
        if key == KEY_UP:
            state["gripper"] = min(GRIPPER_MAX, state["gripper"] + 0.005)
        elif key == KEY_DOWN:
            state["gripper"] = max(0.0, state["gripper"] - 0.005)
        elif key == KEY_HOME:
            state["go_home"] = True

    viewer = None
    if not (args.headless or args.no_viewer):
        viewer = mujoco.viewer.launch_passive(m, d, key_callback=key_callback)
        viewer.cam.lookat[:] = [0.25, 0.0, 0.3]
        viewer.cam.distance = 1.3

    print(f"[teleop] ready: {start_btn} = arm, {stop_btn} = disarm, hold grip = move, "
          "trigger = precision, stick up/down = open/close, stick left/right = roll")
    t_start = time.perf_counter()
    next_tick, last_print, tick = t_start, 0.0, 0
    try:
        while viewer is None or viewer.is_running():
            now = time.perf_counter() - t_start
            if args.duration is not None and now > args.duration:
                break

            # ---- 1. controller -> arm state, TCP target, gripper ------------
            s = source.read()
            a_pressed, b_pressed = s.reset, s.toggle_rot  # A/B (X/Y on the left hand)
            if a_pressed and not state["prev_a"] and not state["armed"]:
                state["armed"] = True
                print(f"[teleop] {start_btn}: ARMED (hold grip to move)")
            if b_pressed and not state["prev_b"] and state["armed"]:
                state["armed"] = False
                print(f"[teleop] {stop_btn}: DISARMED (arm holds its pose)")
            state["prev_a"], state["prev_b"] = a_pressed, b_pressed

            moving = state["armed"] and s.valid and s.clutch
            precise = moving and s.trigger > 0.5
            changed = moving != state["moving"] or precise != state["precise"]
            state["moving"], state["precise"] = moving, precise
            if changed and state["armed"]:
                print(f"[teleop] {status_text()}")
            gain = args.scale * (args.precision_scale if precise else 1.0)
            target_pos, target_rot = mapper.update(s, moving, gain, *state["target"])

            if state["armed"] and s.valid:
                rate = args.precision_scale if s.trigger > 0.5 else 1.0
                # stick up (+y) opens, down closes; left/right rolls the gripper
                # about its pointing axis (tool x), left = counter-clockwise from behind.
                state["gripper"] = float(np.clip(
                    state["gripper"] + stick(s.joystick[1]) * rate * args.grip_speed * dt,
                    0.0, GRIPPER_MAX))
                roll = stick(s.joystick[0]) * rate * args.roll_speed * dt
                if roll:
                    target_rot = np.asarray(target_rot) @ _rot_x(roll)

            if state["go_home"]:
                state["go_home"] = False
                state["armed"] = False
                target_pos, target_rot = home_pos.copy(), home_rot.copy()
                print("[teleop] going home (DISARMED)")
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
            if bridge is not None and tick % sync_every == 0:
                bridge.publish(d)
                if tick % (sync_every * 10) == 0:
                    bridge.status(status_text() + f"   grip {state['gripper'] * 1000:.0f} mm",
                                  state["moving"])

            if now - last_print > 0.5:
                last_print = now
                tcp = d.site_xpos[m.site(GRASP_SITE).id]
                mode = ("MOVE*  " if state["precise"] else "MOVE   ") if state["moving"] else \
                    ("armed  " if state["armed"] else "off    ")
                track = "" if s.valid else " (controller not tracked)"
                print(f"[{now:6.1f}s] {mode} target={np.round(target_pos, 3)} "
                      f"grasp={np.round(tcp, 3)} ik_err={pos_err * 1000:5.1f}mm/"
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
        if bridge is not None:
            bridge.close()
        # MuJoCo's passive viewer can segfault while shutting down GLFW, and the
        # OculusReader logcat thread is not a daemon: exit hard.
        sys.stdout.flush()
        os._exit(0)


if __name__ == "__main__":
    main()
