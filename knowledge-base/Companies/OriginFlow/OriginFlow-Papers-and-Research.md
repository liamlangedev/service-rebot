---
type: papers
company: "OriginFlow"
slug: OriginFlow
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# OriginFlow — Papers and Research

⬆ [OriginFlow profile](OriginFlow.md) · [Solutions and projects](OriginFlow-Solutions-and-Projects.md) · [Developer guide](OriginFlow-Developer-Guide.md)

> **Bottom line:** OriginFlow has **no published paper** on its products or models (PULSE, CHORD, ORACLE, Fusion2Force, NeuroScale, Human Tokens) as of 2026-11-14. Its only public research artifact is **one gated dataset**. No third-party paper using its hardware or data was found. The reading lists below therefore point to the **closest independent work** (sEMG wristbands, force-from-EMG, egocentric human data) — none of it runs on OriginFlow hardware.

## Research footprint

- **Product-first, not paper-first.** Founded August 2025; all technical claims come from press interviews, the website and a Hugging Face dataset card. Searches of arXiv for "OriginFlow", "OriginData", "Fusion2Force", "NeuroScale + sEMG" and "Human Tokens + sEMG" returned **0** results.
- **Key person:** founder / CEO **Qin Shentao (秦深涛)**, PhD candidate at Tsinghua University School of Vehicle and Mobility, BSc Harbin Institute of Technology (robotics-competition background). No other researcher, chief scientist, advisor or partner lab is named publicly. The Hugging Face org lists **6 members**; the GitHub org shows no public members.
- **Open-source posture: data-first, models closed.** Released: one gated dataset of *derived* signals (pose, estimated force, language). Not released: raw sEMG / IMU, any model weights, any device SDK, any paper or model card. The Hugging Face org shows **0 models**.
- **No independent validation.** Accuracy figures that exist are self-reported (dataset card, internal calibration notes). Force is model-estimated, not measured.
- **Web search for this doc:** available but limited to **one** query (it surfaced related work only, nothing by OriginFlow). Everything else comes from direct reads of arXiv (abs / HTML pages and catalogue queries), Hugging Face, GitHub, the official site and press. A paper under a different company or author name could still have been missed.

## Company-authored and company-affiliated papers

**No paper authored by OriginFlow as an organisation was found.** One founder-linked preprint exists; it is unrelated to the sEMG product line and has been withdrawn.

| Paper | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts (code / weights / data links) | Tracks |
|---|---|---|---|---|---|
| [Task-Centric Policy Optimization from Misaligned Motion Priors](https://arxiv.org/abs/2601.19411) | Ziang Zheng, Kai Feng, Yi Nie, **Shentao Qin** — Tsinghua University (School of Vehicle and Mobility; Dept. of Automation), BUPT. ⚠️ unverified that this Shentao Qin is the OriginFlow founder (same name and same Tsinghua school; OriginFlow not mentioned) | arXiv preprint, 2026-01-27 — **withdrawn 2026-02-03** ("requires further details and not complete yet"); v1 still readable | Task-priority adversarial imitation (TCMP) for humanoid control when human motion priors are misaligned; tested on a **Unitree G1 in Isaac Lab** (simulation) | None released | — (humanoid RL, not sensing; do not cite as a finished result) |

Excluded on purpose (name match only):
- Two arXiv preprints list a "Shentao Qin" with a **Peking University** affiliation — [RiskPO (2510.00911)](https://arxiv.org/abs/2510.00911) and [Recursive Likelihood Ratio optimizer for diffusion fine-tuning (2502.00639)](https://arxiv.org/abs/2502.00639). Topics are LLM post-training and diffusion models; nothing ties this author to OriginFlow. Not counted.

## Datasets, models and benchmarks released

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| **OriginData preview sample** ✅ | Dataset — egocentric human manipulation. **100.62 h, 7,717 episodes, 10.87M frames (~30 FPS), 414 GB**; LeRobot v3.0 (Parquet + MP4). Stereo RGB, 21-joint 3D hand pose, head SLAM pose, per-finger **estimated** force (model "Fusion2Force"), 3,323 task descriptions, 26,117 subtask + 101,445 atomic-action labels. Full corpus described as 28 domains / 1,170 tasks. No paper, no BibTeX | Custom `LICENSE.md`, **gated (manual approval)** — licence text could not be opened without login ⚠️ unverified terms | [Hugging Face](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample) (last modified 2026-10-30; 6,742 downloads last month, 25 likes) | Pre-training grasp / contact / task-segmentation models; retargeting human hand trajectories to a dexterous hand; grounding a VLM planner in household and light-industrial tasks (T01, T03, T04) |
| OriginData documentation set (video, hand pose, SLAM, force, semantic annotations) + CHORD-vs-VLM annotation-quality report | Technical notes shipped inside the dataset repo | Same gate as the dataset | [File tree](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample/tree/main) (`assets/docs/`) | The closest thing to a methods description. Card reports contact-label quality **F1 72.41 %** (precision 82.38 %, recall 64.59 %) against a provisional VLM reference |
| `OriginFlow-AI` GitHub org — 5 repos (`wild-few-shot`, `double_gesture_detect`, `rgbd_hand_object_recon`, `repo_for_data_cache`, fork of `DPVO`) ⚠️ unverified affiliation | Internal-looking tools; no paper links, no citation blocks | None stated (DPVO fork: MIT) | [GitHub](https://github.com/OriginFlow-AI) | Hints only: capture gating by two-hand gesture; force recalibration notes (one logged result, MAE **6.53 N → 3.26 N** on one test set); head trajectory likely from patch-based visual odometry |
| PULSE (0.2 / 0.3), CHORD, ORACLE, Fusion2Force | Models 🧪 | — | **Not released** (no weights, API, model card or paper) | Only via an on-site runtime, if the team offers one |
| Benchmarks | — | — | None released | — |

Sample task categories visible in the dataset preview (file names): food and drink packing, shelf and tableware organising, parcel packing, buttoning a shirt, document sorting, **circuit-board assembly, fibre-optic component processing, mobile-phone repair**, infant-massage demonstration.

## Third-party papers using their hardware or software

**None found.** No arXiv paper mentions OriginFlow, OriginKitGen, PULSE-by-OriginFlow or OriginData. The only downstream artifact located is a hobby model, not a paper:

| Paper (link) | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| *(not a paper)* [Nirbaplayz/Dabby](https://huggingface.co/Nirbaplayz/Dabby) | Individual Hugging Face user | Model repo, 2026-10-25 | Tags OriginData preview sample as training data; fine-tune of Qwen2.5-0.5B-Instruct; MIT | Question-answering chatbot; 0 downloads; no evaluation. Not evidence of research use | — |

### Closest independent work (NOT on OriginFlow hardware)

Use these for architectures, training recipes and evaluation ideas. Electrode count, layout and scaling differ from the OriginFlow Band (16 channels), so **weights will not transfer**.

| Paper (link) | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [ForceBand: Learning Forceful Manipulation with sEMG](https://arxiv.org/abs/2606.26093) | Botao He, Zhi Wang, Linna Kuang, Ishaan Ghosh, Jitendra Malik, Cornelia Fermuller, Tingfan Wu, Jiayuan Mao, Ruoshi Liu, Haozhi Qi, Yiannis Aloimonos — Amazon FAR, Univ. of Maryland, Johns Hopkins | arXiv, 2026-06 | Custom **8-channel** sEMG + IMU wristband (OpenBCI Cyton, 250 Hz, BOM about **USD 300**); UR5 + Robotiq gripper + fingertip force sensors | sEMG + IMU to per-finger force; **> 50 %** lower force error than vision baselines; **87 %** success on pick-squeeze-place over 9 objects. Same thesis as OriginFlow, fully open: [code + BOM, Apache-2.0](https://github.com/Bottle101/ForceBand), [project page](https://forceband-emg.github.io/) | T01 T02 T04 |
| [Wearable Multimodal Human-Machine Interface for Integrated Hand Intentions Decoding in Dynamic Teleoperation](https://arxiv.org/abs/2609.07495) | Jiaxuan Li, Yinshi Wu, Xiao Zhang, Hongyu Wang, Renzhen Le, Zhenzhi Ying, Liming Shu — Dalian Univ. of Technology, Univ. of Tokyo | arXiv, 2026-09 | **64-channel** HD-sEMG armband (2 kHz) + 2 IMUs; KUKA iiwa 14 + Inspire five-finger hand over ROS 2 | Decodes gesture, grasp force and hand pose together under free wrist motion (**> 97 %** gesture accuracy, force R² **0.95**); online pouring and grasp-and-place teleoperation. Latency not reported; no code | T02 T04 |
| [Beyond Gestures: Estimating Full Hand Pose and Contact Forces from Wrist-Worn Pressure Sensor Array](https://arxiv.org/abs/2609.16518) | Svetoslav Kolev, Lingni Ma, Michael Goesele, Renzo De Nardi, Jakob Engel, Richard Newcombe | arXiv, 2026-09 | Capacitive pressure-array wristband (no skin electrodes); mocap + tactile-glove ground truth | Continuous full-hand pose and per-finger contact force from wrist pressure — an alternative sensing route to the same outputs PULSE targets | T02 T04 |
| [WristPP: A Wrist-Worn System for Hand Pose And Pressure Estimation](https://arxiv.org/abs/2603.00606) | Ziheng Xi, Zihang Ao, Yitao Wang, Mingeze Gao, Wanmei Zhang, Jianjiang Feng, Jie Zhou | arXiv, 2026-02 (submitted to CHI 2026) | Wrist-worn wide-FoV RGB camera, ViT model | Real-time 3D hand pose + per-vertex pressure from one camera; 133k frames, 20 subjects; [project page](https://zhenqis123.github.io/WristPP/) | T04 |
| [EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data](https://arxiv.org/abs/2602.16710) | Ruijie Zheng, Dantong Niu, Yuqi Xie, ..., Yuke Zhu, Danfei Xu, Linxi Fan | arXiv, 2026-02 | **20,854 h** of action-labelled egocentric human video; 22-DoF dexterous hand | Human-video pre-training lifts dexterous-policy success by **54 %** over no pre-training. This is the "video-only" paradigm OriginFlow positions NeuroScale against / alongside | T01 |
| [A generic non-invasive neuromotor interface for human-computer interaction](https://github.com/facebookresearch/generic-neuromotor-interface) | Patrick Kaifosh, Thomas R. Reardon, CTRL-labs at Reality Labs (Meta) | *Nature*, 2025 (DOI 10.1038/s41586-025-09255-w; journal page not opened — citation taken from the official repo) | Meta research sEMG wristband, 2 kHz | Cross-user sEMG decoding of discrete gestures, handwriting and wrist control without per-user training; data for 100 participants per task + checkpoints, CC-BY-NC-4.0 | T02 T04 |
| [emg2pose: A Large and Diverse Benchmark for Surface Electromyographic Hand Pose Estimation](https://arxiv.org/abs/2412.02725) | Sasha Salter, Richard Warren, Collin Schlager, Adrian Spurr, ..., Jesse Marshall (Meta Reality Labs) | NeurIPS 2024 Datasets and Benchmarks | Wrist sEMG, 2 kHz; 26-camera mocap labels | **193 users, 370 h**; baselines and splits testing generalisation to new users and band placements — the reference benchmark for EMG-to-pose | T04 |
| [Posture-Informed Muscular Force Learning for Robust Hand Pressure Estimation](https://arxiv.org/abs/2410.23629) | Kyungjin Seo, Junghoon Seo, Hanseok Jeong, Sangpil Kim, Sang Ho Yoon | NeurIPS 2024 | Forearm sEMG armband + markerless hand tracking; pressure-glove ground truth; 21 participants | Fusing 3D hand posture with sEMG beats either alone for whole-hand pressure — same recipe as OriginFlow's pose + EMG force estimation; [project page](https://pimforce.hcitech.org/) | T04 |
| [Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots](https://arxiv.org/abs/2402.10329) | Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, Shuran Song | arXiv, 2024 | Hand-held gripper with camera; open hardware and software | Portable demonstration capture that transfers to several robots — the "UMI-style" baseline OriginFlow calls itself a complement to; [project](https://umi-gripper.github.io) | T01 T03 |
| [Dual-Modality Haptic Feedback Improves Dexterous Task Execution with Virtual EMG-Controlled Gripper](https://arxiv.org/abs/2209.15578) | Kezi Li, Jeremy D. Brown | arXiv, 2022 | EMG-controlled virtual gripper; vibration + squeeze feedback; 20 participants | Combined slip + grip-force feedback clearly beats either cue alone for holding a brittle object under EMG control — argues for closing the loop to the user | T02 T04 |
| [Deep Patch Visual Odometry](https://arxiv.org/abs/2208.04726) | Zachary Teed, Lahav Lipson, Jia Deng (Princeton) | arXiv, 2022 | Monocular VO; [code](https://github.com/princeton-vl/DPVO) | Sparse patch tracking for accurate, light visual odometry. Forked in the `OriginFlow-AI` GitHub org ⚠️ affiliation unverified — plausibly behind the head-pose stream | T01 T02 |

## Reading list by track

No OriginFlow paper exists, so every entry is independent work or the company's dataset card.

### T01 Autonomous Urban Services
- [OriginData preview sample (dataset card)](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample) — the only OriginFlow asset you can build on without their hardware; packing, shelf-organising and hand-over style tasks fit T01.1 / T01.3.
- [ForceBand](https://arxiv.org/abs/2606.26093) — shortest path from wrist sEMG to a force-aware pick-and-place policy; code and BOM are open.
- [Universal Manipulation Interface](https://arxiv.org/abs/2402.10329) — baseline for "record a human demo, replay on a robot" (T01.1, T01.2).
- [EgoScale](https://arxiv.org/abs/2602.16710) — how far egocentric video alone goes; useful framing for what force data adds.
- [Deep Patch Visual Odometry](https://arxiv.org/abs/2208.04726) — only if you need head / camera trajectory from the Glass video yourself.

### T02 Resilient & Safe City
- [MI-DHMI teleoperation interface](https://arxiv.org/abs/2609.07495) — closest blueprint for EMG + IMU teleoperation of an arm and five-finger hand over ROS 2 (T02.7).
- [ForceBand](https://arxiv.org/abs/2606.26093) — evidence that sEMG recovers contact for occluded fingers better than vision (ring / pinky contact PR-AUC 0.763 vs 0.398 and 0.590 vs 0.314), the core argument for gloved or smoke-obscured hands.
- [Dual-modality haptic feedback with EMG gripper](https://arxiv.org/abs/2209.15578) — why the operator needs grip-force and slip feedback when the robot hand is remote.
- [Generic neuromotor interface (Meta, Nature 2025)](https://github.com/facebookresearch/generic-neuromotor-interface) — robust discrete-gesture decoding and released checkpoints, a fallback command channel if continuous pose is not available.
- [Beyond Gestures](https://arxiv.org/abs/2609.16518) — alternative wrist sensing for pose + force when skin contact is unreliable.

### T03 Sustainable City
- No directly relevant paper found.
- Nearest material: the [OriginData preview sample](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample) includes phone-repair, circuit-board-assembly and sorting / organising episodes that could seed a repair or sorting skill model (T03.1, T03.6); [UMI](https://arxiv.org/abs/2402.10329) is the standard reference for capturing such skills for robot replay.

### T04 Elderly Care & Rehabilitation
- [PiMForce — posture-informed muscular force](https://arxiv.org/abs/2410.23629) — recipe for grip / press force estimation from sEMG + hand pose; directly reusable for a rehab-exercise feedback demo (T04.3, T04.7).
- [emg2pose](https://arxiv.org/abs/2412.02725) — quantifies cross-user and band-placement generalisation; read before promising that a demo works on a second person.
- [Generic neuromotor interface (Meta, Nature 2025)](https://github.com/facebookresearch/generic-neuromotor-interface) — cross-user intent decoding without per-user training; basis for intent-triggered assistance (T04.1, T04.4).
- [ForceBand](https://arxiv.org/abs/2606.26093) — open training code for sEMG-to-finger-force; adapt for graded grip-strength tracking.
- [Dual-modality haptic feedback with EMG gripper](https://arxiv.org/abs/2209.15578) — feedback design for EMG-driven assistive or prosthetic grasping.
- [MI-DHMI](https://arxiv.org/abs/2609.07495) — from a medical-device lab; joint gesture + force + pose decoding under natural arm movement.
- Caveat: none of these is a clinical study on older adults, and OriginFlow hardware is not a medical device.

## White papers, patents and technical reports

- **White papers / technical reports:** none published. The website has no research, technology-paper, blog or news section. The only method descriptions are the gated documentation files inside the dataset repo and press interviews (QbitAI, TMTPost).
- **Patents:** not checked against patent registers; none cited by the company ⚠️ unverified.
- **Standards:** a joint standards effort with LinkerBot is mentioned in press only ⚠️ unverified (source page not opened in this run).

## Sources

- [OriginFlow official site](https://www.originflow.ai/)
- [OriginFlow — About](https://www.originflow.ai/about)
- [Hugging Face org: OriginFlow-AI](https://huggingface.co/OriginFlow-AI)
- [Hugging Face dataset: OriginData preview sample](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample)
- [Hugging Face API record for the dataset (gating, last-modified, file list)](https://huggingface.co/api/datasets/OriginFlow-AI/origindata-preview-sample)
- [Hugging Face model: Nirbaplayz/Dabby](https://huggingface.co/Nirbaplayz/Dabby)
- [GitHub org: OriginFlow-AI](https://github.com/OriginFlow-AI) (affiliation unverified)
- [GitHub: OriginFlow-AI/wild-few-shot](https://github.com/OriginFlow-AI/wild-few-shot)
- [QbitAI, 2026-08-22 — OriginFlow profile (Chinese)](https://www.qbitai.com/2026/08/477094.html)
- [TMTPost, 2026-05-21 — funding report and founder background](https://en.tmtpost.com/post/7997613)
- [arXiv 2601.19411 — Task-Centric Policy Optimization from Misaligned Motion Priors (abs)](https://arxiv.org/abs/2601.19411) · [v1 HTML](https://arxiv.org/html/2601.19411v1)
- [arXiv 2510.00911 — RiskPO](https://arxiv.org/abs/2510.00911)
- [arXiv 2502.00639 — Recursive Likelihood Ratio optimizer](https://arxiv.org/abs/2502.00639)
- [arXiv 2606.26093 — ForceBand](https://arxiv.org/abs/2606.26093) · [project page](https://forceband-emg.github.io/) · [GitHub](https://github.com/Bottle101/ForceBand)
- [arXiv 2609.07495 — Wearable Multimodal Human-Machine Interface (MI-DHMI)](https://arxiv.org/abs/2609.07495)
- [arXiv 2609.16518 — Beyond Gestures](https://arxiv.org/abs/2609.16518)
- [arXiv 2603.00606 — WristPP](https://arxiv.org/abs/2603.00606)
- [arXiv 2602.16710 — EgoScale](https://arxiv.org/abs/2602.16710)
- [arXiv 2412.02725 — emg2pose](https://arxiv.org/abs/2412.02725)
- [arXiv 2410.23629 — Posture-Informed Muscular Force Learning](https://arxiv.org/abs/2410.23629)
- [arXiv 2402.10329 — Universal Manipulation Interface](https://arxiv.org/abs/2402.10329)
- [arXiv 2209.15578 — Dual-Modality Haptic Feedback with EMG-Controlled Gripper](https://arxiv.org/abs/2209.15578)
- [arXiv 2208.04726 — Deep Patch Visual Odometry](https://arxiv.org/abs/2208.04726)
- [GitHub: facebookresearch/generic-neuromotor-interface (citation for the Nature 2025 paper)](https://github.com/facebookresearch/generic-neuromotor-interface)
- [arXiv API catalogue queries](https://export.arxiv.org/api/query?search_query=all:OriginFlow) (terms: OriginFlow, OriginData, Fusion2Force, NeuroScale, Human Tokens, author "Shentao Qin")
