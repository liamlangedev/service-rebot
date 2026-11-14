"""Planners: prompt (+ scene) -> task graph.

RulePlanner    instant, offline; covers the common sentence shapes ("put X in Y",
               "sort all X into Y and all Z into W", "pick up X").
ClaudePlanner  anything else: Claude sees the skill catalogue, the detected objects and the
               overhead image, and returns a graph as structured JSON. The graph is validated;
               errors go back to Claude for a fix. After a failed run it re-plans from the trace.
AutoPlanner    rules first (no latency, no cost), Claude when the rules don't understand.
"""
from __future__ import annotations

import json
import os
import re

from autonomy.graph import GRAPH_SCHEMA, validate
from autonomy.perception import _jpeg_b64
from autonomy.skills import SKILLS

CLAUDE_MODEL = os.environ.get("AUTONOMY_CLAUDE_MODEL", "claude-opus-5-5")


class PlannerError(RuntimeError):
    pass


def _n(id_, skill, on_success, on_failure, object="", target="", text=""):
    return {"id": id_, "skill": skill, "args": {"object": object, "target": target, "text": text},
            "on_success": on_success, "on_failure": on_failure}


# ---------------------------------------------------------------------------------
# Rule-based planner
# ---------------------------------------------------------------------------------
_VERBS = r"(?:put|place|move|bring|drop|throw|sort|stack|transfer|carry|clear|tidy|pick up and put|pick and place)"
_PREP = r"(?:into|in|onto|on top of|on|to|inside)"
_CLEAN = re.compile(r"\b(the|all|every|each|of|please|remaining|objects?|items?|things?)\b")


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", _CLEAN.sub(" ", s)).strip(" ,.")


class RulePlanner:
    name = "rules"

    def parse(self, prompt: str):
        """-> list of (object_phrase, target_phrase or None, loop?) or None."""
        p = prompt.lower().strip().rstrip(".!")
        p = re.sub(r"^(please |can you |could you |robot,? )+", "", p)
        if re.fullmatch(r"(pick up|grab|take|lift) (?P<o>.+)", p):
            o = re.fullmatch(r"(pick up|grab|take|lift) (?P<o>.+)", p).group("o")
            return [(_clean(o), None, False)]
        if not re.match(_VERBS + r"\b", p):
            return None
        body = re.sub("^" + _VERBS + r"\s*", "", p)
        clauses = re.split(r"\s*(?:,|;| and then | then | and (?=(?:the |all |every |each )?\w+(?: \w+){0,3} " + _PREP + r"\b))\s*", body)
        out = []
        loop_all = bool(re.match(r"(sort|clear|tidy)\b", p))
        for c in clauses:
            c = re.sub(r"^(?:(?:then|and|also)\s+)*(?:" + _VERBS + r"\s+)?", "", c.strip())
            m = re.fullmatch(r"(?P<o>.+?)\s+" + _PREP + r"\s+(?P<t>.+)", c.strip())
            if not m:
                if c.strip() in ("everything", "") and out:
                    continue
                return None
            obj, tgt = m.group("o"), m.group("t")
            loop = loop_all or bool(re.search(r"\b(all|every|each|everything)\b|s$", obj.strip()))
            o = _clean(obj) or "any"
            out.append((o if o not in ("everything", "anything", "table", "stuff") else "any", _clean(tgt), loop))
        return out or None

    def plan(self, prompt: str, world=None, image=None) -> dict:
        clauses = self.parse(prompt)
        if not clauses:
            raise PlannerError("the rule planner does not understand this sentence")
        nodes = []
        for i, (obj, tgt, loop) in enumerate(clauses):
            nxt = f"s{i + 1}_start" if i + 1 < len(clauses) else "done"
            start = f"s{i}_start"
            if tgt is None:
                nodes += [_n(start, "pick", "done", f"s{i}_relook", object=obj),
                          _n(f"s{i}_relook", "look", f"s{i}_retry", f"s{i}_say", object=obj),
                          _n(f"s{i}_retry", "pick", "done", f"s{i}_say", object=obj),
                          _n(f"s{i}_say", "say", "fail", "fail", text=f"I could not pick up the {obj}.")]
            elif loop:
                nodes += [_n(start, "select_next", f"s{i}_pick", nxt, object=obj, target=tgt),
                          _n(f"s{i}_pick", "pick", f"s{i}_place", start, object="$current"),
                          _n(f"s{i}_place", "place", start, f"s{i}_say", target=tgt),
                          _n(f"s{i}_say", "say", "fail", "fail", text=f"I could not place it in the {tgt}.")]
            else:
                nodes += [_n(start, "pick", f"s{i}_place", f"s{i}_relook", object=obj),
                          _n(f"s{i}_relook", "look", f"s{i}_retry", f"s{i}_say", object=obj),
                          _n(f"s{i}_retry", "pick", f"s{i}_place", f"s{i}_say", object=obj),
                          _n(f"s{i}_place", "place", f"s{i}_check", f"s{i}_say", target=tgt),
                          _n(f"s{i}_check", "check", nxt, f"s{i}_say", object=obj, target=tgt),
                          _n(f"s{i}_say", "say", "fail", "fail", text=f"I could not move the {obj} to the {tgt}.")]
            if i + 1 == len(clauses):
                break
        # the last segment ends at "home" so the cameras see the result
        nodes.append(_n("finish", "home", "done", "done"))
        for n in nodes:
            for e in ("on_success", "on_failure"):
                if n[e] == "done" and n["id"] != "finish":
                    n[e] = "finish"
        graph = {"goal": prompt, "start": "s0_start", "nodes": nodes}
        errs = validate(graph)
        if errs:
            raise PlannerError(f"rule planner built an invalid graph: {errs}")
        return graph

    def replan(self, *a, **k):
        raise PlannerError("the rule planner cannot re-plan")


# ---------------------------------------------------------------------------------
# Claude planner
# ---------------------------------------------------------------------------------
def _catalogue() -> str:
    lines = []
    for s in SKILLS.values():
        args = ", ".join(f"{k}: {v}" + (" (required)" if k in s.required else "") for k, v in s.args.items()) or "no args"
        fails = ", ".join(s.failures) or "-"
        lines.append(f"- {s.name}({args})\n    {s.description}\n    failure codes: {fails}")
    return "\n".join(lines)


SYSTEM_PROMPT = f"""You are the task planner of a 6-DoF robot arm (Seeed reBot B601-DM with a parallel \
gripper) that works on a table. Fixed cameras and a wrist camera feed a perception system; you never \
see joint angles and never move the arm directly. You compile the operator's request into a TASK GRAPH \
of skill calls. Deterministic code executes the graph and follows on_success / on_failure edges.

Skills (args are always the three strings object, target, text; use "" for unused ones):
{_catalogue()}

Graph rules
- Every node: id, skill, args, on_success, on_failure. Edges point to a node id or to "done", \
"fail" or "replan".
- For "all/every/sort/clear" requests, loop: select_next(object=<category>, target=<destination>) -> \
pick($current) -> place(<destination>) -> back to select_next. select_next fails with none_left when \
the loop is finished: route that failure onward (next category or done).
- In a loop, a failed pick should go back to select_next (the object is skipped after two failures).
- For a single move use pick -> place -> check. After an unexpected failure route to "replan", or add \
one retry (look then pick again) first.
- End with a "home" node so the cameras can see the result.
- Refer to objects by the ids or labels in the scene list, or by a category word for select_next. Only \
use zone names that exist in the scene list, or object ids/labels as place targets.
- If the request is impossible, unsafe, or unclear (e.g. the object is not on the table), return a \
graph with a single say node that explains why, with both edges -> "done".
- Keep graphs small: no node the request does not need.
"""


class ClaudePlanner:
    name = "claude"

    def __init__(self, model: str = CLAUDE_MODEL, effort: str = "medium", client=None, max_fixes: int = 2):
        if client is None:
            import anthropic
            client = anthropic.Anthropic()
        self.client, self.model, self.effort, self.max_fixes = client, model, effort, max_fixes
        self.messages: list = []

    def _call(self):
        resp = self.client.beta.messages.create(
            model=self.model, max_tokens=8000,
            betas=["server-side-fallback-2026-07-01"], fallbacks="default",
            system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
            output_config={"effort": self.effort,
                           "format": {"type": "json_schema", "schema": GRAPH_SCHEMA}},
            messages=self.messages)
        if resp.stop_reason == "refusal":
            raise PlannerError("the model declined this request")
        if resp.stop_reason == "max_tokens":
            raise PlannerError("the plan was cut off (max_tokens)")
        self.messages.append({"role": "assistant", "content": resp.content})
        text = next((b.text for b in resp.content if b.type == "text"), "")
        return json.loads(text)

    def _solve(self):
        for attempt in range(self.max_fixes + 1):
            graph = self._call()
            errs = validate(graph)
            if not errs:
                return graph
            self.messages.append({"role": "user", "content":
                                  "The graph is invalid:\n- " + "\n- ".join(errs) + "\nReturn a corrected graph."})
        raise PlannerError(f"no valid graph after {self.max_fixes + 1} attempts: {errs}")

    def _scene_content(self, world, image):
        content = []
        if image is not None:
            data, _ = _jpeg_b64(image)
            content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}})
        content.append({"type": "text", "text": world.describe() if world else "(no scene information)"})
        return content

    def plan(self, prompt: str, world=None, image=None) -> dict:
        self.messages = [{"role": "user", "content": self._scene_content(world, image) +
                          [{"type": "text", "text": f"Operator request: {prompt}"}]}]
        return self._solve()

    def replan(self, prompt: str, graph: dict, run, world=None, image=None) -> dict:
        trace = "\n".join(f"- [{s['node']}] {s['skill']}({', '.join(f'{k}={v!r}' for k, v in s['args'].items() if v)}) "
                          f"-> {'ok' if s['ok'] else 'FAILED ' + s['code']}: {s['info']}" for s in run.steps[-15:])
        self.messages.append({"role": "user", "content": self._scene_content(world, image) + [{"type": "text", "text":
                              f"The graph stopped with status '{run.status}' ({run.reason}). Trace:\n{trace}\n"
                              f"The scene above is the CURRENT state. Return a new graph that finishes the "
                              f"original request '{prompt}' from here, avoiding what failed."}]})
        return self._solve()


class AutoPlanner:
    name = "auto"

    def __init__(self, claude_factory):
        self.rules = RulePlanner()
        self._claude_factory = claude_factory
        self._claude = None
        self.last = None

    @property
    def claude(self):
        if self._claude is None:
            self._claude = self._claude_factory()
        return self._claude

    def plan(self, prompt, world=None, image=None):
        if self.rules.parse(prompt):
            self.last = self.rules
            return self.rules.plan(prompt, world, image)
        self.last = self.claude
        return self.claude.plan(prompt, world, image)

    def replan(self, prompt, graph, run, world=None, image=None):
        # Rules don't re-plan; hand the situation to Claude with a fresh conversation.
        if self.last is self.rules:
            self.last = self.claude
            return self.claude.plan(f"{prompt}\n(An earlier attempt stopped: {run.reason}. "
                                    f"Continue from the current scene.)", world, image)
        return self.claude.replan(prompt, graph, run, world, image)
