---
type: dev-guide
company: "OriginFlow"
slug: OriginFlow
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# OriginFlow — Developer Guide (hackathon edition)

⬆ [OriginFlow profile](OriginFlow.md) · [Product portfolio](OriginFlow-Products.md) · [Roadmap and strategy](OriginFlow-Roadmap-and-Strategy.md)

> OriginFlow sells **sensing and data, not robots**. Headings below are adapted: "control" means *how you get signals out of the kit and into someone else's robot*.
> Research note: search-engine queries were unavailable for this pass; everything here comes from direct reads of official pages, the official Hugging Face org and known press. Absence of an SDK is "none found", not "confirmed none".

## TL;DR — how you program it

- **No public device SDK, API, docs portal or ROS 2 package** for OriginKitGen 1.0 (Glass + Band + Space). Live access to raw sEMG or PULSE outputs depends on what the team hands out on site — **ask first, commit second**.
- **There is one real public developer asset:** the gated Hugging Face dataset **OriginData preview sample** — **100.62 h, 7,717 episodes, 10.87M frames**, LeRobot v3.0 Parquet + MP4, with stereo egocentric video, 21-joint 3D hand pose, head SLAM pose, **per-finger force estimates (mN)** and language annotations.
- **Raw 16-channel sEMG and IMU are not listed among the released columns** — the public data is the *derived* layer (pose, force), not the muscle signal.
- **PULSE, CHORD, ORACLE and Fusion2Force have no public weights, API or model card.** You cannot run them yourself unless OriginFlow provides a runtime on site.
- **Any robot motion is your own bridge code** to another vendor's SDK (WUJI, Unitree, Flexiv, ROKAE, Dobot ...). Budget half a day for that bridge and a clutch / dead-man mechanism.

## SDKs and interfaces

| SDK / repo / interface | Language | What it gives you | Link | Notes |
|---|---|---|---|---|
| OriginKitGen 1.0 live stream (raw sEMG, IMU, video) | not public | — | — | No documented transport (UDP / WebSocket / BLE / ROS 2). **Question 1 at the booth** |
| PULSE runtime (hand pose + fingertip force from sEMG) | not public | — | — | 🧪 v0.2 shown live at WAIC 2026; availability to teams unknown |
| Space unit (capture controller) | GUI on the device | Device status, 5-step capture workflow, local recording, unified-timeline preview | [originflow.ai](https://www.originflow.ai/) | ✅ Export format and file access **not public** |
| **OriginData preview sample** | Python (`datasets`, LeRobot v3.0 Parquet + MP4; Dask / Polars also listed) | 100.62 h of human manipulation: stereo video, hand pose, head pose, finger force, language | [Hugging Face](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample) | ✅ **Gated** (log in, accept conditions). Custom `LICENSE.md` — read it before reuse. **414 GB** total |
| OriginFlow-AI GitHub org | C++, Python | Internal-looking tools (see below) — **no device SDK** | [github.com/OriginFlow-AI](https://github.com/OriginFlow-AI) | ⚠️ unverified affiliation (no website link on the org page; name and content match). No licences stated |

Public repositories in the GitHub org (⚠️ affiliation unverified, none is a supported SDK):

| Repo | Language | What it is | Hackathon value |
|---|---|---|---|
| `double_gesture_detect` | C++20, OpenCV 4, Qt5, MediaPipe (Python) | "Capture gate": starts capture only when glasses pose is in range and both hands hold a stable OK gesture in view | Shows the glasses write a **pose JSON (pitch / roll / yaw)**; reusable idea for a hands-free start/stop trigger |
| `rgbd_hand_object_recon` | Python | Early-phase RGB-D hand / object reconstruction (mock pipeline + ICP; TSDF planned) | Low — research scaffold |
| `wild-few-shot` | not stated | Field-capture **force calibration** experiments; one logged result: MAE **6.53 N → 3.26 N** after recalibration on one test set | Tells you force estimates have newton-level error and are calibration-sensitive |
| `DPVO` (fork of princeton-vl/DPVO) | C++ / Python | Deep Patch Visual Odometry | Hints at how head trajectory is computed; not needed by teams |
| `repo_for_data_cache` | — | No description | None |

## Control levels

No actuators, so think in **data levels**. What is known about each:

| Level | Signal | Public rate / spec | Access today |
|---|---|---|---|
| L0 raw | 16-channel sEMG + wrist IMU (Band); egocentric video + head motion (Glass) | Band stream about **96 KB/s**; sampling rate **not public** | Device only. Live API not public |
| L1 reconstructed | Continuous hand pose, fingertip force (PULSE 0.2) | Rate and latency **not public** | Demo by staff; API not public |
| L2 recorded episode | Time-synchronised video + motion + sEMG on one timeline (Space) | not public | Export path not public |
| L3 curated dataset | Pose, force, head pose, language (OriginData) | about **30 FPS**; video nominally **1920 × 1080** per eye | ✅ Public, gated |

- **High-level vs low-level:** if you get L1 (pose + force), map it directly to robot targets. If you only get L0 (raw sEMG), you must train your own decoder — realistic in 48 h only for **2–4 discrete gestures or a single grip-effort scalar**, not full hand pose.
- **EDU / developer editions:** none exist publicly. No firmware tiers or licence unlocks are documented.
- **Force is estimated, not measured.** The official site says pose, intent, force and contact depend on "defined algorithms, calibration, and task conditions".

## ROS 2 and middleware

- **ROS 2 package:** not public. **DDS / LSL / OSC support:** not public.
- Plan a ~50-line bridge node yourself. Suggested topic layout (your own convention, not an OriginFlow standard):

| Topic | Type | Content |
|---|---|---|
| `/originflow/emg_raw` | `std_msgs/Float32MultiArray` | 16 channels per sample or per window |
| `/originflow/hand_pose` | `geometry_msgs/PoseArray` | 21 joints per hand |
| `/originflow/finger_force` | `std_msgs/Float32MultiArray` | 5 values per hand, mN |
| `/originflow/clutch` | `std_msgs/Bool` | Operator enable (dead-man) |

- If the team can only give you files, not a stream: replay recorded episodes through the same topics so the rest of your stack does not care.
- Edge compute for the bridge: any laptop, or a **D-Robotics RDK** board if you want it robot-mounted.

## Simulation and digital twins

- **URDF / MJCF / USD assets:** none (no robot). **Isaac Lab / MuJoCo / Gazebo repos:** none.
- Useful substitute: replay OriginData hand trajectories (21 joints, metres, camera frame, plus head pose in SLAM world frame) against the **target hand's own sim model** from its vendor (for example WUJI Hand or Unitree Dex hand assets) to test your retargeting before touching hardware.
- Retargeting is on you: OriginFlow's cross-embodiment mapping is described in press but not released.

## AI stack

| Asset | What it is | Status | Can you use it this weekend? |
|---|---|---|---|
| **PULSE** | sEMG to hand pose, contact force, actuation force; v0.2 = continuous tracking + fingertip force; v0.3 (tendon force, hand forward kinematics) in development | 🧪 | Only via an on-site runtime, if offered |
| **CHORD** | Omni-modal alignment base (sEMG, vision, IMU, language, robot state); also appears in an annotation-quality report shipped with the dataset | 🧪 | No public artefact |
| **ORACLE** | Auto-annotation of action, force, semantics, task segments | 🧪 internal | No |
| **Fusion2Force** | Model named on the dataset card as the source of the per-finger force values | 🧪 internal | No — you get its outputs in the dataset |
| **OriginData preview sample** | 7,717 episodes; full corpus described as 28 domains, 1,170 tasks | ✅ gated | **Yes** |

OriginData preview — what is inside (from the dataset card):

| Group | Columns (prefix) | Detail |
|---|---|---|
| Video | `observation.images.head_left`, `.head_right` | Stereo RGB, MP4 / H.264, about 30 FPS |
| Hand pose | `observation.hand.{left,right}.joints_3d_camera_m`, `.joints_2d_pixel`, `.wrist_rotation_camera`, `.detected` | **21 3D joints per hand**, metres, camera frame |
| Head | `observation.head.position_in_slam_world`, `.orientation_in_slam_world_xyzw` | SLAM trajectory, quaternion x, y, z, w |
| Force | `left.force_values`, `right.force_values`, `left.force_valid`, `right.force_valid` | **5 channels per hand (thumb to little finger), mN**, estimated; use the `*_valid` flags |
| Language | `task_index`, `language_persistent`, episode `tasks`, `semantic_events_json` | 3,323 task descriptions, **26,117** subtask and **101,445** atomic-action annotations |

- Episode length: mean **46.94 s**, median 31.97 s.
- Annotation quality stated on the card: finger-contact labels vs a provisional VLM reference — **F1 72.41 %**, precision 82.38 %, recall 64.59 %. Treat contact labels as noisy.
- **LeRobot:** tagged LeRobot, v3.0 layout "with multimodal extensions" — expect standard loaders to need small adaptations for the extra columns ⚠️ unverified.
- **Teleoperation pipeline:** not released. Human-data-only: there are **no robot actions** in the dataset, so it suits pre-training, retargeting, task segmentation and VLM grounding rather than direct policy cloning.

Load it (snippet from the dataset card; requires `hf auth login` and accepted conditions):

```python
from datasets import load_dataset
frames = load_dataset("OriginFlow-AI/origindata-preview-sample",
                      name="full_parquet", split="train")
```

- **Do not pull 414 GB over venue Wi-Fi.** Start with the dataset viewer's four sample shards, or download metadata only (`lerobot/meta/**`) and pick a few episodes.

If you get raw sEMG but no PULSE, public third-party starting points (different hardware — electrode layout and scaling will not match, so use them for architectures and training recipes, not weights):

| Resource | Content | Licence |
|---|---|---|
| [Meta emg2pose](https://github.com/facebookresearch/emg2pose) | 193 participants, about 370 h, 2 kHz sEMG + mocap joint angles; baseline checkpoints; 600 MiB mini set | CC-BY-NC-SA-4.0 |
| [Meta generic-neuromotor-interface](https://github.com/facebookresearch/generic-neuromotor-interface) | Discrete gestures, handwriting, wrist tasks; 100 participants per task; 2 kHz; checkpoints | CC-BY-NC-4.0 |
| [Hugging Face LeRobot](https://github.com/huggingface/lerobot) | Dataset format (Parquet + MP4), policies, recording tools | Apache-2.0 |

## Compute, sensors and connectivity

| Item | Known | Not public |
|---|---|---|
| Band | 16-channel microvolt-level sEMG + wrist motion; about 96 KB/s; strap slightly wider than an Apple Watch band | Sampling rate, bit depth, radio (BLE / Wi-Fi / wired), battery life, left / right or dual-wrist use |
| Glass | First-person video + head motion; public dataset is **stereo** 1920 × 1080 (⚠️ unverified that the dataset was shot on this exact Glass) | FoV, shutter, on-device compute, pose output rate |
| Space | Device control, workflow, status, local recording and storage | CPU / GPU, storage size, ports, OS, whether it exposes a network API |
| Laptop link | — | No documented IP defaults, ports or pairing procedure |

- On-device signal conditioning (filtering, motion-artefact suppression) is done in hardware per press; decoding is done by the model.
- Assume **your own laptop does inference and robot control**. Bring a USB-C hub and a small router or switch in case the stream is IP-based.

## First 60 minutes checklist

1. **(0–5 min) Ask the four gating questions** at the booth: live stream of raw sEMG and/or PULSE outputs? Transport, rate, latency? Per-user calibration time? Can recordings be exported, and in what format?
2. **(5–10 min) In parallel, one teammate requests dataset access:** log in to Hugging Face, accept the conditions on [OriginData preview sample](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample), open `LICENSE.md`.
3. **(10–20 min) Fit and calibrate:** wear Band (and Glass if needed), run Device Setup and Quick Calibration on Space, confirm all devices show connected and timeline-aligned.
4. **(20–30 min) Verify signal:** do rest, fist, pinch, wrist flex. In the preview you should see clearly different EMG activity per gesture and, if PULSE is running, fingertip force rising during pinch. If not, re-seat the band and recalibrate.
5. **(30–40 min) Record one 30-second episode** and get it off the device (or have staff export it). Open it on your laptop. If you cannot read the file, you cannot build on recordings — pivot to live stream or to the public dataset.
6. **(40–50 min) Hello-world bridge:** print the live values (or replay the file) in a Python loop; publish one scalar — pinch aperture (thumb-tip to index-tip distance) or index-finger force — on a ROS 2 topic or straight into the target robot SDK.
7. **(50–60 min) First motion with a clutch:** map that scalar to gripper open / close on the partner robot at low speed, gated by a keyboard or foot-pedal dead-man. Measure end-to-end latency by filming hand and gripper together.
8. **Decision gate at minute 60:** live stream working → build teleop / intent control. Files only → build a demonstration-capture or rehab-feedback story. Neither → use OriginData for an offline model and switch hardware vendor for the live demo.

## Known gotchas and safety

- **No e-stop of its own.** The robot's e-stop and speed limits are your only safety layer; never drive an arm from EMG without a dead-man switch and workspace limits.
- **EMG is person- and placement-specific.** Expect recalibration per user and after re-seating the band; sweat, dry skin and band shift degrade signal. The pipeline explicitly includes "individual calibration".
- **Force values are model estimates.** Internal calibration notes show newton-level error (MAE of several N in one experiment ⚠️ single data point, unverified affiliation). Do not use them as a safety-rated force limit or a clinical measurement.
- **Wristband alone cannot fully resolve fingers** — the company itself combines it with vision and IMU. Occluded or out-of-view hands will be weaker.
- **Not a medical device.** No public CE / MDR / FDA status. For T04, present it as a research prototype; no diagnostic or therapeutic claims.
- **Privacy:** Glass records first-person video. In a spa town with clinic guests, get consent, avoid filming bystanders, and check event rules before recording outside the venue.
- **Dataset licence and gating:** access requires sharing your Hugging Face identity; the licence is custom. Check redistribution and commercial terms before publishing derived models.
- **Dataset scope:** human hands only, no robot actions; raw sEMG / IMU not listed as released; contact labels are noisy (F1 about 72 %); always filter on `force_valid` and `detected`.
- **Website caveat:** parts of the official site still carry template placeholder text (generic FAQ) — it is not a documentation source.
- **Hygiene:** skin-contact wearable shared between teammates — wipe electrodes between users.

## Community resources

| Resource | Link | Use |
|---|---|---|
| Official site | [originflow.ai](https://www.originflow.ai/) | Product overview, enquiry |
| Email | contact@originflow.ai | Demo / partnership requests |
| Hugging Face org | [OriginFlow-AI](https://huggingface.co/OriginFlow-AI) | Dataset, discussions tab on the dataset page |
| GitHub org ⚠️ unverified | [OriginFlow-AI](https://github.com/OriginFlow-AI) | Internal tools, no issue-tracker support implied |
| X / LinkedIn | [x.com/originflowai](https://x.com/originflowai) · [LinkedIn](https://www.linkedin.com/company/originflow/) | Announcements |
| Forum / Discord / docs | not public | — |

**The fastest support channel this weekend is the OriginFlow staff on site.**

## Sources

- [OriginFlow official site](https://www.originflow.ai/)
- [OriginFlow — About](https://www.originflow.ai/about)
- [OriginFlow — Portfolio](https://www.originflow.ai/portfolio)
- [OriginFlow — Contact](https://www.originflow.ai/contact)
- [Hugging Face org: OriginFlow-AI](https://huggingface.co/OriginFlow-AI)
- [Hugging Face dataset: OriginData preview sample (card)](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample)
- [Hugging Face dataset: file tree](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample/tree/main)
- [GitHub org: OriginFlow-AI](https://github.com/OriginFlow-AI) (affiliation unverified)
- [GitHub: OriginFlow-AI/double_gesture_detect](https://github.com/OriginFlow-AI/double_gesture_detect)
- [GitHub: OriginFlow-AI/rgbd_hand_object_recon](https://github.com/OriginFlow-AI/rgbd_hand_object_recon)
- [GitHub: OriginFlow-AI/wild-few-shot](https://github.com/OriginFlow-AI/wild-few-shot)
- [QbitAI, 2026-08-22 — OriginFlow profile (Chinese)](https://www.qbitai.com/2026/08/477094.html)
- [36Kr Europe, 2026-08-24 — republished profile (English)](https://eu.36kr.com/en/p/3950735048031365)
- [TMTPost, 2026-05-21 — funding report](https://en.tmtpost.com/post/7997613)
- [Meta emg2pose (GitHub)](https://github.com/facebookresearch/emg2pose)
- [Meta generic-neuromotor-interface (GitHub)](https://github.com/facebookresearch/generic-neuromotor-interface)
- [Hugging Face LeRobot (GitHub)](https://github.com/huggingface/lerobot)
