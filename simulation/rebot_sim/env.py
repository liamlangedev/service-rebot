"""RealSetupEnv: the teleop reBot model in the real-setup scene, plus helpers
for tests, scripted policies and data generation.

    from rebot_sim import RealSetupEnv, TOP_DOWN
    env = RealSetupEnv()                       # or RealSetupEnv(config="my_setup.json")
    env.reset(seed=0, randomize=True)          # random object positions
    can = env.object_pos("can")
    env.move_grasp_to(can + [0, 0, 0.20])      # IK, top-down tool
    env.move_grasp_to(can + [0, 0, 0.06]); env.set_gripper(0.0)
    env.move_grasp_to(env.bin_pos("bin_0") + [0, 0, 0.30]); env.set_gripper(env.GRIPPER_OPEN)
    assert env.in_bin("can", "bin_0")
    img = env.render("cam_corner")             # HxWx3 uint8

It subclasses the teleop `RebotSim`, so `command()`, `tcp_pose()`, `q_arm` and the
actuator/joint indices are all there too.
"""
from __future__ import annotations

from pathlib import Path

import mujoco
import numpy as np

from .scene import SceneInfo, apply_real_setup, load_config

from teleop.ik import DiffIK  # noqa: E402  (path set by .scene)
from teleop.rebot_model import ARM_JOINTS, GRASP_SITE, GRIPPER_MAX, HOME_QPOS, RebotSim  # noqa: E402

# Tool (end_link +x) pointing straight down, fingers closing along world y.
TOP_DOWN = np.column_stack([[0, 0, -1], [0, 1, 0], [1, 0, 0]]).astype(float)


class RealSetupEnv(RebotSim):
    GRIPPER_OPEN = GRIPPER_MAX
    GRIPPER_CLOSED = 0.0

    def __init__(self, config: Path | str | dict | None = None, objects: bool = True,
                 control_hz: int = 100):
        cfg = config if isinstance(config, dict) else load_config(config)
        self.cfg = cfg
        self._with_objects = objects
        self._renderers: dict[tuple[int, int], mujoco.Renderer] = {}
        super().__init__(scene=lambda spec: apply_real_setup(spec, cfg, objects))
        self.info: SceneInfo = self.scene_info
        self.control_dt = 1.0 / control_hz
        self.n_sub = max(1, round(self.control_dt / self.model.opt.timestep))
        self._ik = None

    # ------------------------------------------------------------------ basics
    @property
    def ws(self):
        return self.info.workspace

    @property
    def objects(self) -> list[str]:
        return list(self.info.objects)

    @property
    def bins(self) -> list[str]:
        return list(self.info.bin_sites)

    @property
    def cameras(self) -> list[str]:
        return [self.model.camera(i).name for i in range(self.model.ncam)]

    def reset(self, q_arm: np.ndarray = HOME_QPOS, gripper: float = GRIPPER_MAX,
              objects: dict | None = None, randomize: bool = False, seed: int | None = None,
              settle: float = 0.3):
        """Resets the robot and the objects. `objects` maps name -> (from_left,
        from_near[, yaw]) in workspace coordinates; `randomize` samples the rest
        from the config's spawn_region."""
        super().reset(q_arm, gripper)
        if not hasattr(self, "n_sub"):  # called from RebotSim.__init__
            return
        if randomize:
            self.randomize_objects(np.random.default_rng(seed), keep=objects or {})
        for name, where in (objects or {}).items():
            self.place_object(name, *where)
        mujoco.mj_forward(self.model, self.data)
        if settle:
            self.step(n=int(settle / self.control_dt))

    def step(self, q_arm: np.ndarray | None = None, gripper: float | None = None, n: int = 1):
        """Advances `n` control ticks, optionally with a new joint/gripper command."""
        if q_arm is not None or gripper is not None:
            self.command(self.data.ctrl[self.arm_act] if q_arm is None else q_arm,
                         self.data.ctrl[self.grip_act] if gripper is None else gripper)
        for _ in range(n):
            mujoco.mj_step(self.model, self.data, nstep=self.n_sub)

    # ------------------------------------------------------------------ objects
    def _free_qadr(self, name: str) -> int:
        return self.model.joint(f"{name}_free").qposadr[0]

    def place_object(self, name: str, from_left: float, from_near: float, yaw: float = 0.0):
        """Puts an object upright on the table at a workspace position."""
        a = self._free_qadr(name)
        self.data.qpos[a:a + 3] = self.ws.world(from_left, from_near, 0.001)
        q = np.empty(4)
        mujoco.mju_axisAngle2Quat(q, [0, 0, 1], yaw)
        self.data.qpos[a + 3:a + 7] = q
        dadr = self.model.joint(f"{name}_free").dofadr[0]
        self.data.qvel[dadr:dadr + 6] = 0

    def randomize_objects(self, rng: np.random.Generator, keep: dict | None = None):
        r = self.cfg["spawn_region"]
        robot = np.array([self.ws.robot_from_left, self.ws.robot_from_near])
        placed = [np.array(v[:2]) for v in (keep or {}).values()]
        for name in self.objects:
            if keep and name in keep:
                continue
            for _ in range(1000):
                p = np.array([rng.uniform(*r["from_left"]), rng.uniform(*r["from_near"])])
                if np.linalg.norm(p - robot) < r["min_robot_distance"]:
                    continue
                if all(np.linalg.norm(p - q) >= r["min_spacing"] for q in placed):
                    break
            else:
                raise RuntimeError("spawn_region too small for the objects")
            placed.append(p)
            self.place_object(name, *p, yaw=rng.uniform(-np.pi, np.pi))

    def object_pos(self, name: str) -> np.ndarray:
        """World position of the object's base (bottom centre)."""
        return self.data.body(name).xpos.copy()

    def object_upright(self, name: str, tol_deg: float = 20.0) -> bool:
        z = self.data.body(name).xmat.reshape(3, 3)[:, 2]
        return bool(z[2] > np.cos(np.radians(tol_deg)))

    def bin_pos(self, bin_name: str) -> np.ndarray:
        """World position of the centre of a compartment's floor."""
        return self.data.site(bin_name).xpos.copy()

    def in_bin(self, name: str, bin_name: str) -> bool:
        p, c = self.object_pos(name), self.bin_pos(bin_name)
        half = self.model.site(bin_name).size
        h = self.cfg["bin"]["height"]
        return bool(abs(p[0] - c[0]) < half[0] + 0.01 and abs(p[1] - c[1]) < half[1] + 0.01
                    and p[2] < self.ws.table_z + h)

    # ------------------------------------------------------------------ motion
    @property
    def ik(self) -> DiffIK:
        if self._ik is None:
            self._ik = DiffIK(self.model, GRASP_SITE, ARM_JOINTS, q_rest=HOME_QPOS,
                              max_joint_vel=1.5)
        return self._ik

    def grasp_pos(self) -> np.ndarray:
        return self.data.site(GRASP_SITE).xpos.copy()

    def move_grasp_to(self, pos, rot: np.ndarray | None = TOP_DOWN, speed: float = 0.15,
                      settle: float = 0.3) -> float:
        """Straight-line move of the grasp point (between the finger pads) with
        the IK. Returns the remaining position error [m]."""
        pos = np.asarray(pos, float)
        q = self.data.ctrl[self.arm_act].copy()
        start = self.ik.fk(q)[0]
        n = max(1, int(np.linalg.norm(pos - start) / speed / self.control_dt))
        for s in np.linspace(0, 1, n + 1)[1:]:
            q, _, _ = self.ik.solve(q, start + s * (pos - start), rot, self.control_dt)
            self.step(q_arm=q)
        self.step(n=int(settle / self.control_dt))
        return float(np.linalg.norm(self.grasp_pos() - pos))

    def set_gripper(self, opening: float, secs: float = 0.6):
        """Finger opening command [m per finger, 0 = closed, GRIPPER_OPEN = open]."""
        self.step(gripper=opening, n=int(secs / self.control_dt))

    # ------------------------------------------------------------------ cameras
    def hide_markers(self):
        """Hide the teleop target marker and the debug sites, so renders show only
        what a real camera would see."""
        target = self.model.body("ik_target").id
        self.model.geom_rgba[self.model.geom_bodyid == target, 3] = 0.0
        self.model.site_rgba[:, 3] = 0.0

    def render(self, camera: str = "cam_corner", width: int = 640, height: int = 480) -> np.ndarray:
        key = (width, height)
        if key not in self._renderers:
            self._renderers[key] = mujoco.Renderer(self.model, height=height, width=width)
        r = self._renderers[key]
        r.update_scene(self.data, camera=camera)
        return r.render()

    def close(self):
        for r in self._renderers.values():
            r.close()
        self._renderers.clear()
