---
type: papers
company: "Binabik AI"
slug: Binabik-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# Binabik AI — Papers and Research

⬆ [Binabik AI profile](Binabik-AI.md) · [Solutions and projects](Binabik-AI-Solutions-and-Projects.md) · [Developer guide](Binabik-AI-Developer-Guide.md)

## Research footprint

- **Academic team, thin company output.** Binabik is a ZHAW spin-off (founded Jan 2026) whose founders come from ZHAW (Centre for AI, Institute of Computer Science), the University of Turku (TIERS lab) and Tampere University. Only **2** papers carry a "Binabik.ai" affiliation, both preprints from 2025 on LLM agents for robots. Neither describes Studio, the Skill Engine or the BDK.
- **The product stack is unpublished.** No paper, technical report or benchmark covers teach-by-demonstration, skill segmentation or Binabik Sim. The website's "**200+** papers" figure is a team-wide career count (company claim), not company research. The blog ("Insights & Research") is empty.
- **Key people and where their research sits:** Jorge Peña Queralta (CEO; ZHAW CAI, earlier Turku): navigation, scene graphs, sim-to-real RL, humanoid loco-manipulation, assistive wheelchairs · Giovanni Toffetti (CPO; ZHAW InIT): cloud robotics, MoveIt2, VLA grasping · Lei Fu (lead engineer): MCP tooling, ROS 2 · Lauri Suomela (engineer; Tampere): learned visual navigation · Pascal Sager (CTO; ZHAW CAI): AI agents for computer use, representation learning · Harry Edelman (CFO; spelled "Edelmann" on the website): co-author on the agent and navigation papers.
- **Open-source posture:** two small Apache-2.0 tools (`mcp-rosbags`, `mcp-lab`) and one undocumented policy checkpoint. The affiliated labs release far more (MIT-licensed navigation and scene-graph code, a 103,000-demonstration multi-gripper dataset), but none of it is a Binabik product.
- **How this doc was researched:** one extended web search was available and used; everything else comes from direct reads of arXiv abstract and full-text pages, arXiv author listings, project pages, GitHub and Hugging Face. Every paper below was opened on arXiv. Conference-only papers without an arXiv copy (IEEE Xplore and similar) may be missing.

## Company-authored and company-affiliated papers

Rows marked **[B]** list Binabik.ai as an author affiliation. All other rows are work by current Binabik staff at their university labs (affiliation in the paper: ZHAW, Turku or Tampere), included because it shows what the team knows how to build. Venue is given only where arXiv or the project page states it; otherwise "arXiv preprint".

| Paper | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts | Tracks |
|---|---|---|---|---|---|
| [ReGATE: Recurrent Gated Visual Fusion for Reactive Humanoid-Object Interaction](https://arxiv.org/abs/2611.02871) | H. Zhu, J. Peña-Queralta · ZHAW CAI | arXiv preprint, Nov 2026 | Whole-body controller for a **Unitree G1** that grasps, carries and releases boxes from onboard depth + proprioception; **85.2%** success over 330 simulated trials vs 48.5% for the VisualMimic baseline; real-robot demos. Done in an Innosuisse project with Belimed AG on humanoids for cleaning and sterilising medical equipment | none linked | T01 T04 |
| [Kairos: Grounded Forecasting of Presence and Directional Flow in 4D Scene Graphs](https://arxiv.org/abs/2609.27467) | I. Catalano, J. A. Placed, J. Civera, J. Peña-Queralta · Turku, Zaragoza, ZHAW | arXiv preprint, Sep 2026 | Scene-graph memory that forecasts where people will be and which way they move at a future time; plans built on it meet more people at equal success rate | [code](https://github.com/IacopomC/kairos) (MIT) | T01 |
| [Gripper-aware Vision Language Action Models](https://arxiv.org/abs/2608.24603) | H. Zhang … J. Peña Queralta, G. Toffetti … B. Huang (19 authors) · multi-university incl. ZHAW | ECCV 2026 (per project page) | **MiGA** dataset: **103,000** demonstrations over **5** gripper types (parallel-jaw, three-finger, soft, suction …); GVLA model that picks a grasp strategy to match the gripper | [project page](https://airvlab.github.io/G-VLA/) · [MiGA dataset](https://huggingface.co/datasets/GVLA/MiGA-Dataset) · code "coming soon" | T03 T01 |
| [Occupancy-Grounded Room Segmentation for Hierarchical 3D Scene Graphs](https://arxiv.org/abs/2606.13727) | C. Cueto Zumaya, I. Catalano, J. Peña-Queralta, W. Moreira Bessa · Turku, ZHAW | arXiv preprint, Jun 2026 | Room nodes anchored to free-space regions with explicit polygon footprints; evaluated on 12 Matterport3D scenes against Hydra | [code](https://github.com/crcz25/OccuSG) (MIT, ROS 2 Humble) | T01 T02 |
| [AgiPIX: Bridging Simulation and Reality in Indoor Aerial Inspection](https://arxiv.org/abs/2604.08009) | S. Kuruppu Arachchige … L. Suomela … J.-K. Kämäräinen (7 authors) · Tampere and partners | Submitted to ICUAS 2026 | Open hardware + containerised ROS 2 stack + digital twin for indoor drone inspection of critical assets | project page linked in paper (⚠️ unverified: page did not load when checked) | T02 |
| [EgoMoD: Predicting Global Maps of Dynamics from Local Egocentric Observations](https://arxiv.org/abs/2603.00167) | I. Catalano, D. Morilla-Cabello, J. Peña-Queralta, E. Montijano · Turku, Zaragoza, ZHAW | arXiv preprint, Feb 2026 | Predicts site-wide pedestrian motion patterns from short robot-view video clips | none linked | T01 |
| [Data Scaling for Navigation in Unknown Environments](https://arxiv.org/abs/2601.09444) | L. Suomela, N. Takahata, S. Kuruppu Arachchige, H. Edelman, J.-K. Kämäräinen · Tampere | IEEE RA-L, 2026 | Map-free visual navigation trained on **4,565 h** of crowd-sourced driving from **161** locations in **35** countries; tested on sidewalk robots over **125 km**; diversity of places matters more than hours | [project page](https://lasuomela.github.io/navigation_scaling/) · [code](https://github.com/lasuomela/NavigationScaling) · [HF collection](https://huggingface.co/collections/lauriasuo/frodobots) | T01 |
| [Aion: Towards Hierarchical 4D Scene Graphs with Temporal Flow Dynamics](https://arxiv.org/abs/2512.11903) | I. Catalano, E. Montijano, J. Civera, J. A. Placed, J. Peña-Queralta | ICRA 2026 | Adds typical motion flows over time to a 3D scene graph for navigation among people | [code](https://github.com/IacopomC/aion) (MIT, ROS 1 Noetic) | T01 |
| [Follow-Me in Micro-Mobility with End-to-End Imitation Learning](https://arxiv.org/abs/2511.05158) | S. Salimpour, I. Catalano, T. Westerlund, M. Falahi, J. Peña Queralta · Turku, DAAV S.A., ZHAW | arXiv preprint, Nov 2025 | Imitation-learned controller lets DAAV's autonomous wheelchair follow an attendant more smoothly than hand-tuned controllers; real-world validation | none linked | T04 T01 |
| **[B]** [ROSBag MCP Server: Analyzing Robot Data with LLMs for Agentic Embodied AI Applications](https://arxiv.org/abs/2511.03497) | L. Fu, S. Salimpour, L. Militano, H. Edelman, J. Peña Queralta, G. Toffetti · ZHAW, Binabik.ai, Turku | arXiv preprint, Nov 2025 | MCP server that lets an LLM query ROS 1 / ROS 2 bags (trajectories, laser scans, TF, time series); benchmark of **8** LLMs on tool calling, with Kimi K2 and Claude Sonnet 4 best | [mcp-rosbags](https://github.com/binabik-ai/mcp-rosbags) · [mcp-lab](https://github.com/binabik-ai/mcp-lab) (both Apache-2.0) | T01 T02 T03 T04 |
| [Synthetic vs. Real Training Data for Visual Navigation](https://arxiv.org/abs/2509.11791) | L. Suomela, S. Kuruppu Arachchige, G. F. Torres, H. Edelman, J.-K. Kämäräinen · Tampere, Turku UAS | ICRA 2026 | FAINT policy trained only in simulation beats its real-data version by **31** points of success rate on a wheeled robot; same model also flies a drone | [project page](https://lasuomela.github.io/faint/) · [code](https://github.com/lasuomela/faint) · [weights](https://huggingface.co/collections/lauriasuo/faint-67b71dbaf71f1b648986f382) | T01 T02 |
| **[B]** [Towards Embodied Agentic AI: Review and Classification of LLM- and VLM-Driven Robot Autonomy and Interaction](https://arxiv.org/abs/2508.05294) | S. Salimpour, L. Fu, K. Rachwał, P. Bertrand, K. O'Sullivan, R. Jakob, F. Keramat, L. Militano, G. Toffetti, H. Edelman, J. Peña Queralta · Turku, ZHAW, ETH, Robotec.ai, Binabik.ai | arXiv preprint, Aug 2025 (v4 Nov 2025) | Survey and taxonomy of how LLMs / VLMs are wired into robots as planners, coordinators and tool users; covers open-source and industrial projects | none | T01 T02 T03 T04 |
| [Shared Control of Holonomic Wheelchairs through Reinforcement Learning](https://arxiv.org/abs/2507.17055) | J. Bähler, D. Paez-Granados, J. Peña-Queralta · ETH SCAI Lab, ZHAW | arXiv preprint, Jul 2025 | RL policy turns a 2D joystick input into safe 3D motion for an omnidirectional wheelchair; trained in Isaac Gym, transferred to a real platform | none linked | T04 |
| [A Comprehensive Survey of Agents for Computer Use](https://arxiv.org/abs/2501.16150) | P. J. Sager and 9 co-authors · ZHAW CAI | JAIR vol. 85, 2026 | Taxonomy of agents that operate software through screenshots, mouse and keyboard (CTO's main line of research; not robotics) | none | — |
| [Sim-to-Real Transfer for Mobile Robots with Reinforcement Learning: from NVIDIA Isaac Sim to Gazebo and Real ROS 2 Robots](https://arxiv.org/abs/2501.02902) | S. Salimpour, J. Peña-Queralta, D. Paez-Granados, J. Heikkonen, T. Westerlund · Turku, ETH | arXiv preprint, Jan 2025 | Recipe for training local-navigation policies in Isaac Sim and running them zero-shot on real ROS 2 robots; compared with Nav2 | none linked | T01 T02 |
| [Benchmarking ML Approaches to UWB-Based Range-Only Posture Recognition for Human Robot-Interaction](https://arxiv.org/abs/2408.15717) | S. Salimi, S. Salimpour, J. Peña Queralta, W. Moreira Bessa, T. Westerlund · Turku | arXiv preprint, Aug 2024 | Five body-worn UWB tags classify human posture and map it to robot commands, without cameras | none linked | T04 T01 |
| [A Method for Multi-Robot Asynchronous Trajectory Execution in MoveIt2](https://arxiv.org/abs/2310.08597) | P. Stoop, T. Ratnayake, G. Toffetti · ZHAW | IROS 2023 workshop (Task and Motion Planning) | MoveIt2 extension so two arms can run independent trajectories with continuous collision checking | none linked | T01 T03 |
| [PlaceNav: Topological Navigation through Place Recognition](https://arxiv.org/abs/2309.17260) | L. Suomela, J. Kalliola, H. Edelman, J.-K. Kämäräinen · Tampere | ICRA 2024 | Uses visual place recognition to pick sub-goals in image-based navigation; cheaper and more robust than earlier pipelines | [project page](https://lasuomela.github.io/placenav/) · [code](https://github.com/lasuomela/placenav) | T01 |
| [Benchmarking UWB-Based Infrastructure-Free Positioning and Multi-Robot Relative Localization: Dataset and Characterization](https://arxiv.org/abs/2305.08532) | P. Torrico Morón, S. Salimpour, L. Fu, X. Yu, J. Peña Queralta, T. Westerlund · Turku | arXiv preprint, May 2023 | Dataset with motion-capture ground truth for anchor-free UWB localisation between robots (Lei Fu presumed to be Binabik's Lei Fu, ⚠️ unverified) | none linked on arXiv page | T02 |
| [Simulation Analysis of Exploration Strategies and UAV Planning for Search and Rescue](https://arxiv.org/abs/2304.05107) | P. Nguyen Thuan, J. Peña Queralta, T. Westerlund · Turku | arXiv preprint, Apr 2023 | Simulator to compare drone search patterns for victim detection, optimising recall and scan time | none linked | T02 |
| [Event-driven Fabric Blockchain – ROS 2 Interface: Towards Secure and Auditable Teleoperation of Mobile Robots](https://arxiv.org/abs/2304.00781) | L. Fu, S. Salimi, J. Peña Queralta, T. Westerlund · Turku | arXiv preprint, Apr 2023 | Low-latency bridge that logs teleoperation commands to a permissioned ledger for audit (same caveat on Lei Fu, ⚠️ unverified) | none linked | T02 |
| [Cloud Native Robotic Applications with GPU Sharing on Kubernetes](https://arxiv.org/abs/2210.03936) | G. Toffetti, L. Militano, S. Murphy, R. Maurer, M. Straub · ZHAW | IROS 2022 Cloud Robotics workshop | Lessons from running many ROS applications, simulation and real robots from one Kubernetes cluster with shared GPUs | none linked | — |
| [Self-Calibrating Anomaly and Change Detection for Autonomous Inspection Robots](https://arxiv.org/abs/2209.02379) | S. Salimpour, J. Peña Queralta, T. Westerlund · Turku | arXiv preprint, Aug 2022 | Compares a patrol image with a reference image (SuperPoint + SuperGlue matching) to flag changes in unknown environments without retraining; closest published match to Binabik's 2025 "patrol and look for changes" prototype (link to the product is an inference) | none linked | T02 |
| [Benchmarking Visual Localization for Autonomous Navigation](https://arxiv.org/abs/2203.13048) | L. Suomela, J. Kalliola, A. Dag, H. Edelman, J.-K. Kämäräinen · Tampere | WACV 2023 | CARLA-based benchmark of how weather, time of day and camera view affect localisation inside a full navigation stack | [code](https://github.com/lasuomela/carla_vloc_benchmark) (MIT) | T01 |

Not listed: older Turku work by Jorge Peña Queralta (about 35 more arXiv papers from 2020–2023 on multi-robot UWB localisation, lidar SLAM datasets, blockchain for robot fleets, federated learning) and Pascal Sager's machine-learning papers outside robotics. They are far from what Binabik sells.

## Datasets, models and benchmarks released

**Released by Binabik AI itself (3):**

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| `mcp-rosbags` | ✅ MCP server (Python) for LLM analysis of `.bag` / `.db3` / `.mcap` recordings | Apache-2.0 | [GitHub](https://github.com/binabik-ai/mcp-rosbags) · [paper](https://arxiv.org/abs/2511.03497) | Debugging any ROS robot on site by asking an LLM questions about a recorded run; "explain what the robot did" demo feature |
| `mcp-lab` | ✅ Local web UI to benchmark LLM tool calling against MCP servers (the test bench used in the paper) | Apache-2.0 | [GitHub](https://github.com/binabik-ai/mcp-lab) | Choosing which LLM drives your agent; logging tokens, latency and tool calls |
| `act_PickPlaceRedBlock` | 🧪 Policy checkpoint, **51.6M** parameters, uploaded 2 Jul 2026; no model card, no paper | not stated | [Hugging Face](https://huggingface.co/binabik-ai/act_PickPlaceRedBlock) | Reference only: an action-chunking policy for a Unitree G1 simulation pick-and-place task (details in the [developer guide](Binabik-AI-Developer-Guide.md)) |

Binabik has published **no dataset** and **no benchmark** of its own (Hugging Face organisation: 1 model, 0 datasets).

**Released by affiliated labs with Binabik staff as co-authors (not Binabik products):**

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| MiGA | Dataset, **103,000** manipulation demonstrations, 5 gripper types, real + simulation, LeRobot format | not stated | [Hugging Face](https://huggingface.co/datasets/GVLA/MiGA-Dataset) · [project page](https://airvlab.github.io/G-VLA/) | Fine-tuning a grasp policy when your robot has a suction or non-standard gripper (T03 sorting) |
| FAINT | Navigation policy code + pretrained weights | see repo | [code](https://github.com/lasuomela/faint) · [weights](https://huggingface.co/collections/lauriasuo/faint-67b71dbaf71f1b648986f382) | Image-goal navigation on a wheeled base without a map |
| NavigationScaling | Code + model / data collection for map-free point-goal navigation | see repo | [code](https://github.com/lasuomela/NavigationScaling) · [HF collection](https://huggingface.co/collections/lauriasuo/frodobots) | Zero-shot sidewalk navigation baseline |
| PlaceNav | Topological navigation code | see repo | [code](https://github.com/lasuomela/placenav) | Teach-and-repeat style route following from images |
| carla_vloc_benchmark | Simulation benchmark for visual localisation | MIT | [code](https://github.com/lasuomela/carla_vloc_benchmark) | Testing localisation under weather and lighting change |
| Aion | 4D scene-graph code (ROS 1 Noetic, needs Hydra) | MIT | [code](https://github.com/IacopomC/aion) | People-flow-aware route planning |
| Kairos | Flow and presence forecasting code | MIT | [code](https://github.com/IacopomC/kairos) | Predicting busy areas and times |
| OccuSG | ROS 2 Humble workspace for room segmentation and scene graphs | MIT | [code](https://github.com/crcz25/OccuSG) | Turning an occupancy map into named rooms for task planning |

## Third-party papers using their hardware or software

Binabik has no hardware. **No third-party paper was found that runs Studio, the BDK or `mcp-rosbags` in its experiments.** Semantic Scholar lists five outside works that cite the ROSBag MCP paper; the two available on arXiv were opened and both only cite it. The other three (IEEE / ACM proceedings) could not be opened and are not listed.

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [When Video Misreads: Closed-Loop Distillation of Reading Heuristics for Exploratory Manipulation Trace QA](https://arxiv.org/abs/2606.08542) | H. Ge and 7 co-authors | arXiv preprint, 2026 | None of Binabik's. Cites ROSBag MCP Server as a design inspiration for its log-inspection interface | An agent that reads robot video + proprioception logs to work out why a manipulation attempt failed | — |
| [Structured Authority Injection: Persistent Human Control for LLM Agents via Typed MCP Overrides](https://arxiv.org/abs/2610.22373) | R. Tran and 8 co-authors | arXiv preprint, 2026 | None of Binabik's. Cites ROSBag MCP Server as related work | Typed MCP tool calls so an operator's corrections keep binding an LLM agent across planning cycles | — |

## Reading list by track

### T01 Autonomous Urban Services
- [Data Scaling for Navigation in Unknown Environments](https://arxiv.org/abs/2601.09444): sidewalk-robot navigation without a map, with code and models; the nearest thing here to a delivery baseline (T01.1, T01.6).
- [Synthetic vs. Real Training Data for Visual Navigation](https://arxiv.org/abs/2509.11791): FAINT weights are downloadable and run in real time on robot hardware (T01.6).
- [Aion](https://arxiv.org/abs/2512.11903) and [Kairos](https://arxiv.org/abs/2609.27467): how to plan around where people usually walk; MIT code (T01.3, T01.7).
- [Towards Embodied Agentic AI](https://arxiv.org/abs/2508.05294): quick map of LLM-agent architectures for a guidance or information robot (T01.5, T01.7).
- [ROSBag MCP Server](https://arxiv.org/abs/2511.03497): the one Binabik tool you can install in minutes; also tells you which LLMs call tools reliably.
- [ReGATE](https://arxiv.org/abs/2611.02871): box pick-carry-place on a Unitree G1, useful if a team attempts humanoid delivery (T01.1).

### T02 Resilient & Safe City
- [Self-Calibrating Anomaly and Change Detection for Autonomous Inspection Robots](https://arxiv.org/abs/2209.02379): reference-image change detection that needs no retraining; buildable in a day with off-the-shelf SuperPoint / SuperGlue (T02.3, T02.5).
- [AgiPIX](https://arxiv.org/abs/2604.08009): full sim-plus-real pipeline for indoor inspection drones (T02.2).
- [Sim-to-Real Transfer for Mobile Robots with Reinforcement Learning](https://arxiv.org/abs/2501.02902): Isaac Sim to real ROS 2 robot workflow for obstacle avoidance (T02.6).
- [Simulation Analysis of Exploration Strategies and UAV Planning for Search and Rescue](https://arxiv.org/abs/2304.05107): search-pattern comparison and why recall beats precision for victim detection (T02.1).
- [Event-driven Fabric Blockchain – ROS 2 Interface](https://arxiv.org/abs/2304.00781): auditable teleoperation logging, relevant to a human-in-the-loop response story (T02.7).
- [Occupancy-Grounded Room Segmentation](https://arxiv.org/abs/2606.13727): ROS 2 code that turns a map into rooms a responder can refer to by name (T02.4).

### T03 Sustainable City
- [Gripper-aware Vision Language Action Models](https://arxiv.org/abs/2608.24603): the only directly useful paper; shows how grasp strategy must change between suction and jaw grippers, with an open dataset (T03.1, T03.6).
- [A Method for Multi-Robot Asynchronous Trajectory Execution in MoveIt2](https://arxiv.org/abs/2310.08597): two arms sorting in parallel without waiting on each other (T03.1).
- [ROSBag MCP Server](https://arxiv.org/abs/2511.03497): LLM-driven analysis of recorded sensor data, usable for an environmental data-collection demo (T03.7).
- No paper on energy, water or environmental monitoring was found.

### T04 Elderly Care & Rehabilitation
- [Shared Control of Holonomic Wheelchairs through Reinforcement Learning](https://arxiv.org/abs/2507.17055): assistive driving that keeps the user in control; first real-world RL shared control on an omnidirectional platform according to the authors (T04.4).
- [Follow-Me in Micro-Mobility with End-to-End Imitation Learning](https://arxiv.org/abs/2511.05158): comfort-first person following for people with reduced mobility; the metrics transfer to any follow-me robot (T04.4).
- [Benchmarking ML Approaches to UWB-Based Range-Only Posture Recognition](https://arxiv.org/abs/2408.15717): camera-free posture sensing, a privacy-friendly angle for monitoring (T04.7, T04.5).
- [ReGATE](https://arxiv.org/abs/2611.02871): humanoid handling of boxes in a medical-equipment cleaning and sterilisation project (T04.6).
- [Towards Embodied Agentic AI](https://arxiv.org/abs/2508.05294): patterns for a natural-language interface to a care robot (T04.5).

## White papers, patents and technical reports

- **White papers / technical reports:** none published by Binabik.
- **Patents:** none found (no patent database search was possible; ⚠️ unverified absence).
- **Funded research project (from a paper acknowledgement):** Innosuisse innovation project **134.504 IP-ICT**, "Humanoid Robots for Cleaning and Sterilization of Medical Equipment", ZHAW with Belimed AG. It is a ZHAW project led from the CEO's lab; a formal role for Binabik in it is not stated (⚠️ unverified). Source: acknowledgements in [ReGATE](https://arxiv.org/abs/2611.02871).
- **Company claim:** "200+ papers" on the About page, with no list behind it.

## Sources

- [arXiv 2511.03497 — ROSBag MCP Server](https://arxiv.org/abs/2511.03497)
- [arXiv 2508.05294 — Towards Embodied Agentic AI](https://arxiv.org/abs/2508.05294)
- [arXiv 2611.02871 — ReGATE](https://arxiv.org/abs/2611.02871)
- [arXiv 2609.27467 — Kairos](https://arxiv.org/abs/2609.27467)
- [arXiv 2608.24603 — Gripper-aware Vision Language Action Models](https://arxiv.org/abs/2608.24603)
- [arXiv 2606.13727 — Occupancy-Grounded Room Segmentation](https://arxiv.org/abs/2606.13727)
- [arXiv 2604.08009 — AgiPIX](https://arxiv.org/abs/2604.08009)
- [arXiv 2603.00167 — EgoMoD](https://arxiv.org/abs/2603.00167)
- [arXiv 2601.09444 — Data Scaling for Navigation in Unknown Environments](https://arxiv.org/abs/2601.09444)
- [arXiv 2512.11903 — Aion](https://arxiv.org/abs/2512.11903)
- [arXiv 2511.05158 — Follow-Me in Micro-Mobility](https://arxiv.org/abs/2511.05158)
- [arXiv 2509.11791 — Synthetic vs. Real Training Data for Visual Navigation](https://arxiv.org/abs/2509.11791)
- [arXiv 2507.17055 — Shared Control of Holonomic Wheelchairs](https://arxiv.org/abs/2507.17055)
- [arXiv 2501.16150 — A Comprehensive Survey of Agents for Computer Use](https://arxiv.org/abs/2501.16150)
- [arXiv 2501.02902 — Sim-to-Real Transfer for Mobile Robots](https://arxiv.org/abs/2501.02902)
- [arXiv 2408.15717 — UWB-Based Posture Recognition](https://arxiv.org/abs/2408.15717)
- [arXiv 2310.08597 — Multi-Robot Asynchronous Trajectory Execution in MoveIt2](https://arxiv.org/abs/2310.08597)
- [arXiv 2309.17260 — PlaceNav](https://arxiv.org/abs/2309.17260)
- [arXiv 2305.08532 — UWB relative localisation dataset](https://arxiv.org/abs/2305.08532)
- [arXiv 2304.05107 — UAV planning for search and rescue](https://arxiv.org/abs/2304.05107)
- [arXiv 2304.00781 — Fabric Blockchain – ROS 2 Interface](https://arxiv.org/abs/2304.00781)
- [arXiv 2210.03936 — Cloud Native Robotic Applications](https://arxiv.org/abs/2210.03936)
- [arXiv 2209.02379 — Anomaly and Change Detection for Inspection Robots](https://arxiv.org/abs/2209.02379)
- [arXiv 2203.13048 — Benchmarking Visual Localization](https://arxiv.org/abs/2203.13048)
- [arXiv 2606.08542 — When Video Misreads (citing paper)](https://arxiv.org/abs/2606.08542)
- [arXiv 2610.22373 — Structured Authority Injection (citing paper)](https://arxiv.org/abs/2610.22373)
- [Semantic Scholar — ROSBag MCP Server record and citations](https://www.semanticscholar.org/paper/ROSBag-MCP-Server:-Analyzing-Robot-Data-with-LLMs-Fu-Salimpour/f6599bead9c8c3eb733022eae1228af12c3ceac5)
- [GitHub — binabik-ai/mcp-rosbags](https://github.com/binabik-ai/mcp-rosbags)
- [GitHub — binabik-ai/mcp-lab](https://github.com/binabik-ai/mcp-lab)
- [Hugging Face — binabik-ai organisation](https://huggingface.co/binabik-ai)
- [Hugging Face — binabik-ai/act_PickPlaceRedBlock](https://huggingface.co/binabik-ai/act_PickPlaceRedBlock)
- [G-VLA project page](https://airvlab.github.io/G-VLA/)
- [Hugging Face — GVLA/MiGA-Dataset](https://huggingface.co/datasets/GVLA/MiGA-Dataset)
- [FAINT project page](https://lasuomela.github.io/faint/)
- [GitHub — lasuomela/FAINT](https://github.com/lasuomela/faint)
- [Navigation scaling project page](https://lasuomela.github.io/navigation_scaling/)
- [PlaceNav project page](https://lasuomela.github.io/placenav/)
- [GitHub — lasuomela/carla_vloc_benchmark](https://github.com/lasuomela/carla_vloc_benchmark)
- [GitHub — IacopomC/aion](https://github.com/IacopomC/aion)
- [GitHub — IacopomC/kairos](https://github.com/IacopomC/kairos)
- [GitHub — crcz25/OccuSG](https://github.com/crcz25/OccuSG)
- [Binabik AI — About](https://binabik.ai/about)
- [Binabik AI — Blog](https://binabik.ai/blog)
