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

from rebot_trash_sorting_agent.perception.detector import Detection, YoloeDetector, annotate, discovery_vocabulary

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
         grid-template-columns:minmax(0,1fr) 320px; gap:12px; padding:12px; }
  .left-col { display:grid; grid-template-rows:minmax(0,1fr) auto; gap:12px; min-height:0; }
    .cam-pair { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; align-items:start; min-height:0; }
  .right-col { display:flex; flex-direction:column; gap:12px; min-height:0; }
  .panel { background:var(--panel); border:1px solid var(--line); border-radius:10px;
           overflow:hidden; display:flex; flex-direction:column; min-height:0; }
  .panel h2 { font-size:11px; text-transform:uppercase; letter-spacing:.08em; color:var(--dim);
              margin:0; padding:7px 12px; border-bottom:1px solid var(--line); flex:0 0 auto;
              display:flex; justify-content:space-between; align-items:center; gap:8px; }
  .cam-meta { font:11px ui-monospace,monospace; text-transform:none; letter-spacing:0; color:var(--dim); }
  .video { width:100%; flex:1 1 auto; min-height:0; display:block; background:#000; object-fit:contain; border:0; }
    .cam-pair img.video { flex:0 0 auto; height:auto; aspect-ratio:4/3; object-fit:contain; }
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
  .log .obs { color:#79c0ff; }
  .log .act { color:#7ee787; }
  .log .err { color:var(--bad); }
  .log .ok { color:var(--ok); }
  .log .note { color:var(--warn); }
  .objs-wrap { flex:1 1 auto; min-height:0; max-height:170px; overflow:auto; }
  table.objs-tbl { width:100%; border-collapse:collapse; font:11px ui-monospace,monospace; }
  table.objs-tbl th, table.objs-tbl td { padding:4px 10px; text-align:left; border-bottom:1px solid #232b36; }
  table.objs-tbl th { color:var(--dim); font-weight:600; position:sticky; top:0; background:var(--panel); }
  table.objs-tbl tr.remembered { opacity:.55; }
  .chip { display:inline-block; width:9px; height:9px; border-radius:2px;
          margin-right:6px; vertical-align:baseline; border:1px solid #444; }
  .task-hdr { color:var(--warn); font-weight:600; font-size:12px; }
  .chatmsg { font:11px ui-monospace,monospace; color:var(--dim); margin-top:6px; min-height:15px; }
    dd { min-width:0; overflow-wrap:anywhere; }
    header { flex-wrap:wrap; }
    .task-hdr { overflow-wrap:anywhere; min-width:0; }
    @media (max-width:900px) {
        html,body { height:auto; min-height:100%; overflow:auto; }
        main { grid-template-columns:minmax(0,1fr); }
        .left-col { grid-template-rows:300px auto; }
        .cam-pair { grid-template-columns:minmax(0,1fr); }
        .events-panel { height:220px; flex:none; }
    }
</style></head><body>
<header>
  <h1>reBot trash sorting</h1>
  <span id="state" class="badge">connecting</span>
  <span id="task-hdr" class="task-hdr"></span>
  <span id="model" class="meta"></span>
</header>
<main>
  <section class="left-col">
    <div class="panel">
      <h2>MuJoCo 3D view (interactive)</h2>
      <iframe id="sim3d" class="video" title="mujoco 3d view"></iframe>
    </div>
    <div class="cam-pair">
      <div class="panel">
        <h2><span>Table camera</span><span id="table-meta" class="cam-meta"></span></h2>
        <img class="video" src="/stream" alt="table camera">
      </div>
      <div class="panel">
                <h2><span>Front camera</span><span id="front-meta" class="cam-meta"></span></h2>
                <img class="video" src="/front_stream" alt="front camera">
            </div>
            <div class="panel">
        <h2><span>Wrist camera</span><span id="wrist-meta" class="cam-meta"></span></h2>
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
        <div id="chatmsg" class="chatmsg"></div>
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
    <div class="panel">
      <h2>Objects</h2>
      <div class="objs-wrap">
        <table class="objs-tbl">
          <thead><tr><th>object</th><th>color</th><th>pos (m) / px</th><th>state</th></tr></thead>
          <tbody id="objs"></tbody>
        </table>
      </div>
    </div>
  </section>
</main>
<script>
const $ = (id) => document.getElementById(id);
$("sim3d").src = `${location.protocol}//${location.hostname}:8765/?embed=1`;
let lastEventKey = "";
const SWATCH = {red:"#e5484d", orange:"#f76b15", yellow:"#ffe629", green:"#46a758",
  cyan:"#00a2c7", blue:"#0090ff", purple:"#8e4ec6", pink:"#f76190",
  brown:"#ad7f58", white:"#eee", gray:"#888", silver:"#b8c0cc", black:"#111"};
function colorOf(o) {
  if (o.color) return o.color;
  const words = String(o.label || "").toLowerCase().split(/\s+/);
  return words.find(w => SWATCH[w]) || "";
}
function esc(v) { return String(v ?? "").replace(/[<>&]/g, ""); }

async function refresh() {
  try {
    const s = await (await fetch("/api/status", {cache:"no-store"})).json();
    const badge = $("state");
    badge.textContent = s.state || "idle";
    badge.className = "badge " + (s.state || "idle");
    $("task-hdr").textContent = s.task ? `task: ${s.task}` : "";
    $("table-meta").textContent = s.table_stats || "";
    $("wrist-meta").textContent = s.wrist_stats || "";
    $("front-meta").textContent = s.front_stats || "";
    const camCount = (s.frames > 0 ? 1 : 0) + (s.wrist_frames > 0 ? 1 : 0) + (s.front_frames > 0 ? 1 : 0);
    $("model").textContent = [
      `${camCount} cams`,
      s.provider && s.model ? `${s.provider}/${s.model}` : (s.provider || s.model),
      s.calibrated ? "calibrated" : "uncalibrated",
      s.dry_run ? "dry run" : null,
    ].filter(Boolean).join(" · ");
    $("run").disabled = !!s.busy;
    const facts = [
      ["camera", s.calibrated ? "calibrated" : "NOT calibrated"],
      ["frames", `${s.frames} / wrist ${s.wrist_frames || 0}`],
      ["objects", (s.objects || []).length || (s.live_detections || []).length],
    ["holding", s.holding || "nothing confirmed"],
    ["classes", (s.detector_classes || []).join(", ")],
      ["task", s.task || "—"],
    ];
    if (s.result) facts.push(["result", s.result.success ? "success" : "failed"]);
    $("facts").innerHTML = facts.map(([k, v]) =>
      `<dt>${k}</dt><dd>${esc(v)}</dd>`).join("");
    const worldObjs = s.objects || [];
    const liveObjs = s.live_detections || [];
    if (worldObjs.length) {
      $("objs").innerHTML = worldObjs.map(o => {
        const c = colorOf(o);
        return `<tr class="${esc(o.state)}"><td>${esc(o.label)}</td>` +
          `<td><span class="chip" style="background:${SWATCH[c] || "#333"}"></span>${esc(c || "?")}</td>` +
          `<td>[${Number(o.x).toFixed(3)}, ${Number(o.y).toFixed(3)}]${o.height_m != null ? ` h=${Number(o.height_m).toFixed(3)}` : ""}</td>` +
          `<td>${esc(o.state)}</td></tr>`;
      }).join("");
    } else if (liveObjs.length) {
      $("objs").innerHTML = liveObjs.map(o => {
        const c = colorOf(o);
        return `<tr><td>${esc(o.label)}</td>` +
          `<td><span class="chip" style="background:${SWATCH[c] || "#333"}"></span>${esc(c || "?")}</td>` +
          `<td>px (${o.bbox.map(v => Math.round(v)).join(", ")})</td>` +
          `<td>live ${(o.score * 100).toFixed(0)}%</td></tr>`;
      }).join("");
    } else {
      $("objs").innerHTML = `<tr><td colspan="4" style="color:var(--dim)">no objects detected yet</td></tr>`;
    }
    const events = s.events || [];
    const key = events.length + ":" + (events[events.length-1]?.ts ?? "");
    if (key !== lastEventKey) {
      lastEventKey = key;
      const log = $("log");
      const stick = log.scrollTop + log.clientHeight >= log.scrollHeight - 8;
      log.innerHTML = events.map(e => {
        const cls = (e.kind === "task_error" || (e.kind === "tool_result" && !e.ok)) ? "err"
                  : (e.kind === "task_done" && e.success) ? "ok"
                  : (e.kind === "tool_call" || e.kind === "action") ? "act"
                  : (e.kind === "observation" || e.kind === "plan") ? "obs"
                  : (e.kind === "note") ? "note" : "";
        const detail = e.summary || e.error || e.tool || e.text || "";
        return `<div class="${cls}"><b>${e.ts}s</b> ${esc(e.kind)} ${esc(detail).slice(0,180)}</div>`;
      }).join("");
      if (stick) log.scrollTop = log.scrollHeight;
    }
  } catch (err) {
    $("state").textContent = "offline";
    $("state").className = "badge failed";
  }
}

async function post(path, body, okMsg) {
  const msg = $("chatmsg");
  msg.textContent = "sending...";
  try {
    const r = await (await fetch(path, {method:"POST", headers:{"Content-Type":"application/json"},
                                      body: JSON.stringify(body || {})})).json();
    msg.textContent = r.ok ? okMsg : (r.error || "request failed");
  } catch (err) {
    msg.textContent = "error: " + err;
  }
  refresh();
}

$("run").onclick = () => {
  const task = $("task").value.trim();
  if (task) post("/api/task", {task}, `running: ${task}`);
};
$("stop").onclick = () => post("/api/stop", {}, "stop requested — aborting current action");
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
        self._frame_seq = 0
        self._frame_fps = 0.0
        self._wrist_frame: np.ndarray | None = None
        self._wrist_stamp = 0.0
        self._wrist_seq = 0
        self._wrist_fps = 0.0
        self._front_frame: np.ndarray | None = None
        self._front_stamp = 0.0
        self._front_seq = 0
        self._front_fps = 0.0
        self._sim_frame: np.ndarray | None = None
        self._sim_stamp = 0.0
        self._bad_frame = 0
        self._jpeg_cache: dict[str, tuple[tuple, bytes]] = {}
        self._bboxes_enabled = True
        self._table_dets: list[Detection] = []
        self._wrist_dets: list[Detection] = []
        self._front_dets: list[Detection] = []
        self._perception_cfg = dict(config.perception)
        self._detector: YoloeDetector | None = None
        self._bbox_wake = threading.Event()
        self._bbox_wake.set()
        self._stop_event = threading.Event()

        self._task_pub = self.create_publisher(String, "/agent/task", 10)
        self._cancel_pub = self.create_publisher(Empty, "/agent/cancel", 10)
        self.create_subscription(String, "/agent/status", self._on_status, 10)
        self.create_subscription(CompressedImage, "/agent/annotated", self._on_annotated, 5)
        self.create_subscription(
            Image,
            config.capture_topic(table_camera),
            self._on_frame,
            qos_profile_sensor_data,
        )
        self.create_subscription(
            Image,
            "/sim_view/image_raw",
            self._on_sim_frame,
            qos_profile_sensor_data,
        )
        wrist_name = next((c["name"] for c in config.camera_list if c["name"] == "wrist"), None)
        if wrist_name:
            self.create_subscription(
                Image,
                config.capture_topic(wrist_name),
                self._on_wrist_frame,
                qos_profile_sensor_data,
            )
        if any(camera["name"] == "front_camera" and camera.get("enabled", True) for camera in config.camera_list):
            self.create_subscription(
                Image,
                config.capture_topic("front_camera"),
                self._on_front_frame,
                qos_profile_sensor_data,
            )

        import cv2

        self._cv2 = cv2
        self._server = ThreadingHTTPServer((host, port), _handler(self))
        self._thread = threading.Thread(target=self._server.serve_forever, name="dashboard_http", daemon=True)
        self._thread.start()
        self._detect_thread = threading.Thread(target=self._detect_loop, name="dashboard_detect", daemon=True)
        self._detect_thread.start()
        self.get_logger().info(f"dashboard on http://{host}:{port}")

    # ------------------------------------------------------------------ ros in
    def _on_status(self, msg: Any) -> None:
        try:
            data = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        with self._lock:
            self._status = data
            classes = discovery_vocabulary(data.get("detector_classes"))
            if classes and classes != self._perception_cfg.get("classes"):
                self._perception_cfg["classes"] = classes
                self._table_dets = []
                self._wrist_dets = []
                self._front_dets = []
                self._jpeg_cache.clear()

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
        now = time.monotonic()
        with self._lock:
            if self._frame_stamp > 0:
                dt = now - self._frame_stamp
                if dt > 0:
                    inst = 1.0 / dt
                    self._frame_fps = inst if self._frame_fps <= 0 else 0.8 * self._frame_fps + 0.2 * inst
            self._frame = frame
            self._frame_stamp = now
            self._frame_seq += 1

    def _on_wrist_frame(self, msg: Any) -> None:
        try:
            frame = imgmsg_to_bgr(msg)
        except Exception:  # noqa: BLE001
            return
        now = time.monotonic()
        with self._lock:
            if self._wrist_stamp > 0:
                dt = now - self._wrist_stamp
                if dt > 0:
                    inst = 1.0 / dt
                    self._wrist_fps = inst if self._wrist_fps <= 0 else 0.8 * self._wrist_fps + 0.2 * inst
            self._wrist_frame = frame
            self._wrist_stamp = now
            self._wrist_seq += 1

    def _on_sim_frame(self, msg: Any) -> None:
        try:
            frame = imgmsg_to_bgr(msg)
        except Exception:  # noqa: BLE001
            return
        with self._lock:
            self._sim_frame = frame
            self._sim_stamp = time.monotonic()

    def _on_front_frame(self, msg: Any) -> None:
        try:
            frame = imgmsg_to_bgr(msg)
        except Exception:
            return
        now = time.monotonic()
        with self._lock:
            if self._front_stamp > 0:
                elapsed = now - self._front_stamp
                if elapsed > 0:
                    measured = 1.0 / elapsed
                    self._front_fps = measured if self._front_fps <= 0 else 0.8 * self._front_fps + 0.2 * measured
            self._front_frame = frame
            self._front_stamp = now
            self._front_seq += 1

    # ------------------------------------------------------------------ http out
    def status_json(self) -> dict[str, Any]:
        with self._lock:
            status = dict(self._status)
            status["video_age_s"] = round(time.monotonic() - self._frame_stamp, 2)
            status["bad_frames"] = self._bad_frame
            status["bboxes"] = self._bboxes_enabled
            status["live_detections"] = [
                {"label": d.label, "score": round(d.score, 2), "bbox": [round(v, 1) for v in d.bbox]}
                for d in self._table_dets
            ]
            status["table_stats"] = _cam_stats(self._frame, self._frame_fps, len(self._table_dets))
            status["wrist_stats"] = _cam_stats(self._wrist_frame, self._wrist_fps, len(self._wrist_dets))
            status["front_stats"] = _cam_stats(self._front_frame, self._front_fps, len(self._front_dets))
            status.setdefault("frames", self._frame_seq)
            status.setdefault("wrist_frames", self._wrist_seq)
            status.setdefault("front_frames", self._front_seq)
            status.setdefault("detector_classes", self._perception_cfg.get("classes", []))
        return status

    def set_bboxes(self, enabled: bool) -> None:
        with self._lock:
            self._bboxes_enabled = bool(enabled)
            if not self._bboxes_enabled:
                self._table_dets = []
                self._wrist_dets = []
                self._front_dets = []
        if enabled:
            self._bbox_wake.set()
        self.get_logger().info(f"live bboxes {'enabled' if enabled else 'disabled'}")

    def _detect_loop(self) -> None:
        while not self._stop_event.is_set():
            with self._lock:
                enabled = self._bboxes_enabled
                table = None if self._frame is None else self._frame.copy()
                wrist = None if self._wrist_frame is None else self._wrist_frame.copy()
                front = None if self._front_frame is None else self._front_frame.copy()
                classes = list(self._perception_cfg.get("classes") or ())
            if not enabled:
                self._bbox_wake.wait(timeout=1.0)
                self._bbox_wake.clear()
                continue
            try:
                if table is None and wrist is None and front is None:
                    self._stop_event.wait(0.35)
                    continue
                if self._detector is None:
                    self._detector = YoloeDetector(self._perception_cfg)
                    self._detector.load()
                if classes:
                    self._detector.set_vocabulary(classes)
                t_dets = self._detector.detect(table) if table is not None else []
                w_dets = self._detector.detect(wrist) if wrist is not None else []
                f_dets = self._detector.detect(front) if front is not None else []
                with self._lock:
                    if self._bboxes_enabled and classes == list(self._perception_cfg.get("classes") or ()):
                        self._table_dets = t_dets
                        self._wrist_dets = w_dets
                        self._front_dets = f_dets
            except Exception as exc:  # noqa: BLE001
                self.get_logger().warning(f"live bbox detection failed: {exc}")
                self._stop_event.wait(1.0)
                continue
            self._stop_event.wait(0.35)

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
        """Annotated frame with HUD overlay and per-frame JPEG caching."""
        with self._lock:
            jpeg, jpeg_age = self._jpeg, time.monotonic() - self._jpeg_stamp
            frame, frame_age = self._frame, time.monotonic() - self._frame_stamp
            seq, fps = self._frame_seq, self._frame_fps
            bboxes = self._bboxes_enabled
            dets = list(self._table_dets) if bboxes else []
            agent_state = str(self._status.get("state", "idle"))
        if bboxes and not dets and jpeg is not None and jpeg_age < 0.5:
            return jpeg
        return self._render_stream("table", frame, frame_age, seq, dets, fps, agent_state)

    def wrist_jpeg(self) -> bytes | None:
        with self._lock:
            frame, frame_age = self._wrist_frame, time.monotonic() - self._wrist_stamp
            seq, fps = self._wrist_seq, self._wrist_fps
            bboxes = self._bboxes_enabled
            dets = list(self._wrist_dets) if bboxes else []
            agent_state = str(self._status.get("state", "idle"))
        return self._render_stream("wrist", frame, frame_age, seq, dets, fps, agent_state)

    def sim_jpeg(self) -> bytes | None:
        with self._lock:
            frame, frame_age = self._sim_frame, time.monotonic() - self._sim_stamp
        return self._encode(frame, frame_age)

    def front_jpeg(self) -> bytes | None:
        with self._lock:
            frame, age = self._front_frame, time.monotonic() - self._front_stamp
            detections = list(self._front_dets) if self._bboxes_enabled else []
            sequence, fps = self._front_seq, self._front_fps
            state = str(self._status.get("state", "idle"))
        return self._render_stream("front", frame, age, sequence, detections, fps, state)

    def _render_stream(
        self,
        name: str,
        frame: np.ndarray | None,
        age: float,
        seq: int,
        dets: list[Detection],
        fps: float,
        agent_state: str,
    ) -> bytes | None:
        if frame is None or age > 5.0:
            return None
        det_sig = tuple((d.label, round(d.score, 2), tuple(d.bbox), tuple(d.polygon)) for d in dets)
        cache_key = (seq, det_sig)
        cached = self._jpeg_cache.get(name)
        if cached is not None and cached[0] == cache_key:
            return cached[1]
        img = annotate(frame, dets) if dets else frame
        encoded = self._encode(img, age)
        if encoded is not None:
            self._jpeg_cache[name] = (cache_key, encoded)
        return encoded

    def _encode(self, frame: np.ndarray | None, age: float) -> bytes | None:
        if frame is None or age > 5.0:
            return None
        image = frame
        height, width = image.shape[:2]
        scale = min(1.0, 960.0 / max(height, width))
        if scale < 1.0:
            image = self._cv2.resize(
                image, (int(width * scale), int(height * scale)), interpolation=self._cv2.INTER_AREA
            )
        ok, buffer = self._cv2.imencode(".jpg", image, [int(self._cv2.IMWRITE_JPEG_QUALITY), 80])
        return buffer.tobytes() if ok else None

    def destroy_node(self) -> bool:
        self._stop_event.set()
        self._bbox_wake.set()
        self._server.shutdown()
        return super().destroy_node()


def _cam_stats(frame: np.ndarray | None, fps: float, dets: int) -> str:
    if frame is None:
        return "waiting..."
    h, w = frame.shape[:2]
    return f"{w}x{h} · {fps:.1f} fps · {dets} dets"


def _handler(node: DashboardNode):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *_args):
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
        def do_GET(self) -> None:
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
            elif self.path == "/front.jpg":
                data = node.front_jpeg()
                if data is None:
                    self._send(503, b"no frame", "text/plain")
                else:
                    self._send(200, data, "image/jpeg")
            elif self.path == "/stream":
                self._stream(node.jpeg)
            elif self.path == "/wrist_stream":
                self._stream(node.wrist_jpeg)
            elif self.path == "/front_stream":
                self._stream(node.front_jpeg)
            elif self.path == "/sim_stream":
                self._stream(node.sim_jpeg)
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self) -> None:
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
