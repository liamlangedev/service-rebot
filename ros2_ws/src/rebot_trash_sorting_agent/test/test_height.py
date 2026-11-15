"""Synthetic metric-camera checks; no ROS graph or robot required."""

import numpy as np
import pytest
from rebot_trash_sorting_agent.perception.height import HeightCamera
from rebot_trash_sorting_agent.types import Detection, WorldObject


def camera():
    return HeightCamera(np.array([[700, 0, 320, 320], [0, 700, -300, 400], [0, 0, 1, 1]]), (640, 480))


def calibration_points():
    return np.array(
        [
            [horizontal, lateral, height]
            for horizontal in (-0.2, 0.0, 0.2)
            for lateral in (-0.15, 0.15)
            for height in (0.0, 0.08, 0.2)
        ],
    )


def test_fit_and_round_trip():
    import cv2

    intrinsic = np.array([[700.0, 0, 320], [0, 700.0, 240], [0, 0, 1.0]])
    rotation, _ = cv2.Rodrigues(np.array([2.0, 0.1, -0.1]))
    original = HeightCamera(intrinsic @ np.column_stack((rotation, [0.0, 0.0, 0.8])), (640, 480))
    points = calibration_points()[::3]
    fitted = HeightCamera.fit_table(original.project(points), points[:, :2], 0.0, (640, 480), intrinsic)
    restored = HeightCamera.from_mapping(fitted.to_mapping())
    assert restored is not None
    assert np.allclose(restored.project(calibration_points()), original.project(calibration_points()), atol=1e-5)
    assert fitted.meta["error_px"] < 1e-5


def test_refuses_degenerate_calibration():
    points = np.array([[0, 0], [0.1, 0], [0.2, 0], [0.3, 0], [0.4, 0]])
    with pytest.raises(ValueError, match="degenerate"):
        HeightCamera.fit_table(np.zeros((5, 2)), points, 0, (640, 480), np.eye(3))


def object_detection(model, obj, height):
    angles = np.linspace(0, 2 * np.pi, 32, endpoint=False)
    points = [
        [obj.x + obj.width_m / 2 * np.cos(angle), obj.y + obj.width_m / 2 * np.sin(angle), obj.z + elevation]
        for angle in angles
        for elevation in (0, height)
    ]
    pixels = model.project(points)
    bounds = (*pixels.min(axis=0), *pixels.max(axis=0))
    return Detection(obj.label, 0.9, bounds, tuple(map(tuple, pixels)))


@pytest.mark.parametrize("height", [0.02, 0.075, 0.13, 0.24])
def test_measures_height_including_nonzero_table_and_footprint(height):
    model = camera()
    obj = WorldObject("can", 0.02, -0.03, 0.025, width_m=0.05)
    detection = object_detection(model, obj, height)
    result = model.estimate_heights([obj], [detection], (640, 480))
    assert result[0] == pytest.approx(height, abs=1e-6)


def test_refuses_wrong_resolution_and_out_of_range_height():
    model = camera()
    obj = WorldObject("can", 0, 0, 0)
    detection = object_detection(model, obj, 0.5)
    assert model.estimate_heights([obj], [detection], (640, 480)) == {}
    with pytest.raises(ValueError, match="resolution"):
        model.estimate_heights([obj], [detection], (1280, 720))


def test_refuses_ambiguous_or_wrong_label_matches():
    model = camera()
    obj = WorldObject("can", 0, 0, 0)
    detection = object_detection(model, obj, 0.1)
    assert model.estimate_heights([obj], [detection, detection], (640, 480)) == {}
    assert model.estimate_heights([obj, obj], [detection], (640, 480)) == {}
    other = Detection("cup", 0.9, detection.bbox)
    assert model.estimate_heights([obj], [other], (640, 480)) == {}


@pytest.mark.parametrize("approximate", [False, True])
@pytest.mark.parametrize("legacy_flag", [False, True])
def test_calibration_records_five_marks_once_then_clicks_both_views(tmp_path, monkeypatch, approximate, legacy_flag):
    import cv2
    import yaml
    from rebot_trash_sorting_agent import calibrate_table
    from rebot_trash_sorting_agent.config import Config

    intrinsic = np.array([[700.0, 0, 320], [0, 700.0, 240], [0, 0, 1.0]])
    rotation, _ = cv2.Rodrigues(np.array([2.0, 0.1, -0.1]))
    model = HeightCamera(intrinsic @ np.column_stack((rotation, [0.0, 0.0, 0.8])), (640, 480))
    points = [(-0.15, -0.1), (0.15, -0.1), (-0.15, 0.1), (0.15, 0.1), (0.0, 0.0)]
    pixels = model.project([[horizontal, lateral, 0] for horizontal, lateral in points]).tolist()
    config = Config(
        tmp_path,
        {},
        {
            "cameras": [
                {"name": "table", "width": 640, "height": 480},
                {
                    "name": "front_camera",
                    "width": 640,
                    "height": 480,
                    "camera_matrix": None if approximate else intrinsic.tolist(),
                    "fov_deg": float(np.degrees(2 * np.arctan(320 / 700))) if approximate else 30.0,
                },
            ],
        },
        {},
        {"table": {"z": 0}},
    )
    monkeypatch.setattr(calibrate_table.Config, "load", lambda _directory: config)
    recorded, captured, clicked = [], [], []

    def record(count, topic):
        recorded.append((count, topic))
        return points

    def capture(name, directory):
        captured.append(name)
        return np.zeros((480, 640, 3), dtype=np.uint8)

    def click(image, expected):
        clicked.append(expected)
        return pixels

    monkeypatch.setattr(calibrate_table, "_record_from_arm", record)
    monkeypatch.setattr(calibrate_table, "_grab_frame", capture)
    monkeypatch.setattr(calibrate_table, "_click_points", click)
    output = tmp_path / "calibration.yaml"
    output.write_text("wrist: {unchanged: true}\n")
    options = ["--from-arm", "--count", "5", "--out", str(output)]
    if legacy_flag:
        options.append("--allow-approximate-intrinsics")
    calibrate_table.main(options)
    saved = yaml.safe_load(output.read_text())
    assert recorded == [(5, "/joint_states")]
    assert captured == ["table", "front_camera"]
    assert clicked == [5, 5]
    assert saved["wrist"] == {"unchanged": True}
    assert "homography" in saved["table"]
    assert "homography" in saved["front_camera"]
    assert saved["front_camera"]["height_camera"]["approximate_intrinsics"] is approximate
    restored = HeightCamera.from_mapping(saved["front_camera"]["height_camera"])
    assert np.allclose(restored.project([[0, 0, 0.1]]), model.project([[0, 0, 0.1]]), atol=1e-4)


def test_front_observation_updates_scene_height_and_grasp_then_clears_on_failure():
    from types import SimpleNamespace

    from rebot_trash_sorting_agent.skills.grasp import plan_grasp
    from rebot_trash_sorting_agent.skills.skills import SkillRunner

    model = camera()
    obj = WorldObject("can", 0, 0, 0, width_m=0.05)
    detection = object_detection(model, obj, 0.2)
    runner = SkillRunner(
        places={"table": {"z": 0}},
        motion_cfg={},
        scene=None,
        camera=None,
        detector=SimpleNamespace(detect=lambda _frame: [detection]),
        motion=None,
        gripper=None,
        events=SimpleNamespace(emit=lambda *_args, **_kwargs: None),
        height_camera=model,
        front_camera=SimpleNamespace(wait_fresh=lambda _timeout: np.zeros((480, 640, 3))),
    )
    assert "estimated 1/1" in runner._update_heights([obj])
    assert obj.height_m == pytest.approx(0.2, abs=1e-6)
    grasp = plan_grasp(obj, {}, 0)
    assert grasp.best.pinch_m == pytest.approx(0.12, abs=1e-6)
    assert grasp.pre_grasp.z >= 0.24 - 1e-6
    runner.front_camera = None
    runner._update_heights([obj])
    assert obj.height_m is None
    assert plan_grasp(obj, {"grasp": {"pinch_heights_m": [0.06]}}, 0).best.pinch_m == pytest.approx(0.06)
