#!/usr/bin/env python3
"""lerobot-record with the Leap teleoperator registered. Same CLI as lerobot-record:

  python record_rebot.py \
    --robot.type=rebot_b601_follower --robot.port=/dev/tty.usbmodem00000000050C1 \
    --robot.max_relative_target=3 \
    --teleop.type=leap_ik \
    --dataset.repo_id=<user>/rebot_leap --dataset.single_task="pick up the cube" \
    --display_data=false

The arm is moved to the ready pose automatically after connecting (it asks for Enter).
Add --robot.disable_torque_on_disconnect=false so the arm does not drop when recording ends,
and --robot.control_mode=pos_vel --robot.pos_vel_velocity=150 --robot.max_relative_target=10.
"""
import teleop.lerobot_leap  # noqa: F401  (registers --teleop.type=leap_ik)
from lerobot.robots.rebot_b601_follower import RebotB601Follower
from lerobot.scripts.lerobot_record import main

from teleop.ready_move import move_to_ready

# Move to the ready pose inside this process, right after connecting, so the
# motors never stop receiving commands between a separate script and recording.
_connect = RebotB601Follower.connect


def _connect_and_ready(self, *args, **kwargs):
    _connect(self, *args, **kwargs)
    if not move_to_ready(self):
        raise RuntimeError("arm did not reach the ready pose; not starting")


RebotB601Follower.connect = _connect_and_ready

if __name__ == "__main__":
    main()
