"""MuJoCo replica of the team's real reBot B601 workspace.

Takes the teleop-ready reBot model (teleoperation/teleop/rebot_model.py) and
replaces Seeed's demo table and cubes with the measured hackathon setup from
real_setup.json (next to this file):

  * the wood table (texture cropped from the photos) and the floor below it
  * the two green clamps on the robot's base plate (the plate itself is part of
    the robot mesh: 20 x 14 x 1.4 cm, bottom at the robot origin)
  * cardboard walls behind and right of the robot, black board on the left
  * the yellow tape on the table (a line next to the robot and three marks)
  * the white foam bin with its compartments (place targets `bin_0`, `bin_1`, ...)
  * the two external cameras (`cam_far`, `cam_corner`) at their measured spots
  * placeholder pick objects (a can and a paper cup), or your own meshes

The robot base stays at the world origin (+x = towards the far edge, +y = towards
the bin side), so the IK, teleop mapping and LeRobot recording work unchanged.
The table top is at z = 0 (the robot's base plate stands on it), the same frame
as base_link in the ROS stack.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import mujoco
import numpy as np

PKG_DIR = Path(__file__).resolve().parent
REPO_ROOT = PKG_DIR.parents[1]
TELEOP_DIR = REPO_ROOT / "teleoperation"
if str(TELEOP_DIR) not in sys.path:
    sys.path.insert(0, str(TELEOP_DIR))

from teleop.rebot_model import _lookat_quat, build_spec  # noqa: E402

DEFAULT_CONFIG = PKG_DIR / "real_setup.json"

# Bodies and geoms of Seeed's demo scene that the real setup replaces.
_DEMO_BODIES = ["task_table", "red_cube", "blue_block", "yellow_cylinder"]
_DEMO_GEOMS = ["floor"]

_COLORS = {
    "cardboard": [0.70, 0.58, 0.44, 1],
    "black": [0.07, 0.07, 0.08, 1],
    "foam": [0.96, 0.96, 0.95, 1],
    "plate": [0.11, 0.11, 0.12, 1],
    "clamp": [0.10, 0.50, 0.40, 1],
    "floor": [0.42, 0.38, 0.30, 1],
    "camera": [0.05, 0.05, 0.05, 1],
}

# Contact settings for graspable things (same as Seeed's demo objects, which
# the gripper's collision meshes are tuned for).
_GRASP_CONTACT = dict(condim=6, friction=[1.5, 0.04, 0.01],
                      solref=[0.002, 1], solimp=[0.98, 0.995, 0.0005, 0.5, 2])
_STATIC_CONTACT = dict(condim=3, friction=[1.0, 0.01, 0.001])


def load_config(path: Path | str | None = None) -> dict:
    """Reads a setup JSON. Relative file paths inside it (texture, meshes) are
    resolved against the folder of that JSON."""
    path = Path(path or DEFAULT_CONFIG).resolve()
    with open(path) as f:
        cfg = json.load(f)
    cfg["_dir"] = str(path.parent)
    cfg["_path"] = str(path)
    return cfg


def scene_version(cfg: dict | None = None) -> str:
    return (cfg or load_config()).get("version", "unversioned")


def _resolve(cfg_or_dir, rel: str) -> Path:
    base = Path(cfg_or_dir.get("_dir", PKG_DIR)) if isinstance(cfg_or_dir, dict) else Path(cfg_or_dir)
    p = Path(rel)
    return p if p.is_absolute() else (base / p).resolve()


@dataclass
class Workspace:
    """Converts workspace coordinates (from_left, from_near, height) to world."""
    width: float
    depth: float
    robot_from_left: float
    robot_from_near: float
    table_z: float  # world z of the table top

    def world(self, from_left: float, from_near: float, height: float = 0.0) -> np.ndarray:
        return np.array([from_near - self.robot_from_near,
                         self.robot_from_left - from_left,
                         self.table_z + height])

    def from_world(self, p) -> np.ndarray:
        """World point -> workspace (from_left, from_near, height)."""
        return np.array([self.robot_from_left - p[1], p[0] + self.robot_from_near,
                         p[2] - self.table_z])

    @staticmethod
    def half(lo: float, hi: float) -> float:
        return abs(hi - lo) / 2


@dataclass
class SceneInfo:
    """Names added to the model, handy for tasks and scripted policies."""
    workspace: Workspace
    config: dict = field(default_factory=dict)
    bin_sites: list[str] = field(default_factory=list)
    cameras: list[str] = field(default_factory=list)
    objects: list[str] = field(default_factory=list)
    # Image size (width, height) of the real camera, where the config gives one.
    camera_resolutions: dict[str, tuple[int, int]] = field(default_factory=dict)


def apply_real_setup(spec: mujoco.MjSpec, cfg: dict | None = None,
                     with_objects: bool = True) -> SceneInfo:
    cfg = cfg or load_config()
    _remove_demo_scene(spec)

    ws_cfg, rob = cfg["workspace"], cfg["robot"]
    ws = Workspace(ws_cfg["width"], ws_cfg["depth"], rob["from_left"], rob["from_near"],
                   table_z=0.0)
    info = SceneInfo(ws, cfg)

    if rob.get("yaw_deg"):
        q = np.empty(4)
        mujoco.mju_euler2Quat(q, [0, 0, np.radians(rob["yaw_deg"])], "xyz")
        spec.body("base_link").quat = q

    _add_visual_settings(spec)
    _add_table(spec, ws, cfg["table"], _resolve(cfg, cfg["table"]["texture"]))
    _add_clamps(spec, ws)
    _add_walls(spec, ws, cfg["walls"])
    if cfg.get("tape"):
        _add_tape(spec, ws, cfg["tape"])
    info.bin_sites = _add_bin(spec, ws, cfg["bin"])
    if cfg.get("charuco", {}).get("enabled"):
        _add_charuco(spec, ws, cfg["charuco"])
    info.cameras = _add_cameras(spec, ws, cfg["cameras"])
    if "wrist_camera" in cfg and spec.camera("wrist") is not None:
        wc, cam = cfg["wrist_camera"], spec.camera("wrist")
        cam.fovy = camera_fovy(wc)
        if "pos" in wc:
            cam.pos = wc["pos"]
            cam.quat = _camera_quat(wc["pos"], wc["look_at"], wc.get("roll_deg", 0.0))
    for c in cfg["cameras"] + [{"name": "wrist", **cfg.get("wrist_camera", {})}]:
        if c.get("resolution"):
            info.camera_resolutions[c["name"]] = tuple(c["resolution"])
    if with_objects:
        info.objects = [_add_object(spec, ws, o, cfg) for o in cfg.get("objects", [])]
    return info


def build_real_setup_spec(cfg_path: Path | str | None = None,
                          with_objects: bool = True) -> tuple[mujoco.MjSpec, SceneInfo]:
    spec = build_spec()
    info = apply_real_setup(spec, load_config(cfg_path), with_objects)
    return spec, info


# --------------------------------------------------------------------------- scene parts

def _remove_demo_scene(spec):
    for name in _DEMO_BODIES:
        body = spec.body(name)
        if body is not None:
            spec.delete(body)
    for name in _DEMO_GEOMS:
        geom = spec.geom(name)
        if geom is not None:
            spec.delete(geom)


def _material(spec, name, rgba, **kw):
    mat = spec.add_material(name=name)
    mat.rgba = rgba
    for k, v in kw.items():
        setattr(mat, k, v)
    return name


def _box(body, name, center, half, material, collide=True, contact=None, **kw):
    g = body.add_geom(name=name, type=mujoco.mjtGeom.mjGEOM_BOX, pos=center, size=half,
                      material=material, **kw)
    if collide:
        g.contype, g.conaffinity = 1, 1
        for k, v in (contact or _STATIC_CONTACT).items():
            setattr(g, k, v)
    else:
        g.contype, g.conaffinity = 0, 0
    return g


def _add_visual_settings(spec):
    vis = spec.visual
    vis.headlight.ambient = [0.30, 0.30, 0.30]
    vis.headlight.diffuse = [0.45, 0.45, 0.45]
    vis.rgba.haze = [0.55, 0.55, 0.55, 1]
    vis.global_.offwidth = max(vis.global_.offwidth, 1920)   # real cameras are 1920x1080
    vis.global_.offheight = max(vis.global_.offheight, 1080)
    # Ceiling lights of the room (warm, from above).
    for i, pos in enumerate(([0.3, 0.3, 1.8], [0.3, -0.4, 1.8])):
        spec.worldbody.add_light(name=f"room_light_{i}", pos=pos, dir=[0, 0, -1],
                                 diffuse=[0.45, 0.43, 0.40], specular=[0.1, 0.1, 0.1],
                                 castshadow=(i == 0))


def _add_table(spec, ws: Workspace, t, tex_path: Path):
    tex = spec.add_texture(name="table_wood", type=mujoco.mjtTexture.mjTEXTURE_2D,
                           file=str(tex_path))
    mat = spec.add_material(name="table_wood_mat")
    mat.textures[mujoco.mjtTextureRole.mjTEXROLE_RGB] = tex.name
    mat.texuniform = True
    mat.texrepeat = [1.0 / t["texture_tile"]] * 2
    mat.specular, mat.shininess, mat.reflectance = 0.15, 0.2, 0.0

    lo_l, hi_l = -t["extend_sides"], ws.width + t["extend_sides"]
    lo_n, hi_n = -0.05, ws.depth + t["extend_far"]
    c = ws.world((lo_l + hi_l) / 2, (lo_n + hi_n) / 2, -t["thickness"] / 2)
    _box(spec.worldbody, "table_top", c,
         [Workspace.half(lo_n, hi_n), Workspace.half(lo_l, hi_l), t["thickness"] / 2],
         "table_wood_mat")

    floor_z = ws.table_z - t["thickness"] - t["height_above_floor"]
    spec.worldbody.add_geom(name="floor", type=mujoco.mjtGeom.mjGEOM_PLANE,
                            pos=[0, 0, floor_z], size=[3, 3, 0.05],
                            material=_material(spec, "room_floor_mat", _COLORS["floor"]))


# The robot mesh's base plate (base_link_matte_black): half sizes and thickness.
BASE_PLATE_HALF = (0.07, 0.10)   # along x (near-far), y (left-right) [m]
BASE_PLATE_T = 0.014


def _add_clamps(spec, ws: Workspace):
    """Two green C-clamps on the near corners of the robot's base plate (visual)."""
    clamp = _material(spec, "clamp_mat", _COLORS["clamp"])
    body = spec.worldbody.add_body(name="clamps")
    hx, hy = BASE_PLATE_HALF
    for i, side in enumerate((-1, 1)):
        _box(body, f"clamp_{i}", [-hx + 0.02, side * (hy - 0.015), BASE_PLATE_T + 0.012],
             [0.02, 0.008, 0.012], clamp, collide=False)


def _add_tape(spec, ws: Workspace, t):
    """Tape strips on the table (visual only, a fraction of a millimetre thick)."""
    mat = _material(spec, "tape_mat", t.get("color", [0.96, 0.84, 0.10, 1]),
                    specular=0.3, shininess=0.4)
    body = spec.worldbody.add_body(name="tape")
    for i, strip in enumerate(t["strips"]):
        (l0, l1), (n0, n1) = strip["from_left"], strip["from_near"]
        c = ws.world((l0 + l1) / 2, (n0 + n1) / 2, 0.00015)
        _box(body, strip.get("name", f"tape_{i}"), c,
             [Workspace.half(n0, n1), Workspace.half(l0, l1), 0.00015], mat, collide=False)


def _add_walls(spec, ws: Workspace, w):
    t = w["thickness"]
    mats = {k: _material(spec, f"wall_{k}_mat", v) for k, v in _COLORS.items()
            if k in ("cardboard", "black")}
    body = spec.worldbody.add_body(name="walls")
    walls = {
        # name: (from_left range, from_near range)
        "near": ((0, ws.width), (-t, 0)),
        "right": ((ws.width, ws.width + t), (-t, ws.depth)),
        "left": ((-t, 0), (-t, ws.depth)),
    }
    for name, ((l0, l1), (n0, n1)) in walls.items():
        h = w[name]["height"]
        c = ws.world((l0 + l1) / 2, (n0 + n1) / 2, h / 2)
        _box(body, f"wall_{name}", c, [Workspace.half(n0, n1), Workspace.half(l0, l1), h / 2],
             mats[w[name]["color"]])


# How the board image must be turned so MuJoCo's box-face texture mapping shows
# it the right way round (found by rendering and detecting it, see the tests).
_CHARUCO_TEX_OP = "rot90_cw"


def _add_charuco(spec, ws: Workspace, c):
    """The printed ChArUco board lying on the table (see charuco.py)."""
    import cv2
    from .charuco import BoardSpec
    board = BoardSpec.from_config(c)
    img = board.image(100)
    img = {"none": img, "rot90_ccw": np.rot90(img, 1), "rot90_cw": np.rot90(img, -1),
           "rot180": np.rot90(img, 2), "flipud": img[::-1], "fliplr": img[:, ::-1]}[
        c.get("_tex_op", _CHARUCO_TEX_OP)]
    img = np.ascontiguousarray(img)
    # Name by content: MuJoCo caches assets by file name, so rewriting one file
    # with a different board could reuse the stale image.
    import hashlib
    digest = hashlib.sha1(img.tobytes() + str(img.shape).encode()).hexdigest()[:12]
    path = PKG_DIR / "textures" / "generated" / f"charuco_{digest}.png"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(path), img)
    tex = spec.add_texture(name="charuco_tex", type=mujoco.mjtTexture.mjTEXTURE_2D,
                           file=str(path))
    mat = spec.add_material(name="charuco_mat")
    mat.textures[mujoco.mjtTextureRole.mjTEXROLE_RGB] = tex.name
    mat.specular, mat.shininess = 0.0, 0.0
    w, h = board.size
    nl = board.near_left
    center = ws.world(nl[0] + w / 2, nl[1] + h / 2, 0.00025)
    spec.worldbody.add_geom(name="charuco_board", type=mujoco.mjtGeom.mjGEOM_BOX, pos=center,
                            size=[h / 2, w / 2, 0.00025], material="charuco_mat",
                            contype=0, conaffinity=0)


def _add_bin(spec, ws: Workspace, b) -> list[str]:
    mat = _material(spec, "foam_mat", _COLORS["foam"], specular=0.05, shininess=0.05)
    body = spec.worldbody.add_body(name="bin")
    l0, n0 = b["from_left"], b["from_near"]
    l1, n1 = l0 + b["size_left_right"], n0 + b["size_near_far"]
    h, wt, fl = b["height"], b["wall"], b["floor"]

    def part(name, la, lb, na, nb, z0, z1):
        c = ws.world((la + lb) / 2, (na + nb) / 2, (z0 + z1) / 2)
        _box(body, name, c, [Workspace.half(na, nb), Workspace.half(la, lb), (z1 - z0) / 2], mat)

    part("bin_floor", l0, l1, n0, n1, 0, fl)
    part("bin_wall_left", l0, l0 + wt, n0, n1, fl, h)
    part("bin_wall_right", l1 - wt, l1, n0, n1, fl, h)
    part("bin_wall_near", l0 + wt, l1 - wt, n0, n0 + wt, fl, h)
    part("bin_wall_far", l0 + wt, l1 - wt, n1 - wt, n1, fl, h)

    # Inner walls split the box into compartments along near -> far.
    inner_n0, inner_n1 = n0 + wt, n1 - wt
    cuts = [inner_n0]
    for i, frac in enumerate(b.get("dividers", [])):
        nc = n0 + frac * b["size_near_far"]
        part(f"bin_divider_{i}", l0 + wt, l1 - wt, nc - wt / 2, nc + wt / 2, fl, h)
        cuts += [nc - wt / 2, nc + wt / 2]
    cuts.append(inner_n1)

    sites = []
    for i in range(len(cuts) // 2):
        na, nb = cuts[2 * i], cuts[2 * i + 1]
        name = f"bin_{i}"  # bin_0 is nearest to the robot's wall
        body.add_site(name=name, pos=ws.world((l0 + l1) / 2, (na + nb) / 2, fl),
                      size=[Workspace.half(na, nb) - 0.005, Workspace.half(l0, l1) - wt - 0.005,
                            0.001],
                      type=mujoco.mjtGeom.mjGEOM_BOX, rgba=[0.2, 0.6, 1.0, 0.15], group=4)
        sites.append(name)
    return sites


def camera_fovy(cam: dict) -> float:
    """Vertical fov [deg] from `fovy`, or from a spec-sheet diagonal fov and the aspect."""
    if "fovy" in cam:
        return float(cam["fovy"])
    w, h = cam.get("aspect", [4, 3])
    half_diag = np.tan(np.radians(cam["fov_diagonal_deg"]) / 2)
    return float(np.degrees(2 * np.arctan(half_diag * h / np.hypot(w, h))))


def _camera_quat(pos, target, roll_deg: float = 0.0) -> np.ndarray:
    """Looks from pos at target (image up = world up), then rolls the image by
    roll_deg about the optical axis (positive = clockwise in the image)."""
    quat = _lookat_quat(pos, target, [0, 0, 1])
    if roll_deg:
        q_roll, out = np.empty(4), np.empty(4)
        mujoco.mju_axisAngle2Quat(q_roll, [0, 0, 1], np.radians(roll_deg))
        mujoco.mju_mulQuat(out, quat, q_roll)
        quat = out
    return quat


def _add_cameras(spec, ws: Workspace, cams) -> list[str]:
    mat = _material(spec, "camera_body_mat", _COLORS["camera"])
    names = []
    for cam in cams:
        pos = ws.world(cam["from_left"], cam["from_near"], cam["height"])
        target = ws.world(*cam["look_at"])
        quat = _camera_quat(pos, target, cam.get("roll_deg", 0.0))
        spec.worldbody.add_camera(name=cam["name"], pos=pos, quat=quat, fovy=camera_fovy(cam))
        # Camera housing and its post down to the table (visual only).
        body = spec.worldbody.add_body(name=f"{cam['name']}_mount", pos=pos, quat=quat)
        _box(body, f"{cam['name']}_housing", [0, 0, 0.02], [0.045, 0.02, 0.02], mat,
             collide=False)
        if cam.get("mount", "post") == "post":  # "none": e.g. a gooseneck from outside
            spec.worldbody.add_geom(name=f"{cam['name']}_post",
                                    type=mujoco.mjtGeom.mjGEOM_CAPSULE,
                                    fromto=np.concatenate([pos - [0, 0, 0.03],
                                                           [pos[0], pos[1], ws.table_z]]),
                                    size=[0.008, 0, 0], material=mat, contype=0, conaffinity=0)
        names.append(cam["name"])
    return names


def _add_object(spec, ws: Workspace, o, cfg) -> str:
    kind = o["type"]
    mat = _material(spec, f"{o['name']}_mat", o.get("rgba", [0.8, 0.8, 0.8, 1]))
    z_base = o.get("height_offset", 0.0) + 0.001
    body = spec.worldbody.add_body(name=o["name"],
                                   pos=ws.world(o["from_left"], o["from_near"], z_base))
    body.add_freejoint(name=f"{o['name']}_free")

    def contact(g):
        g.contype, g.conaffinity = 1, 1
        for k, v in _GRASP_CONTACT.items():
            setattr(g, k, v)
        return g

    if kind == "can":
        r, h = o["radius"], o["height"]
        contact(body.add_geom(name=f"{o['name']}_geom", type=mujoco.mjtGeom.mjGEOM_CYLINDER,
                              pos=[0, 0, h / 2], size=[r, h / 2, 0], material=mat,
                              mass=o["mass"]))
    elif kind == "roll":  # a cylinder lying on the table along the body's x axis
        r, l = o["radius"], o["length"]
        contact(body.add_geom(name=f"{o['name']}_geom", type=mujoco.mjtGeom.mjGEOM_CYLINDER,
                              pos=[0, 0, r], quat=[np.sqrt(0.5), 0, np.sqrt(0.5), 0],
                              size=[r, l / 2, 0], material=mat, mass=o["mass"]))
    elif kind == "cup":
        _add_cup_geoms(body, o, mat, contact)
    elif kind == "mesh":
        mesh_path = _resolve(cfg, o["file"])
        spec.add_mesh(name=f"{o['name']}_mesh", file=str(mesh_path),
                      scale=[o.get("scale", 1.0)] * 3)
        contact(body.add_geom(name=f"{o['name']}_geom", type=mujoco.mjtGeom.mjGEOM_MESH,
                              meshname=f"{o['name']}_mesh", material=mat, mass=o["mass"]))
    else:
        raise ValueError(f"unknown object type {kind!r} (can, roll, cup, mesh)")
    body.add_site(name=f"{o['name']}_site", pos=[0, 0, 0], size=[0.004], group=4)
    return o["name"]


def _add_cup_geoms(body, o, mat, contact, n: int = 20):
    """Open paper cup: a truncated cone made of thin wall slats plus a bottom disc."""
    rt, rb, h, w = o["top_radius"], o["bottom_radius"], o["height"], o["wall"]
    tilt = np.arctan2(rt - rb, h)
    slant = np.hypot(rt - rb, h)
    m = o["mass"] / (n + 2)
    for i in range(n):
        th = 2 * np.pi * i / n
        r_mid = (rt + rb) / 2
        q_yaw, q_tilt, q = np.empty(4), np.empty(4), np.empty(4)
        mujoco.mju_axisAngle2Quat(q_yaw, [0, 0, 1], th)
        mujoco.mju_axisAngle2Quat(q_tilt, [0, 1, 0], tilt)
        mujoco.mju_mulQuat(q, q_yaw, q_tilt)
        contact(body.add_geom(name=f"{o['name']}_wall_{i}", type=mujoco.mjtGeom.mjGEOM_BOX,
                              pos=[r_mid * np.cos(th), r_mid * np.sin(th), h / 2], quat=q,
                              size=[w / 2, np.pi * rt / n * 1.1, slant / 2],
                              material=mat, mass=m))
    contact(body.add_geom(name=f"{o['name']}_bottom", type=mujoco.mjtGeom.mjGEOM_CYLINDER,
                          pos=[0, 0, 0.002], size=[rb, 0.002, 0], material=mat, mass=2 * m))
