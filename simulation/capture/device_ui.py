"""Device setup page: which camera is which, which port is the arm, lens calibration.

  cd simulation
  uv run --project ../teleoperation python -m capture.device_ui          # open http://localhost:8770
  uv run --project ../teleoperation python -m capture.device_ui --fake   # sim cameras, no hardware

1. Every USB camera shows a live preview. Pick its role (cam_corner, cam_far, wrist).
   Cover a lens with your hand if you are unsure which preview is which.
2. Pick the arm's serial port, press Save. That writes capture/devices.json.
3. Optional, with the printed ChArUco board (python -m rebot_sim.charuco board.pdf):
   per camera, press "Collect", then move the board slowly in front of that camera
   (tilt it, near/far, all corners of the image) until about 20 views are kept, then
   "Solve". That calibrates the lens (focal length + distortion) into
   rebot_sim/calibration/<role>.json.
"""
from __future__ import annotations

import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import cv2
import numpy as np

from capture.devices import (DEVICES_FILE, ROLES, CameraStream, Device, SimCameraHub,
                             list_cameras, list_serial_ports, load_devices, resolve,
                             save_devices)
from capture.calib import save_intrinsics
from rebot_sim.charuco import BoardSpec, calibrate_intrinsics, detect, draw
from rebot_sim.scene import load_config

MIN_CORNERS = 12        # a view must show at least this many board corners
NEW_VIEW_PX = 60.0      # ...and differ this much (mean corner shift) from kept views
MAX_VIEWS = 40


class CamWorker:
    """Reads one camera, detects the board, keeps lens-calibration views,
    and prepares the preview JPEG."""

    def __init__(self, idx: int, dev: Device, stream, board: BoardSpec):
        self.idx, self.dev, self.stream, self.board = idx, dev, stream, board
        self.preview = None
        self.corners = 0
        self.collecting = False
        self.views = []
        self.result = None
        self.error = None
        self._stop = threading.Event()
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while not self._stop.is_set():
            try:
                frame = self.stream.read()
            except Exception as exc:  # noqa: BLE001
                self.error = str(exc)
                time.sleep(0.5)
                continue
            det = detect(self.board, frame, min_corners=4)
            self.corners = 0 if det is None else len(det)
            if self.collecting and det is not None and len(det) >= MIN_CORNERS:
                if self._is_new(det) and len(self.views) < MAX_VIEWS:
                    self.views.append(det)
                    self.size = (frame.shape[1], frame.shape[0])
            img = draw(frame, det)
            h, w = img.shape[:2]
            small = cv2.resize(img, (640, int(640 * h / w)))
            cv2.putText(small, f"#{self.idx}  {w}x{h}  board corners: {self.corners}",
                        (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
            ok, jpg = cv2.imencode(".jpg", small, [cv2.IMWRITE_JPEG_QUALITY, 75])
            if ok:
                self.preview = jpg.tobytes()
            time.sleep(0.15)

    def _is_new(self, det) -> bool:
        for v in self.views:
            common, a, b = np.intersect1d(v.ids, det.ids, return_indices=True)
            if len(common) >= 4 and np.mean(np.linalg.norm(
                    v.corners[a] - det.corners[b], axis=1)) < NEW_VIEW_PX:
                return False
        return True

    def solve(self, role: str):
        if len(self.views) < 8:
            raise ValueError("need at least 8 views (aim for ~20)")
        K, dist, rms = calibrate_intrinsics(self.board, self.views, self.size)
        path = save_intrinsics(role, K, dist, self.size, rms, len(self.views))
        self.result = {"rms_px": round(rms, 3), "fx": round(float(K[0, 0]), 1),
                       "fy": round(float(K[1, 1]), 1), "file": str(path.name)}
        return self.result

    def close(self):
        self._stop.set()
        self.stream.close()


class App:
    def __init__(self, fake: bool):
        cfg = load_config()
        self.board = BoardSpec.from_config(cfg.get("charuco"))
        # --fake never touches the real device map.
        self.devices_path = DEVICES_FILE.with_name("devices.fake.json") if fake else DEVICES_FILE
        saved = load_devices(self.devices_path) or {"cameras": {}, "arm": None}
        self.roles = {d["key"]: r for r, d in saved["cameras"].items()}
        self.arm = (saved.get("arm") or {}).get("key")
        self.ports = list_serial_ports()
        self.workers: list[CamWorker] = []
        if fake:
            from rebot_sim import RealSetupEnv
            cfg["charuco"] = {**cfg.get("charuco", {}), "enabled": True,
                              "near_left": cfg.get("charuco", {}).get("near_left") or [0.48, 0.175]}
            self.env = RealSetupEnv(cfg, objects=False)
            self.env.hide_markers()
            self.hub = SimCameraHub(self.env, ROLES)
            for i, role in enumerate(ROLES):
                dev = Device(f"sim:{role}", f"sim:{role}", f"simulated {role}")
                self.workers.append(CamWorker(i, dev, self.hub.stream(role), self.board))
            self.ports = self.ports or [Device("fake", "fake", "fake arm (no hardware)")]
        else:
            for i, dev in enumerate(list_cameras()):
                try:
                    stream = CameraStream(resolve({"key": dev.key, "path": dev.path}))
                except RuntimeError as exc:
                    print(f"[ui] {dev.label}: {exc}")
                    continue
                self.workers.append(CamWorker(i, dev, stream, self.board))
        print(f"[ui] {len(self.workers)} camera(s), {len(self.ports)} serial port(s)")

    def state(self):
        return {
            "roles": ROLES,
            "cameras": [{"idx": w.idx, "key": w.dev.key, "label": w.dev.label,
                         "role": self.roles.get(w.dev.key, ""), "corners": w.corners,
                         "collecting": w.collecting, "views": len(w.views),
                         "result": w.result, "error": w.error} for w in self.workers],
            "ports": [{"key": p.key, "label": p.label} for p in self.ports],
            "arm": self.arm, "devices_file": str(self.devices_path),
            "board": f"{self.board.squares_x}x{self.board.squares_y} {self.board.dictionary}, "
                     f"square {self.board.square * 1000:.0f} mm"}

    def save(self, body):
        roles = {k: r for k, r in body.get("roles", {}).items() if r}
        if len(set(roles.values())) != len(roles):
            raise ValueError("each role can only be given to one camera")
        self.roles = roles
        self.arm = body.get("arm") or None
        cams = {r: w.dev for w in self.workers for k, r in roles.items() if w.dev.key == k}
        arm = next((p for p in self.ports if p.key == self.arm), None)
        save_devices(cams, arm, self.devices_path)
        return {"saved": str(self.devices_path), "cameras": sorted(cams), "arm": arm.label if arm else None}

    def intrinsics(self, body):
        w = self.workers[int(body["cam"])]
        action = body["action"]
        if action == "start":
            w.collecting = True
        elif action == "stop":
            w.collecting = False
        elif action == "clear":
            w.views, w.result = [], None
        elif action == "solve":
            role = self.roles.get(w.dev.key)
            if not role:
                raise ValueError("give this camera a role and Save first")
            w.collecting = False
            return w.solve(role)
        return {"ok": True}


PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>reBot capture setup</title>
<style>
body{font-family:system-ui,sans-serif;margin:16px;background:#f6f6f4;color:#222}
h1{font-size:20px} .grid{display:flex;flex-wrap:wrap;gap:14px}
.card{background:#fff;border:1px solid #ddd;border-radius:8px;padding:10px;width:660px}
.card img{width:640px;border-radius:4px;background:#000}
select,button{font-size:14px;padding:4px 8px;margin:2px} .muted{color:#777;font-size:13px}
.ok{color:#17803d} .err{color:#b42318} label{display:block;margin:4px 0}
</style></head><body>
<h1>reBot capture setup</h1>
<p class="muted">Pick each camera's role and the arm's port, then Save.
Cover a lens with your hand to see which preview it is. Board: <span id="board"></span></p>
<div class="grid" id="cams"></div>
<h2 style="font-size:16px">Arm serial port</h2><div id="ports"></div>
<p><button onclick="save()"><b>Save</b></button> <span id="msg"></span></p>
<script>
let S=null, built=false;
async function api(path, body){const r=await fetch(path,{method:'POST',
 headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
 const j=await r.json(); if(!r.ok) throw new Error(j.error||r.statusText); return j;}
function build(){
 document.getElementById('board').textContent=S.board;
 document.getElementById('cams').innerHTML=S.cameras.map(c=>`
 <div class="card"><img src="/preview/${c.idx}.mjpg">
  <div><b>#${c.idx}</b> ${c.label}<div class="muted">${c.key}</div></div>
  <label>Role: <select id="role${c.idx}"><option value="">(not used)</option>
   ${S.roles.map(r=>`<option ${c.role==r?'selected':''}>${r}</option>`).join('')}</select></label>
  <div>Lens calibration: <button onclick="intr(${c.idx},'start')">Collect</button>
   <button onclick="intr(${c.idx},'stop')">Stop</button>
   <button onclick="intr(${c.idx},'clear')">Clear</button>
   <button onclick="intr(${c.idx},'solve')">Solve</button>
   <span id="st${c.idx}" class="muted"></span></div></div>`).join('');
 document.getElementById('ports').innerHTML=S.ports.length?S.ports.map(p=>`<label>
  <input type="radio" name="arm" value="${p.key}" ${S.arm==p.key?'checked':''}> ${p.label}</label>`).join('')
  :'<p class="muted">No serial ports found. Plug in the arm and reload.</p>';
 built=true;}
async function poll(){S=await (await fetch('/api/state')).json(); if(!built) build();
 for(const c of S.cameras){const r=c.result?` <span class="ok">rms ${c.result.rms_px}px, fy ${c.result.fy} -> ${c.result.file}</span>`:'';
  document.getElementById('st'+c.idx).innerHTML=`${c.collecting?'<b>collecting</b>, ':''}${c.views} views kept${r}`+(c.error?` <span class="err">${c.error}</span>`:'');}}
async function save(){const roles={}; for(const c of S.cameras){roles[c.key]=document.getElementById('role'+c.idx).value;}
 const a=document.querySelector('input[name=arm]:checked');
 try{const j=await api('/api/save',{roles, arm:a?a.value:null});
  document.getElementById('msg').innerHTML=`<span class="ok">saved ${j.cameras.join(', ')}; arm: ${j.arm||'none'} -> ${j.saved}</span>`;}
 catch(e){document.getElementById('msg').innerHTML=`<span class="err">${e.message}</span>`;}}
async function intr(i,action){try{const j=await api('/api/intrinsics',{cam:i,action});
 if(action=='solve') alert(`Lens calibrated: rms ${j.rms_px}px, fy ${j.fy}px -> ${j.file}`);}catch(e){alert(e.message);}}
poll(); setInterval(poll,1000);
</script></body></html>"""


def make_handler(app: App):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, obj, code=200):
            data = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/":
                data = PAGE.encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            elif self.path == "/api/state":
                self._json(app.state())
            elif self.path.startswith("/preview/"):
                w = app.workers[int(self.path.split("/")[2].split(".")[0])]
                self.send_response(200)
                self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
                self.end_headers()
                try:
                    while True:
                        if w.preview:
                            self.wfile.write(b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                                             + w.preview + b"\r\n")
                        time.sleep(0.2)
                except (BrokenPipeError, ConnectionResetError):
                    pass
            else:
                self.send_error(404)

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            try:
                if self.path == "/api/save":
                    self._json(app.save(body))
                elif self.path == "/api/intrinsics":
                    self._json(app.intrinsics(body))
                else:
                    self.send_error(404)
            except Exception as exc:  # noqa: BLE001
                self._json({"error": str(exc)}, 400)
    return Handler


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", type=int, default=8770)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--fake", action="store_true", help="simulated cameras, no hardware")
    args = p.parse_args()
    app = App(args.fake)
    server = ThreadingHTTPServer((args.host, args.port), make_handler(app))
    print(f"[ui] open http://localhost:{args.port}  (Ctrl-C to quit)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for w in app.workers:
            w.close()


if __name__ == "__main__":
    main()
