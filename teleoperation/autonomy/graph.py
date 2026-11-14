"""Task graphs: the plan is a small, typed, validated graph of skill calls.

This is the "graph as policy" idea (GaP, CoRL 2026) at hackathon scale: the language model
compiles the prompt into a graph ONCE; deterministic code then executes it, branching on
each skill's success/failure code, with loops for "do this for every object". The model is
called again only to re-plan after an unexpected failure, never per control step.

Graph JSON:
{
  "goal": "put every can in the yellow bin",
  "start": "next",
  "nodes": [
    {"id": "next",  "skill": "select_next", "args": {"object": "can", "target": "yellow bin", "text": ""},
     "on_success": "pick", "on_failure": "done"},
    {"id": "pick",  "skill": "pick",  "args": {"object": "$current", ...}, "on_success": "place", "on_failure": "next"},
    {"id": "place", "skill": "place", "args": {"target": "yellow bin", ...}, "on_success": "next", "on_failure": "replan"}
  ]
}
Edges point to a node id or to one of: done, fail, replan.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

from autonomy.skills import SKILLS, SkillContext

TERMINALS = ("done", "fail", "replan")
ARG_KEYS = ("object", "target", "text")
MAX_VISITS = 12          # per node: bounds every loop
MAX_STEPS = 80

GRAPH_SCHEMA = {
    "type": "object",
    "properties": {
        "goal": {"type": "string"},
        "start": {"type": "string"},
        "nodes": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "skill": {"type": "string", "enum": sorted(SKILLS)},
                "args": {"type": "object",
                         "properties": {k: {"type": "string"} for k in ARG_KEYS},
                         "required": list(ARG_KEYS), "additionalProperties": False},
                "on_success": {"type": "string"},
                "on_failure": {"type": "string"},
            },
            "required": ["id", "skill", "args", "on_success", "on_failure"],
            "additionalProperties": False}},
    },
    "required": ["goal", "start", "nodes"],
    "additionalProperties": False,
}


def validate(graph: dict) -> list[str]:
    """Returns a list of problems (empty = valid)."""
    errs = []
    nodes = graph.get("nodes") or []
    ids = [n.get("id") for n in nodes]
    if not nodes:
        return ["graph has no nodes"]
    if len(set(ids)) != len(ids):
        errs.append("duplicate node ids")
    if any(i in TERMINALS for i in ids):
        errs.append(f"node ids may not be {TERMINALS}")
    if graph.get("start") not in ids:
        errs.append(f"start {graph.get('start')!r} is not a node")
    for n in nodes:
        spec = SKILLS.get(n.get("skill"))
        if spec is None:
            errs.append(f"{n.get('id')}: unknown skill {n.get('skill')!r}")
            continue
        args = n.get("args") or {}
        for k in spec.required:
            if not str(args.get(k, "")).strip():
                errs.append(f"{n['id']}: skill {spec.name} needs '{k}'")
        for k, v in args.items():
            if k not in ARG_KEYS:
                errs.append(f"{n['id']}: unknown arg {k!r}")
            elif v and k not in spec.args:
                errs.append(f"{n['id']}: skill {spec.name} takes no '{k}'")
        for edge in ("on_success", "on_failure"):
            t = n.get(edge)
            if t not in ids and t not in TERMINALS:
                errs.append(f"{n['id']}.{edge} -> {t!r} is neither a node nor {TERMINALS}")
        if "$current" in json.dumps(args) and not any(m.get("skill") == "select_next" for m in nodes):
            errs.append(f"{n['id']}: uses $current but no select_next node binds it")
    if errs:
        return errs
    # every node reachable from start, and "done" reachable
    by_id = {n["id"]: n for n in nodes}
    seen, stack, done_reachable = set(), [graph["start"]], False
    while stack:
        i = stack.pop()
        if i == "done":
            done_reachable = True
        if i in seen or i in TERMINALS:
            continue
        seen.add(i)
        stack += [by_id[i]["on_success"], by_id[i]["on_failure"]]
    unreachable = set(ids) - seen
    if unreachable:
        errs.append(f"unreachable nodes: {sorted(unreachable)}")
    if not done_reachable:
        errs.append("no path reaches 'done'")
    return errs


def to_text(graph: dict) -> str:
    lines = [f"goal: {graph.get('goal', '')}  (start: {graph.get('start')})"]
    for n in graph["nodes"]:
        a = ", ".join(f"{k}={v!r}" for k, v in n["args"].items() if v)
        lines.append(f"  [{n['id']}] {n['skill']}({a})  ok -> {n['on_success']}  fail -> {n['on_failure']}")
    return "\n".join(lines)


@dataclass
class RunResult:
    status: str                       # done | fail | replan | estop
    steps: list[dict] = field(default_factory=list)
    reason: str = ""


def execute(graph: dict, ctx: SkillContext, on_step=None) -> RunResult:
    """Runs a validated graph. on_step(record) is called after every skill."""
    by_id = {n["id"]: n for n in graph["nodes"]}
    visits: dict[str, int] = {}
    cur, steps = graph["start"], []
    for _ in range(MAX_STEPS):
        if cur in TERMINALS:
            return RunResult(cur, steps, steps[-1]["info"] if steps and cur != "done" else "")
        node = by_id[cur]
        visits[cur] = visits.get(cur, 0) + 1
        if visits[cur] > MAX_VISITS:
            return RunResult("replan", steps, f"node {cur} looped {MAX_VISITS} times")
        args = {k: node["args"].get(k, "") for k in ARG_KEYS}
        ctx.log(f"  -> [{cur}] {node['skill']}({', '.join(f'{k}={v!r}' for k, v in args.items() if v)})")
        res = ctx.run(node["skill"], args)
        rec = {"t": time.time(), "node": cur, "skill": node["skill"], "args": args, "ok": res.ok,
               "code": res.code, "info": res.info, "seconds": res.data.get("seconds")}
        steps.append(rec)
        ctx.log(f"     {'OK ' if res.ok else 'FAIL'} {res.code if not res.ok else ''} {res.info}".rstrip())
        if on_step:
            on_step(rec)
        cur = node["on_success"] if res.ok else node["on_failure"]
    return RunResult("replan", steps, f"more than {MAX_STEPS} steps")
