---
type: papers
company: "WUJI"
slug: WUJI
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# WUJI — Papers and Research

⬆ [WUJI profile](WUJI.md) · [Solutions and projects](WUJI-Solutions-and-Projects.md) · [Developer guide](WUJI-Developer-Guide.md)

> **Coverage note (read first):** this pass was built from pages opened directly (arXiv, the paper project page, the `wuji-technology` GitHub READMEs, Wuji Docs, wuji.tech). The open-web search budget for this run was exhausted before any paper hunt could be run, so **the third-party section is a lower bound, not a census**. Everything listed below was opened and checked; nothing is listed from memory.

## Research footprint

- **One peer-reviewed paper, a lot of open code.** The only paper tied to WUJI that could be confirmed is **TopoRetarget (CoRL 2026, arXiv 2606.16272)**. The rest of the research output ships as citable open-source repositories (RL, retargeting, teleoperation, VLA fine-tuning), not as papers.
- **Academic link: IIIS, Tsinghua University.** The TopoRetarget paper lists a single affiliation (IIIS, Tsinghua; corresponding author **Hang Zhao**), yet the code lives in the WUJI GitHub organisation, support goes to support@wuji.tech, and the same people are the listed contributors of WUJI's own repos. Whether individual authors are WUJI employees, interns or Tsinghua students is **not stated** — ⚠️ unverified.
- **Recurring names** across WUJI repos: **Guanqi He** and **Xiaohan Liu** (project leads of TopoRetarget), **Wentao Zhang**, **Jielin Wu**, **Shenzhe Yao**, **Han Yang**, **Xiangrui Jiang**. Guanqi He and Wentao Zhang are the cited authors of `wuji-retargeting`; Guanqi He is first cited author of `wuji-hand-teleop`.
- **Open-source posture: strong.** 24 public repos; MIT for SDK, models, retargeting and teleop; Apache-2.0 for the RL and VLA stacks. Trained RL checkpoints, motion clips and CAD for the test rigs are published as GitHub release bundles.
- **No research page, blog or white paper** on wuji.tech (site navigation is Hand, Hand 2, Glove, Docs, Careers, Contact). No WUJI foundation model, benchmark or large dataset was found.

## Company-authored and company-affiliated papers

| Paper | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts (code / weights / data links) | Tracks |
|---|---|---|---|---|---|
| [TopoRetarget: Interaction-Preserving Retargeting for Dexterous Manipulation](https://arxiv.org/abs/2606.16272) | Jielin Wu*, Shenzhe Yao*, Guanqi He*‡, Xiaohan Liu*‡, Zhaoqing Zeng, Xiangrui Jiang, Han Yang, Wentao Zhang, Hang Zhao† — IIIS, Tsinghua University (code released by Wuji Technology) | CoRL 2026 (per project page and repo BibTeX); arXiv v1 2026-06-15, v2 2026-06-22 | Converts human hand-object motion (21 keypoints + object pose) into robot-hand reference motion that keeps **which parts touch the object and how**, by solving a per-frame QP over an interaction mesh; one parameter set for all clips, no training stage, CPU only. References feed a PPO tracking policy that runs **zero-shot on the real Wuji Hand** (cube reorientation, pen spinning). | [Code (MIT)](https://github.com/wuji-technology/toporetarget) · [Project page](https://toporetarget2026.github.io/TopoRetarget/) · [Raw pen-spin capture bundle](https://github.com/wuji-technology/toporetarget/releases/latest/download/toporetarget-assets.zip) · [RL training + checkpoints in wuji-mjlab](https://github.com/wuji-technology/wuji-mjlab) | T02 T04 (indirect: demonstration-to-robot pipeline) |

\* equal contribution · ‡ project lead · † corresponding author.

**Key numbers reported for TopoRetarget** (from the arXiv abstract, paper body and project page):

| Result | Value |
|---|---|
| Pen-spin RL training success versus existing retargeting baselines | **+40.6 percentage points** |
| Grasp tracking on HO-Cap (32 single-hand clips) | **84.4 %** success, **0.87 cm** position error (best of compared methods) |
| Versus baseline average (project page) | contact-precision error **−55 %**, maximum penetration **−92 %** |
| Retargeting-quality benchmark | ContactPose, **25 of 28** grasps (3 deeply concave objects excluded) |
| Real hardware | zero-shot cube reorientation and pen spinning on the Wuji Hand; pen kept spinning in **5 / 5** trials |
| Own capture data | **32** pen-spin demonstrations (mocap + Wuji Glove), average **12.4 s** |
| Baselines compared | OmniRetarget, Mink, DexPilot, GeoRT |
| Embodiments shown | MANO, Wuji Hand, LEAP Hand |
| Stated limitation | fails when the human demo itself has a missing contact (finger hovers without touching) |

![TopoRetarget pipeline: input, bone-direction warm-up, interaction-mesh optimisation, output](https://raw.githubusercontent.com/wuji-technology/toporetarget/main/docs/images/pipeline.png)

![TopoRetarget demos: pen-spin capture and GRAB, TACO, OakInk2, HOT3D clips retargeted to Wuji Hand 2](https://raw.githubusercontent.com/wuji-technology/toporetarget/main/docs/images/demos.jpg)

**Citable WUJI software records (no paper behind them)** — these carry a `@software` citation block in the README and are the closest thing to technical reports:

| Record | Cited authors | Year | What it documents | Link | Tracks |
|---|---|---|---|---|---|
| Wuji-MJLab: RL Training for Wuji Hand Dexterous Manipulation | Wuji Technology (9 named contributors) | 2026 | PPO in-hand **cube reorientation** (Hand 1 and Hand 2) and reference-tracking **pen spinning** (Hand 2, 20 joints at 50 Hz), with camera-in-the-loop sim-to-real deployment and ONNX export | [wuji-mjlab](https://github.com/wuji-technology/wuji-mjlab) | — |
| Wuji-IsaacLab: RL Training for Wuji Hand Dexterous Manipulation in Isaac Lab | Wuji Technology | 2026 | Same reorientation task for Hand 2 on Isaac Lab 2.3.2 / Isaac Sim 5.1 with rsl_rl PPO; exported policies run on the wuji-mjlab deployment stack | [wuji-isaaclab](https://github.com/wuji-technology/wuji-isaaclab) | — |
| WujiHand Retargeting | Guanqi He, Wentao Zhang | 2026 | Hand-pose retargeting (adaptive analytical + key-vector optimisers) from Wuji Glove, Vision Pro, video, RealSense, ZED; now folded into Wuji SDK (repo archived in docs) | [wuji-retargeting](https://github.com/wuji-technology/wuji-retargeting) | T02 T04 |
| Wuji Hand Teleop: ROS2 Teleoperation for Dexterous Hands and Robot Arms | Guanqi He, Wentao Zhang, Liang Zhu, Duo Han, Shiquan Qiu | 2026 (BibTeX key says 2025) | Glove-driven dual-hand teleop plus arm teleop (HTC Vive Tracker or PICO 4, Tianji arms), head stereo + wrist D405 cameras, MCAP recording. Marked **not actively maintained** | [wuji-hand-teleop](https://github.com/wuji-technology/wuji-hand-teleop) | T02 T04 |
| wuji-openpi | Wuji Technology (fork of Physical Intelligence openpi) | 2026 | Fine-tuning and ROS 2 deployment of **pi0 / pi0.5** for any dual-arm + Wuji Hand layout; reference config `pi05_wuji_multi_54d` (7+7 arm, 20+20 hand = **54-dim** action) | [wuji-openpi](https://github.com/wuji-technology/wuji-openpi) | T01 T03 T04 |

## Datasets, models and benchmarks released

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| ✅ TopoRetarget solver | Code (CPU-only QP retargeting; importers for GRAB, TACO, OakInk2, HOT3D and keypoint-capture bundles) | MIT | [toporetarget](https://github.com/wuji-technology/toporetarget) | Turning a human demo (glove or public dataset) into Wuji Hand 2 joint references in about half a minute per clip |
| ✅ `data/pen_spin` example clip | Data: one right-hand pen-spin keypoint capture (`pen_spin_029`, 231 frames, 250 mm pen) | ships in the MIT repo | [data/README](https://github.com/wuji-technology/toporetarget/blob/main/data/README.md) | Testing the retargeting pipeline with no downloads |
| ✅ `toporetarget-assets.zip` (release v2026.10.23) | Data: raw pen-spin capture package (mocap + Wuji Glove keypoints, pen asset metadata) | not stated separately — ⚠️ unverified | [release asset](https://github.com/wuji-technology/toporetarget/releases/latest/download/toporetarget-assets.zip) | Reproducing the paper's pen-spin references; template for your own capture format |
| ✅ wuji-mjlab | Code: RL training + sim-to-real (mjlab, PPO), tasks Cube Reorient and PenSpin | Apache-2.0 | [wuji-mjlab](https://github.com/wuji-technology/wuji-mjlab) | Training or replaying in-hand skills; needs NVIDIA GPU (CUDA 12.8) and pixi |
| ✅ wuji-mjlab asset bundle v2026.10.22 | **Trained policies + data + CAD**: reorient checkpoints per hand and **five pen-spin checkpoint sets** (`model.pt`, `policy.onnx`, `config.json`), **40 pen-spin motion clips**, five recipes, cube / pen / jig CAD (STEP, 3MF) | not stated separately (repo is Apache-2.0) — ⚠️ unverified | [asset bundle](https://github.com/wuji-technology/wuji-mjlab/releases/download/v2026.10.22/wuji-mjlab-v2026.10.22-assets.zip) | A ready-made in-hand manipulation demo without training; note it needs the camera + tag rig described in the repo |
| ✅ wuji-isaaclab | Code: Isaac Lab task `Wuji-Hand2-Reorient-v0` | Apache-2.0 (Isaac Sim itself is proprietary) | [wuji-isaaclab](https://github.com/wuji-technology/wuji-isaaclab) | Teams already on Isaac Lab; no pretrained checkpoint mentioned in the README |
| ✅ wuji-openpi | Code: pi0 / pi0.5 fine-tuning configs and ROS 2 deployment client; MCAP → LeRobot v2.1 data path | Apache-2.0 | [wuji-openpi](https://github.com/wuji-technology/wuji-openpi) | VLA fine-tuning on arm + Wuji Hand data. **No WUJI fine-tuned weights or demonstration dataset are published** — you start from the upstream `pi05_base` checkpoint and your own teleop data |
| ✅ wuji-description | Robot models: URDF, MJCF, MJX, USD, STEP for Hand 1, Hand 2.1, Hand 2.2 (left / right; bare, cover, glove variants) | MIT | [wuji-description](https://github.com/wuji-technology/wuji-description) | Simulation and planning without hardware; mechanical integration |
| ✅ wuji-retargeting | Code + sample recordings (e.g. Vision Pro replay file) | MIT | [wuji-retargeting](https://github.com/wuji-technology/wuji-retargeting) | Webcam / Vision Pro / glove to hand joint angles; superseded by SDK retargeting |
| ✅ wuji-hand-teleop | Code: ROS 2 teleop + data capture (Docker only, ROS 2 Humble) | MIT (vendored XRoboToolkit parts keep their own licences) | [wuji-hand-teleop](https://github.com/wuji-technology/wuji-hand-teleop) | Collecting arm + hand demonstrations as ROS 2 MCAP |
| ✅ wuji-mujoco / mujoco-sim / isaaclab-sim | Minimal sim demos (load, control, replay a recorded trajectory) | Apache-2.0 (wuji-mujoco) | [wuji-mujoco](https://github.com/wuji-technology/wuji-mujoco) | First smoke test in simulation |
| MoCap Pen-Spin Dataset (paper) | Dataset described in the paper: 32 demonstrations | see the two bundles above | [paper appendix A.4](https://arxiv.org/html/2606.16272v2) | Reference only; the downloadable form is the bundles above |
| Benchmarks | none released | — | — | — |

Correction to the first-pass profile: trained RL checkpoints **are** published (inside the wuji-mjlab release bundle); what is still missing is any WUJI VLA / foundation-model checkpoint.

## Third-party papers using their hardware or software

**No third-party paper that uses a Wuji Hand, Wuji Glove or the WUJI software stack could be confirmed in this pass.** The search budget ran out before the hunt, and the pages that were opened (TopoRetarget reference list, upstream mjlab research page, SPIDER and dex-retargeting READMEs) name no such paper. The mjlab project lists `wuji-technology/wuji-mjlab` among community projects, which is a code listing, not a paper. Ask WUJI staff on site for customer publications.

The table below is therefore the **verified research the WUJI stack is built on or interoperates with** (opened on arXiv; none of these used Wuji hardware):

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [mjlab: A Lightweight Framework for GPU-Accelerated Robot Learning](https://arxiv.org/abs/2601.22074) | Zakka, Liao, Yi, Le Lay, Sreenath, Abbeel | arXiv, 2026 | Base framework of `wuji-mjlab` (MuJoCo Warp + Isaac-Lab-style API) | How the manager-based RL environments WUJI extends are structured | — |
| [Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning](https://arxiv.org/abs/2511.04831) | NVIDIA (Mittal et al.) | arXiv, 2025 | Base framework of `wuji-isaaclab` | Reference for the Isaac Lab task and sensor model | — |
| [pi0: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164) | Black et al., Physical Intelligence | RSS 2025 | Model fine-tuned by `wuji-openpi` | Flow-matching VLA with action chunks; base of the WUJI fine-tuning path | T01 T03 T04 |
| [pi0.5: a Vision-Language-Action Model with Open-World Generalization](https://arxiv.org/abs/2504.16054) | Physical Intelligence | arXiv, 2025 | Default model of `pi05_wuji_multi_54d` | Household tasks in unseen homes; the checkpoint WUJI's reference config starts from | T01 T04 |
| [DexPilot: Vision Based Teleoperation of Dexterous Robotic Hand-Arm System](https://arxiv.org/abs/1910.03135) | Handa et al., NVIDIA | ICRA 2020 | Credited by `wuji-retargeting`; baseline in TopoRetarget | Key-vector retargeting cost that most hand teleop still uses | T02 T04 |
| [AnyTeleop: A General Vision-Based Dexterous Robot Arm-Hand Teleoperation System](https://arxiv.org/abs/2307.04577) | Qin et al., UCSD / NVIDIA | RSS 2023 | Source of `dex-retargeting`, credited by `wuji-retargeting` | Camera-only arm + hand teleop across hand models | T02 T04 |
| [OmniRetarget: Interaction-Preserving Data Generation for Humanoid Whole-Body Loco-Manipulation and Scene Interaction](https://arxiv.org/abs/2509.26633) | Yang et al. | arXiv, 2025 | Interaction-mesh idea TopoRetarget adapts to hands; baseline | Interaction-preserving retargeting at whole-body scale | — |
| [Geometric Retargeting: A Principled, Ultrafast Neural Hand Retargeting Algorithm](https://arxiv.org/abs/2503.07541) | Yin et al. | IROS 2025 | Baseline in TopoRetarget | 1 kHz learned retargeting for teleop | T02 |
| [SPIDER: Scalable Physics-Informed Dexterous Retargeting](https://arxiv.org/abs/2511.09484) | Pan et al. | arXiv, 2025 | Related work cited by TopoRetarget (its repo covers Allegro, XHand, Inspire, Schunk, Sharpa — not Wuji) | Physics-based sampling to make human demos dynamically feasible | — |
| [Lessons from Learning to Spin "Pens"](https://arxiv.org/abs/2407.18902) | Wang et al., UCSD / UC Berkeley | CoRL 2024 | Prior work for the pen-spin task | What makes pen spinning transfer from sim to real | — |
| [HO-Cap: A Capture System and Dataset for 3D Reconstruction and Pose Tracking of Hand-Object Interaction](https://arxiv.org/abs/2406.06843) | Wang et al. | arXiv, 2024 | Evaluation data in TopoRetarget | Grasp-centric hand-object clips usable as references | T04 |
| [ContactPose: A Dataset of Grasps with Object Contact and Hand Pose](https://arxiv.org/abs/2007.09545) | Brahmbhatt et al. | ECCV 2020 | Contact benchmark in TopoRetarget | Measured contact maps for functional grasps of household objects | T04 |
| [GRAB](https://arxiv.org/abs/2008.11200) · [TACO](https://arxiv.org/abs/2401.08399) · [OAKINK2](https://arxiv.org/abs/2403.19417) · [HOT3D](https://arxiv.org/abs/2406.09598) | Taheri et al. · Liu et al. · Zhan et al. · Banerjee et al. | ECCV 2020 · arXiv 2024 · CVPR 2024 · arXiv 2024 | Public motion sources with importers in `toporetarget` | Thousands of human hand-object clips (tools, kitchen, daily objects) you can retarget to Wuji Hand 2; each keeps its own licence (HOT3D is non-commercial) | T01 T03 T04 |
| [DexCap: Scalable and Portable Mocap Data Collection System for Dexterous Manipulation](https://arxiv.org/abs/2403.07788) | Wang et al., Stanford | arXiv, 2024 | Related work cited by TopoRetarget | Glove-based in-the-wild data collection, the same idea as the Wuji Glove data loop | T02 T04 |

## Reading list by track

No paper applies WUJI devices to a track task directly; the lists below are the shortest route from the confirmed research to a 48-hour build.

### T01 Autonomous Urban Services
- [pi0.5](https://arxiv.org/abs/2504.16054) — the model `wuji-openpi` fine-tunes; read with the [wuji-openpi README](https://github.com/wuji-technology/wuji-openpi) to judge whether a few dozen teleop demos of a service task (hand over, press, open) are feasible in the time.
- [pi0](https://arxiv.org/abs/2410.24164) — explains action chunking and why the fork adds chunk-boundary smoothing.
- [AnyTeleop](https://arxiv.org/abs/2307.04577) — camera-only teleop; the fallback if no glove is free.
- [TopoRetarget](https://arxiv.org/abs/2606.16272) — only if you plan to script a contact-rich hand skill from a recorded human demo.

### T02 Resilient & Safe City
- [DexPilot](https://arxiv.org/abs/1910.03135) — the retargeting cost behind glove-to-hand teleoperation; helps when tuning pinch and thumb behaviour for valves and switches.
- [AnyTeleop](https://arxiv.org/abs/2307.04577) — system design for remote arm + hand operation, including latency handling.
- [Geometric Retargeting](https://arxiv.org/abs/2503.07541) — fast learned alternative if the built-in retargeting feels wrong for a tool grasp.
- [DexCap](https://arxiv.org/abs/2403.07788) — portable glove data collection, useful for logging operator demonstrations in the field.
- [TopoRetarget](https://arxiv.org/abs/2606.16272) — contact-preserving mapping when the operator handles an object rather than free space.

### T03 Sustainable City
No directly relevant paper found (nothing on sorting, disassembly or environmental tasks with WUJI devices). Closest useful reading:
- [pi0](https://arxiv.org/abs/2410.24164) / [pi0.5](https://arxiv.org/abs/2504.16054) with [wuji-openpi](https://github.com/wuji-technology/wuji-openpi) — learn a pick-and-sort skill from teleop demos instead of hand-coding grasps.
- [TACO](https://arxiv.org/abs/2401.08399) and [OAKINK2](https://arxiv.org/abs/2403.19417) — tool-use and multi-step human clips that `toporetarget` can import, for unscrewing or dismantling motions.

### T04 Elderly Care & Rehabilitation
No directly relevant paper found (no rehabilitation, assistive or clinical study using the Wuji Glove or Hand was confirmed). Closest useful reading:
- [ContactPose](https://arxiv.org/abs/2007.09545) — reference contact maps of functional grasps; a comparison target for glove tactile maps in a grip-assessment demo.
- [HO-Cap](https://arxiv.org/abs/2406.06843) and [GRAB](https://arxiv.org/abs/2008.11200) — everyday-object grasp motions (cups, bottles, utensils) to retarget for assistive fetch or feeding.
- [TopoRetarget](https://arxiv.org/abs/2606.16272) — shows the Wuji Glove used as a capture device and the pipeline from caregiver demo to robot hand motion.
- [pi0.5](https://arxiv.org/abs/2504.16054) — home-task generalisation, relevant to assistive manipulation in a living space.
- [AnyTeleop](https://arxiv.org/abs/2307.04577) — basis for a telepresence / remote-caregiver hand.

## White papers, patents and technical reports

- **Lecture notes:** [robotics-rigid-body-mechanics](https://github.com/wuji-technology/robotics-rigid-body-mechanics) — WUJI-published LaTeX notes on rotation, screw theory, dynamics and multibody systems (MIT; build the PDF yourself with XeLaTeX; includes Chinese-language packages).
- **Algorithm notes in docs:** the archived Wuji Retargeting docs have an appendix on algorithm principles and a tuning guide; the wuji-mjlab docs have an architecture page on the reorientation MDP and contact-parameter domain randomisation ([docs index](https://docs.wuji.tech/_llms/en.txt)).
- **White papers and patents:** none found or checked in this pass (patent databases were not searched) — not public / ⚠️ unverified.

## Sources

- [arXiv 2606.16272 — TopoRetarget (abstract)](https://arxiv.org/abs/2606.16272) · [HTML v2 (affiliations, appendix, references)](https://arxiv.org/html/2606.16272v2)
- [TopoRetarget project page](https://toporetarget2026.github.io/TopoRetarget/)
- [GitHub: wuji-technology/toporetarget](https://github.com/wuji-technology/toporetarget) · [releases](https://github.com/wuji-technology/toporetarget/releases) · [data README](https://github.com/wuji-technology/toporetarget/blob/main/data/README.md)
- [GitHub: wuji-technology/wuji-mjlab](https://github.com/wuji-technology/wuji-mjlab) · [release v2026.10.22](https://github.com/wuji-technology/wuji-mjlab/releases/tag/v2026.10.22)
- [GitHub: wuji-technology/wuji-isaaclab](https://github.com/wuji-technology/wuji-isaaclab)
- [GitHub: wuji-technology/wuji-openpi](https://github.com/wuji-technology/wuji-openpi)
- [GitHub: wuji-technology/wuji-retargeting](https://github.com/wuji-technology/wuji-retargeting)
- [GitHub: wuji-technology/wuji-hand-teleop](https://github.com/wuji-technology/wuji-hand-teleop)
- [GitHub: wuji-technology/wuji-description](https://github.com/wuji-technology/wuji-description)
- [GitHub: wuji-technology/wuji-mujoco](https://github.com/wuji-technology/wuji-mujoco)
- [GitHub: wuji-technology/robotics-rigid-body-mechanics](https://github.com/wuji-technology/robotics-rigid-body-mechanics)
- [GitHub organisation: wuji-technology](https://github.com/wuji-technology) (repository list and organisation profile)
- [Wuji Docs — English index](https://docs.wuji.tech/_llms/en.txt) · [Videos](https://docs.wuji.tech/docs/en/videos.md)
- [Wuji Technology official site](https://www.wuji.tech/en)
- [mjlab repository](https://github.com/mujocolab/mjlab) · [mjlab research page](https://mujocolab.github.io/mjlab/main/source/research.html)
- [SPIDER repository](https://github.com/facebookresearch/spider) · [dex-retargeting repository](https://github.com/dexsuite/dex-retargeting) (checked for Wuji support; none listed)
- arXiv abstract pages opened for verification: [2601.22074](https://arxiv.org/abs/2601.22074) · [2511.04831](https://arxiv.org/abs/2511.04831) · [2410.24164](https://arxiv.org/abs/2410.24164) · [2504.16054](https://arxiv.org/abs/2504.16054) · [1910.03135](https://arxiv.org/abs/1910.03135) · [2307.04577](https://arxiv.org/abs/2307.04577) · [2509.26633](https://arxiv.org/abs/2509.26633) · [2503.07541](https://arxiv.org/abs/2503.07541) · [2511.09484](https://arxiv.org/abs/2511.09484) · [2407.18902](https://arxiv.org/abs/2407.18902) · [2406.06843](https://arxiv.org/abs/2406.06843) · [2007.09545](https://arxiv.org/abs/2007.09545) · [2008.11200](https://arxiv.org/abs/2008.11200) · [2401.08399](https://arxiv.org/abs/2401.08399) · [2403.19417](https://arxiv.org/abs/2403.19417) · [2406.09598](https://arxiv.org/abs/2406.09598) · [2403.07788](https://arxiv.org/abs/2403.07788)
