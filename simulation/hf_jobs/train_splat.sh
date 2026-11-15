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
# colmap/ (sparse model), session.json. Env knobs: FPS (video frames per second
# to extract, default 2), ITERS (default 30000), MATCHING (exhaustive|sequential).
set -euo pipefail
DATA=${DATA:-/data}
WORK=${WORK:-/tmp/work}
FPS=${FPS:-2}
ITERS=${ITERS:-30000}
MATCHING=${MATCHING:-exhaustive}
: "${OUTPUT_REPO:?set OUTPUT_REPO=<user>/<repo> for the trained splat}"

mkdir -p "$WORK/images" "$WORK/export"
python -m pip install -q -U "huggingface_hub>=0.34"

shopt -s nullglob nocaseglob
for v in "$DATA"/phone/*.{mp4,mov,m4v,avi}; do
  echo ">> frames from $(basename "$v") at $FPS fps"
  ffmpeg -loglevel error -i "$v" -vf "fps=$FPS" -qscale:v 2 \
    "$WORK/images/$(basename "${v%.*}")_%05d.jpg"
done
for p in "$DATA"/phone/*.{jpg,jpeg,png}; do cp "$p" "$WORK/images/"; done
n=$(ls "$WORK/images" | wc -l)
echo ">> $n images"
[ "$n" -ge 30 ] || { echo "too few images (need >= 30)"; exit 1; }

echo ">> COLMAP camera poses"
ns-process-data images --data "$WORK/images" --output-dir "$WORK/ns" --matching-method "$MATCHING"

echo ">> training splatfacto ($ITERS iterations)"
ns-train splatfacto --data "$WORK/ns" --output-dir "$WORK/out" \
  --max-num-iterations "$ITERS" --vis tensorboard --viewer.quit-on-train-completion True

CONFIG=$(find "$WORK/out" -name config.yml | head -1)
ns-export gaussian-splat --load-config "$CONFIG" --output-dir "$WORK/export"
cp "$WORK/ns/transforms.json" "$WORK/export/"
[ -d "$WORK/ns/colmap" ] && cp -r "$WORK/ns/colmap" "$WORK/export/colmap"
cp "$DATA/session.json" "$WORK/export/" 2>/dev/null || true
cp "$CONFIG" "$WORK/export/nerfstudio_config.yml"

echo ">> uploading to $OUTPUT_REPO"
hf upload "$OUTPUT_REPO" "$WORK/export" . --repo-type model --private
echo ">> done"
