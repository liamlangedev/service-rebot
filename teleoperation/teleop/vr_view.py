"""Shows the live MuJoCo scene inside the Quest (WebXR) and reads its controllers.

One small server (HTTP page + WebSocket on the same port) runs on the PC:

  PC                                     Quest browser (WebXR page)
  VRBridge.publish(data) ── poses ──►    three.js draws the robot + scene
  BridgeSource.read()    ◄── xr_frame ── controller poses / buttons

Over USB, `adb reverse` maps the port so the headset opens
http://localhost:<port>/ ; localhost counts as a secure context, so WebXR
works without TLS certificates.

Wire format (WebSocket):
  text   {"type": "scene", ...}       once per connection: geoms, meshes, colours
  binary tag 1 + vertex/face buffers  once per connection: all mesh data
  binary tag 2 + n x (pos3, mat9)     every frame: world pose of every drawn geom
  text   {"type": "status", ...}      a few times a second: HUD text
  page -> PC: {"type": "xr_frame", "controllers": {"right": {...}, "left": {...}}}
              (same format as vr-teleop-kit, parsed by WebXRSource)
"""
import http
import json
import subprocess
import threading
import time
from pathlib import Path

import mujoco
import numpy as np

from teleop.quest_input import HANDS, WebXRSource, _QuestSource

PAGE = Path(__file__).resolve().parent / "web" / "vr_view.html"
TAG_MESH, TAG_FRAME = 1, 2


def _drawn_geoms(model: mujoco.MjModel) -> list[int]:
    """Geoms to draw: all primitives, and only the visual (non-colliding) meshes.

    Seeed's MJCF has a coloured visual mesh plus a collision mesh for most
    links; drawing both would double the triangle count. Plane geoms are drawn
    as the floor, group 3+ (hidden in the MuJoCo viewer) is skipped.
    """
    out = []
    for g in range(model.ngeom):
        if model.geom_group[g] >= 3:
            continue
        collides = model.geom_contype[g] != 0 or model.geom_conaffinity[g] != 0
        if model.geom_type[g] == mujoco.mjtGeom.mjGEOM_MESH and collides:
            continue
        out.append(g)
    return out


class VRBridge:
    def __init__(self, model: mujoco.MjModel, port: int = 8765, extra_sites=()):
        self.model = model
        self.port = port
        self.geoms = _drawn_geoms(model)
        self.sites = [model.site(s).id for s in extra_sites]
        self._scene_json, self._mesh_blob = self._build_scene()
        self._clients = set()
        self._clients_lock = threading.Lock()
        self.sources: list["BridgeSource"] = []
        self._server = None
        self.n_frames_in = 0

    # ---- scene export --------------------------------------------------------
    def _build_scene(self):
        m = self.model
        meshes, mesh_index, verts, faces = [], {}, [], []
        geoms = []
        for g in self.geoms:
            mat = int(m.geom_matid[g])
            rgba = (m.mat_rgba[mat] if mat >= 0 else m.geom_rgba[g]).tolist()
            entry = dict(type=int(m.geom_type[g]), size=m.geom_size[g].tolist(),
                         rgba=[round(c, 3) for c in rgba], mesh=-1,
                         name=m.geom(g).name or m.body(m.geom_bodyid[g]).name)
            if m.geom_type[g] == mujoco.mjtGeom.mjGEOM_MESH:
                mid = int(m.geom_dataid[g])
                if mid not in mesh_index:
                    va, nv = int(m.mesh_vertadr[mid]), int(m.mesh_vertnum[mid])
                    fa, nf = int(m.mesh_faceadr[mid]), int(m.mesh_facenum[mid])
                    mesh_index[mid] = len(meshes)
                    meshes.append(dict(nv=nv, nf=nf))
                    verts.append(m.mesh_vert[va:va + nv].astype(np.float32))
                    faces.append(m.mesh_face[fa:fa + nf].astype(np.uint32))
                entry["mesh"] = mesh_index[mid]
            geoms.append(entry)
        for s in self.sites:  # e.g. the grasp point, drawn as a small sphere
            geoms.append(dict(type=int(mujoco.mjtGeom.mjGEOM_SPHERE),
                              size=[float(m.site_size[s][0]), 0, 0],
                              rgba=m.site_rgba[s].tolist(), mesh=-1, name=m.site(s).name))
        scene = dict(type="scene", geoms=geoms, meshes=meshes)
        v = np.concatenate(verts) if verts else np.zeros((0, 3), np.float32)
        f = np.concatenate(faces) if faces else np.zeros((0, 3), np.uint32)
        blob = np.array([TAG_MESH], np.uint32).tobytes() + v.tobytes() + f.tobytes()
        return json.dumps(scene), blob

    # ---- server ----------------------------------------------------------------
    def start(self):
        from websockets.sync.server import serve

        page = PAGE.read_text()

        def process_request(connection, request):
            path = request.path.split("?")[0]
            if path == "/ws":
                return None  # continue with the WebSocket handshake
            if path in ("/", "/index.html"):
                resp = connection.respond(http.HTTPStatus.OK, page)
                del resp.headers["Content-Type"]
                resp.headers["Content-Type"] = "text/html; charset=utf-8"
                resp.headers["Cache-Control"] = "no-store"
                return resp
            return connection.respond(http.HTTPStatus.NOT_FOUND, "not found\n")

        self._server = serve(self._handle, "0.0.0.0", self.port,
                             process_request=process_request, max_size=2 ** 20,
                             compression=None)
        threading.Thread(target=self._server.serve_forever, daemon=True).start()
        print(f"[vr] serving the VR view on http://localhost:{self.port}/ "
              f"({len(self.geoms)} geoms, {len(self._mesh_blob) / 1e6:.1f} MB of meshes)")

    def _handle(self, ws):
        peer = ws.remote_address
        print(f"[vr] headset page connected ({peer[0]}), sending the scene...")
        ws.send(self._scene_json)
        ws.send(self._mesh_blob)
        with self._clients_lock:
            self._clients.add(ws)
        try:
            for raw in ws:
                if isinstance(raw, bytes):
                    continue
                msg = json.loads(raw)
                if msg.get("type") == "xr_frame":
                    self.n_frames_in += 1
                    ctrls = msg.get("controllers") or {}
                    now = time.time()
                    for src in self.sources:
                        ctrl = ctrls.get(HANDS[src.hand])
                        if ctrl is not None:
                            with src._lock:
                                src._latest = (ctrl, now)
                elif msg.get("type") == "log":
                    print(f"[vr page] {msg.get('text')}")
        except Exception:
            pass
        finally:
            with self._clients_lock:
                self._clients.discard(ws)
            print("[vr] headset page disconnected")

    def _broadcast(self, payload):
        with self._clients_lock:
            clients = list(self._clients)
        for ws in clients:
            try:
                ws.send(payload)
            except Exception:
                with self._clients_lock:
                    self._clients.discard(ws)

    @property
    def connected(self) -> bool:
        with self._clients_lock:
            return bool(self._clients)

    def publish(self, data: mujoco.MjData):
        """Sends the world pose of every drawn geom (call at ~30-60 Hz)."""
        if not self.connected:
            return
        pos = np.concatenate([data.geom_xpos[self.geoms], data.site_xpos[self.sites]])
        mat = np.concatenate([data.geom_xmat[self.geoms], data.site_xmat[self.sites]])
        frame = np.hstack([pos, mat]).astype(np.float32)
        self._broadcast(np.array([TAG_FRAME], np.uint32).tobytes() + frame.tobytes())

    def status(self, text: str, following: bool):
        if self.connected:
            self._broadcast(json.dumps(dict(type="status", text=text, following=following)))

    def source(self, hand: str = "r", robot_from_quest=None) -> "BridgeSource":
        src = BridgeSource(hand, robot_from_quest)
        self.sources.append(src)
        return src

    def close(self):
        if self._server is not None:
            self._server.shutdown()


class BridgeSource(WebXRSource):
    """WebXRSource fed by VRBridge instead of a vr-teleop-kit relay."""

    def __init__(self, hand: str = "r", robot_from_quest=None):
        _QuestSource.__init__(self, hand, robot_from_quest)  # no relay connection
        self._latest = None
        self._lock = threading.Lock()
        self._running = True

    def close(self):
        self._running = False


def adb(*args, check=False) -> subprocess.CompletedProcess:
    return subprocess.run(["adb", *args], capture_output=True, text=True, timeout=15, check=check)


def open_on_headset(port: int, query: str = "") -> bool:
    """adb reverse the port and open the page in the Quest browser."""
    try:
        devices = adb("devices").stdout.split("\n")[1:]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("[vr] adb not available; open the page on the headset yourself")
        return False
    if not any(line.strip().endswith("device") for line in devices):
        print("[vr] no authorized Quest on adb (`adb devices`); plug it in over USB")
        return False
    r = adb("reverse", f"tcp:{port}", f"tcp:{port}")
    if r.returncode != 0:
        print(f"[vr] adb reverse failed: {r.stderr.strip()}")
        return False
    url = f"http://localhost:{port}/" + (f"?{query}" if query else "")
    adb("shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url,
        "com.oculus.browser")
    print(f"[vr] opened {url} in the Quest browser (port forwarded over USB)")
    return True
