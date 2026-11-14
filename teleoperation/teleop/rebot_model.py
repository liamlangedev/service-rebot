"""Builds a teleop-ready MuJoCo model of the Seeed reBot Arm B601-DM.

Seeed's official MJCF (rebotarm_b601_colored.xml) ships without actuators and
without material colors, so we load it with MjSpec and add on top:
  * position servos on joint1..joint6 (the real arm runs its Damiao motors in
    position/velocity mode, so position servos are the closest analogue)
  * a coupled parallel gripper (finger_right mirrors finger_left)
  * material colors and a visible teleop target marker (the `ik_target` mocap)
"""
from pathlib import Path

import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTION_DIR = ROOT / "assets" / "reBot-DevArm" / "Rebot_Arm_description"
DM_MJCF = DESCRIPTION_DIR / "DM" / "mjcf" / "rebotarm_b601_colored.xml"

ARM_JOINTS = [f"joint{i}" for i in range(1, 7)]
TCP_SITE = "tcp"  # Seeed's site: at the gripper palm, ~7 cm behind the fingertips
# Added by build_spec: centre of the finger pads, where an object is held.
# Control this point to place the fingers around an object.
GRASP_SITE = "grasp"
TARGET_BODY = "ik_target"

# Elbow-up pose with the tool pointing forward, TCP ~(0.32, 0, 0.44) m.
HOME_QPOS = np.array([0.0, -1.2, -1.2, 0.0, 0.0, 0.0])

GRIPPER_MAX = 0.05  # finger_left slide range in the MJCF [m]

# (kp, kv, max torque Nm). Torque limits roughly follow the Damiao motors:
# 4340P on joints 1-3, smaller motors on the wrist.
_SERVO_GAINS = {
    "joint1": (300.0, 20.0, 27.0),
    "joint2": (400.0, 30.0, 27.0),
    "joint3": (300.0, 20.0, 27.0),
    "joint4": (100.0, 6.0, 10.0),
    "joint5": (60.0, 4.0, 10.0),
    "joint6": (40.0, 3.0, 10.0),
}

# Soft limits [deg] of the real DM arm in LeRobot (rebot_b601_follower DM
# profile, same as the team's follower.json). Sim joint ranges are clipped to
# them so recorded actions are always valid on the real arm.
REAL_SOFT_LIMITS_DEG = {
    "joint1": (-150.0, 150.0),
    "joint2": (-200.0, 1.0),
    "joint3": (-200.0, 1.0),
    "joint4": (-80.0, 90.0),
    "joint5": (-90.0, 90.0),
    "joint6": (-90.0, 90.0),
}

_MATERIAL_RGBA = {
    "anodized_grey_mat": [0.62, 0.64, 0.66, 1],
    "hardware_black_mat": [0.10, 0.10, 0.11, 1],
    "matte_black_mat": [0.16, 0.16, 0.17, 1],
    "seeed_yellow_mat": [0.96, 0.76, 0.06, 1],
    "silver_trim_mat": [0.80, 0.81, 0.83, 1],
    "gripper_finger_black_mat": [0.14, 0.14, 0.15, 1],
    "gripper_rack_metal_mat": [0.75, 0.76, 0.78, 1],
    "gripper_seeed_yellow_mat": [0.96, 0.76, 0.06, 1],
    "gripper_hardware_black_mat": [0.10, 0.10, 0.11, 1],
    "gripper_base_metal_mat": [0.75, 0.76, 0.78, 1],
    "target_mat": [0.10, 0.85, 0.35, 0.35],
}


def build_spec(mjcf_path: Path = DM_MJCF) -> mujoco.MjSpec:
    if not mjcf_path.exists():
        raise FileNotFoundError(
            f"{mjcf_path} not found. Run ./scripts/setup_assets.sh first."
        )
    spec = mujoco.MjSpec.from_file(str(mjcf_path))

    for name, rgba in _MATERIAL_RGBA.items():
        spec.material(name).rgba = rgba

    for joint, (lo, hi) in REAL_SOFT_LIMITS_DEG.items():
        rng = spec.joint(joint).range
        spec.joint(joint).range = [max(rng[0], np.radians(lo)), min(rng[1], np.radians(hi))]

    for joint, (kp, kv, tau) in _SERVO_GAINS.items():
        act = spec.add_actuator(name=f"{joint}_pos", target=joint,
                                trntype=mujoco.mjtTrn.mjTRN_JOINT)
        act.set_to_position(kp=kp, kv=kv)
        act.forcelimited = True
        act.forcerange = [-tau, tau]
        rng = spec.joint(joint).range
        act.ctrllimited = True
        act.ctrlrange = [rng[0], rng[1]]

    grip = spec.add_actuator(name="gripper_pos", target="finger_left",
                             trntype=mujoco.mjtTrn.mjTRN_JOINT)
    grip.set_to_position(kp=200.0, kv=5.0)
    grip.forcelimited = True
    grip.forcerange = [-20.0, 20.0]
    grip.ctrllimited = True
    grip.ctrlrange = [0.0, GRIPPER_MAX]

    # finger_right = -finger_left
    spec.add_equality(type=mujoco.mjtEq.mjEQ_JOINT, name1="finger_right",
                      name2="finger_left", data=[0, -1, 0, 0, 0] + [0] * 7)

    # The real Damiao POS_VEL loop has an integral term, so it holds position
    # under load. Emulate that with gravity compensation routed through the
    # actuators (so it still respects the torque limits).
    for name in ["link1", "link2", "link3", "link4", "link5", "link6", "end_link",
                 "finger_left_link", "finger_right_link"]:
        spec.body(name).gravcomp = 1.0
    for joint in ARM_JOINTS:
        spec.joint(joint).actgravcomp = True

    # Small frame at the target so its orientation is visible too.
    target = spec.body(TARGET_BODY)
    for axis, rgba in zip(np.eye(3), ([1, 0, 0, 0.6], [0, 1, 0, 0.6], [0, 0, 1, 0.6])):
        target.add_geom(type=mujoco.mjtGeom.mjGEOM_CAPSULE, size=[0.003, 0, 0],
                        fromto=np.concatenate([np.zeros(3), 0.06 * axis]),
                        rgba=rgba, contype=0, conaffinity=0, group=2)

    # Grasp point between the finger pads, 7 cm ahead of the palm `tcp` site
    # (tcp is at end_link x = -0.105; the finger pads span about x = -0.06 .. 0).
    spec.body("end_link").add_site(name=GRASP_SITE, pos=[-0.035, 0, 0], size=[0.006],
                                   rgba=[0.2, 0.8, 0.3, 1])

    # Cameras for dataset recording (the MJCF already has `overhead_rgb`).
    # end_link sits at the fingertips and the tool points along its +x.
    spec.worldbody.add_camera(name="front", pos=[0.95, 0, 0.5], fovy=50,
                              quat=_lookat_quat([0.95, 0, 0.5], [0.3, 0, 0.15], [0, 0, 1]))
    spec.body("end_link").add_camera(name="wrist", pos=[-0.13, 0, 0.05], fovy=80,
                                     quat=_lookat_quat([-0.13, 0, 0.05], [0.15, 0, 0], [0, 0, 1]))
    return spec


def _lookat_quat(pos, target, up):
    """Quaternion of a MuJoCo camera (looks along -z, y up) at pos facing target."""
    z = np.asarray(pos, float) - np.asarray(target, float)
    z /= np.linalg.norm(z)
    x = np.cross(up, z)
    x /= np.linalg.norm(x)
    quat = np.empty(4)
    mujoco.mju_mat2Quat(quat, np.column_stack([x, np.cross(z, x), z]).reshape(-1))
    return quat


SCENES = ("default", "real")  # or a path to a setup JSON (see simulation/rebot_sim)


def apply_scene(spec: mujoco.MjSpec, scene="default"):
    """Adds the workspace around the robot.

    `default`: Seeed's demo table and cubes. `real`: the team's measured setup
    (simulation/rebot_sim/real_setup.json). A `*.json` path: a setup in the same
    format. A callable: called with the spec (returns the scene info)."""
    if callable(scene):
        return scene(spec)
    if scene == "default":
        return None
    import sys
    sim_dir = str(ROOT.parent / "simulation")
    if sim_dir not in sys.path:
        sys.path.insert(0, sim_dir)
    from rebot_sim import apply_real_setup, load_config
    if scene == "real":
        return apply_real_setup(spec)
    if str(scene).endswith(".json"):
        return apply_real_setup(spec, load_config(scene))
    raise ValueError(f"unknown scene {scene!r}: use one of {SCENES} or a setup .json")


class RebotSim:
    """Compiled model plus handy indices."""

    def __init__(self, mjcf_path: Path = DM_MJCF, scene="default"):
        self.spec = build_spec(mjcf_path)
        self.scene_info = apply_scene(self.spec, scene)
        self.model = self.spec.compile()
        self.data = mujoco.MjData(self.model)
        m = self.model
        self.arm_qadr = np.array([m.joint(j).qposadr[0] for j in ARM_JOINTS])
        self.arm_dadr = np.array([m.joint(j).dofadr[0] for j in ARM_JOINTS])
        self.arm_act = np.array([m.actuator(f"{j}_pos").id for j in ARM_JOINTS])
        self.grip_act = m.actuator("gripper_pos").id
        self.grip_qadr = m.joint("finger_left").qposadr[0]
        self.tcp_site = m.site(TCP_SITE).id
        self.target_mocap = m.body_mocapid[m.body(TARGET_BODY).id]
        self.reset()

    def reset(self, q_arm: np.ndarray = HOME_QPOS, gripper: float = GRIPPER_MAX):
        mujoco.mj_resetData(self.model, self.data)
        self.data.qpos[self.arm_qadr] = q_arm
        self.data.ctrl[self.arm_act] = q_arm
        self.data.ctrl[self.grip_act] = gripper
        mujoco.mj_forward(self.model, self.data)
        self.set_target(*self.tcp_pose())

    @property
    def q_arm(self) -> np.ndarray:
        return self.data.qpos[self.arm_qadr].copy()

    @property
    def gripper(self) -> float:
        """Measured finger_left opening [m]."""
        return float(self.data.qpos[self.grip_qadr])

    def tcp_pose(self):
        return (self.data.site_xpos[self.tcp_site].copy(),
                self.data.site_xmat[self.tcp_site].reshape(3, 3).copy())

    def set_target(self, pos, rot):
        quat = np.empty(4)
        mujoco.mju_mat2Quat(quat, np.asarray(rot).reshape(-1))
        self.data.mocap_pos[self.target_mocap] = pos
        self.data.mocap_quat[self.target_mocap] = quat

    def get_target(self):
        rot = np.empty(9)
        mujoco.mju_quat2Mat(rot, self.data.mocap_quat[self.target_mocap])
        return self.data.mocap_pos[self.target_mocap].copy(), rot.reshape(3, 3)

    def mirror(self, q_arm: np.ndarray, finger: float):
        """Shows a measured (real-arm) pose: kinematics only, no physics."""
        self.data.qpos[self.arm_qadr] = q_arm
        self.data.qpos[self.grip_qadr] = finger
        self.data.qpos[self.model.joint("finger_right").qposadr[0]] = -finger
        self.data.qvel[:] = 0
        mujoco.mj_forward(self.model, self.data)

    def command(self, q_arm: np.ndarray, gripper: float):
        self.data.ctrl[self.arm_act] = q_arm
        self.data.ctrl[self.grip_act] = np.clip(gripper, 0.0, GRIPPER_MAX)
