---
title: reBot policy inference
emoji: 🦾
colorFrom: gray
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

GPU inference server for the reBot B601 policies (default `niru-5/xvla_rebot_merged_V2`).
Source: `teleoperation/remote_inference/` in the steel_team repo. Client: `rollout_policy.py --remote-url`.

- `GET /info`: policy type, chunk size, expected camera sizes
- `POST /act`: `{state: {"<joint>.pos": deg}, images: {name: base64 JPEG}, task, n_action_steps}` -> `{actions: [[7 deg] x n], infer_ms}`

Space variables `POLICY_REPO` / `POLICY_SUBFOLDER` / `POLICY_REVISION` select another checkpoint (secret `HF_TOKEN` for private ones).

Deploy / update (from `teleoperation/`):

```bash
hf repo create <user>/rebot-policy-server --repo-type space --space-sdk docker --private
hf upload <user>/rebot-policy-server remote_inference . --repo-type space
# then pick GPU hardware in the Space settings (or: HfApi().request_space_hardware(...))
```
