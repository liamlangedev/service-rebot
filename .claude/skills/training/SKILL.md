---
name: training
description: Train, monitor and evaluate the reBot B601 manipulation policies (ACT, SmolVLA) with lerobot on Hugging Face Jobs. Use when the user wants to start or change a training run, check a job's status, logs or loss, pick a checkpoint, train on a new dataset, or log results in training/RUNS.md.
---

# Training reBot policies (lerobot on HF Jobs)

Everything lives in `training/`. Read `training/README.md` (setup, flags, and why each one is
there) and `training/RUNS.md` (every run so far, results, suggested checkpoints) before
changing anything.

## Facts

- **Dataset:** `RoboCrafty/rebot_sort_v1`: 35 episodes, 19,177 frames at 30 fps. State and
  action are 7-DoF (`shoulder_pan.pos` … `wrist_roll.pos`, `gripper.pos`, in degrees). Three
  640×480 cameras: `front_wide`, `gripper`, `high_oblique`.
- **Tooling:** lerobot 0.7.0, from the teleop venv: `teleoperation/.venv/bin/lerobot-train`.
  `--job.target=<flavor>` stages the config on the Hub and runs it in
  `huggingface/lerobot-gpu:latest`.
- **Scripts:** `training/act/train.sh` (from scratch) and `training/smolvla/train.sh` (fine-tunes
  `lerobot/smolvla_base`, cameras renamed to `camera1/2/3`). Extra args are appended, so they
  override the defaults.
- **Defaults:** `rtx-pro-6000` (23 vCPU, 96 GB) with 16 dataloader workers. Trackio logs to
  `niru-5/rebot-training` (private Space). Checkpoints are pushed to the Hub.

## Run

```bash
./training/act/train.sh                          # submit and detach (prints the job id)
./training/smolvla/train.sh
TARGET=local ./training/act/train.sh --steps=100 # local smoke test before spending GPU money
./training/act/train.sh --dataset.repo_id=<user>/<new_dataset> --steps=20000
hf jobs ps                                       # status
hf jobs logs <job_id>                            # loss, speed (data_s vs updt_s), errors
hf jobs cancel <job_id>
```

HF Jobs cost money. Confirm the flavor, steps and timeout with the user before submitting,
unless they already asked for a run.

## Pitfalls already found (don't rediscover them)

- Keep `--dataset.video_backend=torchcodec`. Without it, the staged config is pinned to the
  slow `pyav` decoder, because the teleop venv's torchcodec is broken locally.
- Keep 16 workers. 22 workers on `rtx-pro-6000` killed the job about 15 s in (SIGINT at worker
  spawn, exit code 1, no OOM).
- Training is limited by CPU video decoding, so more vCPUs beat a faster GPU. Single-GPU
  flavors top out at 23 vCPUs. `image_transforms.backend=gpu` can't be used: lerobot validates
  the config on the submitting machine, which has no GPU.
- Remote runs need `--trackio.space_id`, because the pod's local Trackio database dies with the pod.
- With `--policy.path`, `--policy.repo_id` is ignored on remote runs. SmolVLA models land in a
  timestamped repo, `niru-5/smolvla_rebot_sort_v1_<date>_<time>`.
- When changing the batch size, scale the steps so the total samples stay comparable (ACT
  96 × 13.5k ≈ SmolVLA 128 × 10k ≈ 1.3M samples, about 67 epochs).

## Evaluate

- There's no validation split, so training loss can't show overfitting. Robot trials are the
  evaluation. Run policies at **30 Hz** (the dataset fps).
- Suggested checkpoints are in `RUNS.md`. ACT hadn't converged at 13.5k; SmolVLA converged at
  about 0.027.
- Sim data recorded with `teleoperation/sim_teleop.py --scene real --record` has the same
  features as the real arm (`robot_type=rebot_b601_follower`). Use the real camera names before
  mixing it with real data. See the `simulation` skill.

## After a run

Add it to `training/RUNS.md`: job id, model repo, Trackio run, flavor, batch × steps, wall time
and cost, the loss table, and a short analysis. Note aborted runs and why they stopped.
