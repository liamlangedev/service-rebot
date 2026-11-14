"""Tests for the prompt -> task graph -> robot pipeline (simulation only, no API keys).

  uv run --extra autonomy pytest tests -q
"""
import json
import types

import numpy as np
import pytest

from autonomy.app import build
from autonomy.calibrate import average_transforms, solve_extrinsics
from autonomy.geometry import CameraModel, intrinsics_from_fovy, make_T, triangulate_rays
from autonomy.graph import execute, validate
from autonomy.planner import AutoPlanner, ClaudePlanner, RulePlanner
from autonomy.safety import SafetyError

CFG = json.load(open("autonomy/config/sim.json"))


def make_ctx():
    return build(CFG, types.SimpleNamespace(robot="sim", viewer=False, detector="color"))


def body_pos(ctx, name):
    m, d = ctx.arm.sim.model, ctx.arm.sim.data
    return d.xpos[m.body(name).id].copy()


def test_camera_roundtrip_and_triangulation():
    K = intrinsics_from_fovy(60, 640, 480)
    R = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1.0]])        # looking straight down
    cams = [CameraModel("a", K, make_T(R, [0.3, 0, 1.0]), 640, 480),
            CameraModel("b", K, make_T(R, [0.6, 0.2, 0.9]), 640, 480)]
    p = np.array([0.42, 0.05, 0.07])
    rays = [c.ray(c.project(p)[0]) for c in cams]
    q, res = triangulate_rays([r[0] for r in rays], [r[1] for r in rays])
    assert np.allclose(q, p, atol=1e-6) and res < 1e-6


def test_world_model_finds_objects():
    ctx = make_ctx()
    objs = ctx.world.look()
    for name, color in [("red_cube", "red"), ("yellow_cylinder", "yellow"), ("blue_block", "blue")]:
        o = ctx.world.find(color)
        assert o is not None, name
        assert np.linalg.norm(o.pos[:2] - body_pos(ctx, name)[:2]) < 0.01, (name, o.pos)
    assert len(objs) == 3


def test_graph_validation_catches_mistakes():
    bad = {"goal": "x", "start": "a", "nodes": [
        {"id": "a", "skill": "pick", "args": {"object": "", "target": "", "text": ""},
         "on_success": "b", "on_failure": "fail"},
        {"id": "c", "skill": "fly", "args": {"object": "", "target": "", "text": ""},
         "on_success": "done", "on_failure": "done"}]}
    errs = validate(bad)
    assert any("needs 'object'" in e for e in errs)
    assert any("unknown skill" in e for e in errs)
    assert any("'b'" in e for e in errs)


@pytest.mark.parametrize("prompt, clauses", [
    ("put the red cube in the place zone", [("red cube", "place zone", False)]),
    ("sort the cans into the yellow bin and the bottles into the blue bin",
     [("cans", "yellow bin", True), ("bottles", "blue bin", True)]),
    ("put everything in the place zone", [("any", "place zone", True)]),
    ("pick up the yellow cylinder", [("yellow cylinder", None, False)]),
])
def test_rule_planner(prompt, clauses):
    r = RulePlanner()
    assert r.parse(prompt) == clauses
    assert validate(r.plan(prompt)) == []


def test_rule_planner_rejects_open_ended():
    assert RulePlanner().parse("what do you see on the table?") is None


def test_safety_blocks_the_table():
    ctx = make_ctx()
    from autonomy.geometry import top_down_rotation
    with pytest.raises(SafetyError):
        ctx.arm.move_tcp(np.array([0.35, 0.0, 0.05]), top_down_rotation(0.0))


def test_e2e_put_cube_in_zone():
    ctx = make_ctx()
    res = execute(RulePlanner().plan("put the red cube in the place zone"), ctx)
    assert res.status == "done", res.steps
    assert ctx.world.zones["place zone"].contains(body_pos(ctx, "red_cube")[:2])


def test_e2e_put_everything_in_zone():
    ctx = make_ctx()
    res = execute(RulePlanner().plan("put everything in the place zone"), ctx)
    assert res.status == "done", res.steps
    for name in ("red_cube", "yellow_cylinder", "blue_block"):
        assert ctx.world.zones["place zone"].contains(body_pos(ctx, name)[:2]), name


def test_e2e_stack():
    ctx = make_ctx()
    res = execute(RulePlanner().plan("put the red cube on the blue block"), ctx)
    assert res.status == "done", res.steps
    red, blue = body_pos(ctx, "red_cube"), body_pos(ctx, "blue_block")
    assert np.linalg.norm(red[:2] - blue[:2]) < 0.03 and red[2] > blue[2] + 0.02


class FakeClaude:
    """Stands in for anthropic.Anthropic(): returns queued JSON graphs, records requests."""

    def __init__(self, graphs):
        self.graphs, self.requests = list(graphs), []
        self.beta = types.SimpleNamespace(messages=types.SimpleNamespace(create=self._create))

    def _create(self, **kw):
        self.requests.append(json.loads(json.dumps(kw, default=str)))
        text = json.dumps(self.graphs.pop(0))
        return types.SimpleNamespace(stop_reason="end_turn",
                                     content=[types.SimpleNamespace(type="text", text=text)])


def test_claude_planner_fixes_invalid_graph_and_runs():
    bad = {"goal": "g", "start": "p", "nodes": [
        {"id": "p", "skill": "pick", "args": {"object": "red", "target": "", "text": ""},
         "on_success": "q", "on_failure": "fail"}]}
    good = {"goal": "g", "start": "p", "nodes": [
        {"id": "p", "skill": "pick", "args": {"object": "red", "target": "", "text": ""},
         "on_success": "q", "on_failure": "replan"},
        {"id": "q", "skill": "place", "args": {"object": "", "target": "yellow", "text": ""},
         "on_success": "h", "on_failure": "replan"},
        {"id": "h", "skill": "home", "args": {"object": "", "target": "", "text": ""},
         "on_success": "done", "on_failure": "done"}]}
    fake = FakeClaude([bad, good])
    ctx = make_ctx()
    ctx.world.look()
    graph = ClaudePlanner(client=fake).plan("the red one belongs on top of the yellow one", ctx.world)
    assert graph == good and len(fake.requests) == 2
    req = fake.requests[0]
    assert req["model"] == "claude-opus-5-5"
    assert req["output_config"]["format"]["type"] == "json_schema"
    assert "invalid" in json.dumps(fake.requests[1]["messages"][-1]["content"])
    res = execute(graph, ctx)
    assert res.status == "done", res.steps
    red, yellow = body_pos(ctx, "red_cube"), body_pos(ctx, "yellow_cylinder")
    assert np.linalg.norm(red[:2] - yellow[:2]) < 0.03 and red[2] > yellow[2]


def test_auto_planner_skips_llm_for_simple_sentences():
    calls = []
    auto = AutoPlanner(lambda: calls.append(1))
    auto.plan("put the red cube in the place zone")
    assert calls == [] and auto.last is auto.rules


def test_calibration_solvers_recover_sim_cameras():
    ctx = make_ctx()
    rig = ctx.world.rig
    cam = rig.model("overhead_rgb")
    rng = np.random.default_rng(0)
    world = np.column_stack([rng.uniform(0.15, 0.65, 8), rng.uniform(-0.2, 0.2, 8), np.full(8, 0.03)])
    px = cam.project(world) + rng.normal(0, 0.3, (8, 2))
    T, rms = solve_extrinsics(world, px, cam.K, np.zeros(5))
    assert np.linalg.norm(T[:3, 3] - cam.center) < 0.005 and rms < 1.0
    a = rig.wrist_mount()
    ctx.arm.move_joints(np.radians([0, -100, -100, 60, 20, 0]))
    b = rig.wrist_mount()
    assert np.allclose(average_transforms([a, b]), a, atol=1e-6)


class FakeRebot:
    """Stands in for teleop.real_robot.RealRebot: the 'arm' follows commands (or lags)."""

    def __init__(self, *a, lag=False, **k):
        self.q, self.g, self.lag, self.sent = np.radians([0, -100, -100, 60, 0, 0]), 0.02, lag, 0

    def read(self):
        return self.q.copy(), self.g

    def send(self, q, g):
        self.sent += 1
        if not self.lag:
            self.q, self.g = np.asarray(q, float).copy(), g

    def close(self):
        pass


def test_real_arm_streams_and_aborts_when_not_tracking(monkeypatch):
    import teleop.real_robot
    from autonomy.arm import RealArm
    from autonomy.safety import Safety
    monkeypatch.setattr(teleop.real_robot, "RealRebot", FakeRebot)
    arm = RealArm(Safety(), port="fake")
    goal = arm.q + np.radians([5, 0, 0, 0, 0, 0])
    arm.move_joints(goal)
    assert np.allclose(arm.q, goal) and arm.robot.sent > 10
    arm.robot.lag = True                     # the arm stops following: must abort
    with pytest.raises(SafetyError):
        arm.move_joints(goal + np.radians([30, 0, 0, 0, 0, 0]))
