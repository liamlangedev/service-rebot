"""Client for the GPU inference server in remote_inference/ (e.g. a Hugging Face Space).

Mirrors the local `policy.select_action` path: when the action queue is empty it sends the current observation
(joint state + camera frames as JPEG + task) and receives a whole chunk of joint targets (deg), then hands them
out one per policy step.
"""
import base64
import os
from collections import deque

import cv2
import numpy as np
import requests

JOINTS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_yaw", "wrist_roll", "gripper"]


def _hf_token():
    tok = os.environ.get("HF_TOKEN")
    if tok:
        return tok
    try:
        from huggingface_hub import get_token
        return get_token()
    except Exception:
        return None


def _raise(r):
    """raise_for_status, with the server's error message (e.g. which policies are available)."""
    if r.status_code >= 400:
        try:
            detail = r.json().get("detail")
        except Exception:
            detail = r.text[:300]
        raise SystemExit(f"remote policy server: HTTP {r.status_code} on {r.url}: {detail}")


class RemotePolicy:
    def __init__(self, url: str, policy: str | None = None, n_action_steps: int | None = None,
                 jpeg_quality: int = 90, timeout: float = 30.0):
        """policy: repo id served by the server (GET /policies); None = the server's default."""
        self.url = url.rstrip("/")
        self.session = requests.Session()
        tok = _hf_token()
        if tok:  # private Spaces accept the HF token as a bearer token
            self.session.headers["Authorization"] = f"Bearer {tok}"
        self.timeout, self.jpeg_quality = timeout, jpeg_quality
        r = self.session.get(f"{self.url}/info", params={"policy": policy} if policy else None,
                             timeout=max(timeout, 60.0))
        _raise(r)
        self.info = r.json()
        self.policy = self.info["policy"]
        self.image_sizes = {n: (int(h), int(w)) for n, (h, w) in self.info["image_sizes"].items()}
        self.chunk_size = int(self.info["chunk_size"])
        if n_action_steps and n_action_steps > self.chunk_size:
            raise SystemExit(f"--n-action-steps {n_action_steps} exceeds the model's chunk size {self.chunk_size}")
        self.n_action_steps = n_action_steps or int(self.info["n_action_steps"])
        self.queue: deque = deque()
        self.last_ms = {"rtt": 0.0, "infer": 0.0}

    def reset(self):
        self.queue.clear()

    def _encode(self, img_rgb: np.ndarray) -> str:
        ok, buf = cv2.imencode(".jpg", cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR),
                               [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality])
        if not ok:
            raise RuntimeError("JPEG encode failed")
        return base64.b64encode(buf.tobytes()).decode()

    def request_chunk(self, obs: dict, task: str) -> list[dict]:
        import time
        payload = {"state": {f"{j}.pos": float(obs[f"{j}.pos"]) for j in JOINTS},
                   "images": {n: self._encode(obs[n]) for n in self.image_sizes},
                   "task": task, "n_action_steps": self.n_action_steps, "policy": self.policy}
        t0 = time.perf_counter()
        r = self.session.post(f"{self.url}/act", json=payload, timeout=self.timeout)
        _raise(r)
        out = r.json()
        self.last_ms = {"rtt": 1000 * (time.perf_counter() - t0), "infer": float(out.get("infer_ms", 0.0))}
        names = out["names"]
        return [{f"{n}.pos": float(v) for n, v in zip(names, row)} for row in out["actions"]]

    def select_action(self, obs: dict, task: str) -> dict:
        """obs: robot observation with images already at the policy's size. Returns {"<joint>.pos": deg}."""
        if not self.queue:
            self.queue.extend(self.request_chunk(obs, task))
        return self.queue.popleft()
