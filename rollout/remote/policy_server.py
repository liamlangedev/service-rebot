"""Policy inference server for rollouts on a remote GPU (HF Jobs, see rollout/remote/README.md).

    python policy_server.py --port 8000 --device cuda

Stdlib HTTP + JSON, one request at a time. It wraps the same PolicyRunner the local
rollout uses (copied next to this file as the `grasp_policy` package), so units,
relative anchoring and camera handling are identical.

    POST /load     {"policy", "subfolder", "mode", "use_cameras", "task"}  -> {"key", "cameras", "chunk_size"}
    POST /start    {"key", "anchor": [7]}                                 -> {"ok": true}
    POST /predict  {"key", "state": [7], "images": {cam: base64 JPEG}}    -> {"actions": [[7]...], "clipped", "infer_ms"}
    GET  /health                                                          -> {"ok": true, "loaded": [...]}

Loaded policies are cached by their load request, so one server can serve several models.
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from grasp_policy.runner import PolicyRunner, RunnerConfig  # noqa: E402

RUNNERS: dict[str, PolicyRunner] = {}
LOCK = threading.Lock()
DEVICE = "cuda"


def _key(req: dict) -> str:
    return json.dumps({k: req.get(k) for k in ("policy", "subfolder", "mode", "use_cameras", "task")},
                      sort_keys=True)


def load(req: dict) -> dict:
    key = _key(req)
    if key not in RUNNERS:
        path = req["policy"]
        if req.get("subfolder"):
            from huggingface_hub import snapshot_download
            sub = req["subfolder"]
            path = str(Path(snapshot_download(path, allow_patterns=[f"{sub}/*"])) / sub)
        tic = time.monotonic()
        RUNNERS[key] = PolicyRunner(RunnerConfig(
            policy_path=path, mode=req.get("mode", "absolute"), device=DEVICE,
            task=req.get("task") or "", max_offset_deg=float(req.get("max_offset_deg", 180.0)),
            use_cameras=tuple(req["use_cameras"]) if req.get("use_cameras") else None))
        print(f"loaded {req['policy']} {req.get('subfolder') or ''} in "
              f"{time.monotonic() - tic:.1f} s", flush=True)
    r = RUNNERS[key]
    return {"key": key, "cameras": {n: list(hw) for n, hw in
                                    zip(r.camera_names, r.cameras.values())},
            "chunk_size": r.chunk_size}


def decode(b64: str) -> np.ndarray:
    import cv2
    buf = np.frombuffer(base64.b64decode(b64), np.uint8)
    bgr = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    return np.ascontiguousarray(bgr[:, :, ::-1])


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, obj: dict) -> None:
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if self.path.rstrip("/") in ("", "/health"):
            self._send(200, {"ok": True, "device": DEVICE,
                             "loaded": [json.loads(k)["policy"] for k in RUNNERS]})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):  # noqa: N802
        try:
            n = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(n) or b"{}")
            with LOCK:
                if self.path == "/load":
                    out = load(req)
                elif self.path == "/start":
                    RUNNERS[req["key"]].start(np.asarray(req["anchor"], np.float32))
                    out = {"ok": True}
                elif self.path == "/predict":
                    r = RUNNERS[req["key"]]
                    imgs = {c: decode(b) for c, b in req["images"].items()}
                    tic = time.monotonic()
                    acts, clipped = r.predict(np.asarray(req["state"], np.float32), imgs,
                                              n=req.get("n") or r.chunk_size)
                    out = {"actions": acts.tolist(), "clipped": clipped,
                           "infer_ms": (time.monotonic() - tic) * 1000}
                else:
                    self._send(404, {"error": f"unknown path {self.path}"})
                    return
            self._send(200, out)
        except Exception as exc:  # noqa: BLE001 - reported to the client
            traceback.print_exc()
            self._send(500, {"error": f"{type(exc).__name__}: {exc}"})

    def log_message(self, fmt, *args):  # quieter: one line per request
        print(f"{self.address_string()} {fmt % args}", flush=True)


def main() -> None:
    global DEVICE
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--device", default="cuda")
    p.add_argument("--preload", nargs="*", default=[],
                   help="policies to load at start, as JSON load requests")
    a = p.parse_args()
    DEVICE = a.device
    for req in a.preload:
        load(json.loads(req))
    print(f"policy server on :{a.port} ({DEVICE})", flush=True)
    ThreadingHTTPServer(("0.0.0.0", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
