#!/usr/bin/env python
"""Run the WRC pipeline on the reBot B601-DM through the DM bridge (hackathon DM port).

Start local_dm/dm_bridge_server.py first (./START_WRC.sh dm does both). Then:

  python local_dm/run_dm.py --dashboard                 # web UI at http://127.0.0.1:8090/
  python local_dm/run_dm.py --task "pick and place the red cube"
  python local_dm/run_dm.py --task "put the red cube on the blue block" --llm claude

  --llm claude   Claude plans from the camera image + tool results (needs ANTHROPIC_API_KEY,
                 read from the environment or from wrc/.env). Default when a key is present.
  --llm mock     no LLM: only WRC's built-in reflex commands work (look around / go home /
                 open the gripper / pick and place X / put X on Y).

Same wiring as wrc_demo.apps.demo (build_runtime + AgentOrchestrator); the only
additions are the DM arm + sim camera backends (wrc_dm_plugin) and the Claude client.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
os.environ.setdefault("YOLO_OFFLINE", "True")
os.chdir(REPO)   # YOLOE resolves its text encoder (mobileclip2_b.ts) relative to the CWD


# The detector names objects from a top-down camera image, so its labels do not always match the
# user's words (a cylinder seen from above is a disc and gets labelled "ball"). Without this note
# Claude sometimes refuses to act because "no yellow cylinder was detected".
LABEL_HINT = """Notes for this robot:
- Object names in tool results come from a camera detector looking straight down, and may differ from \
the user's words. A cylinder or can seen from above is often labelled "ball"; "cube", "block" and "box" \
are used interchangeably.
- If exactly one detected object fits the user's description by colour and rough shape, act on it and \
pass the detector's label to the tool. Say in your summary which label you used.
- pick_and_place without a destination moves the object to a free spot on the table that the robot \
chooses; other objects are not disturbed.
- An entry with state "remembered" is only where an object was seen EARLIER; it is not a second object. \
When a "visible" entry with the same label exists, the visible one is the object: use it and ignore the \
remembered one. Never call a request ambiguous because of a remembered entry.
- Only if several VISIBLE objects could fit, or none does, do not guess: call task_done(success=false) \
and say what you see."""


def load_dotenv(path: Path) -> None:
    """Minimal .env loader: KEY=VALUE lines; existing environment variables win."""
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if v.strip():
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


# Spots where an object may be put down when the task names no destination. Candidates are
# visible to an overhead camera with the arm at home; each one is checked with WRC's own IK
# before it is used, because a straight-down put-down reaches less far than a grasp.
FREE_SPOTS = [(x / 100, y / 100) for x in (24, 28, 32, 36, 40) for y in range(-20, 21, 4)]


def _can_put_down(runtime, cfg, x: float, y: float) -> bool:
    """Would WRC's place_at find a pose here? Same poses and yaw candidates as skill_place_at."""
    import math

    import numpy as np
    import pinocchio as pin

    g, table_z = cfg.grasp, float(cfg.safety.get("table_z", 0.0))
    release_z = table_z + float(g.get("release_height_m", 0.05))
    z_cap = float(g.get("topdown_z_max", 0.15)) - 0.005
    release_z = min(release_z, z_cap)
    hover_z = min(release_z + float(g.get("pregrasp_offset_m", 0.12)), z_cap)
    pitch = float(g.get("approach_pitch_rad", 1.2))
    home = np.asarray(cfg.arm.home_q, dtype=float)
    for yaw in (0.0, math.atan2(y, x), math.pi / 4, -math.pi / 4, math.pi / 2, -math.pi / 2):
        T = np.eye(4)
        T[:3, :3] = pin.rpy.rpyToMatrix(0.0, pitch, float(yaw))
        T[:3, 3] = [x, y, hover_z]
        pre = runtime.kin.ik(T, home)
        if not pre.success:
            continue
        T[2, 3] = release_z
        if runtime.kin.ik(T, pre.q).success:
            return True
    return False


def free_spot(runtime, cfg, default):
    """The reachable candidate spot furthest from every object the camera currently sees."""
    def recent():   # seen in the last few seconds (ignores old "remembered" ghosts)
        return [o["position"][:2] for o in runtime.beliefs.summary() if float(o.get("age_s", 99)) <= 5.0]
    seen = recent()
    deadline = time.monotonic() + 4.0
    while not seen and time.monotonic() < deadline:      # right after start-up the first detection may be pending
        time.sleep(0.2)
        seen = recent()

    def clearance(s):
        return min((((s[0] - p[0]) ** 2 + (s[1] - p[1]) ** 2) ** 0.5 for p in seen), default=1.0)

    for spot in sorted(FREE_SPOTS, key=clearance, reverse=True):
        if clearance(spot) < 0.09:
            break
        if _can_put_down(runtime, cfg, *spot):
            return list(spot)
    return list(default)


def build_cfg(args, run_dir: Path):
    from wrc_demo.config import load_demo_config

    cfg = load_demo_config(cameras=[args.camera], arm=args.arm, llm="mock")
    d = cfg._data
    d["safety"]["table_z"] = args.table_z            # sim table top is 3 cm above the arm base plane
    d["detect_classes"] = [c.strip() for c in args.classes.split(",") if c.strip()]
    d["grasp"]["memory_path"] = str(run_dir / "grasp_memory.json")
    d["grasp"]["drop_zone"] = [0.25, 0.14]           # free spot on the table, inside the workspace
    # Put objects down with the gripper pointing straight down. WRC's default tilts the tool 21 deg
    # (tuned for the RS arm); objects are grasped vertically here, so a tilted release sets tall
    # objects down at an angle and they end up leaning or fall over (measured: 30 deg lean).
    d["grasp"]["approach_pitch_rad"] = 1.5707963267948966
    d["stream"]["host"] = "127.0.0.1"                # dashboard on localhost only
    d["stream"]["port"] = args.port
    for kv in args.set or []:                        # e.g. --set grasp.approach_pitch_rad=1.5708
        key, val = kv.split("=", 1)
        node = d
        parts = key.split(".")
        for p in parts[:-1]:
            node = node[p]
        node[parts[-1]] = json.loads(val)
    return cfg


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--task", default=None, help="run one task and exit")
    p.add_argument("--dashboard", action="store_true", help="serve the web dashboard and wait for tasks")
    p.add_argument("--llm", choices=["auto", "claude", "mock"], default="auto")
    p.add_argument("--arm", default="rebot_dm", help="arm profile in configs/arms/")
    p.add_argument("--camera", default="dm_sim_overhead", help="camera profile in configs/cameras/")
    p.add_argument("--classes", default="red block,blue block,yellow ball",
                   help="detector vocabulary (object names the camera should look for)")
    p.add_argument("--table-z", type=float, default=0.03)
    p.add_argument("--drop-zone", default="auto",
                   help="where 'pick X' with no destination puts the object: 'auto' = a free spot on the table "
                        "chosen before every task (so objects do not pile up), or fixed 'x,y' in metres")
    p.add_argument("--port", type=int, default=8090)
    p.add_argument("--reflex", action="store_true",
                   help="with Claude: try WRC's keyword shortcuts first (faster, no API call, but a "
                        "free-form sentence can be misread). Without Claude they are always on.")
    p.add_argument("--max-steps", type=int, default=12)
    p.add_argument("--run-dir", default=None)
    p.add_argument("--notes", action="store_true", help="with --task: print the robot's own step-by-step notes")
    p.add_argument("--json-out", default=None, help="with --task: also write the result as JSON (for test scripts)")
    p.add_argument("--set", action="append", metavar="KEY=JSON", help="override a config value")
    args = p.parse_args(argv)
    if not args.task and not args.dashboard:
        p.error("give --task \"...\" or --dashboard")

    load_dotenv(REPO / ".env")
    import wrc_dm_plugin
    wrc_dm_plugin.register()

    from wrc_demo.agent.llm import make_llm
    from wrc_demo.agent.orchestrator import AgentOrchestrator
    from wrc_demo.agent.reflex import ExperienceMemory, FastPlanner
    from wrc_demo.apps.demo import _print_report, build_runtime, shutdown_runtime

    run_dir = Path(args.run_dir) if args.run_dir else REPO / "runs" / ("dm_" + time.strftime("%Y%m%d_%H%M%S"))
    cfg = build_cfg(args, run_dir)

    have_key = bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))
    use_claude = args.llm == "claude" or (args.llm == "auto" and have_key)
    if args.llm == "claude" and not have_key:
        print("ERROR: --llm claude needs ANTHROPIC_API_KEY (environment or wrc/.env)", file=sys.stderr)
        return 2
    if use_claude:
        from claude_llm import ClaudeLLM
        llm = ClaudeLLM(system_suffix=LABEL_HINT)
        llm_name = f"claude ({llm.model}, effort {llm.effort})"
    else:
        llm = make_llm(cfg.llm)
        llm_name = "mock (reflex commands only)"

    print(f"[wrc-dm] arm={args.arm} camera={args.camera} llm={llm_name}", flush=True)
    print(f"[wrc-dm] traces -> {run_dir}", flush=True)
    try:
        runtime, arm = build_runtime(cfg, run_dir, view=False, serve=args.dashboard)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if args.dashboard and runtime.stream_server is None:
        print(f"ERROR: dashboard port {args.port} is already in use (another WRC dashboard running?)",
              file=sys.stderr)
        shutdown_runtime(runtime, arm)
        return 2

    # With Claude connected, Claude reads every instruction (WRC's keyword matcher misreads
    # free-form sentences, e.g. "stack it on top of the blue one" -> destination "top of the
    # blue one"). Without an LLM the keyword shortcuts are the only way to act.
    fast = FastPlanner(ExperienceMemory(run_dir / "experience.json")) if (args.reflex or not use_claude) else None
    if use_claude:                       # every Claude decision shows up in the dashboard narration
        def _show_decision(rec):
            what = f"{rec['tool']}({json.dumps(rec['args'])})" if rec["tool"] else "a text reply"
            runtime.memory.add("note", f"planner Claude ({rec['model']}) chose {what} -- {rec['s']} s, "
                                       f"{rec['in']} input tokens, API request {rec['request_id']}")
        llm.on_call = _show_decision

    if args.notes:                       # print the robot's own notes live (its memory only keeps 15 s)
        _add = runtime.memory.add

        def _add_and_print(kind, text, *a, **k):
            print(f"  note[{kind}] {text}"[:600], flush=True)
            return _add(kind, text, *a, **k)

        runtime.memory.add = _add_and_print

    agent = AgentOrchestrator(
        llm, runtime, advisor=None, max_steps=args.max_steps, decompose=False,
        fast_planner=fast, cfg=cfg,
    )

    default_drop = list(cfg._data["grasp"]["drop_zone"])
    if args.drop_zone != "auto":
        default_drop = [float(v) for v in args.drop_zone.split(",")]
        cfg._data["grasp"]["drop_zone"] = default_drop

    def put_down_if_still_holding():
        """A task that ends with something still in the gripper (its put-down failed) must not leave it
        there: the next task would open the gripper and drop it from wherever the arm is."""
        try:
            if not runtime.held_object or runtime.arm.harness.estopped:
                return
            held = runtime.held_object
            spot = free_spot(runtime, cfg, default_drop)
            res = runtime.execute("place_at", {"x": spot[0], "y": spot[1]})
            if res.get("ok"):
                runtime.memory.add("outcome", f"the task ended with '{held}' still in the gripper, so I put it "
                                              f"down on a free spot at ({spot[0]:.2f}, {spot[1]:.2f})")
            else:
                runtime.memory.add("outcome", f"I am still holding '{held}' and could not put it down: "
                                              f"{str(res.get('error'))[:120]}")
            print(f"[wrc-dm] still holding {held!r} after the task -> put down at {spot}: ok={res.get('ok')}", flush=True)
        except Exception as e:  # noqa: BLE001 -- clean-up must never mask the task's own result
            print(f"[wrc-dm] could not put down the held object: {e}", flush=True)

    def run_task(task: str):
        runtime.current_task = task
        try:
            if runtime.arm.harness.estopped:
                runtime.arm.resume()
            if args.drop_zone == "auto":
                cfg._data["grasp"]["drop_zone"] = free_spot(runtime, cfg, default_drop)
            try:
                report = agent.run_task(task)
            except RuntimeError as e:          # e.g. the Claude API rejected the key or is unreachable
                runtime.memory.add("outcome", f"could not do {task!r}: {e}")
                print(f"TASK {task!r}: FAILED before finishing | {e}", flush=True)
                raise
            if report.path == "llm" and not use_claude:
                runtime.memory.add("note", f"{task!r} is not a built-in reflex command and no LLM is "
                                           "connected (set ANTHROPIC_API_KEY).")
            print(f"TASK {task!r}: success={report.success} path={report.path} {report.duration_s}s | "
                  f"{report.summary[:300]}", flush=True)
            return report
        finally:
            put_down_if_still_holding()
            runtime.current_task = None

    def cancel_task():
        runtime.memory.add("outcome", "USER pressed STOP -- aborting the current action")
        runtime.arm.stop()

    try:
        # wait for the first detector pass so commands resolve against a warm world model
        deadline = time.monotonic() + 60
        while not runtime.beliefs.summary() and time.monotonic() < deadline:
            time.sleep(0.2)
        print("[wrc-dm] camera sees:", [(o["label"], o["position"]) for o in runtime.beliefs.summary()], flush=True)

        if args.dashboard:
            runtime.stream_server.set_task_fn(run_task)
            runtime.stream_server.set_cancel_fn(cancel_task)
            print(f"DASHBOARD: http://127.0.0.1:{args.port}/   (Ctrl+C to stop)", flush=True)
            while True:
                time.sleep(5)
        before = arm.sim_objects() if hasattr(arm, "sim_objects") else {}
        try:
            report = run_task(args.task)
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        _print_report(report)
        print("\n=== tool log ===")
        for e in report.tool_log:
            r = e.get("result", {})
            print(f"- {e.get('tool')}({json.dumps(e.get('args', {}))}) -> ok={r.get('ok')} {str(r.get('error') or '')[:300]}")
        after = arm.sim_objects() if hasattr(arm, "sim_objects") else {}
        if args.json_out:
            Path(args.json_out).write_text(json.dumps({
                "task": args.task, "success": bool(report.success), "path": report.path,
                "duration_s": report.duration_s, "steps": report.steps, "summary": report.summary,
                "tool_log": [{"tool": e.get("tool"), "args": e.get("args", {}),
                              "ok": e.get("result", {}).get("ok"),
                              "error": str(e.get("result", {}).get("error") or "")[:400]} for e in report.tool_log],
                "claude_calls": getattr(llm, "calls", []),
            }, indent=1))
        if after:
            print("\n=== simulator ground truth (verification only; WRC used the camera) ===")
            for name in after:
                b, a = before.get(name, [0, 0, 0]), after[name]
                moved = sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
                print(f"- {name}: {[round(v, 3) for v in b]} -> {[round(v, 3) for v in a]}  (moved {moved * 100:.1f} cm)")
        return 0 if report.success else 1
    except KeyboardInterrupt:
        return 0
    finally:
        shutdown_runtime(runtime, arm)


if __name__ == "__main__":
    sys.exit(main())
