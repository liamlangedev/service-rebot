"""Torque/position grasp judgement - pure functions, no ROS graph.

Run with:  python3 -m pytest ros2_ws/src/rebot_trash_sorting_agent/test
"""

from rebot_trash_sorting_agent.skills.gripper import judge_holding, judge_slip

CLOSED_M = 0.0
GAP_M = 0.004
DELTA_NM = 0.15


def hold(position, torque, baseline=0.02):
    return judge_holding(position, CLOSED_M, torque, baseline, GAP_M, DELTA_NM)


def test_closed_on_air_is_not_a_grasp():
    assert hold(0.0, None) is False
    assert hold(0.002, 1.0) is False  # 2 mm < 4 mm gap: nothing there


def test_position_only_when_torque_is_missing():
    # Mock hardware reports zero effort, which the client turns into None.
    assert hold(0.021, None) is True


def test_torque_confirms_a_soft_object():
    assert hold(0.021, 0.30) is True


def test_position_alone_is_not_enough_when_torque_is_flat():
    # Finger stopped early, but the motor is pushing no harder than in free air:
    # something springy, or the object slipped out and the finger is resting on it.
    assert hold(0.021, 0.05, baseline=0.02) is False


def test_slip_is_detected_by_position_or_torque():
    reference = {"position": 0.021, "torque": 0.60}
    assert judge_slip(0.021, 0.60, reference, 0.003, 0.10) is False
    assert judge_slip(0.010, 0.60, reference, 0.003, 0.10) is True  # finger closed further
    assert judge_slip(0.021, 0.40, reference, 0.003, 0.10) is True  # torque collapsed
    assert judge_slip(None, None, reference, 0.003, 0.10) is False  # no telemetry


def test_negative_torque_and_finger_opening_also_detect_slip():
    reference = {"position": 0.021, "torque": -0.6, "baseline_torque": -0.02}
    assert judge_slip(0.021, -0.3, reference, 0.003, 0.10)
    assert judge_slip(0.03, -0.6, reference, 0.003, 0.10)
    assert not judge_slip(0.021, -0.7, reference, 0.003, 0.10)


def test_hold_guard_debounces_slip_and_fails_on_missing_feedback(monkeypatch):
    from types import SimpleNamespace

    import pytest
    from rebot_trash_sorting_agent.skills.gripper import GripperClient, HoldLost

    clock = [0.0]
    state = {"holding": False, "feedback_missing": False}
    monkeypatch.setattr("rebot_trash_sorting_agent.skills.gripper.time.monotonic", lambda: clock[0])
    client = SimpleNamespace(_slip_debounce_s=0.15, hold_snapshot=lambda reference: state)
    guard = GripperClient.hold_guard(client, {})
    guard()
    clock[0] = 0.1
    guard()
    state["holding"] = True
    guard()
    state["holding"] = False
    guard()
    clock[0] = 0.3
    with pytest.raises(HoldLost):
        guard()
    state["feedback_missing"] = True
    with pytest.raises(HoldLost, match="feedback"):
        GripperClient.hold_guard(client, {})()


def test_stable_hold_requires_continuous_success(monkeypatch):
    from types import SimpleNamespace

    from rebot_trash_sorting_agent.skills.gripper import GripperClient

    clock = [0.0]
    monkeypatch.setattr("rebot_trash_sorting_agent.skills.gripper.time.monotonic", lambda: clock[0])
    monkeypatch.setattr(
        "rebot_trash_sorting_agent.skills.gripper.time.sleep", lambda seconds: clock.__setitem__(0, clock[0] + seconds)
    )
    client = SimpleNamespace(
        _stable_s=0.1, _hold_timeout_s=0.5, hold_snapshot=lambda reference: {"holding": clock[0] > 0.08}
    )
    result = GripperClient.stable_hold(client)
    assert result["holding"] and clock[0] >= 0.18
    client.hold_snapshot = lambda reference: {"holding": False}
    assert not GripperClient.stable_hold(client)["holding"]
