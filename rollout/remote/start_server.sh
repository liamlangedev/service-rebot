#!/usr/bin/env bash
# Start the policy server on an HF Jobs GPU and print its URL for `--remote`.
#
#   rollout/remote/start_server.sh                 # T4 ($0.40/h), stops itself after 2 h
#   FLAVOR=l4x1 TIMEOUT=1h rollout/remote/start_server.sh
#   hf jobs cancel <job id>                        # stop it (and the billing) when done
#
# The job runs huggingface/lerobot-gpu:latest with rollout/remote/policy_server.py and a
# copy of the rollout's PolicyRunner, mounted read-only. HF_TOKEN from the repo's .env is
# passed as a job secret so the server can download private models. The port is exposed
# through the HF jobs proxy with token auth: only your HF token can call it.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HF="${HF:-$ROOT/teleoperation/.venv/bin/hf}"
PY="${PY:-$ROOT/teleoperation/.venv/bin/python}"
FLAVOR="${FLAVOR:-t4-small}"
TIMEOUT="${TIMEOUT:-2h}"
ENV_FILE="${ENV_FILE:-$ROOT/.env}"
[[ -f "$ENV_FILE" ]] || ENV_FILE="$(git -C "$ROOT" rev-parse --path-format=absolute --git-common-dir)/../.env"
[[ -f "$ENV_FILE" ]] || { echo "no .env with HF_TOKEN found (set ENV_FILE=)"; exit 1; }

MOUNT="$ROOT/rollout/remote/.mount"
rm -rf "$MOUNT" && mkdir -p "$MOUNT/grasp_policy"
cp "$ROOT/rollout/remote/policy_server.py" "$MOUNT/"
SRC="$ROOT/ros2_ws/src/rebot_trash_sorting_agent/rebot_trash_sorting_agent/grasp_policy"
cp "$SRC/__init__.py" "$SRC/runner.py" "$SRC/relative.py" "$MOUNT/grasp_policy/"

echo "submitting policy server: $FLAVOR, timeout $TIMEOUT"
out="$("$HF" jobs run --flavor "$FLAVOR" --timeout "$TIMEOUT" --detach --name rebot_policy_server \
  --secrets-file "$ENV_FILE" --expose 8000 -v "$MOUNT:/work" \
  huggingface/lerobot-gpu:latest python /work/policy_server.py --port 8000 --device cuda 2>&1)"
job="$(sed -n 's/^id=\([0-9a-f]*\).*/\1/p' <<<"$out" | head -1)"
[[ -n "$job" ]] || { echo "$out"; exit 1; }
echo "job $job  (stop it with: $HF jobs cancel $job)"

"$PY" - "$job" <<'EOF'
import json, sys, time, urllib.request
from huggingface_hub import HfApi, get_token
job, api, tok = sys.argv[1], HfApi(), get_token()
t0 = time.time()
while True:
    st = api.inspect_job(job_id=job).status
    stage = str(st.stage).split(".")[-1]
    urls = list(getattr(st, "expose_urls", None) or [])
    if stage in ("ERROR", "CANCELED", "COMPLETED", "DELETED"):
        sys.exit(f"job ended: {stage} {getattr(st, 'message', '') or ''}")
    if stage == "RUNNING" and urls:
        url = urls[0].rstrip("/")
        try:
            req = urllib.request.Request(url + "/health", headers={"Authorization": f"Bearer {tok}"})
            with urllib.request.urlopen(req, timeout=10) as r:
                print("server up:", json.loads(r.read()))
                print(f"\nREMOTE={url}\n\nuse it with:  rollout/run.sh towel-smolvla-rel --remote $REMOTE")
                break
        except Exception as e:
            pass
    print(f"  {stage.lower()}... {time.time() - t0:.0f} s", flush=True)
    time.sleep(10)
EOF
