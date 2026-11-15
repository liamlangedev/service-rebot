"""End-to-end Orchestrator + SkillRunner + VLAPolicyClient test (ROS-free)."""

from types import SimpleNamespace

import numpy as np

from web_ui.agent.events import EventLog
from web_ui.agent.orchestrator import Orchestrator, OrchestratorSettings
from web_ui.agent.tools import TOOLS
from web_ui.perception.scene import SceneModel
from web_ui.skills.skills import SkillRunner
from web_ui.skills.vla_policy import VLAPolicyClient
from web_ui.types import Detection, LLMResponse, ToolCall


class _ScriptedSession:
    def __init__(self, calls: list[ToolCall]) -> None:
        self._calls = list(calls)

    def send(self, _parts):
        return LLMResponse(text="", tool_calls=[self._calls.pop(0)], model="scripted")

    def submit_tool_results(self, _response, _results):
        return None


def test_orchestrator_runs_list_then_vla_then_done():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    cam = SimpleNamespace(wait_fresh=lambda timeout_s=2.0: frame, latest=lambda max_age_s=2.0: frame)
    detector = SimpleNamespace(
        classes=["can"],
        set_vocabulary=lambda c: None,
        detect=lambda _f: [Detection("can", 0.9, (10.0, 10.0, 50.0, 50.0))],
    )
    scene = SceneModel()
    events = EventLog()
    runner = SkillRunner(
        places={},
        scene=scene,
        camera=cam,
        detector=detector,
        vla=VLAPolicyClient({"backend": "stub"}),
        events=events,
        cameras={"table": cam, "front": cam, "wrist": cam},
        plan_only=True,
    )
    session = _ScriptedSession([
        ToolCall("list_objects", {}, "c1"),
        ToolCall("run_vla_policy", {"instruction": "put the can in the bin", "object": "can", "destination": "metal"}, "c2"),
        ToolCall("task_done", {"success": True, "summary": "Placed the can in the bin."}, "c3"),
    ])
    orch = Orchestrator(
        session=session,
        tools=TOOLS,
        runner=runner,
        events=events,
        settings=OrchestratorSettings(max_steps=6),
        scene=scene.summary_text,
    )
    res = orch.run("put the can in the bin")
    assert res.success is True
    assert res.steps == 3
    assert "Placed the can" in res.summary
