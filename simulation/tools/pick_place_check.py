"""Scripted pick-and-place in the real-setup scene (no headset needed).

Grasps an object top-down with the IK, carries it over a bin compartment and
drops it, then reports whether it landed inside. A quick physics/reach sanity
check of the scene, and a template for scripted demos.

  uv run --project ../teleoperation tools/pick_place_check.py                  # can -> bin_0
  uv run --project ../teleoperation tools/pick_place_check.py --obj cup --bin bin_1 --view
"""
import argparse
import sys
import time
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from real_setup import build_real_setup_spec  # noqa: E402

from teleop.ik import DiffIK  # noqa: E402
from teleop.rebot_model import ARM_JOINTS, GRASP_SITE, GRIPPER_MAX, HOME_QPOS  # noqa: E402

# Tool (end_link +x) pointing straight down, fingers closing along world y.
TOP_DOWN = np.column_stack([[0, 0, -1], [0, 1, 0], [1, 0, 0]]).astype(float)
RATE = 100


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--obj", default="can")
    p.add_argument("--bin", default="bin_0")
    p.add_argument("--grip-height", type=float, default=0.06,
                   help="grasp point height above the object's base [m]")
    p.add_argument("--speed", type=float, default=0.15, help="TCP speed [m/s]")
    p.add_argument("--view", action="store_true", help="watch it in the viewer")
    args = p.parse_args()

    spec, info = build_real_setup_spec()
    m = spec.compile()
    d = mujoco.MjData(m)
    qadr = np.array([m.joint(j).qposadr[0] for j in ARM_JOINTS])
    arm_act = np.array([m.actuator(f"{j}_pos").id for j in ARM_JOINTS])
    grip_act = m.actuator("gripper_pos").id
    d.qpos[qadr] = HOME_QPOS
    d.ctrl[arm_act] = HOME_QPOS
    d.ctrl[grip_act] = GRIPPER_MAX
    mujoco.mj_forward(m, d)

    ik = DiffIK(m, GRASP_SITE, ARM_JOINTS, q_rest=HOME_QPOS, max_joint_vel=1.5,
                rot_weight=0.5)
    obj = m.body(args.obj).id
    table_z = info.workspace.table_z
    n_sub = round(1.0 / RATE / m.opt.timestep)

    viewer = None
    if args.view:
        viewer = mujoco.viewer.launch_passive(m, d)

    state = {"q": HOME_QPOS.copy(), "grip": GRIPPER_MAX, "worst": 0.0}

    def step(n=1):
        for _ in range(n):
            d.ctrl[arm_act] = state["q"]
            d.ctrl[grip_act] = state["grip"]
            mujoco.mj_step(m, d, nstep=n_sub)
            if viewer is not None:
                viewer.sync()
                time.sleep(1.0 / RATE)

    def move_to(target, settle=0.3):
        start = ik.fk(state["q"])[0]
        n = max(1, int(np.linalg.norm(target - start) / args.speed * RATE))
        for s in np.linspace(0, 1, n + 1)[1:]:
            state["q"], err, _ = ik.solve(state["q"], start + s * (target - start), TOP_DOWN,
                                          1.0 / RATE)
            state["worst"] = max(state["worst"], err)
            step()
        step(int(settle * RATE))
        return np.linalg.norm(d.site(GRASP_SITE).xpos - target)

    def grip(value, secs=0.6):
        state["grip"] = value
        step(int(secs * RATE))

    step(int(0.5 * RATE))  # let objects settle
    o = d.xpos[obj].copy()
    above = np.array([o[0], o[1], table_z + 0.25])
    grasp = np.array([o[0], o[1], o[2] + args.grip_height])
    b = d.site(args.bin).xpos.copy()
    over_bin = np.array([b[0], b[1], table_z + 0.30])

    log = []
    log.append(("above object", move_to(above)))
    log.append(("descend", move_to(grasp)))
    grip(0.0)
    log.append(("lift", move_to(above)))
    lifted = d.xpos[obj][2] - o[2]
    log.append(("over bin", move_to(over_bin)))
    grip(GRIPPER_MAX, 1.0)
    log.append(("retreat", move_to(over_bin + [0, 0, 0.05])))
    step(int(1.0 * RATE))

    for name, err in log:
        print(f"  {name:13s} reached within {err * 1000:5.1f} mm")
    final = d.xpos[obj]
    half = m.site(args.bin).size
    inside = (abs(final[0] - b[0]) < half[0] + 0.005 and abs(final[1] - b[1]) < half[1] + 0.005
              and final[2] < table_z + 0.15)
    print(f"  final object pos {np.round(final, 3)}  {args.bin} centre {np.round(b, 3)}")
    print(f"RESULT: {args.obj} {'IN' if inside else 'NOT in'} {args.bin} (lifted {lifted * 100:.0f} cm)")
    if viewer is not None:
        while viewer.is_running():
            step()
    return 0 if inside else 1


if __name__ == "__main__":
    sys.exit(main())
