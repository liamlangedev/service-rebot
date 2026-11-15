"""Composable tool checks using fake motion and gripper clients."""

from types import SimpleNamespace

import numpy as np
from rebot_trash_sorting_agent.skills.skills import SkillRunner
from rebot_trash_sorting_agent.types import Detection, WorldObject


def runner(plan_only=False, holding=None):
    calls = []
    obj = WorldObject("can", 0.22, 0, 0, height_m=0.13)
    scene = SimpleNamespace(all=lambda: [obj], remove=lambda label: calls.append(("remove", label)))
    motion = SimpleNamespace(
        ik_feasible=lambda pose: True,
        move_to_pose=lambda pose, **kwargs: (
            calls.append(("move", pose, kwargs)) or {"executed": not kwargs.get("plan_only", False)}
        ),
    )
    gripper = SimpleNamespace(
        open=lambda: calls.append(("open",)) or {},
        close=lambda: calls.append(("close",)) or {"holding": True, "position": 0.02},
        check_hold=lambda reference: {"holding": True, "slipped": False},
    )
    skill = SkillRunner(
        places={"table": {"z": 0}},
        motion_cfg={},
        scene=scene,
        camera=None,
        detector=None,
        motion=motion,
        gripper=gripper,
        events=SimpleNamespace(emit=lambda *args, **kwargs: None),
        table_map=object(),
        plan_only=plan_only,
        holding=holding,
    )
    return skill, calls


def test_move_above_does_not_grasp_or_place():
    skill, calls = runner()
    result = skill("move_above_object", {"object": "can"})
    assert not result.is_error
    assert len(calls) == 1 and calls[0][0] == "move"
    assert calls[0][1].z >= 0.23


def test_grasp_is_standalone_and_holding_survives_runner_recreation():
    state = {}
    skill, calls = runner(holding=state)
    result = skill("grasp_object", {"object": "can"})
    assert not result.is_error and result.payload["holding"]
    assert sum(call[0] == "open" for call in calls) == 1
    assert state["object"].label == "can"
    next_skill, _ = runner(holding=state)
    assert next_skill("grasp_object", {"object": "can"}).is_error


def test_invalid_or_unreachable_motion_and_unknown_objects_do_not_move():
    skill, calls = runner()
    assert skill("move_to_pose", {"x": 0.2, "y": 0, "z": -0.1}).is_error
    assert skill("move_to_pose", {"x": float("nan"), "y": 0, "z": 0.2}).is_error
    assert skill("move_above_object", {"object": "bottle"}).is_error
    assert not calls


def test_dry_run_grasp_and_gripper_never_actuate_or_change_holding():
    skill, calls = runner(plan_only=True)
    assert not skill("grasp_object", {"object": "can"}).is_error
    assert not skill("open_gripper", {}).is_error
    assert not skill("close_gripper", {}).is_error
    assert not calls and not skill.holding


def test_detection_accepts_classes_and_returns_pixel_geometry_without_calibration():
    skill, calls = runner()
    skill.table_map = None
    skill.camera = SimpleNamespace(wait_fresh=lambda timeout: np.zeros((120, 120, 3)))
    vocabulary = []
    skill.detector = SimpleNamespace(
        set_vocabulary=lambda classes: vocabulary.extend(classes),
        detect=lambda frame: [Detection("wrapper", 0.8, (10, 10, 40, 40), ((10, 10), (40, 10), (40, 40)))],
    )
    skill.scene.update = lambda detections, table_map: []
    skill.baseline_classes = ["can"]
    result = skill("detect_objects", {"classes": ["wrapper"]})
    assert not result.is_error
    assert vocabulary == ["wrapper", "can"]
    assert result.payload["detections"][0]["polygon"]
    assert not calls

    def test_tool_schemas_expose_composable_actions_and_discovery():
        from rebot_trash_sorting_agent.agent.tools import TOOL_NAMES, TOOLS

        assert {
            "detect_objects",
            "move_above_object",
            "move_to_pose",
            "grasp_object",
            "place_object",
            "open_gripper",
            "close_gripper",
            "pick_and_place",
            "list_objects",
        } <= TOOL_NAMES
        schemas = {tool.name: tool.parameters for tool in TOOLS}
        assert "classes" in schemas["detect_objects"]["properties"]
        assert "classes" in schemas["list_objects"]["properties"]
        assert schemas["move_to_pose"]["required"] == ["x", "y", "z"]

    def test_standalone_place_and_composed_pick_place_share_the_same_primitives():
        from rebot_trash_sorting_agent.skills.poses import ToolPose
        from rebot_trash_sorting_agent.types import PlaceTarget

        for composed in (False, True):
            skill, calls = runner()
            release = ToolPose(0.2, 0.3, 0.2)
            skill._reachable_place = lambda destination, objects: (
                PlaceTarget("bin_0", 0.2, 0.3, 0.2, kind="bin"),
                release,
                release.offset(dz=0.1),
                [],
            )
            if composed:
                result = skill("pick_and_place", {"object": "can", "destination": "bin_0"})
            else:
                assert not skill("grasp_object", {"object": "can"}).is_error
                result = skill("place_object", {"destination": "bin_0"})
            assert not result.is_error
            assert result.payload["destination"] == "bin_0"
            assert not skill.holding
            assert sum(call[0] == "close" for call in calls) == 1
            assert sum(call[0] == "open" for call in calls) == 2

    def test_error_after_close_preserves_holding_state_and_cancel_stops_motion():
        skill, calls = runner()
        original = skill.motion.move_to_pose

        def fail_lift(pose, **kwargs):
            if kwargs.get("label") == "lift":
                raise RuntimeError("lift failed")
            return original(pose, **kwargs)

        skill.motion.move_to_pose = fail_lift
        assert skill("grasp_object", {"object": "can"}).is_error
        assert skill.holding["object"].label == "can"
        before = len(calls)
        skill.cancel()
        result = skill("open_gripper", {})
        assert result.is_error and result.payload["cancelled"]
        assert len(calls) == before

    def test_scripted_vlm_can_discover_move_above_and_finish_without_grasping():
        from rebot_trash_sorting_agent.agent.orchestrator import Orchestrator, OrchestratorSettings
        from rebot_trash_sorting_agent.agent.tools import TOOLS
        from rebot_trash_sorting_agent.types import LLMResponse, ToolCall

        skill, calls = runner()
        vocabulary = []
        skill.baseline_classes = ["can"]
        skill.detector = SimpleNamespace(
            set_vocabulary=lambda classes: vocabulary.extend(classes),
            detect=lambda frame: [Detection("can", 0.9, (10, 10, 40, 40))],
        )
        skill.camera = SimpleNamespace(wait_fresh=lambda timeout: np.zeros((120, 120, 3)))
        skill.scene.update = lambda detections, table_map: skill.scene.all()
        skill.scene.as_summaries = lambda: [obj.summary() for obj in skill.scene.all()]
        pending = iter(
            [
                ToolCall("detect_objects", {"classes": ["wrapper", "can"]}),
                ToolCall("move_above_object", {"object": "can"}),
                ToolCall("task_done", {"success": True, "summary": "hovering above can"}),
            ]
        )
        session = SimpleNamespace(
            send=lambda parts: LLMResponse(tool_calls=[next(pending)]),
            submit_tool_results=lambda response, results: None,
        )
        events = SimpleNamespace(bind=lambda **kwargs: None, emit=lambda *args, **kwargs: None)
        agent = Orchestrator(session, TOOLS, skill, events, OrchestratorSettings(), lambda: "table ready")
        result = agent.run("go above the can; do not grasp")
        assert result.success
        assert vocabulary == ["wrapper", "can"]
        assert len(calls) == 1 and calls[0][0] == "move"
