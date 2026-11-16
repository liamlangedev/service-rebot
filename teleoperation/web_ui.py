#!/usr/bin/env python3
"""Web UI for the robot concierge: a guest page and an operator dashboard.

  python robot_server.py --port <PORT> --policy <checkpoint> ...        # terminal 1
  python web_ui.py                                                       # terminal 2 (Claude Opus 5.5 by default)

  http://localhost:8080/           guest page: animated face, chat, voice, live cameras, STOP
  http://localhost:8080/operator   operator dashboard: issues (failed / stuck hand-outs, items that ran out, robot or
                                   assistant errors, staff requests from the concierge) with camera snapshots,
                                   acknowledge / resolve, STOP, Task done, New guest, conversation and technical log

Guests never see technical errors; those go to the operator dashboard (and logs/issues.json).
Voice uses the browser's speech recognition and synthesis (Chrome or Edge). Use --host 0.0.0.0 to open the operator
page from another device on the network.
No robot: `python robot_server.py --fake` and `python web_ui.py --backend demo`.
"""
import argparse
import asyncio
import json
import threading
import time
from collections import deque
from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel

import orchestrator as orch
from issues import IssueLog

WEB = Path(__file__).resolve().parent / "web"
LOGS = Path(__file__).resolve().parent / "logs"
GUEST_SORRY = "I'm sorry, something went wrong on my side. A staff member has been notified and will help you."


class Say(BaseModel):
    text: str


class IssueAction(BaseModel):
    note: str = ""


def make_app(brain: orch.Brain, robot_url: str) -> FastAPI:
    app = FastAPI(title="reBot concierge")
    robot = brain.robot
    http = httpx.Client(base_url=robot_url, timeout=10.0)
    subs: list[asyncio.Queue] = []
    loop_ref: dict = {}
    busy = threading.Lock()

    recent: deque = deque(maxlen=300)  # conversation + technical log, for an operator page opened later

    def emit(kind: str, text: str, **extra):
        ev = {"kind": kind, "text": text, "t": time.time(), **extra}
        if kind in ("user", "reply", "error", "log", "issue_log", "reset"):
            recent.append(ev)
        lp = loop_ref.get("loop")
        if lp:
            for q in list(subs):
                lp.call_soon_threadsafe(q.put_nowait, ev)

    issues = IssueLog(LOGS, on_change=lambda event, issue: emit(event, issue["message"], issue=issue))
    robot.report = lambda d: issues.add(**d)
    orch.EVENT = emit

    def monitor_robot():
        """Robot server unreachable -> one issue (deduplicated); back online -> resolved automatically."""
        offline = False
        while True:
            try:
                http.get("/status", timeout=3.0).raise_for_status()
                if offline:
                    offline = False
                    issues.resolve_kind("robot_offline", "robot server reachable again")
                    emit("log", "[robot] robot server is reachable again")
            except Exception as e:  # noqa: BLE001
                if not offline:
                    offline = True
                    issues.add("robot_offline", "error", "Robot server not reachable", reason=repr(e)[:200],
                               suggestion="check that robot_server.py is running (and the arm is powered)",
                               dedupe_s=3600)
            time.sleep(3.0)

    @app.on_event("startup")
    async def _startup():
        loop_ref["loop"] = asyncio.get_running_loop()
        threading.Thread(target=monitor_robot, daemon=True).start()

    # ---------------------------------------------------------------- pages
    @app.get("/")
    def index():
        return FileResponse(WEB / "index.html")

    @app.get("/operator")
    def operator():
        return FileResponse(WEB / "operator.html")

    @app.get("/api/info")
    def info():
        return {"skills": robot.skills, "backend": brain.backend, "model": brain.model,
                "judge_model": brain.judge_model}

    @app.get("/api/status")
    def status():
        try:
            return http.get("/status").json()
        except Exception as e:
            return JSONResponse({"state": "offline", "error": str(e)}, status_code=200)

    # ---------------------------------------------------------------- guest actions
    @app.post("/api/say")
    def say(req: Say):
        text = req.text.strip()
        if not text:
            return {"ok": False}
        if not busy.acquire(blocking=False):
            return JSONResponse({"ok": False, "error": "busy with another request"}, status_code=409)

        def work():
            try:
                emit("user", text)
                emit("state", "thinking")
                reply = brain.ask(text) or "Done."
                emit("reply", reply)
            except Exception as e:  # noqa: BLE001 - guests get a polite message, the operator the details
                try:
                    robot.stop()
                except Exception:  # noqa: BLE001
                    pass
                issues.add("assistant_error", "error", "The assistant failed while handling a request",
                           reason=repr(e)[:500], request=text,
                           suggestion="check the web_ui terminal; API key, network or robot server")
                emit("error", GUEST_SORRY)
            finally:
                emit("state", "idle")
                busy.release()

        threading.Thread(target=work, daemon=True).start()
        return {"ok": True}

    @app.post("/api/stop")
    def stop():
        robot.stop()  # also blocks any further robot action for this request
        emit("log", "STOP pressed")
        return {"ok": True}

    @app.post("/api/done")
    def done():
        robot.finish()
        emit("log", "[operator] marked the task as done")
        return {"ok": True}

    # ---------------------------------------------------------------- operator
    @app.post("/api/reset")
    def reset():
        """New guest: the concierge forgets the conversation."""
        brain.reset()
        emit("log", "[operator] new guest: conversation cleared")
        emit("reset", "new guest")
        return {"ok": True}

    @app.get("/api/recent")
    def recent_events():
        return {"events": list(recent)}

    @app.get("/api/issues")
    def list_issues():
        return {"issues": issues.list(), "counts": issues.counts()}

    @app.post("/api/issues/{iid}/{action}")
    def issue_action(iid: str, action: str, body: IssueAction | None = None):
        status_for = {"ack": "acknowledged", "resolve": "resolved", "reopen": "open"}
        if action not in status_for:
            raise HTTPException(404, f"unknown action {action!r}")
        issue = issues.set_status(iid, status_for[action], (body.note if body else ""))
        if issue is None:
            raise HTTPException(404, f"no issue {iid}")
        return issue

    @app.get("/api/issues/{iid}/snapshot")
    def issue_snapshot(iid: str):
        p = issues.snapshot_path(iid)
        if p is None:
            raise HTTPException(404, "no snapshot")
        return FileResponse(p, media_type="image/jpeg")

    @app.post("/api/issues/test")
    def issue_test():
        """Create a sample issue (to check the operator page and its alert sound)."""
        return issues.add("test", "warning", "Test issue from the operator page", reason="manual test",
                          suggestion="resolve it", snapshot=robot.look("front_wide"))

    # ---------------------------------------------------------------- streams
    @app.get("/api/events")
    async def events():
        q: asyncio.Queue = asyncio.Queue()
        subs.append(q)

        async def gen():
            try:
                yield "retry: 1000\n\n"
                while True:
                    try:
                        ev = await asyncio.wait_for(q.get(), timeout=15)
                        yield f"data: {json.dumps(ev)}\n\n"
                    except asyncio.TimeoutError:
                        yield ": keepalive\n\n"
            finally:
                subs.remove(q)

        return StreamingResponse(gen(), media_type="text/event-stream")

    @app.get("/api/cam/{name}")
    async def cam(name: str):
        """MJPEG stream proxied from the robot server (about 6 fps per camera)."""
        async def gen():
            async with httpx.AsyncClient(base_url=robot_url, timeout=5.0) as c:
                while True:
                    try:
                        r = await c.get("/frame", params={"camera": name})
                        if r.status_code == 200:
                            yield (b"--frame\r\nContent-Type: image/jpeg\r\nContent-Length: " + str(len(r.content)).encode()
                                   + b"\r\n\r\n" + r.content + b"\r\n")
                    except Exception:
                        pass
                    await asyncio.sleep(0.16)

        return StreamingResponse(gen(), media_type="multipart/x-mixed-replace; boundary=frame")

    return app


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    orch.add_backend_args(p)
    p.add_argument("--port", type=int, default=8080)
    p.add_argument("--host", default="127.0.0.1", help="0.0.0.0 to open it to other devices on the network")
    args = p.parse_args()
    robot = orch.Robot(args.server)
    brain = orch.Brain(args.backend, args.model, robot, args.judge_model)
    print(f"guest page    http://{args.host}:{args.port}/\n"
          f"operator page http://{args.host}:{args.port}/operator\n"
          f"backend {args.backend} ({brain.model}, checks: {brain.judge_model})   skills {list(robot.skills)}")
    try:
        uvicorn.run(make_app(brain, args.server), host=args.host, port=args.port, log_level="warning")
    finally:
        try:
            robot.stop()  # quitting the UI must not leave the arm running
        except Exception:
            pass


if __name__ == "__main__":
    main()
