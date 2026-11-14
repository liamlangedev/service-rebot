"""2D detectors: image + optional object names -> list of Detection (pixels).

Backends (pick with --detector):
  color   HSV colour blobs. Offline, fast, gives a mask angle for grasp yaw. Best for a
          controlled demo with coloured objects; also what the tests use.
  claude  Claude vision, open vocabulary ("the crushed can"). One API call per image.
  gemini  Gemini Robotics-ER pointing (google-genai). Open vocabulary, trained for
          pointing. Needs GEMINI_API_KEY; not exercised by the tests.
  oracle  Simulation only: projects ground-truth object poses (debugs motion vs vision).
"""
from __future__ import annotations

import base64
import json
import os
import re
from dataclasses import dataclass

import numpy as np

CLAUDE_MODEL = os.environ.get("AUTONOMY_CLAUDE_MODEL", "claude-opus-5-5")


@dataclass
class Detection:
    label: str
    uv: tuple[float, float]                         # centre pixel
    camera: str = ""
    bbox: tuple[float, float, float, float] | None = None   # x0, y0, x1, y1
    score: float = 1.0
    angle: float | None = None                      # image angle of the long axis [rad]
    size_px: tuple[float, float] | None = None      # long, short side [px]


_STOP = {"the", "a", "an", "of", "any", "object", "objects", "item", "items", "thing", "things"}


def _singular(w: str) -> str:
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 4 and w.endswith("es") and w[:-2].endswith(("s", "x", "ch", "sh")):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def _words(s: str) -> set[str]:
    return {_singular(w) for w in re.findall(r"[a-z0-9]+", s.lower())} - _STOP


def label_matches(query: str, label: str) -> float:
    """0..1 similarity between a requested name and a detected label (word overlap)."""
    q, l = _words(query), _words(label)
    if not q:
        return 0.5          # "any object"
    if not l:
        return 0.0
    return len(q & l) / len(q)


class Detector:
    name = "base"

    def detect(self, image: np.ndarray, queries: list[str] | None = None,
               camera: str = "") -> list[Detection]:
        raise NotImplementedError


# ---------------------------------------------------------------------------------
# Colour blobs
# ---------------------------------------------------------------------------------
# OpenCV hue is 0..180. Ranges are deliberately wide; saturation/value floors reject
# the grey table, the checkered floor and the faint zone markings.
COLOR_RANGES = {
    "red": [((0, 140, 90), (8, 255, 255)), ((170, 140, 90), (180, 255, 255))],
    "orange": [((9, 150, 120), (18, 255, 255))],
    "yellow": [((19, 120, 120), (35, 255, 255))],
    "green": [((40, 150, 70), (80, 255, 255))],
    "blue": [((85, 150, 120), (128, 255, 255))],
    "purple": [((129, 90, 70), (165, 255, 255))],
}


class ColorDetector(Detector):
    name = "color"

    def __init__(self, min_area: int = 120, colors: dict | None = None):
        import cv2
        self.cv2 = cv2
        self.min_area = min_area
        self.colors = colors or COLOR_RANGES

    def detect(self, image, queries=None, camera=""):
        cv2 = self.cv2
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        wanted = list(self.colors)
        if queries:
            asked = {c for q in queries for c in self.colors if c in _words(q)}
            wanted = [c for c in wanted if c in asked] or wanted
        out = []
        for color in wanted:
            mask = np.zeros(hsv.shape[:2], np.uint8)
            for lo, hi in self.colors[color]:
                mask |= cv2.inRange(hsv, np.array(lo), np.array(hi))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
            n, lab, stats, cents = cv2.connectedComponentsWithStats(mask)
            for i in range(1, n):
                if stats[i, cv2.CC_STAT_AREA] < self.min_area:
                    continue
                ys, xs = np.where(lab == i)
                pts = np.column_stack([xs, ys]).astype(np.float32)
                (cx, cy), (w, h), ang = cv2.minAreaRect(pts)
                long_ang = np.radians(ang) if w >= h else np.radians(ang + 90)
                x, y, bw, bh = stats[i, :4]
                out.append(Detection(
                    label=f"{color} object", uv=(float(cents[i][0]), float(cents[i][1])),
                    camera=camera, bbox=(x, y, x + bw, y + bh),
                    score=float(min(1.0, stats[i, cv2.CC_STAT_AREA] / 2000)),
                    angle=float(long_ang), size_px=(max(w, h), min(w, h))))
        return out


# ---------------------------------------------------------------------------------
# Simulation ground truth
# ---------------------------------------------------------------------------------
class OracleDetector(Detector):
    """Projects the true pose of every free body in the MuJoCo scene (sim only)."""
    name = "oracle"

    def __init__(self, sim, rig):
        import mujoco
        self.mj = mujoco
        self.sim, self.rig = sim, rig
        m = sim.model
        self.bodies = [m.body(m.jnt_bodyid[j]).name for j in range(m.njnt)
                       if m.jnt_type[j] == mujoco.mjtJoint.mjJNT_FREE]

    def detect(self, image, queries=None, camera=""):
        m, d = self.sim.model, self.sim.data
        cam = self.rig.model(camera)
        out = []
        for name in self.bodies:
            b = m.body(name).id
            g = m.body_geomadr[b]
            corners = np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)])
            size = m.geom_size[g].copy()
            if m.geom_type[g] == self.mj.mjtGeom.mjGEOM_CYLINDER:
                size = np.array([size[0], size[0], size[1]])
            pts = d.geom_xpos[g] + (corners * size) @ d.geom_xmat[g].reshape(3, 3).T
            uv = cam.project(pts)
            c = cam.project(d.geom_xpos[g])[0]
            if np.any(np.isnan(uv)) or not (0 <= c[0] < cam.width and 0 <= c[1] < cam.height):
                continue
            R = d.geom_xmat[g].reshape(3, 3)
            axis = R[:, 0] if size[0] >= size[1] else R[:, 1]
            p2 = cam.project(np.array([d.geom_xpos[g], d.geom_xpos[g] + 0.05 * axis]))
            ang = float(np.arctan2(*(p2[1] - p2[0])[::-1]))
            out.append(Detection(label=name.replace("_", " "), uv=(float(c[0]), float(c[1])),
                                 camera=camera, bbox=(*uv.min(0), *uv.max(0)), angle=ang))
        return out


# ---------------------------------------------------------------------------------
# Vision-language models
# ---------------------------------------------------------------------------------
def _jpeg_b64(image: np.ndarray, max_side: int = 1024) -> tuple[str, float]:
    import cv2
    h, w = image.shape[:2]
    s = min(1.0, max_side / max(h, w))
    if s < 1:
        image = cv2.resize(image, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    return base64.standard_b64encode(buf.tobytes()).decode(), s


_POINT_PROMPT = (
    "You are the vision system of a robot arm looking at a table. List the graspable "
    "objects on the table{focus}. For each, give a short identifying label (colour + "
    "type, e.g. 'red can', 'clear plastic bottle'), the centre point and a tight bounding "
    "box. Coordinates are normalised to 0-1000 as [y, x] and [ymin, xmin, ymax, xmax]. "
    "Ignore the robot itself, the table and anything off the table.")

_POINT_SCHEMA = {
    "type": "object",
    "properties": {"objects": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "label": {"type": "string"},
            "point": {"type": "array", "items": {"type": "number"}},
            "box_2d": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["label", "point", "box_2d"], "additionalProperties": False}}},
    "required": ["objects"], "additionalProperties": False,
}


def _to_detections(items, w, h, camera) -> list[Detection]:
    out = []
    for it in items:
        try:
            y, x = it["point"][:2]
            box = it.get("box_2d") or None
            bbox = (box[1] * w / 1000, box[0] * h / 1000, box[3] * w / 1000, box[2] * h / 1000) if box and len(box) == 4 else None
            out.append(Detection(label=str(it["label"]).lower(), uv=(x * w / 1000, y * h / 1000),
                                 camera=camera, bbox=bbox, score=0.9))
        except (KeyError, TypeError, ValueError, IndexError):
            continue
    return out


class ClaudeDetector(Detector):
    name = "claude"

    def __init__(self, model: str = CLAUDE_MODEL, effort: str = "low"):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model, self.effort = model, effort

    def detect(self, image, queries=None, camera=""):
        h, w = image.shape[:2]
        data, _ = _jpeg_b64(image)
        focus = f", in particular: {', '.join(queries)} (use exactly these names as labels)" if queries else ""
        resp = self.client.beta.messages.create(
            model=self.model, max_tokens=4000,
            betas=["server-side-fallback-2026-07-01"], fallbacks="default",
            output_config={"effort": self.effort,
                           "format": {"type": "json_schema", "schema": _POINT_SCHEMA}},
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}},
                {"type": "text", "text": _POINT_PROMPT.format(focus=focus)}]}])
        if resp.stop_reason == "refusal":
            return []
        text = next((b.text for b in resp.content if b.type == "text"), "{}")
        return _to_detections(json.loads(text).get("objects", []), w, h, camera)


class GeminiDetector(Detector):
    """Gemini Robotics-ER pointing (set GEMINI_ER_MODEL to the model id you have access to)."""
    name = "gemini"

    def __init__(self, model: str | None = None):
        from google import genai
        self.genai = genai
        self.client = genai.Client()     # reads GEMINI_API_KEY
        self.model = model or os.environ.get("GEMINI_ER_MODEL", "gemini-robotics-er-1.5-preview")

    def detect(self, image, queries=None, camera=""):
        from google.genai import types
        h, w = image.shape[:2]
        data, _ = _jpeg_b64(image)
        focus = f", in particular: {', '.join(queries)} (use exactly these names as labels)" if queries else ""
        prompt = _POINT_PROMPT.format(focus=focus) + (
            ' Answer only with JSON: [{"label": str, "point": [y, x], "box_2d": [ymin, xmin, ymax, xmax]}, ...]')
        resp = self.client.models.generate_content(
            model=self.model,
            contents=[types.Part.from_bytes(data=base64.b64decode(data), mime_type="image/jpeg"), prompt],
            config=types.GenerateContentConfig(temperature=0.3))
        text = resp.text or "[]"
        m = re.search(r"\[.*\]", text, re.S)
        return _to_detections(json.loads(m.group(0)) if m else [], w, h, camera)


def make_detector(name: str, sim=None, rig=None) -> Detector:
    if name == "color":
        return ColorDetector()
    if name == "oracle":
        if sim is None:
            raise ValueError("the oracle detector only works in simulation")
        return OracleDetector(sim, rig)
    if name == "claude":
        return ClaudeDetector()
    if name == "gemini":
        return GeminiDetector()
    raise ValueError(f"unknown detector {name!r}")
