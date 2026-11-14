#!/usr/bin/env python3
"""lerobot-record with the Leap teleoperator registered. Same CLI as lerobot-record:

  python record_rebot.py \
    --robot.type=rebot_b601_follower --robot.port=/dev/tty.usbmodem00000000050C1 \
    --robot.max_relative_target=3 \
    --teleop.type=leap_ik \
    --dataset.repo_id=<user>/rebot_leap --dataset.single_task="pick up the cube" \
    --display_data=false

Extra options (MIT mode): --mit.grip_mode=force_pos|impedance|mit (default force_pos; force = --robot.gripper_torque_ratio;
impedance: --robot.gripper_torque_limit=1.5 moving, --robot.gripper_hold_torque_limit=0.15 holding, N.m),
--mit.grip_err_deg / --mit.grip_kp (mit mode only), --mit.kp_scale, --mit.kd_scale,
--mit.cmd_tau, --mit.ready_speed.

The arm is moved to the ready pose automatically after connecting (it asks for Enter).
Add --robot.disable_torque_on_disconnect=false so the arm does not drop when recording ends,
and --robot.control_mode=mit (default) --dataset.fps=60 --teleop.track_rotation=true.
MIT mode is driven from the 200 Hz thread with velocity + gravity feed-forward (teleop/mit_ff.py).
Leave --robot.max_relative_target unset: the IK and gripper slew limits already bound the speed,
and the clamp warnings are printed at 200 Hz. Leave --robot.pos_vel_velocity unset too (150 deg/s arm, 900 gripper).
"""
import sys
from dataclasses import fields

import teleop.lerobot_leap  # noqa: F401  (registers --teleop.type=leap_ik)
from lerobot.robots.rebot_b601_follower import RebotB601Follower
from lerobot.scripts.lerobot_record import main

from teleop.fast_loop import FastLoop
from teleop.mit_ff import MitFF, MitParams
from teleop.ready_move import move_to_ready


def _pop_mit_params() -> MitParams:
    """Pull --mit.<name>=<value> out of sys.argv so lerobot's parser never sees them."""
    kinds = {f.name: type(getattr(MitParams(), f.name)) for f in fields(MitParams)}
    values, rest = {}, [sys.argv[0]]
    for arg in sys.argv[1:]:
        if arg.startswith("--mit."):
            name, _, val = arg[len("--mit."):].partition("=")
            if name not in kinds or not val:
                raise SystemExit(f"unknown or empty option {arg}; valid: " + ", ".join(f"--mit.{k}=<float>" for k in kinds))
            values[name] = kinds[name](val)
        else:
            rest.append(arg)
    sys.argv[:] = rest
    return MitParams(**values)


MIT_PARAMS = _pop_mit_params()

# Move to the ready pose inside this process, right after connecting, so the
# motors never stop receiving commands between a separate script and recording.
_connect = RebotB601Follower.connect


def _connect_and_ready(self, *args, **kwargs):
    from lerobot.robots.rebot_b601_follower.motor_family import ArmControlMode, GripperControlMode
    from teleop import gripper_limits
    limits = gripper_limits.load()
    if limits is None:
        raise SystemExit(
            "Gripper range not measured. Run first:\n"
            f"  python tools/measure_gripper.py --port {self.config.port}")
    # lerobot's default gripper range (-270..0) is wrong for this arm; use the measured one.
    self._joint_limits["gripper"] = self.config.joint_limits["gripper"] = gripper_limits.bounds(limits)
    if MIT_PARAMS.grip_mode == "mit":
        self.config.gripper_control_mode = GripperControlMode.MIT  # driven by MitFF like the arm
    elif MIT_PARAMS.grip_mode == "impedance":
        # lerobot's force-limited impedance mode: strong torque while moving, weak torque while holding an object
        self.config.gripper_control_mode = GripperControlMode.MIT_IMPEDANCE
        if self.config.gripper_torque_limit is None:
            self.config.gripper_torque_limit = 1.5
        if self.config.gripper_hold_torque_limit is None:
            self.config.gripper_hold_torque_limit = 0.15
    else:
        self.config.gripper_control_mode = GripperControlMode.FORCE_POS  # firmware force limit
    _connect(self, *args, **kwargs)
    mit = MitFF(self, MIT_PARAMS) if self.config.control_mode is ArmControlMode.MIT else None
    loop = FastLoop(self, rate=200.0, mit=mit)  # takes over the bus once the teleoperator starts
    if not loop.gravity_check():
        raise RuntimeError("gravity feed-forward check failed; not starting")
    if not move_to_ready(self, speed=MIT_PARAMS.ready_speed):
        raise RuntimeError("arm did not reach the ready pose; not starting")


RebotB601Follower.connect = _connect_and_ready

if __name__ == "__main__":
    main()
