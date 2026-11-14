---
type: track-research-library
challenge: T01
challenge_title: "Autonomous Urban Services"
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, papers]
---
# T01 Autonomous Urban Services — Research Library

> Compiled 2026-11-14 15:57: papers relevant to this track, per company (company-authored and third-party work on their hardware).

[Start here](../../00-START-HERE.md) · [Track overview](T01-0-Track-Overview.md) · [Hardware shortlist](T01-2-Hardware-Shortlist.md)

## AGIBOT

**Reading list from the company papers doc:**

- [SOP](https://arxiv.org/abs/2601.03044) — the closest thing to a published "retail robot" recipe: grocery restocking learned by a robot fleet with human corrections.
- [AgiBot World Colosseo / GO-1](https://arxiv.org/abs/2503.06669) — the dataset and open weights you would actually fine-tune for a shop, café or concierge manipulation task.
- [Genie Sim 3.0](https://arxiv.org/abs/2601.02078) — retail, catering and office scenes in sim; lets a team iterate before robot time is available.
- [WholeBodyVLA](https://arxiv.org/abs/2512.11047) — the only verified paper on the **X2**, the robot most likely to be handed to teams; walk-to-and-manipulate.
- [Learning to Live (LIFE)](https://arxiv.org/abs/2611.00180) — RoboBeats gives a concierge / guide robot an "event trigger" on its camera stream and a memory to answer questions later.
- [UniVLA](https://arxiv.org/abs/2505.06111) — how to get a policy from little labelled data (uses video, incl. human video).

→ [All papers of AGIBOT](../../Companies/AGIBOT/AGIBOT-Papers-and-Research.md)

## Galaxea

**Reading list from the company papers doc:**

- [G0.5](https://arxiv.org/abs/2608.11739) — the model you would fine-tune on R1 Lite / R1 Pro; prompts steer task horizon and granularity, useful for fetch, deliver and tidy services (T01.1, T01.2, T01.3).
- [Galaxea Open-World Dataset and G0](https://arxiv.org/abs/2509.00576) — what data exists for retail and office scenes and how the three-stage training recipe works.
- [NavDP](https://arxiv.org/abs/2505.08712) — sim-trained navigation policy already run on the R1 base; closest paper to T01.6.
- [NeSyPack](https://arxiv.org/abs/2506.06567) — competition-winning packing with few demos; a 48-hour-friendly pattern (symbolic task graph + small learned skills) for T01.1.
- [BEHAVIOR Robot Suite](https://arxiv.org/abs/2503.05652) — whole-body teleop and policy for cleaning-type tasks on the R1 (T01.2).
- [VLASH](https://arxiv.org/abs/2512.01031) — how to keep a VLA responsive around people (T01.7).

→ [All papers of Galaxea](../../Companies/Galaxea/Galaxea-Papers-and-Research.md)

## Genisom AI

**Reading list from the company papers doc:**

- [The Marathon 2](https://arxiv.org/abs/2003.00368) — RoamerX Lite is Nav2 underneath; knowing behaviour trees, planners and recoveries saves hours when tuning delivery or guiding routes.
- [UniGoal](https://arxiv.org/abs/2503.10630) — the method behind the `genisom_vln` baseline; fastest route to "take me to the reception desk / the object in this photo" concierge behaviour.
- [SmolVLM](https://arxiv.org/abs/2504.05299) — explains the 256M model `genisom_vln` runs locally; tells you what it can and cannot recognise on an Orin NX.
- [Faster-LIO](https://github.com/gaoxiang12/faster-lio) — drop-in LiDAR-inertial odometry if the bundled localisation is not available on the loaned unit.

→ [All papers of Genisom AI](../../Companies/Genisom-AI/Genisom-AI-Papers-and-Research.md)

## Magiclab Robotics

**No directly relevant paper found** — nothing company-authored or third-party on navigation, delivery, cleaning, guiding or public-space HRI with Magiclab hardware. The company's five arXiv preprints (autumn 2026) are about manipulation policies and were run on AgileX Piper arms, not on MagicBot or MagicDog. The rows below are the nearest useful reading; all four were opened on arXiv today. No third-party paper using MagicDog / MagicBot was confirmed (search coverage limited to two queries).

| Paper (title as a link) | Authors / organisation | Venue, year | Why it matters here | Code / data |
|---|---|---|---|---|
| [Toward Real-Time VLAs: Stage-Aware Two-Step Flow Denoising and System-Level Evaluation](https://arxiv.org/abs/2609.39822) | Di Wu, Rongtian Shen, Ping Liu, Yan Shen, Zhenhan Yin, Shun Zuo, Xuhua Chen, He Zheng, Lingfeng Zhang, Jianglin Zhang, Tao Zhang — Magiclab Robotics and university co-affiliations | arXiv preprint, 30 Sep 2026 | Method for measuring the full camera-to-motion delay chain; useful to judge whether a remote-inference or teleoperation link is fast enough for a service robot among people | [Inference runtime, Apache-2.0](https://github.com/MagiclabRobotics/Inference) |
| [Magic-W0: A Structured World-Action Foundation Model for Physical Intelligence](https://arxiv.org/abs/2609.39870) | Xuhua Chen, Zhenhan Yin, Yuan Zhang, Lingfeng Zhang, He Zheng … Tao Zhang (18 authors) — Magic-Lab Team, Magiclab Robotics | arXiv preprint, 30 Sep 2026 | The company's open manipulation foundation model; only relevant if your service demo needs a learned pick / place / hand-over skill and you have a GPU and demonstrations | [Code, MIT](https://github.com/MagiclabRobotics/Magic-W0) |
| [Dual-Stream Memory for Vision-Language-Action Policies](https://arxiv.org/abs/2610.13262) | Yang Wang, Ping Liu, Ruiyu Wang, Xuhua Chen, Lingfeng Zhang, Tao Zhang — Magiclab Robotics; UCLA | arXiv preprint, 9 Oct 2026 | Task-progress memory for policies ("have I already done this?") — idea transferable to multi-stop delivery or tour state tracking | none found |
| [BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion](https://arxiv.org/abs/2508.08241) | Qiayuan Liao, Takara E. Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, C. Karen Liu (third-party; not Magiclab hardware in the original) | arXiv preprint, Aug 2025 | Magiclab ports it to MagicBot Z1 — the documented route to convincing waving, pointing and greeting motions for a guide robot | [magicbot-mimic, MIT](https://github.com/MagiclabRobotics/magicbot-mimic) |

Also read (not a paper): [In-Context Visual Guidance with Magic-Brain](https://embodied.magiclab.top/works/brain/en.html) — company technical article describing an agent stack with navigation, grasping, interaction and sentinel agents, a task graph with up to three re-plans, and separate interrupt (pause / abort / e-stop) and steering channels. A ready architecture sketch for a concierge or delivery robot; no code released. More detail and the full paper list: [Papers and research](../../Companies/Magiclab/Magiclab-Papers-and-Research.md).

**Reading list from the company papers doc:**

- [In-Context Visual Guidance with Magic-Brain](https://embodied.magiclab.top/works/brain/en.html) (company article) — describes an agent stack with separate **navigation, grasping, interaction and "sentinel" agents**, a task DAG with re-planning, and pause / abort / e-stop buses; a ready-made architecture sketch for a concierge or delivery robot.
- [π0](https://arxiv.org/abs/2410.24164) with the [`magicbot-gen1_pi0_demo`](https://github.com/MagiclabRobotics/magicbot-gen1_pi0_demo) repo — the documented way to teach a MagicLab humanoid a service manipulation skill from teleoperated demos.
- [BeyondMimic](https://arxiv.org/abs/2508.08241) — if you want Z1 to wave, point or greet convincingly in a guide-robot demo.
- No company paper on navigation, SLAM or delivery was found; use the ROS 2 SDK docs instead (see the [Developer guide](../../Companies/Magiclab/Magiclab-Developer-Guide.md)).

→ [All papers of Magiclab Robotics](../../Companies/Magiclab/Magiclab-Papers-and-Research.md)

## Unitree Robotics

**Reading list from the company papers doc:**

- **[Uni-NaVid](https://arxiv.org/abs/2412.06224)** — closest to a ready recipe for a Go2 concierge: language instructions, object search and human following from one camera, using Unitree's stock local controller.
- **[NaVILA](https://arxiv.org/abs/2412.04453)** — shows the split you should copy: a VLM emits "move forward 75 cm / turn left 30°" and the built-in locomotion executes it.
- **[LOVON](https://arxiv.org/abs/2507.06747)** — plug-and-play LLM + open-vocabulary detector on Go2 / B2; a realistic 48 h architecture for "find and go to X".
- **[WildLMa](https://arxiv.org/abs/2411.15131)** and **[Helpful DoggyBot](https://arxiv.org/abs/2410.00231)** — fetch / deliver / tidy with a quadruped plus arm or mouth gripper.
- **[PRELUDE](https://arxiv.org/abs/2209.09233)** — walking among pedestrians (dynamic obstacles) with a small quadruped.
- Not a paper but directly usable: **[unitree_robotskills](https://github.com/unitreerobotics/unitree_robotskills)** (agent + SDK tools, language navigation skill).

→ [All papers of Unitree Robotics](../../Companies/Unitree/Unitree-Papers-and-Research.md)

## UniX AI

**Reading list from the company papers doc:**

- [UniTac](https://arxiv.org/abs/2606.31451) — the only paper with a UniX AI affiliation; its towel-selection and cup-grasp experiments are the closest published thing to the housekeeping and tea-service skills the company demos (T01.2, T01.3). Read sections 4.5 and appendix B.1 for the task definitions and success criteria.
- No directly relevant paper found for navigation, guidance, delivery or public-space interaction (T01.1, T01.4–T01.7). UniX's key-point imitation learning (UniFlex), which is what powers its hotel skills, is unpublished.

→ [All papers of UniX AI](../../Companies/UniX-AI/UniX-AI-Papers-and-Research.md)

## Binabik AI

**Reading list from the company papers doc:**

- [Data Scaling for Navigation in Unknown Environments](https://arxiv.org/abs/2601.09444): sidewalk-robot navigation without a map, with code and models; the nearest thing here to a delivery baseline (T01.1, T01.6).
- [Synthetic vs. Real Training Data for Visual Navigation](https://arxiv.org/abs/2509.11791): FAINT weights are downloadable and run in real time on robot hardware (T01.6).
- [Aion](https://arxiv.org/abs/2512.11903) and [Kairos](https://arxiv.org/abs/2609.27467): how to plan around where people usually walk; MIT code (T01.3, T01.7).
- [Towards Embodied Agentic AI](https://arxiv.org/abs/2508.05294): quick map of LLM-agent architectures for a guidance or information robot (T01.5, T01.7).
- [ROSBag MCP Server](https://arxiv.org/abs/2511.03497): the one Binabik tool you can install in minutes; also tells you which LLMs call tools reliably.
- [ReGATE](https://arxiv.org/abs/2611.02871): box pick-carry-place on a Unitree G1, useful if a team attempts humanoid delivery (T01.1).

→ [All papers of Binabik AI](../../Companies/Binabik-AI/Binabik-AI-Papers-and-Research.md)

## D-Robotics

**Reading list from the company papers doc:**

- [DOSOD](https://arxiv.org/abs/2412.14680): text-prompted detection at 47 FPS on RDK X5. Lets a service or inspection robot look for "wheelchair", "parcel", "spill" without training a model.
- [X-Lens](https://arxiv.org/abs/2607.12993): one small model for depth from fisheye + pinhole cameras; weights are public (non-commercial licence).
- [FSR-VLN](https://arxiv.org/abs/2509.13733): a workable recipe for "guide me to X" robots (T01.5): scene graph first, VLM only at the end.
- [SkillNav](https://arxiv.org/abs/2607.15758): cheap fixes for VLM navigators that get stuck or loop (T01.6).
- [HoloAgent-0](https://arxiv.org/abs/2606.23565): architecture reference for a language-driven robot agent with re-planning (code public).
- [Debris detection on RDK X5](https://doi.org/10.3390/s26144386): a full, published INT8 deployment recipe on the board most teams will get.

→ [All papers of D-Robotics](../../Companies/D-Robotics/D-Robotics-Papers-and-Research.md)

## Dobot Robotics

**Reading list from the company papers doc:**

- [DobotTrack](https://arxiv.org/abs/2611.09041) — language-specified person following with public code and weights; the fastest route to a "guide / follow-me / carry-behind" behaviour on any mobile base with a front camera.
- [DobotRoam repo](https://github.com/Dobot-Team/dobot_roam) — same team's waypoint-output navigation policy; read the README for the interface (RGB history + instruction → 8 waypoints) even if you do not train it.
- [Video + speech + LLM HRI on Dobot Magician](https://arxiv.org/abs/2602.20219) — a complete open-model recipe for voice-commanded pick-and-place at a service counter.
- [Phone2Act](https://arxiv.org/abs/2605.01948) — collect 100+ demonstrations on a CR5 with a phone and fine-tune a VLA inside the 48 hours.
- [GM-100](https://arxiv.org/abs/2601.11421) — task designs and X-Trainer baselines to pick a manipulation task that is hard but feasible.

→ [All papers of Dobot Robotics](../../Companies/Dobot/Dobot-Papers-and-Research.md)

## Flexiv Robotics

**Reading list from the company papers doc:**

- **[AnyGrasp](https://arxiv.org/abs/2212.08333)** — fastest route to "pick up whatever is in front of the camera"; SDK available, already run on a Rizon.
- **[Flexible Handover](https://arxiv.org/abs/2308.15622)** — taking an item from a person's moving hand; template for a concierge / retail hand-over demo.
- **[RISE](https://arxiv.org/abs/2404.12281)** and **[CAGE](https://arxiv.org/abs/2410.14974)** — imitation policies trained from tens of demos; code targets the Rizon + RealSense setup you are likely to get.
- **[History-Aware Policy](https://arxiv.org/abs/2509.17141)** — read if your service task has repeated steps (stock three shelves, press a button twice).
- **[VAMPS](https://arxiv.org/abs/2610.05331)** — whiteboard erasing is a small-scale surface-cleaning task with force in the loop.

→ [All papers of Flexiv Robotics](../../Companies/Flexiv/Flexiv-Papers-and-Research.md)

## Leadshine Technology

**Reading list from the company papers doc:**

No directly relevant paper found for Leadshine's hands or joint modules. Closest material:
- [Precast-concrete surface robot (Sensors 2024)](https://doi.org/10.3390/s24113336) — coverage path planning around obstacles with A* dead-zone escape; the planner idea transfers to cleaning / maintenance coverage (T01.2, T01.6).
- General background, not Leadshine-specific and does not mention Leadshine: [Dexterous Robotic Hands in the Foundation-Model Era: A Full-Stack Survey (arXiv 2611.06724, Ji Pei, Nov 2026)](https://arxiv.org/abs/2611.06724) — orientation on data collection, retargeting and evaluation if you put a DH-series hand on a service robot.

→ [All papers of Leadshine Technology](../../Companies/Leadshine/Leadshine-Papers-and-Research.md)

## Omnicor AI

**Reading list from the company papers doc:**

- [OpenVLA](https://arxiv.org/abs/2406.09246) — the baseline for language-conditioned pick / place / hand-over; its quantisation result is the evidence that quantised serving can keep success rate (T01.1, T01.3).
- [OpenVLA-OFT](https://arxiv.org/abs/2502.19645) — if OpenVLA is too slow on your robot, this recipe gives 26x throughput with chunked actions (T01.3).
- [Real-time chunking](https://arxiv.org/abs/2506.07339) — how to keep motion smooth when on-board inference is slower than the control loop; no retraining needed (T01.6, T01.7).
- [Apertus](https://arxiv.org/abs/2509.14233) and [Qwen3](https://arxiv.org/abs/2505.09388) — local multilingual LLMs for a guidance / information robot without cloud access (T01.5).
- [SmolVLA](https://arxiv.org/abs/2506.01844) — realistic to fine-tune inside 48 h on one GPU.

→ [All papers of Omnicor AI](../../Companies/Omnicor-AI/Omnicor-AI-Papers-and-Research.md)

## SKYLANDX

**Reading list from the company papers doc:**

- **Wanderland (CVPR 2026)** — the closest thing to a recipe for T01.6 / T01.1: scan a street or corridor with a MetaCam, build a 3DGS + USDZ scene, and evaluate a navigation policy in closed loop before touching a robot. Code and data are Apache-2.0.
- **wanderland-lab README** — read this rather than the paper if you only have an hour: installation, the `Policy` interface, KPIs.
- **VINS-Fusion, global pose paper** — how to fuse a local odometry source with GNSS in a pose graph; useful when a delivery robot crosses between sky-view and covered areas.
- **GVINS (T-RO 2022)** — indoor ↔ outdoor transitions with intermittent GNSS; relevant to a village route that passes through arcades or buildings.
- **Teach-Repeat-Replan (T-RO 2020)** — the "teach a route once, repeat it safely" pattern maps directly onto a scan-once, relocalize-later delivery demo.

→ [All papers of SKYLANDX](../../Companies/SKYLANDX/SKYLANDX-Papers-and-Research.md)

## Spirit AI

**Reading list from the company papers doc:**

- **[Spirit-v1.5 blog](https://www.spirit-ai.com/en/blog/spirit-v1-5)** — what the open model can and cannot do, and how to collect teleop data that transfers (diverse, goal-driven sessions rather than repeated scripts).
- **[Point-VLA](https://arxiv.org/abs/2512.18933)** — "fetch *that* one": box-on-image instructions fix the ambiguity that breaks text-only VLAs in cluttered retail / concierge scenes.
- **[CoPa](https://arxiv.org/abs/2403.08248)** + **[ViLa](https://arxiv.org/abs/2311.17842)** — no training needed: VLM planning plus part-level grasp constraints. The most realistic recipe for a 48-hour build on Moz1's SDK.
- **[OneTwoVLA](https://arxiv.org/abs/2505.11917)** — pattern for long multi-step service tasks: act fast, reason only at decision points.
- **[Data Scaling Laws](https://arxiv.org/abs/2410.18647)** — if you do collect demos, vary environments and objects; do not pile up repeats of one setup.

→ [All papers of Spirit AI](../../Companies/Spirit-AI/Spirit-AI-Papers-and-Research.md)

## coprod Inc.

**Reading list from the company papers doc:**

No directly relevant paper found from coprod. Closest useful background:

- [LeRobot library paper](https://arxiv.org/abs/2602.22818) — fastest route to a learned manipulation skill for a service robot (T01.3, T01.7); coprod's own team has used it on SO-100 arms.
- [Robot Learning: A Tutorial](https://arxiv.org/abs/2510.12403) — read the imitation-learning chapters before recording your first demonstrations.
- [ACT / low-cost bimanual manipulation](https://arxiv.org/abs/2304.13705) — how many demonstrations and which action representation you need for a hand-over or dispensing task (T01.1, T01.3).

For T01.6 navigation and path planning coprod offers nothing; use another vendor's stack and papers.

→ [All papers of coprod Inc.](../../Companies/coprod/coprod-Papers-and-Research.md)

## OriginFlow

**Reading list from the company papers doc:**

- [OriginData preview sample (dataset card)](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample) — the only OriginFlow asset you can build on without their hardware; packing, shelf-organising and hand-over style tasks fit T01.1 / T01.3.
- [ForceBand](https://arxiv.org/abs/2606.26093) — shortest path from wrist sEMG to a force-aware pick-and-place policy; code and BOM are open.
- [Universal Manipulation Interface](https://arxiv.org/abs/2402.10329) — baseline for "record a human demo, replay on a robot" (T01.1, T01.2).
- [EgoScale](https://arxiv.org/abs/2602.16710) — how far egocentric video alone goes; useful framing for what force data adds.
- [Deep Patch Visual Odometry](https://arxiv.org/abs/2208.04726) — only if you need head / camera trajectory from the Glass video yourself.

→ [All papers of OriginFlow](../../Companies/OriginFlow/OriginFlow-Papers-and-Research.md)

## WUJI

**Reading list from the company papers doc:**

- [pi0.5](https://arxiv.org/abs/2504.16054) — the model `wuji-openpi` fine-tunes; read with the [wuji-openpi README](https://github.com/wuji-technology/wuji-openpi) to judge whether a few dozen teleop demos of a service task (hand over, press, open) are feasible in the time.
- [pi0](https://arxiv.org/abs/2410.24164) — explains action chunking and why the fork adds chunk-boundary smoothing.
- [AnyTeleop](https://arxiv.org/abs/2307.04577) — camera-only teleop; the fallback if no glove is free.
- [TopoRetarget](https://arxiv.org/abs/2606.16272) — only if you plan to script a contact-rich hand skill from a recorded human demo.

→ [All papers of WUJI](../../Companies/WUJI/WUJI-Papers-and-Research.md)
