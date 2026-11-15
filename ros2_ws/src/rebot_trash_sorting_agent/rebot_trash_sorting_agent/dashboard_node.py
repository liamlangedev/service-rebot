#!/usr/bin/env python3
"""A one-page operator dashboard: live camera, one text box, one STOP button.

Deliberately the same shape as ``teleoperation/teleop/vr_view.py``: a stdlib
``ThreadingHTTPServer`` serving an inline page, with rclpy spinning in the main
thread. No npm, no build step, no extra dependency.

    http://127.0.0.1:8090

Endpoints

    GET  /              the page
    GET  /stream        MJPEG of the latest camera frame (or the annotated one)
    GET  /api/status    agent status JSON (proxied from /agent/status)
    POST /api/task      {"task": "..."}  -> publishes /agent/task
    POST /api/stop      -> publishes /agent/cancel

It binds to 127.0.0.1 by default: this thing commands a robot arm, and there is no
authentication in front of it.
"""

from __future__ import annotations

import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import numpy as np
import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from .config import Config
from .ros_image import imgmsg_to_bgr

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>reBot trash sorting</title>
<style>
  :root { --bg:#11151c; --panel:#1a2029; --line:#2a3342; --fg:#dbe3ee; --dim:#8b98a9;
          --ok:#3fb950; --warn:#d29922; --bad:#f85149; --accent:#58a6ff; }
  * { box-sizing:border-box; }
  html, body { height:100%; overflow:hidden; }
  body { margin:0; background:var(--bg); color:var(--fg); display:flex; flex-direction:column;
         font:13px/1.4 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; }
  header { display:flex; align-items:center; gap:14px; padding:8px 16px; flex:0 0 auto;
           border-bottom:1px solid var(--line); background:var(--panel); }
  header h1 { font-size:15px; margin:0; font-weight:600; letter-spacing:.02em; }
  .badge { padding:2px 9px; border-radius:999px; font-size:12px; font-weight:600;
           background:#243040; color:var(--dim); text-transform:uppercase; letter-spacing:.06em; }
  .badge.running { background:#12303f; color:var(--accent); }
  .badge.done { background:#12301c; color:var(--ok); }
  .badge.failed,.badge.stopped { background:#3a1b1b; color:var(--bad); }
  header .meta { margin-left:auto; color:var(--dim); font-size:12px; }
  main { flex:1 1 auto; min-height:0; display:grid;
         grid-template-columns:minmax(0,1.7fr) minmax(300px,1fr); gap:12px; padding:12px; }
  .left-col { display:grid; grid-template-rows:minmax(0,1.15fr) minmax(0,1fr); gap:12px; min-height:0; }
  .cam-pair { display:grid; grid-template-columns:1fr 1fr; gap:12px; min-height:0; }
  .right-col { display:flex; flex-direction:column; gap:12px; min-height:0; }
  .panel { background:var(--panel); border:1px solid var(--line); border-radius:10px;
           overflow:hidden; display:flex; flex-direction:column; min-height:0; }
  .panel h2 { font-size:11px; text-transform:uppercase; letter-spacing:.08em; color:var(--dim);
              margin:0; padding:7px 12px; border-bottom:1px solid var(--line); flex:0 0 auto; }
  .video { width:100%; flex:1 1 auto; min-height:0; display:block; background:#000; object-fit:contain; border:0; }
  .body { padding:10px 12px; }
  textarea { width:100%; height:54px; resize:none; background:#0f141b; color:var(--fg);
             border:1px solid var(--line); border-radius:8px; padding:8px; font:inherit; }
  .row { display:flex; gap:8px; margin-top:8px; }
  button { flex:1; padding:8px 12px; border-radius:8px; border:1px solid var(--line);
           background:#202a36; color:var(--fg); font:inherit; font-weight:600; cursor:pointer; }
  button.primary { background:#1f6feb; border-color:#1f6feb; }
  button.danger { background:#8b1f1f; border-color:#a12626; }
  button:disabled { opacity:.45; cursor:not-allowed; }
  .hint { color:var(--dim); font-size:11px; margin-top:6px; }
  dl { display:grid; grid-template-columns:auto 1fr; gap:3px 12px; margin:0; font-size:12px; }
  dt { color:var(--dim); } dd { margin:0; text-align:right; font-variant-numeric:tabular-nums; }
  .events-panel { flex:1 1 auto; min-height:0; }
  .log { flex:1 1 auto; min-height:0; overflow:auto; padding:8px 12px; font:11px/1.45 ui-monospace,monospace; }
  .log div { padding:2px 0; border-bottom:1px solid #232b36; color:var(--dim); }
  .log b { color:var(--fg); font-weight:600; }
  .log .err { color:var(--bad); }
  .log .ok { color:var(--ok); }
  .objs { padding:5px 12px; font:11px ui-monospace,monospace; color:var(--dim);
          border-top:1px solid var(--line); flex:0 0 auto; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
</style></head><body>
<header>
  <h1>reBot trash sorting</h1>
  <span id="state" class="badge">connecting</span>
  <span id="model" class="meta"></span>
</header>
<main>
  <section class="left-col">
    <div class="panel">
      <h2>MuJoCo 3D view (interactive)</h2>
      <iframe id="sim3d" class="video" title="mujoco 3d view"></iframe>
      <div class="objs" id="objects">&mdash;</div>
    </div>
    <div class="cam-pair">
      <div class="panel">
        <h2>Table camera</h2>
        <img class="video" src="/stream" alt="table camera">
      </div>
      <div class="panel">
        <h2>Wrist camera</h2>
        <img class="video" src="/wrist_stream" alt="wrist camera">
      </div>
    </div>
  </section>
  <section class="right-col">
    <div class="panel">
      <h2>Task</h2>
      <div class="body">
        <textarea id="task" placeholder="Put the can in the bin"></textarea>
        <div class="row">
          <button id="run" class="primary">Run</button>
          <button id="stop" class="danger">STOP</button>
        </div>
        <div class="hint">Enter runs, Shift+Enter adds a line.</div>
      </div>
    </div>
    <div class="panel">
      <h2>Robot</h2>
      <div class="body"><dl id="facts"></dl></div>
    </div>
    <div class="panel events-panel">
      <h2>Events</h2>
      <div class="log" id="log"></div>
    </div>
  </section>
</main>
<script>
const $ = (id) => document.getElementById(id);
$("sim3d").src = `${location.protocol}//${location.hostname}:8765/?embed=1`;
let lastEventKey = "";

async function refresh() {
  try {
    const s = await (await fetch("/api/status", {cache:"no-store"})).json();
    const badge = $("state");
    badge.textContent = s.state || "idle";
    badge.className = "badge " + (s.state || "idle");
    $("model").textContent = [s.provider, s.model, s.dry_run ? "dry run" : null]
      .filter(Boolean).join(" · ");
    $("run").disabled = !!s.busy;
    const facts = [
      ["camera", s.calibrated ? "calibrated" : "NOT calibrated"],
      ["frames", s.frames],
      ["objects", (s.objects || []).length],
      ["task", s.task || "—"],
    ];
    if (s.result) facts.push(["result", s.result.success ? "success" : "failed"]);
    $("facts").innerHTML = facts.map(([k, v]) =>
      `<dt>${k}</dt><dd>${String(v).replace(/[<>&]/g, "")}</dd>`).join("");
    const objs = (s.objects || []).map(o =>
      `${o.label} (${o.state}) x=${o.x.toFixed(3)} y=${o.y.toFixed(3)}`).join("\n");
    $("objects").textContent = objs || "no objects detected yet";
    const events = s.events || [];
    const key = events.length + ":" + (events[events.length-1]?.ts ?? "");
    if (key !== lastEventKey) {
      lastEventKey = key;
      $("log").innerHTML = events.slice().reverse().map(e => {
        const cls = e.kind === "task_error" || e.kind === "tool_result" && !e.ok ? "err"
                  : e.kind === "task_done" && e.success ? "ok" : "";
        const detail = e.summary || e.error || e.tool || e.text || "";
        return `<div class="${cls}"><b>${e.ts}s</b> ${e.kind} ${String(detail).slice(0,180)}</div>`;
      }).join("");
    }
  } catch (err) {
    $("state").textContent = "offline";
    $("state").className = "badge failed";
  }
}

async function post(path, body) {
  await fetch(path, {method:"POST", headers:{"Content-Type":"application/json"},
                     body: JSON.stringify(body || {})});
  refresh();
}

$("run").onclick = () => {
  const task = $("task").value.trim();
  if (task) post("/api/task", {task});
};
$("stop").onclick = () => post("/api/stop");
$("task").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); $("run").click(); }
});
refresh();
setInterval(refresh, 900);
</script></body></html>
"""


class DashboardNode(Node):
    def __init__(self, config: Config, host: str, port: int, table_camera: str) -> None:
        super().__init__("dashboard_node")
        from sensor_msgs.msg import CompressedImage, Image
        from std_msgs.msg import Empty, String

        self._lock = threading.Lock()
        self._status: dict[str, Any] = {}
        self._jpeg: bytes | None = None
        self._jpeg_stamp = 0.0
        self._frame: np.ndarray | None = None
        self._frame_stamp = 0.0
        self._wrist_frame: np.ndarray | None = None
        self._wrist_stamp = 0.0
        self._sim_frame: np.ndarray | None = None
        self._sim_stamp = 0.0
        self._bad_frame = 0

        self._task_pub = self.create_publisher(String, "/agent/task", 10)
        self._cancel_pub = self.create_publisher(Empty, "/agent/cancel", 10)
        self.create_subscription(String, "/agent/status", self._on_status, 10)
        self.create_subscription(CompressedImage, "/agent/annotated", self._on_annotated, 5)
        self.create_subscription(
            Image, config.capture_topic(table_camera), self._on_frame, qos_profile_sensor_data
        )
        self.create_subscription(
            Image, "/sim_view/image_raw", self._on_sim_frame, qos_profile_sensor_data
        )
        wrist_name = next((c["name"] for c in config.camera_list if c["name"] == "wrist"), None)
        if wrist_name:
            self.create_subscription(
                Image, config.capture_topic(wrist_name), self._on_wrist_frame, qos_profile_sensor_data
            )

        import cv2

        self._cv2 = cv2
        self._server = ThreadingHTTPServer((host, port), _handler(self))
        self._thread = threading.Thread(target=self._server.serve_forever, name="dashboard_http",
                                        daemon=True)
        self._thread.start()
        self.get_logger().info(f"dashboard on http://{host}:{port}")

    # ------------------------------------------------------------------ ros in
    def _on_status(self, msg: Any) -> None:
        try:
            data = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        with self._lock:
            self._status = data

    def _on_annotated(self, msg: Any) -> None:
        with self._lock:
            self._jpeg = bytes(msg.data)
            self._jpeg_stamp = time.monotonic()

    def _on_frame(self, msg: Any) -> None:
        try:
            frame = imgmsg_to_bgr(msg)
        except Exception:  # noqa: BLE001 - one bad frame is not a dashboard outage
            self._bad_frame += 1
            return
        with self._lock:
            self._frame = frame
            self._frame_stamp = time.monotonic()

    def _on_wrist_frame(self, msg: Any) -> None:
        try:
            frame = imgmsg_to_bgr(msg)
        except Exception:  # noqa: BLE001
            return
        with self._lock:
            self._wrist_frame = frame
            self._wrist_stamp = time.monotonic()

    def _on_sim_frame(self, msg: Any) -> None:
        try:
            frame = imgmsg_to_bgr(msg)
        except Exception:  # noqa: BLE001
            return
        with self._lock:
            self._sim_frame = frame
            self._sim_stamp = time.monotonic()

    # ------------------------------------------------------------------ http out
    def status_json(self) -> dict[str, Any]:
        with self._lock:
            status = dict(self._status)
            status["video_age_s"] = round(time.monotonic() - self._frame_stamp, 2)
            status["bad_frames"] = self._bad_frame
        return status

    def submit(self, task: str) -> None:
        from std_msgs.msg import String

        message = String()
        message.data = task
        self._task_pub.publish(message)
        self.get_logger().info(f"dashboard task: {task}")

    def stop_robot(self) -> None:
        from std_msgs.msg import Empty

        self._cancel_pub.publish(Empty())

    def jpeg(self) -> bytes | None:
        """Annotated frame briefly after detection, otherwise the live camera frame."""
        with self._lock:
            jpeg, jpeg_age = self._jpeg, time.monotonic() - self._jpeg_stamp
            frame, frame_age = self._frame, time.monotonic() - self._frame_stamp
        if jpeg is not None and jpeg_age < 1.5:
            return jpeg
        return self._encode(frame, frame_age)

    def wrist_jpeg(self) -> bytes | None:
        with self._lock:
            frame, frame_age = self._wrist_frame, time.monotonic() - self._wrist_stamp
        return self._encode(frame, frame_age)

    def sim_jpeg(self) -> bytes | None:
        with self._lock:
            frame, frame_age = self._sim_frame, time.monotonic() - self._sim_stamp
        return self._encode(frame, frame_age)

    def _encode(self, frame: np.ndarray | None, age: float) -> bytes | None:
        if frame is None or age > 5.0:
            return None
        image = frame
        height, width = image.shape[:2]
        scale = min(1.0, 960.0 / max(height, width))
        if scale < 1.0:
            image = self._cv2.resize(image, (int(width * scale), int(height * scale)),
                                     interpolation=self._cv2.INTER_AREA)
        ok, buffer = self._cv2.imencode(".jpg", image, [int(self._cv2.IMWRITE_JPEG_QUALITY), 80])
        return buffer.tobytes() if ok else None

    def destroy_node(self) -> bool:
        self._server.shutdown()
        return super().destroy_node()


def _handler(node: DashboardNode):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *_args):  # noqa: D401 - silence per-request logging
            return

        # -------------------------------------------------------------- helpers
        def _send(self, code: int, body: bytes, ctype: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, payload: dict[str, Any], code: int = 200) -> None:
            self._send(code, json.dumps(payload).encode(), "application/json")

        # -------------------------------------------------------------- routes
        def do_GET(self) -> None:  # noqa: N802 - http.server API
            if self.path in ("/", "/index.html"):
                self._send(200, PAGE.encode(), "text/html; charset=utf-8")
            elif self.path == "/api/status":
                self._json(node.status_json())
            elif self.path == "/frame.jpg":
                data = node.jpeg()
                if data is None:
                    self._send(503, b"no frame", "text/plain")
                else:
                    self._send(200, data, "image/jpeg")
            elif self.path == "/wrist.jpg":
                data = node.wrist_jpeg()
                if data is None:
                    self._send(503, b"no frame", "text/plain")
                else:
                    self._send(200, data, "image/jpeg")
            elif self.path == "/sim.jpg":
                data = node.sim_jpeg()
                if data is None:
                    self._send(503, b"no frame", "text/plain")
                else:
                    self._send(200, data, "image/jpeg")
            elif self.path == "/stream":
                self._stream(node.jpeg)
            elif self.path == "/wrist_stream":
                self._stream(node.wrist_jpeg)
            elif self.path == "/sim_stream":
                self._stream(node.sim_jpeg)
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self) -> None:  # noqa: N802 - http.server API
            length = int(self.headers.get("Content-Length", "0") or 0)
            raw = self.rfile.read(length) if length else b"{}"
            try:
                payload = json.loads(raw or b"{}")
            except json.JSONDecodeError:
                self._json({"ok": False, "error": "invalid json"}, 400)
                return
            if self.path == "/api/task":
                task = str(payload.get("task", "")).strip()
                if not task:
                    self._json({"ok": False, "error": "empty task"}, 400)
                    return
                node.submit(task)
                self._json({"ok": True})
            elif self.path == "/api/stop":
                node.stop_robot()
                self._json({"ok": True})
            else:
                self._send(404, b"not found", "text/plain")

        # -------------------------------------------------------------- mjpeg
        def _stream(self, provider) -> None:
            boundary = "frame"
            self.send_response(200)
            self.send_header("Content-Type", f"multipart/x-mixed-replace; boundary={boundary}")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                while True:
                    data = provider()
                    if data is not None:
                        self.wfile.write(f"--{boundary}\r\n".encode())
                        self.wfile.write(b"Content-Type: image/jpeg\r\n")
                        self.wfile.write(f"Content-Length: {len(data)}\r\n\r\n".encode())
                        self.wfile.write(data)
                        self.wfile.write(b"\r\n")
                        self.wfile.flush()
                    time.sleep(1.0 / 30.0)
            except (BrokenPipeError, ConnectionResetError):
                return

    return Handler


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", default=None)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    parser.add_argument("--camera", default="table", help="camera whose frames are shown")
    args, ros_args = parser.parse_known_args(argv)

    rclpy.init(args=ros_args)
    node = DashboardNode(Config.load(args.config_dir), args.host, args.port, args.camera)
    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
