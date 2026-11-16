"""Which robot cameras a checkpoint needs, and at what size. Shared by remote_inference/app.py and rollout_policy.py.

A checkpoint's `input_features` are not always what the robot must send:
- the preprocessor may rename cameras (SmolVLA fine-tunes map front_wide -> camera1, ...), and
- a fine-tune can keep the base model's declared shapes (smolvla_base: 256x256, 6-dim state) even though it was
  trained on 640x360 frames and a 7-dim state; the policy resizes / pads internally.
So: robot camera names come from inverting the preprocessor's rename map, and the image size from the training
dataset's meta/info.json (train_config.json -> dataset.repo_id). Fallback: the declared input_features shape.
"""
import json
import os

PREFIX = "observation.images."


def _read_json(path_or_repo: str, filename: str, subfolder: str | None = None):
    """filename from a local checkpoint folder or a Hub repo; None if missing."""
    local = os.path.join(path_or_repo, subfolder or "", filename)
    if os.path.isfile(local):
        with open(local) as f:
            return json.load(f)
    if os.path.isdir(path_or_repo):
        return None
    try:
        from huggingface_hub import hf_hub_download
        with open(hf_hub_download(path_or_repo, filename, subfolder=subfolder)) as f:
            return json.load(f)
    except Exception:
        return None


def rename_map(path_or_repo: str, subfolder: str | None = None) -> dict:
    pre = _read_json(path_or_repo, "policy_preprocessor.json", subfolder) or {}
    for step in pre.get("steps", []):
        if step.get("registry_name") == "rename_observations_processor":
            return dict(step.get("config", {}).get("rename_map") or {})
    return {}


def dataset_image_sizes(path_or_repo: str, subfolder: str | None = None) -> dict:
    """{robot camera: (h, w)} from the training dataset's meta/info.json, or {} if unavailable."""
    tc = _read_json(path_or_repo, "train_config.json", subfolder) or {}
    repo = (tc.get("dataset") or {}).get("repo_id")
    if isinstance(repo, list):
        repo = repo[0] if repo else None
    if not repo:
        return {}
    try:
        from huggingface_hub import hf_hub_download
        with open(hf_hub_download(repo, "meta/info.json", repo_type="dataset")) as f:
            feats = json.load(f)["features"]
    except Exception:
        return {}
    out = {}
    for k, v in feats.items():
        if k.startswith(PREFIX) and len(v.get("shape", [])) == 3:
            h, w, _ = v["shape"]
            out[k.removeprefix(PREFIX)] = (int(h), int(w))
    return out


def robot_camera_sizes(cfg, path_or_repo: str, subfolder: str | None = None) -> dict:
    """{robot camera name: (h, w)} the robot should send for this checkpoint."""
    inverse = {v: k for k, v in rename_map(path_or_repo, subfolder).items()}
    declared = {}
    for key, ft in cfg.input_features.items():
        if key.startswith(PREFIX):
            _, h, w = tuple(ft.shape)
            declared[inverse.get(key, key).removeprefix(PREFIX)] = (int(h), int(w))
    ds = dataset_image_sizes(path_or_repo, subfolder)
    return {name: ds.get(name, hw) for name, hw in declared.items()}
