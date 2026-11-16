---
title: reBot policy inference
emoji: 🦾
colorFrom: gray
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

GPU inference server for the reBot B601 policies. Serves several checkpoints at once (all loaded at startup):

- `niru-5/xvla_rebot_merged_V2` (default)
- `RoboCrafty/smolvla_rebot_merged_V2`

Source: `teleoperation/remote_inference/` in the steel_team repo. Client: `rollout_policy.py --remote-url <space url> [--policy <repo>]`.

- `GET /policies`: default, available, and any that failed to load
- `GET /info?policy=<repo>`: policy type, chunk size, robot cameras and sizes to send
- `POST /act`: `{policy, state: {"<joint>.pos": deg}, images: {camera: base64 JPEG}, task, n_action_steps}` -> `{actions: [[7 deg] x n], infer_ms}`

Space variables: `POLICIES` (comma-separated; `repo@revision` or `repo:subfolder` allowed; the first is the default),
`POLICY_DTYPE` (auto | bfloat16 | float32), `POLICY_DENOISING_STEPS`; secret `HF_TOKEN` for private checkpoints.

Deploy / update (from `teleoperation/`):

```bash
hf upload niru-5/rebot-policy-server remote_inference . --repo-type space
```
