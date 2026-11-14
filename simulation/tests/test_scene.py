"""Checks that the simulated setup still matches the measurements and works.

  uv run --project ../teleoperation tests/test_scene.py     # plain runner
  uv run --project ../teleoperation --with pytest pytest tests/   # or with pytest

Run after changing real_setup.json or scene.py.
"""
import sys
import tempfile
from pathlib import Path

import mujoco
import numpy as np

SIM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SIM))
sys.path.insert(0, str(SIM / "examples"))

from rebot_sim import RealSetupEnv, load_config  # noqa: E402

_ENV = None


def env() -> RealSetupEnv:
    global _ENV
    if _ENV is None:
        _ENV = RealSetupEnv()
    _ENV.reset()
    return _ENV


def test_builds_with_named_parts():
    e = env()
    assert {"cam_far", "cam_corner", "wrist"} <= set(e.cameras)
    assert e.bins == ["bin_0", "bin_1"]
    assert set(e.objects) == {"can", "cup"}
    assert e.model.nu == 7


def test_layout_matches_measurements():
    cfg, e = load_config(), env()
    ws, m = e.ws, e.model
    # Robot (world origin) 38 cm from the right wall's inner face.
    right = m.geom("wall_right")
    assert abs((right.pos[1] + right.size[1]) - (-0.38)) < 1e-6
    # Bin 12 cm tall, against the left wall, 15 cm from the near wall.
    top = max(m.geom(g).pos[2] + m.geom(g).size[2] for g in ("bin_wall_left", "bin_divider_0"))
    assert abs(top - (ws.table_z + cfg["bin"]["height"])) < 1e-6
    # Walls 37 cm.
    for w in ("near", "right", "left"):
        g = m.geom(f"wall_{w}")
        assert abs(g.pos[2] + g.size[2] - (ws.table_z + 0.37)) < 1e-6
    # Camera heights above the table.
    assert abs(m.camera("cam_corner").pos[2] - ws.table_z - 0.60) < 1e-6
    assert abs(m.camera("cam_far").pos[2] - ws.table_z - 0.30) < 1e-6


def test_camera_fov_from_diagonal():
    m = env().model
    assert abs(m.camera("cam_corner").fovy[0] - 49.4) < 0.2   # C920, 75 deg diagonal
    assert abs(m.camera("cam_far").fovy[0] - 71.1) < 0.2      # 100 deg diagonal
    assert abs(m.camera("wrist").fovy[0] - 71.1) < 0.2


def test_objects_rest_upright_on_table():
    e = env()
    e.step(n=50)
    for o in e.objects:
        assert abs(e.object_pos(o)[2] - e.ws.table_z) < 0.003, o
        assert e.object_upright(o), o


def test_randomize_is_reproducible_and_valid():
    e = env()
    e.reset(randomize=True, seed=7)
    a = {o: e.object_pos(o) for o in e.objects}
    e.reset(randomize=True, seed=7)
    for o in e.objects:
        assert np.allclose(a[o], e.object_pos(o), atol=1e-3)
        assert e.object_upright(o)
    assert np.linalg.norm(a["can"][:2] - a["cup"][:2]) > 0.1


def test_pick_and_place_into_both_bins():
    from pick_place import pick_and_place
    e = env()
    for obj, bin_name in (("can", "bin_0"), ("cup", "bin_1")):
        e.reset()
        assert pick_and_place(e, obj, bin_name), f"{obj} -> {bin_name}"


def test_render_cameras():
    e = env()
    for cam in ("cam_corner", "cam_far", "wrist"):
        img = e.render(cam, 160, 120)
        assert img.shape == (120, 160, 3) and img.std() > 5, cam


def test_teleop_scene_flag_and_custom_json():
    import json
    from teleop.rebot_model import RebotSim
    assert RebotSim(scene="real").scene_info.bin_sites == ["bin_0", "bin_1"]
    cfg = load_config()
    cfg["objects"] = cfg["objects"][:1]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "my_setup.json"
        cfg["table"]["texture"] = str(Path(cfg["_dir"]) / cfg["table"]["texture"])
        p.write_text(json.dumps(cfg))
        assert RebotSim(scene=str(p)).scene_info.objects == ["can"]


def test_export_is_standalone():
    import subprocess
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "exported"
        subprocess.run([sys.executable, "-m", "rebot_sim", "export", str(out)], cwd=SIM,
                       check=True, capture_output=True)
        m = mujoco.MjModel.from_xml_path(str(out / "scene.xml"))
        assert m.ncam == env().model.ncam and m.nbody == env().model.nbody


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as exc:  # noqa: BLE001
                failed += 1
                print(f"FAIL {name}: {exc!r}")
    print(f"{'all passed' if not failed else f'{failed} failed'}")
    sys.exit(1 if failed else 0)
