#!/usr/bin/env python3
"""Prompt the robot: sentence in, task graph out, executed with perception and safety.

  # simulation (no hardware, no API key needed with --planner rules / --detector color)
  uv run python -m autonomy.app "put the red cube in the place zone" --viewer
  uv run python -m autonomy.app "put everything in the place zone"
  uv run python -m autonomy.app                       # interactive: type prompts

  # Claude plans anything the rules don't understand (needs ANTHROPIC_API_KEY)
  uv run python -m autonomy.app "the cube is in the way, move it next to the cylinder"

  # real arm (after calibration; asks before every graph)
  uv run python -m autonomy.app --config autonomy/config/real.json

Ctrl+C = E-stop (stops streaming, the arm holds its pose). Ctrl+C twice = quit.
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
import time
from pathlib import Path

from autonomy.graph import execute, to_text
from autonomy.planner import AutoPlanner, ClaudePlanner, PlannerError, RulePlanner
from autonomy.safety import EStopped, Safety, SafetyConfig
from autonomy.skills import GraspParams, SkillContext
from autonomy.world import WorldConfig, WorldModel, Zone

HERE = Path(__file__).resolve().parent


def build(cfg: dict, args) -> SkillContext:
    from autonomy.perception import make_detector
    wcfg = WorldConfig(**{k: tuple(v) if isinstance(v, list) else v for k, v in cfg.get("world", {}).items()})
    scfg = SafetyConfig.from_dict(cfg.get("safety"))
    safety = Safety(scfg, table_z=wcfg.table_z)
    robot = args.robot or cfg.get("robot", "sim")
    if robot == "sim":
        from autonomy.arm import SimArm
        from autonomy.cameras import SimCameraRig
        arm = SimArm(safety, viewer=args.viewer, max_joint_vel=scfg.max_joint_vel)
        cams = cfg.get("cameras", {})
        rig = SimCameraRig(arm.sim, cams.get("scene", ["overhead_rgb", "front"]), cams.get("wrist", "wrist"))
    else:
        from autonomy.arm import RealArm
        from autonomy.cameras import RealCameraRig
        cal_dir = cfg.get("calibration_dir", "..")
        cal_dir = (HERE.parent / cal_dir).resolve() if not Path(cal_dir).is_absolute() else Path(cal_dir)
        arm = RealArm(safety, cfg.get("port", "/dev/ttyACM0"), cfg.get("robot_id", "follower"),
                      cal_dir, max_joint_vel=scfg.max_joint_vel)
        rig = RealCameraRig(arm.sim, cfg["cameras"], HERE.parent / cfg.get("calibration", "autonomy/config/calibration.json"))
    detector = make_detector(args.detector, sim=arm.sim if robot == "sim" else None, rig=rig)
    zones = [Zone(z["name"], tuple(z["center"]), tuple(z["size"]), z.get("drop_height", 0.02)) for z in cfg.get("zones", [])]
    world = WorldModel(rig, detector, wcfg, zones)
    return SkillContext(arm, world, GraspParams(**cfg.get("grasp", {})))


def make_planner(name: str, effort: str):
    if name == "rules":
        return RulePlanner()
    if name == "claude":
        return ClaudePlanner(effort=effort)
    return AutoPlanner(lambda: ClaudePlanner(effort=effort))


def run_prompt(prompt: str, ctx: SkillContext, planner, args, run_dir: Path) -> str:
    t0 = time.perf_counter()
    ctx._look()
    scene_img = ctx.world.last_images.get(ctx.world.rig.scene[0])
    print(ctx.world.describe())
    try:
        graph = planner.plan(prompt, ctx.world, scene_img)
    except PlannerError as e:
        print(f"[plan] {e}")
        return "fail"
    t_plan = time.perf_counter() - t0
    who = getattr(getattr(planner, "last", planner), "name", "?")
    print(f"[plan] {who} planner, {t_plan:.1f} s\n{to_text(graph)}")
    record = {"prompt": prompt, "planner": who, "plan_seconds": round(t_plan, 2), "graphs": [graph], "runs": []}
    if args.plan_only:
        return "planned"
    if args.robot_kind == "real" and not args.yes:
        if input("Execute this graph on the REAL arm? [y/N] ").strip().lower() != "y":
            return "skipped"
    status = "fail"
    for attempt in range(args.max_replans + 1):
        res = execute(graph, ctx)
        record["runs"].append({"status": res.status, "reason": res.reason, "steps": res.steps})
        status = res.status
        if res.status != "replan" or attempt == args.max_replans:
            break
        print(f"[plan] re-planning: {res.reason}")
        ctx._look()
        try:
            graph = planner.replan(prompt, graph, res, ctx.world, ctx.world.last_images.get(ctx.world.rig.scene[0]))
        except PlannerError as e:
            print(f"[plan] cannot re-plan: {e}")
            break
        print(to_text(graph))
        record["graphs"].append(graph)
    total = time.perf_counter() - t0
    record.update(status=status, total_seconds=round(total, 1))
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "run.json").write_text(json.dumps(record, indent=2, default=str))
    try:
        import cv2
        ctx._look()
        for n, im in ctx.world.last_images.items():
            cv2.imwrite(str(run_dir / f"{n}.jpg"), cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    except Exception as e:  # images are a nice-to-have
        print(f"[run] could not save images: {e}")
    n_ok = sum(s["ok"] for r in record["runs"] for s in r["steps"])
    print(f"[run] {status.upper()} in {total:.1f} s ({n_ok} skills ok) -> {run_dir}")
    return status


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("prompt", nargs="?", help="what the robot should do (omit for interactive mode)")
    p.add_argument("--config", default=str(HERE / "config" / "sim.json"))
    p.add_argument("--robot", choices=["sim", "real"], default=None, help="override the config")
    p.add_argument("--planner", choices=["auto", "rules", "claude"], default="auto")
    p.add_argument("--detector", choices=["color", "oracle", "claude", "gemini"], default="color")
    p.add_argument("--effort", choices=["low", "medium", "high"], default="medium", help="Claude planner effort")
    p.add_argument("--max-replans", type=int, default=2)
    p.add_argument("--plan-only", action="store_true", help="print the graph, do not move")
    p.add_argument("--yes", action="store_true", help="real arm: do not ask before executing")
    p.add_argument("--viewer", action="store_true", help="sim: open the MuJoCo viewer")
    p.add_argument("--runs", default=str(HERE.parent / "runs"), help="where traces are saved")
    args = p.parse_args(argv)
    cfg = json.loads(Path(args.config).read_text())
    args.robot_kind = args.robot or cfg.get("robot", "sim")

    ctx = build(cfg, args)
    planner = make_planner(args.planner, args.effort)
    safety = ctx.arm.safety

    def on_sigint(signum, frame):
        if safety.stopped:
            print("\n[app] quitting")
            ctx.arm.close()
            sys.exit(130)
        safety.estop("Ctrl+C")
    signal.signal(signal.SIGINT, on_sigint)

    def one(prompt):
        safety.reset_estop()
        stamp = time.strftime("%Y%m%d_%H%M%S")
        try:
            return run_prompt(prompt, ctx, planner, args, Path(args.runs) / stamp)
        except EStopped as e:
            print(f"[app] stopped: {e}. Arm is holding. Next prompt resets the E-stop.")
            return "estop"

    try:
        if args.prompt:
            status = one(args.prompt)
            return 0 if status in ("done", "planned") else 1
        print("Type a prompt (empty line or 'quit' to exit). Ctrl+C = E-stop.")
        while True:
            try:
                line = input("\nprompt> ").strip()
            except EOFError:
                break
            if line.lower() in ("", "quit", "exit"):
                break
            one(line)
        return 0
    finally:
        ctx.arm.close()


if __name__ == "__main__":
    sys.exit(main())
