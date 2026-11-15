# Training

Policies for the reBot B601 pick-and-place task ("pickup the keys and put it in the designated
bin"), trained on [RoboCrafty/rebot_sort_v1](https://huggingface.co/datasets/RoboCrafty/rebot_sort_v1)
with lerobot 0.7.0 on HF Jobs.

**Dataset:** 35 episodes, 19,177 frames at 30 fps. State and action are 7-DoF (6 arm joints plus
the gripper). There are three 640×480 AV1 cameras: `front_wide`, `gripper` and `high_oblique`.
Most episodes run 13–19 s. One outlier is 50 s; it's kept for now.

| | `act/` (baseline) | `smolvla/` |
|---|---|---|
| Init | From scratch (ImageNet ResNet18) | Fine-tune `lerobot/smolvla_base` |
| Cameras | All 3 | All 3, renamed to `camera1/2/3` |
| Chunk size / actions executed | 100 / 100 | 50 / 50 |
| Batch size / steps | 32 / 50k | 64 / 20k |
| Learning rate | 1e-5 (default) | 1e-4, cosine decay (default) |
| Checkpoints | Every 5k steps, pushed to the Hub | Every 5k steps, pushed to the Hub |
| HF Jobs flavor | `a10g-large` | `a100-large` |

## Run

```bash
./training/act/train.sh          # submits to HF Jobs and detaches
./training/smolvla/train.sh
TARGET=local ./training/act/train.sh --steps=100   # quick local smoke test
hf jobs ps                       # status
hf jobs logs <job_id>            # logs
```

Both scripts use `teleoperation/.venv/bin/lerobot-train`. lerobot's built-in `--job.target`
stages the config on the Hub and runs it in `huggingface/lerobot-gpu:latest`, using your HF token
as a secret.

## Notes

- `--dataset.video_backend=torchcodec` is set explicitly. Without it, the client resolves the
  default backend locally, and the teleop venv's torchcodec is broken, so the staged config gets
  pinned to the slower `pyav` decoder.
- With `--policy.path`, lerobot 0.7.0 ignores `--policy.repo_id` on remote runs. The SmolVLA model
  is pushed to a timestamped repo (`niru-5/smolvla_rebot_sort_v1_<date>_<time>`).
- Run the policy on the robot at 30 Hz to match the dataset fps.
