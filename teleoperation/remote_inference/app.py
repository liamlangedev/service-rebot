"""GPU inference server for LeRobot policies (XVLA, SmolVLA, ACT, ...). Runs as a Hugging Face Space (Docker SDK).

The robot computer (rollout_policy.py --remote-url ...) sends one observation per action chunk:
joint state (deg), the policy's camera frames as JPEG, and the task text. The server returns the whole chunk of
unnormalized joint targets (deg), which the robot then plays at 30 Hz through its 200 Hz MIT loop.

Env vars: POLICY_REPO (default niru-5/xvla_rebot_merged_V2), POLICY_SUBFOLDER, POLICY_REVISION,
POLICY_DTYPE (auto | bfloat16 | float32), POLICY_DENOISING_STEPS, HF_TOKEN (only for private policy repos). Run locally: uvicorn app:app --port 7860
"""
import base64
import os
import threading
import time

import cv2
import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from lerobot.configs.policies import PreTrainedConfig
from lerobot.policies.factory import get_policy_class, make_pre_post_processors
from lerobot.policies.utils import build_inference_frame, make_robot_action
from lerobot.utils.feature_utils import hw_to_dataset_features

REPO = os.environ.get("POLICY_REPO", "niru-5/xvla_rebot_merged_V2")
SUBFOLDER = os.environ.get("POLICY_SUBFOLDER") or None
REVISION = os.environ.get("POLICY_REVISION") or None
ROBOT_TYPE = "rebot_b601_follower"
ACTION_NAMES = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_yaw", "wrist_roll", "gripper"]
DEVICE = os.environ.get("POLICY_DEVICE") or ("cuda" if torch.cuda.is_available() else "cpu")


def load():
    path = REPO
    if not os.path.isdir(REPO):
        from huggingface_hub import snapshot_download
        path = snapshot_download(REPO, revision=REVISION)
    if SUBFOLDER:
        path = os.path.join(path, SUBFOLDER)
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
    for attr in ("num_denoising_steps", "num_inference_steps"):
        if os.environ.get("POLICY_DENOISING_STEPS") and hasattr(cfg, attr):
            setattr(cfg, attr, int(os.environ["POLICY_DENOISING_STEPS"]))
    with torch.device(DEVICE):  # build on the target device instead of random-initialising on the CPU first
        pol = get_policy_class(cfg.type).from_pretrained(path, config=cfg)
    pol = pol.to(DEVICE).eval()
    pre_, post_ = make_pre_post_processors(policy_cfg=cfg, pretrained_path=path,
                                           preprocessor_overrides={"device_processor": {"device": DEVICE}})
    return pol, pre_, post_, cfg


policy, pre, post, cfg = load()
IMAGE_SIZES = {k.removeprefix("observation.images."): tuple(int(x) for x in v.shape[1:])
               for k, v in cfg.input_features.items() if k.startswith("observation.images.")}
_act_feats = {f"{n}.pos": float for n in ACTION_NAMES}
_obs_feats = {**_act_feats, **{n: (h, w, 3) for n, (h, w) in IMAGE_SIZES.items()}}
DS_FEATURES = {**hw_to_dataset_features(_act_feats, "action"), **hw_to_dataset_features(_obs_feats, "observation")}
LOCK = threading.Lock()  # one GPU, one request at a time
print(f"loaded {cfg.type} from {REPO} on {DEVICE}; cameras {IMAGE_SIZES}", flush=True)

app = FastAPI()


class Obs(BaseModel):
    state: dict[str, float]  # "<joint>.pos" -> deg, 6 joints + gripper
    images: dict[str, str]   # camera name -> base64 JPEG (BGR-encoded), ideally already at the policy's size
    task: str = ""
    n_action_steps: int | None = None


@app.get("/info")
def info():
    return {"policy": REPO, "subfolder": SUBFOLDER, "type": cfg.type, "device": DEVICE,
            "gpu": torch.cuda.get_device_name() if DEVICE == "cuda" else None,
            "dtype": str(getattr(cfg, "dtype", None)),
            "chunk_size": cfg.chunk_size, "n_action_steps": cfg.n_action_steps,
            "image_sizes": {n: [h, w] for n, (h, w) in IMAGE_SIZES.items()}, "action_names": ACTION_NAMES}


@app.get("/")
def root():
    return {"ok": True, **info()}


def _decode(b64: str) -> np.ndarray:
    img = cv2.imdecode(np.frombuffer(base64.b64decode(b64), np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(400, "bad JPEG")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


@app.post("/act")
def act(o: Obs):
    t0 = time.perf_counter()
    obs = dict(o.state)
    for name, (h, w) in IMAGE_SIZES.items():
        if name not in o.images:
            raise HTTPException(400, f"missing camera {name}")
        img = _decode(o.images[name])
        if img.shape[:2] != (h, w):
            img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
        obs[name] = img
    n = max(1, min(o.n_action_steps or cfg.n_action_steps, cfg.chunk_size))
    with LOCK, torch.inference_mode():
        policy.reset()
        policy.config.n_action_steps = n
        frame = pre(build_inference_frame(obs, torch.device(DEVICE), DS_FEATURES, o.task, ROBOT_TYPE))
        chunk = []
        for _ in range(n):  # the first call computes the chunk, the rest pop the policy's queue
            a = make_robot_action(post(policy.select_action(frame)), DS_FEATURES)
            chunk.append([a[f"{k}.pos"] for k in ACTION_NAMES])
    return {"actions": chunk, "names": ACTION_NAMES, "infer_ms": round(1000 * (time.perf_counter() - t0), 1)}
