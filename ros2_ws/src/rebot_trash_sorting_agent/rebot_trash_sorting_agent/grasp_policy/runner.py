"""Run a lerobot policy (ACT, SmolVLA) on dataset-unit observations, one chunk at a time.

Works in the policy's own units (lerobot degrees, see ``units``). In ``relative`` mode the
state fed to the policy and the actions it returns are offsets from the handoff anchor
(``relative``); in ``absolute`` mode they pass through unchanged.

Needs lerobot and torch, so it runs under the teleoperation venv's Python.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .relative import from_relative, to_relative


@dataclass
class RunnerConfig:
    policy_path: str                 # Hub repo id or local checkpoint dir (pretrained_model)
    mode: str = "absolute"           # "absolute" | "relative"
    device: str = "cpu"
    n_steps: int = 10                # actions executed per inference (<= chunk size)
    task: str = "grasp the keys and lift them"
    max_offset_deg: float = 45.0     # arm joints may not leave the anchor by more than this
    revision: str | None = None


def fit_image(rgb: np.ndarray, height: int, width: int) -> np.ndarray:
    """Centre-crop to the target aspect ratio, then resize (HWC uint8 RGB)."""
    import cv2

    h, w = rgb.shape[:2]
    target = width / height
    if abs(w / h - target) > 1e-3:
        if w / h > target:  # too wide
            new_w = int(round(h * target))
            x0 = (w - new_w) // 2
            rgb = rgb[:, x0:x0 + new_w]
        else:
            new_h = int(round(w / target))
            y0 = (h - new_h) // 2
            rgb = rgb[y0:y0 + new_h]
    if rgb.shape[:2] != (height, width):
        rgb = cv2.resize(rgb, (width, height), interpolation=cv2.INTER_AREA)
    return np.ascontiguousarray(rgb, dtype=np.uint8)


class PolicyRunner:
    def __init__(self, cfg: RunnerConfig):
        if cfg.mode not in ("absolute", "relative"):
            raise ValueError(f"mode must be absolute or relative, got {cfg.mode!r}")
        import torch
        from lerobot.configs.policies import PreTrainedConfig
        from lerobot.policies.factory import get_policy_class, make_pre_post_processors

        self.cfg = cfg
        self._torch = torch
        pcfg = PreTrainedConfig.from_pretrained(cfg.policy_path, revision=cfg.revision)
        pcfg.device = cfg.device
        self.policy = get_policy_class(pcfg.type).from_pretrained(
            cfg.policy_path, config=pcfg, revision=cfg.revision)
        self.policy.to(cfg.device).eval()
        self.pre, self.post = make_pre_post_processors(
            pcfg, pretrained_path=cfg.policy_path, pretrained_revision=cfg.revision,
            preprocessor_overrides={"device_processor": {"device": cfg.device}})
        #: policy image key -> (H, W)
        self.cameras = {k: (int(f.shape[1]), int(f.shape[2]))
                        for k, f in pcfg.image_features.items()}
        self.chunk_size = int(getattr(pcfg, "chunk_size", getattr(pcfg, "n_action_steps", 1)))
        self.n_steps = max(1, min(cfg.n_steps, self.chunk_size))
        self.anchor: np.ndarray | None = None

    @property
    def camera_names(self) -> list[str]:
        """Short names, e.g. 'gripper' for 'observation.images.gripper'."""
        return [k.rsplit(".", 1)[-1] for k in self.cameras]

    def start(self, anchor_state: np.ndarray) -> None:
        self.anchor = np.asarray(anchor_state, dtype=np.float32).copy()
        self.policy.reset()

    def predict(self, state: np.ndarray, images: dict[str, np.ndarray]) -> tuple[np.ndarray, bool]:
        """Next `n_steps` absolute actions [n, 7] (dataset degrees) and whether any were clipped.

        `images` maps short camera names to RGB HWC uint8 frames of any size.
        """
        if self.anchor is None:
            raise RuntimeError("call start() first")
        from lerobot.policies.utils import prepare_observation_for_inference

        state = np.asarray(state, dtype=np.float32)
        obs_state = to_relative(state, self.anchor) if self.cfg.mode == "relative" else state
        obs = {"observation.state": obs_state}
        for key, (h, w) in self.cameras.items():
            name = key.rsplit(".", 1)[-1]
            if name not in images:
                raise KeyError(f"no image for camera {name!r} (policy needs {self.camera_names})")
            obs[key] = fit_image(images[name], h, w)

        torch = self._torch
        with torch.inference_mode():
            batch = prepare_observation_for_inference(obs, torch.device(self.cfg.device),
                                                      task=self.cfg.task)
            batch = self.pre(batch)
            chunk = self.policy.predict_action_chunk(batch)[:, : self.n_steps]
            chunk = self.post(chunk)
        actions = chunk.squeeze(0).float().cpu().numpy()
        if self.cfg.mode == "relative":
            actions = from_relative(actions, self.anchor)
        return self._limit(actions)

    def _limit(self, actions: np.ndarray) -> tuple[np.ndarray, bool]:
        lo = self.anchor[:6] - self.cfg.max_offset_deg
        hi = self.anchor[:6] + self.cfg.max_offset_deg
        clipped = np.clip(actions[:, :6], lo, hi)
        hit = bool(np.any(clipped != actions[:, :6]))
        actions = actions.copy()
        actions[:, :6] = clipped
        return actions, hit
