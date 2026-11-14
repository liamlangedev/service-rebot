"""View or render the simulated real setup.

  uv run --project ../teleoperation view_real_setup.py              # interactive viewer
  uv run --project ../teleoperation view_real_setup.py --render     # PNG per camera -> renders/
  uv run --project ../teleoperation view_real_setup.py --export-xml scene.xml

To drive the arm in this scene use the teleop apps with `--scene real`, e.g.
  cd ../teleoperation && uv run sim_teleop.py --input mouse --scene real
"""
import argparse
import time
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np

from real_setup import SIM_DIR, build_real_setup_spec

from teleop.rebot_model import ARM_JOINTS, GRIPPER_MAX, HOME_QPOS  # noqa: E402  (path set by real_setup)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", default=None, help="setup JSON (default config/real_setup.json)")
    p.add_argument("--no-objects", action="store_true", help="leave out the can and cup")
    p.add_argument("--render", action="store_true", help="save one PNG per camera and exit")
    p.add_argument("--out", default=str(SIM_DIR / "renders"))
    p.add_argument("--size", default="640x480", help="render size WxH")
    p.add_argument("--settle", type=float, default=0.5, help="sim seconds before rendering")
    p.add_argument("--export-xml", default=None, help="write the compiled scene as MJCF")
    return p.parse_args()


def make(args):
    spec, info = build_real_setup_spec(args.config, with_objects=not args.no_objects)
    model = spec.compile()
    data = mujoco.MjData(model)
    qadr = [model.joint(j).qposadr[0] for j in ARM_JOINTS]
    data.qpos[qadr] = HOME_QPOS
    for j in ARM_JOINTS:
        data.ctrl[model.actuator(f"{j}_pos").id] = data.qpos[model.joint(j).qposadr[0]]
    data.ctrl[model.actuator("gripper_pos").id] = GRIPPER_MAX
    mujoco.mj_forward(model, data)
    return spec, info, model, data


def render_all(model, data, info, out: Path, size: str):
    w, h = map(int, size.lower().split("x"))
    out.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    with mujoco.Renderer(model, height=h, width=w) as r:
        cams = [model.camera(i).name for i in range(model.ncam)]
        for name in cams:
            r.update_scene(data, camera=name)
            Image.fromarray(r.render()).save(out / f"{name}.png")
        # A free bird's-eye view matching the top-down reference photo.
        cam = mujoco.MjvCamera()
        cam.lookat[:] = [0.35, 0.11, 0.0]
        cam.distance, cam.azimuth, cam.elevation = 1.55, 0.0, -89.0
        r.update_scene(data, camera=cam)
        Image.fromarray(r.render()).save(out / "topdown.png")
        cam.lookat[:] = [0.35, 0.11, 0.05]
        cam.distance, cam.azimuth, cam.elevation = 1.5, 90.0, -40.0
        r.update_scene(data, camera=cam)
        Image.fromarray(r.render()).save(out / "side.png")
    print(f"rendered {', '.join(cams)}, topdown, side -> {out}")


def main():
    args = parse_args()
    spec, info, model, data = make(args)
    print(f"cameras: {info.cameras}   place targets: {info.bin_sites}   objects: {info.objects}")

    if args.export_xml:
        Path(args.export_xml).write_text(spec.to_xml())
        print(f"wrote {args.export_xml}")
        return

    if args.render:
        mujoco.mj_step(model, data, nstep=int(args.settle / model.opt.timestep))
        render_all(model, data, info, Path(args.out), args.size)
        return

    with mujoco.viewer.launch_passive(model, data) as viewer:
        viewer.cam.lookat[:] = [0.3, 0.1, 0.1]
        viewer.cam.distance, viewer.cam.azimuth, viewer.cam.elevation = 1.6, 200, -35
        while viewer.is_running():
            t0 = time.time()
            mujoco.mj_step(model, data, nstep=10)
            viewer.sync()
            time.sleep(max(0.0, 10 * model.opt.timestep - (time.time() - t0)))


if __name__ == "__main__":
    main()
