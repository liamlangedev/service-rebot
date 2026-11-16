"""Client side of rollout/remote/policy_server.py: a drop-in for PolicyRunner whose
inference runs on a remote GPU. Images are resized to the policy's input size and sent as
JPEG; units, anchoring and safety all stay as in a local rollout (the server runs the
same PolicyRunner; the safety filter runs here)."""

from __future__ import annotations

import base64
import json
import time
import urllib.request

import numpy as np


class RemoteRunner:
    def __init__(self, url: str, policy: str, subfolder: str | None, mode: str, task: str,
                 use_cameras: tuple[str, ...] | None, max_offset_deg: float,
                 jpeg_quality: int = 90, timeout_s: float = 120.0):
        from huggingface_hub import get_token

        self.url = url.rstrip("/")
        self.token = get_token()
        self.quality = jpeg_quality
        self.timeout = timeout_s
        print(f"remote policy server {self.url}: loading {policy} {subfolder or ''} "
              "(first load downloads the model on the server)")
        info = self._post("/load", {"policy": policy, "subfolder": subfolder, "mode": mode,
                                    "task": task, "max_offset_deg": max_offset_deg,
                                    "use_cameras": list(use_cameras) if use_cameras else None},
                          timeout=900)
        self.key = info["key"]
        self._sizes = {n: tuple(hw) for n, hw in info["cameras"].items()}
        self.chunk_size = int(info["chunk_size"])
        self.n_steps = self.chunk_size
        self.last_rtt_ms = None
        self.last_infer_ms = None

    @property
    def camera_names(self) -> list[str]:
        return list(self._sizes)

    def _post(self, path: str, obj: dict, timeout: float | None = None) -> dict:
        req = urllib.request.Request(self.url + path, data=json.dumps(obj).encode(),
                                     headers={"Content-Type": "application/json"})
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(req, timeout=timeout or self.timeout) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")[:500]
            raise RuntimeError(f"policy server {path}: HTTP {e.code} {body}") from None

    def start(self, anchor_state: np.ndarray) -> None:
        self._post("/start", {"key": self.key, "anchor": np.asarray(anchor_state).tolist()})

    def predict(self, state: np.ndarray, images: dict[str, np.ndarray],
                n: int | None = None) -> tuple[np.ndarray, bool]:
        import cv2

        from rebot_trash_sorting_agent.grasp_policy.runner import fit_image

        enc = {}
        for name, (h, w) in self._sizes.items():
            rgb = fit_image(images[name], h, w)
            ok, buf = cv2.imencode(".jpg", rgb[:, :, ::-1],
                                   [cv2.IMWRITE_JPEG_QUALITY, self.quality])
            enc[name] = base64.b64encode(buf.tobytes()).decode()
        tic = time.monotonic()
        out = self._post("/predict", {"key": self.key, "state": np.asarray(state).tolist(),
                                      "images": enc, "n": n})
        self.last_rtt_ms = (time.monotonic() - tic) * 1000
        self.last_infer_ms = out.get("infer_ms")
        return np.asarray(out["actions"], np.float32), bool(out["clipped"])
