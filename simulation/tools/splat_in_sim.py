"""Show the scanned (Gaussian-splat) objects inside the MuJoCo scene.

  ../teleoperation/.venv/bin/python tools/splat_in_sim.py --out splats/in_sim
  ../teleoperation/.venv/bin/python tools/splat_in_sim.py --out splats/in_sim --video

Each object gets a physics proxy with its measured size (bottle: upright cylinder,
towel: lying cylinder) and is drawn with its splat (splats/<name>_object.ply, made
by tools/crop_object_splat.py). The default setup (real_setup.json) is not changed;
the objects are added to a copy of it here. Writes, per camera, the plain sim render
next to the splat render, and with --video a short clip of the arm moving over the
objects (cam_corner).
"""
import argparse
import copy
import sys
from pathlib import Path

import cv2
import numpy as np

SIM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SIM))
from rebot_sim import RealSetupEnv  # noqa: E402
from rebot_sim.scene import load_config  # noqa: E402
from rebot_sim.splat_render import SplatCompositor, SplatObject  # noqa: E402

# name, proxy object (workspace placement), splat file
OBJECTS = [
    ({"name": "bottle_pellegrino", "type": "can", "radius": 0.025, "height": 0.23,
      "mass": 0.3, "rgba": [0.2, 0.55, 0.3, 1]}, (0.58, 0.36, 0.0), "pellegrino_object.ply"),
    ({"name": "bottle_powerade", "type": "can", "radius": 0.025, "height": 0.23,
      "mass": 0.3, "rgba": [0.2, 0.3, 0.6, 1]}, (0.70, 0.50, 0.0), "powerade_object.ply"),
    ({"name": "towel", "type": "roll", "radius": 0.02, "length": 0.26,
      "mass": 0.08, "rgba": [0.9, 0.9, 0.9, 1]}, (0.45, 0.52, 0.5), "towel_object.ply"),
]


def label(img, text):
    img = img.copy()
    cv2.putText(img, text, (12, 34), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4)
    cv2.putText(img, text, (12, 34), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    return img


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--splats", default=str(SIM / "splats"), help="folder with *_object.ply")
    p.add_argument("--out", default=str(SIM / "splats" / "in_sim"))
    p.add_argument("--cameras", default="cam_corner,cam_far,front")
    p.add_argument("--width", type=int, default=960)
    p.add_argument("--video", action="store_true")
    args = p.parse_args()

    cfg = copy.deepcopy(load_config())
    cfg["objects"], splats, where = [], {}, {}
    for obj, pos, ply in OBJECTS:
        f = Path(args.splats) / ply
        if not f.exists():
            print(f"  - {obj['name']}: no {f.name} yet, skipped")
            continue
        o = dict(obj, from_left=pos[0], from_near=pos[1])
        cfg["objects"].append(o)
        splats[obj["name"]] = SplatObject.load(f)
        where[obj["name"]] = pos
        print(f"  + {obj['name']}: {len(splats[obj['name']].opacity)} gaussians")
    if not splats:
        sys.exit("no object splats found")

    env = RealSetupEnv(cfg)
    env.reset(objects=where, settle=0.5)
    env.hide_markers()
    comp = SplatCompositor(env, splats)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    for cam in args.cameras.split(","):
        w = args.width
        rw, rh = env.info.camera_resolutions.get(cam, (640, 480))
        h = int(round(w * rh / rw))
        env_geoms = comp.render(cam, w, h, splats=False, proxies=True)  # physics shapes
        with_splats = comp.render(cam, w, h)
        row = np.hstack([label(env_geoms, "sim proxies"), label(with_splats, "splats")])
        cv2.imwrite(str(out / f"{cam}.jpg"), row[..., ::-1])
        cv2.imwrite(str(out / f"{cam}_splats.jpg"), with_splats[..., ::-1])
        print(f"  wrote {out / cam}.jpg")

    if args.video:
        # sweep the gripper over the objects and back, rendering cam_corner
        cam, w = "cam_corner", 640
        rw, rh = env.info.camera_resolutions.get(cam, (640, 480))
        h = int(round(w * rh / rw))
        vw = cv2.VideoWriter(str(out / "sweep.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), 15, (w, h))
        names = list(where)
        for name in names + names[:1]:
            target = env.object_pos(name) + np.array([0, 0, 0.30])
            for _ in range(20):
                cur = env.grasp_pos()
                step = target - cur
                if np.linalg.norm(step) < 0.01:
                    break
                env.move_grasp_to(cur + step * min(1.0, 0.04 / np.linalg.norm(step)), speed=0.3,
                                 settle=0.0)
                vw.write(comp.render(cam, w, h)[..., ::-1])
        vw.release()
        print(f"  wrote {out / 'sweep.mp4'}")
    comp.close()
    env.close()


if __name__ == "__main__":
    main()
