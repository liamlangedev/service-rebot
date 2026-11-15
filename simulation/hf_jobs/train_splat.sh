#!/usr/bin/env bash
# Trains a Gaussian splat of the reBot workspace from a capture-session dataset,
# on Hugging Face Jobs (GPU) in the nerfstudio image. prepare_splat_dataset.py
# puts this script into the dataset; the job mounts the dataset at /data:
#
#   hf jobs run --flavor a10g-large --timeout 3h --secrets HF_TOKEN \
#     -e OUTPUT_REPO=<user>/rebot_scene_splat \
#     -v hf://datasets/<user>/<dataset>:/data \
#     ghcr.io/nerfstudio-project/nerfstudio:latest bash /data/train_splat.sh
#
# Output repo (model type, private): splat.ply, transforms.json (camera poses),
# dataparser_transforms.json (maps those poses into the splat.ply frame),
# colmap/ (sparse model), session.json / object.json. Env knobs: FRAMES (frames kept
# per video, default 200), PICK (candidates per kept frame: the sharpest one is kept,
# default 3), ITERS (default 30000), MATCHING (exhaustive|sequential).
set -euo pipefail
DATA=${DATA:-/data}
WORK=${WORK:-/tmp/work}
FRAMES=${FRAMES:-200}
PICK=${PICK:-3}
ITERS=${ITERS:-30000}
MATCHING=${MATCHING:-exhaustive}
: "${OUTPUT_REPO:?set OUTPUT_REPO=<user>/<repo> for the trained splat}"

mkdir -p "$WORK/images" "$WORK/export"
python -m pip install -q -U "huggingface_hub>=0.34"

shopt -s nullglob nocaseglob
for v in "$DATA"/phone/*.{mp4,mov,m4v,avi}; do
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
  fps=$(python -c "print(min(30, $FRAMES * $PICK / $dur))")
  name=$(basename "${v%.*}")
  echo ">> $name: ${dur}s, candidates at $fps fps, keeping the sharpest of each $PICK"
  mkdir -p "$WORK/cand/$name"
  ffmpeg -loglevel error -i "$v" -vf "fps=$fps" -qscale:v 2 "$WORK/cand/$name/%05d.jpg"
  python - "$WORK/cand/$name" "$WORK/images" "$name" "$PICK" <<'PY'
import sys, cv2
from pathlib import Path
src, dst, name, k = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
files = sorted(src.glob("*.jpg"))
def sharp(f):
    g = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
    return cv2.Laplacian(cv2.resize(g, None, fx=0.5, fy=0.5), cv2.CV_64F).var()
for i in range(0, len(files), k):
    best = max(files[i:i + k], key=sharp)
    best.rename(dst / f"{name}_{i // k:05d}.jpg")
PY
done
for p in "$DATA"/phone/*.{jpg,jpeg,png}; do cp "$p" "$WORK/images/"; done
n=$(ls "$WORK/images" | wc -l)
echo ">> $n images"
[ "$n" -ge 30 ] || { echo "too few images (need >= 30)"; exit 1; }

echo ">> COLMAP camera poses"
ns-process-data images --data "$WORK/images" --output-dir "$WORK/ns" --matching-method "$MATCHING"

# COLMAP can split a video into several models; nerfstudio always takes sparse/0,
# which may be a 2-image fragment. Use the model with the most registered images.
best=$(python - "$WORK/ns/colmap/sparse" <<'PY'
import struct, sys
from pathlib import Path
models = sorted((struct.unpack("<Q", (d / "images.bin").read_bytes()[:8])[0], d.name)
                for d in Path(sys.argv[1]).iterdir() if (d / "images.bin").exists())
print(" ".join(f"sparse/{m}: {k} images" for k, m in models), file=sys.stderr)
print(models[-1][1])
PY
)
if [ "$best" != "0" ]; then
  # rewrite transforms.json and sparse_pc.ply (splatfacto's init) from that model;
  # its images already have their frame_ names, so no rename map
  echo ">> using COLMAP model sparse/$best (the largest)"
  python - "$WORK/ns" "$best" <<'PY'
import sys
from pathlib import Path
from nerfstudio.process_data.colmap_utils import colmap_to_json
ns = Path(sys.argv[1])
n = colmap_to_json(recon_dir=ns / "colmap" / "sparse" / sys.argv[2], output_dir=ns)
print(f">> transforms.json rewritten: {n} frames")
PY
fi
python -c "import json; f=json.load(open('$WORK/ns/transforms.json'))['frames']; print('>>', len(f), 'posed frames'); assert len(f) >= 30, 'too few posed frames'"

echo ">> training splatfacto ($ITERS iterations)"
ns-train splatfacto --data "$WORK/ns" --output-dir "$WORK/out" \
  --max-num-iterations "$ITERS" --vis tensorboard --viewer.quit-on-train-completion True

CONFIG=$(find "$WORK/out" -name config.yml | head -1)
ns-export gaussian-splat --load-config "$CONFIG" --output-dir "$WORK/export"
cp "$WORK/ns/transforms.json" "$WORK/export/"
# splat.ply is in the training (dataparser) frame; this maps transforms.json into it
cp "$(dirname "$CONFIG")/dataparser_transforms.json" "$WORK/export/" 2>/dev/null || true
[ -d "$WORK/ns/colmap" ] && cp -r "$WORK/ns/colmap" "$WORK/export/colmap"
for f in session.json object.json; do cp "$DATA/$f" "$WORK/export/" 2>/dev/null || true; done
cp "$CONFIG" "$WORK/export/nerfstudio_config.yml"

echo ">> uploading to $OUTPUT_REPO"
hf upload "$OUTPUT_REPO" "$WORK/export" . --repo-type model --private
echo ">> done"
