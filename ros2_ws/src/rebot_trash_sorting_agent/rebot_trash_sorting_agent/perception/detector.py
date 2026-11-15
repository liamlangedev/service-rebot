"""Local open-vocabulary detection with YOLOE.

Runs in-process; no cloud vision, no depth. The vocabulary is a list of words in
``agent.yaml``: an object that no word matches simply does not exist for the agent,
so tune it with ``scripts/detect_once.py`` before blaming the planner.

Weights are not committed. ``scripts/fetch_models.sh`` copies or downloads them and
``agent.yaml`` points at ``${models}/yoloe-26l-seg.pt``.
"""

from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
import re
from typing import Any, Iterable, Sequence

import numpy as np

from ..types import Detection
from .scene import combine

#: Prompt expansion. YOLOE compares text embeddings, so "can" and "red can" are
#: genuinely different detectors. The task sentence supplies the nouns; these
#: attributes make a bare noun ("can") survive contact with colour and shape.
_COLOURS = ("red", "orange", "yellow", "green", "blue", "black", "white", "silver")
_STOPWORDS = {
    "a", "an", "the", "this", "that", "these", "those", "it", "them", "its",
    "please", "now", "then", "and", "or", "but", "to", "into", "in", "on", "at",
    "from", "with", "for", "of", "by", "up", "down", "over", "under", "left",
    "right", "front", "back", "near", "far", "table", "robot", "arm", "gripper",
    "bin", "bins", "compartment", "compartments", "trash", "waste", "recycling",
    "put", "place", "pick", "move", "drop", "take", "grab", "sort", "throw",
    "bring", "get", "remove", "clean", "clear", "release", "hold", "lift", "send",
    "there", "here", "one", "two", "first", "second", "all",
}
_MAX_PROMPTS = 32


def vocabulary_from_task(task: str, base: Iterable[str] = ()) -> list[str]:
    """Prompt vocabulary for one task sentence plus the configured defaults.

    A task like "put the red can in the bin" contributes ``can`` and ``red can``;
    ``bin`` is a place, not a pickable object, so it is not prompted. Colour
    variants are added for every noun because a bare noun often scores poorly on a
    small open-vocabulary model. Nothing here describes size or class geometry: the
    width and orientation are measured from the mask at runtime.
    """
    text = (task or "").lower()
    words = re.findall(r"[a-z][a-z0-9_-]+", text)
    phrases = [
        f"{colour} {noun}"
        for colour, noun in re.findall(
            r"\b(" + "|".join(_COLOURS) + r")\s+([a-z][a-z0-9_-]+)", text
        )
        if noun not in _STOPWORDS
    ]
    nouns: list[str] = []
    for word in words:
        if len(word) < 3 or word in _STOPWORDS or word in _COLOURS:
            continue
        nouns.append(word)
        if word.endswith("s") and len(word) > 4:
            nouns.append(word[:-1])

    vocabulary: list[str] = []
    for prompt in (*base, *phrases, *nouns):
        prompt = " ".join(str(prompt).strip().lower().split())
        if prompt and prompt not in vocabulary:
            vocabulary.append(prompt)
    for noun in nouns:
        for colour in _COLOURS:
            prompt = f"{colour} {noun}"
            if prompt not in vocabulary:
                vocabulary.append(prompt)
    return vocabulary[:_MAX_PROMPTS]


class YoloeDetector:
    """Thin wrapper that turns ultralytics results into :class:`Detection`."""

    def __init__(self, settings: dict[str, Any]) -> None:
        try:
            from ultralytics import YOLOE  # noqa: F401  (import check)
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "local perception needs ultralytics + torch: run scripts/setup_agent.sh "
                "or pip install ultralytics"
            ) from exc

        model_path = Path(str(settings.get("model", "yoloe-26l-seg.pt"))).expanduser()
        if not model_path.is_file():
            raise FileNotFoundError(
                f"detector weights not found: {model_path}\n"
                "run scripts/fetch_models.sh (or set perception.model in agent.yaml)"
            )
        self.model_path = model_path
        self.classes = [str(c) for c in (settings.get("classes") or ["can", "cup"])]
        self.conf = float(settings.get("conf", 0.15))
        self.device = str(settings.get("device", "cpu"))
        self.text_encoder = settings.get("text_encoder", "mobileclip2_b.ts")
        self._model = None

    # ------------------------------------------------------------------ model
    def set_vocabulary(self, words: Iterable[str]) -> None:
        """Replace the prompts, reloading them if the model is already warm."""
        vocabulary = [str(w).strip().lower() for w in words if str(w).strip()]
        if vocabulary == self.classes:
            return
        self.classes = vocabulary or self.classes
        if self._model is not None:
            self._apply_classes()

    def _apply_classes(self) -> None:
        assert self._model is not None
        if self.classes:
            self._model.set_classes(self.classes, self._model.get_text_pe(self.classes))

    def load(self) -> None:
        """Load the weights and bake in the open-vocabulary class prompts."""
        if self._model is not None:
            return
        os.environ.setdefault("YOLO_OFFLINE", "True")
        from ultralytics import YOLOE

        with _in_directory(self.model_path.parent):
            model = YOLOE(str(self.model_path))
            if self.classes:
                model.set_classes(self.classes, model.get_text_pe(self.classes))
        self._model = model

    def detect(self, bgr: np.ndarray) -> list[Detection]:
        if self._model is None:
            self.load()
        assert self._model is not None
        results = self._model.predict(bgr, conf=self.conf, device=self.device, verbose=False)
        if not results:
            return []
        # One object can fire under two prompts ("cup" and "white cup"); keep the
        # more confident label so the planner does not see a phantom duplicate.
        return combine(detections_from_result(results[0]))


def detections_from_result(result: Any) -> list[Detection]:
    """Convert one ultralytics ``Results`` object into detections."""
    boxes = getattr(result, "boxes", None)
    if boxes is None or len(boxes) == 0:
        return []
    names = getattr(result, "names", {}) or {}
    polygons: Sequence[Any] = ()
    masks = getattr(result, "masks", None)
    if masks is not None and getattr(masks, "xy", None) is not None:
        polygons = masks.xy

    out: list[Detection] = []
    xyxy = boxes.xyxy.cpu().numpy() if hasattr(boxes.xyxy, "cpu") else np.asarray(boxes.xyxy)
    confs = boxes.conf.cpu().numpy() if hasattr(boxes.conf, "cpu") else np.asarray(boxes.conf)
    classes = boxes.cls.cpu().numpy() if hasattr(boxes.cls, "cpu") else np.asarray(boxes.cls)
    for index in range(len(xyxy)):
        label = names.get(int(classes[index]), str(int(classes[index]))) if isinstance(names, dict) else str(names[int(classes[index])])
        polygon: tuple[tuple[float, float], ...] = ()
        if index < len(polygons):
            points = np.asarray(polygons[index], dtype=float)
            if points.size:
                polygon = tuple((float(p[0]), float(p[1])) for p in points)
        out.append(
            Detection(
                label=str(label),
                score=float(confs[index]),
                bbox=tuple(float(v) for v in xyxy[index]),
                polygon=polygon,
            )
        )
    return out


def annotate(bgr: np.ndarray, detections: Iterable[Detection], colour: tuple[int, int, int] = (0, 200, 0)) -> np.ndarray:
    """Draw boxes, labels and contact points (for the dashboard and debugging)."""
    import cv2

    frame = bgr.copy()
    for det in detections:
        x1, y1, x2, y2 = (int(v) for v in det.bbox)
        cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)
        cv2.putText(frame, f"{det.label} {det.score:.2f}", (x1, max(y1 - 6, 12)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 1, cv2.LINE_AA)
        try:
            u, v = det.bottom_mid_px()
            cv2.circle(frame, (int(u), int(v)), 4, (0, 0, 255), -1)
        except Exception:  # noqa: BLE001 - annotation must never break the pipeline
            pass
    return frame


@contextmanager
def _in_directory(path: Path):
    """YOLOE resolves its text encoder relative to the CWD; keep that local."""
    previous = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(previous)
