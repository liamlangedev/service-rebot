"""Safe joint-space move of a connected reBot follower to READY_QPOS."""
import time

import numpy as np

from teleop.rebot_real import READY_QPOS, joint_space_path, obs_to_q, q_to_action


def move_to_ready(robot, speed=0.3, rate=50.0, follow_deg=3.0, stall_s=5.0,
                  confirm=True, skip_within_deg=3.0) -> bool:
    """Returns True if the arm ends at the ready pose. Advances the path only
    as fast as the arm follows; aborts (holding position) if it stalls."""
    obs = robot.get_observation()
    q0, grip = obs_to_q(obs), obs["gripper.pos"]
    print("current [deg]:", np.degrees(q0).round(1))
    print("ready   [deg]:", np.degrees(READY_QPOS).round(1))
    if np.degrees(np.max(np.abs(q0 - READY_QPOS))) < skip_within_deg:
        print("already at the ready pose")
        return True
    if confirm:
        input("Clear the workspace and keep a hand near the power switch. Enter to move... ")
    path = list(joint_space_path(q0, READY_QPOS, speed, rate))
    i, progress_t = 0, time.time()
    try:
        while i < len(path):
            robot.send_action(q_to_action(path[i], grip))
            time.sleep(1.0 / rate)
            lag = np.degrees(np.max(np.abs(path[i] - obs_to_q(robot.get_observation()))))
            if lag < follow_deg:
                i += 1
                progress_t = time.time()
            elif time.time() - progress_t > stall_s:
                print(f"ABORT: arm is not following (lag {lag:.1f} deg for {stall_s:.0f} s).")
                break
        time.sleep(0.5)
    finally:
        robot.send_action(q_to_action(obs_to_q(robot.get_observation()), grip))  # hold
    err = np.degrees(np.abs(obs_to_q(robot.get_observation()) - READY_QPOS))
    print("residual error [deg]:", err.round(1))
    return bool(err.max() < 5.0)
