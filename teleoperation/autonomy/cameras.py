"""Camera rig: N fixed scene cameras + an optional wrist camera.

Each camera has a role:
  * ``scene``  fixed to the table/frame, calibrated once (intrinsics + pose in world)
  * ``wrist``  rigidly mounted on the gripper; its pose follows the arm (hand-eye)

``SimCameraRig`` renders MuJoCo cameras and reads exact calibrations from the model.
``RealCameraRig`` opens USB cameras with OpenCV and loads calibration.json.
"""
from __future__ import annotations

import json
from pathlib import Path

import mujoco
import numpy as np

from autonomy.geometry import CameraModel, intrinsics_from_fovy, make_T

CV_FROM_MJ = np.diag([1.0, -1.0, -1.0])   # MuJoCo camera (y up, looks -z) -> OpenCV


def sim_wrist_mount(model, camera: str = "wrist") -> np.ndarray:
    """T_endlink_cam (OpenCV convention) of the wrist camera defined in the MuJoCo model.
    Used for the real wrist camera until `calibrate wrist` has measured the mount."""
    cid = model.camera(camera).id
    R = np.empty(9)
    mujoco.mju_quat2Mat(R, model.cam_quat[cid])
    return make_T(R.reshape(3, 3) @ CV_FROM_MJ, model.cam_pos[cid])


class CameraRig:
    scene: list[str]
    wrist: str | None

    @property
    def names(self) -> list[str]:
        return self.scene + ([self.wrist] if self.wrist else [])

    def grab(self, names: list[str] | None = None) -> dict[str, np.ndarray]:
        raise NotImplementedError

    def model(self, name: str) -> CameraModel:
        raise NotImplementedError

    def close(self):
        pass


class SimCameraRig(CameraRig):
    def __init__(self, sim, scene=("overhead_rgb", "front"), wrist="wrist",
                 width=640, height=480):
        self.sim = sim
        self.scene, self.wrist = list(scene), wrist
        self.width, self.height = width, height
        self.renderer = mujoco.Renderer(sim.model, height=height, width=width)
        self.opt = mujoco.MjvOption()
        self.opt.sitegroup[:] = 0          # hide the orange TCP marker
        self.opt.geomgroup[2] = 0          # hide the target-frame axes
        # Park the teleop target marker under the floor so cameras never see it.
        sim.data.mocap_pos[sim.target_mocap] = [0, 0, -5]

    def grab(self, names=None):
        mujoco.mj_forward(self.sim.model, self.sim.data)
        out = {}
        for n in names or self.names:
            self.renderer.update_scene(self.sim.data, camera=n, scene_option=self.opt)
            out[n] = self.renderer.render().copy()
        return out

    def model(self, name):
        m, d = self.sim.model, self.sim.data
        mujoco.mj_forward(m, d)
        cid = m.camera(name).id
        R = d.cam_xmat[cid].reshape(3, 3) @ CV_FROM_MJ
        K = intrinsics_from_fovy(m.cam_fovy[cid], self.width, self.height)
        return CameraModel(name, K, make_T(R, d.cam_xpos[cid]), self.width, self.height)

    def wrist_mount(self) -> np.ndarray:
        """T_endlink_cam of the simulated wrist camera (used as the real default)."""
        m, d = self.sim.model, self.sim.data
        mujoco.mj_forward(m, d)
        b = m.body("end_link").id
        T_wb = make_T(d.xmat[b].reshape(3, 3), d.xpos[b])
        return np.linalg.inv(T_wb) @ self.model(self.wrist).T_world_cam

    def close(self):
        self.renderer.close()


class RealCameraRig(CameraRig):
    """USB cameras through OpenCV.

    config["cameras"] = [{"name": "top", "role": "scene", "device": 0, "width": 1280,
                          "height": 720}, ...]
    calibration.json holds, per scene camera, {"K", "dist", "T_world_cam", ...} and, for
    the wrist camera, {"K", "dist", "T_endlink_cam", ...}.
    """

    def __init__(self, sim, cameras: list[dict], calibration_path: str | Path):
        import cv2
        self.cv2 = cv2
        self.sim = sim            # the arm's MuJoCo mirror: gives the end_link pose
        self.specs = {c["name"]: c for c in cameras}
        self.scene = [c["name"] for c in cameras if c["role"] == "scene"]
        wr = [c["name"] for c in cameras if c["role"] == "wrist"]
        self.wrist = wr[0] if wr else None
        calib = json.loads(Path(calibration_path).read_text()) if Path(calibration_path).exists() else {}
        self.calib = calib.get("cameras", {})
        missing = [n for n in self.specs if n not in self.calib]
        if missing:
            print(f"[cameras] WARNING: no calibration for {missing}; run autonomy.calibrate")
        self.caps = {}
        for name, spec in self.specs.items():
            cap = cv2.VideoCapture(spec["device"])
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, spec.get("width", 1280))
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, spec.get("height", 720))
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if not cap.isOpened():
                raise RuntimeError(f"camera {name!r} (device {spec['device']}) did not open")
            self.caps[name] = cap

    def grab(self, names=None):
        out = {}
        for n in names or self.names:
            cap = self.caps[n]
            for _ in range(2):    # drop a buffered frame so the image is fresh
                cap.grab()
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError(f"camera {n!r} returned no frame")
            out[n] = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)
        return out

    def model(self, name):
        c = self.calib[name]
        K, dist = np.array(c["K"], float), np.array(c.get("dist", [0] * 5), float)
        w, h = int(c["width"]), int(c["height"])
        if name == self.wrist:
            m, d = self.sim.model, self.sim.data
            mujoco.mj_kinematics(m, d)
            b = m.body("end_link").id
            mount = np.array(c["T_endlink_cam"], float) if "T_endlink_cam" in c else sim_wrist_mount(m)
            T = make_T(d.xmat[b].reshape(3, 3), d.xpos[b]) @ mount
        else:
            T = np.array(c["T_world_cam"], float)
        return CameraModel(name, K, T, w, h, dist)

    def close(self):
        for cap in self.caps.values():
            cap.release()
