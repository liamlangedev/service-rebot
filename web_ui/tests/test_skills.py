"""Tests for ROS-free SkillRunner and VLAPolicyClient."""

from types import SimpleNamespace

import numpy as np

from web_ui.agent.events import EventLog
from web_ui.perception.scene import SceneModel
from web_ui.skills.skills import SkillRunner
from web_ui.skills.vla_policy import VLAPolicyClient
from web_ui.types import Detection


def _fake_camera(frame):
    return SimpleNamespace(
        wait_fresh=lambda timeout_s=2.0: frame,
        latest=lambda max_age_s=2.0: frame,
    )


def test_detect_and_list_objects():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    det = Detection("can", 0.9, (10.0, 10.0, 50.0, 50.0))
    detector = SimpleNamespace(classes=["can"], set_vocabulary=lambda c: None, detect=lambda _f: [det])
    runner = SkillRunner(
        places={},
        scene=SceneModel(),
        camera=_fake_camera(frame),
        detector=detector,
        vla=VLAPolicyClient({"backend": "stub"}),
        events=EventLog(),
    )
    res = runner("list_objects", {})
    assert not res.is_error
    assert res.payload["count"] == 1


def test_run_vla_policy_dry_run_and_stub_error():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    cams = {"table": _fake_camera(frame), "front": _fake_camera(frame), "wrist": _fake_camera(frame)}
    vla = VLAPolicyClient({"backend": "stub"})

    dry_runner = SkillRunner(
        places={}, scene=SceneModel(), camera=cams["table"], detector=None,
        vla=vla, events=EventLog(), cameras=cams, plan_only=True,
    )
    dry_res = dry_runner("run_vla_policy", {"instruction": "pick up the can", "object": "can", "destination": "metal"})
    assert not dry_res.is_error
    assert dry_res.payload["executed"] is False
    assert dry_res.payload["cameras"] == ["front", "table", "wrist"]

    live_runner = SkillRunner(
        places={}, scene=SceneModel(), camera=cams["table"], detector=None,
        vla=vla, events=EventLog(), cameras=cams, plan_only=False,
    )
    live_res = live_runner("run_vla_policy", {"instruction": "pick up the can"})
    assert live_res.is_error
    assert "stub" in live_res.payload["error"]


def test_cancel_stops_skill_execution():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    runner = SkillRunner(
        places={}, scene=SceneModel(), camera=_fake_camera(frame), detector=None,
        vla=VLAPolicyClient({"backend": "stub"}), events=EventLog(), plan_only=True,
    )
    runner.cancel()
    res = runner("run_vla_policy", {"instruction": "pick up the can"})
    assert res.is_error
    assert res.payload["cancelled"] is True
