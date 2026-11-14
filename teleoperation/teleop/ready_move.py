"""Safe joint-space move of a connected reBot follower to READY_QPOS."""
import time

import numpy as np

from teleop.rebot_real import GRIPPER_CLOSED_DEG, GRIPPER_OPEN_DEG, READY_QPOS, joint_space_path, obs_to_q, q_to_action


def move_to_ready(robot, speed=0.6, rate=50.0, max_lag_deg=20.0,
                  confirm=True, skip_within_deg=3.0) -> bool:
    """Returns True if the arm ends at the ready pose."""
    obs = robot.get_observation()
    q0, grip = obs_to_q(obs), obs["gripper.pos"]
    print("current [deg]:", np.degrees(q0).round(1))
    print(f"gripper [deg]: {grip:.1f} (measured open {GRIPPER_OPEN_DEG:.0f}, closed {GRIPPER_CLOSED_DEG:.0f})")
    print("ready   [deg]:", np.degrees(READY_QPOS).round(1))
    if np.degrees(np.max(np.abs(q0 - READY_QPOS))) < skip_within_deg:
        print("already at the ready pose")
        return True
    if confirm:
        input("Clear the workspace and keep a hand near the power switch. Enter to move... ")
    path = list(joint_space_path(q0, READY_QPOS, speed, rate))
    t0, lag_since = time.time(), None
    try:
        # Time-based trajectory: the setpoint moves on schedule, the motor's own
        # loop tracks it. Only a large, persistent lag aborts.
        while True:
            i = int((time.time() - t0) * rate)
            robot.send_action(q_to_action(path[min(i, len(path) - 1)], grip))
            time.sleep(1.0 / rate)
            if i >= len(path) + rate:  # one second to settle at the end
                break
            lag = np.degrees(np.max(np.abs(path[min(i, len(path) - 1)] - obs_to_q(robot.get_observation()))))
            if lag > max_lag_deg:
                lag_since = lag_since or time.time()
                if time.time() - lag_since > 1.5:
                    print(f"ABORT: arm lags the trajectory by {lag:.0f} deg. Holding.")
                    break
            else:
                lag_since = None
    finally:
        robot.send_action(q_to_action(obs_to_q(robot.get_observation()), grip))  # hold
    err = np.degrees(np.abs(obs_to_q(robot.get_observation()) - READY_QPOS))
    print("residual error [deg]:", err.round(1))
    return bool(err.max() < 5.0)
