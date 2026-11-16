#!/usr/bin/env python3
"""Create the lerobot calibration file for the reBot B601 on a NEW computer WITHOUT re-zeroing the motors.

Why: the motor zeros are stored in the Damiao motors themselves (set once with lerobot-calibrate). The calibration
file in ~/.cache/huggingface/lerobot/calibration/robots/rebot_b601_follower/ only holds ids and limits. On a computer
without that file, robot.connect() starts calibration: "move the arm to its ZERO POSITION ... press ENTER" and then
calls set_zero_position() on every motor wherever the arm happens to be. That shifts the joint frame the policies and
config/gripper_limits.json were recorded in. Run this once instead:

    python tools/write_calibration.py --port /dev/ttyACM0      # Linux
    python tools/write_calibration.py --port /dev/tty.usbmodem00000000050C1   # macOS

It writes the file exactly like RebotB601Follower.calibrate() does, minus the set_zero_position() calls, and does not
touch the motors (it does not even open the serial port). It refuses to overwrite an existing file.
"""
import argparse
import sys

from lerobot.motors import MotorCalibration
from lerobot.robots.rebot_b601_follower import RebotB601Follower, RebotB601FollowerRobotConfig


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", required=True, help="arm serial port (only stored in the config; not opened)")
    args = p.parse_args()
    robot = RebotB601Follower(RebotB601FollowerRobotConfig(port=args.port))
    if robot.calibration_fpath.exists():
        sys.exit(f"already exists, not touching it: {robot.calibration_fpath}")
    robot.calibration = {}
    for name, (send_id, _recv) in robot._motor_can_ids.items():
        lo, hi = robot._public_to_motor_limits(name, robot._joint_limits[name])
        robot.calibration[name] = MotorCalibration(id=send_id, drive_mode=0, homing_offset=0,
                                                   range_min=int(lo), range_max=int(hi))
    robot._save_calibration()
    print("wrote", robot.calibration_fpath)


if __name__ == "__main__":
    main()
