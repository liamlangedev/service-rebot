#!/usr/bin/env bash
# Put the detector weights where agent.yaml expects them.
#
# agent.yaml points at ${models}/yoloe-26l-seg.pt, and ${models} resolves to
# $REBOT_AGENT_MODELS or ~/.cache/rebot_agent/models. YOLOE also needs its text
# encoder next to the weights (it is loaded from the working directory).
#
#   ./scripts/fetch_models.sh /path/to/weights    copy from a local directory
#   MODEL_URL=https://... MOBILE_URL=https://... ./scripts/fetch_models.sh
#
# Nothing is downloaded unless you set the URLs: the exact file names change with
# ultralytics releases, and a wrong 40 MB download is worse than a clear message.
set -euo pipefail

MODELS="${REBOT_AGENT_MODELS:-$HOME/.cache/rebot_agent/models}"
MODEL_NAME="${MODEL_NAME:-yoloe-26l-seg.pt}"
TEXT_ENCODER="${TEXT_ENCODER:-mobileclip2_b.ts}"
mkdir -p "$MODELS"

if [[ -n "${1:-}" ]]; then
  SRC="$1"
  for file in "$MODEL_NAME" "$TEXT_ENCODER"; do
    if [[ -f "$SRC/$file" ]]; then
      cp -v "$SRC/$file" "$MODELS/"
    else
      echo "warning: $SRC/$file not found" >&2
    fi
  done
fi

if [[ -n "${MODEL_URL:-}" ]]; then
  echo "downloading $MODEL_NAME"
  curl -fL --retry 3 -o "$MODELS/$MODEL_NAME" "$MODEL_URL"
fi
if [[ -n "${MOBILE_URL:-}" ]]; then
  echo "downloading $TEXT_ENCODER"
  curl -fL --retry 3 -o "$MODELS/$TEXT_ENCODER" "$MOBILE_URL"
fi

echo
echo "model directory: $MODELS"
ls -lh "$MODELS" 2>/dev/null || true

for file in "$MODEL_NAME" "$TEXT_ENCODER"; do
  if [[ ! -f "$MODELS/$file" ]]; then
    cat >&2 <<EOF

missing: $MODELS/$file
   copy it in by hand, or set MODEL_URL / MOBILE_URL, or point
   perception.model in config/agent.yaml at wherever it already lives.
EOF
    exit 1
  fi
done

echo "ok: agent.yaml -> \${models}/$MODEL_NAME resolves here ($MODELS)"
