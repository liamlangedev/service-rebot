"""python -m rebot_sim {info,view,render,export} [--config my_setup.json]

  info     version, git commit, cameras, bins, objects
  view     interactive MuJoCo viewer (arm holds the home pose)
  render   one PNG per camera (+ top-down and side views) into --out
  export   standalone model for other tools: a folder with scene.xml + assets/,
           or the same folder zipped when the path ends in .zip
"""
import argparse
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import mujoco
import numpy as np

from .env import RealSetupEnv
from .scene import REPO_ROOT, build_real_setup_spec, load_config, scene_version


def git_commit() -> str:
    try:
        out = subprocess.run(["git", "-C", str(REPO_ROOT), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, check=True)
        dirty = subprocess.run(["git", "-C", str(REPO_ROOT), "status", "--porcelain",
                                "simulation", "teleoperation/teleop/rebot_model.py"],
                               capture_output=True, text=True).stdout.strip()
        return out.stdout.strip() + ("+dirty" if dirty else "")
    except Exception:
        return "unknown"


def cmd_info(args):
    env = RealSetupEnv(args.config, objects=not args.no_objects)
    cfg = env.cfg
    print(f"rebot_sim scene version {scene_version(cfg)}  (git {git_commit()})")
    print(f"config   {cfg['_path']}")
    print(f"cameras  " + ", ".join(f"{c} (fovy {env.model.camera(c).fovy[0]:.0f})"
                                    for c in env.cameras))
    print(f"bins     " + ", ".join(f"{b} @ {np.round(env.bin_pos(b), 3)}" for b in env.bins))
    print(f"objects  " + ", ".join(f"{o} @ {np.round(env.object_pos(o), 3)}" for o in env.objects))
    print(f"model    nbody {env.model.nbody}, ngeom {env.model.ngeom}, nu {env.model.nu}, "
          f"timestep {env.model.opt.timestep}")


def cmd_view(args):
    import mujoco.viewer
    env = RealSetupEnv(args.config, objects=not args.no_objects)
    with mujoco.viewer.launch_passive(env.model, env.data) as viewer:
        viewer.cam.lookat[:] = [0.3, 0.1, 0.1]
        viewer.cam.distance, viewer.cam.azimuth, viewer.cam.elevation = 1.6, 200, -35
        while viewer.is_running():
            t0 = time.time()
            env.step()
            viewer.sync()
            time.sleep(max(0.0, env.control_dt - (time.time() - t0)))


def cmd_render(args):
    from PIL import Image
    env = RealSetupEnv(args.config, objects=not args.no_objects)
    w, h = map(int, args.size.lower().split("x"))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for cam in env.cameras:
        Image.fromarray(env.render(cam, w, h)).save(out / f"{cam}.png")
    with mujoco.Renderer(env.model, height=h, width=w) as r:
        free = mujoco.MjvCamera()
        for name, look, dist, az, el in (("topdown", [0.35, 0.11, 0.0], 1.55, 0.0, -89.0),
                                         ("side", [0.35, 0.11, 0.05], 1.5, 90.0, -40.0)):
            free.lookat[:] = look
            free.distance, free.azimuth, free.elevation = dist, az, el
            r.update_scene(env.data, camera=free)
            Image.fromarray(r.render()).save(out / f"{name}.png")
    env.close()
    print(f"rendered {', '.join(env.cameras)}, topdown, side -> {out}")


def _export_folder(spec: mujoco.MjSpec, out: Path) -> Path:
    """Writes scene.xml plus every mesh/texture it uses into `out` (self-contained)."""
    base = Path(spec.modelfiledir)
    roots = {"mesh": base / spec.meshdir, "tex": base / spec.texturedir}
    (out / "assets").mkdir(parents=True, exist_ok=True)
    for kind, items in (("mesh", spec.meshes), ("tex", spec.textures)):
        for item in items:
            if not item.file:  # builtin texture
                continue
            src = Path(item.file)
            src = src if src.is_absolute() else roots[kind] / src
            dst = (out / "assets" / f"{kind}_{item.name}{src.suffix}").resolve()
            shutil.copyfile(src.resolve(), dst)
            item.file = str(dst)
    spec.meshdir = ""
    spec.texturedir = ""
    # to_xml() recompiles, so the files must resolve now; then make them relative.
    text = spec.to_xml().replace(str((out / "assets").resolve()) + "/", "assets/")
    xml = out / "scene.xml"
    xml.write_text(text)
    mujoco.MjModel.from_xml_path(str(xml))  # check it loads on its own
    return xml


def cmd_export(args):
    spec, info = build_real_setup_spec(args.config, with_objects=not args.no_objects)
    spec.compile()  # fail early if broken
    meta = {"scene_version": scene_version(info.config), "commit": git_commit(),
            "cameras": info.cameras, "bins": info.bin_sites, "objects": info.objects,
            "frame": "robot base at origin, +x towards the far edge, +y towards the bin; "
                     f"table top at z={info.workspace.table_z}",
            "actuators": "joint1_pos..joint6_pos (position, rad), gripper_pos (finger opening, m)"}
    out = Path(args.path)
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp) / out.stem if out.suffix == ".zip" else out
        _export_folder(spec, folder)
        (folder / "rebot_sim_info.json").write_text(json.dumps(meta, indent=2))
        if out.suffix == ".zip":
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.make_archive(str(out.with_suffix("")), "zip", folder.parent, folder.name)
    print(f"exported scene v{meta['scene_version']} (commit {meta['commit']}) -> {out}")
    print("load it with: mujoco.MjModel.from_xml_path('<folder>/scene.xml')")


def main():
    p = argparse.ArgumentParser(prog="python -m rebot_sim", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("info", "view", "render", "export"):
        s = sub.add_parser(name)
        s.add_argument("--config", default=None, help="setup JSON (default: the measured setup)")
        s.add_argument("--no-objects", action="store_true", help="leave out the pick objects")
        if name == "render":
            s.add_argument("--out", default="renders")
            s.add_argument("--size", default="640x480", help="WxH")
        if name == "export":
            s.add_argument("path", help="out.zip, or a folder")
    args = p.parse_args()
    {"info": cmd_info, "view": cmd_view, "render": cmd_render, "export": cmd_export}[args.cmd](args)


if __name__ == "__main__":
    main()
