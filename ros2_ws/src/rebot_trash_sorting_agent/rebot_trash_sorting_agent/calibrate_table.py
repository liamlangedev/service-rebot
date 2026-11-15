#!/usr/bin/env python3
"""Fit the table-plane homography: image pixels -> base_link metres.

Record table marks once, then click them in the table and front_camera views.
Front-view height uses camera_matrix from cameras.yaml when available, otherwise
intrinsics are approximated from the configured FOV automatically. Approximate
heights must be checked against measured objects.

Procedure

1. Put four or more marks on the table at known or reachable locations (masking
   tape crosses are fine). Pick them spread over the reachable area, not clustered.
2. Either record each mark's ``base_link`` (x, y) using the arm itself (recommended),
   or measure them manually:

   - **From the arm (``--from-arm``)**: to move the arm by hand, disable the
     arm motors (``/rebotarm/joint_states`` keeps publishing). **WARNING: the
     arm will drop immediately when disabled — support/catch it with your hand
     before calling:**

         ros2 service call /rebotarm/disable std_srvs/srv/Trigger "{}"

     Keep the gripper **closed** so the fingertips meet at the TCP, touch the
     closed gripper tip to each mark in turn and press Enter to record its FK
     position, then move the arm out of the camera view and click the same
     marks in the same order:

         ros2 run rebot_trash_sorting_agent calibrate_table \
             --from-arm --count 5 --joint-states-topic /rebotarm/joint_states

   - **Manual coordinates (``--points``)**: measure (x, y) in ``base_link``
     (x straight ahead of the arm, y to its left) and pass them in click order:

         ros2 run rebot_trash_sorting_agent calibrate_table \
             --points "0.15,-0.20;0.45,-0.20;0.15,0.20;0.45,0.20;0.30,0.00"

For a headless machine pass the pixel coordinates too and no window opens:

    ... --pixels "412,610;1010,608;395,240;1020,236"

The result goes to ``config/calibration.yaml`` (updating both the workspace
source ``config/`` when present and the installed config directory, not
``cameras.yaml``), so hand-written comments in the config survive every
recalibration. It is printed as well, so it can be pasted into
``cameras.yaml -> table_map`` if you prefer.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

from rebot_trash_sorting_agent.config import Config
from rebot_trash_sorting_agent.perception.height import HeightCamera
from rebot_trash_sorting_agent.perception.table_map import TableMap


def _parse_pairs(text: str, label: str) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for chunk in (text or "").replace(";", " ").replace("\n", " ").split():
        parts = chunk.split(",")
        if len(parts) != 2:
            raise SystemExit(f"{label}: expected 'a,b' pairs, got {chunk!r}")
        out.append((float(parts[0]), float(parts[1])))
    return out


def _grab_frame(camera: str, config_dir: str | None) -> np.ndarray:
    """Take one frame from the camera topic (needs camera_node running)."""
    import rclpy
    from rclpy.node import Node

    from .perception.scene import CameraClient

    config = Config.load(config_dir)
    topic = config.capture_topic(camera)
    rclpy.init()
    node = Node("calibrate_table")
    client = CameraClient(node, topic, timeout_s=10.0)
    node.get_logger().info(f"waiting for a frame on {topic}")
    deadline = time.monotonic() + 10.0
    frame = None
    while time.monotonic() < deadline:
        rclpy.spin_once(node, timeout_sec=0.1)
        frame = client.latest(max_age_s=2.0)
        if frame is not None:
            break
    node.destroy_node()
    rclpy.shutdown()
    if frame is None:
        raise SystemExit(
            f"no frame on {topic}: is camera_node running? (ros2 launch rebot_trash_sorting_agent agent.launch.py)",
        )
    return frame


def _click_points(image: np.ndarray, expected: int) -> list[tuple[float, float]]:
    import cv2

    points: list[tuple[float, float]] = []
    window = "calibrate_table - click points, Enter=accept, r=reset, Esc=abort"

    def on_mouse(event, x, y, _flags, _param):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < expected:
            points.append((float(x), float(y)))
            print(f"  point {len(points)}: pixel ({x}, {y})")

    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window, on_mouse)
    while True:
        canvas = image.copy()
        for index, (x, y) in enumerate(points, start=1):
            cv2.circle(canvas, (int(x), int(y)), 6, (0, 0, 255), -1)
            cv2.putText(
                canvas,
                str(index),
                (int(x) + 9, int(y) - 9),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
        cv2.putText(
            canvas,
            f"{len(points)}/{expected} points",
            (12, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 200, 0),
            2,
            cv2.LINE_AA,
        )
        cv2.imshow(window, canvas)
        key = cv2.waitKey(30) & 0xFF
        if key in (13, 10, 32) and points:
            break
        if key in (ord("r"), ord("R")):
            points.clear()
        if key == 27:
            cv2.destroyAllWindows()
            raise SystemExit("aborted")
    cv2.destroyAllWindows()
    return points


def _write(out: Path, camera: str, table_map: TableMap) -> None:
    import yaml

    data: dict = {}
    if out.is_file():
        try:
            data = yaml.safe_load(out.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            data = {}
    data[camera] = table_map.to_mapping()
    out.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "# Written by calibrate_table.py. One homography per camera:\n"
        "# [u, v, 1] * H -> [x, y, 1] in metres on the table plane (z = places.yaml table.z).\n"
        "# Regenerate after moving the camera; this file is disposable.\n"
    )
    out.write_text(header + yaml.safe_dump(data, sort_keys=False, default_flow_style=False), encoding="utf-8")


def _record_from_arm(count: int, joint_states_topic: str) -> list[tuple[float, float]]:
    """Compute gripper-tip (x, y) in base_link from live /joint_states via MuJoCo FK."""
    import os

    import mujoco
    import rclpy
    from rclpy.node import Node
    from rclpy.qos import qos_profile_sensor_data
    from sensor_msgs.msg import JointState

    os.environ.setdefault("MUJOCO_GL", "egl")
    teleop_dir = None
    here = Path(__file__).resolve()
    for parent in (here, *here.parents):
        cand = parent / "teleoperation"
        if (cand / "teleop" / "rebot_model.py").is_file():
            teleop_dir = cand
            break
    if teleop_dir is None:
        raise SystemExit("cannot locate teleoperation/teleop/rebot_model.py for FK")
    if str(teleop_dir) not in sys.path:
        sys.path.insert(0, str(teleop_dir))
    from teleop.rebot_model import build_spec

    model = build_spec().compile()
    data = mujoco.MjData(model)
    end_id = model.body("end_link").id
    arm_joints = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
    qpos_adr = [model.jnt_qposadr[model.joint(n).id] for n in arm_joints]
    tip_offset = np.array([0.02858, 0.0, 0.0])  # gripper_tcp in end_link

    rclpy.init()
    node = Node("calibrate_table_fk")
    latest: dict[str, float] = {}

    def on_js(msg: JointState) -> None:
        for name, pos in zip(msg.name, msg.position):
            latest[name] = float(pos)

    node.create_subscription(JointState, joint_states_topic, on_js, qos_profile_sensor_data)
    print(f"waiting for joint states on {joint_states_topic} ...")
    deadline = time.monotonic() + 10.0
    while time.monotonic() < deadline and not all(j in latest for j in arm_joints):
        rclpy.spin_once(node, timeout_sec=0.1)
    if not all(j in latest for j in arm_joints):
        node.destroy_node()
        rclpy.shutdown()
        raise SystemExit(
            f"no joint states on {joint_states_topic} "
            "(is the arm driver running? try --joint-states-topic /rebotarm/joint_states)",
        )

    points: list[tuple[float, float]] = []
    try:
        for idx in range(1, count + 1):
            ans = input(f"Move closed gripper tip onto mark {idx}/{count}, then press Enter (q=abort): ")
            if ans.strip().lower() == "q":
                raise SystemExit("aborted")
            for _ in range(5):
                rclpy.spin_once(node, timeout_sec=0.02)
            for name, adr in zip(arm_joints, qpos_adr):
                data.qpos[adr] = latest[name]
            mujoco.mj_kinematics(model, data)
            tip = data.xpos[end_id] + data.xmat[end_id].reshape(3, 3) @ tip_offset
            print(f"  point {idx}: x={tip[0]:+.4f} y={tip[1]:+.4f} (z={tip[2]:+.4f})")
            points.append((float(tip[0]), float(tip[1])))
        input("Move the arm out of the way so all marks are visible, then press Enter to capture frame...")
    finally:
        node.destroy_node()
        rclpy.shutdown()
    return points


def _source_config_dir() -> Path | None:
    """Return the git-tracked package config directory if running inside the workspace."""
    for base in (Path(__file__).resolve(), Path.cwd().resolve()):
        for parent in (base, *base.parents):
            candidate = parent / "src" / "rebot_trash_sorting_agent" / "config"
            if (candidate / "cameras.yaml").is_file():
                return candidate
            if parent.name == "rebot_trash_sorting_agent" and (parent / "config" / "cameras.yaml").is_file():
                return parent / "config"
    return None


def _calibrate_view(
    args: argparse.Namespace,
    config: Config,
    camera: str,
    table_points: list[tuple[float, float]],
    first: bool,
) -> TableMap:
    import cv2

    cfg = config.camera(camera)
    front = camera == "front_camera"
    image_path = args.front_image if front and args.front_image else args.image if first else None
    pixel_text = args.front_pixels if front and args.front_pixels else args.pixels if first else None
    if image_path:
        image = cv2.imread(image_path)
        if image is None:
            raise SystemExit(f"cannot read image {image_path}")
    elif pixel_text:
        image = np.empty((int(cfg.get("height", 480)), int(cfg.get("width", 640)), 3), dtype=np.uint8)
    else:
        print(f"\n{camera}: capture the same table marks, with the arm out of view")
        image = _grab_frame(camera, args.config_dir)
    if pixel_text:
        pixels = _parse_pairs(pixel_text, f"{camera} pixels")
    else:
        print(f"{camera}: click {len(table_points)} marks in this order:")
        for index, (horizontal, lateral) in enumerate(table_points, start=1):
            print(f"  {index}: x={horizontal:+.3f} y={lateral:+.3f}")
        pixels = _click_points(image, len(table_points))
    if len(pixels) != len(table_points):
        raise SystemExit(f"{camera}: got {len(pixels)} pixels for {len(table_points)} marks")
    table_z = float(config.table().get("z", 0.0))
    table_map = TableMap.fit(pixels, table_points, table_z)
    error = table_map.reprojection_error_mm(pixels, table_points)
    print(f"{camera}: mean table reprojection error {error:.1f} mm")
    if not np.isfinite(error) or (error > args.max_error_mm and not args.force):
        raise SystemExit(f"{camera}: table error exceeds --max-error-mm; check point order and measurements")
    table_map.meta.update(error_mm=round(error, 2), camera=camera, points=len(pixels))
    if front:
        intrinsic = cfg.get("camera_matrix")
        approximate = intrinsic is None
        image_size = (image.shape[1], image.shape[0])
        if approximate and args.allow_approximate_intrinsics:
            focal = image_size[0] / (2 * np.tan(np.radians(float(cfg.get("fov_deg", 75))) / 2))
            intrinsic = [[focal, 0, image_size[0] / 2], [0, focal, image_size[1] / 2], [0, 0, 1]]
            print("WARNING: front_camera height uses approximate horizontal FOV intrinsics")
        if intrinsic is not None:
            try:
                model = HeightCamera.fit_table(
                    pixels,
                    table_points,
                    table_z,
                    image_size,
                    intrinsic,
                    cfg.get("distortion") or (),
                )
            except (ValueError, cv2.error) as exc:
                raise SystemExit(f"front_camera height calibration failed: {exc}") from exc
            if model.meta["max_error_px"] > args.max_error_px and not args.force:
                raise SystemExit("front_camera pose reprojection error exceeds --max-error-px; check intrinsics")
            model.meta["approximate_intrinsics"] = approximate
            table_map.meta["height_camera"] = model.to_mapping()
            print(f"front_camera: height pose mean error {model.meta['error_px']:.2f} px")
        else:
            print("front_camera: XY saved only; set camera_matrix or pass --allow-approximate-intrinsics for height")
    return table_map


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cameras = parser.add_mutually_exclusive_group()
    cameras.add_argument("--camera", default=None, help="calibrate just one camera (legacy mode)")
    cameras.add_argument(
        "--cameras",
        nargs="+",
        default=None,
        help="camera names in capture order (default: table front_camera)",
    )
    parser.add_argument("--config-dir", default=None)
    parser.add_argument("--points", default=None, help="base_link coordinates 'x,y;x,y;...' in click order (metres)")
    parser.add_argument(
        "--from-arm",
        action="store_true",
        help="record base_link (x, y) from live joint_states FK by touching each mark",
    )
    parser.add_argument("--count", type=int, default=5, help="number of marks to record when using --from-arm")
    parser.add_argument(
        "--joint-states-topic",
        default="/joint_states",
        help="JointState topic for --from-arm (e.g. /joint_states or /rebotarm/joint_states)",
    )
    parser.add_argument("--pixels", default=None, help="skip the window: 'u,v;u,v;...' in the same order")
    parser.add_argument("--image", default=None, help="use this still instead of the live topic")
    parser.add_argument("--front-image", default=None, help="front_camera still for the second click set")
    parser.add_argument("--front-pixels", default=None, help="headless front_camera pixel coordinates")
    parser.add_argument(
        "--allow-approximate-intrinsics",
        action="store_true",
        default=True,
        help="use horizontal fov_deg when camera_matrix is unset (already enabled by default)",
    )
    parser.add_argument(
        "--max-error-px",
        type=float,
        default=5.0,
        help="maximum front-camera pose reprojection error in pixels",
    )
    parser.add_argument("--out", default=None, help="default: <config_dir>/calibration.yaml")
    parser.add_argument(
        "--max-error-mm",
        type=float,
        default=10.0,
        help="refuse to save above this mean reprojection error",
    )
    parser.add_argument("--force", action="store_true", help="save even above the error limit")
    args, _unknown = parser.parse_known_args(argv)

    config = Config.load(args.config_dir)
    names = args.cameras or ([args.camera] if args.camera else ["table", "front_camera"])
    if len(set(names)) != len(names):
        raise SystemExit("camera names must not repeat")
    for name in names:
        config.camera(name)
    if args.from_arm:
        table_points = _record_from_arm(args.count, args.joint_states_topic)
    elif args.points:
        table_points = _parse_pairs(args.points, "--points")
    else:
        raise SystemExit("pass either --points 'x1,y1;...' or --from-arm")
    if len(table_points) < 4:
        raise SystemExit("need at least 4 table points (6-8 spread out is better)")

    maps = {name: _calibrate_view(args, config, name, table_points, index == 0) for index, name in enumerate(names)}
    if args.out:
        targets = [Path(args.out).expanduser()]
    elif args.config_dir:
        targets = [config.directory / "calibration.yaml"]
    else:
        src_config = _source_config_dir()
        targets = [src_config / "calibration.yaml"] if src_config is not None else []
        install_out = config.directory / "calibration.yaml"
        if not targets or install_out.resolve() != targets[0].resolve():
            targets.append(install_out)

    for out in targets:
        for name, table_map in maps.items():
            _write(out, name, table_map)
        print(f"\nsaved {out}")
    print("restart agent_node (or the launch file) to pick it up")


if __name__ == "__main__":
    main()
