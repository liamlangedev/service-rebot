"""GPU inference server for LeRobot policies (XVLA, SmolVLA, ACT, ...). Runs as a Hugging Face Space (Docker SDK).

The robot computer (rollout_policy.py --remote-url ... [--policy <repo>]) sends one observation per action chunk:
joint state (deg), the camera frames as JPEG, the task text and which policy to use. The server returns the whole chunk
of unnormalized joint targets (deg), which the robot then plays at 30 Hz through its 200 Hz MIT loop.

Several policies are loaded at startup and stay on the GPU; requests pick one by repo id (the first is the default).
Only the listed repos can be used.

Env vars: POLICIES (comma-separated repo ids or local folders; repo@revision or repo:subfolder allowed; default
niru-5/xvla_rebot_merged_V2,RoboCrafty/smolvla_rebot_merged_V2), POLICY_DTYPE (auto | bfloat16 | float32),
POLICY_DENOISING_STEPS, HF_TOKEN (only for private policy repos). Run locally: uvicorn app:app --port 7860
"""
import base64
import os
import threading
import time
import traceback

import cv2
import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from lerobot.configs.policies import PreTrainedConfig
from lerobot.policies.factory import get_policy_class, make_pre_post_processors
from lerobot.policies.utils import build_inference_frame, make_robot_action
from lerobot.utils.feature_utils import hw_to_dataset_features

from policy_cameras import robot_camera_sizes

DEFAULT_POLICIES = "niru-5/xvla_rebot_merged_V2,RoboCrafty/smolvla_rebot_merged_V2"
POLICY_SPECS = [s.strip() for s in os.environ.get("POLICIES", DEFAULT_POLICIES).split(",") if s.strip()]
ROBOT_TYPE = "rebot_b601_follower"
ACTION_NAMES = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_yaw", "wrist_roll", "gripper"]
DEVICE = os.environ.get("POLICY_DEVICE") or ("cuda" if torch.cuda.is_available() else "cpu")


def _parse_spec(spec: str):
    """'repo', 'repo@revision', 'repo:subfolder' -> (name, repo, revision, subfolder). name is what clients send."""
    repo, rev, sub = spec, None, None
    if not os.path.isdir(spec):
        if ":" in repo:
            repo, sub = repo.split(":", 1)
        if "@" in repo:
            repo, rev = repo.split("@", 1)
    return spec, repo, rev, sub


class Loaded:
    def __init__(self, spec: str):
        self.name, repo, rev, sub = _parse_spec(spec)
        path = repo
        if not os.path.isdir(repo):
            from huggingface_hub import snapshot_download
            path = snapshot_download(repo, revision=rev)
        if sub:
            path = os.path.join(path, sub)
        cfg = PreTrainedConfig.from_pretrained(path)
        cfg.pretrained_path, cfg.device = path, DEVICE
        if hasattr(cfg, "dtype"):
            # Checkpoints trained in bf16 (XVLA) fail in cuDNN on GPUs without native bf16 (T4: "unable to find an
            # engine"); use fp32 there.
            want = os.environ.get("POLICY_DTYPE", "auto")
            if want == "auto":
                native_bf16 = DEVICE == "cuda" and torch.cuda.get_device_capability()[0] >= 8
                want = "bfloat16" if native_bf16 or DEVICE == "cpu" else "float32"
            cfg.dtype = getattr(torch, want)
        for attr in ("num_denoising_steps", "num_inference_steps", "num_steps"):  # XVLA, pi0, SmolVLA
            if os.environ.get("POLICY_DENOISING_STEPS") and hasattr(cfg, attr):
                setattr(cfg, attr, int(os.environ["POLICY_DENOISING_STEPS"]))
        with torch.device(DEVICE):  # build on the target device instead of random-initialising on the CPU first
            pol = get_policy_class(cfg.type).from_pretrained(path, config=cfg)
        self.policy = pol.to(DEVICE).eval()
        self.pre, self.post = make_pre_post_processors(
            policy_cfg=cfg, pretrained_path=path, preprocessor_overrides={"device_processor": {"device": DEVICE}})
        self.cfg = cfg
        # Robot camera names and sizes (undoing the checkpoint's camera renaming); the preprocessor renames them.
        self.image_sizes = robot_camera_sizes(cfg, path)
        act = {f"{n}.pos": float for n in ACTION_NAMES}
        obs = {**act, **{n: (h, w, 3) for n, (h, w) in self.image_sizes.items()}}
        self.ds_features = {**hw_to_dataset_features(act, "action"), **hw_to_dataset_features(obs, "observation")}

    def info(self):
        return {"policy": self.name, "type": self.cfg.type, "device": DEVICE,
                "gpu": torch.cuda.get_device_name() if DEVICE == "cuda" else None,
                "dtype": str(getattr(self.cfg, "dtype", None)),
                "chunk_size": self.cfg.chunk_size, "n_action_steps": self.cfg.n_action_steps,
                "image_sizes": {n: [h, w] for n, (h, w) in self.image_sizes.items()}, "action_names": ACTION_NAMES}


POLICIES: dict[str, Loaded] = {}
ERRORS: dict[str, str] = {}
for _spec in POLICY_SPECS:
    try:
        t = time.time()
        POLICIES[_spec] = Loaded(_spec)
        print(f"loaded {_spec} ({POLICIES[_spec].cfg.type}) on {DEVICE} in {time.time() - t:.0f} s; "
              f"cameras {POLICIES[_spec].image_sizes}", flush=True)
    except Exception as e:  # keep serving the others
        ERRORS[_spec] = repr(e)
        traceback.print_exc()
if not POLICIES:
    raise SystemExit(f"no policy could be loaded: {ERRORS}")
DEFAULT = next(s for s in POLICY_SPECS if s in POLICIES)
LOCK = threading.Lock()  # one GPU, one request at a time

app = FastAPI()


def _get(name: str | None) -> Loaded:
    name = name or DEFAULT
    if name in POLICIES:
        return POLICIES[name]
    if name in ERRORS:
        raise HTTPException(503, f"policy {name} failed to load on the server: {ERRORS[name]}")
    raise HTTPException(404, f"policy {name} is not served here. Available: {list(POLICIES)} "
                             f"(add it to the POLICIES Space variable)")


class Obs(BaseModel):
    state: dict[str, float]  # "<joint>.pos" -> deg, 6 joints + gripper
    images: dict[str, str]   # robot camera name -> base64 JPEG (BGR-encoded), ideally already at the policy's size
    task: str = ""
    n_action_steps: int | None = None
    policy: str | None = None  # repo id from /policies; None = the default


@app.get("/policies")
def policies():
    return {"default": DEFAULT, "available": list(POLICIES), "failed": ERRORS}


@app.get("/info")
def info(policy: str | None = None):
    return _get(policy).info()


@app.get("/")
def root():
    return {"ok": True, **policies()}


def _decode(b64: str) -> np.ndarray:
    img = cv2.imdecode(np.frombuffer(base64.b64decode(b64), np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(400, "bad JPEG")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


@app.post("/act")
def act(o: Obs):
    t0 = time.perf_counter()
    p = _get(o.policy)
    obs = dict(o.state)
    for name, (h, w) in p.image_sizes.items():
        if name not in o.images:
            raise HTTPException(400, f"missing camera {name}")
        img = _decode(o.images[name])
        if img.shape[:2] != (h, w):
            img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
        obs[name] = img
    n = max(1, min(o.n_action_steps or p.cfg.n_action_steps, p.cfg.chunk_size))
    with LOCK, torch.inference_mode():
        p.policy.reset()
        p.policy.config.n_action_steps = n
        frame = p.pre(build_inference_frame(obs, torch.device(DEVICE), p.ds_features, o.task, ROBOT_TYPE))
        chunk = []
        for _ in range(n):  # the first call computes the chunk, the rest pop the policy's queue
            a = make_robot_action(p.post(p.policy.select_action(frame)), p.ds_features)
            chunk.append([a[f"{k}.pos"] for k in ACTION_NAMES])
    return {"policy": p.name, "actions": chunk, "names": ACTION_NAMES,
            "infer_ms": round(1000 * (time.perf_counter() - t0), 1)}
