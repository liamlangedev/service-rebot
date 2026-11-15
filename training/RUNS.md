# Training runs

Log of every training run on [RoboCrafty/rebot_sort_v1](https://huggingface.co/datasets/RoboCrafty/rebot_sort_v1),
including the aborted ones, and why each was stopped. All runs used lerobot 0.7.0 on HF Jobs
(`huggingface/lerobot-gpu:latest`) and all 35 episodes and 3 cameras, with image augmentation on.
Metrics come from the Trackio Space `niru-5/rebot-training`, a private Space backed by the bucket
`niru-5/rebot-training-bucket`.

## Completed runs (2026-11-15)

| | ACT | SmolVLA |
|---|---|---|
| HF job | `6af915bb23985fb9cd82ca00` | `6af915c129dd05ff03681426` |
| Model repo | [`niru-5/act_rebot_sort_v1`](https://huggingface.co/niru-5/act_rebot_sort_v1) | [`niru-5/smolvla_rebot_sort_v1_2026-11-15_02-15-27`](https://huggingface.co/niru-5/smolvla_rebot_sort_v1_2026-11-15_02-15-27) |
| Trackio run | `act_rebot_sort_v1-d77af51a` | `smolvla_rebot_sort_v1-69ba291c` |
| Init | From scratch (ImageNet ResNet18) | `lerobot/smolvla_base` |
| Flavor / workers | `rtx-pro-6000` / 16 | `rtx-pro-6000` / 16 |
| Batch × steps | 96 × 13,500 (1.30M samples, 67 epochs) | 128 × 10,000 (1.28M samples, 67 epochs) |
| Learning rate | 1e-5, constant | 1e-4, cosine (warmup 500, floor 2.5e-6) |
| Chunk size / actions executed | 100 / 100 | 50 / 50 |
| Checkpoint tags | `001500` … `013500` (every 1.5k steps, 9 total) | `002500`, `005000`, `007500`, `010000` |
| Wall time / cost | 2 h 55 m / ~$8.0 | 2 h 57 m / ~$8.1 |
| Speed | 125 samples/s, 0.77 s/step, limited by the GPU | 122 samples/s, 1.05 s/step |
| GPU memory | 62 GB | 38 GB |

### Loss

| Step | ACT loss (L1 / KL) | SmolVLA loss |
|---|---|---|
| 100 | 8.376 (0.638 / 0.774) | 0.862 |
| 1,000 | 0.976 (0.304 / 0.067) | 0.113 |
| 3,000 | 0.262 (0.193 / 0.0069) | 0.057 |
| 6,000 | 0.159 (0.138 / 0.0020) | 0.033 |
| 9,000 | 0.123 (0.114 / 0.0008) | 0.027 |
| 10,000 | — | **0.027** (final) |
| 13,500 | **0.096** (0.093 / 0.0003) (final) | — |

The two losses can't be compared with each other. ACT's is L1 + 10·KL on actions normalised by
mean and std; SmolVLA's is a flow-matching MSE.

### Analysis

- **ACT hasn't converged.** Mean loss over successive tenths of the run went 0.138 (50–60%) →
  0.114 (70–80%) → 0.100 (90–100%), so it was still falling about 13% per 20% of the run. Grad norm
  went 108 → 5.3. The final L1 of 0.093 is in units of each joint's standard deviation, roughly
  1–3° per arm joint and about 15 units on the gripper (range ~360). That's training error.
- **ACT's KL term collapsed** (0.77 → 0.0003), so the CVAE latent is unused and the policy is
  effectively deterministic. This is common with small single-task datasets and harmless at
  inference, which uses a zero latent.
- **SmolVLA converged.** The loss was flat at about 0.027 over the last ~20%, with grad norm
  0.34. That matches the learning rate reaching its floor; lerobot fitted the cosine schedule to
  the 10k steps. More steps on this data wouldn't change much.
- **There's no validation split**, so training loss can't show overfitting after 67 epochs.
  Robot trials are the real evaluation.

### Suggested checkpoints for robot evaluation

Run the policy at 30 Hz to match the dataset fps.

- **ACT:** `013500` (final), and `009000` or `007500` in case the final one overfits. If motion is
  jerky, try temporal ensembling at inference (`n_action_steps=1`, `temporal_ensemble_coeff=0.01`).
- **SmolVLA:** `010000` (final) and `005000`.

## Aborted runs

| # | Policy | Flavor | Settings | HF job | Outcome |
|---|---|---|---|---|---|
| 1 | ACT | a10g-large | b32, 50k steps | `6af90fe4…` | Cancelled while scheduling. The staged config had pinned the slow `pyav` video decoder, so `--dataset.video_backend=torchcodec` was added. |
| 2 | ACT | a10g-large | b32, 50k steps | `6af90ffc…` | Cancelled at step ~200. It ran at 1.16 steps/s, limited by the GPU, so it needed ~12 h and would have hit the 12 h job timeout. |
| 3 | SmolVLA | a100-large | b64, 20k steps | `6af91003…` | Cancelled at step ~200 (1.26 s/step) to restart with Trackio. |
| 4 | ACT | a100-large | b32, 40k steps, Trackio | `6af91263…` | Cancelled at step ~400. It ran at 1.85 steps/s, but data loading took as long as the GPU step (`data_s` ≈ `updt_s`) on 12 vCPUs. Restarted with a larger batch. |
| 5 | SmolVLA | a100-large | b64, 20k steps, Trackio | `6af9126a…` | Cancelled early to restart with a larger batch. |
| 6–7 | ACT, SmolVLA | a100-large | b96 / b128, 10 workers | `6af91416…`, `6af9141d…` | Cancelled within ~1 min to move to `rtx-pro-6000` (23 vCPUs) and feed the GPU faster. |
| 8–9 | ACT, SmolVLA | rtx-pro-6000 | b96 / b128, 22 workers | `6af914ce…`, `6af914d5…` | **Failed** about 15 s into training. The spawned dataloader workers got SIGINT while still importing modules, and the job exited with code 1 and no OOM reason. With 16 workers the same setup worked, giving the completed runs above. |

Total spend on aborted runs was about $1–2.

## Notes for future runs

- Hold out 3–4 episodes with lerobot's eval split to get a validation curve.
- Review or drop the 1,512-frame (50 s) outlier episode. It may be a fumble-and-retry demo.
- lerobot made both model repos public at the final push, even though the staged config is
  private. Set them private with `hf repos settings <repo> --private` if needed.
