---
type: papers
company: "Galaxea"
slug: Galaxea
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# Galaxea — Papers and Research

⬆ [Galaxea profile](Galaxea.md) · [Solutions and projects](Galaxea-Solutions-and-Projects.md) · [Developer guide](Galaxea-Developer-Guide.md)

## Research footprint

- **Very research-driven.** The model line (G0 → G0 Plus / G0 Tiny → G0.5) is published on arXiv under "Galaxea Team"; the core authors sit jointly at **IIIS, Tsinghua University and Galaxea AI** (Hang Zhao's group: Tianyuan Yuan, Yicheng Liu, Zibin Dong, Tao Jiang, Baijun Ye). The G0 paper is co-signed by CEO **Jiyang Gao**, **Huazhe Xu** and **Hang Zhao**.
- **Two feeder labs.** Hang Zhao's group produces the VLA / world-model papers (G0, DepthVLA, FASTer, Fast-WAM, G0.5). Huazhe Xu's group at Tsinghua (project pages on the TEA Lab domain) produces data-efficiency and manipulation papers on Galaxea hardware (DemoGen, DemoSpeedup, DenseMatcher, HERMES, ViTaS).
- **Open, but non-commercial.** Code, weights and a **500+ h** dataset are public (GitHub `OpenGalaxea`, **824 stars** on GalaxeaVLA on 2026-11-14; Hugging Face `OpenGalaxea`). Licences moved from Apache-2.0 (2025) to non-commercial community licences (2026). The G0.5 weights and the dataset are **gated on Hugging Face** (an unauthenticated request returns "restricted") — log in and accept the terms before the hackathon clock runs.
- **Large third-party footprint.** Galaxea keeps a public list of 30+ external projects on its hardware (Stanford, NVIDIA GEAR, MIT, NTU, CMU, BAAI, UCSD ...). The R1 / R1 Pro is the reference robot of Stanford's BEHAVIOR Robot Suite and BEHAVIOR Challenge.
- **How this doc was built.** Web search was available but rationed (2 extended searches used). Every paper below was opened on arXiv (metadata via the arXiv listing, full text via the arXiv HTML version) and, where the table states a robot, the hardware mention was checked in the paper text. Venue labels marked "per Galaxea list" come from Galaxea's developer list, not from the arXiv record.

## Company-authored and company-affiliated papers

"Company" = Galaxea Team / Galaxea AI in the author affiliations. "Founder lab" = paper from Huazhe Xu's Tsinghua group (reported co-founder, co-author of the G0 paper) that runs on Galaxea hardware.

| Paper | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts | Tracks |
|---|---|---|---|---|---|
| [G0.5: One Autoregressive Stream for Robot Reasoning and Action](https://arxiv.org/abs/2608.11739) | Galaxea Team — Yicheng Liu, Zibin Dong, Baijun Ye, Tianyuan Yuan, Tao Jiang ... Hang Zhao (**27 authors**) | arXiv, Aug 2026 | One transformer decoder emits reasoning and action tokens in a single stream (cross-embodiment action tokenizer, built-in chain-of-thought, visual memory). Reported: **76.7%** real-world fine-tune success on R1 Lite / R1 Pro (vs 53.3% for pi0.5), **31.4%** on the 2025 BEHAVIOR Challenge, **82.5%** DROID zero-shot, LIBERO **98.9%**, RoboTwin 2.0 **93.3%**, SimplerEnv-Bridge **87.3%** (all self-reported) | [Code](https://github.com/OpenGalaxea/GalaxeaVLA) · [Weights (gated)](https://huggingface.co/OpenGalaxea/G05) · [Project page](https://opengalaxea.github.io/G05/) | T01 T03 T04 |
| [Fast-WAM: Do World Action Models Need Test-time Future Imagination?](https://arxiv.org/abs/2603.16666) | Tianyuan Yuan, Zibin Dong, Yicheng Liu, Hang Zhao — IIIS Tsinghua + Galaxea AI | arXiv, Mar 2026 | World action model that keeps video co-training but skips future-frame generation at inference: **190 ms** latency, over **4x** faster than imagine-then-execute models, no embodied pre-training. Real test: towel folding on R1 Lite from **60 h** of teleop data | [Code](https://github.com/yuantianyuan01/FastWAM) · [Weights](https://huggingface.co/yuanty/fastwam) · [Project page](https://yuantianyuan01.github.io/FastWAM/) | T04 |
| [ViTaS: Visual Tactile Soft Fusion Contrastive Learning for Visuomotor Learning](https://arxiv.org/abs/2602.11643) | Yufeng Tian, Shuiqi Cheng, Tianming Wei, Tianxing Zhou, Yuanhang Zhang ... Huazhe Xu (9 authors) — founder lab | ICRA 2026 | Visuo-tactile representation learning for self-occluded manipulation; real tests on a Galaxea R1 with tactile sensors on the end effector (e.g. moving bottles between fridge shelves) | [Project page](https://skyrainwind.github.io/ViTaS/index.html) | T04 |
| [FASTer: Toward Efficient Autoregressive Vision Language Action Modeling via Neural Action Tokenization](https://arxiv.org/abs/2512.04952) | Yicheng Liu, Shiduo Zhang, Zibin Dong, Baijun Ye, Tianyuan Yuan ... Hang Zhao (15 authors) — Tsinghua, Galaxea AI, Fudan, Shanghai Innovation Institute and others | arXiv, Dec 2025 | Learned action tokenizer (FASTerVQ) plus block-wise autoregressive VLA; **97.9%** on LIBERO; real tests on xArm and R1 Lite (bimanual and whole-body); also evaluated in GalaxeaManipSim. Same research line as the G0.5 action tokenizer | No code link found in the paper | T01 T04 |
| [DepthVLA: Enhancing Vision-Language-Action Models with Depth-Aware Spatial Reasoning](https://arxiv.org/abs/2510.13375) | Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Zhuoguang Chen, Tao Jiang, Hang Zhao — IIIS Tsinghua + Galaxea AI | arXiv, Oct 2025 | Adds a pretrained depth-prediction expert to the VLA (mixture of transformers). **78.5% vs 65.0%** task progress in real tests on R1 Lite after pre-training on the Galaxea Open-World Dataset; LIBERO 94.9% | "Code will be made public" — none found | T01 T03 |
| [Galaxea Open-World Dataset and G0 Dual-System VLA Model](https://arxiv.org/abs/2509.00576) | Galaxea Team — Tao Jiang, Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Jianning Cui, Xiao Liu, Shuiqi Cheng, Jiyang Gao, Huazhe Xu, Hang Zhao | arXiv, Aug 2025 | The dataset paper (**500 h, 100K trajectories, 150 task categories, 50 scenes, 1,600+ objects, 58 skills**, one embodiment) and G0: a VLM planner plus a VLA executor, trained in three stages. Shows single-embodiment pre-training matters most | [Dataset (gated)](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset) · [Weights](https://huggingface.co/OpenGalaxea/G0-VLA) · [Project page](https://opengalaxea.github.io/GalaxeaVLA/) | T01 T03 T04 |
| [HERMES: Human-to-Robot Embodied Learning from Multi-Source Motion Data for Mobile Dexterous Manipulation](https://arxiv.org/abs/2508.20085) | Zhecheng Yuan, Tianming Wei, Langzhe Gu, Pu Hua, Tianhai Liang ... Huazhe Xu (7 authors) — founder lab | arXiv, Aug 2025 | Turns human hand motion into RL-trained mobile bimanual dexterous skills with sim-to-real transfer. Robot: X1 mobile base + two 6-DoF Galaxea A1 arms + dexterous hands | [Project page](https://gemcollector.github.io/HERMES/) | T04 |
| [DemoSpeedup: Accelerating Visuomotor Policies via Entropy-Guided Demonstration Acceleration](https://arxiv.org/abs/2506.05064) | Lingxiao Guo, Zhengrong Xue, Zijing Xu, Huazhe Xu — founder lab | arXiv, Jun 2025 | Self-supervised speed-up of slow teleop demonstrations so the learned policy runs faster; 5 real tasks on a Galaxea R1, 100 demos each collected with the Galaxea VR suite | [Project page](https://demospeedup.github.io/) | T01 T04 |
| [DemoGen: Synthetic Demonstration Generation for Data-Efficient Visuomotor Policy Learning](https://arxiv.org/abs/2502.16932) | Zhengrong Xue, Shuying Deng, Zhenyang Chen, Yixuan Wang, Zhecheng Yuan, Huazhe Xu — founder lab | RSS 2025 (per Galaxea list) | Generates spatially augmented demonstrations from **one** real demo; includes a bimanual fruit-basket task on a Galaxea R1 | [Project page](https://demo-generation.github.io/) | T03 T04 |
| [VR-Robo: A Real-to-Sim-to-Real Framework for Visual Robot Navigation and Locomotion](https://arxiv.org/abs/2502.01536) | Shaoting Zhu, Linzhan Mou, Derun Li, Baijun Ye, Runhan Huang, Hang Zhao — Galaxea AI listed among the affiliations | RA-L 2025 (per Galaxea list) | Photorealistic digital twin from RGB for training visual navigation policies. Galaxea's list says it was validated on the R1 — ⚠️ unverified in the paper text (the abstract is about legged locomotion) | [Project page](https://vr-robo.github.io/) | T01 T02 |
| [DenseMatcher: Learning 3D Semantic Correspondence for Category-Level Manipulation from a Single Demo](https://arxiv.org/abs/2412.05268) | Junzhe Zhu, Yuanchen Ju, Junyi Zhang, Muhan Wang, Zhecheng Yuan ... Huazhe Xu (7 authors) — founder lab | ICLR 2025 spotlight (per Galaxea list) | Dense 3D semantic correspondence lets a robot copy a task from one human demo (banana peeling with a Galaxea A1 arm plus a UR5) | [Project page](https://tea-lab.github.io/DenseMatcher/) | T04 |

**No paper found** for: G0 Plus (3B), G0 Tiny (250M), GalaxeaDP and GalaxeaManipSim (both cite only "Galaxea Team, 2025" in their READMEs), LEMO, Nexo, Kengo.

## Datasets, models and benchmarks released

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| G0.5 checkpoints: `g05-base`, `g05-so101`, `g05-droid`, `g05-libero`, `g05-robotwin20` (about **11 GB** each) ✅ | VLA weights (Qwen3.5 2B backbone) | G0.5 Community License (non-commercial); gated | [HF OpenGalaxea/G05](https://huggingface.co/OpenGalaxea/G05) | Zero-shot and fine-tuning on R1 Lite / R1 Pro; SO-100/101; Franka (DROID). Inference **more than 8 GB VRAM**, full fine-tune **more than 70 GB** |
| GalaxeaVLA ✅ | Training, fine-tuning and deployment code | Apache-2.0 before 2026-01-04; G0 Plus Community License until 2026-06-16; G0.5 Community License after | [GitHub](https://github.com/OpenGalaxea/GalaxeaVLA) | The single repo to clone; entry points under `experiments/r1lite`, `r1pro`, `so100`, `droid`, `libero`, `robotwin` |
| G0-VLA, G0Plus_3B-base, G0Plus_3B-pick_and_place, G0Tiny_250M-base ✅ (legacy) | VLA weights | CC BY-NC-SA 4.0 on the model card (G0 Plus items also fall under the G0 Plus Community License in the repo) | [HF OpenGalaxea/G0-VLA](https://huggingface.co/OpenGalaxea/G0-VLA) · [ModelScope](https://www.modelscope.cn/models/Galaxea/G0-VLA) | Ready pick-and-place checkpoint; G0 Tiny runs on the R1 Pro's Orin (TensorRT, up to 10 Hz); legacy code at commit `13a16a9` |
| Galaxea Open-World Dataset ✅ | Real-robot mobile-manipulation data, **500+ h**, RLDS and LeRobot formats, subtask language labels | CC BY-NC-SA 4.0; gated | [HF dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset) · [ModelScope](https://www.modelscope.cn/datasets/Galaxea/Galaxea-Open-World-Dataset) | Pre-training / co-training for R1 Lite policies; home, kitchen, retail and office scenes |
| R1Pro_Pick_and_Place_Cube ✅ | Small R1 Pro demo dataset | CC BY-NC-SA 4.0 | [HF dataset](https://huggingface.co/datasets/OpenGalaxea/R1Pro_Pick_and_Place_Cube) | Smoke-testing an R1 Pro fine-tuning pipeline |
| G05-LIBERO-Dataset ✅ | Five LIBERO suites in LeRobot v3.0 format | not stated | [HF dataset](https://huggingface.co/datasets/OpenGalaxea/G05-LIBERO-Dataset) | Reproducing G0.5 LIBERO fine-tuning |
| g05-robodojo 🧪 | G0.5 checkpoint and training assets for the RoboDojo benchmark | "other"; card says private | [HF model](https://huggingface.co/OpenGalaxea/g05-robodojo) | Benchmark reproduction only |
| GalaxeaManipSim ✅ | Simulation benchmark: **30+ environments, 17 tasks** for R1 / R1 Pro / R1 Lite, joint-space and IK controllers | README says MIT; GitHub detects Apache-2.0 — ⚠️ inconsistent | [GitHub](https://github.com/OpenGalaxea/GalaxeaManipSim) | Generating demos and testing policies without a robot |
| GalaxeaDP ✅ | Diffusion-policy baseline wired to ManipSim and LeRobot data | README says MIT; GitHub detects Apache-2.0 — ⚠️ inconsistent | [GitHub](https://github.com/OpenGalaxea/GalaxeaDP) | Small policy trainable in hours on one consumer GPU |
| GalaxeaLeRobotToolkit ✅ | rosbag / MCAP to LeRobot converter | Apache-2.0 | [GitHub](https://github.com/OpenGalaxea/GalaxeaLeRobotToolkit) | Turning on-site teleop recordings into training data |
| GalaxeaLeRobot and GalaxeaLerobot3.0 ✅ | LeRobot forks (fixes, faster data generation, merge tools) | Apache-2.0 | [GalaxeaLeRobot](https://github.com/OpenGalaxea/GalaxeaLeRobot) · [GalaxeaLerobot3.0](https://github.com/OpenGalaxea/GalaxeaLerobot3.0) | Dataset tooling |
| EFMNode ✅ | On-robot deployment node for policies | no licence file detected | [GitHub](https://github.com/OpenGalaxea/EFMNode) | Running a trained policy against the robot's ROS interfaces |
| BEHAVIOR-1K fork ✅ | Fork of Stanford's household simulation benchmark | upstream licence | [GitHub](https://github.com/OpenGalaxea/BEHAVIOR-1K) | Reproducing the G0.5 BEHAVIOR result (R1 Pro in simulation) |
| Fast-WAM code, weights and converted LIBERO / RoboTwin data ✅ | World action model (author-hosted, not under OpenGalaxea) | ⚠️ unverified | [GitHub](https://github.com/yuantianyuan01/FastWAM) · [HF yuanty/fastwam](https://huggingface.co/yuanty/fastwam) | Research baseline; repo reports about **110 ms** inference on an RTX 4090 after the latest update |
| awesome-galaxea-developers ✅ | Curated list of third-party projects and competitions | none | [GitHub](https://github.com/OpenGalaxea/awesome-galaxea-developers) | Finding existing code for a given Galaxea robot |

## Third-party papers using their hardware or software

Newest first. "Checked" in the hardware column means the Galaxea robot or dataset is named in the paper text.

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [MobileVISTA: Generative Data Augmentation for Pose Generalization in Mobile Manipulation](https://arxiv.org/abs/2610.07511) | Suzannah Wistreich, Stephen Tian, Isabella Huang, Vitor Campagnolo Guizilini, Sergey Zakharov ... Jiajun Wu (7 authors) | arXiv, Oct 2026 | R1 Pro (checked) | Augments demos so policies survive base-pose errors; real tasks: **laundry sort into two bins** and book stacking | T03 T04 |
| [Automatic Labelling for Bimanual Mobile Manipulation](https://arxiv.org/abs/2609.24059) | Yupu Lu, Jia Pan | arXiv, Sep 2026 | Galaxea Open-World Dataset, 29 tasks (checked) | Automatic subtask segmentation and language labels from kinematics plus a VLM | T01 |
| [Morphology-Aware Human Motion Retargeting for Wheeled-Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.11357) | Chenbo Xia, Chao Ye | arXiv, Sep 2026 | R1 Pro URDF, simulation pipeline (checked) | Converts SMPL-X human motion into base + torso + arm motion for a wheeled humanoid | T04 |
| [World Tokens: Enhancing Embodied Policies with Training-Time World Modeling](https://arxiv.org/abs/2608.09730) | Qu Tang, Benhui Zhuang, Bo Yuan, Xue Yu, Longteng Guo ... Junlan Feng (6 authors) | arXiv, Aug 2026 | R1 Pro, right arm (checked) | Training-time world modelling improves a VLA without slowing inference | — |
| [AffordTrajDP: Dynamic Affordance-Guided Visuomotor Policy Learning for Robotic Manipulation](https://arxiv.org/abs/2608.01603) | Gaoyuan Wu, Ziyu Shan, Haoyang Du, Yuyao Jiang, Ziwei Wang | arXiv, Aug 2026 | A1 arm (checked) | Affordance trajectories for precise tasks (stack cube, pick cup, adapter insertion) with unseen objects | T03 |
| [CORAL: Scalable Multi-Task Robot Learning via LoRA Experts](https://arxiv.org/abs/2603.09298) | Yuankai Luo, Woping Chen, Tong Liang, Zhenguo Li | arXiv, Mar 2026 | R1 Lite (checked) | One LoRA adapter per task on a shared VLA; add tasks without forgetting | T01 T04 |
| [AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models](https://arxiv.org/abs/2603.08519) | Xiaoquan Sun, Zetian Xu, Chen Cao, Zonghe Liu, Yihan Sun ... Jiayu Chen (12 authors) | arXiv, Mar 2026 | R1 Lite (checked) | Sub-task instruction grounding for long-horizon tasks, incl. T-shirt folding | T04 |
| [EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data](https://arxiv.org/abs/2602.16710) | Ruijie Zheng, Dantong Niu, Yuqi Xie, Jing Wang, Mengda Xu ... Linxi Fan (15 authors) — NVIDIA GEAR | arXiv, Feb 2026 | R1 Pro with 22-DoF Sharpa hands (checked) | Pre-training on 20,000+ h of human video; one-shot adaptation, e.g. shirt folding | T04 |
| [VLASH: Real-Time VLAs via Future-State-Aware Asynchronous Inference](https://arxiv.org/abs/2512.01031) | Jiaming Tang, Yufei Sun, Yilong Zhao, Shang Yang, Yujun Lin ... Song Han (10 authors) — MIT and others | arXiv, Nov 2025 | R1 Lite and SO-101 (checked) | Asynchronous inference makes pi0.5 react fast enough for ping-pong and whack-a-mole; [code](https://github.com/mit-han-lab/vlash/) | T01 T04 |
| [RoboCOIN: An Open-Sourced Bimanual Robotic Data Collection for Integrated Manipulation](https://arxiv.org/abs/2511.17441) | Shihan Wu, Xuecheng Liu, Shaoxuan Xie, Pengwei Wang, Xinghang Li ... (84 authors; Galaxea is one listed affiliation) | arXiv, Nov 2025 | R1 Lite among 15 platforms (checked) | **180,000+** bimanual trajectories, 421 tasks; [project page](https://flagopen.github.io/RoboCOIN/) | T01 T04 |
| [NORA-1.5: A Vision-Language-Action Model Trained using World Model- and Action-based Preference Rewards](https://arxiv.org/abs/2511.14659) | Chia-Yu Hung, Navonil Majumder, Haoyuan Deng, Liu Renhang, Yankang Ang ... Soujanya Poria (10 authors) | arXiv, Nov 2025 | A1 arm (checked) | Reward-guided post-training of a VLA, real tests on the A1 | — |
| [iFlyBot-VLA Technical Report](https://arxiv.org/abs/2511.01914) | Yuan Zhang, Chenyu Xue, Wenjie Xu, Chao Ji, Jiajia Wu, Jia Pan | arXiv, Nov 2025 | Galaxea Open-World Dataset in pre-training (checked) | Latent-action VLA with dual-level action representation | — |
| [GSWorld: Closed-Loop Photo-Realistic Simulation Suite for Robotic Manipulation](https://arxiv.org/abs/2510.20813) | Guangqi Jiang, Haoran Chang, Ri-Zhao Qiu, Yutong Liang, Mazeyu Ji ... Xiaolong Wang (9 authors) | arXiv, Oct 2025 | R1 (checked) | Gaussian-splat simulator for sim-to-real and virtual teleoperation of the R1 | T01 |
| [MoMaGen: Generating Demonstrations under Soft and Hard Constraints for Multi-Step Bimanual Mobile Manipulation](https://arxiv.org/abs/2510.18316) | Chengshu Li, Mengdi Xu, Arpit Bahety, Hang Yin, Yunfan Jiang ... Li Fei-Fei (14 authors) — Stanford | ICLR 2026 | R1 in simulation and real (checked) | Generates large mobile-manipulation datasets from one demo, with reachability and visibility constraints | T01 T04 |
| [UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning](https://arxiv.org/abs/2510.10642) (listed by Galaxea as "UniCoD") | Jianke Zhang, Yucheng Hu, Yanjiang Guo, Xiaoyu Chen, Yichen Liu ... Jianyu Chen (8 authors) | ICML 2026 | Galaxea Open-World Dataset, 99k samples (checked) | Policy pre-training that combines understanding and generation objectives | — |
| [Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking](https://arxiv.org/abs/2510.02252) | Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, C. Karen Liu — Stanford | arXiv, Oct 2025 | R1 Pro supported in the [GMR code](https://github.com/YanjieZe/GMR) since Aug 2025 (repo README; not named in the paper) | Real-time human-to-robot whole-body retargeting for teleoperation | T04 |
| [Pixel Motion Diffusion is What We Need for Robot Control (DAWN)](https://arxiv.org/abs/2509.22652) | E-Ro Nguyen, Yichi Zhang, Kanchana Ranasinghe, Xiang Li, Michael S. Ryoo | CVPR 2026 | R1 Lite bimanual setup and Galaxea Open-World Dataset (checked) | Language → pixel-motion map → action, both stages as diffusion; interpretable intermediate | T01 T04 |
| [VLA-Reasoner: Empowering Vision-Language-Action Models with Reasoning via Online Monte Carlo Tree Search](https://arxiv.org/abs/2509.22643) | Wenkai Guo, Guanxing Lu, Haoyuan Deng, Zhenyu Wu, Yansong Tang, Ziwei Wang | ICRA 2026 | A1 arm (checked) | Test-time tree search over imagined futures improves long-horizon VLA behaviour | — |
| [SafeBimanual: Diffusion-based Trajectory Optimization for Safe Bimanual Manipulation](https://arxiv.org/abs/2508.18268) | Haoyuan Deng, Wenkai Guo, Qianzhun Wang, Zhenyu Wu, Ziwei Wang | CoRL 2025 (per Galaxea list) | R1 (checked) | Test-time safety costs on a pretrained diffusion policy cut unsafe dual-arm interactions on 4 real tasks | T02 T04 |
| [XRoboToolkit: A Cross-Platform Framework for Robot Teleoperation](https://arxiv.org/abs/2508.00097) | Zhigen Zhao, Liuchuan Yu, Ke Jing, Ning Yang | IEEE/SICE SII 2026 | R1 Lite (checked) | OpenXR teleoperation with low-latency stereo video; data used to train VLAs; [project page](https://xr-robotics.github.io/) | T01 T02 T04 |
| [NeSyPack: A Neuro-Symbolic Framework for Bimanual Logistics Packing](https://arxiv.org/abs/2506.06567) | Bowei Li, Peiqi Yu, Zhenran Tang, Han Zhou, Yifan Sun, Ruixuan Liu, Changliu Liu — CMU | RSS 2025 workshop | Dual A1X arms (checked) | Symbolic skill graph plus learned skills; **first prize, WBCD competition at ICRA 2025**; over 90% task success | T01 T03 |
| [NavDP: Learning Sim-to-Real Navigation Diffusion Policy with Privileged Information Guidance](https://arxiv.org/abs/2505.08712) | Wenzhe Cai, Jiaqi Peng, Yuqiang Yang, Yujian Zhang, Meng Wei ... Jiangmiao Pang (9 authors) | arXiv, May 2025 | R1, alongside Unitree Go2 / G1 and Turtlebot4 (checked) | Navigation policy trained only in simulation, zero-shot on real robots in cluttered indoor and outdoor scenes | T01 T02 |
| [pi0.5: a Vision-Language-Action Model with Open-World Generalization](https://arxiv.org/abs/2504.16054) | Physical Intelligence (36 authors) | arXiv, Apr 2025 | R1 Lite per Galaxea's list — ⚠️ unverified, the paper does not name Galaxea | Household clean-up in unseen homes with a mobile manipulator | T04 |
| [BEHAVIOR Robot Suite: Streamlining Real-World Whole-Body Manipulation for Everyday Household Activities](https://arxiv.org/abs/2503.05652) | Yunfan Jiang, Ruohan Zhang, Josiah Wong, Chen Wang, Yanjie Ze ... Li Fei-Fei (10 authors) — Stanford | CoRL 2025 | R1 (checked) | Low-cost whole-body teleop (JoyLo) plus a whole-body policy (WB-VIMA) on 5 household tasks, e.g. clean the toilet, put items onto shelves, lay clothes out; [project page](https://behavior-robot-suite.github.io/) | T01 T04 |
| [AVR: Active Vision-Driven Precise Robot Manipulation with Viewpoint and Focal Length Optimization](https://arxiv.org/abs/2503.01439) | Yushan Liu, Shilong Mu, Xintao Chao, Zizhen Li, Yao Mu ... Wenbo Ding (10 authors) | arXiv, Mar 2025 | Two 6-DoF Galaxea A1 arms (checked) | Bimanual teleop with an actively controlled camera for precise manipulation | — |

Related software and benchmarks without their own row:

- **RoboBrain-X0** (BAAI) ✅ — cross-embodiment model whose repo ships inference examples for R1 Lite (ROS 1 and ROS 2). No dedicated paper found; the linked report is OmniSAT. [GitHub](https://github.com/FlagOpen/RoboBrain-X0)
- **BEHAVIOR Challenge** (Stanford) ✅ — 50 long-horizon household tasks; Galaxea states the benchmark robot is the R1 Pro and G0.5 reports 31.4% on the 2025 edition. [Site](https://behavior.stanford.edu/)
- **RoCo Challenge** (NTU, AAAI 2026) — listed by Galaxea as supporting the R1 Pro; the linked page did not load — ⚠️ unverified.
- **CogVLA** (NeurIPS 2025) — listed by Galaxea as demonstrated on R1 Lite, but the paper's real-world table is on an Agilex ALOHA platform — ⚠️ unverified, not counted above. [arXiv 2508.21046](https://arxiv.org/abs/2508.21046)

## Reading list by track

### T01 Autonomous Urban Services

- [G0.5](https://arxiv.org/abs/2608.11739) — the model you would fine-tune on R1 Lite / R1 Pro; prompts steer task horizon and granularity, useful for fetch, deliver and tidy services (T01.1, T01.2, T01.3).
- [Galaxea Open-World Dataset and G0](https://arxiv.org/abs/2509.00576) — what data exists for retail and office scenes and how the three-stage training recipe works.
- [NavDP](https://arxiv.org/abs/2505.08712) — sim-trained navigation policy already run on the R1 base; closest paper to T01.6.
- [NeSyPack](https://arxiv.org/abs/2506.06567) — competition-winning packing with few demos; a 48-hour-friendly pattern (symbolic task graph + small learned skills) for T01.1.
- [BEHAVIOR Robot Suite](https://arxiv.org/abs/2503.05652) — whole-body teleop and policy for cleaning-type tasks on the R1 (T01.2).
- [VLASH](https://arxiv.org/abs/2512.01031) — how to keep a VLA responsive around people (T01.7).

### T02 Resilient & Safe City

No directly relevant paper found (nothing on rescue, hazardous inspection or disaster sensing with Galaxea hardware). Closest adjacent work:

- [SafeBimanual](https://arxiv.org/abs/2508.18268) — adds safety constraints to an existing policy at test time; relevant to human-robot collaboration (T02.7).
- [XRoboToolkit](https://arxiv.org/abs/2508.00097) — VR teleoperation of the R1 Lite; basis for an operator-in-the-loop response demo.
- [NavDP](https://arxiv.org/abs/2505.08712) — obstacle-avoiding navigation in clutter; flat ground only on the R1.
- [VR-Robo](https://arxiv.org/abs/2502.01536) — camera-only navigation trained in a reconstructed digital twin.

### T03 Sustainable City

No paper on waste sorting, recycling or environmental monitoring found. Useful for a sorting demo:

- [MobileVISTA](https://arxiv.org/abs/2610.07511) — category-based sorting into bins on the R1 Pro that tolerates imprecise base placement (T03.1, T03.6).
- [DemoGen](https://arxiv.org/abs/2502.16932) — one real demonstration expanded into many; cuts data collection time.
- [G0.5](https://arxiv.org/abs/2608.11739) — includes a language-following pick-and-place benchmark; start from `g05-base` or the legacy pick-and-place checkpoint.
- [DepthVLA](https://arxiv.org/abs/2510.13375) — why depth awareness helps grasp accuracy in cluttered bins.
- [NeSyPack](https://arxiv.org/abs/2506.06567) — reliable pick-and-pack of mixed objects with dual A1X arms.

### T04 Elderly Care & Rehabilitation

No care-home or clinical study found; the household-assistance literature is strong:

- [BEHAVIOR Robot Suite](https://arxiv.org/abs/2503.05652) — the reference for daily-living tasks on the R1 (T04.1), with open teleop hardware design.
- [G0.5](https://arxiv.org/abs/2608.11739) — household long-horizon results (BEHAVIOR Challenge) and R1 fine-tuning numbers.
- [Fast-WAM](https://arxiv.org/abs/2603.16666) — towel folding on R1 Lite in real time; laundry is a credible T04.6 demo.
- [EgoScale](https://arxiv.org/abs/2602.16710) — dexterous hands on the R1 Pro learned mostly from human video.
- [SafeBimanual](https://arxiv.org/abs/2508.18268) — safety layer for dual-arm motion near a person.
- [MoMaGen](https://arxiv.org/abs/2510.18316) — scale one demo of a multi-step home task into a training set.

## White papers, patents and technical reports

- The G0 and G0.5 arXiv papers are the company's technical reports (both signed "Galaxea Team").
- No separate white papers found. Patents were not searched.

## Sources

- [arXiv 2608.11739 — G0.5](https://arxiv.org/abs/2608.11739)
- [arXiv 2603.16666 — Fast-WAM](https://arxiv.org/abs/2603.16666)
- [arXiv 2512.04952 — FASTer](https://arxiv.org/abs/2512.04952)
- [arXiv 2510.13375 — DepthVLA](https://arxiv.org/abs/2510.13375)
- [arXiv 2509.00576 — Galaxea Open-World Dataset and G0](https://arxiv.org/abs/2509.00576)
- [arXiv 2602.11643 — ViTaS](https://arxiv.org/abs/2602.11643)
- [arXiv 2508.20085 — HERMES](https://arxiv.org/abs/2508.20085)
- [arXiv 2506.05064 — DemoSpeedup](https://arxiv.org/abs/2506.05064)
- [arXiv 2502.16932 — DemoGen](https://arxiv.org/abs/2502.16932)
- [arXiv 2502.01536 — VR-Robo](https://arxiv.org/abs/2502.01536)
- [arXiv 2412.05268 — DenseMatcher](https://arxiv.org/abs/2412.05268)
- [arXiv 2610.07511 — MobileVISTA](https://arxiv.org/abs/2610.07511)
- [arXiv 2609.24059 — Automatic Labelling for Bimanual Mobile Manipulation](https://arxiv.org/abs/2609.24059)
- [arXiv 2609.11357 — Morphology-Aware Human Motion Retargeting](https://arxiv.org/abs/2609.11357)
- [arXiv 2608.09730 — World Tokens](https://arxiv.org/abs/2608.09730)
- [arXiv 2608.01603 — AffordTrajDP](https://arxiv.org/abs/2608.01603)
- [arXiv 2603.09298 — CORAL](https://arxiv.org/abs/2603.09298)
- [arXiv 2603.08519 — AtomVLA](https://arxiv.org/abs/2603.08519)
- [arXiv 2602.16710 — EgoScale](https://arxiv.org/abs/2602.16710)
- [arXiv 2512.01031 — VLASH](https://arxiv.org/abs/2512.01031)
- [arXiv 2511.17441 — RoboCOIN](https://arxiv.org/abs/2511.17441)
- [arXiv 2511.14659 — NORA-1.5](https://arxiv.org/abs/2511.14659)
- [arXiv 2511.01914 — iFlyBot-VLA](https://arxiv.org/abs/2511.01914)
- [arXiv 2510.20813 — GSWorld](https://arxiv.org/abs/2510.20813)
- [arXiv 2510.18316 — MoMaGen](https://arxiv.org/abs/2510.18316)
- [arXiv 2510.10642 — UniJEPA](https://arxiv.org/abs/2510.10642)
- [arXiv 2510.02252 — General Motion Retargeting](https://arxiv.org/abs/2510.02252)
- [arXiv 2509.22652 — DAWN](https://arxiv.org/abs/2509.22652)
- [arXiv 2509.22643 — VLA-Reasoner](https://arxiv.org/abs/2509.22643)
- [arXiv 2508.21046 — CogVLA](https://arxiv.org/abs/2508.21046)
- [arXiv 2508.18268 — SafeBimanual](https://arxiv.org/abs/2508.18268)
- [arXiv 2508.00097 — XRoboToolkit](https://arxiv.org/abs/2508.00097)
- [arXiv 2506.06567 — NeSyPack](https://arxiv.org/abs/2506.06567)
- [arXiv 2505.08712 — NavDP](https://arxiv.org/abs/2505.08712)
- [arXiv 2504.16054 — pi0.5](https://arxiv.org/abs/2504.16054)
- [arXiv 2503.05652 — BEHAVIOR Robot Suite](https://arxiv.org/abs/2503.05652)
- [arXiv 2503.01439 — AVR](https://arxiv.org/abs/2503.01439)
- [GitHub — OpenGalaxea organisation](https://github.com/OpenGalaxea)
- [GitHub — OpenGalaxea/GalaxeaVLA (README, news, citation, licence)](https://github.com/OpenGalaxea/GalaxeaVLA)
- [GitHub — OpenGalaxea/awesome-galaxea-developers](https://github.com/OpenGalaxea/awesome-galaxea-developers)
- [GitHub — OpenGalaxea/GalaxeaDP](https://github.com/OpenGalaxea/GalaxeaDP)
- [GitHub — OpenGalaxea/GalaxeaManipSim](https://github.com/OpenGalaxea/GalaxeaManipSim)
- [GitHub — OpenGalaxea/GalaxeaLeRobotToolkit](https://github.com/OpenGalaxea/GalaxeaLeRobotToolkit)
- [GitHub — OpenGalaxea/EFMNode](https://github.com/OpenGalaxea/EFMNode)
- [GitHub — yuantianyuan01/FastWAM](https://github.com/yuantianyuan01/FastWAM)
- [GitHub — YanjieZe/GMR](https://github.com/YanjieZe/GMR)
- [GitHub — FlagOpen/RoboBrain-X0](https://github.com/FlagOpen/RoboBrain-X0)
- [Hugging Face — OpenGalaxea/G05](https://huggingface.co/OpenGalaxea/G05)
- [Hugging Face — OpenGalaxea/G0-VLA](https://huggingface.co/OpenGalaxea/G0-VLA)
- [Hugging Face — Galaxea Open-World Dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset)
- [Hugging Face — OpenGalaxea/G05-LIBERO-Dataset](https://huggingface.co/datasets/OpenGalaxea/G05-LIBERO-Dataset)
- [Hugging Face — OpenGalaxea/R1Pro_Pick_and_Place_Cube](https://huggingface.co/datasets/OpenGalaxea/R1Pro_Pick_and_Place_Cube)
- [Hugging Face — OpenGalaxea/g05-robodojo](https://huggingface.co/OpenGalaxea/g05-robodojo)
- [G0.5 project page](https://opengalaxea.github.io/G05/)
- [Fast-WAM project page](https://yuantianyuan01.github.io/FastWAM/)
- [BEHAVIOR Robot Suite project page](https://behavior-robot-suite.github.io/)
- [BEHAVIOR benchmark site](https://behavior.stanford.edu/)
- [Galaxea blog — Fast-WAM](https://galaxea-dynamics.com/blogs/developer-hub/fast-wam-world-action-model)
- [Galaxea blog — G0.5](https://galaxea-dynamics.com/blogs/developer-hub/galaxea-g05-a-new-generation-embodied-foundation-model-for-robotics)
- [Galaxea blog — Stanford x Galaxea household robotics](https://galaxea-dynamics.com/blogs/robotics-applications/stanford-galaxea-brs-household-robotics)
