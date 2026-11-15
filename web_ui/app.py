"""Standalone Web UI, 3-camera live feed, and VLM orchestrator (ROS-free)."""

from __future__ import annotations

import argparse
from dataclasses import replace
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import os
from pathlib import Path
import threading
import time
from typing import Any

import numpy as np
import yaml

from .agent.events import EventLog
from .agent.orchestrator import Orchestrator, OrchestratorSettings
from .agent.prompts import system_prompt
from .agent.tools import TOOLS
from .cameras import CameraRig, CameraStream
from .config import Config, load_env_files
from .digital_twin import DigitalTwin
from .perception.detector import Detection, YoloeDetector, annotate, discovery_vocabulary
from .perception.scene import SceneModel
from .perception.table_map import TableMap
from .skills.skills import SkillRunner
from .skills.vla_policy import VLAPolicyClient
from .types import TaskResult
from .vlm.json_tools import encode_jpeg
from .vlm.registry import list_provider_models, make_session

log = logging.getLogger(__name__)
_DISPLAY_CONFIDENCE = 0.5

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>reBot VLA Sorting</title>
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
         grid-template-columns:minmax(0,1fr) 400px; gap:12px; padding:12px; }
  .left-col { display:grid; grid-template-rows:auto minmax(0,1fr); gap:12px; min-height:0; }
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
  .chat-panel { flex:0 0 auto; }
  .chat-feed { max-height:140px; min-height:48px; overflow:auto; display:flex; flex-direction:column;
               gap:6px; padding:8px 10px; background:#0d1218; border-bottom:1px solid var(--line); }
  .bubble { max-width:92%; padding:6px 10px; border-radius:12px; font-size:12px; line-height:1.35;
            overflow-wrap:anywhere; white-space:pre-wrap; }
  .bubble.user { align-self:flex-end; background:#1f6feb; color:#fff; border-bottom-right-radius:4px; }
  .bubble.bot { align-self:flex-start; background:#222a36; color:var(--fg); border-bottom-left-radius:4px; }
  .bubble.bot.err { background:#3a1b1b; color:#ffb4ae; }
  .bubble.empty { align-self:center; color:var(--dim); font-size:11px; background:none; padding:6px 0; }
  .composer { display:flex; align-items:flex-end; gap:6px; background:#0f141b;
              border:1px solid var(--line); border-radius:14px; padding:6px 6px 6px 10px; }
  .composer:focus-within { border-color:var(--accent); }
  textarea { flex:1 1 auto; min-height:22px; max-height:96px; resize:none; background:transparent;
             color:var(--fg); border:0; outline:none; padding:4px 0; font:inherit; line-height:1.35; }
  .icon-btn { flex:0 0 auto; width:30px; height:30px; border-radius:999px; border:1px solid var(--line);
              background:#202a36; color:var(--fg); font:inherit; font-weight:700; cursor:pointer;
              display:inline-flex; align-items:center; justify-content:center; padding:0; }
  .icon-btn.primary { background:#1f6feb; border-color:#1f6feb; color:#fff; }
  .icon-btn.danger { background:#8b1f1f; border-color:#a12626; color:#fff; }
  .icon-btn:disabled { opacity:.4; cursor:not-allowed; }
  .hint { color:var(--dim); font-size:11px; margin-top:6px; display:flex; justify-content:space-between; gap:8px; }
  dl { display:grid; grid-template-columns:auto 1fr; gap:3px 12px; margin:0; font-size:12px; }
  dt { color:var(--dim); } dd { margin:0; text-align:right; font-variant-numeric:tabular-nums; min-width:0; overflow-wrap:anywhere; }
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
  .task-hdr { color:var(--warn); font-weight:600; font-size:12px; overflow-wrap:anywhere; min-width:0; }
  .chatmsg { font:11px ui-monospace,monospace; color:var(--dim); margin-top:6px; min-height:15px; }
  .model-select { background:#0f141b; color:var(--fg); border:1px solid var(--line);
                  border-radius:8px; padding:3px 8px; font:12px ui-monospace,monospace; cursor:pointer; }
  .model-select:disabled { opacity:.5; cursor:not-allowed; }
  header { flex-wrap:wrap; }
  @media (max-width:900px) {
    html,body { height:auto; min-height:100%; overflow:auto; }
    main { grid-template-columns:minmax(0,1fr); }
    .cam-pair { grid-template-columns:minmax(0,1fr); }
    .events-panel { height:220px; flex:none; }
  }
</style></head><body>
<header>
  <h1>reBot VLA sorting</h1>
  <span id="state" class="badge">connecting</span>
  <span id="task-hdr" class="task-hdr"></span>
  <span id="model" class="meta"></span>
  <select id="model-select" class="model-select" title="Switch VLM model"></select>
</header>
<main>
  <section class="left-col">
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
    <div class="panel">
      <h2><span>Simulation</span><span id="twin-meta" class="cam-meta"></span></h2>
      <iframe id="sim3d" class="video" title="simulation"></iframe>
    </div>
  </section>
  <section class="right-col">
    <div class="panel chat-panel">
      <h2>Chat</h2>
      <div id="chat-feed" class="chat-feed">
        <div class="bubble empty">Send a task to start...</div>
      </div>
      <div class="body">
        <div class="composer">
          <textarea id="task" rows="1" placeholder="Message robot (e.g. Put the can in the bin)..."></textarea>
          <button id="run" class="icon-btn primary" title="Send (Enter)">&#8593;</button>
          <button id="stop" class="icon-btn danger" title="Stop">&#9632;</button>
        </div>
        <div class="hint"><span>Enter to send · Shift+Enter newline</span><span id="chatmsg" class="chatmsg" style="margin-top:0"></span></div>
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
let lastResultKey = "";
function addBubble(role, text, isErr) {
  const feed = $("chat-feed");
  const empty = feed.querySelector(".empty");
  if (empty) empty.remove();
  const div = document.createElement("div");
  div.className = `bubble ${role}${isErr ? " err" : ""}`;
  div.textContent = text;
  feed.appendChild(div);
  feed.scrollTop = feed.scrollHeight;
}
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
    const twin = s.digital_twin || {};
    $("twin-meta").textContent = twin.error
      ? `err: ${twin.error}`
      : (twin.ready ? `${twin.camera} · ${twin.frames} frames · ${(twin.splats || []).length} splats` : "initializing...");
    const camCount = (s.frames > 0 ? 1 : 0) + (s.wrist_frames > 0 ? 1 : 0) + (s.front_frames > 0 ? 1 : 0);
    $("model").textContent = [
      `${camCount} cams`,
      s.dry_run ? "dry run" : null,
    ].filter(Boolean).join(" · ");
    const sel = $("model-select");
    const avail = s.available_models || [];
    const availSig = JSON.stringify(avail);
    if (sel.dataset.sig !== availSig) {
      sel.dataset.sig = availSig;
      sel.innerHTML = avail.map(m =>
        `<option value="${esc(m.provider)}::${esc(m.model)}">${esc(m.provider)}/${esc(m.model)}</option>`
      ).join("");
    }
    const curVal = `${s.provider}::${s.model}`;
    if ([...sel.options].some(o => o.value === curVal)) sel.value = curVal;
    sel.disabled = !!s.busy || avail.length <= 1;
    $("run").disabled = !!s.busy;
    const facts = [
      ["frames", `${s.frames} / front ${s.front_frames || 0} / wrist ${s.wrist_frames || 0}`],
      ["objects", (s.objects || []).length || (s.live_detections || []).length],
      ["vla", s.vla_backend || "stub"],
      ["joints", twin.joint_updates ? `${Object.keys(twin.joints || {}).length} streamed (${twin.joint_age_s}s)` : "not streamed"],
      ["classes", (s.detector_classes || []).join(", ")],
      ["task", s.task || "—"],
    ];
    if (s.result) {
      facts.push(["result", s.result.success ? "success" : "failed"]);
      const rk = `${s.task}:${s.result.success}:${s.result.summary}`;
      if (rk !== lastResultKey) {
        lastResultKey = rk;
        addBubble("bot", s.result.summary || s.result.error || (s.result.success ? "Done." : "Failed."), !s.result.success);
      }
    }
    $("facts").innerHTML = facts.map(([k, v]) =>
      `<dt>${k}</dt><dd>${esc(v)}</dd>`).join("");
    const worldObjs = s.objects || [];
    const liveObjs = s.live_detections || [];
    if (worldObjs.length) {
      $("objs").innerHTML = worldObjs.map(o => {
        const c = colorOf(o);
        return `<tr class="${esc(o.state)}"><td>${esc(o.label)}</td>` +
          `<td><span class="chip" style="background:${SWATCH[c] || "#333"}"></span>${esc(c || "?")}</td>` +
          `<td>[${Number(o.x).toFixed(3)}, ${Number(o.y).toFixed(3)}]</td>` +
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
      const logEl = $("log");
      const stick = logEl.scrollTop + logEl.clientHeight >= logEl.scrollHeight - 8;
      logEl.innerHTML = events.map(e => {
        const cls = (e.kind === "task_error" || (e.kind === "tool_result" && !e.ok)) ? "err"
                  : (e.kind === "task_done" && e.success) ? "ok"
                  : (e.kind === "tool_call" || e.kind === "action") ? "act"
                  : (e.kind === "observation" || e.kind === "plan") ? "obs"
                  : (e.kind === "note") ? "note" : "";
        const detail = e.summary || e.error || e.tool || e.text || "";
        return `<div class="${cls}"><b>${e.ts}s</b> ${esc(e.kind)} ${esc(detail).slice(0,180)}</div>`;
      }).join("");
      if (stick) logEl.scrollTop = logEl.scrollHeight;
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
  const el = $("task");
  const task = el.value.trim();
  if (!task) return;
  addBubble("user", task, false);
  el.value = "";
  el.style.height = "auto";
  post("/api/task", {task}, "running");
};
$("stop").onclick = () => post("/api/stop", {}, "stop requested");
$("model-select").onchange = (e) => {
  const [provider, model] = String(e.target.value || "").split("::");
  if (provider && model) post("/api/model", {provider, model}, `model: ${provider}/${model}`);
};
$("task").addEventListener("input", (e) => {
  e.target.style.height = "auto";
  e.target.style.height = Math.min(96, e.target.scrollHeight) + "px";
});
$("task").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); $("run").click(); }
});
refresh();
setInterval(refresh, 900);
</script></body></html>
"""


class LazyDetector:
    """Build the detector on first use so UI startup never blocks."""

    def __init__(self, cfg: dict[str, Any]) -> None:
        self._cfg = cfg
        self._inner: YoloeDetector | None = None
        self._lock = threading.Lock()
        self.classes: list[str] = list(cfg.get("classes") or ())

    def _ensure(self) -> YoloeDetector:
        if self._inner is None:
            with self._lock:
                if self._inner is None:
                    det = YoloeDetector(self._cfg)
                    det.load()
                    if self.classes:
                        det.set_vocabulary(self.classes)
                    self._inner = det
        return self._inner

    def set_vocabulary(self, classes: list[str]) -> None:
        self.classes = list(classes)
        self._ensure().set_vocabulary(self.classes)

    def detect(self, frame: np.ndarray) -> list[Detection]:
        return self._ensure().detect(frame)


def _load_yaml_section(config_dir: Path, filename: str, section: str) -> dict[str, Any]:
    path = config_dir / filename
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return dict(data.get(section) or data) if isinstance(data, dict) else {}


def _cam_stats(stream: CameraStream | None, dets: int) -> str:
    if stream is None:
        return "disabled"
    frame = stream.latest(max_age_s=5.0)
    if frame is None:
        return "waiting..."
    h, w = frame.shape[:2]
    return f"{w}x{h} · {stream.fps:.1f} fps · {dets} dets"


class DashboardApp:
    """In-process Web UI + 3-camera live feed + VLM orchestrator + VLA skills."""

    def __init__(
        self,
        config: Config,
        host: str = "127.0.0.1",
        port: int = 8090,
        table_camera: str = "table",
        *,
        dry_run: bool | None = None,
        provider: str | None = None,
        model: str | None = None,
        start_cameras: bool = True,
        start_server: bool = True,
    ) -> None:
        import cv2

        self._cv2 = cv2
        self._config = config
        self._host = host
        self._port = port
        self._table_name = table_camera
        self._dry_run = bool(config.run.get("dry_run", False) if dry_run is None else dry_run)
        self._provider = provider or config.vlm.provider
        self._model = model or config.vlm.model

        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._bbox_wake = threading.Event()

        self._perception_cfg = dict(config.perception)
        self._bboxes_enabled = bool(self._perception_cfg.get("live_bboxes", True))
        self._detector = LazyDetector(self._perception_cfg)
        self._scene = SceneModel(
            merge_radius=float(self._perception_cfg.get("merge_radius_m", 0.05)),
            ttl_s=float(self._perception_cfg.get("object_ttl_s", 45.0)),
        )
        tmap_cfg = config.table_map(table_camera)
        self._table_map = TableMap.from_mapping(tmap_cfg) if tmap_cfg else None

        self._rig = CameraRig(config.camera_list)
        if start_cameras:
            self._rig.start()

        vla_cfg = _load_yaml_section(config.directory, "vla.yaml", "vla")
        self._vla = VLAPolicyClient(vla_cfg)

        twin_cfg = _load_yaml_section(config.directory, "digital_twin.yaml", "digital_twin")
        self._twin = DigitalTwin(twin_cfg)
        if start_cameras:
            self._twin.start()

        self._table_dets: list[Detection] = []
        self._front_dets: list[Detection] = []
        self._wrist_dets: list[Detection] = []
        self._jpeg_cache: dict[str, tuple[tuple[int, tuple[Any, ...]], bytes]] = {}
        self._model_cache: dict[tuple[str, str], tuple[float, list[str]]] = {}

        self._state = "idle"
        self._task = ""
        self._result: dict[str, Any] | None = None
        self._events = EventLog(Path(str(config.run.get("log_dir", "~/.cache/rebot_agent/runs"))).expanduser())
        self._runner: SkillRunner | None = None
        self._orchestrator: Orchestrator | None = None
        self._worker: threading.Thread | None = None

        self._detect_thread = threading.Thread(target=self._detect_loop, name="live-bboxes", daemon=True)
        self._detect_thread.start()

        self._server: ThreadingHTTPServer | None = None
        if start_server:
            self._server = ThreadingHTTPServer((host, port), _handler(self))
            self._http_thread = threading.Thread(target=self._server.serve_forever, daemon=True)
            self._http_thread.start()
            log.info("dashboard listening on http://%s:%d", host, port)

    def _stream_for(self, name: str) -> CameraStream | None:
        stream = self._rig.get(name)
        if stream is None and name == "front":
            return self._rig.get("front_camera")
        return stream

    def _cached_provider_models(self, provider: str, api_key: str | None, base_url: str | None = None) -> list[str]:
        cache: dict[tuple[str, str], tuple[float, list[str]]] | None = getattr(self, "_model_cache", None)
        if cache is None:
            cache = {}
            self._model_cache = cache
        key = (provider, f"{api_key or ''}|{base_url or ''}")
        now = time.monotonic()
        entry = cache.get(key)
        if entry is not None and (now - entry[0]) < 300.0:
            return list(entry[1])
        models = list_provider_models(provider, api_key=api_key, base_url=base_url)
        cache[key] = (now, list(models))
        return list(models)

    def available_models(self) -> list[dict[str, str]]:
        """Return provider/model options whose credentials are available."""
        options: list[dict[str, str]] = []
        gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or self._config.api_key()
        if gemini_key:
            models = self._cached_provider_models("gemini", gemini_key)
            if self._provider == "gemini" and self._model not in models:
                models.insert(0, self._model)
            for m in models:
                options.append({"provider": "gemini", "model": m})

        openai_key = os.environ.get("OPENAI_API_KEY")
        base_url = self._config.vlm.base_url
        if openai_key or base_url:
            models = self._cached_provider_models("openai", openai_key, base_url=base_url)
            if self._provider == "openai" and self._model not in models:
                models.insert(0, self._model)
            for m in models:
                options.append({"provider": "openai", "model": m})

        anthropic_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY")
        if anthropic_key:
            models = self._cached_provider_models("anthropic", anthropic_key)
            if self._provider == "anthropic" and self._model not in models:
                models.insert(0, self._model)
            for m in models:
                options.append({"provider": "anthropic", "model": m})

        options.append({"provider": "mock", "model": "mock"})
        return options

    def set_model(self, provider: str, model: str) -> bool:
        allowed = {(m["provider"], m["model"]) for m in self.available_models()}
        if (provider, model) not in allowed:
            raise ValueError(f"model {provider}/{model} has no available credentials")
        with self._lock:
            if self._worker is not None and self._worker.is_alive():
                return False
            self._provider = provider
            self._model = model
        self._events.emit("note", text=f"switched model to {provider}/{model}")
        return True

    def _api_key_for(self, provider: str) -> str | None:
        if provider == "gemini":
            return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or self._config.api_key()
        if provider == "openai":
            return os.environ.get("OPENAI_API_KEY")
        if provider == "anthropic":
            return os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY")
        return None

    def status_json(self) -> dict[str, Any]:
        t_cam = self._stream_for(self._table_name)
        f_cam = self._stream_for("front")
        w_cam = self._stream_for("wrist")
        avail = self.available_models()
        with self._lock:
            return {
                "state": self._state,
                "busy": self._worker is not None and self._worker.is_alive(),
                "task": self._task,
                "result": self._result,
                "provider": self._provider,
                "model": self._model,
                "available_models": avail,
                "dry_run": self._dry_run,
                "vla_backend": self._vla.backend,
                "digital_twin": self._twin.status(),
                "frames": t_cam.frames_received if t_cam else 0,
                "front_frames": f_cam.frames_received if f_cam else 0,
                "wrist_frames": w_cam.frames_received if w_cam else 0,
                "table_stats": _cam_stats(t_cam, len(self._table_dets)),
                "front_stats": _cam_stats(f_cam, len(self._front_dets)),
                "wrist_stats": _cam_stats(w_cam, len(self._wrist_dets)),
                "objects": [o.summary() for o in self._scene.all()],
                "live_detections": [
                    {"label": d.label, "score": round(d.score, 2), "bbox": [round(v, 1) for v in d.bbox]}
                    for d in self._table_dets
                ],
                "detector_classes": list(self._detector.classes),
                "events": self._events.tail(80),
            }

    def submit(self, task: str) -> bool:
        task = (task or "").strip()
        if not task:
            return False
        with self._lock:
            if self._worker is not None and self._worker.is_alive():
                return False
            self._task = task
            self._state = "running"
            self._result = None
            self._worker = threading.Thread(target=self._run_task, args=(task,), name="orchestrator", daemon=True)
            self._worker.start()
        return True

    def stop_robot(self) -> None:
        if self._orchestrator is not None:
            self._orchestrator.cancel()
        if self._runner is not None:
            self._runner.cancel()
        self._vla.cancel()
        self._events.emit("note", text="stop requested by operator")

    def _run_task(self, task: str) -> None:
        self._scene.clear()
        self._vla.reset()
        t_cam = self._stream_for(self._table_name)
        runner = SkillRunner(
            places=self._config.places,
            scene=self._scene,
            camera=t_cam,
            detector=self._detector,
            vla=self._vla,
            events=self._events,
            table_map=self._table_map,
            cameras=self._rig.streams,
            plan_only=self._dry_run,
            baseline_classes=self._perception_cfg.get("classes") or (),
        )
        self._runner = runner
        settings = OrchestratorSettings(
            max_steps=int(self._config.run.get("max_steps", 12)),
            timeout_s=float(self._config.run.get("timeout_s", 240.0)),
            max_consecutive_errors=int(self._config.run.get("max_consecutive_errors", 3)),
        )
        try:
            vlm_settings = replace(self._config.vlm, provider=self._provider, model=self._model)
            session = make_session(
                vlm_settings,
                system_prompt(self._config.places),
                TOOLS,
                api_key=self._api_key_for(self._provider),
            )
            orch = Orchestrator(
                session=session,
                tools=TOOLS,
                runner=runner,
                events=self._events,
                settings=settings,
                scene=self._scene.summary_text,
                capture=lambda: _capture_jpeg(t_cam),
            )
            self._orchestrator = orch
            res: TaskResult = orch.run(task)
            with self._lock:
                self._result = {"success": res.success, "summary": res.summary, "steps": res.steps, "error": res.error}
                self._state = "stopped" if res.stopped else ("done" if res.success else "failed")
        except Exception as exc:  # noqa: BLE001
            self._events.emit("task_error", error=str(exc))
            with self._lock:
                self._result = {"success": False, "summary": str(exc), "steps": 0, "error": str(exc)}
                self._state = "failed"
        finally:
            self._orchestrator = None
            self._runner = None

    def _detect_loop(self) -> None:
        while not self._stop_event.is_set():
            if not self._bboxes_enabled:
                self._bbox_wake.wait(timeout=1.0)
                self._bbox_wake.clear()
                continue
            t_cam = self._stream_for(self._table_name)
            f_cam = self._stream_for("front")
            w_cam = self._stream_for("wrist")
            table = t_cam.latest(max_age_s=2.0) if t_cam else None
            front = f_cam.latest(max_age_s=2.0) if f_cam else None
            wrist = w_cam.latest(max_age_s=2.0) if w_cam else None
            if table is None and front is None and wrist is None:
                self._stop_event.wait(0.35)
                continue
            try:
                t_dets = self._detector.detect(table) if table is not None else []
                f_dets = self._detector.detect(front) if front is not None else []
                w_dets = self._detector.detect(wrist) if wrist is not None else []
                with self._lock:
                    self._table_dets = t_dets
                    self._front_dets = f_dets
                    self._wrist_dets = w_dets
            except Exception as exc:  # noqa: BLE001
                log.warning("live bbox detection failed: %s", exc)
                self._stop_event.wait(1.0)
                continue
            self._stop_event.wait(0.35)

    def jpeg(self) -> bytes | None:
        return self._camera_jpeg(self._table_name, self._table_dets)

    def front_jpeg(self) -> bytes | None:
        return self._camera_jpeg("front", self._front_dets)

    def wrist_jpeg(self) -> bytes | None:
        return self._camera_jpeg("wrist", self._wrist_dets)

    def _camera_jpeg(self, name: str, dets: list[Detection]) -> bytes | None:
        stream = self._stream_for(name)
        if stream is None:
            return None
        frame = stream.latest(max_age_s=5.0)
        if frame is None:
            return None
        seq = stream.frames_received
        filtered = [d for d in dets if d.score >= _DISPLAY_CONFIDENCE] if self._bboxes_enabled else []
        det_sig = tuple((d.label, round(d.score, 2), tuple(d.bbox), tuple(d.polygon)) for d in filtered)
        cache_key = (seq, det_sig)
        cached = self._jpeg_cache.get(name)
        if cached is not None and cached[0] == cache_key:
            return cached[1]
        img = annotate(frame, filtered) if filtered else frame
        encoded = self._encode(img)
        if encoded is not None:
            self._jpeg_cache[name] = (cache_key, encoded)
        return encoded

    def _encode(self, frame: np.ndarray | None) -> bytes | None:
        if frame is None:
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

    def sim_jpeg(self) -> bytes | None:
        return self._twin.latest_jpeg()

    def update_joints(self, joints: Any) -> dict[str, float]:
        return self._twin.update_joints(joints)

    def joints_json(self) -> dict[str, Any]:
        return self._twin.joints_snapshot()

    def close(self) -> None:
        self._stop_event.set()
        self._bbox_wake.set()
        self.stop_robot()
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
        self._rig.stop()
        self._twin.stop()


def _capture_jpeg(stream: CameraStream | None) -> bytes | None:
    if stream is None:
        return None
    frame = stream.latest(max_age_s=2.0)
    return None if frame is None else encode_jpeg(frame)


def _handler(app: DashboardApp):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *_args):
            return

        def _send(self, code: int, body: bytes, ctype: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, payload: dict[str, Any], code: int = 200) -> None:
            self._send(code, json.dumps(payload).encode(), "application/json")

        def do_GET(self) -> None:
            if self.path in ("/", "/index.html"):
                self._send(200, PAGE.encode(), "text/html; charset=utf-8")
            elif self.path == "/api/status":
                self._json(app.status_json())
            elif self.path == "/api/joints":
                self._json(app.joints_json())
            elif self.path == "/frame.jpg":
                self._serve_jpg(app.jpeg())
            elif self.path == "/front.jpg":
                self._serve_jpg(app.front_jpeg())
            elif self.path == "/wrist.jpg":
                self._serve_jpg(app.wrist_jpeg())
            elif self.path == "/sim.jpg":
                self._serve_jpg(app.sim_jpeg())
            elif self.path == "/stream":
                self._stream(app.jpeg)
            elif self.path == "/front_stream":
                self._stream(app.front_jpeg)
            elif self.path == "/wrist_stream":
                self._stream(app.wrist_jpeg)
            elif self.path == "/sim_stream":
                self._stream(app.sim_jpeg)
            else:
                self._send(404, b"not found", "text/plain")

        def _serve_jpg(self, data: bytes | None) -> None:
            if data is None:
                self._send(503, b"no frame", "text/plain")
            else:
                self._send(200, data, "image/jpeg")

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
                if not app.submit(task):
                    self._json({"ok": False, "error": "agent is busy"}, 409)
                    return
                self._json({"ok": True})
            elif self.path == "/api/stop":
                app.stop_robot()
                self._json({"ok": True})
            elif self.path == "/api/model":
                provider = str(payload.get("provider", "")).strip()
                model = str(payload.get("model", "")).strip()
                try:
                    ok = app.set_model(provider, model)
                except ValueError as exc:
                    self._json({"ok": False, "error": str(exc)}, 400)
                    return
                if not ok:
                    self._json({"ok": False, "error": "agent is busy"}, 409)
                    return
                self._json({"ok": True, "provider": provider, "model": model})
            elif self.path == "/api/joints":
                raw_joints = payload.get("joints", payload)
                try:
                    snapshot = app.update_joints(raw_joints)
                except (TypeError, ValueError) as exc:
                    self._json({"ok": False, "error": str(exc)}, 400)
                    return
                self._json({"ok": True, "joints": snapshot})
            else:
                self._send(404, b"not found", "text/plain")

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
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", default=None)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    parser.add_argument("--camera", default="table", help="primary table camera name")
    parser.add_argument("--dry-run", action="store_true", default=None)
    parser.add_argument("--provider", default=None)
    parser.add_argument("--model", default=None)
    args = parser.parse_args(argv)

    load_env_files()
    app = DashboardApp(
        Config.load(args.config_dir),
        host=args.host,
        port=args.port,
        table_camera=args.camera,
        dry_run=args.dry_run,
        provider=args.provider,
        model=args.model,
    )
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        app.close()


if __name__ == "__main__":
    main()
