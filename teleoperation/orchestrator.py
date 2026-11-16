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

SYSTEM = """You are the brain of a robot arm that can fetch and tidy objects. The arm picks an object and puts it in
the designated bin. You control it ONLY through the tools:
- fetch(item): run the learned skill for one item. It blocks until done and supervises itself: it checks that the item is
  present first, watches the cameras while the arm works, and ends the skill as soon as the item is in the bin, or reports
  why it is stuck or failed. The result tells you what happened (status, reason, suggestion).
- look(camera): get a current camera image. Cameras: front_wide (whole workspace), high_oblique, gripper.
- stop(): stop the arm now.
Rules:
- To bring or tidy an item, just call fetch(item). If it says nothing is there, tell the user there is none left.
- Do NOT retry automatically after a failure. Tell the user briefly what happened and give the suggestion (for example
  "rotate the bottle a little"), then wait for them. Only retry if the user asks.
- Say just "Stopped." ONLY when the result status is "aborted" (the operator pressed STOP). For any other result, explain in a
  sentence what happened, using the reason and suggestion from the result.
- Fetch one item at a time. For "clean up", fetch each item type that has a skill, one after another, and stop if one fails.
- Items without a skill are not possible: say so.
- Keep spoken replies short (one or two sentences), friendly, and say what you are about to do before long actions."""


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
        self.skills = self.http.get("/skills").json()
        cfg = json.loads(config_path.read_text()) if config_path.exists() else {}
        self.scene, self.skill_cfg = cfg.get("scene", {}), cfg.get("skills", {})
        self.attempts: dict[str, int] = {}
        self.aborted = False
        self.judge = None  # set by Brain: judge(kind, item, images, **info) -> dict
        if "motion_deg_3s" not in self._status():
            log("  [robot] WARNING: robot_server.py is an old version (no motion data, no stop reasons). Restart it.")

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
                return {"ok": False, "status": "no_item", "message": f"There is no {item} left at the pick-up area, so nothing was done.",
                        "reason": pre.get("reason", "")}

        r = self.http.post("/run", json={"skill": item})
        if r.status_code != 200:
            return {"ok": False, "error": r.text}
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
    ])]


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
    cfg = types.GenerateContentConfig(system_instruction=SYSTEM, tools=tools)
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
    ]


def handle_claude(client, model: str, robot: Robot, messages: list, tools, max_turns: int = 14) -> str:
    import base64
    for _ in range(max_turns):
        log("  [claude] thinking...")
        t0 = time.time()
        resp = client.messages.create(model=model, max_tokens=1024, system=SYSTEM, tools=tools, messages=messages)
        log(f"  [claude] answered in {time.time() - t0:.1f} s")
        messages.append({"role": "assistant", "content": resp.content})
        uses = [b for b in resp.content if b.type == "tool_use"]
        if not uses:
            return "".join(b.text for b in resp.content if b.type == "text")
        results = []
        for u in uses:
            log(f"  [claude] {u.name}({u.input})")
            if u.name == "fetch":
                content = str(robot.fetch(u.input.get("item", "")))
            elif u.name == "look":
                img = robot.look(u.input.get("camera", "front_wide"))
                content = ([{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                         "data": base64.b64encode(img).decode()}}]
                           if img else "camera unavailable")
            elif u.name == "stop":
                content = str(robot.stop())
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


class Brain:
    """One backend (gemini / claude / demo) with a single entry point: ask(text) -> reply."""

    def __init__(self, backend: str, model: str | None, robot: Robot, judge_model: str | None = None):
        self.backend, self.robot = backend, robot
        if backend == "claude":
            import anthropic
            if not os.environ.get("ANTHROPIC_API_KEY"):
                sys.exit("Set ANTHROPIC_API_KEY.")
            self.model = model or "claude-sonnet-5"
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
                r = self.client.messages.create(model=self.judge_model, max_tokens=250,
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
        contents = ([{"role": "user", "content": text}] if self.backend in ("claude", "demo")
                    else [types.Content(role="user", parts=[types.Part(text=text)])])
        return self.fn(self.client, self.model, self.robot, contents, self.tools)


def add_backend_args(p):
    p.add_argument("--server", default="http://127.0.0.1:8000")
    p.add_argument("--backend", choices=["gemini", "claude", "demo"], default="gemini")
    p.add_argument("--judge-model", default=None,
                   help="model for the quick progress checks every few seconds (default: same as --model; a smaller, faster one is fine)")
    p.add_argument("--model", default=None,
                   help="gemini default gemini-3.8-flash; claude default claude-sonnet-5 (use any current model with vision + tools)")


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
