---
type: papers
company: "Dobot Robotics"
slug: Dobot
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# Dobot Robotics — Papers and Research

⬆ [Dobot Robotics profile](Dobot.md) · [Solutions and projects](Dobot-Solutions-and-Projects.md) · [Developer guide](Dobot-Developer-Guide.md)

> **Coverage note (read this first).** General web search was unavailable for this pass (search quota exhausted), so discovery relied on primary catalogues only: arXiv's own listing (title / abstract / author metadata), Dobot's GitHub organisations, Hugging Face listings and Dobot's official news pages. Every paper below was opened on arXiv. **Not covered:** papers that name Dobot hardware only in the full text, and non-arXiv journals (MDPI, IEEE Xplore, Springer) where most Dobot Magician sorting / rehabilitation / education papers live. Treat the third-party list as a verified minimum, not a complete census.

## Research footprint

- **Product-first company that started publishing in 2026.** Only **2 arXiv papers** with a Dobot Robotics affiliation were found, both from Aug–Nov 2026. No earlier company-authored paper, and no paper for the flagship models **DobotWAM** or **ROM-1**, was found; Dobot's own news calls DobotWAM "proprietary".
- **A second GitHub organisation, [Dobot-Team](https://github.com/Dobot-Team), is the research outlet.** It hosts the navigation / tracking VLA work (DobotTrack, DobotRoam) and the legged-robot stack (quadruped SDK, RL training and sim2real, hexapod SDK). The older [Dobot-Arm](https://github.com/Dobot-Arm) organisation holds arm, X-Trainer and Atom SDKs.
- **Named research people (from paper author lists):** Pengkun Zheng (project lead on DobotTrack and DobotRoam), Chengrui Wei, Liu Liang, Songyuan Liu, Yajun Zheng, Ying Zhang, Yuan Tian, Xi Li (also co-author of the Atom tennis paper). Three of these names also appear on 2026 world-model driving papers (X-Mind, X-Foresight) — name match only, affiliation there not checked ⚠️ unverified.
- **Academic links seen in papers and news:** Tsinghua University, The University of Hong Kong and Foshan University (DobotTrack co-authors); Shanghai AI Laboratory, Shanghai Jiao Tong University and Noitom Robotics (Atom tennis paper). Dobot's news also names a "DOBOT Global Education and Advanced Research Institute" that ran an education forum with Fraunhofer institutes, TUM and Tecnalia (Oct 2026).
- **Open-source posture: code and small demo data are open, foundation models are closed.** Open: SDKs (MIT / GPL-3.0 / BSD-3), DobotTrack code and weights, LeRobot-format demo datasets and one ACT checkpoint on Hugging Face. Closed: DobotWAM, ROM-1. Several brand-new Hugging Face repos are still empty placeholders.

## Company-authored and company-affiliated papers

| Paper | Authors / organisation | Venue, year | What it contributes | Artifacts | Tracks |
|---|---|---|---|---|---|
| [DobotTrack: Target-Grounded Vision-Language-Action Learning for Embodied Person Tracking](https://arxiv.org/abs/2611.09041) | S. Deng, Y. Zhang, C. Wei, L. Liang, S. Liu, P. Zheng, Y. Zheng, Y. Zhang, Y. Tian, X. Li, T. Wang — Foshan Univ., Tsinghua, **Dobot Robotics**, HKU | arXiv preprint (cs.RO), 6 Nov 2026 | **0.8B-parameter** VLA (built on InternVL3) that follows a person described in natural language; mask + box grounding supervision and a "Q-identity" history compressor. **77.9%** average success on EVT-Bench (**+16.9 pp** over OmTrackVLA). Deployed on a quadruped with front cameras, LiDAR and an onboard **Jetson Orin Nano**. Real-world dataset: **126 episodes, 596,323 mask-annotated frames** (about 10.2 h) | ✅ Code: [Dobot-Team/dobot_track](https://github.com/Dobot-Team/dobot_track) (training + Habitat evaluation; no licence file found ⚠️) · ✅ Weights: [dddsky/dobottrack](https://huggingface.co/dddsky/dobottrack) (linked from the official README, released 2026-11-11; licence not stated) · 🔭 Real-world dataset marked "coming soon" · Project page: [dobottrack-web](https://dobot-team.github.io/dobottrack-web/) | T01 T02 T04 |
| [Towards Professional Tennis Styles for Humanoid Robots with Adaptive Motion Planning and Tracking (AdaPT)](https://arxiv.org/abs/2608.20087) | T. Huang, R. Liu, X. Tang, X. Zhang, J. Ren, H. Wang, F. Jia, Y. Qi, K. Yin, W. Zeng, L. Chen, **X. Li (Dobot Robotics)**, T. Wu, K. Li, R. Dai, J. Wang, L. Han, J. Pang — Noitom Robotics, Shanghai AI Laboratory, SJTU, Dobot Robotics | arXiv preprint (cs.RO), 20 Aug 2026 | Hierarchical planner + tracker that learns tennis serve and rally styles from broadcast video; validated on Unitree G1 and **deployed on the full-size Dobot Atom (about 1.7 m per the paper)** for in-the-wild serving without motion capture. Acknowledges the Dobot engineering team for ball and robot localisation | Project page: [humanoidtennis.github.io/AdaPT](https://humanoidtennis.github.io/AdaPT/) (abstract says videos and code are available there; not inspected) | — |

**Company research without a paper (verified repositories / announcements):**

| Item | Status | What is public | Tracks |
|---|---|---|---|
| **DobotRoam** — "Roaming and Motion-Intent Navigation with a Shared Vision-Language-Action Policy" (C. Wei, S. Liu, L. Liang, P. Zheng, all Dobot Robotics) | 🧪 README-level technical write-up, updated 2026-11-05; **no arXiv paper found** | [Dobot-Team/dobot_roam](https://github.com/Dobot-Team/dobot_roam): Qwen3.5-0.8B backbone, one ACT token, shared head predicting **8 egocentric waypoints (x, y, yaw) over 2.4 s**; two tasks ("Roam", "Motion Intent" such as "Turn right"). Only open-loop visualisations are shown; README states no robot actuation is shown. Weights and licence not confirmed ⚠️ | T01 T02 |
| **Kongyi DobotWAM** (embodied foundation model powering LUMO) | 🧪 announced Jun 2026; proprietary | Official description only: builds on vision-language-action modelling with 3D spatial understanding, motion constraints and closed-loop real-world data. **No paper, code or weights found.** The 99.25% LIBERO figure in the profile comes from secondary press and could not be re-opened in this pass ⚠️ unverified | — |
| **ROM-1** (operator model on Atom, per the company profile) | ✅ in product; proprietary | No paper, code or weights found | — |

## Datasets, models and benchmarks released

**Official Dobot releases**

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| DobotTrack code | Training + Habitat (EVT-Bench) evaluation code | No licence file found ⚠️ | [GitHub](https://github.com/Dobot-Team/dobot_track) | Person-following / "follow me" policy on a mobile base (T01, T02, T04) |
| DobotTrack weights | VLA checkpoint (InternVL3-1B based, 448×448 input, 7 history frames + current) | Not stated | [Hugging Face](https://huggingface.co/dddsky/dobottrack) | Same; small enough for Jetson Orin Nano per the paper |
| DobotTrack real-world dataset | 126 quadruped following episodes, mask-annotated | 🔭 "coming soon" | [repo README](https://github.com/Dobot-Team/dobot_track) | Not available yet |
| DobotRoam | Navigation VLA training code and docs | Not found ⚠️ | [GitHub](https://github.com/Dobot-Team/dobot_roam) | Instruction-conditioned roaming / heading intent on a mobile robot |
| dobot_rover_simulation | RL training (legged_gym refactor, Isaac Gym), MuJoCo sim2sim, ONNX export, sim2real deployment for the Dobot quadruped | BSD-3-Clause | [GitHub](https://github.com/Dobot-Team/dobot_rover_simulation) | Locomotion policy training if a Rover-class quadruped is on site |
| dobot_quad_sdk | Quadruped SDK (legged and wheel-legged): gRPC high-level, CycloneDDS low-level, C++ / Python | MIT | [GitHub](https://github.com/Dobot-Team/dobot_quad_sdk) | Driving the wheel-legged robot from your own code |
| dobot_hex_sdk | Joint-motor SDK and examples for the **Hexplorer** hexapod (miniHex_v2) | MIT | [GitHub](https://github.com/Dobot-Team/dobot_hex_sdk) | Hexapod low-level control (hardware unlikely on site) |
| dobot_xtrainer | X-Trainer teleoperation + data-processing software | GPL-3.0 | [GitHub](https://github.com/Dobot-Arm/dobot_xtrainer) | Collecting bimanual demonstrations for imitation learning |
| Embodylink | Desktop tool (Qt, Ubuntu 20.04) for embodied data workflows | GPL-3.0-only | [GitHub](https://github.com/Dobot-Arm/Embodylink) | Data collection / management around X-Trainer and Atom |
| dobot_atom_sdk | Atom humanoid SDK (high-level RPC, low-level DDS joint control, joint recording) | Not checked ⚠️ | [GitHub](https://github.com/Dobot-Arm/dobot_atom_sdk) | Humanoid control if Atom is on site |
| voice_txt_command | Voice → Whisper ASR → Grounding DINO → KCF real-time object tracker demo | Not checked ⚠️ | [GitHub](https://github.com/Dobot-Arm/voice_txt_command) | Ready-made "say the object, robot finds it" perception front end |
| CR5A-Pick_Orange | Dataset, **LeRobot v3.0**: **51 episodes, 25,484 frames**, 30 Hz, wrist + front RGB, CR5A + DH AG95 gripper, teleoperated in Isaac Sim | MIT | [Hugging Face](https://huggingface.co/datasets/Dobot-Official/CR5A-Pick_Orange) | Template for a CR5A pick-and-place imitation pipeline (sorting, fetch) |
| CR5A-act-Pick_Orange | ACT policy (ResNet18 backbone, 50k steps, chunk 100) trained on the dataset above; smoke-tested in simulation only | MIT | [Hugging Face](https://huggingface.co/Dobot-Official/CR5A-act-Pick_Orange) | Starting checkpoint / config for ACT on CR5A |
| X-Trainer-clothes | Dataset (parquet episodes, 10K–100K rows); card has no description | Apache-2.0 | [Hugging Face](https://huggingface.co/datasets/Dobot-Official/X-Trainer-clothes) | Bimanual cloth-handling demonstrations (content inferred from name ⚠️) |
| ATOM_Trainer | Model repo, empty card | Apache-2.0 | [Hugging Face](https://huggingface.co/Dobot-Official/ATOM_Trainer) | Not usable until documented ⚠️ |
| ATOM_10.23, ATOM_10.26_put, jianada-parts-sorting | Dataset repos created 2026-11-12; **empty placeholders** when checked | Not stated | [Dobot-Official on Hugging Face](https://huggingface.co/Dobot-Official) | 🧪 watch for uploads during the event |
| Dobot-robot/X-trainer | Dataset repo described only as "x-trainer source files"; official status of the account not confirmed ⚠️ | Not stated | [Hugging Face](https://huggingface.co/datasets/Dobot-robot/X-trainer) | — |

No company-run public benchmark or leaderboard was found.

**Third-party artifacts on Dobot hardware (seen in listings; only the first was inspected)**

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| GM-100, Xtrainer part | Raw teleoperation dataset (HDF5; 14-dim joint action, top + two wrist cameras) from the GM-100 benchmark | MIT | [rhos-ai/gm100-xtrainer](https://huggingface.co/datasets/rhos-ai/gm100-xtrainer) | Largest public X-Trainer dataset found; pretraining / baselines |
| dobot_xtrainer_tac_1107 | Community X-Trainer dataset | Apache-2.0 | [michaelyeah7/dobot_xtrainer_tac_1107](https://huggingface.co/datasets/michaelyeah7/dobot_xtrainer_tac_1107) | Not inspected ⚠️ |
| Dobot-Nova2-RealData-Lerobot | Community Nova 2 dataset in LeRobot format | "other" | [baiyu858/Dobot-Nova2-RealData-Lerobot](https://huggingface.co/datasets/baiyu858/Dobot-Nova2-RealData-Lerobot) | Not inspected ⚠️ |
| dobot-grootn1.5-v2 | Community GR00T N1.5 fine-tune for a Dobot arm (uploader name matches the Phone2Act first author; link to the paper not confirmed ⚠️) | Not stated | [OmMandhane27/dobot-grootn1.5-v2](https://huggingface.co/OmMandhane27/dobot-grootn1.5-v2) | Not inspected ⚠️ |

## Third-party papers using their hardware or software

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [Differentiable Iterative Learning Control for Black-Box Position-Commanded Manipulators](https://arxiv.org/abs/2611.01220) | M. Al-Ghaili, Y. Qasim, H. Almubarak — KFUPM | arXiv, Oct 2026 | **DOBOT CR3**, joint-position interface only, 100 Hz | Learns to correct repetitive trajectories on an arm whose low-level controller is closed; **78.8% / 76.4%** lower joint / Cartesian RMSE than fixed-parameter ILC after two updates | T04 (repeatable trajectories) |
| [A Taxonomy of Construction Task Activities for Robot Workers (TARCAT)](https://arxiv.org/abs/2608.25395) | S. Sakib, Z. Peng, Y. Pang, Y. Otsuki, M. A. Al Faruque — UC Irvine | IROS 2026 Workshop on Future of Construction (per arXiv comment) | **DOBOT CR3** + 15-actuator tendon-driven CRAFT hand | 41 work primitives composed into reusable skills; scripted demos of screwdriver, hammering, brushing on the CR3. Annotations: [AICPS/TARCAT-Taxonomy](https://github.com/AICPS/TARCAT-Taxonomy) | T01 T02 (maintenance tasks) |
| [SPINE: Bridging the Cyber-Physical Gap with Agentic AI](https://arxiv.org/abs/2607.13049) | M. Ham, D. Kim, C. Lee, M. J. Kim, Y. Zhang, J. Wang, H. Liu — Northwestern University | arXiv, Jun 2026 (v2 Sep 2026) | **DOBOT X-Trainer**, AgileX PiPER | LLM-agent workflow that debugs a bimanual teleop rig until it works; on X-Trainer success rose **76% → 100%** and time-to-teleoperation fell **30%**. Site: [SPINE-web](https://magics-lab.github.io/SPINE-web) | any (bring-up tooling) |
| [Human-Robot Shared Control for Humanized End-Effector Teleoperation](https://arxiv.org/abs/2606.24629) | B. Ibrahim, I. H. Elhajj, D. Asmar, R. El Hakim — American University of Beirut | arXiv, Jun 2026 | **Dobot CR10**, ROS, joystick | Real-time shaping of teleoperated motion to human-like profiles (two-thirds power law); about **34%** smoother (RMS torque rate) with similar task time | T02 T04 |
| [Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection](https://arxiv.org/abs/2605.01948) | O. Mandhane, B. Yadav, S. Prasanna Ram, G. Narayanan — VESIT Mumbai | arXiv, May 2026 | **Dobot CR5** via real-time TCP port, ROS 2 | Smartphone (ARCore) as 6-DoF controller; records straight to LeRobot format; GR00T-N1.5 fine-tuned on **130 episodes** reaches **90%** on a multi-stage pick-and-place | T01 T02 T03 T04 |
| [An Approach to Combining Video and Speech with Large Language Models in Human-Robot Interaction](https://arxiv.org/abs/2602.20219) | G. Shen, Z. Tian — Dalian University of Technology | arXiv, Feb 2026 | **Dobot Magician** | Spoken commands → Whisper + Llama 3.1 + Florence-2 + fuzzy logic → pick actions on consumer hardware; **75%** command execution accuracy | T01 T03 T04 |
| [The Great March 100: 100 Detail-oriented Tasks for Evaluating Embodied AI Agents (GM-100)](https://arxiv.org/abs/2601.11421) | Z. Wang, C. Liu, Y. Xiang … Y.-L. Li — SJTU, SII, Robbyant | arXiv, Jan 2026 | **Dobot Xtrainer** and AgileX Cobot Magic | 100-task manipulation benchmark, **13,000+** teleoperated trajectories; **10 tasks collected on Xtrainer** with real-world baseline results. Data: [rhos.ai/research/gm-100](https://rhos.ai/research/gm-100) | T01 T03 T04 (generic manipulation) |
| [A0: An Affordance-Aware Hierarchical Model for General Robotic Manipulation](https://arxiv.org/abs/2504.12636) | R. Xu, J. Zhang, M. Guo, Y. Wen … F. Zheng, X. Liang — SYSU, SUSTech, Spatialtemporal AI, CMU, MBZUAI | arXiv, Apr 2025 (v5 Jan 2026) | **Dobot X-Trainer**, plus Franka, Kinova Gen3, Realman | Predicts contact points and post-contact trajectories (embodiment-agnostic), then executes; tasks include wiping a board and placing objects. Project: [A0](https://a-embodied.github.io/A0/) | T01 T03 T04 |

## Reading list by track

### T01 Autonomous Urban Services
- [DobotTrack](https://arxiv.org/abs/2611.09041) — language-specified person following with public code and weights; the fastest route to a "guide / follow-me / carry-behind" behaviour on any mobile base with a front camera.
- [DobotRoam repo](https://github.com/Dobot-Team/dobot_roam) — same team's waypoint-output navigation policy; read the README for the interface (RGB history + instruction → 8 waypoints) even if you do not train it.
- [Video + speech + LLM HRI on Dobot Magician](https://arxiv.org/abs/2602.20219) — a complete open-model recipe for voice-commanded pick-and-place at a service counter.
- [Phone2Act](https://arxiv.org/abs/2605.01948) — collect 100+ demonstrations on a CR5 with a phone and fine-tune a VLA inside the 48 hours.
- [GM-100](https://arxiv.org/abs/2601.11421) — task designs and X-Trainer baselines to pick a manipulation task that is hard but feasible.

### T02 Resilient & Safe City
- [Human-robot shared control on CR10](https://arxiv.org/abs/2606.24629) — smoother, more predictable teleoperation for hazardous-environment manipulation.
- [Phone2Act](https://arxiv.org/abs/2605.01948) — zero-hardware teleop bridge to a Dobot cobot over its TCP real-time port.
- [DobotTrack](https://arxiv.org/abs/2611.09041) — target following from an egocentric camera for patrol or responder-following; runs on Orin Nano.
- [TARCAT](https://arxiv.org/abs/2608.25395) — primitive vocabulary for tool use (screwdriver, hammer, brushing) on a CR3; useful to scope an infrastructure-maintenance demo.
- [SPINE](https://arxiv.org/abs/2607.13049) — how to recover an X-Trainer teleop rig quickly when it breaks mid-event.

### T03 Sustainable City
No directly relevant paper found (nothing on waste sorting, energy or environmental monitoring with Dobot hardware in the catalogues this pass could reach). Closest building blocks:
- [Video + speech + LLM HRI on Dobot Magician](https://arxiv.org/abs/2602.20219) — open-vocabulary detection driving a desktop arm; swap the prompt for waste classes to get a sorter.
- [Phone2Act](https://arxiv.org/abs/2605.01948) and [CR5A-Pick_Orange dataset + ACT checkpoint](https://huggingface.co/datasets/Dobot-Official/CR5A-Pick_Orange) — learned pick-and-place pipeline to adapt to sorting bins.
- [A0](https://arxiv.org/abs/2504.12636) — affordance (contact point) prediction that transfers across arms, shown on X-Trainer.

### T04 Elderly Care & Rehabilitation
No directly relevant paper found (no physiotherapy, massage, rehabilitation or assistive-feeding paper on Dobot hardware surfaced in this pass, despite Dobot marketing Nova 5 for physiotherapy). Closest building blocks:
- [Human-robot shared control on CR10](https://arxiv.org/abs/2606.24629) — human-like, lower-jerk motion; relevant to any arm moving near a patient or to caregiver telepresence.
- [Video + speech + LLM HRI on Dobot Magician](https://arxiv.org/abs/2602.20219) — voice interface for "fetch / hand me" assistance.
- [DobotTrack](https://arxiv.org/abs/2611.09041) — follow a specific person described in words; basis for a companion or walking-escort robot.
- [Diff-ILC on CR3](https://arxiv.org/abs/2611.01220) — improves accuracy of repeated trajectories using only the position interface; applicable to repetitive guided-exercise paths.
- [GM-100](https://arxiv.org/abs/2601.11421) — household-style bimanual tasks and data on X-Trainer for assistive manipulation policies.

## White papers, patents and technical reports

- **Atom series SDK application development guide v2.1 (Aug 2026)** — official technical document for the humanoid ([PDF](https://a.storyblok.com/f/298593/x/ad7c499105/dobot-atom-series-humanoid-robot-sdk-application-development-guide_v2-1_20260826_en.pdf), carried over from the company profile; not re-opened in this pass).
- **DobotWAM / ROM-1:** no white paper or technical report found; only product-news descriptions.
- **Financial filings as R&D evidence:** the H1 2026 HKEX interim announcement (cited in the profile) reports R&D at about 32% of revenue; not re-opened here.
- **Patents:** not researched in this pass.

## Sources

- [arXiv 2611.09041 — DobotTrack](https://arxiv.org/abs/2611.09041)
- [arXiv 2608.20087 — AdaPT humanoid tennis](https://arxiv.org/abs/2608.20087)
- [arXiv 2611.01220 — Differentiable ILC on DOBOT CR3](https://arxiv.org/abs/2611.01220)
- [arXiv 2608.25395 — TARCAT](https://arxiv.org/abs/2608.25395)
- [arXiv 2607.13049 — SPINE](https://arxiv.org/abs/2607.13049)
- [arXiv 2606.24629 — Human-robot shared control](https://arxiv.org/abs/2606.24629)
- [arXiv 2605.01948 — Phone2Act](https://arxiv.org/abs/2605.01948)
- [arXiv 2602.20219 — Video and speech with LLMs in HRI](https://arxiv.org/abs/2602.20219)
- [arXiv 2601.11421 — GM-100](https://arxiv.org/abs/2601.11421)
- [arXiv 2504.12636 — A0](https://arxiv.org/abs/2504.12636)
- [GitHub — Dobot-Team organisation](https://github.com/Dobot-Team)
- [GitHub — Dobot-Team/dobot_track](https://github.com/Dobot-Team/dobot_track)
- [GitHub — Dobot-Team/dobot_roam](https://github.com/Dobot-Team/dobot_roam)
- [GitHub — Dobot-Team/dobot_rover_simulation](https://github.com/Dobot-Team/dobot_rover_simulation)
- [GitHub — Dobot-Team/dobot_quad_sdk](https://github.com/Dobot-Team/dobot_quad_sdk)
- [GitHub — Dobot-Team/dobot_hex_sdk](https://github.com/Dobot-Team/dobot_hex_sdk)
- [GitHub — Dobot-Arm organisation](https://github.com/Dobot-Arm)
- [GitHub — Dobot-Arm/dobot_xtrainer](https://github.com/Dobot-Arm/dobot_xtrainer)
- [GitHub — Dobot-Arm/Embodylink](https://github.com/Dobot-Arm/Embodylink)
- [GitHub — Dobot-Arm/dobot_atom_sdk](https://github.com/Dobot-Arm/dobot_atom_sdk)
- [GitHub — Dobot-Arm/voice_txt_command](https://github.com/Dobot-Arm/voice_txt_command)
- [Hugging Face — Dobot-Official](https://huggingface.co/Dobot-Official)
- [Hugging Face — Dobot-Official/CR5A-Pick_Orange](https://huggingface.co/datasets/Dobot-Official/CR5A-Pick_Orange)
- [Hugging Face — Dobot-Official/CR5A-act-Pick_Orange](https://huggingface.co/Dobot-Official/CR5A-act-Pick_Orange)
- [Hugging Face — Dobot-Official/X-Trainer-clothes](https://huggingface.co/datasets/Dobot-Official/X-Trainer-clothes)
- [Hugging Face — dddsky/dobottrack](https://huggingface.co/dddsky/dobottrack)
- [Hugging Face — rhos-ai/gm100-xtrainer](https://huggingface.co/datasets/rhos-ai/gm100-xtrainer)
- [Dobot news — three new products at the 2026 Robotics Ecosystem Conference](https://www.dobot-robots.com/insights/news/dobot-unveils-three-new-products-at-its-2026-robotics-ecosystem-conference.html)
- [Dobot — LUMO overview page](https://www.dobot-robots.com/insights/case-studies/1283.html)
