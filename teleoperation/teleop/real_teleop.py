"""quest_ee_teleop.py --real-robot: the Quest controller drives the REAL reBot B601.

Uses dev/roboCrafy's hardware path unchanged, in the order of record_rebot.py:
  connect (measured gripper range, MIT arm, force-limited gripper, team
  calibration, never re-zeroes) -> MitFF + 200 Hz FastLoop (velocity + gravity
  feed-forward) -> gravity_check -> move_to_ready (asks first) -> teleop.

The 200 Hz step runs the same controller as the simulator (teleop/ee_control.py:
A arm, B disarm, hold grip to move, trigger = precision, stick = gripper/roll),
then dev/roboCrafy's singularity-guarded IK on the fingertip (grasp) point.
The main thread mirrors the measured pose in the MuJoCo window and prints status.
"""
import os
import sys
import time
from pathlib import Path

import mujoco
import numpy as np

from teleop import gripper_limits
from teleop.ee_control import EEController
from teleop.ik import DiffIK
from teleop.rebot_model import ARM_JOINTS, GRASP_SITE, GRIPPER_MAX, RebotSim

RUNAWAY_M = 0.05  # target further than this from the arm -> snap the target back


def finger_to_deg(finger_m: float) -> float:
    from teleop.rebot_real import gripper_from_closing
    return gripper_from_closing(1.0 - float(np.clip(finger_m / GRIPPER_MAX, 0.0, 1.0)))


def deg_to_finger(deg: float) -> float:
    from teleop.rebot_real import GRIPPER_CLOSED_DEG, GRIPPER_OPEN_DEG
    closing = (deg - GRIPPER_OPEN_DEG) / (GRIPPER_CLOSED_DEG - GRIPPER_OPEN_DEG)
    return GRIPPER_MAX * (1.0 - float(np.clip(closing, 0.0, 1.0)))


class RealArmStep:
    """FastLoop step function: controller -> EEController -> guarded IK -> action (deg)."""

    def __init__(self, source, ctrl_cfg, model, q_start, gripper_deg, args):
        from teleop.rebot_real import READY_QPOS
        self.source = source
        self.ik = DiffIK(model, GRASP_SITE, ARM_JOINTS, q_rest=READY_QPOS,
                         max_joint_vel=args.max_joint_vel,
                         min_rot_weight=None if args.strict_rotation else 0.05)
        self.q = np.array(q_start, dtype=float)
        pos, rot = self.ik.fk(self.q)
        self.ctrl = EEController(ctrl_cfg, pos, rot, gripper=deg_to_finger(gripper_deg),
                                 hand=args.hand)
        self.blocked = False
        self.last_action = None

    def step(self, dt: float) -> dict:
        from teleop.rebot_real import guarded_solve, q_to_action
        s = self.source.read()
        target_pos, target_rot, finger = self.ctrl.update(s, dt)
        q, pos_err, _, blocked = guarded_solve(self.ik, self.q, target_pos, target_rot, dt)
        if blocked and not self.blocked:
            print("[real] IK step refused: it would move into a singularity (arm holds)")
        self.blocked = blocked
        self.q = q
        # Safety brake: never let the target run away from what the arm can do.
        arm_pos, arm_rot = self.ik.fk(q)
        if np.linalg.norm(np.asarray(target_pos) - arm_pos) > RUNAWAY_M:
            self.ctrl.resync(arm_pos, target_rot)
        self.last_action = q_to_action(q, finger_to_deg(finger))
        return self.last_action

    def resync(self, joints_deg: dict) -> None:
        """Called by FastLoop after a stop / return-to-ready: re-anchor on the arm."""
        from teleop.rebot_real import JOINT_NAMES
        self.q = np.radians([joints_deg[f"{n}.pos"] for n in JOINT_NAMES])
        pos, rot = self.ik.fk(self.q)
        self.ctrl.disarm(" (resync)")
        self.ctrl.resync(pos, rot, deg_to_finger(joints_deg["gripper.pos"]))


def connect_robot(args):
    limits = gripper_limits.load()
    if limits is None:
        sys.exit("[real] gripper range not measured. Run first:\n"
                 f"  uv run tools/measure_gripper.py --port {args.port}")
    lo, hi = gripper_limits.bounds(limits)
    from lerobot.robots.rebot_b601_follower import (RebotB601Follower,
                                                    RebotB601FollowerRobotConfig)
    from lerobot.robots.rebot_b601_follower.motor_family import (ArmControlMode,
                                                                 GripperControlMode)
    calib = Path(args.calibration_dir) / f"{args.robot_id}.json"
    if not args.fake_hardware and not calib.exists():
        sys.exit(f"[real] calibration file {calib} not found (use --calibration-dir / "
                 "--robot-id). Not connecting: lerobot would start a motor re-zeroing.")
    config = RebotB601FollowerRobotConfig(
        port=args.port, id=args.robot_id, calibration_dir=Path(args.calibration_dir),
        joint_limits={"gripper": (lo, hi)},       # measured, not lerobot's -270..0
        control_mode=ArmControlMode.MIT,
        gripper_control_mode=GripperControlMode.FORCE_POS,
        disable_torque_on_disconnect=False)       # the arm must not drop on exit
    if args.fake_hardware:
        from teleop.fake_rebot import FakeRebotFollower
        robot = FakeRebotFollower(config, limits)
        print("[real] FAKE HARDWARE: simulated stand-in for the arm (nothing physical moves)")
    else:
        robot = RebotB601Follower(config)
    robot.connect(calibrate=False)  # never re-zero the motors from here
    return robot


def run_real(args):
    from teleop.fast_loop import FastLoop
    from teleop.mit_ff import MitFF, MitParams
    from teleop.ready_move import move_to_ready
    from teleop.rebot_real import JOINT_NAMES, obs_to_q

    from quest_ee_teleop import ee_config, open_quest, wait_for_controller

    print("=" * 72)
    print(" REAL ROBOT teleop" + (" (FAKE HARDWARE)" if args.fake_hardware else ""))
    print("  - clear the workspace, keep a hand near the arm's power switch")
    print("  - the arm moves to the ready pose first (asks for Enter)")
    print("  - A = arm, B = disarm/hold, HOLD GRIP to move, trigger = precision")
    print("  - Ctrl-C = stop: the arm holds its pose (torque stays ON; support it")
    print("    before switching the power off)")
    print("=" * 72)

    sim = RebotSim()
    m, d = sim.model, sim.data

    # Controller first, so a missing headset fails before anything moves.
    bridge = None
    if args.demo:
        source = None  # created right before teleop starts (its script is timed)
    elif args.passthrough:
        from teleop.vr_view import VRBridge, open_on_headset
        bridge = VRBridge(m, port=args.vr_port, extra_sites=[GRASP_SITE])
        bridge.start()
        open_on_headset(args.vr_port, "view=passthrough")
        source = bridge.source(args.hand)
        print("[vr] on the headset page press 'Start AR' to see the real arm")
    else:
        source = open_quest(args.hand, args.ip)
        wait_for_controller(source, args.hand)

    robot = connect_robot(args)
    loop = None
    viewer = None
    try:
        mit = MitFF(robot, MitParams(kp_scale=args.kp_scale, kd_scale=args.kd_scale,
                                     ready_speed=args.ready_speed))
        loop = FastLoop(robot, rate=200.0, mit=mit)
        print("[real] gravity feed-forward check (the arm holds its pose)...")
        if not loop.gravity_check():
            raise RuntimeError("gravity feed-forward check failed; not starting")
        if not move_to_ready(robot, speed=args.ready_speed, confirm=not args.yes):
            raise RuntimeError("arm did not reach the ready pose; not starting")

        obs = robot.get_observation()
        if args.demo:
            from quest_ee_teleop import DemoController
            source = DemoController()
        step = RealArmStep(source, ee_config(args), m, obs_to_q(obs), obs["gripper.pos"], args)
        ctrl = step.ctrl
        loop.start(step.step)
        print(f"[real] teleop running at 200 Hz: press {ctrl.start_btn} to arm, "
              "hold grip to move")

        if not (args.headless or args.no_viewer):
            import mujoco.viewer
            viewer = mujoco.viewer.launch_passive(m, d)
            viewer.cam.lookat[:] = [0.25, 0.0, 0.3]
            viewer.cam.distance = 1.3

        t0, last_print = time.perf_counter(), 0.0
        while viewer is None or viewer.is_running():
            now = time.perf_counter() - t0
            if args.duration is not None and now > args.duration:
                break
            obs = robot.get_observation()  # cached by the fast loop
            q_meas = obs_to_q(obs)
            sim.mirror(q_meas, deg_to_finger(obs["gripper.pos"]))
            sim.set_target(*ctrl.target)
            if viewer is not None:
                viewer.sync()
            if bridge is not None:
                bridge.status(ctrl.status_text() + f"   grip {ctrl.gripper * 1000:.0f} mm",
                              ctrl.moving)
            if now - last_print > 0.5:
                last_print = now
                a = step.last_action
                lag = (max(abs(a[f"{n}.pos"] - obs[f"{n}.pos"]) for n in JOINT_NAMES)
                       if a else 0.0)
                grasp = d.site_xpos[m.site(GRASP_SITE).id]
                mode = ("MOVE*  " if ctrl.precise else "MOVE   ") if ctrl.moving else \
                    ("armed  " if ctrl.armed else "off    ")
                track = "" if ctrl.last_sample.valid else " (controller not tracked)"
                print(f"[{now:6.1f}s] {mode} target={np.round(ctrl.target[0], 3)} "
                      f"grasp={np.round(grasp, 3)} grip={ctrl.gripper * 1000:4.1f}mm "
                      f"lag={lag:4.1f}deg loop={loop.hz:3.0f}Hz{track}")
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("\n[real] Ctrl-C: stopping")
    finally:
        try:
            if source is not None:
                source.close()
        except Exception:
            pass
        if bridge is not None:
            bridge.close()
        # FastLoop's disconnect: stop the 200 Hz thread, command the measured pose
        # (hold), save /tmp/fast_loop_log.npz, then close the bus with torque ON.
        robot.disconnect()
        print("[real] disconnected; the arm holds with torque ON. Support it before power-off.")
        sys.stdout.flush()
        os._exit(0)
