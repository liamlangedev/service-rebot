#!/usr/bin/env python3
"""Gemini orchestrator: turns what you say or type into robot skills, and checks the result with the cameras.

  export GEMINI_API_KEY=...        # from Google AI Studio; never commit it
  python robot_server.py --port <PORT> --policy <checkpoint> ...     # terminal 1 (loads the model once)
  python orchestrator.py                                              # terminal 2, type requests
  ANTHROPIC_API_KEY=... python orchestrator.py --backend claude       # same, with Claude

Gemini only has three tools: fetch(item), look(camera), stop(). fetch maps to a fixed training prompt from
config/skills.json, so Gemini cannot send arbitrary prompts or joint commands to the robot.
Test without a robot: `python robot_server.py --fake` and run this against it.
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import httpx
from google import genai
from google.genai import types

SKILLS_CONFIG = Path(__file__).resolve().parent / "config" / "skills.json"
FALLBACK_MODELS = ["gemini-3.5-flash", "gemini-3-flash", "gemini-flash-latest"]  # tried in order if the main model fails; names unchecked

DEFAULT_CLAUDE_MODEL = "claude-opus-5-5"
_CLAUDE_FALLBACK_MODELS = ("claude-opus-5-5", "claude-sonnet-5-5")  # accept the server-side refusal fallback
_CLAUDE_FALLBACK_BETA = "server-side-fallback-2026-07-01"


def concierge_prompt(skills: dict, skill_cfg: dict, concierge: dict) -> str:
    """System prompt of the concierge: understands what a guest needs and hands out the matching item."""
    venue = concierge.get("venue", "a wellness spa")
    handout = concierge.get("handout", "the hand-out tray (the white box on the right of the counter)")
    lines = []
    for name in skills:
        c = skill_cfg.get(name, {})
        lines.append(f"- {name}: {c.get('offer', name)}. Good for: {c.get('good_for', 'when a guest asks for it')}.")
    items = "\n".join(lines)
    return f"""You are the friendly concierge robot at {venue}. Guests talk to you (by voice or text) and you hand out the
items they need with your robot arm: the arm picks the item up from the counter and places it in {handout}, where the
guest takes it.

Items you can hand out (nothing else):
{items}

How to help:
- Work out what the guest actually needs, also when they do not name the item ("I'm off to the sauna" -> towel,
  "I'm so thirsty" -> water). If a need clearly matches one item, say in a short sentence what you are getting and
  call fetch(item). If it is really unclear, ask one short question first.
- One item at a time. If the guest needs several, hand them out one after another.
- If they want something you do not have (a bathrobe, slippers, food, ...), say kindly that you can only offer the
  items above, suggest one if it helps, and call notify_staff so a staff member can help them.
- Use notify_staff also when a guest has a complaint, feels unwell, needs a human, or anything is wrong with the robot.
  The staff see it on their operator screen. Never mention internal details (skills, cameras, policies, errors) to guests.

Tools:
- fetch(item): hands out one item. It blocks until done and supervises itself (checks the item is there, watches the arm,
  ends as soon as the item is in the tray). The result tells you what happened (status, reason, suggestion).
- look(camera): current camera image (front_wide shows the whole counter), if you need to check something yourself.
- notify_staff(message, urgency): alert the staff on the operator screen.
- stop(): stop the arm immediately.

After fetch:
- status "done": tell the guest it is ready in the tray; offer briefly if they need anything else.
- status "no_item": that item has run out. Apologise, say a staff member will restock it (they are already notified).
- any other status (stuck, failed, ran_out_of_time, error): apologise briefly and say a staff member is on the way (they
  are already notified). Do NOT retry on your own; only if the guest asks.
- status "aborted": the staff pressed STOP. Just say "Stopped." and do nothing else.

Style: warm, calm, short (one or two sentences; it is read aloud). Reply in the guest's language."""


EVENT = None  # optional hook (kind, text): the web UI sets it to receive progress


def log(msg: str, kind: str = "log"):
    print(msg, flush=True)
    if EVENT:
        EVENT(kind, msg.strip())


class Robot:
    CHECK_EVERY = 4.0      # seconds between vision checks while a skill runs
    DONE_CONFIRMS = 2      # consecutive "done" verdicts before ending the skill
    STUCK_CONFIRMS = 2     # consecutive "stuck" verdicts before giving up
    FAILED_CONFIRMS = 3    # consecutive "failed" verdicts (the policy often recovers, e.g. re-grasps)
    NO_MOTION_S = 10.0     # arm essentially still for this long -> stuck, without waiting for the LLM

    def __init__(self, url: str, config_path: Path = SKILLS_CONFIG):
        self.http = httpx.Client(base_url=url, timeout=30.0)
        self.skills = self._wait_for_server(url)
        cfg = json.loads(config_path.read_text()) if config_path.exists() else {}
        self.scene, self.skill_cfg = cfg.get("scene", {}), cfg.get("skills", {})
        self.system_prompt = concierge_prompt(self.skills, self.skill_cfg, cfg.get("concierge", {}))
        self.attempts: dict[str, int] = {}
        self.aborted = False
        self.request = ""      # the guest's current request (for issue reports)
        self.judge = None  # set by Brain: judge(kind, item, images, **info) -> dict
        self.report = None  # set by the web UI: report(issue dict) -> operator dashboard
        if "motion_deg_3s" not in self._status():
            log("  [robot] WARNING: robot_server.py is an old version (no motion data, no stop reasons). Restart it.")

    def _wait_for_server(self, url: str, timeout_s: float = 600.0) -> dict:
        """The robot server may still be connecting to the arm (or waiting for Enter): wait instead of crashing."""
        t0, said = time.time(), False
        while True:
            try:
                return self.http.get("/skills").raise_for_status().json()
            except httpx.HTTPError:
                if time.time() - t0 > timeout_s:
                    raise SystemExit(f"robot server at {url} did not come up within {timeout_s:.0f} s")
                if not said:
                    print(f"waiting for the robot server at {url} (start robot_server.py; it prints 'robot ready.')...",
                          flush=True)
                    said = True
                time.sleep(1.0)

    def issue(self, kind: str, severity: str, message: str, item: str | None = None, reason: str = "",
              suggestion: str = "", snapshot: bool = True) -> None:
        """Send a problem to the operator dashboard (or print it when there is no dashboard)."""
        log(f"  [issue] {severity}: {message}" + (f" ({reason})" if reason else ""), kind="issue_log")
        if self.report is None:
            return
        img = self.look("front_wide") if snapshot else None
        try:
            self.report({"kind": kind, "severity": severity, "message": message, "item": item, "reason": reason,
                         "suggestion": suggestion, "request": self.request, "snapshot": img})
        except Exception as e:  # noqa: BLE001 - reporting must never break the robot flow
            print(f"[issue] could not report: {e!r}")

    def notify_staff(self, message: str, urgency: str = "normal") -> dict:
        sev = {"high": "error", "urgent": "error", "low": "info"}.get(str(urgency).lower(), "warning")
        self.issue("staff_request", sev, message, snapshot=False)
        return {"ok": True, "note": "the staff have been notified on the operator screen"}

    def _status(self) -> dict:
        return self.http.get("/status").json()

    def fetch(self, item: str) -> dict:
        if self.aborted:
            return {"ok": False, "status": "aborted", "message": "the operator stopped everything; do not continue"}
        if item not in self.skills:
            return {"ok": False, "error": f"no skill for {item!r}; available: {list(self.skills)}"}
        self.attempts[item] = self.attempts.get(item, 0) + 1
        if self.attempts[item] > 2:
            return {"ok": False, "error": f"already tried {item!r} twice this request; report failure to the user"}
        hint = self.skill_cfg.get(item, {}).get("pickup", "")
        looks = self.skill_cfg.get(item, {}).get("looks_like", "")
        bin_desc = self.scene.get("bin", "the designated bin")
        before = self.look("front_wide")

        # 1. is there anything to pick up? Do not move the arm if not.
        if self.judge and before:
            pre = self.judge("pre", item, [before], pickup=hint, bin=bin_desc, looks_like=looks)
            log(f"  [judge] before: present={pre.get('present')} sees '{pre.get('what_i_see', '')}' - {pre.get('reason', '')}")
            if pre.get("present") is False:
                self.issue("no_item", "warning", f"Out of {item}: none at the pick-up area", item=item,
                           reason=pre.get("reason", ""), suggestion=f"restock the {item} at the pick-up area")
                return {"ok": False, "status": "no_item", "message": f"There is no {item} left at the pick-up area, so nothing was done.",
                        "reason": pre.get("reason", "")}

        try:
            r = self.http.post("/run", json={"skill": item})
        except httpx.HTTPError as e:
            self.issue("robot_offline", "error", f"Robot server not reachable when starting '{item}'", item=item,
                       reason=repr(e), suggestion="check that robot_server.py is running", snapshot=False)
            return {"ok": False, "status": "error", "reason": "the robot is not reachable"}
        if r.status_code != 200:
            self.issue("robot_error", "error", f"Robot refused to start '{item}'", item=item, reason=r.text[:300])
            return {"ok": False, "status": "error", "reason": r.text[:300]}
        log(f"  [robot] running {item!r}...")

        # 2. supervise: every few seconds compare the scene with the start and decide done / working / stuck
        t_start, next_check, done_n, stuck_n, still_since = time.time(), time.time() + self.CHECK_EVERY, 0, 0, None
        failed_n = 0
        verdict, reason, suggestion, decided = "timeout", "", "", False
        while True:
            time.sleep(0.4)
            st = self._status()
            if st["state"] == "idle":
                last = st["last"]
                if self.aborted:
                    verdict = "aborted"
                elif decided:
                    pass  # we ended it ourselves (done / stuck / failed); keep that verdict
                elif last.get("reason") == "operator_done":
                    verdict = "done"
                elif last.get("finished") is False:  # the skill crashed (e.g. the inference Space failed)
                    verdict, reason = "error", str(last.get("note") or "the skill stopped with an error")
                elif last.get("stopped_early"):
                    verdict = "ended_early"
                else:
                    verdict = "ran_out_of_time"
                break
            if self.aborted:
                continue  # the stop was already sent; wait for the arm to return to ready
            now = time.time()
            # no motion for a while: stuck, no need to ask the LLM
            if st.get("motion_deg_3s", 99) < 1.0 and st["elapsed"] > 6:
                still_since = still_since or now
                if now - still_since > self.NO_MOTION_S:
                    verdict, reason, suggestion, decided = "stuck", "the arm stopped moving", "check the scene and try again", True
                    log("  [judge] arm has not moved for a while -> stuck")
                    self.http.post("/stop", params={"reason": "stuck"})
                    continue
            else:
                still_since = None
            if self.judge and now >= next_check:
                cur = self.look("front_wide")
                if cur and before:
                    j = self.judge("progress", item, [before, cur], pickup=hint, bin=bin_desc, looks_like=looks,
                                   elapsed=st["elapsed"], motion=st.get("motion_deg_3s"))
                    s_ = j.get("status", "working")
                    log(f"  [judge] {st['elapsed']:.0f}s: {s_} - {j.get('reason', '')}")
                    done_n = done_n + 1 if s_ == "done" else 0
                    stuck_n = stuck_n + 1 if s_ == "stuck" else 0
                    failed_n = failed_n + 1 if s_ == "failed" else 0
                    reason, suggestion = j.get("reason", ""), j.get("suggestion", "")
                    if done_n >= self.DONE_CONFIRMS:
                        verdict, decided = "done", True
                        self.http.post("/stop", params={"reason": "done"})
                    elif stuck_n >= self.STUCK_CONFIRMS or failed_n >= self.FAILED_CONFIRMS:
                        verdict, decided = s_, True
                        self.http.post("/stop", params={"reason": "stuck"})
                next_check = time.time() + self.CHECK_EVERY
        log(f"  [robot] finished: {verdict}")
        if verdict == "aborted":
            self.issue("aborted", "info", f"STOP pressed while handing out '{item}'", item=item)
        elif verdict != "done":
            what = {"stuck": "got stuck", "failed": "failed", "ran_out_of_time": "ran out of time",
                    "ended_early": "was ended early", "error": "stopped with an error"}.get(verdict, verdict)
            self.issue(f"skill_{verdict}", "error" if verdict in ("failed", "error") else "warning",
                       f"Handing out '{item}' {what}", item=item, reason=reason, suggestion=suggestion)
        res = {"ok": verdict == "done", "status": verdict, "reason": reason, "suggestion": suggestion,
               "message": "the arm is back at its ready pose"}
        if verdict == "ran_out_of_time":
            res["message"] += "; the time limit passed without the item being confirmed in the bin"
        if verdict == "ended_early":
            res["message"] += "; it was ended early by the operator"
        return res

    def look(self, camera: str) -> bytes | None:
        try:
            r = self.http.get("/frame", params={"camera": camera})
            return r.content if r.status_code == 200 else None
        except httpx.HTTPError:
            return None

    def stop(self) -> dict:
        """Operator/LLM stop: ends the skill AND blocks any further robot actions for this request."""
        self.aborted = True
        self.http.post("/stop", params={"reason": "abort"})
        return {"ok": True}

    def finish(self) -> dict:
        """Operator says the task is done: end the skill now and let the LLM wrap up."""
        self.http.post("/stop", params={"reason": "operator_done"})
        return {"ok": True}


def tool_declarations(skills: dict) -> list[types.Tool]:
    S = types.Schema
    return [types.Tool(function_declarations=[
        types.FunctionDeclaration(
            name="fetch", description="Run the robot skill that picks this item and puts it in the bin. Blocks until done.",
            parameters=S(type="OBJECT", properties={"item": S(type="STRING", enum=list(skills))}, required=["item"])),
        types.FunctionDeclaration(
            name="look", description="Get a current image from a camera.",
            parameters=S(type="OBJECT", properties={"camera": S(type="STRING", enum=["front_wide", "high_oblique", "gripper"])},
                         required=["camera"])),
        types.FunctionDeclaration(name="stop", description="Stop the arm immediately.", parameters=S(type="OBJECT", properties={})),
        types.FunctionDeclaration(
            name="notify_staff", description=NOTIFY_DESC,
            parameters=S(type="OBJECT", properties={"message": S(type="STRING"),
                                                    "urgency": S(type="STRING", enum=["low", "normal", "high"])},
                         required=["message"])),
    ])]


NOTIFY_DESC = ("Alert the human staff on the operator screen: a guest needs something we do not have, a complaint, "
               "a guest feels unwell or asks for a person, or something is wrong with the robot. One short sentence.")


def generate(client, models: list[str], contents, cfg):
    """Retry on overload (503/429) with backoff, then try the next model in the list."""
    last = None
    for model in models:
        for attempt in range(4):
            try:
                return client.models.generate_content(model=model, contents=contents, config=cfg)
            except genai.errors.APIError as e:
                last = e
                if e.code in (429, 500, 503, 504):
                    wait = 2 ** attempt
                    log(f"  [gemini] {model}: {e.code} {e.status}; retry in {wait}s")
                    time.sleep(wait)
                    continue
                if e.code == 404:
                    log(f"  [gemini] {model} not available; trying the next model")
                break
    raise last


def handle(client, model, robot: Robot, contents: list, tools, max_turns: int = 14) -> str:
    cfg = types.GenerateContentConfig(system_instruction=robot.system_prompt, tools=tools)
    for _ in range(max_turns):
        log("  [gemini] thinking...")
        t0 = time.time()
        resp = generate(client, [model, *FALLBACK_MODELS], contents, cfg)
        log(f"  [gemini] answered in {time.time() - t0:.1f} s")
        if not resp.candidates or resp.candidates[0].content is None:
            return f"(no answer from Gemini: {getattr(resp, 'prompt_feedback', None) or resp.candidates})"
        contents.append(resp.candidates[0].content)
        calls = resp.function_calls or []
        if not calls:
            return resp.text or ""
        parts = []
        for c in calls:
            args = dict(c.args or {})
            log(f"  [gemini] {c.name}({args})")
            if c.name == "fetch":
                result = robot.fetch(args.get("item", ""))
                parts.append(types.Part.from_function_response(name=c.name, response=result))
            elif c.name == "look":
                img = robot.look(args.get("camera", "front_wide"))
                parts.append(types.Part.from_function_response(
                    name=c.name, response={"ok": img is not None, "note": "image follows"}))
                if img:
                    parts.append(types.Part.from_bytes(data=img, mime_type="image/jpeg"))
            elif c.name == "stop":
                parts.append(types.Part.from_function_response(name=c.name, response=robot.stop()))
            elif c.name == "notify_staff":
                parts.append(types.Part.from_function_response(
                    name=c.name, response=robot.notify_staff(args.get("message", ""), args.get("urgency", "normal"))))
            else:
                parts.append(types.Part.from_function_response(name=c.name, response={"ok": False, "error": "unknown tool"}))
        contents.append(types.Content(role="user", parts=parts))
        if robot.aborted:
            return "Stopped."
    robot.stop()
    return "I stopped because this is taking too many steps."


def claude_tools(skills: dict) -> list[dict]:
    return [
        {"name": "fetch", "description": "Run the robot skill that picks this item and puts it in the bin. Blocks until done.",
         "input_schema": {"type": "object", "properties": {"item": {"type": "string", "enum": list(skills)}}, "required": ["item"]}},
        {"name": "look", "description": "Get a current image from a camera.",
         "input_schema": {"type": "object", "properties": {"camera": {"type": "string", "enum": ["front_wide", "high_oblique", "gripper"]}},
                          "required": ["camera"]}},
        {"name": "stop", "description": "Stop the arm immediately.", "input_schema": {"type": "object", "properties": {}}},
        {"name": "notify_staff", "description": NOTIFY_DESC,
         "input_schema": {"type": "object", "properties": {
             "message": {"type": "string"}, "urgency": {"type": "string", "enum": ["low", "normal", "high"]}},
             "required": ["message"]}},
    ]


CLAUDE_EFFORT = os.environ.get("CLAUDE_EFFORT", "low")  # Opus 5.5 always thinks; low keeps spoken replies quick


def claude_create(client, model: str, **kwargs):
    """messages.create for current Claude models: adaptive thinking (always on for Opus 5.5) at CLAUDE_EFFORT, no
    sampling parameters, and on Opus 5.5 / Sonnet 5.5 the server-side refusal fallback."""
    kwargs.setdefault("output_config", {"effort": CLAUDE_EFFORT})
    if model in _CLAUDE_FALLBACK_MODELS:
        return client.beta.messages.create(model=model, betas=[_CLAUDE_FALLBACK_BETA], fallbacks="default", **kwargs)
    return client.messages.create(model=model, **kwargs)


def handle_claude(client, model: str, robot: Robot, messages: list, tools, max_turns: int = 14) -> str:
    import base64
    for _ in range(max_turns):
        log("  [claude] thinking...")
        t0 = time.time()
        resp = claude_create(client, model, max_tokens=16000, system=robot.system_prompt, tools=tools,
                             messages=messages)
        log(f"  [claude] answered in {time.time() - t0:.1f} s")
        if resp.stop_reason == "refusal":
            robot.issue("llm_refusal", "warning", "The assistant declined a guest request",
                        reason=str(getattr(resp, "stop_details", "") or ""), snapshot=False)
            return "I'm sorry, I can't help with that. A staff member will be happy to assist you."
        messages.append({"role": "assistant", "content": resp.content})  # thinking blocks included, unchanged
        uses = [b for b in resp.content if b.type == "tool_use"]
        if not uses:
            return "".join(b.text for b in resp.content if b.type == "text")
        results = []
        for u in uses:
            log(f"  [claude] {u.name}({u.input})")
            if u.name == "fetch":
                content = json.dumps(robot.fetch(u.input.get("item", "")))
            elif u.name == "notify_staff":
                content = json.dumps(robot.notify_staff(u.input.get("message", ""), u.input.get("urgency", "normal")))
            elif u.name == "look":
                img = robot.look(u.input.get("camera", "front_wide"))
                content = ([{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                         "data": base64.b64encode(img).decode()}}]
                           if img else "camera unavailable")
            elif u.name == "stop":
                content = json.dumps(robot.stop())
            else:
                content = "unknown tool"
            results.append({"type": "tool_result", "tool_use_id": u.id, "content": content})
        messages.append({"role": "user", "content": results})
        if robot.aborted:
            return "Stopped."
    robot.stop()
    return "I stopped because this is taking too many steps."


def handle_demo(client, model, robot: Robot, contents, tools) -> str:
    """No LLM: keyword matching. For testing the UI/robot without an API key, or as an offline fallback."""
    text = contents[0]["content"].lower()
    items = [k for k in robot.skills if k in text]
    if any(w in text for w in ("stop", "halt")):
        robot.stop()
        return "Stopping."
    if not items:
        return "I can fetch: " + ", ".join(robot.skills) + "."
    for item in items:
        log("  [demo] look(front_wide)")
        robot.look("front_wide")
        log(f"  [demo] fetch({{'item': '{item}'}})")
        res = robot.fetch(item)
        if not res.get("ok"):
            return f"I could not fetch the {item}: {res.get('error') or res.get('note')}"
    return "Done: " + ", ".join(items) + " fetched."


def judge_prompt(kind: str, item: str, pickup: str = "", bin: str = "the bin", elapsed: float = 0.0,
                 motion: float | None = None, looks_like: str = "", **_) -> str:
    if kind == "pre":
        return (f"This is the front_wide camera of a robot workspace. {pickup} The bin is {bin}.\n"
                f"Is there a {item} on the table at the pick-up area (not already in the bin, not in the gripper)?\n"
                + (f"A {item} looks like this: {looks_like}. " if looks_like else "")
                + f"Only answer true if you can clearly see an object that is a {item}. Other objects (a rolled-up cloth, "
                  f"cables, boxes, the robot itself) do not count. If you are not sure, answer false.\n"
                'Answer ONLY with JSON: {"present": true or false, "what_i_see": "the object you think it is", "reason": "short"}')
    return (f"A robot arm is doing this task: pick up the {item} from the pick-up area and put it in the bin. {pickup} The bin is {bin}.\n"
            f"Image 1 was taken before the robot started. Image 2 is {elapsed:.0f} seconds later. "
            + (f"The arm's joints moved {motion:.1f} degrees in the last 3 seconds (a skill starts moving within a second or two).\n"
               if motion is not None else "")
            +
            "Decide the status:\n"
            '- "done": the {item} is now in the bin and the gripper has let go of it (it is no longer at the pick-up area).\n'
            '- "working": the arm is making progress (moving toward the item, carrying it, moving to the bin).\n'
            '- "stuck": the arm is not making progress (hovering without grasping, repeated failed grasps, not moving).\n'
            '- "failed": the item was dropped outside the bin, knocked away, or something else went wrong.\n'
            'Answer ONLY with JSON: {"status": "...", "reason": "short", "suggestion": "what a human could change to help, or empty"}'
            ).replace("{item}", item)


def parse_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text or "", re.S)
    try:
        return json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        return {}


def load_env():
    """Read KEY=VALUE lines from .env in the repo root and teleoperation/ (git-ignored) into os.environ, without
    overriding variables already set. ANTHROPIC_TOKEN is accepted as an alias of ANTHROPIC_API_KEY."""
    here = Path(__file__).resolve().parent
    for path in (here.parent / ".env", here / ".env"):
        if not path.is_file():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.removeprefix("export ").split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k and v and k not in os.environ:
                os.environ[k] = v
    if not os.environ.get("ANTHROPIC_API_KEY") and os.environ.get("ANTHROPIC_TOKEN"):
        os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_TOKEN"]


class Brain:
    """One backend (gemini / claude / demo) with a single entry point: ask(text) -> reply."""

    def __init__(self, backend: str, model: str | None, robot: Robot, judge_model: str | None = None):
        load_env()
        self.backend, self.robot = backend, robot
        if backend == "claude":
            import anthropic
            if not os.environ.get("ANTHROPIC_API_KEY"):
                sys.exit("Set ANTHROPIC_API_KEY.")
            self.model = model or DEFAULT_CLAUDE_MODEL
            self.client = anthropic.Anthropic(timeout=60.0, max_retries=3)
            self.tools, self.fn = claude_tools(robot.skills), handle_claude
        elif backend == "gemini":
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                sys.exit("Set GEMINI_API_KEY (Google AI Studio key).")
            self.model = model or "gemini-3.8-flash"
            self.client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=60_000))  # ms
            self.tools, self.fn = tool_declarations(robot.skills), handle
        else:
            self.model, self.client, self.tools, self.fn = "keywords", None, None, handle_demo
        self.judge_model = judge_model or self.model
        robot.judge = self.judge
        # Short conversation memory (plain text turns), so "towel or water?" -> "water, please" works.
        self.history: list[tuple[str, str]] = []  # (guest text, reply)
        self.last_active = 0.0

    MAX_HISTORY = 6            # remembered exchanges
    NEW_GUEST_AFTER_S = 300.0  # forget the conversation after this long without a request

    def reset(self):
        """New guest: forget the conversation."""
        self.history.clear()

    def judge(self, kind: str, item: str, images: list[bytes], **info) -> dict:
        """One quick vision call; returns a dict (empty if the answer could not be parsed, which callers treat as 'unknown')."""
        prompt = judge_prompt(kind, item, **info)
        labels = ["Image 1 (before)", "Image 2 (now)"] if len(images) == 2 else ["Image"]
        try:
            if self.backend == "demo":
                el = float(info.get("elapsed", 0))
                return {"present": True, "reason": "demo"} if kind == "pre" else \
                       {"status": "done" if el > 9 else "working", "reason": "demo", "suggestion": ""}
            if self.backend == "claude":
                content = []
                for lab, img in zip(labels, images):
                    import base64
                    content += [{"type": "text", "text": lab + ":"},
                                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                             "data": base64.b64encode(img).decode()}}]
                content.append({"type": "text", "text": prompt})
                # room for Opus 5.5's (always-on) thinking before the short JSON answer
                r = claude_create(self.client, self.judge_model, max_tokens=4000,
                                  messages=[{"role": "user", "content": content}])
                return parse_json("".join(b.text for b in r.content if b.type == "text"))
            parts = []
            for lab, img in zip(labels, images):
                parts += [types.Part(text=lab + ":"), types.Part.from_bytes(data=img, mime_type="image/jpeg")]
            parts.append(types.Part(text=prompt))
            r = generate(self.client, [self.judge_model, *FALLBACK_MODELS], [types.Content(role="user", parts=parts)],
                         types.GenerateContentConfig())
            return parse_json(r.text)
        except Exception as e:
            log(f"  [judge] check failed ({e!r}); continuing without it")
            return {}

    def ask(self, text: str) -> str:
        self.robot.attempts.clear()
        self.robot.aborted = False
        self.robot.request = text
        if time.time() - self.last_active > self.NEW_GUEST_AFTER_S:
            self.reset()
        self.last_active = time.time()
        if self.backend == "demo":
            contents = [{"role": "user", "content": text}]
        elif self.backend == "claude":
            contents = [m for u, a in self.history for m in ({"role": "user", "content": u},
                                                              {"role": "assistant", "content": a})]
            contents.append({"role": "user", "content": text})
        else:
            contents = [types.Content(role=r, parts=[types.Part(text=t)])
                        for u, a in self.history for r, t in (("user", u), ("model", a))]
            contents.append(types.Content(role="user", parts=[types.Part(text=text)]))
        reply = self.fn(self.client, self.model, self.robot, contents, self.tools)
        if reply and not self.robot.aborted:
            self.history = (self.history + [(text, reply)])[-self.MAX_HISTORY:]
        self.last_active = time.time()
        return reply


def add_backend_args(p):
    p.add_argument("--server", default="http://127.0.0.1:8000")
    p.add_argument("--backend", choices=["gemini", "claude", "demo"], default="claude")
    p.add_argument("--judge-model", default=None,
                   help="model for the quick progress checks every few seconds (default: same as --model; a smaller, faster one is fine)")
    p.add_argument("--model", default=None,
                   help=f"gemini default gemini-3.8-flash; claude default {DEFAULT_CLAUDE_MODEL} (any current model with vision + tools)")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_backend_args(p)
    args = p.parse_args()
    robot = Robot(args.server)
    brain = Brain(args.backend, args.model, robot, args.judge_model)
    print(f"skills: {list(robot.skills)}   backend: {args.backend}   model: {brain.model}\n"
          "Type a request (e.g. 'I need a towel'), or 'quit'. Ctrl-C during a skill stops the arm.")
    while True:
        try:
            text = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text in ("quit", "exit"):
            break
        if not text:
            continue
        try:
            print("robot>", brain.ask(text) or "(empty reply)")
        except KeyboardInterrupt:
            robot.stop()
            print("\n(stopped)")
        except Exception as e:
            robot.stop()
            print(f"error: {e!r}")


if __name__ == "__main__":
    main()
