"""Pack a capture session (+ your phone video/photos) as a Hugging Face dataset
for Gaussian-splat training on HF Jobs.

  cd simulation
  uv run --project ../teleoperation python -m capture.prepare_splat_dataset s1 \
      --media ~/Downloads/VID_2026*.mp4 --repo-id <user>/rebot_scene_s1
  # then run the printed `hf jobs run ...` command

Needs `hf auth login` (a token with write access). The dataset is private
unless you pass --public. --no-upload only builds the folder.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from capture.devices import SIM_DIR

MEDIA = {".mp4", ".mov", ".m4v", ".avi", ".jpg", ".jpeg", ".png"}
JOB_SCRIPT = SIM_DIR / "hf_jobs" / "train_splat.sh"
IMAGE = "ghcr.io/nerfstudio-project/nerfstudio:latest"

CARD = """---
tags: [robotics, gaussian-splatting, rebot-b601, mujoco]
---
# reBot B601 workspace capture: {name}

Capture session of the team's real reBot B601 workspace (`simulation/capture` in the
steel_team repo), for training a Gaussian splat of the static scene.

- `phone/`: handheld video/photos of the scene ({n_media} files) used for the splat
- `frames/<pose>/<camera>.png`: the fixed cameras (`cam_corner`, `cam_far`) and the
  wrist camera at each arm pose, 1920x1080
- `compare/`: real vs. sim images for each pose
- `session.json`: measured joint angles per pose, devices, the ChArUco board's spot,
  and the camera calibration results
- `train_splat.sh`: the HF Jobs training script

Scene version {version}. Board on the table: {board}.
"""


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("session", help="session name (captures/<name>) or path")
    p.add_argument("--media", nargs="*", default=[], help="phone videos/photos or folders")
    p.add_argument("--repo-id", default=None, help="<user>/<dataset name>")
    p.add_argument("--public", action="store_true")
    p.add_argument("--no-upload", action="store_true")
    args = p.parse_args()

    sess = Path(args.session)
    if not sess.exists():
        sess = SIM_DIR / "captures" / args.session
    if not (sess / "session.json").exists():
        sys.exit(f"{sess} is not a capture session (no session.json)")
    phone = sess / "phone"
    phone.mkdir(exist_ok=True)
    for m in args.media:
        m = Path(m).expanduser()
        files = [f for f in m.iterdir()] if m.is_dir() else [m]
        for f in files:
            if f.suffix.lower() in MEDIA:
                shutil.copy2(f, phone / f.name)
                print(f"  + {f.name}")
    media = [f for f in phone.iterdir() if f.suffix.lower() in MEDIA]
    if not media:
        sys.exit(f"no phone video/photos in {phone}: pass --media or copy them there")
    heic = [f.name for f in phone.iterdir() if f.suffix.lower() == ".heic"]
    if heic:
        print(f"  ! {len(heic)} HEIC photo(s) will be ignored: export them as JPEG")

    info = json.loads((sess / "session.json").read_text())
    shutil.copy2(JOB_SCRIPT, sess / "train_splat.sh")
    board = info.get("board")
    (sess / "README.md").write_text(CARD.format(
        name=info["name"], n_media=len(media), version=info.get("scene_version"),
        board="no" if not board else f"yes, near-left corner at {board['near_left']} m"))
    print(f"dataset folder ready: {sess} ({len(media)} phone files)")

    repo = args.repo_id
    if args.no_upload or not repo:
        if not repo:
            print("pass --repo-id <user>/<name> to upload")
        return
    from huggingface_hub import HfApi
    api = HfApi()
    api.create_repo(repo, repo_type="dataset", private=not args.public, exist_ok=True)
    api.upload_folder(folder_path=str(sess), repo_id=repo, repo_type="dataset",
                      commit_message=f"capture session {info['name']}")
    user = repo.split("/")[0]
    print(f"\nuploaded: https://huggingface.co/datasets/{repo}")
    print("\nTrain the splat on HF Jobs (about 30-60 min on an A10G):\n")
    print(f"  hf jobs run --flavor a10g-large --timeout 3h --secrets HF_TOKEN \\\n"
          f"    -e OUTPUT_REPO={user}/{repo.split('/')[1]}_splat \\\n"
          f"    -v hf://datasets/{repo}:/data \\\n"
          f"    {IMAGE} bash /data/train_splat.sh")
    print("\n  hf jobs ps / hf jobs logs <job id>   to follow it")


if __name__ == "__main__":
    main()
