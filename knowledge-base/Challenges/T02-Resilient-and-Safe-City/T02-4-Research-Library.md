---
type: track-research-library
challenge: T02
challenge_title: "Resilient & Safe City"
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, papers]
---
# T02 Resilient & Safe City — Research Library

> Compiled 2026-11-14 15:57: papers relevant to this track, per company (company-authored and third-party work on their hardware).

[Start here](../../00-START-HERE.md) · [Track overview](T02-0-Track-Overview.md) · [Hardware shortlist](T02-2-Hardware-Shortlist.md)

## Unitree Robotics

**Reading list from the company papers doc:**

- **[Agile But Safe](https://arxiv.org/abs/2401.17583)** — safety-switch idea for fast patrol without collisions (Go1).
- **[Commonsense Reasoning for Legged Robot Adaptation](https://arxiv.org/abs/2407.02666)** — VLM-in-the-loop skill selection for debris, gaps and dead ends; easy to prototype on top of high-level SDK commands.
- **[Open-TeleVision](https://arxiv.org/abs/2407.01512)** + **[xr_teleoperate](https://github.com/unitreerobotics/xr_teleoperate)** — hazardous-environment teleoperation of a G1 from a headset, working code today.
- **[Point-LIO](https://onlinelibrary.wiley.com/doi/epdf/10.1002/aisy.202200459)** + **[point_lio_unilidar](https://github.com/unitreerobotics/point_lio_unilidar)** — 3D mapping / digital twin from the Unitree L1 / L2 LiDAR.
- **[Robot Parkour Learning](https://arxiv.org/abs/2309.05665)** / **[Extreme Parkour](https://arxiv.org/abs/2309.14341)** — what rubble-style terrain is feasible; do not retrain in 48 h, use the factory gait.
- **[LOVON](https://arxiv.org/abs/2507.06747)** — open-vocabulary target search, maps directly to "find the victim / find the hazard sign".

→ [All papers of Unitree Robotics](../../Companies/Unitree/Unitree-Papers-and-Research.md)

## Genisom AI

**Reading list from the company papers doc:**

- [FAST-LIO2](https://arxiv.org/abs/2107.06829) and [Faster-LIO](https://github.com/gaoxiang12/faster-lio) — the standard recipe for a 3D map / digital twin from the robot's LiDAR + IMU in an afternoon.
- [The Marathon 2](https://arxiv.org/abs/2003.00368) — waypoint patrol and inspection routes with recovery behaviours.
- [UniGoal](https://arxiv.org/abs/2503.10630) — goal-directed exploration ("find the fire extinguisher / the person") for search tasks; test it in MATRiX first.

→ [All papers of Genisom AI](../../Companies/Genisom-AI/Genisom-AI-Papers-and-Research.md)

## Magiclab Robotics

**No directly relevant paper found.** The company's five arXiv preprints (Sep–Oct 2026) are all about manipulation models on table-top arms; none covers legged locomotion, navigation, SLAM, inspection, patrol or rescue. An arXiv metadata query for "MagicDog" and "MagicBot" returned **no third-party paper**. The two items below are the nearest useful reading (both opened on arXiv in this run).

| Paper (title as a link) | Authors / organisation | Venue, year | Why it matters here | Code / data |
|---|---|---|---|---|
| [Toward Real-Time VLAs: Stage-Aware Two-Step Flow Denoising and System-Level Evaluation](https://arxiv.org/abs/2609.39822) | Di Wu, Rongtian Shen, Ping Liu, …, Tao Zhang — Magiclab Robotics with university co-authors | arXiv 2609.39822, Sep 2026 (preprint) | Company-authored. Its camera-to-motion latency measurement transfers directly to checking whether a teleoperation or remote-inference link is fast enough for a response robot | [Inference runtime, Apache-2.0](https://github.com/MagiclabRobotics/Inference) |
| [TWIST: Teleoperated Whole-Body Imitation System](https://arxiv.org/abs/2505.02833) | Yanjie Ze, Zixuan Chen, João Pedro Araújo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, C. Karen Liu (Stanford / SFU) | arXiv 2505.02833, May 2025 | Third-party, **not** on MagicLab hardware; cited by MagicLab's motion-retargeting repo. Background for whole-body humanoid teleoperation in hazardous tasks | [pico_teleoperate (MagicLab tooling)](https://github.com/MagiclabRobotics/pico_teleoperate) |

Full list of company papers and repos: [Papers and research](../../Companies/Magiclab/Magiclab-Papers-and-Research.md).

**Reading list from the company papers doc:**

No directly relevant paper found (nothing on inspection, patrol, search and rescue, mapping or legged locomotion). Closest useful items:
- [TWIST](https://arxiv.org/abs/2505.02833) plus the [`pico_teleoperate`](https://github.com/MagiclabRobotics/pico_teleoperate) repo — background and tooling for a hazardous-environment teleoperation demo on a humanoid.
- [Toward Real-Time VLAs](https://arxiv.org/abs/2609.39822) — its latency-measurement method (camera, network, robot response) transfers directly to judging whether a teleoperation or remote-inference link is fast enough.

→ [All papers of Magiclab Robotics](../../Companies/Magiclab/Magiclab-Papers-and-Research.md)

## SKYLANDX

**Reading list from the company papers doc:**

- **GVINS (T-RO 2022)** — robust state estimation when satellites drop out; the published background to the "GPS-denied" claim.
- **Teach-Repeat-Replan (T-RO 2020)** — explicitly motivated by infrastructure inspection and search-and-rescue; shows global map + local replanning around unmapped obstacles.
- **RAPTOR (T-RO 2021)** — perception-aware replanning for fast flight in unknown clutter (T02.6); a reference for what "safe at speed with limited sensing" requires.
- **LiVisSfM (arXiv 2024)** — evidence of the reconstruction accuracy reachable from MetaCam data; relevant if your demo is scan-to-scan change detection (T02.3).
- **Real-time dense stereo embedded in a UAV for road inspection (UAVision 2019)** — a compact example of robot-carried surface-damage inspection (T02.3).
- **Wanderland (CVPR 2026)** — its indoor–outdoor capture protocol and geometry-quality findings apply to digital twins for emergency planning.

→ [All papers of SKYLANDX](../../Companies/SKYLANDX/SKYLANDX-Papers-and-Research.md)

## AGIBOT

**Reading list from the company papers doc:**

- [Learning to Live (LIFE)](https://arxiv.org/abs/2611.00180) — robot-agnostic streaming detector for user-defined conditions ("smoke", "person on the floor"); the released code runs on any webcam, so it also fits a D1 patrol dog.
- [Genie Sim 3.0](https://arxiv.org/abs/2601.02078) — its 3DGS reconstruction pipeline is a route to a quick digital twin of a room or corridor.
- [SONIC](https://arxiv.org/abs/2511.07820) with AGIBOT's `sonic_for_a3` port — whole-body humanoid teleoperation, relevant to hazardous-environment remote work (only if an A3 is available).
- No AGIBOT-authored paper on quadruped patrol, inspection, mapping or search and rescue was found; use the D1 SDK docs rather than papers.

→ [All papers of AGIBOT](../../Companies/AGIBOT/AGIBOT-Papers-and-Research.md)

## D-Robotics

**Reading list from the company papers doc:**

- [WM-LOCO](https://arxiv.org/abs/2609.02542): humanoid walking on stepping stones and stairs, tested on a Unitree G1 (T02.6). Unitree robots are on site; note it ran on a Jetson, not an RDK.
- [GeoFlow-SLAM](https://arxiv.org/abs/2503.14247): SLAM that holds up on a fast-moving quadruped in texture-poor places.
- [Humanoid-OmniOcc](https://arxiv.org/abs/2606.22971) and [FoundationSSC](https://arxiv.org/abs/2508.13601): how to turn stereo cameras into a 3D occupancy map for safe movement. Use `dstereo_occnet` for the on-board version.
- [DOSOD](https://arxiv.org/abs/2412.14680): prompt for hazards ("fire extinguisher", "person lying down", "fallen rock") on a low-power node.
- [TrustVLA](https://arxiv.org/abs/2607.12571): short read on why an unaudited robot policy is a safety risk; good pitch material.

→ [All papers of D-Robotics](../../Companies/D-Robotics/D-Robotics-Papers-and-Research.md)

## Omnicor AI

**Reading list from the company papers doc:**

- **No directly relevant paper found** (nothing from OmniCor; none of the model papers targets rescue, inspection or security).
- Closest useful background for the "works when the network is down" argument (T02.4, T02.7): [EdgeVLA](https://arxiv.org/abs/2507.14049) for fast edge inference, and [Qwen3](https://arxiv.org/abs/2505.09388) (0.6B-class models) or [Apertus](https://arxiv.org/abs/2509.14233) for an offline multilingual operator assistant.

→ [All papers of Omnicor AI](../../Companies/Omnicor-AI/Omnicor-AI-Papers-and-Research.md)

## UniX AI

**Reading list from the company papers doc:**

- No directly relevant paper found.
- Closest, as background only: [Touch and Go](https://arxiv.org/abs/2211.12498) (surface-material recognition from touch could support T02.3 infrastructure checks) and [TaRF](https://arxiv.org/abs/2405.04534) (predicting surface feel across a scanned scene). Neither is practical in 48 hours.

→ [All papers of UniX AI](../../Companies/UniX-AI/UniX-AI-Papers-and-Research.md)

## WUJI

**Reading list from the company papers doc:**

- [DexPilot](https://arxiv.org/abs/1910.03135) — the retargeting cost behind glove-to-hand teleoperation; helps when tuning pinch and thumb behaviour for valves and switches.
- [AnyTeleop](https://arxiv.org/abs/2307.04577) — system design for remote arm + hand operation, including latency handling.
- [Geometric Retargeting](https://arxiv.org/abs/2503.07541) — fast learned alternative if the built-in retargeting feels wrong for a tool grasp.
- [DexCap](https://arxiv.org/abs/2403.07788) — portable glove data collection, useful for logging operator demonstrations in the field.
- [TopoRetarget](https://arxiv.org/abs/2606.16272) — contact-preserving mapping when the operator handles an object rather than free space.

→ [All papers of WUJI](../../Companies/WUJI/WUJI-Papers-and-Research.md)

## Binabik AI

**Reading list from the company papers doc:**

- [Self-Calibrating Anomaly and Change Detection for Autonomous Inspection Robots](https://arxiv.org/abs/2209.02379): reference-image change detection that needs no retraining; buildable in a day with off-the-shelf SuperPoint / SuperGlue (T02.3, T02.5).
- [AgiPIX](https://arxiv.org/abs/2604.08009): full sim-plus-real pipeline for indoor inspection drones (T02.2).
- [Sim-to-Real Transfer for Mobile Robots with Reinforcement Learning](https://arxiv.org/abs/2501.02902): Isaac Sim to real ROS 2 robot workflow for obstacle avoidance (T02.6).
- [Simulation Analysis of Exploration Strategies and UAV Planning for Search and Rescue](https://arxiv.org/abs/2304.05107): search-pattern comparison and why recall beats precision for victim detection (T02.1).
- [Event-driven Fabric Blockchain – ROS 2 Interface](https://arxiv.org/abs/2304.00781): auditable teleoperation logging, relevant to a human-in-the-loop response story (T02.7).
- [Occupancy-Grounded Room Segmentation](https://arxiv.org/abs/2606.13727): ROS 2 code that turns a map into rooms a responder can refer to by name (T02.4).

→ [All papers of Binabik AI](../../Companies/Binabik-AI/Binabik-AI-Papers-and-Research.md)

## coprod Inc.

**Reading list from the company papers doc:**

No directly relevant paper found from coprod. Closest useful background:

- [Learning to Walk in Minutes](https://arxiv.org/abs/2109.11978) — terrain curriculum for rough-ground locomotion (T02.6); the pipeline behind the library coprod forked.
- [RMA](https://arxiv.org/abs/2107.04034) — history-encoder adaptation to slopes, payload and slippery ground (T02.6); explains the encoder + policy pair you see in the co:dodo simulator.
- [RSL-RL](https://arxiv.org/abs/2509.10771) — practical reference if you retrain any legged policy on site.
- [Open torque-controlled modular architecture](https://arxiv.org/abs/1910.00093) — test protocol ideas (impact, torque tracking) for a rugged custom mechanism built from actuator modules.
- [Proprioceptive actuator design](https://doi.org/10.1109/TRO.2016.2640183) — impact mitigation, useful when an actuated tool or mast must survive knocks (T02.2, T02.3).

→ [All papers of coprod Inc.](../../Companies/coprod/coprod-Papers-and-Research.md)

## Dobot Robotics

**Reading list from the company papers doc:**

- [Human-robot shared control on CR10](https://arxiv.org/abs/2606.24629) — smoother, more predictable teleoperation for hazardous-environment manipulation.
- [Phone2Act](https://arxiv.org/abs/2605.01948) — zero-hardware teleop bridge to a Dobot cobot over its TCP real-time port.
- [DobotTrack](https://arxiv.org/abs/2611.09041) — target following from an egocentric camera for patrol or responder-following; runs on Orin Nano.
- [TARCAT](https://arxiv.org/abs/2608.25395) — primitive vocabulary for tool use (screwdriver, hammer, brushing) on a CR3; useful to scope an infrastructure-maintenance demo.
- [SPINE](https://arxiv.org/abs/2607.13049) — how to recover an X-Trainer teleop rig quickly when it breaks mid-event.

→ [All papers of Dobot Robotics](../../Companies/Dobot/Dobot-Papers-and-Research.md)

## Flexiv Robotics

**Reading list from the company papers doc:**

- **[AirExo](https://arxiv.org/abs/2309.14975)** / **[AirExo-2](https://arxiv.org/abs/2503.03081)** — low-cost exoskeleton teleoperation; the pattern for a hazardous-environment remote-handling demo.
- **[Reactive Diffusion Policy](https://arxiv.org/abs/2503.02881)** — the TactAR part: AR headset teleoperation with force feedback from the Rizon's joint torque sensors.
- **[Force Policy](https://arxiv.org/abs/2602.22088)** — connector / plug insertion with regulated force; maps to "mate a connector or turn a valve on damaged infrastructure".
- **[Safety Value-Constrained MPC](https://arxiv.org/abs/2604.23863)** — how to keep a torque-controlled Rizon 10s inside hard safety limits.
- **[ADEPT](https://arxiv.org/abs/2608.19182)** — dexterous-hand insertion on a Rizon, for teams that also have a multi-finger hand.
- No paper found on search-and-rescue, patrol or outdoor inspection with Flexiv hardware.

→ [All papers of Flexiv Robotics](../../Companies/Flexiv/Flexiv-Papers-and-Research.md)

## Galaxea

**Reading list from the company papers doc:**

No directly relevant paper found (nothing on rescue, hazardous inspection or disaster sensing with Galaxea hardware). Closest adjacent work:

- [SafeBimanual](https://arxiv.org/abs/2508.18268) — adds safety constraints to an existing policy at test time; relevant to human-robot collaboration (T02.7).
- [XRoboToolkit](https://arxiv.org/abs/2508.00097) — VR teleoperation of the R1 Lite; basis for an operator-in-the-loop response demo.
- [NavDP](https://arxiv.org/abs/2505.08712) — obstacle-avoiding navigation in clutter; flat ground only on the R1.
- [VR-Robo](https://arxiv.org/abs/2502.01536) — camera-only navigation trained in a reconstructed digital twin.

→ [All papers of Galaxea](../../Companies/Galaxea/Galaxea-Papers-and-Research.md)

## Leadshine Technology

**Reading list from the company papers doc:**

No directly relevant paper found.

→ [All papers of Leadshine Technology](../../Companies/Leadshine/Leadshine-Papers-and-Research.md)

## OriginFlow

**Reading list from the company papers doc:**

- [MI-DHMI teleoperation interface](https://arxiv.org/abs/2609.07495) — closest blueprint for EMG + IMU teleoperation of an arm and five-finger hand over ROS 2 (T02.7).
- [ForceBand](https://arxiv.org/abs/2606.26093) — evidence that sEMG recovers contact for occluded fingers better than vision (ring / pinky contact PR-AUC 0.763 vs 0.398 and 0.590 vs 0.314), the core argument for gloved or smoke-obscured hands.
- [Dual-modality haptic feedback with EMG gripper](https://arxiv.org/abs/2209.15578) — why the operator needs grip-force and slip feedback when the robot hand is remote.
- [Generic neuromotor interface (Meta, Nature 2025)](https://github.com/facebookresearch/generic-neuromotor-interface) — robust discrete-gesture decoding and released checkpoints, a fallback command channel if continuous pose is not available.
- [Beyond Gestures](https://arxiv.org/abs/2609.16518) — alternative wrist sensing for pose + force when skin contact is unreliable.

→ [All papers of OriginFlow](../../Companies/OriginFlow/OriginFlow-Papers-and-Research.md)

## Spirit AI

**Reading list from the company papers doc:**

- No directly relevant paper found (nothing on search and rescue, inspection, security or hazardous-environment teleoperation).
- Nearest enablers: **[ViLa](https://arxiv.org/abs/2311.17842)** / **[CoPa](https://arxiv.org/abs/2403.08248)** for zero-shot "open the valve / press the switch" manipulation, and **[HuMI](https://arxiv.org/abs/2602.06643)** / **[OpenHLM](https://arxiv.org/abs/2606.22174)** if a team works with a Unitree G1 humanoid rather than Moz1.

→ [All papers of Spirit AI](../../Companies/Spirit-AI/Spirit-AI-Papers-and-Research.md)
