---
type: papers
company: "AGIBOT"
slug: AGIBOT
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# AGIBOT — Papers and Research

⬆ [AGIBOT profile](AGIBOT.md) · [Solutions and projects](AGIBOT-Solutions-and-Projects.md) · [Developer guide](AGIBOT-Developer-Guide.md)

> **Method note (read once):** every paper below was opened on arXiv (abstract page plus HTML full text) on 2026-11-14; titles, authors, dates and the AGIBOT link (affiliation, hardware or dataset use) come from those pages. Discovery ran through the AgibotTech GitHub organisation, the `agibot-world` Hugging Face organisation and the OpenDriveLab publication list. **General web search was not available in this run**, and `agibot.com/research` is a JavaScript-rendered page that could not be read — so the list is verified but **probably not exhaustive** (see "Known gaps").

## Research footprint

- **Heavily research-driven for a robot maker.** At least **18 verified papers** since January 2025 from three in-house groups that sign as **"AgiBot Genie Team"** (world models, VLA), **"AgiBot Research"** (online post-training, reasoning; senior author Jianlan Luo) and **"AgiBot Yuanzheng Research Team"** (lifelong agents). Recurring senior / corresponding authors: **Maoqing Yao** and **Guanghui Ren**. Co-founder **Peng Zhihui** appears as co-author on WholeBodyVLA.
- **Main academic partner: OpenDriveLab / MMLab at the University of Hong Kong (Hongyang Li).** It co-produced AgiBot World, GO-1, UniVLA and WholeBodyVLA and hosts the GO-1 code. Other repeat partners: Beihang University (Si Liu), LV-NUS Lab (Shuicheng Yan), CUHK MMLab (Hongsheng Li), Shanghai AI Laboratory, HKUST, Fudan, SJTU.
- **Four research lines**, each tied to a product: (1) data — AgiBot World datasets → Genie Studio; (2) VLA policies — GO-1, ACoT-VLA, GenieReasoner → GO series; (3) video world models — EnerVerse → Genie Envisioner → GE-Sim 2.0; (4) real-world improvement loops — Genie Centurion, SOP, ALOE, VINE → fleet post-training.
- **Open-source posture: strong on data, sim and research code; restrictive on licence.** Datasets, world models and GO-1 are public but mostly **CC BY-NC-SA 4.0 (non-commercial)**; Genie Sim code is **MPL-2.0**; the X1 humanoid is fully open (hardware + RL code). Production models (GO-2, GO-3, locomotion and interaction models) are **not** published as papers or weights as far as this pass could confirm.
- **Almost all published work is tabletop / mobile manipulation on the G1 and G2 wheeled dual-arm robots.** Only one verified paper uses the X2 humanoid; **none** covers the D1 quadrupeds, the C5 cleaning robot, outdoor navigation, inspection, or elder care.

## Company-authored and company-affiliated papers

Newest first. "Affiliated" = AGIBOT staff among the authors. Venue is "arXiv" unless a conference is stated on the arXiv page or the lab's publication list.

| Paper | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts | Tracks |
|---|---|---|---|---|---|
| [Learning to Live: A Step Toward Lifelong Embodied Intelligence](https://arxiv.org/abs/2611.00180) | Lirong Che, Peidong Wang, Yimeng Su … Jian Su (15 authors) — AgiBot Yuanzheng Research Team | arXiv, Oct 2026 | **LIFE** framework: a small streaming VLM gate (**RoboBeats**, 1 fps) decides when something worth reacting to or remembering happens; "Plastic Memory" stores evidence; Explore-Distill-Mount turns solved problems into reusable tools. Case study replays **24 h** of robot video | [Code](https://github.com/AgibotTech/LIFE) · RoboBeats weights 0.8B / 2B / 4B (LoRA on Qwen3.5) · SSS-Bench · local webcam demo | T01 T02 T04 |
| [VINE: Taming Generative Control Policies for Reinforcement Learning](https://arxiv.org/abs/2607.10369) | Rushuai Yang, Zhuo Han, Houlin Li … Wei Shan, Maoqing Yao (13) — AgiBot, HKUST | arXiv, Jul 2026 | Sampling method that makes value-gradient RL stable for flow-matching policies; tested on OGBench and a real manipulation task | [Project page](https://agibottech.github.io/vine) · `vine-code` repo exists in the org (content not checked) | — |
| [GE-Sim 2.0: A Roadmap Towards Comprehensive Closed-loop Video World Simulators for Robotic Manipulation](https://arxiv.org/abs/2605.27491) | Boxiang Qiu, Liliang Chen, Yue Liao … Maoqing Yao, Guanghui Ren (15) — AgiBot, BUAA, LV-NUS Lab, TJU | arXiv, May 2026 | Closed-loop video world simulator: state expert, "world judge" that scores rollouts, **25-frame rollout in 2.3 s** on one H100; reported top of the WorldArena leaderboard at 2B parameters | [Code](https://github.com/AgibotTech/GE-Sim-V2) · [weights](https://huggingface.co/agibot-world/Genie-Envisioner-Sim-v2.0) | — |
| [ALOE: Action-Level Off-Policy Evaluation for Vision-Language-Action Model Post-Training](https://arxiv.org/abs/2602.12691) | Rushuai Yang, Hecheng Wang, Zhichao Wu … Wei Shan, Maoqing Yao (14) — AgiBot, HKUST, Fudan | arXiv, Feb 2026 | Human-in-the-loop RL for VLAs with a value function that evaluates the *current* policy; real tasks include smartphone packing, laundry folding and multi-object sorting | Project page repo `AgibotTech/aloe` (page only) | T03 |
| [ACoT-VLA: Action Chain-of-Thought for Vision-Language-Action Models](https://arxiv.org/abs/2601.11404) | Linqing Zhong, Yi Liu, Yifei Wei, Ziyu Xiong, Maoqing Yao, Si Liu, Guanghui Ren — Beihang, AgiBot | **CVPR 2026** | Reasoning directly in action space (coarse action "thoughts" guide the final action). Real tests on **AgiBot G1**: wipe stain, pour water, open-set pick. Reported by trade press as the idea behind GO-2 | [Code](https://github.com/AgibotTech/ACoT-VLA) (README links the ICRA 2026 Reasoning-to-Action challenge data) | T01 T03 T04 |
| [SOP: A Scalable Online Post-Training System for Vision-Language-Action Models](https://arxiv.org/abs/2601.03044) | Mingjie Pan, Siyuan Feng, Qinglin Zhang … Jianlan Luo (12) — Agibot Research | arXiv, Jan 2026 | Fleet learning: many robots stream on-policy experience and human corrections to a cloud learner and get updated policies back. Tested with a **fleet of G1 robots** on grocery restocking, laundry folding, box assembly; gains within hours | [Research page](https://www.agibot.com/research/sop) (no public code found) | T01 T03 T04 |
| [Genie Sim 3.0: A High-Fidelity Comprehensive Simulation Platform for Humanoid Robot](https://arxiv.org/abs/2601.02078) | Chenghao Yin, Da Huang, Di Yang … Maoqing Yao (19) — AgiBot | arXiv, Jan 2026 | LLM-driven scene generator, 3DGS reconstruction, LLM/VLM-automated benchmark, **10,000+ h** synthetic data over **200+ tasks** on G1 and G2; zero-shot sim-to-real validated | [Code](https://github.com/AgibotTech/genie_sim) · [assets](https://huggingface.co/datasets/agibot-world/GenieSimAssets) · [dataset](https://huggingface.co/datasets/agibot-world/GenieSim3.0-Dataset) | T01 T02 T03 T04 |
| [Unified Embodied VLM Reasoning with Robotic Action via Autoregressive Discretized Pre-training](https://arxiv.org/abs/2512.24125) | Yi Liu, Sukai Wang, Dafeng Wei … Jianlan Luo (13) — AgiBot Research | arXiv, Dec 2025 | **GenieReasoner**: joint reasoning + action model; **ERIQ** benchmark (**6K+** embodied-reasoning QA pairs); **FACT** flow-matching action tokenizer. Real tests on G1 vs π0, π0.5, GR00T | none confirmed | T01 T04 |
| [WholeBodyVLA: Towards Unified Latent VLA for Whole-Body Loco-Manipulation Control](https://arxiv.org/abs/2512.11047) | Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi … Zhihui Peng, Hongyang Li (11) — Fudan, OpenDriveLab / HKU, AgiBot | **ICLR 2026** | Humanoid walks *and* manipulates from one VLA: latent actions learned from egocentric human video + a loco-manipulation RL controller. Verified on the **AgiBot X2**, **+21.3%** over the prior baseline | [Repo](https://github.com/OpenDriveLab/WholebodyVLA) (content not checked) | T01 T04 |
| [Genie Envisioner: A Unified World Foundation Platform for Robotic Manipulation](https://arxiv.org/abs/2508.05635) | Yue Liao, Pengfei Zhou, Siyuan Huang … Maoqing Yao, Guanghui Ren (14) — AgiBot Genie Team, LV-NUS Lab, BUAA | arXiv, Aug 2025 | One video-diffusion backbone for policy (**GE-Act**), simulation (**GE-Sim**) and evaluation; trained on AgiBot World Beta; cross-embodiment tests incl. Agilex Cobot Magic | [Code](https://github.com/AgibotTech/Genie-Envisioner) · [weights](https://huggingface.co/agibot-world/Genie-Envisioner-v1.0) | — |
| [Is Diversity All You Need for Scalable Robotic Manipulation?](https://arxiv.org/abs/2507.06219) | Modi Shi, Li Chen, Jin Chen, Yuxiang Lu, Chiming Liu, Guanghui Ren, Ping Luo, Di Huang, Maoqing Yao, Hongyang Li — HKU, AgiBot, Beihang | arXiv, Jul 2025 ("GO-1-Pro") | Data-scaling study: task diversity beats per-task quantity; single-embodiment data transfers well; a velocity-debiasing step gives **+15%** (equal to 2.5× more pre-training data) | [Repo](https://github.com/OpenDriveLab/AgiBot-World) | — |
| [Hume: Introducing System-2 Thinking in Visual-Language-Action Model](https://arxiv.org/abs/2505.21432) | Haoming Song, Delin Qu … Modi Shi, Guanghui Ren, Maoqing Yao … Xuelong Li (12) — Shanghai AI Laboratory, AgiBot | arXiv, May 2025 | Dual-system VLA that samples several candidate actions and picks by estimated value; tested on WidowX, Franka and **AgiBot G-1** | none checked | T01 T04 |
| [Genie Centurion: Accelerating Scalable Real-World Robot Training with Human Rewind-and-Refine Guidance](https://arxiv.org/abs/2505.18793) | Wenhao Wang, Jianheng Song, Chiming Liu … Maoqing Yao (16) — all AgiBot | arXiv, May 2025 | Data collection during deployment: robot rewinds after a failure, a human corrects; one operator supervises several robots via a "Task Sentinel". **Up to 40%** higher success, under half the data | none confirmed | T01 T03 |
| [EnerVerse-AC: Envisioning Embodied Environments with Action Condition](https://arxiv.org/abs/2505.09723) | Yuxin Jiang, Shengcong Chen, Siyuan Huang … Maoqing Yao, Guanghui Ren (11) — AgiBot, SJTU, MMLab-CUHK | arXiv, May 2025 | Action-conditioned world model (EVAC) used as a neural simulator for policy testing; trained incl. failure trajectories | [Code](https://github.com/AgibotTech/EnerVerse-AC) · [weights](https://huggingface.co/agibot-world/EnerVerse-AC) | — |
| [EWMBench: Evaluating Scene, Motion, and Semantic Quality in Embodied World Models](https://arxiv.org/abs/2505.09694) | Yue Hu, Siyuan Huang, Yue Liao, Shengcong Chen, Pengfei Zhou, Liliang Chen, Maoqing Yao, Guanghui Ren — AgiBot, SJTU, MMLab-CUHK | arXiv, May 2025 | Benchmark + metrics for video world models on robot tasks (scene consistency, motion, semantics) | [Code](https://github.com/AgibotTech/EWMBench) · [data](https://huggingface.co/datasets/agibot-world/EWMBench) · [model](https://huggingface.co/agibot-world/EWMBench-model) | — |
| [UniVLA: Learning to Act Anywhere with Task-centric Latent Actions](https://arxiv.org/abs/2505.06111) | Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, Hongyang Li — HKU, OpenDriveLab, AgiBot | **RSS 2025** | Cross-embodiment VLA that learns task-centric latent actions from video (incl. human video), so little labelled robot data is needed | [Code](https://github.com/OpenDriveLab/UniVLA) | T01 |
| [AgiBot World Colosseo: A Large-scale Manipulation Platform for Scalable and Intelligent Embodied Systems](https://arxiv.org/abs/2503.06669) | Team AgiBot-World — 50+ contributors, alphabetical (Qingwen Bu, Jisong Cai, Li Chen … Jianchao Zhu); AgiBot + OpenDriveLab | **IROS 2025** (Best Paper Finalist per OpenDriveLab) | The foundation paper: **1M+ trajectories, 217 tasks, 5 scenarios**, collected on about 100 G1 robots; introduces **GO-1** (latent-action generalist policy); **+30%** vs pre-training on Open X-Embodiment | [Repo](https://github.com/OpenDriveLab/AgiBot-World) · [HF org](https://huggingface.co/agibot-world) · GO-1 weights | T01 T03 T04 |
| [EnerVerse: Envisioning Embodied Future Space for Robotics Manipulation](https://arxiv.org/abs/2501.01895) | Siyuan Huang, Liliang Chen, Pengfei Zhou … Maoqing Yao, Guanghui Ren (11) — SJTU, AgiBot, Shanghai AI Lab, CUHK MMLab, LV-NUS Lab | **NeurIPS 2025** | First AGIBOT world model: chunk-wise autoregressive multi-view video diffusion + 4D Gaussian-splatting data engine | [Project page](https://sites.google.com/view/enerverse) | — |

**Known gaps (searched for, not found or not verifiable in this pass):**
- No paper or technical report found for **GO-2**, **GO-3 Preview**, **GE-2**, **BFM**, **GCFM**, **WITA Omni** or **AGIBOT WORLD 2026** (the dataset is released, see below, but has no arXiv paper on its card). ⚠️ unverified whether any exist.
- No AGIBOT paper found on quadruped locomotion (D1 / D2), the X1 open-source humanoid (code only, built on humanoid-gym), LinkSoul / LinkCraft interaction, the C5 cleaning robot or OmniHand hardware.

## Datasets, models and benchmarks released

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| **AgiBot World Beta** ✅ | Real-robot dataset, about **1.0M trajectories**, 217 tasks, G1 robot | CC BY-NC-SA 4.0 (gated: accept terms) | [HF](https://huggingface.co/datasets/agibot-world/AgiBotWorld-Beta) | Pre-training / fine-tuning manipulation policies; retail, home, industrial, catering, office scenes |
| **AgiBot World Alpha** ✅ | Subset, **92,214 trajectories** | CC BY-NC-SA 4.0 (gated) | [HF](https://huggingface.co/datasets/agibot-world/AgiBotWorld-Alpha) | Smaller download for a 48-hour build; the set NVIDIA used for GR00T N1 |
| **AgiBot World 2026** ✅ | Real-robot dataset on the **G2**, free-form collection, LeRobot v2.1 format, per-task download | CC BY-NC-SA 4.0 (open, not gated) | [HF](https://huggingface.co/datasets/agibot-world/AgiBotWorld2026) | Best match if a G2 is on site; plugs straight into LeRobot tooling |
| **AgiBot Digital World** ✅ | Simulation dataset: **1M+ steps** of digital-twin long-horizon tasks, **500k+** auto-generated atomic steps, 180+ object classes | CC BY-NC-SA 4.0 | [HF](https://huggingface.co/datasets/agibot-world/AgiBotDigitalWorld) | Sim pre-training without a robot |
| **Genie Sim 3.x** (v3.5.0, 2 Nov 2026) ✅ | Simulator + benchmark (Isaac Sim), LLM scene generation, teleop, auto data collection, packaged agent "skills" | **MPL-2.0** (code); some sub-modules differ | [GitHub](https://github.com/AgibotTech/genie_sim) | Prototype manipulation in sim before touching the robot; digital-twin scenes via 3DGS |
| **GenieSim Assets** ✅ | **5,140** sim-ready 3D assets (retail, industry, catering, home, office) | CC BY-NC-SA 4.0 | [HF](https://huggingface.co/datasets/agibot-world/GenieSimAssets) | Building custom scenes (shop shelf, kitchen, care room) |
| **GenieSim3.0-Dataset** ✅ | Synthetic data, **10,000+ h**, 200+ tasks (company figure) | not stated in HF metadata ⚠️ unverified | [HF](https://huggingface.co/datasets/agibot-world/GenieSim3.0-Dataset) | Sim-to-real training data for G1 / G2 |
| **Genie Sim Benchmark / RoboColiseum** ✅ | Public leaderboard; 200+ tasks, 100,000+ scenarios; sim-vs-real gap under 10% (company claim) | — | [robocoliseum.ai](https://robocoliseum.ai/) | Objective score for a policy during the hackathon |
| **GO-1** and **GO-1 Air** ✅ | VLA model weights + fine-tuning code (open-sourced 2025-09-19) | CC BY-NC-SA 4.0 (repo) | [GO-1](https://huggingface.co/agibot-world/GO-1) · [GO-1 Air](https://huggingface.co/agibot-world/GO-1-Air) · [code](https://github.com/OpenDriveLab/AgiBot-World) | Fine-tune a manipulation policy on a G-series robot; LIBERO recipe included |
| **ACoT-VLA** ✅ | VLA code (CVPR 2026) | README badges: MIT and CC BY 4.0 | [GitHub](https://github.com/AgibotTech/ACoT-VLA) | Newer open policy code; pairs with the Reasoning-to-Action challenge data |
| **Genie Envisioner v1** (GE-Base, GE-Act, GE-Sim) ✅ | Video world model + policy head | CC BY-NC-SA 4.0 (third-party parts Apache-2.0) | [GitHub](https://github.com/AgibotTech/Genie-Envisioner) · [HF](https://huggingface.co/agibot-world/Genie-Envisioner-v1.0) | Policy from video backbone; needs serious GPU |
| **GE-Sim 2.0** ✅ | World simulator weights incl. G02 / YAM variants, WorldOracle eval code | Apache-2.0 / CC BY-NC-SA 4.0 | [GitHub](https://github.com/AgibotTech/GE-Sim-V2) · [HF](https://huggingface.co/agibot-world/Genie-Envisioner-Sim-v2.0) | Evaluating a policy in a learned simulator |
| **EnerVerse-AC (EVAC)** ✅ | Action-conditioned world model | CC BY-NC-SA 4.0 | [GitHub](https://github.com/AgibotTech/EnerVerse-AC) · [HF](https://huggingface.co/agibot-world/EnerVerse-AC) | World-model track baseline |
| **EWMBench** ✅ | Benchmark dataset + scoring models | CC BY-NC-SA 4.0 | [GitHub](https://github.com/AgibotTech/EWMBench) · [HF](https://huggingface.co/datasets/agibot-world/EWMBench) | Scoring generated robot video |
| **LIFE: RoboBeats + SSS-Bench** ✅ | Streaming event-gate models (0.8B / 2B / 4B LoRA), benchmark, real-time webcam demo | Code Apache-2.0; SSS-Bench data CC BY-NC 4.0 | [GitHub](https://github.com/AgibotTech/LIFE) | **Robot-agnostic**: "tell me when X happens" on any camera stream — monitoring, fall / hazard triggers, memory for a companion |
| **AgiBot World Challenge datasets** (2025; ICRA 2026) ✅ | Competition data: Reasoning-to-Action (10 G2 tasks in Genie Sim) and World Model tracks | CC BY-NC-SA 4.0 | [2026](https://huggingface.co/datasets/agibot-world/AgiBotWorldChallenge-2026) · [2025](https://huggingface.co/datasets/agibot-world/AgiBotWorldChallenge-2025) · [WM baseline](https://github.com/AgibotTech/AgiBotWorldChallengeICRA2026-WorldModelBaseline) | Ready-made tasks such as package sorting, shelf restocking, desktop cleaning, door opening |
| **AgiBot X1** ✅ | Open-source humanoid: hardware design, RL training, inference | not checked ⚠️ unverified | [hardware](https://github.com/AgibotTech/agibot_x1_hardware) · [train](https://github.com/AgibotTech/agibot_x1_train) · [infer](https://github.com/AgibotTech/agibot_x1_infer) | Reference RL locomotion pipeline (humanoid-gym based) |
| **SONIC for A3** 🧪 | Port of NVIDIA's SONIC whole-body tracking controller to the A3; teleoperation checkpoints (PT / ONNX / RKNN) | Apache-2.0 (A3 model: Mulan PSL v2) | [GitHub](https://github.com/AgibotTech/sonic_for_a3) | Whole-body humanoid teleoperation; safety gantry recommended by the repo |
| **Robot models** ✅ | X2 URDF, A3 / A3 Ultra models and USD, Genie Sim robot models, D1 Edu / Ultra, D1 Max, D1 MaxPro repos | Genie Sim robot model: Apache-2.0; others not checked | [AgibotTech org](https://github.com/AgibotTech) | Simulation of the robots likely on site |
| **OmniHand / OmniGlove SDK, URDF, toolbox, firmware** ✅ | Hand software stack (C++ / Python / ROS 2) | toolbox: Mulan PSL v2; others not checked | [agilink_omnihand_sdk](https://github.com/AgibotTech/agilink_omnihand_sdk) | Dexterous-hand control and data collection |
| **AimRT** ✅ | C++ robotics runtime framework (ROS 2 / HTTP / gRPC compatible) | not checked | [GitHub](https://github.com/AimRT/AimRT) | Middleware; ⚠️ unverified — AGIBOT origin not stated on the page read |

## Third-party papers using their hardware or software

None of these has AGIBOT staff as authors (RISE comes from the partner lab OpenDriveLab).

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](https://arxiv.org/abs/2503.14734) | NVIDIA (Johan Bjorck … Linxi "Jim" Fan, Yuke Zhu) | arXiv, Mar 2025 | **AgiBot-Alpha** dataset (140,000 trajectories) in the pre-training mix | AGIBOT data is a standard ingredient of an open humanoid foundation model | T01 T04 |
| [GigaBrain-0: A World Model-Powered Vision-Language-Action Model](https://arxiv.org/abs/2510.19430) | GigaBrain Team (GigaAI) | arXiv, Oct 2025 | **AgiBot G1 robot**: 983 h of own data collected on it; real-robot tests | Laundry folding, paper-towel preparation and other long-horizon tasks on a G1 with a non-AGIBOT model | T01 T04 |
| [X-VLA: Soft-Prompted Transformer as Scalable Cross-Embodiment Vision-Language-Action Model](https://arxiv.org/abs/2510.10274) | Jinliang Zheng, Jianxiong Li … Xianyuan Zhan (15) | arXiv, Oct 2025 | **AgiBot World Beta** in a 290K-episode pre-training mix (with DROID, RoboMIND) | Soft prompts per data source let one small model absorb heterogeneous robots | T01 |
| [TrajBooster: Boosting Humanoid Whole-Body Manipulation via Trajectory-Centric Learning](https://arxiv.org/abs/2509.11839) | Jiacheng Liu, Pengxiang Ding … Donglin Wang (11) | arXiv, Sep 2025 | **AgiBot World Beta** end-effector trajectories retargeted to a Unitree G1 | Wheeled-robot data can bootstrap a bipedal humanoid's household manipulation at varied heights | T04 |
| [RoboCOIN: An Open-Sourced Bimanual Robotic Data Collection for Integrated Manipulation](https://arxiv.org/abs/2511.17441) | Shihan Wu, Xuecheng Liu … (84 authors) | arXiv, Nov 2025 | **AgiBot G1** is one of 15 collection platforms | **180,000+** bimanual demos in residential, commercial and industrial settings; G1 data usable alongside other robots | T01 T03 T04 |
| [InternVLA-A1: Unifying Understanding, Generation and Action for Robotic Manipulation](https://arxiv.org/abs/2601.02456) | Junhao Cai, Zetao Cai … (42 authors) | arXiv, Jan 2026 | **AgiBot World Beta** (206M frames) for training; **Genie-1** as a test robot | An open VLA from another lab running on AGIBOT hardware | T01 |
| [A Pragmatic VLA Foundation Model](https://arxiv.org/abs/2601.18692) (LingBot-VLA) | Wei Wu, Fan Lu … Kecheng Zheng (25) | arXiv, Jan 2026 | **AgiBot G1** as data source and one of the evaluation platforms (GM-100 benchmark) | About 20,000 h of dual-arm data over 9 robot types; 100-task comparison across robots | T01 |
| [RISE: Self-Improving Robot Policy with Compositional World Model](https://arxiv.org/abs/2602.11075) | Jiazhi Yang, Kunyang Lin … Hongyang Li (13) — OpenDriveLab | **RSS 2026** | **AgiBot World** to pre-train the dynamics model | Policy improvement by "imagined" RL instead of risky real-world trials | — |
| [villa-X: Enhancing Latent Action Modeling in Vision-Language-Action Models](https://arxiv.org/abs/2507.23682) | Xiaoyu Chen, Hangxing Wei … Jiang Bian (12) | arXiv, Jul 2025 | **AgiBot** data in pre-training; extends the ViLLA idea introduced with GO-1 | Latent-action VLAs trained on AGIBOT + OpenX data | — |

Related, not counted above: [SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control](https://arxiv.org/abs/2511.07820) (NVIDIA; Science Robotics 2026) does not use AGIBOT hardware, but AGIBOT ported it to the A3 (`sonic_for_a3`).

No third-party paper was found that uses AGIBOT robots for delivery, search-and-rescue, inspection, waste sorting, environmental monitoring or elder care / rehabilitation.

## Reading list by track

### T01 Autonomous Urban Services
- [SOP](https://arxiv.org/abs/2601.03044) — the closest thing to a published "retail robot" recipe: grocery restocking learned by a robot fleet with human corrections.
- [AgiBot World Colosseo / GO-1](https://arxiv.org/abs/2503.06669) — the dataset and open weights you would actually fine-tune for a shop, café or concierge manipulation task.
- [Genie Sim 3.0](https://arxiv.org/abs/2601.02078) — retail, catering and office scenes in sim; lets a team iterate before robot time is available.
- [WholeBodyVLA](https://arxiv.org/abs/2512.11047) — the only verified paper on the **X2**, the robot most likely to be handed to teams; walk-to-and-manipulate.
- [Learning to Live (LIFE)](https://arxiv.org/abs/2611.00180) — RoboBeats gives a concierge / guide robot an "event trigger" on its camera stream and a memory to answer questions later.
- [UniVLA](https://arxiv.org/abs/2505.06111) — how to get a policy from little labelled data (uses video, incl. human video).

### T02 Resilient & Safe City
- [Learning to Live (LIFE)](https://arxiv.org/abs/2611.00180) — robot-agnostic streaming detector for user-defined conditions ("smoke", "person on the floor"); the released code runs on any webcam, so it also fits a D1 patrol dog.
- [Genie Sim 3.0](https://arxiv.org/abs/2601.02078) — its 3DGS reconstruction pipeline is a route to a quick digital twin of a room or corridor.
- [SONIC](https://arxiv.org/abs/2511.07820) with AGIBOT's `sonic_for_a3` port — whole-body humanoid teleoperation, relevant to hazardous-environment remote work (only if an A3 is available).
- No AGIBOT-authored paper on quadruped patrol, inspection, mapping or search and rescue was found; use the D1 SDK docs rather than papers.

### T03 Sustainable City
- [ALOE](https://arxiv.org/abs/2602.12691) — real multi-object sorting and packing improved by human-in-the-loop RL; the nearest published analogue to waste sorting.
- [SOP](https://arxiv.org/abs/2601.03044) — box assembly and restocking at fleet scale; shows how a few hours of on-robot correction lifts success.
- [Genie Centurion](https://arxiv.org/abs/2505.18793) — rewind-and-refine data collection reaches the same result with under half the demonstrations (less operator time, less energy).
- [AgiBot World Colosseo](https://arxiv.org/abs/2503.06669) plus the ICRA 2026 challenge set — includes package-sorting tasks to start from.
- No directly relevant paper found on energy, EV charging, environmental monitoring, agriculture or low-power edge AI.

### T04 Elderly Care & Rehabilitation
- [ACoT-VLA](https://arxiv.org/abs/2601.11404) — real G1 tests on pouring water, wiping and picking unseen objects: the building blocks of assistive household help.
- [WholeBodyVLA](https://arxiv.org/abs/2512.11047) — X2 humanoid fetching across a room; relevant to "bring me the object" assistance.
- [Learning to Live (LIFE)](https://arxiv.org/abs/2611.00180) — day-long memory and event detection; basis for a companion that notices routines, missed medication or a fall-like event.
- [TrajBooster](https://arxiv.org/abs/2509.11839) — household manipulation at different heights (floor to shelf) transferred from AGIBOT data to a biped.
- [GigaBrain-0](https://arxiv.org/abs/2510.19430) — laundry folding and similar caregiver-relief chores on a G1.
- No paper found on rehabilitation, physiotherapy, exoskeleton / EMG interfaces or clinical elder-care trials with AGIBOT hardware.

## White papers, patents and technical reports

- **Research blog — "Introducing AgiBot World Colosseo"** (Modi Shi, Yuxiang Lu, Huijie Wang, Chengen Xie, Qingwen Bu; March 2025) and **"Open-sourcing GO-1: The Bitter Lessons of Building VLA Systems at Scale"** (Modi Shi, Yuxiang Lu, Huijie Wang, Shaoze Yang; September 2025). Both are cited in the AgiBot-World repository README ([blog 1](https://opendrivelab.com/blog/agibot-world/), [blog 2](https://opendrivelab.com/OpenGO1/)); the blog pages themselves were not opened in this pass.
- **AgiBot World Challenge** — held with the 2025 dataset release and again as **AgiBot World Challenge @ ICRA 2026** (tracks: Reasoning to Action on the G2 in Genie Sim 3.0; World Model, scored with PSNR, scene consistency and nDTW from EWMBench). Source: challenge dataset card and baseline repo.
- **Patents:** none verified in this pass.

## Sources

- [GitHub — AgibotTech organisation (repository list)](https://github.com/AgibotTech)
- [GitHub — OpenDriveLab/AgiBot-World (README: news, citations, licence)](https://github.com/OpenDriveLab/AgiBot-World)
- [GitHub — AgibotTech/genie_sim](https://github.com/AgibotTech/genie_sim)
- [GitHub — AgibotTech/Genie-Envisioner](https://github.com/AgibotTech/Genie-Envisioner)
- [GitHub — AgibotTech/GE-Sim-V2](https://github.com/AgibotTech/GE-Sim-V2)
- [GitHub — AgibotTech/ACoT-VLA](https://github.com/AgibotTech/ACoT-VLA)
- [GitHub — AgibotTech/LIFE](https://github.com/AgibotTech/LIFE)
- [GitHub — AgibotTech/EnerVerse-AC](https://github.com/AgibotTech/EnerVerse-AC)
- [GitHub — AgibotTech/EWMBench](https://github.com/AgibotTech/EWMBench)
- [GitHub — AgibotTech/sonic_for_a3](https://github.com/AgibotTech/sonic_for_a3)
- [GitHub — AgibotTech/AgiBotWorldChallengeICRA2026-WorldModelBaseline](https://github.com/AgibotTech/AgiBotWorldChallengeICRA2026-WorldModelBaseline)
- [GitHub — AgibotTech/agibot_x1_train](https://github.com/AgibotTech/agibot_x1_train)
- [GitHub — AimRT/AimRT](https://github.com/AimRT/AimRT)
- [Hugging Face — agibot-world organisation (models and datasets, licence tags)](https://huggingface.co/agibot-world)
- [Hugging Face — AgiBotWorld2026 dataset card](https://huggingface.co/datasets/agibot-world/AgiBotWorld2026)
- [Hugging Face — AgiBotDigitalWorld dataset card](https://huggingface.co/datasets/agibot-world/AgiBotDigitalWorld)
- [Hugging Face — GenieSimAssets dataset card](https://huggingface.co/datasets/agibot-world/GenieSimAssets)
- [Hugging Face — AgiBotWorldChallenge-2026 dataset card](https://huggingface.co/datasets/agibot-world/AgiBotWorldChallenge-2026)
- [OpenDriveLab — publications list (venues for AgiBot World, UniVLA, WholeBodyVLA, RISE)](https://opendrivelab.com/publications)
- [arXiv 2611.00180 — Learning to Live](https://arxiv.org/abs/2611.00180)
- [arXiv 2607.10369 — VINE](https://arxiv.org/abs/2607.10369)
- [arXiv 2605.27491 — GE-Sim 2.0](https://arxiv.org/abs/2605.27491)
- [arXiv 2602.12691 — ALOE](https://arxiv.org/abs/2602.12691)
- [arXiv 2601.11404 — ACoT-VLA](https://arxiv.org/abs/2601.11404)
- [arXiv 2601.03044 — SOP](https://arxiv.org/abs/2601.03044)
- [arXiv 2601.02078 — Genie Sim 3.0](https://arxiv.org/abs/2601.02078)
- [arXiv 2512.24125 — GenieReasoner / ERIQ / FACT](https://arxiv.org/abs/2512.24125)
- [arXiv 2512.11047 — WholeBodyVLA](https://arxiv.org/abs/2512.11047)
- [arXiv 2508.05635 — Genie Envisioner](https://arxiv.org/abs/2508.05635)
- [arXiv 2507.06219 — Is Diversity All You Need](https://arxiv.org/abs/2507.06219)
- [arXiv 2505.21432 — Hume](https://arxiv.org/abs/2505.21432)
- [arXiv 2505.18793 — Genie Centurion](https://arxiv.org/abs/2505.18793)
- [arXiv 2505.09723 — EnerVerse-AC](https://arxiv.org/abs/2505.09723)
- [arXiv 2505.09694 — EWMBench](https://arxiv.org/abs/2505.09694)
- [arXiv 2505.06111 — UniVLA](https://arxiv.org/abs/2505.06111)
- [arXiv 2503.06669 — AgiBot World Colosseo](https://arxiv.org/abs/2503.06669)
- [arXiv 2501.01895 — EnerVerse](https://arxiv.org/abs/2501.01895)
- [arXiv 2503.14734 — GR00T N1](https://arxiv.org/abs/2503.14734)
- [arXiv 2510.19430 — GigaBrain-0](https://arxiv.org/abs/2510.19430)
- [arXiv 2510.10274 — X-VLA](https://arxiv.org/abs/2510.10274)
- [arXiv 2509.11839 — TrajBooster](https://arxiv.org/abs/2509.11839)
- [arXiv 2511.17441 — RoboCOIN](https://arxiv.org/abs/2511.17441)
- [arXiv 2601.02456 — InternVLA-A1](https://arxiv.org/abs/2601.02456)
- [arXiv 2601.18692 — A Pragmatic VLA Foundation Model (LingBot-VLA)](https://arxiv.org/abs/2601.18692)
- [arXiv 2602.11075 — RISE](https://arxiv.org/abs/2602.11075)
- [arXiv 2507.23682 — villa-X](https://arxiv.org/abs/2507.23682)
- [arXiv 2511.07820 — SONIC](https://arxiv.org/abs/2511.07820)
- [AGIBOT company profile (first pass)](AGIBOT.md)
