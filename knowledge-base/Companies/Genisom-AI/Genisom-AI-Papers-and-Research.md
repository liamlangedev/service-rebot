---
type: papers
company: "Genisom AI"
slug: Genisom-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# Genisom AI — Papers and Research

⬆ [Genisom AI profile](Genisom-AI.md) · [Solutions and projects](Genisom-AI-Solutions-and-Projects.md) · [Developer guide](Genisom-AI-Developer-Guide.md)

> **Coverage note (read first):** the web-search budget for this run was used up before the paper hunt started, so no search-engine queries could be made. Everything below was found by opening primary pages directly: the official GitHub organisation `zsibot` (all 10 repos and their READMEs), arXiv abstract pages, Hugging Face, and the company's English and Chinese sites. Company-authored work is therefore well covered; **third-party papers that use Genisom hardware could not be searched systematically** and that section is thin for this reason, not because such papers are proven not to exist.

## Research footprint

- **Engineering-led, not paper-led.** Only **1 company-authored paper** could be confirmed (a 5-page IROS 2026 workshop paper on world models). The company site (Open Source, Education and Research, News, About pages) lists no publications, labs or named researchers. The Chinese About page states about **500 staff, 70 % R&D** (company-stated).
- **Key people (from the paper only):** Muyuan Liu, Yue Huang, Zheng Liang and Xiang Gao, all listed as "with Genisom AI, Beijing". The corresponding author's contact email is the same one published in the `gaoxiang12/slambook2` README (the "Visual SLAM" textbook code, also the account behind Faster-LIO and Lightning-LM), so this is very likely the same SLAM researcher. ⚠️ unverified by the company; that GitHub profile shows a different organisation domain (zhiyuan-robotics.com).
- **Open-source posture is strong for a hardware company:** 10 public repos under [github.com/zsibot](https://github.com/zsibot/), mostly **BSD-3-Clause** or **MIT** — simulator (MATRiX), navigation stack (RoamerX Lite), VLN framework, world model, URDFs and two SDK generations. Only `gawm` has a citation block; MATRiX, RoamerX and the VLN framework have **no accompanying paper**.
- **No dataset and no benchmark released.** The one paper trains and evaluates on third-party data (LeWM collection, OGBench). No robot-collected dataset, no locomotion-policy weights and no navigation model weights are public.
- **Academic links are through competitions, not co-authored papers:** University of Manchester (IROS 2025 legged challenge winner on L1) and NTU Singapore (IROS 2026 fully autonomous category winner on M1), per the company's IROS 2026 press release. No paper from either team was found.

## Company-authored and company-affiliated papers

| Paper | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts | Tracks |
|---|---|---|---|---|---|
| [Toward Physically Grounded JEPA World Models for Goal-Conditioned Robotic Planning](https://arxiv.org/abs/2609.03565) | Muyuan Liu, Yue Huang (equal contribution), Zheng Liang, Xiang Gao — all Genisom AI, Beijing | arXiv 2609.03565 (v2, 19 Sep 2026); accepted to the IROS 2026 Workshop on Physical World Models for Scaling Embodied AI (PWMS 2026); 5 pages | JEPA-style latent world model that adds **inverse dynamics** and **physical-state alignment** to latent prediction; planning with CEM in latent space. Reported success: **TwoRoom 100 %**, **PushT 98 %**, **OGBench-Cube 87 %**, on par with LeWorldModel on Reacher. Simulation benchmarks only — no Genisom robot in the experiments. | Code: [zsibot/gawm](https://github.com/zsibot/gawm) (MIT) · Weights: [kikihuang/GA-WM](https://huggingface.co/kikihuang/GA-WM) · Data: third-party [LeWM collection](https://huggingface.co/collections/quentinll/lewm) | — |
| [Faster-LIO: Lightweight Tightly Coupled Lidar-Inertial Odometry Using Parallel Sparse Incremental Voxels](https://github.com/gaoxiang12/faster-lio) | Chunge Bai, Tao Xiao, Yajie Chen, Haoqian Wang, Fang Zhang, Xiang Gao — **prior work, not Genisom**: README says supported by Idriver+ Technologies | IEEE Robotics and Automation Letters 7(2), 2022, pp. 4861–4868, DOI 10.1109/LRA.2022.3152830 (citation as printed in the repo README; publisher page not opened) | LiDAR-inertial odometry built on FAST-LIO2 with incremental sparse voxels; README claims **1.5–2× speed-up**, 1–2 kHz on solid-state LiDAR. Listed because a (very likely) current Genisom researcher is a co-author. ⚠️ unverified whether Genisom's on-robot SLAM uses it. | Code: [gaoxiang12/faster-lio](https://github.com/gaoxiang12/faster-lio) (GPL-2.0) | T01 T02 |

**Not a paper, but related work by the same researcher:** [Lightning-LM](https://github.com/gaoxiang12/lightning-lm) — ROS 2 Humble LiDAR mapping + localisation package (Faster-LIO front end, loop closure, 3D-to-2D grid map, map partition loading, runs on under one CPU core per its README; Livox config included; tested on another vendor's quadruped data). No licence file found, no paper. ⚠️ unverified whether it is used in Genisom products — treat it as an optional SLAM building block, not as Genisom software.

## Datasets, models and benchmarks released

No dataset and no benchmark. Released artifacts are code, simulation assets and one set of model checkpoints.

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| GA-WM checkpoints (5 files: TwoRoom, Reacher, PushT, Cube, Cube with BC-init; about 394 MB) | Model weights for the world-model paper | Not stated on the model card (code is MIT) | [huggingface.co/kikihuang/GA-WM](https://huggingface.co/kikihuang/GA-WM) | Reproducing the paper; checkpoint card reports 100 % / 86 % / 98 % / 88 % / 96 % success. Tabletop and toy-navigation benchmarks — **not** deployable on a robot dog as is |
| `gawm` | Training + evaluation code (Python 3.10, CUDA GPU, `uv`) | MIT | [github.com/zsibot/gawm](https://github.com/zsibot/gawm) | Learning latent world models; research reading, not a 48-hour building block |
| MATRiX (README: runtime release **v1.1.2**, Linux x86_64; marketed as MATRiX 2.0) | Simulator: MuJoCo dynamics (500 Hz target) + Unreal Engine 5 rendering, Zenoh data plane with ROS 2-compatible messages | BSD-3-Clause | [github.com/zsibot/matrix](https://github.com/zsibot/matrix) | Testing navigation, perception and SLAM before touching hardware. Robot models: `xgb`, `xg2` (quadrupeds), `xgw`, `xgw2` (wheel-legged), `zgws`, `zgwt`, `zgwsarm` (with arm), plus Unitree `go2` / `go2w` assets. Maps include Town10World, VeniceWorld, YardWorld, CrowdWorld, HouseWorld (downloaded as DLC) |
| `MATRiX_Python_SDK` | Python SDK for MuJoCo scene simulation and UE state sync | No licence stated | [github.com/zsibot/MATRiX_Python_SDK](https://github.com/zsibot/MATRiX_Python_SDK) | Scripting the simulator from Python |
| `genisom_vln` | Vision-language navigation framework + zero-shot baseline (built on UniGoal); ROS 2 ↔ ZMQ bridge; backends: Hugging Face SmolVLM2-256M, Ollama (e.g. gemma3:4b), cloud APIs | BSD-3-Clause | [github.com/zsibot/genisom_vln](https://github.com/zsibot/genisom_vln) | "Go to the thing in this picture / description" behaviours; fine-tuned agents are marked "todo" in the repo |
| `genisom_roamerx_open` (RoamerX Lite) | ROS 2 Humble / Nav2 navigation stack | BSD-3-Clause (GitHub metadata) | [github.com/zsibot/genisom_roamerx_open](https://github.com/zsibot/genisom_roamerx_open) | Mapping, localisation, waypoint navigation for delivery and patrol builds |
| `genisom_model` | URDF + meshes for `zsl-1` (L1) and `zsl-1w` (L1-W) | BSD-3-Clause | [github.com/zsibot/genisom_model](https://github.com/zsibot/genisom_model) | RViz / Gazebo / Isaac import, custom RL training |

## Third-party papers using their hardware or software

**Papers using Genisom robots or MATRiX: none verified.** No search-engine queries were possible in this run (see coverage note), and no such paper is linked from the company site or its repositories. Ask the Genisom booth and the IROS challenge teams (Manchester 2025, NTU 2026) for write-ups.

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| No verified entry | — | — | — | — | — |

**Third-party research software that supports their hardware (not a paper):** [fan-ziqi/robot_lab](https://github.com/fan-ziqi/robot_lab), an IsaacLab reinforcement-learning extension, ships rough-terrain velocity tasks for **Zsibot ZSL1** (`RobotLab-Isaac-Velocity-Rough-Zsibot-ZSL1-v0`) and **ZSL1W** (`...-ZSL1W-v0`) — the L1 and L1-W under their earlier model names. Useful if a team wants to train its own locomotion policy.

**Upstream papers the Genisom open stack is built on** (third-party work; none of these use Genisom hardware, but they explain what the repos do):

| Paper | Authors / organisation | Venue, year | Where it appears in Genisom's stack | What it shows | Tracks |
|---|---|---|---|---|---|
| [UniGoal: Towards Universal Zero-shot Goal-oriented Navigation](https://arxiv.org/abs/2503.10630) | Hang Yin, Xiuwei Xu, et al., Jiwen Lu | CVPR 2025 | Baseline agent inside `genisom_vln` | One zero-shot method for object-, image- and text-goal navigation using an LLM, no task-specific training | T01 T02 T04 |
| [LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels](https://arxiv.org/abs/2603.19312) | Lucas Maes, Quentin Le Lidec, Damien Scieur, Yann LeCun, Randall Balestriero | arXiv, 2026 | Primary baseline, codebase and datasets of the GAWM paper | End-to-end JEPA world model trained from pixels | — |
| [OGBench: Benchmarking Offline Goal-Conditioned RL](https://arxiv.org/abs/2410.20092) | Seohong Park, Kevin Frans, Benjamin Eysenbach, Sergey Levine | ICLR 2025 | Cube task used to evaluate GAWM | Benchmark suite for offline goal-conditioned RL | — |
| [The Marathon 2: A Navigation System](https://arxiv.org/abs/2003.00368) | Steve Macenski, Francisco Martín, Ruffin White, Jonatan Ginés Clavero | IROS 2020 | Nav2, the base of RoamerX Lite | Behaviour-tree-driven ROS 2 navigation, validated in a long campus run | T01 T02 |
| [SmolVLM: Redefining small and efficient multimodal models](https://arxiv.org/abs/2504.05299) | Andrés Marafioti, Orr Zohar, et al., Thomas Wolf | arXiv, 2025 | Default local VLM (SmolVLM2-256M) in `genisom_vln` | Very small vision-language models that run on edge hardware | T01 T03 |
| [FAST-LIO2: Fast Direct LiDAR-inertial Odometry](https://arxiv.org/abs/2107.06829) | Wei Xu, Yixi Cai, Dongjiao He, Jiarong Lin, Fu Zhang | arXiv, 2021 | Base of Faster-LIO (see above) | Direct LiDAR-inertial odometry that works well with Livox sensors such as the Mid-360 class | T02 |

## Reading list by track

### T01 Autonomous Urban Services
- [The Marathon 2](https://arxiv.org/abs/2003.00368) — RoamerX Lite is Nav2 underneath; knowing behaviour trees, planners and recoveries saves hours when tuning delivery or guiding routes.
- [UniGoal](https://arxiv.org/abs/2503.10630) — the method behind the `genisom_vln` baseline; fastest route to "take me to the reception desk / the object in this photo" concierge behaviour.
- [SmolVLM](https://arxiv.org/abs/2504.05299) — explains the 256M model `genisom_vln` runs locally; tells you what it can and cannot recognise on an Orin NX.
- [Faster-LIO](https://github.com/gaoxiang12/faster-lio) — drop-in LiDAR-inertial odometry if the bundled localisation is not available on the loaned unit.

### T02 Resilient & Safe City
- [FAST-LIO2](https://arxiv.org/abs/2107.06829) and [Faster-LIO](https://github.com/gaoxiang12/faster-lio) — the standard recipe for a 3D map / digital twin from the robot's LiDAR + IMU in an afternoon.
- [The Marathon 2](https://arxiv.org/abs/2003.00368) — waypoint patrol and inspection routes with recovery behaviours.
- [UniGoal](https://arxiv.org/abs/2503.10630) — goal-directed exploration ("find the fire extinguisher / the person") for search tasks; test it in MATRiX first.

### T03 Sustainable City
- No directly relevant paper found (nothing from Genisom on waste, energy or environmental monitoring).
- Nearest useful read: [SmolVLM](https://arxiv.org/abs/2504.05299) — low-power on-board vision-language model, relevant to the "low-power edge AI" angle (for example litter or meter recognition on a patrolling robot).

### T04 Elderly Care & Rehabilitation
- No directly relevant paper found (no assistive, rehabilitation or human-interaction research from Genisom or on its hardware).
- Nearest useful read: [UniGoal](https://arxiv.org/abs/2503.10630) — "find and go to" behaviours for a fetch-and-follow companion built on `genisom_vln`.

## White papers, patents and technical reports

- **White papers / technical reports:** none found on the company site or GitHub. The closest thing to technical reports is the MATRiX documentation set in the repo (sensor schemes, motion control, controller guide, LiDAR–camera projection, Docker and pixel-streaming tutorials).
- **Patents:** not searched in this run (no search budget); none are cited on the pages opened.
- **Unpublished technology names** seen in company news with no paper or repo behind them: SomaMind (agent system), GSD (Genisom Self-Driving navigation), "dual-brain" architecture — see the [company profile](Genisom-AI.md).

## Sources
- [arXiv 2609.03565 — abstract page](https://arxiv.org/abs/2609.03565)
- [arXiv 2609.03565 — HTML version (author affiliations)](https://arxiv.org/html/2609.03565)
- [zsibot/gawm (README, citation block)](https://github.com/zsibot/gawm)
- [Hugging Face — kikihuang/GA-WM checkpoints](https://huggingface.co/kikihuang/GA-WM)
- [LeWM data collection on Hugging Face](https://huggingface.co/collections/quentinll/lewm)
- [GitHub organisation zsibot](https://github.com/zsibot/)
- [zsibot/matrix (README)](https://github.com/zsibot/matrix)
- [zsibot/matrix — Robots and Maps doc](https://github.com/zsibot/matrix/blob/main/docs/Robots_and_Maps.md)
- [zsibot/genisom_vln (README and docs/guide.md)](https://github.com/zsibot/genisom_vln)
- [zsibot/genisom_roamerx_open](https://github.com/zsibot/genisom_roamerx_open)
- [zsibot/genisom_model](https://github.com/zsibot/genisom_model)
- [zsibot/MATRiX_Python_SDK](https://github.com/zsibot/MATRiX_Python_SDK)
- [Genisom AI — Official Open Source page](https://www.genisomai.com/en/opensource)
- [Genisom AI — Education and research](https://www.genisomai.com/en/education-research)
- [Genisom AI — About (Chinese)](https://www.genisomai.com/aboutus.html)
- [IROS 2026 press release via TNGlobal](https://technode.global/prnasia/genisom-ai-showcases-embodied-intelligence-and-debuts-worlds-first-industry-grade-educational-quadruped-at-iros-2026/)
- [gaoxiang12/faster-lio (README, citation)](https://github.com/gaoxiang12/faster-lio)
- [gaoxiang12/lightning-lm (README)](https://github.com/gaoxiang12/lightning-lm)
- [gaoxiang12/slambook2 (README)](https://github.com/gaoxiang12/slambook2)
- [bagh2178/UniGoal (README)](https://github.com/bagh2178/UniGoal)
- [arXiv 2503.10630 — UniGoal](https://arxiv.org/abs/2503.10630)
- [lucas-maes/le-wm (README)](https://github.com/lucas-maes/le-wm)
- [arXiv 2603.19312 — LeWorldModel](https://arxiv.org/abs/2603.19312)
- [arXiv 2410.20092 — OGBench](https://arxiv.org/abs/2410.20092)
- [arXiv 2003.00368 — The Marathon 2](https://arxiv.org/abs/2003.00368)
- [arXiv 2504.05299 — SmolVLM](https://arxiv.org/abs/2504.05299)
- [arXiv 2107.06829 — FAST-LIO2](https://arxiv.org/abs/2107.06829)
- [fan-ziqi/robot_lab (README)](https://github.com/fan-ziqi/robot_lab)
