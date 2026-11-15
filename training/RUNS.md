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

## Grasp-only ACT runs (2026-11-15)

Small ACTs trained only on the grasp (handoff to a 5 cm lift), cut out of `rebot_sort_v1` by
[`training_gripper/make_dataset.py`](../training_gripper/README.md) (HF job
`6af9960829dd05ff03689948`, cpu-upgrade). Both datasets and models are private.

| | A: absolute | B: relative |
|---|---|---|
| Dataset | `niru-5/rebot_grasp_keys_abs`: 30 clips, 3,456 frames, 3 cameras | `niru-5/rebot_grasp_keys_rel`: 120 clips (4 start offsets per grasp), 11,124 frames, gripper camera |
| State / action | absolute lerobot degrees | arm joints relative to the clip's first state; gripper absolute |
| Held out | last 3 source episodes (32-34), `eval_split=0.0833` | same episodes (12 clips), `eval_split=0.0958` |
| HF job | `6af9a6eb23985fb9cd8350ac` | `6af9a6e423985fb9cd83509b` |
| Model repo | `niru-5/act_rebot_grasp_keys_abs` | `niru-5/act_rebot_grasp_keys_rel` |
| Settings | rtx-pro-6000, 8 workers, batch 64 x 5k steps, chunk 30, lr 3e-5 (backbone too), eval every 500 steps, checkpoints every 1k | same |
| Result | **stopped at step ~2.1k** (job COMPLETED after 33 min, log ends mid-run with no error; no final model pushed). Checkpoints `001000`, `002000` under `checkpoints/`. Eval loss 0.395 / 0.384 / 0.396 / **0.380** at 0.5k / 1k / 1.5k / 2k. 1.2-1.3 steps/s: data-bound with 3 cameras on 8 workers (`data_s` ~0.4 s ~ `updt_s`). | Completed 5k steps in 27 min. Eval loss 0.446 (0.5k) -> 0.401 (1k) -> 0.386 (2.5k) -> **0.380** (4.5k) -> 0.391 (5k); flat after ~2.5k. Final train loss 0.066 (L1 0.059). Final model at the repo root; checkpoints every 1k. |

First attempt (`6af9a547…` rel, `6af9a557…` abs, 16 workers) crashed at step 500, the first
eval: the eval DataLoader spawned 16 more workers next to the 16 training workers and they
died at spawn ("CPU dispatcher tracer already initlized", OpenBLAS thread limit). Cancelled
and rerun with 8 workers; data loading was far from the bottleneck (`data_s` 0.04 s vs
`updt_s` 0.15 s at 5.6 steps/s).

Suggested for robot trials: rel final (or `004000`), abs `002000` (`rollout/` loads it by
default). Both eval losses settle near 0.38 on the 3 held-out grasps. The abs run's early
stop is unexplained; rerun it if the abs strategy looks promising.

SmolVLA on the same datasets was considered and skipped for now.

On the real arm (`rollout/`, 2026-11-15): grasp-abs gripped and lifted 2/2 from held-out
clip 27. grasp-rel did so 1/4 started runs; in the other three the policy closed the jaw
in the air and kept descending (ended on the floor limit or the timeout).

## Towel grasp runs: ACT and SmolVLA (2026-11-15)

Same pipeline on [RoboCrafty/rebot_sort_towel2](https://huggingface.co/datasets/RoboCrafty/rebot_sort_towel2)
(32 episodes, 640x360 cameras, same joint and gripper conventions as rebot_sort_v1). All 32
grasps pass the filters. Like the keys, the towel grasps are all in one spot (TCP x
0.40-0.47 m, y -0.29 to -0.19 m, xy std 2.3 cm), so "random locations" is what the relative
variant is for. Task text: "pick up the towel" (the SmolVLA prompt). Built on HF Jobs
(`6af9bf4c29dd05ff0368ca52`, cpu-upgrade); the datasets are **public**.

| | abs (specific location) | rel (random locations) |
|---|---|---|
| Dataset | [`niru-5/rebot_grasp_towel_abs`](https://huggingface.co/datasets/niru-5/rebot_grasp_towel_abs): 32 clips, 3,507 frames, 3 cameras, `eval_split=0.078125` | [`niru-5/rebot_grasp_towel_rel`](https://huggingface.co/datasets/niru-5/rebot_grasp_towel_rel): 128 clips, 11,148 frames, gripper camera, `eval_split=0.08984375` |
| Held out | source episodes 29-31 | same |
| ACT | `6af9c3e929dd05ff0368cffc` -> `niru-5/act_rebot_grasp_towel_abs` | `6af9c3d329dd05ff0368cfcd` -> `niru-5/act_rebot_grasp_towel_rel` |
| SmolVLA | `6af9c3f429dd05ff0368d00e` -> `niru-5/smolvla_rebot_grasp_towel_abs_2026-11-15_14-38-42` | `6af9c3de23985fb9cd836e48` -> `niru-5/smolvla_rebot_grasp_towel_rel_2026-11-15_14-38-20` |

ACT settings as for the keys (`training_gripper/train.sh`). SmolVLA
(`training_gripper/train_smolvla.sh`): fine-tunes `smolvla_base`, cameras renamed to
camera1/2/3 (gripper -> camera2), batch 64 x 5k steps, cosine warmup 300 / decay 5k, eval
every 500 steps, 8 workers, rtx-pro-6000. Model repos are private.

All four completed 5k steps (models private, checkpoints every 1k). Eval loss on the 3
held-out grasps:

| step | ACT rel | ACT abs | SmolVLA rel | SmolVLA abs |
|---|---|---|---|---|
| 500 | 0.303 | 0.305 | 0.456 | 0.441 |
| 1000 | 0.260 | 0.306 | **0.469** | **0.575** |
| 2000 | 0.253 | 0.275 | 0.588 | 0.620 |
| 3000 | 0.250 | 0.269 | 0.703 | 0.674 |
| 4000 | 0.242 | **0.267** | 0.759 | 0.853 |
| 5000 | **0.239** | 0.270 | 0.723 | 0.920 |

- **ACT** keeps improving (rel) or flattens (abs) on held-out grasps: use the final models.
- **SmolVLA overfits**: eval loss rises from step 500 while train loss falls (rel final
  train loss 0.044). About 30 short clips from one towel position are not enough for a
  450M fine-tune at 5k steps. Use checkpoint `001000`, the earliest saved. For a rerun:
  fewer steps (~1k), save every 250, or freeze more of the model.
- SmolVLA's flow-matching eval loss and ACT's L1+KL loss are not comparable with each
  other.
- `rollout/run.sh towel-*` loads: ACT final, SmolVLA `checkpoints/001000`.

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
