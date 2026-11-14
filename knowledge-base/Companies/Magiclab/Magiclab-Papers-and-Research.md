---
type: papers
company: "Magiclab Robotics"
slug: Magiclab
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# Magiclab Robotics — Papers and Research

⬆ [Magiclab Robotics profile](Magiclab.md) · [Solutions and projects](Magiclab-Solutions-and-Projects.md) · [Developer guide](Magiclab-Developer-Guide.md)

> **Coverage note (read first).** This pass traced research from the company's own research portal (`embodied.magiclab.top`), the citation blocks of all 22 GitHub repositories, Hugging Face and the arXiv abstract pages. Every paper below was opened on arXiv. A general web search for **third-party** papers was not available in this run, so the third-party table is "none verified", not "proven none".

## Research footprint

- **Young but now publishing.** Founded January 2024; no papers found before autumn 2026. Between **30 Sep and 9 Oct 2026** the in-house "Magic-Lab Team, Magiclab Robotics Inc." posted **5 arXiv preprints** (all cs.RO, none peer-reviewed yet) plus 2 technical articles on a dedicated research portal.
- **Focus is the manipulation "brain", not locomotion.** Topics: a world-action foundation model (Magic-W0), real-time VLA execution, action-chunk consistency, memory for VLAs, an embodied agent framework (Magic-Brain) and a data-training-evaluation loop. No company paper on quadruped or humanoid locomotion, navigation or SLAM was found.
- **Key people (from the author lists).** **Tao Zhang** is project lead / corresponding author on all five papers. Recurring authors: Xuhua Chen, Lingfeng Zhang, Di Wu, Ping Liu, He Zheng, Zhenhan Yin, Rongtian Shen, Shun Zuo. Co-affiliations on individual papers: Zhejiang University, Southeast University, Harbin Institute of Technology, Tongji University, Jilin University, UCLA (these look like student / intern links, not formal lab partnerships ⚠️ unverified).
- **Important caveat for builders:** the real-robot experiments in these papers run on **AgileX Piper dual-arm** table-top setups (stated for Real-Time VLA, EAPN and Dual-Stream Memory; platform not named for Magic-W0 and CTP), **not on MagicBot or MagicDog**. The papers tell you how the company thinks about models; they are not robot-specific recipes.
- **Open-source posture: good and improving.** Magic-W0 ships code (MIT) **and weights** on Hugging Face; the real-time inference runtime is Apache-2.0. For its own robots the company publishes forks of well-known academic stacks (BeyondMimic, GMR, openpi/π0, Isaac Lab RL) adapted to MagicBot Z1 / Gen1. **Not released:** Magic-VLA K02, Magic-Mix, Magic-Brain code, any dataset.

## Company-authored and company-affiliated papers

All are arXiv preprints; author lists are taken from the arXiv abstract pages.

| Paper | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts (code / weights / data links) | Tracks |
|---|---|---|---|---|---|
| [Dual-Stream Memory for Vision-Language-Action Policies](https://arxiv.org/abs/2610.13262) | Yang Wang, Ping Liu, Ruiyu Wang, Xuhua Chen, Lingfeng Zhang, Tao Zhang — Magic-Lab Team, Magiclab Robotics Inc.; UCLA | arXiv 2610.13262, 9 Oct 2026 | Adds two memories to a π0.5 policy: one recurrent "where am I in the task" token plus retrieved past frames. **49.22%** vs 44.51% mean success on 16 RoboMME tasks; **62.5%** vs 37.5% on 4 real Piper tasks (repeat-count and hidden-object tasks). | [Project page](https://embodied.magiclab.top/works/memory/index.html) · no code link found | T04 T03 |
| [Conditional Trajectory Peaks: Single-Pass Multimodal Policies over Action Chunks](https://arxiv.org/abs/2610.06104) | Di Wu, Rongtian Shen, Ping Liu, Xuhua Chen, He Zheng, Lingfeng Zhang, Tao Zhang — Magiclab Robotics | arXiv 2610.06104, 5 Oct 2026 | One forward pass outputs several candidate action chunks with probabilities, instead of iterative denoising. LIBERO **97.25%**; real dual-arm tasks at π0.5-level success with policy latency cut from **218 ms to 76 ms**. | [Project page](https://embodied.magiclab.top/works/ctp/index.html) · no code link found | — (generic manipulation) |
| [Execution-Aligned Progressive Noise for Consistent Asynchronous Replanning in Generative Robot Policies](https://arxiv.org/abs/2610.06090) | Di Wu, Ping Liu, Xuhua Chen, He Zheng, Lingfeng Zhang, Tao Zhang — Magiclab Robotics | arXiv 2610.06090, 5 Oct 2026 | Carries the sampling noise across replans so a diffusion / flow policy does not "change its mind" between action chunks. Real Piper: **90.0%** object storage, **96.7%** bimanual cloth folding. | [Project page](https://embodied.magiclab.top/works/eapn/index.html) · no code link found | T04 (cloth folding, tidying) |
| [Magic-W0: A Structured World-Action Foundation Model for Physical Intelligence](https://arxiv.org/abs/2609.39870) | Xuhua Chen, Zhenhan Yin, Yuan Zhang, Lingfeng Zhang, He Zheng, Tong Mu, Shun Zuo, Dian Zhou, Di Wu, Xuan Zhou, Shaojie Wan, Rongtian Shen, Qiulong Xu, Yiduo Li, Yinglong Wang, Yanqian Wang, Kun Wang, Tao Zhang — Magic-Lab Team, Magiclab Robotics Inc. | arXiv 2609.39870, 30 Sep 2026 (v2 3 Oct) | The company's open foundation model: predicts 3D geometry, 3D motion and future semantics together with actions. Pre-trained on about **2.014M episodes** (egocentric human, UMI, real-robot, simulation) through one **34-D state-action interface**. Company-reported: LIBERO **99.05%**; **94.6%** vs π0.5 91.8% on 5 real tasks (100 trials each); RoboDojo-Sim average Score 27.10 in the arXiv abstract, **37.47** (rank 1 of 27 methods) on the later project page. | [Code, MIT](https://github.com/MagiclabRobotics/Magic-W0) · [Weights](https://huggingface.co/XuhuaX/Magic-W0) · [Project page](https://embodied.magiclab.top/works/wam/magic-w0/index.html) · no dataset | T03 T04 (generic manipulation: folding, storing, kitchen tidy-up) |
| [Toward Real-Time VLAs: Stage-Aware Two-Step Flow Denoising and System-Level Evaluation](https://arxiv.org/abs/2609.39822) | Di Wu, Rongtian Shen, Ping Liu, Yan Shen, Zhenhan Yin, Shun Zuo, Xuhua Chen, He Zheng, Lingfeng Zhang, Jianglin Zhang (printed as "Jiangning Zhang, Zhejiang University" inside the paper), Tao Zhang — Magiclab Robotics; Zhejiang U., Southeast U., HIT, Tongji U., Jilin U. | arXiv 2609.39822, 30 Sep 2026 (v2 3 Oct); technical report | Measures the whole camera-to-motion delay chain, cuts flow-matching denoising from 10 to **2 steps** (**61.6 ms to 22.0 ms**), and compares six real-time execution strategies on T-shirt folding (180 real trials; best: Legato **96.7%**, VLASH 93.3%, naive async 63.3%). | [Code, Apache-2.0](https://github.com/MagiclabRobotics/Inference) (runtime, mock tests, paper PDF) · [Project page (Chinese)](https://embodied.magiclab.top/works/inference/zh/index.html) | T04 (garment handling); useful to any track that runs a VLA |

Not found as papers: **Magic-VLA K02** and **Magic-Mix** (product-level announcements only, no paper, no weights). The "magicVLA" policy is referenced as the baseline in the Magic-Brain article below.

## Datasets, models and benchmarks released

No dataset and no benchmark has been released by the company. Models and research code:

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| Magic-W0 (code) | Training (pre-train + fine-tune) and inference code for the world-action model; RoboDojo adapter | MIT | [GitHub](https://github.com/MagiclabRobotics/Magic-W0) | Fine-tuning a manipulation policy on your own demos; needs Linux, Python 3.11, NVIDIA GPU |
| Magic-W0 (weights) | Pre-trained checkpoint + RoboDojo fine-tuned checkpoint (released 30 Oct 2026) | MIT for the model; bundled teacher models keep their own terms (Track4World is academic-use only, DINOv3 has its own licence) | [Hugging Face](https://huggingface.co/XuhuaX/Magic-W0) (hosted on the first author's personal account) | Starting point for fine-tuning; **not** a plug-and-play policy for MagicBot or MagicDog |
| Inference | Distributed real-time VLA runtime (policy server + robot client, WebSocket or shared memory, JAX / TensorRT), 7 execution modes | Apache-2.0 | [GitHub](https://github.com/MagiclabRobotics/Inference) | Running an openpi-style policy at low rate while the robot is commanded at high rate; client is written for AgileX Piper, has hardware-free mock tests |
| magicbot-gen1_pi0_demo | π0 (openpi) data conversion, training and evaluation pipeline for dual-arm dexterous manipulation on MagicBot Gen1 | Apache-2.0 | [GitHub](https://github.com/MagiclabRobotics/magicbot-gen1_pi0_demo) | The only published VLA recipe for a MagicLab robot (HDF5 to LeRobot v2.0, then openpi training) |
| pico_teleoperate | PICO 4 Ultra whole-body teleoperation for MagicBot Gen1 | BSD-3-Clause | [GitHub](https://github.com/MagiclabRobotics/pico_teleoperate) | Collecting demonstrations; T02 / T04 teleoperation demos |
| magicbot-mimic | BeyondMimic motion-tracking training stack ported to MagicBot Z1 (23 DoF), Isaac Lab + MuJoCo sim-to-sim; includes one sample motion file | MIT | [GitHub](https://github.com/MagiclabRobotics/magicbot-mimic) | Teaching Z1 a whole-body motion (gesture, dance, reach) |
| Magiclab_GMR | General Motion Retargeting fork for MagicBot Z1 (24 driven joints; robot ID in code is `dreame_z1`); BVH / SMPL-X to robot trajectory | MIT | [GitHub](https://github.com/MagiclabRobotics/Magiclab_GMR) | Turning human motion capture into Z1 reference motions |
| magiclab_rl_lab | Isaac Lab (2.3.0) RL environments; currently Z1 12-DoF velocity task | Apache-2.0 | [GitHub](https://github.com/MagiclabRobotics/magiclab_rl_lab) | Training a custom locomotion policy |
| magiclab_mujoco | MuJoCo sim-to-sim runner for Z1 12-DoF | none stated | [GitHub](https://github.com/MagiclabRobotics/magiclab_mujoco) | Checking a policy before real deployment |
| magiclab_deploy | Low-level ONNX policy deployment on a real Z1 (state machine, keyboard / gamepad) | none stated | [GitHub](https://github.com/MagiclabRobotics/magiclab_deploy) | Sim-to-real for RL policies; switches the robot to low-level mode, so use with care |
| Robot descriptions (Z1, Gen1, MagicDog, MagicDog-W) | URDF / MJCF models | BSD-3-Clause | [GitHub org](https://github.com/MagiclabRobotics) | Simulation, motion planning, digital-twin visualisation |

## Third-party papers using their hardware or software

| Paper (link) | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| None verified | — | — | — | No independent paper using MagicBot, MagicDog or MagicLab software could be confirmed in this run (web search unavailable; the company only began selling in May 2025, so few are expected). | — |

### Upstream papers that MagicLab's open-source repos port to its robots

These are **not** MagicLab papers and do not use MagicLab hardware in the original work. They are listed because the company's own repositories implement them for MagicBot Z1 / Gen1, so they are the real "how it works" reading. All opened on arXiv.

| Paper (link) | Authors / organisation | Venue, year | MagicLab repo that uses it | What it gives you | Tracks |
|---|---|---|---|---|---|
| [BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion](https://arxiv.org/abs/2508.08241) | Liao, Truong, Huang, Gao, Tevet, Sreenath, Liu (UC Berkeley / Stanford) | arXiv, Aug 2025 | `magicbot-mimic` | Robust tracking of dynamic human motions on a humanoid | T01 T04 (expressive / gesture behaviours) |
| [Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking](https://arxiv.org/abs/2510.02252) | Araujo, Ze, Xu, Wu, Liu (Stanford) | arXiv, Oct 2025 | `Magiclab_GMR` | Clean human-to-humanoid motion retargeting | T04 (demonstrating exercises), T01 |
| [TWIST: Teleoperated Whole-Body Imitation System](https://arxiv.org/abs/2505.02833) | Ze, Chen, Araújo, Cao, Peng, Wu, Liu (Stanford / SFU) | arXiv, May 2025 | cited by `Magiclab_GMR` | Whole-body humanoid teleoperation from motion capture | T02 T04 (teleoperation, telepresence) |
| [π0: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164) | Black, Brown, Driess, Esmail, Equi, Finn et al. (Physical Intelligence) | arXiv, Oct 2024 | `magicbot-gen1_pi0_demo` | The VLA that MagicLab's Gen1 demo fine-tunes | T01 T03 T04 |
| [π0.5: a Vision-Language-Action Model with Open-World Generalization](https://arxiv.org/abs/2504.16054) | Physical Intelligence | arXiv, Apr 2025 | baseline in all five MagicLab papers; default policy config in `Inference` | The baseline every MagicLab result is measured against | T01 T03 T04 |

## Reading list by track

### T01 Autonomous Urban Services
- [In-Context Visual Guidance with Magic-Brain](https://embodied.magiclab.top/works/brain/en.html) (company article) — describes an agent stack with separate **navigation, grasping, interaction and "sentinel" agents**, a task DAG with re-planning, and pause / abort / e-stop buses; a ready-made architecture sketch for a concierge or delivery robot.
- [π0](https://arxiv.org/abs/2410.24164) with the [`magicbot-gen1_pi0_demo`](https://github.com/MagiclabRobotics/magicbot-gen1_pi0_demo) repo — the documented way to teach a MagicLab humanoid a service manipulation skill from teleoperated demos.
- [BeyondMimic](https://arxiv.org/abs/2508.08241) — if you want Z1 to wave, point or greet convincingly in a guide-robot demo.
- No company paper on navigation, SLAM or delivery was found; use the ROS 2 SDK docs instead (see the [Developer guide](Magiclab-Developer-Guide.md)).

### T02 Resilient & Safe City
No directly relevant paper found (nothing on inspection, patrol, search and rescue, mapping or legged locomotion). Closest useful items:
- [TWIST](https://arxiv.org/abs/2505.02833) plus the [`pico_teleoperate`](https://github.com/MagiclabRobotics/pico_teleoperate) repo — background and tooling for a hazardous-environment teleoperation demo on a humanoid.
- [Toward Real-Time VLAs](https://arxiv.org/abs/2609.39822) — its latency-measurement method (camera, network, robot response) transfers directly to judging whether a teleoperation or remote-inference link is fast enough.

### T03 Sustainable City
- [In-Context Visual Guidance with Magic-Brain](https://embodied.magiclab.top/works/brain/en.html) — a VLM draws the target and the drop zone onto the camera image as coloured masks; pick-and-place success rose from **41% to 84.7%** on MolmoSpaces-Bench. This is the most copyable idea for a **waste-sorting** demo: let a VLM decide "which item, which bin" and keep the low-level policy simple.
- [Magic-W0](https://arxiv.org/abs/2609.39870) — open weights and fine-tuning code for a pick / store / sort policy, if you have a GPU and can collect demos.
- [Dual-Stream Memory](https://arxiv.org/abs/2610.13262) — relevant when sorting needs counting or remembering what was already handled.
- No paper on energy, environmental monitoring or low-power edge AI was found. The two-step denoising result in [Toward Real-Time VLAs](https://arxiv.org/abs/2609.39822) (about 2.8 times faster model inference) is the nearest thing to an efficiency contribution.

### T04 Elderly Care & Rehabilitation
- [Toward Real-Time VLAs](https://arxiv.org/abs/2609.39822) — long-horizon **garment folding** with honest per-method success rates and open runtime code; shows which execution strategy to pick (Legato or VLASH, not naive async) for smooth motion near people.
- [Execution-Aligned Progressive Noise](https://arxiv.org/abs/2610.06090) — why generative policies jerk or switch plan mid-task, and one fix; smoothness matters for assistive use.
- [Magic-W0](https://arxiv.org/abs/2609.39870) — household tasks (clothes folding, object storage, kitchen storage, pen storage) at about 95% success after fine-tuning, company-reported.
- [Dual-Stream Memory](https://arxiv.org/abs/2610.13262) — tasks that need "have I already done this?" (for example, a medication-count or repeat-exercise step).
- [Retargeting Matters (GMR)](https://arxiv.org/abs/2510.02252) with [`Magiclab_GMR`](https://github.com/MagiclabRobotics/Magiclab_GMR) and [`magicbot-mimic`](https://github.com/MagiclabRobotics/magicbot-mimic) — the route to having Z1 **demonstrate a physiotherapy movement** recorded from a human.
- No company paper on elder care, rehabilitation, fall detection or human-safety evaluation was found.

## White papers, patents and technical reports

| Item | Type | Date | What it says | Link |
|---|---|---|---|---|
| In-Context Visual Guidance with Magic-Brain | Company technical article (no arXiv, no code; source document downloadable) | 2026 (also listed in official site news) | Visual prompting layer in front of the "magicVLA" policy: VLM agent outputs a box, a segmentation model refines it, a three-colour mask (target / place zone / fading history) is drawn on the image, and the VLA is post-trained to follow it. MolmoSpaces-Bench: pick **70% to 94.4%**, pick-and-place **41% to 84.7%**. Also outlines the Magic-Brain agent framework (apps, gateway, agent_core). | [English](https://embodied.magiclab.top/works/brain/en.html) |
| Embodied RSI — From Evaluation to Training: the RoboDojo data-training-evaluation loop | Company technical article | 2026 | Frame-level failure diagnosis from a **2-hour** full RoboDojo evaluation feeds a Data Agent (inspect, repair, annotate trajectories) and a Training Agent (sampling and recipe changes). Process description; no code or numbers beyond that. | [English](https://embodied.magiclab.top/works/embodied-rsi/en.html) |
| EmbodiedModel research portal | Index of all the above (Brain, WAM, Inference, Embodied RSI, Memory) | live Nov 2026 | Single entry point for MagicLab research pages. | [Portal (Chinese / English toggle)](https://embodied.magiclab.top/) |

Context papers the Magic-Brain article builds on (opened on arXiv): [VP-VLA: Visual Prompting as an Interface for Vision-Language-Action Models](https://arxiv.org/abs/2603.22003), [In-Context VLA](https://arxiv.org/abs/2608.05738), and the benchmark [MolmoSpaces](https://arxiv.org/abs/2602.11337).

Patents: not checked in this run ⚠️ unverified. RoboDojo, RoboMME and LIBERO are third-party benchmarks used by the company, not released by it (RoboDojo's origin was not checked ⚠️ unverified).

## Sources
- [EmbodiedModel — MagicLab research portal](https://embodied.magiclab.top/)
- [Magic-W0 project page](https://embodied.magiclab.top/works/wam/magic-w0/index.html)
- [Real-Time VLA project page (Chinese)](https://embodied.magiclab.top/works/inference/zh/index.html)
- [EAPN project page](https://embodied.magiclab.top/works/eapn/index.html)
- [CTP project page](https://embodied.magiclab.top/works/ctp/index.html)
- [Dual-Stream Memory project page](https://embodied.magiclab.top/works/memory/index.html)
- [Magic-Brain article (English)](https://embodied.magiclab.top/works/brain/en.html)
- [Embodied RSI article (English)](https://embodied.magiclab.top/works/embodied-rsi/en.html)
- [arXiv 2609.39870 — Magic-W0](https://arxiv.org/abs/2609.39870)
- [arXiv 2609.39822 — Toward Real-Time VLAs](https://arxiv.org/abs/2609.39822)
- [arXiv 2610.06090 — Execution-Aligned Progressive Noise](https://arxiv.org/abs/2610.06090)
- [arXiv 2610.06104 — Conditional Trajectory Peaks](https://arxiv.org/abs/2610.06104)
- [arXiv 2610.13262 — Dual-Stream Memory](https://arxiv.org/abs/2610.13262)
- [arXiv 2508.08241 — BeyondMimic](https://arxiv.org/abs/2508.08241)
- [arXiv 2510.02252 — General Motion Retargeting](https://arxiv.org/abs/2510.02252)
- [arXiv 2505.02833 — TWIST](https://arxiv.org/abs/2505.02833)
- [arXiv 2410.24164 — π0](https://arxiv.org/abs/2410.24164)
- [arXiv 2504.16054 — π0.5](https://arxiv.org/abs/2504.16054)
- [arXiv 2603.22003 — VP-VLA](https://arxiv.org/abs/2603.22003)
- [arXiv 2608.05738 — In-Context VLA](https://arxiv.org/abs/2608.05738)
- [arXiv 2602.11337 — MolmoSpaces](https://arxiv.org/abs/2602.11337)
- [GitHub — MagiclabRobotics organisation (22 repositories)](https://github.com/MagiclabRobotics)
- [GitHub — Magic-W0](https://github.com/MagiclabRobotics/Magic-W0)
- [GitHub — Inference](https://github.com/MagiclabRobotics/Inference)
- [GitHub — magicbot-gen1_pi0_demo](https://github.com/MagiclabRobotics/magicbot-gen1_pi0_demo)
- [GitHub — pico_teleoperate](https://github.com/MagiclabRobotics/pico_teleoperate)
- [GitHub — magicbot-mimic](https://github.com/MagiclabRobotics/magicbot-mimic)
- [GitHub — Magiclab_GMR](https://github.com/MagiclabRobotics/Magiclab_GMR)
- [GitHub — magiclab_rl_lab](https://github.com/MagiclabRobotics/magiclab_rl_lab)
- [GitHub — magiclab_mujoco](https://github.com/MagiclabRobotics/magiclab_mujoco)
- [GitHub — magiclab_deploy](https://github.com/MagiclabRobotics/magiclab_deploy)
- [Hugging Face — XuhuaX/Magic-W0](https://huggingface.co/XuhuaX/Magic-W0)
- [MagicLab — Open source page](https://www.magiclab.top/en/opensource)
- [MagicLab — News](https://www.magiclab.top/en/news)
