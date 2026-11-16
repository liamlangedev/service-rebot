#!/usr/bin/env python3
"""Web UI for the robot assistant: live cameras, animated face, chat, voice (browser), big STOP button.

  python robot_server.py --port <PORT> --policy <checkpoint> ...        # terminal 1
  python web_ui.py --backend claude                                      # terminal 2, then open http://localhost:8080

Voice uses the browser's own speech recognition and speech synthesis (use Chrome or Edge; no extra API key).
No robot: `python robot_server.py --fake` and `python web_ui.py --backend demo`.
"""
import argparse
import asyncio
import json
import threading
import time
from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel

import orchestrator as orch

WEB = Path(__file__).resolve().parent / "web"


class Say(BaseModel):
    text: str


def make_app(brain: orch.Brain, robot_url: str) -> FastAPI:
    app = FastAPI(title="reBot assistant")
    robot = brain.robot
    http = httpx.Client(base_url=robot_url, timeout=10.0)
    subs: list[asyncio.Queue] = []
    loop_ref: dict = {}
    busy = threading.Lock()

    def emit(kind: str, text: str):
        ev = {"kind": kind, "text": text, "t": time.time()}
        lp = loop_ref.get("loop")
        if lp:
            for q in list(subs):
                lp.call_soon_threadsafe(q.put_nowait, ev)

    orch.EVENT = emit

    @app.on_event("startup")
    async def _startup():
        loop_ref["loop"] = asyncio.get_running_loop()

    @app.get("/")
    def index():
        return FileResponse(WEB / "index.html")

    @app.get("/api/info")
    def info():
        return {"skills": robot.skills, "backend": brain.backend, "model": brain.model}

    @app.get("/api/status")
    def status():
        try:
            return http.get("/status").json()
        except Exception as e:
            return JSONResponse({"state": "offline", "error": str(e)}, status_code=200)

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
            except Exception as e:
                robot.stop()
                emit("error", f"{e!r}")
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
    print(f"UI on http://{args.host}:{args.port}   backend {args.backend} ({brain.model})   skills {list(robot.skills)}")
    try:
        uvicorn.run(make_app(brain, args.server), host=args.host, port=args.port, log_level="warning")
    finally:
        try:
            robot.stop()  # quitting the UI must not leave the arm running
        except Exception:
            pass


if __name__ == "__main__":
    main()
