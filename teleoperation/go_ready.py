#!/usr/bin/env python3
"""Move the real reBot B601 to the ready pose (gripper pointing down), safely.

  python go_ready.py --port /dev/tty.usbmodem00000000050C1

By default the script keeps running after the move and keeps streaming hold
commands (the motors can go limp when commands stop). Ctrl-C to quit.
"""
import argparse
import time

from lerobot.robots.rebot_b601_follower import RebotB601FollowerRobotConfig, RebotB601Follower

from teleop.ready_move import move_to_ready
from teleop.rebot_real import obs_to_q, q_to_action


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", required=True)
    p.add_argument("--speed", type=float, default=0.3, help="max joint speed [rad/s]")
    p.add_argument("--rate", type=float, default=50.0)
    p.add_argument("--max-step-deg", type=float, default=6.0)
    p.add_argument("--control-mode", default="pos_vel", choices=["pos_vel", "mit"])
    p.add_argument("--vel-deg", type=float, default=30.0, help="pos_vel speed limit [deg/s]")
    p.add_argument("--no-hold", action="store_true", help="exit right after the move")
    p.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    args = p.parse_args()

    robot = RebotB601Follower(RebotB601FollowerRobotConfig(
        port=args.port, max_relative_target=args.max_step_deg,
        control_mode=args.control_mode, pos_vel_velocity=args.vel_deg,
        disable_torque_on_disconnect=False))
    robot.connect()
    try:
        move_to_ready(robot, args.speed, args.rate, confirm=not args.yes)
        if not args.no_hold:
            print("holding; Ctrl-C to quit (the arm may go limp then).")
            obs = robot.get_observation()
            action = q_to_action(obs_to_q(obs), obs["gripper.pos"])
            while True:
                robot.send_action(action)
                time.sleep(1.0 / args.rate)
    except KeyboardInterrupt:
        pass
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
