"""Print, per episode, where the TCP is around the grasp (forward kinematics in MuJoCo).

    teleoperation/.venv/bin/python training_gripper/analyze_grasps.py <dataset_root>

<dataset_root> is a local copy of RoboCrafty/rebot_sort_v1 (only meta/ and data/ are read).
Columns: tilt of the tool from straight down at the close, gripper state 1 s after the
close, then TCP x,y [m] and z [cm] at frame offsets relative to the close.
"""

from __future__ import annotations

import sys
from pathlib import Path

import mujoco
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "teleoperation"))
sys.path.insert(0, str(HERE))

from segments import episode_arrays, find_grasp, load_frames  # noqa: E402
from teleop.rebot_model import RebotSim  # noqa: E402

OFFSETS = (-60, -45, -30, -15, 0, 15, 30, 45, 60)


def main(root: str) -> None:
    sim = RebotSim(scene="real")

    def tcp(q_deg):
        sim.data.qpos[sim.arm_qadr] = np.radians(q_deg)
        mujoco.mj_forward(sim.model, sim.data)
        return sim.tcp_pose()

    for ep, (state, action) in episode_arrays(load_frames(root)).items():
        g = find_grasp(ep, action)
        if g is None:
            print(ep, "no grasp")
            continue
        cols = []
        for dt in OFFSETS:
            t = min(max(g.t_close + dt, 0), len(state) - 1)
            p, _ = tcp(state[t, :6])
            cols.append(f"{dt:+d}:{p[0]:.2f},{p[1]:+.2f},{p[2] * 100:4.1f}")
        _, R = tcp(state[g.t_close, :6])
        tilt = np.degrees(np.arccos(np.clip(-R[2, 2], -1, 1)))
        g30 = state[min(g.t_close + 30, len(state) - 1), 6]
        flag = "" if g.clean else f" REGRASP x{g.n_closes}"
        print(f"{ep:2d} tilt={tilt:3.0f} g+30={g30:5.0f} " + " ".join(cols) + flag)


if __name__ == "__main__":
    main(sys.argv[1])
