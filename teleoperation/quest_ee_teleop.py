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
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np

from teleop.arm_step import ArmStep
from teleop.ee_control import EEConfig, rot_x
from teleop.quest_input import ControllerSample
from teleop.rebot_model import ARM_JOINTS, GRASP_SITE, GRIPPER_MAX, HOME_QPOS, SCENES, RebotSim

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
    p.add_argument("--rate", type=int, default=None,
                   help="control rate [Hz] (default 100 servo, 200 mit like the real fast loop)")
    p.add_argument("--control", choices=["servo", "mit"], default="servo",
                   help="servo = stiff sim position servos; mit = the real arm's MIT controller "
                        "(teleop/mit_ff.py: soft gains + velocity and gravity feed-forward), "
                        "simulated by teleop/mit_sim.py")
    p.add_argument("--no-velocity-ff", action="store_true",
                   help="with --control mit: send dq_cmd = 0 (compare to see the lag it removes)")
    p.add_argument("--max-joint-vel", type=float, default=None,
                   help="IK joint speed limit [rad/s] (default 2.0 sim, 1.0 real robot)")
    p.add_argument("--strict-rotation", action="store_true",
                   help="never trade orientation for position (by default the tool tilts "
                        "a little when your hand's orientation is out of reach, e.g. "
                        "holding it level close to the table)")
    p.add_argument("--demo", action="store_true", help="scripted controller, no headset")
    p.add_argument("--scene", choices=SCENES, default="default",
                   help="default = Seeed demo table, real = the team's measured workspace")
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
    r = p.add_argument_group(
        "real robot (reBot B601-DM via lerobot, dev/roboCrafy's 200 Hz MIT loop)")
    r.add_argument("--real-robot", action="store_true",
                   help="drive the REAL arm with the controller (no VR; the MuJoCo window "
                        "mirrors the measured pose). Asks before every motion of its own.")
    r.add_argument("--port", default="/dev/ttyACM0", help="Damiao USB-CAN serial port")
    r.add_argument("--robot-id", default="follower",
                   help="calibration file <calibration-dir>/<robot-id>.json")
    r.add_argument("--calibration-dir", default=str(Path(__file__).resolve().parents[1]),
                   help="folder with the calibration json (default: repo root, follower.json)")
    r.add_argument("--fake-hardware", action="store_true",
                   help="with --real-robot: a simulated stand-in for the arm that answers "
                        "the same driver calls (rehearse the whole real path, no hardware)")
    r.add_argument("--kp-scale", type=float, default=1.0, help="MIT arm stiffness factor")
    r.add_argument("--kd-scale", type=float, default=1.0, help="MIT arm damping factor")
    r.add_argument("--ready-speed", type=float, default=0.6,
                   help="peak joint speed of the move to the ready pose [rad/s]")
    r.add_argument("--no-wake", action="store_true",
                   help="do not wake the headset / keep it awake off-head over adb")
    r.add_argument("--no-wrist-guard", dest="wrist_guard", action="store_false",
                   help="let the IK fold the shoulder/elbow when a wrist joint is at its limit")
    r.add_argument("--fingertip-pivot", dest="wrist_pivot", action="store_false",
                   help="rotate the gripper about the fingertips instead of with the wrist "
                        "joints (moves the shoulder/elbow a lot on the reBot)")
    r.add_argument("--yes", action="store_true",
                   help="do not ask before the move to the ready pose (only with --fake-hardware)")
    args = p.parse_args()
    if args.max_joint_vel is None:
        args.max_joint_vel = 1.0 if args.real_robot else 2.0
    if args.real_robot and args.vr:
        p.error("--real-robot does not use the VR scene; use the controller alone "
                "(default) or --passthrough to see the real arm through the headset")
    if args.fake_hardware and not args.real_robot:
        p.error("--fake-hardware only makes sense with --real-robot")
    if args.yes and not args.fake_hardware:
        p.error("--yes is only allowed with --fake-hardware")
    return args


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
        return ControllerSample(valid=True, pos=pos, rot=rot_x(0.3 * np.sin(w * t)),
                                reset=0.5 < t < 0.6,          # A: arm
                                toggle_rot=10.0 < t < 10.1,   # B: disarm
                                clutch=1.0 < t < 9.5,         # grip held
                                trigger=1.0 if 4.5 < t < 5.5 else 0.0,  # precision
                                joystick=(stick_x, stick_y), stamp=time.time())

    def close(self):
        pass


def ee_config(args) -> EEConfig:
    return EEConfig(scale=args.scale, precision_scale=args.precision_scale,
                    grip_speed=args.grip_speed, roll_speed=args.roll_speed,
                    deadzone=args.deadzone, track_rotation=not args.no_hand_rotation)


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
    if args.real_robot:
        from teleop.real_teleop import run_real
        return run_real(args)

    sim = RebotSim(scene=args.scene)
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
    # Same tick as the real arm (teleop/arm_step.py): controller -> wrist pivot ->
    # wrist-limit guard -> guarded IK on the fingertip point -> runaway brake.
    arm = ArmStep(ee_config(args), m, HOME_QPOS, GRIPPER_MAX, HOME_QPOS, args)
    ik, ctrl = arm.ik, arm.ctrl

    mit = None
    if args.control == "mit":
        from teleop.mit_sim import MitSim
        mit = MitSim(sim, velocity_ff=not args.no_velocity_ff)
        print(f"[control] MIT mode (real-arm gains), velocity feed-forward "
              f"{'OFF' if args.no_velocity_ff else 'ON'}, gravity feed-forward ON")
    if args.rate is None:
        args.rate = 200 if mit is not None else 100

    dt = 1.0 / args.rate
    n_sub = max(1, round(dt / m.opt.timestep))
    sync_every = max(1, round(args.rate / VIEWER_HZ))
    home_pos, home_rot = ik.fk(HOME_QPOS)
    state = dict(go_home=False)

    def key_callback(key):
        if key == KEY_UP:
            ctrl.gripper = min(GRIPPER_MAX, ctrl.gripper + 0.005)
        elif key == KEY_DOWN:
            ctrl.gripper = max(0.0, ctrl.gripper - 0.005)
        elif key == KEY_HOME:
            state["go_home"] = True

    viewer = None
    if not (args.headless or args.no_viewer):
        viewer = mujoco.viewer.launch_passive(m, d, key_callback=key_callback)
        viewer.cam.lookat[:] = [0.25, 0.0, 0.3]
        viewer.cam.distance = 1.3

    print(f"[teleop] ready: {ctrl.start_btn} = arm, {ctrl.stop_btn} = disarm, hold grip = move, "
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
            if state["go_home"]:
                state["go_home"] = False
                ctrl.disarm(" (going home)")
                ctrl.resync(home_pos, home_rot)

            # ---- 2. controller + IK -> joints -> physics ----------------------
            q_cmd, _ = arm.update(s, dt)
            pos_err, rot_err = arm.pos_err, arm.rot_err
            target_pos, target_rot = ctrl.target
            sim.set_target(target_pos, target_rot)
            if mit is None:
                sim.command(q_cmd, ctrl.gripper)
                for _ in range(n_sub):
                    mujoco.mj_step(m, d)
            else:
                # Like the real fast loop: build the MIT frame once per tick, the
                # "motors" evaluate the torque law at every physics step.
                d.ctrl[sim.grip_act] = np.clip(ctrl.gripper, 0.0, GRIPPER_MAX)
                mit.set_command(q_cmd, dt)
                for _ in range(n_sub):
                    mit.apply()
                    mujoco.mj_step(m, d)
            if viewer is not None and tick % sync_every == 0:
                viewer.sync()
            if bridge is not None and tick % sync_every == 0:
                bridge.publish(d)
                if tick % (sync_every * 10) == 0:
                    bridge.status(ctrl.status_text() + f"   grip {ctrl.gripper * 1000:.0f} mm",
                                  ctrl.moving)

            if now - last_print > 0.5:
                last_print = now
                tcp = d.site_xpos[m.site(GRASP_SITE).id]
                mode = ("MOVE*  " if ctrl.precise else "MOVE   ") if ctrl.moving else \
                    ("armed  " if ctrl.armed else "off    ")
                track = "" if s.valid else " (controller not tracked)"
                print(f"[{now:6.1f}s] {mode} target={np.round(target_pos, 3)} "
                      f"grasp={np.round(tcp, 3)} ik_err={pos_err * 1000:5.1f}mm/"
                      f"{np.degrees(rot_err):4.1f}deg grip={ctrl.gripper * 1000:4.1f}mm"
                      f" lag={np.degrees(np.max(np.abs(q_cmd - sim.q_arm))):4.1f}deg"
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
