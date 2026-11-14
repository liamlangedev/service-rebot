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


def build_cfg(args, run_dir: Path):
    from wrc_demo.config import load_demo_config

    cfg = load_demo_config(cameras=[args.camera], arm=args.arm, llm="mock")
    d = cfg._data
    d["safety"]["table_z"] = args.table_z            # sim table top is 3 cm above the arm base plane
    d["detect_classes"] = [c.strip() for c in args.classes.split(",") if c.strip()]
    d["grasp"]["memory_path"] = str(run_dir / "grasp_memory.json")
    d["grasp"]["drop_zone"] = [0.25, 0.14]           # free spot on the table, inside the workspace
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
    p.add_argument("--port", type=int, default=8090)
    p.add_argument("--reflex", action="store_true",
                   help="with Claude: try WRC's keyword shortcuts first (faster, no API call, but a "
                        "free-form sentence can be misread). Without Claude they are always on.")
    p.add_argument("--max-steps", type=int, default=12)
    p.add_argument("--run-dir", default=None)
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
        llm = ClaudeLLM()
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
    agent = AgentOrchestrator(
        llm, runtime, advisor=None, max_steps=args.max_steps, decompose=False,
        fast_planner=fast, cfg=cfg,
    )

    def run_task(task: str):
        runtime.current_task = task
        try:
            if runtime.arm.harness.estopped:
                runtime.arm.resume()
            report = agent.run_task(task)
            if report.path == "llm" and not use_claude:
                runtime.memory.add("note", f"{task!r} is not a built-in reflex command and no LLM is "
                                           "connected (set ANTHROPIC_API_KEY).")
            print(f"TASK {task!r}: success={report.success} path={report.path} {report.duration_s}s | "
                  f"{report.summary[:300]}", flush=True)
            return report
        finally:
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
        report = run_task(args.task)
        _print_report(report)
        print("\n=== tool log ===")
        for e in report.tool_log:
            r = e.get("result", {})
            print(f"- {e.get('tool')}({json.dumps(e.get('args', {}))}) -> ok={r.get('ok')} {str(r.get('error') or '')[:300]}")
        after = arm.sim_objects() if hasattr(arm, "sim_objects") else {}
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
