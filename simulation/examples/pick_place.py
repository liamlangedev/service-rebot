"""Scripted top-down pick-and-place in the real setup (template for your own tests).

  uv run --project ../teleoperation examples/pick_place.py                       # can -> bin_0
  uv run --project ../teleoperation examples/pick_place.py --obj cup --bin bin_1 --view
  uv run --project ../teleoperation examples/pick_place.py --random --seed 3     # random start
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rebot_sim import RealSetupEnv  # noqa: E402


def pick_and_place(env: RealSetupEnv, obj: str, bin_name: str, grip_height: float = 0.06) -> bool:
    o = env.object_pos(obj)
    above = o + [0, 0, 0.20]  # grasp point (soft-finger pinch) above the object
    env.move_grasp_to(above)
    env.move_grasp_to(o + [0, 0, grip_height])
    env.set_gripper(env.GRIPPER_CLOSED)
    env.move_grasp_to(above)
    env.move_grasp_to(env.bin_pos(bin_name) + [0, 0, 0.25])
    env.set_gripper(env.GRIPPER_OPEN, secs=1.0)
    env.step(n=100)
    return env.in_bin(obj, bin_name)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--obj", default="can")
    p.add_argument("--bin", default="bin_0")
    p.add_argument("--random", action="store_true", help="random object positions")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--view", action="store_true", help="watch it in the viewer")
    args = p.parse_args()

    env = RealSetupEnv()
    env.reset(randomize=args.random, seed=args.seed)

    if args.view:  # run the same steps, synced to a viewer in real time
        import mujoco.viewer
        viewer = mujoco.viewer.launch_passive(env.model, env.data)
        step = env.step

        def synced(*a, **kw):
            n = kw.pop("n", 1)
            for _ in range(n):
                step(*a, **kw)
                a, kw = (), {}
                viewer.sync()
                time.sleep(env.control_dt)
        env.step = synced

    ok = pick_and_place(env, args.obj, args.bin)
    print(f"{args.obj} at {np.round(env.object_pos(args.obj), 3)}, "
          f"{args.bin} centre {np.round(env.bin_pos(args.bin), 3)}")
    print(f"RESULT: {args.obj} {'IN' if ok else 'NOT in'} {args.bin}")
    if args.view:
        while viewer.is_running():
            env.step()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
