"""Learned-grasp node: the classical stack calls it at a pre-grasp pose; it runs a lerobot
policy until the jaw has closed and the TCP has lifted, holds the arm there and returns.

Interface
---------
* ``~/grasp`` (``std_srvs/Trigger``) - blocking. Takes over from the current pose and
  returns once gripped and lifted (``success=True``), or on timeout / cancel / error
  (``success=False``). ``message`` is a JSON object: ``reason``, ``lifted_m``,
  ``finger_m``, ``elapsed_s``, ``inferences``, ``clipped``.
  On return the arm holds its current pose and the gripper is **not** reopened, so a
  held object stays held; the caller decides what happens next (e.g. ``check_hold``).
* ``~/cancel`` (``std_srvs/Trigger``) - stops a running grasp at the next tick.
* ``~/status`` (``std_msgs/String``) - JSON progress, once per tick while running.

Runs under the teleoperation venv's Python (lerobot + torch) with ROS sourced; see
``launch/grasp_policy.launch.py``. Parameters: ``config/grasp_policy.yaml``.
"""

from __future__ import annotations

import json
import threading
import time
from typing import Any

import numpy as np
import rclpy
from rclpy.action import ActionClient
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.duration import Duration
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.time import Time
from sensor_msgs.msg import Image, JointState
from std_msgs.msg import String
from std_srvs.srv import Trigger

from .grasp_policy.done import DoneConfig, GraspDone
from .grasp_policy.units import ARM_JOINTS, GripperMap, data_to_ros, ros_to_data
from .ros_image import imgmsg_to_bgr


class GraspPolicyNode(Node):
    def __init__(self) -> None:
        super().__init__("grasp_policy")
        p = self.declare_parameter
        p("policy_path", "")
        p("policy_revision", "")
        p("mode", "relative")
        p("device", "cpu")
        p("n_steps", 10)
        p("task", "grasp the keys and lift them")
        p("max_offset_deg", 45.0)
        p("rate_hz", 30.0)
        p("timeout_s", 8.0)
        p("arm_action", "/rebotarm_controller/follow_joint_trajectory")
        p("gripper_action", "/gripper_controller/follow_joint_trajectory")
        p("gripper_joint", "finger_left")
        p("gripper_ros_open_m", 0.05)
        p("gripper_ros_closed_m", 0.0)
        p("gripper_data_open_deg", -365.0)
        p("gripper_data_closed_deg", -5.0)
        p("camera_names", ["gripper"])
        p("camera_topics", ["/wrist_cam/image_raw"])
        p("base_frame", "base_link")
        p("tcp_frame", "gripper_tcp")
        p("stale_s", 0.5)
        p("done_closed_ticks", 6)
        p("done_settle_ticks", 6)
        p("done_settle_m", 0.0008)
        p("lift_m", 0.05)
        p("load_on_start", True)

        from control_msgs.action import FollowJointTrajectory
        from tf2_ros import Buffer, TransformListener

        self._FJT = FollowJointTrajectory
        self._cb = ReentrantCallbackGroup()
        self._srv_cb = MutuallyExclusiveCallbackGroup()
        self._lock = threading.Lock()
        self._joints: dict[str, float] = {}
        self._joints_t = 0.0
        self._images: dict[str, np.ndarray] = {}
        self._images_t: dict[str, float] = {}
        self._cancel = threading.Event()
        self._busy = threading.Lock()
        self._runner = None
        self._arm_goal = None

        self.gmap = GripperMap(
            ros_open_m=self._f("gripper_ros_open_m"), ros_closed_m=self._f("gripper_ros_closed_m"),
            data_open_deg=self._f("gripper_data_open_deg"),
            data_closed_deg=self._f("gripper_data_closed_deg"))

        self.create_subscription(JointState, "/joint_states", self._on_joints, 20,
                                 callback_group=self._cb)
        names = list(self.get_parameter("camera_names").value)
        topics = list(self.get_parameter("camera_topics").value)
        if len(names) != len(topics):
            raise ValueError("camera_names and camera_topics must have the same length")
        for name, topic in zip(names, topics):
            self.create_subscription(Image, topic, lambda m, n=name: self._on_image(n, m), 2,
                                     callback_group=self._cb)

        self._tf = Buffer()
        self._tf_listener = TransformListener(self._tf, self)
        self._arm = ActionClient(self, FollowJointTrajectory, self._s("arm_action"),
                                 callback_group=self._cb)
        self._grip = ActionClient(self, FollowJointTrajectory, self._s("gripper_action"),
                                  callback_group=self._cb)
        self._status = self.create_publisher(String, "~/status", 10)
        self.create_service(Trigger, "~/grasp", self._on_grasp, callback_group=self._srv_cb)
        self.create_service(Trigger, "~/cancel", self._on_cancel, callback_group=self._cb)

        if self.get_parameter("load_on_start").value:
            self._load_policy()
        self.get_logger().info(f"grasp_policy ready (cameras {dict(zip(names, topics))})")

    # ------------------------------------------------------------------ params
    def _f(self, name: str) -> float:
        return float(self.get_parameter(name).value)

    def _s(self, name: str) -> str:
        return str(self.get_parameter(name).value)

    def _load_policy(self) -> None:
        from .grasp_policy.runner import PolicyRunner, RunnerConfig

        path = self._s("policy_path")
        if not path:
            raise ValueError("parameter policy_path is empty")
        cfg = RunnerConfig(policy_path=path, mode=self._s("mode"), device=self._s("device"),
                           n_steps=int(self.get_parameter("n_steps").value),
                           task=self._s("task"), max_offset_deg=self._f("max_offset_deg"),
                           revision=self._s("policy_revision") or None)
        self.get_logger().info(f"loading policy {path} ({cfg.mode}, {cfg.device})")
        self._runner = PolicyRunner(cfg)
        missing = set(self._runner.camera_names) - set(self.get_parameter("camera_names").value)
        if missing:
            raise ValueError(f"policy needs cameras {sorted(missing)}; add them to camera_names")
        self.get_logger().info(f"policy loaded: cameras {self._runner.camera_names}, "
                               f"{self._runner.n_steps} steps per inference")

    # ------------------------------------------------------------------ inputs
    def _on_joints(self, msg: JointState) -> None:
        with self._lock:
            for n, q in zip(msg.name, msg.position):
                self._joints[n] = float(q)
            self._joints_t = time.monotonic()

    def _on_image(self, name: str, msg: Image) -> None:
        rgb = imgmsg_to_bgr(msg)[:, :, ::-1]
        with self._lock:
            self._images[name] = np.ascontiguousarray(rgb)
            self._images_t[name] = time.monotonic()

    def _snapshot(self) -> tuple[np.ndarray, float, dict[str, np.ndarray]]:
        stale = self._f("stale_s")
        now = time.monotonic()
        with self._lock:
            if now - self._joints_t > stale:
                raise RuntimeError("no fresh /joint_states")
            missing = [j for j in (*ARM_JOINTS, self._s("gripper_joint")) if j not in self._joints]
            if missing:
                raise RuntimeError(f"/joint_states lacks {missing}")
            arm = np.array([self._joints[j] for j in ARM_JOINTS])
            finger = self._joints[self._s("gripper_joint")]
            needed = self._runner.camera_names if self._runner else []
            old = [n for n in needed if now - self._images_t.get(n, -1e9) > stale]
            if old:
                raise RuntimeError(f"no fresh image from camera(s) {old}")
            images = {n: self._images[n] for n in needed}
        return arm, finger, images

    def _tcp_z(self) -> float:
        tf = self._tf.lookup_transform(self._s("base_frame"), self._s("tcp_frame"), Time(),
                                       timeout=Duration(seconds=0.1))
        return float(tf.transform.translation.z)

    # ------------------------------------------------------------------ outputs
    def _send_arm(self, arm_rad: np.ndarray, dt: float) -> None:
        """One trajectory goal for the whole chunk; the previous goal is cancelled first."""
        from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

        self._cancel_arm()
        traj = JointTrajectory()
        traj.joint_names = list(ARM_JOINTS)
        for i, q in enumerate(arm_rad):
            pt = JointTrajectoryPoint()
            pt.positions = [float(v) for v in q]
            pt.time_from_start = Duration(seconds=(i + 1) * dt).to_msg()
            traj.points.append(pt)
        goal = self._FJT.Goal()
        goal.trajectory = traj
        fut = self._arm.send_goal_async(goal)
        fut.add_done_callback(self._on_arm_goal)

    def _on_arm_goal(self, fut) -> None:
        handle = fut.result()
        if handle is not None and handle.accepted:
            self._arm_goal = handle

    def _cancel_arm(self) -> None:
        handle, self._arm_goal = self._arm_goal, None
        if handle is not None:
            handle.cancel_goal_async()

    def _send_gripper(self, finger_m: float, seconds: float) -> None:
        from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

        traj = JointTrajectory()
        traj.joint_names = [self._s("gripper_joint")]
        pt = JointTrajectoryPoint()
        pt.positions = [float(finger_m)]
        pt.time_from_start = Duration(seconds=max(seconds, 0.05)).to_msg()
        traj.points.append(pt)
        goal = self._FJT.Goal()
        goal.trajectory = traj
        self._grip.send_goal_async(goal)

    def _hold(self) -> None:
        """Freeze the arm where it is now (gripper untouched)."""
        try:
            with self._lock:
                arm = np.array([self._joints[j] for j in ARM_JOINTS])
            self._send_arm(arm[None, :], 0.2)
        except KeyError as exc:
            self.get_logger().warn(f"could not send hold, no state for {exc}")
            self._cancel_arm()

    # ------------------------------------------------------------------ services
    def _on_cancel(self, _req, res):
        self._cancel.set()
        res.success, res.message = True, "cancel requested"
        return res

    def _on_grasp(self, _req, res):
        if not self._busy.acquire(blocking=False):
            res.success, res.message = False, json.dumps({"reason": "already running"})
            return res
        try:
            ok, info = self._run()
        except Exception as exc:  # noqa: BLE001 - report, never leave the arm moving
            self._hold()
            ok, info = False, {"reason": f"error: {exc}"}
            self.get_logger().error(f"learned grasp failed: {exc}")
        finally:
            self._busy.release()
        res.success, res.message = ok, json.dumps(info)
        return res

    def _run(self) -> tuple[bool, dict[str, Any]]:
        if self._runner is None:
            self._load_policy()
        for client, name in ((self._arm, "arm"), (self._grip, "gripper")):
            if not client.wait_for_server(timeout_sec=2.0):
                raise RuntimeError(f"{name} trajectory action server not available")
        self._cancel.clear()
        rate = self._f("rate_hz")
        dt = 1.0 / rate
        timeout = self._f("timeout_s")
        done = GraspDone(DoneConfig(
            closed_ticks=int(self.get_parameter("done_closed_ticks").value),
            settle_ticks=int(self.get_parameter("done_settle_ticks").value),
            settle_m=self._f("done_settle_m"), lift_m=self._f("lift_m")))

        arm, finger, images = self._snapshot()
        self._runner.start(ros_to_data(arm, finger, self.gmap))
        start = time.monotonic()
        info: dict[str, Any] = {"inferences": 0, "clipped": False, "infer_ms": 0.0}
        last_grip_cmd: float | None = None
        finished, reason = False, "timeout"
        n_steps = self._runner.n_steps

        def infer() -> dict[str, Any]:
            """Observe now and predict; the result is stamped with the observation time."""
            arm_, finger_, images_ = self._snapshot()
            t_obs = time.monotonic()
            acts, clip = self._runner.predict(ros_to_data(arm_, finger_, self.gmap), images_,
                                              n=self._runner.chunk_size)
            return {"t_obs": t_obs, "actions": acts, "clipped": clip,
                    "ms": (time.monotonic() - t_obs) * 1000}

        def start_infer() -> tuple[threading.Thread, dict[str, Any]]:
            box: dict[str, Any] = {}

            def work():
                try:
                    box.update(infer())
                except Exception as exc:  # noqa: BLE001 - re-raised in the control loop
                    box["error"] = exc
            th = threading.Thread(target=work, daemon=True)
            th.start()
            return th, box

        pred = infer()
        while not finished:
            if self._cancel.is_set():
                reason = "cancelled"
                break
            if time.monotonic() - start > timeout:
                break
            info["inferences"] += 1
            info["clipped"] = info["clipped"] or pred["clipped"]
            info["infer_ms"] = round(pred["ms"], 1)
            # Actions are timed from the observation; drop those whose time has passed
            # (inference latency), then execute the next n_steps.
            skip = int(round((time.monotonic() - pred["t_obs"]) / dt))
            actions = pred["actions"][skip:skip + n_steps]
            if len(actions) == 0:
                pred = infer()
                continue
            ros = [data_to_ros(a, self.gmap) for a in actions]
            self._send_arm(np.array([r[0] for r in ros]), dt)
            chunk_t0 = time.monotonic()
            # start the next inference early enough to be ready when this chunk ends
            lead = min(len(actions), int(np.ceil(pred["ms"] / 1000 / dt)) + 1)
            pending = None
            for i, (a, (_, grip_m)) in enumerate(zip(actions, ros)):
                if pending is None and i >= len(actions) - lead:
                    pending = start_infer()
                if last_grip_cmd is None or abs(grip_m - last_grip_cmd) > 0.002:
                    self._send_gripper(grip_m, dt)
                    last_grip_cmd = grip_m
                wait = chunk_t0 + (i + 1) * dt - time.monotonic()
                if wait > 0:
                    time.sleep(wait)
                if self._cancel.is_set():
                    break
                with self._lock:
                    finger = self._joints.get(self._s("gripper_joint"), finger)
                if done.update(self.gmap.data_is_closed(float(a[6])), finger, self._tcp_z()):
                    finished, reason = True, "gripped and lifted"
                    break
                self._publish_status(done, start, finger, info)
            if pending is None:
                pending = start_infer()
            pending[0].join()
            if "error" in pending[1]:
                raise pending[1]["error"]
            pred = pending[1]

        self._hold()
        with self._lock:
            finger = self._joints.get(self._s("gripper_joint"), float("nan"))
        info.update(reason=reason, lifted_m=round(done.lifted_m, 4), phase=done.phase,
                    finger_m=round(float(finger), 4),
                    finger_at_grip_m=done.finger_at_grip,
                    elapsed_s=round(time.monotonic() - start, 2))
        self.get_logger().info(f"learned grasp: {info}")
        return finished, info

    def _publish_status(self, done: GraspDone, start: float, finger: float, info: dict) -> None:
        msg = String()
        msg.data = json.dumps({"phase": done.phase, "lifted_m": round(done.lifted_m, 4),
                               "finger_m": round(float(finger), 4),
                               "elapsed_s": round(time.monotonic() - start, 2),
                               "inferences": info["inferences"]})
        self._status.publish(msg)


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = GraspPolicyNode()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
