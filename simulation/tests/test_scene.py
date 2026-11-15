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
    # Table at the robot origin (the base plate is part of the robot mesh), and no
    # separate plate geom any more.
    top = m.geom("table_top")
    assert abs(top.pos[2] + top.size[2]) < 1e-9 and ws.table_z == 0.0
    assert not any(m.geom(i).name == "base_plate_geom" for i in range(m.ngeom))


def test_camera_fov_from_diagonal():
    from rebot_sim import camera_fovy
    assert abs(camera_fovy({"fov_diagonal_deg": 75, "aspect": [4, 3]}) - 49.4) < 0.2
    assert abs(camera_fovy({"fov_diagonal_deg": 100, "aspect": [4, 3]}) - 71.1) < 0.2
    assert camera_fovy({"fovy": 42.0, "fov_diagonal_deg": 75}) == 42.0


def test_cameras_match_real_frames():
    """The calibration landmarks, projected through the compiled sim cameras,
    land within 30 px of where they are in the real 1920x1080 frames."""
    sys.path.insert(0, str(SIM / "tools"))
    from calibrate_cameras import CAMERAS, H, W
    e = env()
    for cam, obs in CAMERAS.items():
        c = e.data.cam(cam)
        R, C = c.xmat.reshape(3, 3), c.xpos
        f = H / 2 / np.tan(np.radians(e.model.cam_fovy[e.model.camera(cam).id]) / 2)
        for label, P, px in obs["points"]:
            pc = R.T @ (e.ws.world(*P) - C)
            uv = np.array([W / 2 + f * pc[0] / -pc[2], H / 2 - f * pc[1] / -pc[2]])
            err = np.linalg.norm(uv - px)
            assert err < 30, f"{cam} {label}: {err:.0f} px off"


def test_charuco_board_in_sim():
    """The board drawn in the sim is detected and lies where to_workspace() says
    (texture orientation, board geometry and camera model all agree)."""
    from rebot_sim.charuco import BoardSpec, detect
    import cv2
    cfg = load_config()
    cfg["charuco"] = {**cfg["charuco"], "enabled": True}
    e = RealSetupEnv(cfg, objects=False)
    e.hide_markers()
    board = BoardSpec.from_config(cfg["charuco"])
    for cam in ("cam_corner", "cam_far"):
        img = cv2.cvtColor(e.render(cam, 1920, 1080), cv2.COLOR_RGB2BGR)
        det = detect(board, img)
        # The arm hides part of the board from cam_far.
        assert det is not None and len(det) >= 12 and det.spans_2d(board), cam
        c = e.data.cam(cam)
        R, C = c.xmat.reshape(3, 3), c.xpos
        f = 540 / np.tan(np.radians(e.model.cam_fovy[e.model.camera(cam).id]) / 2)
        for p, px in zip(board.to_workspace(det.obj), det.corners):
            pc = R.T @ (e.ws.world(*p) - C)
            uv = np.array([960 + f * pc[0] / -pc[2], 540 - f * pc[1] / -pc[2]])
            assert np.linalg.norm(uv - px) < 1.5, cam
    e.close()


def test_fake_capture_session_recovers_cameras():
    """Full capture session against the simulated arm and cameras: the board
    calibration must recover the sim's own camera poses and wrist mount."""
    import json
    import shutil
    import subprocess
    name = "_test_session"
    out = SIM / "captures" / name
    try:
        subprocess.run([sys.executable, "-m", "capture.capture_session", "--fake", "--yes",
                        "--pause", "0", "--poses", "reach", "--name", name, "--overwrite"],
                       cwd=SIM, check=True, capture_output=True, stdin=subprocess.DEVNULL,
                       timeout=600)
        cal = json.loads((out / "session.json").read_text())["calibration"]
        for cam in ("cam_corner", "cam_far"):
            assert cal["fixed_cameras"][cam]["vs_sim_mm"] < 5, cam
        wrist = cal["wrist_camera"]
        assert wrist and wrist["spread_mm"] < 2
        want = load_config()["wrist_camera"]["pos"]
        assert np.allclose(wrist["entry"]["pos"], want, atol=0.002)
    finally:
        shutil.rmtree(out, ignore_errors=True)


def test_tape_on_the_table():
    """The yellow tape: a line flush against the base plate's right edge, the
    length of the table, and three marks 12-13 cm from the right wall."""
    e = env()
    m, ws = e.model, e.ws
    line = m.geom("tape_line")
    assert abs((line.pos[1] + line.size[1]) - (-0.10)) < 1e-6      # touches the plate edge
    assert abs(2 * line.size[0] - ws.depth) < 1e-6
    for name, from_wall in (("tape_mark_near", 0.12), ("tape_mark_mid", 0.125),
                            ("tape_mark_far", 0.13)):
        g = m.geom(name)
        right_wall_y = ws.robot_from_left - ws.width
        assert abs((g.pos[1] - g.size[1]) - right_wall_y - from_wall) < 1e-6, name
        assert m.geom_contype[g.id] == 0 and g.pos[2] < 0.001, name


def test_ready_pose_fingertips_11cm_above_table():
    """Measured on the real arm (soft gripper): at the ready pose the fingertips
    are 11 cm above the table."""
    from teleop.rebot_real import READY_QPOS
    e = env()
    e.mirror(READY_QPOS, 0.0)
    tip = e.data.site("fingertip").xpos
    assert abs(tip[2] - e.ws.table_z - 0.11) < 0.01, tip
    e.reset()


def test_wrist_camera_full_resolution():
    e = env()
    assert e.info.camera_resolutions["wrist"] == (1920, 1080)
    assert e.render("wrist").shape == (1080, 1920, 3)
    assert e.render("cam_corner").shape == (480, 640, 3)


def test_objects_rest_upright_on_table():
    e = env()
    e.step(n=50)
    for o in e.objects:
        assert abs(e.object_pos(o)[2] - e.ws.table_z) < 0.003, o
        assert e.object_upright(o), o


def _with_roll():
    import copy
    cfg = copy.deepcopy(load_config())
    cfg["objects"] = [{"name": "towel", "type": "roll", "radius": 0.02, "length": 0.26,
                       "mass": 0.08, "from_left": 0.5, "from_near": 0.45}]
    return RealSetupEnv(cfg)


def test_roll_object_lies_on_table():
    e = _with_roll()
    e.reset(objects={"towel": (0.5, 0.45, 0.3)}, settle=0.5)
    g = e.model.geom("towel_geom").id
    assert abs(e.data.geom_xpos[g][2] - (e.ws.table_z + 0.02)) < 0.003  # axis at radius
    axis = e.data.geom_xmat[g].reshape(3, 3)[:, 2]  # cylinder axis
    assert abs(axis[2]) < 0.05, axis  # horizontal


def test_splat_compositor_draws_object_and_hides_proxy():
    import torch
    from rebot_sim.splat_render import SplatCompositor, SplatObject
    e = _with_roll()
    e.reset(objects={"towel": (0.5, 0.45, 0.0)}, settle=0.3)
    e.hide_markers()
    # a solid red 26 x 4 x 4 cm block of small gaussians in the object's frame
    g = torch.stack(torch.meshgrid(torch.linspace(-0.13, 0.13, 60),
                                   torch.linspace(-0.02, 0.02, 10),
                                   torch.linspace(0.0, 0.04, 10), indexing="ij"), -1).view(-1, 3)
    n = len(g)
    red = SplatObject(g, torch.eye(3).expand(n, 3, 3) * 0.003 ** 2, torch.full((n,), 0.95),
                      torch.tensor([[1.7, -1.7, -1.7]]).expand(n, 3), torch.zeros(n, 0, 3))
    comp = SplatCompositor(e, {"towel": red})
    plain = comp.render("front", 320, 240, splats=False)
    img = comp.render("front", 320, 240)
    changed = np.abs(img.astype(int) - plain).sum(-1) > 60
    assert changed.sum() > 100, changed.sum()
    reddish = img[changed]
    assert (reddish[:, 0] > reddish[:, 1] + 60).mean() > 0.8  # it's the red splat
    # the proxy is hidden from the splat render but drawn when asked for
    assert not np.array_equal(comp.render("front", 320, 240, splats=False, proxies=True), plain)
    comp.close()


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
