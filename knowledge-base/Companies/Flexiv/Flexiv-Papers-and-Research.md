---
type: papers
company: "Flexiv Robotics"
slug: Flexiv
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# Flexiv Robotics — Papers and Research

⬆ [Flexiv Robotics profile](Flexiv.md) · [Solutions and projects](Flexiv-Solutions-and-Projects.md) · [Developer guide](Flexiv-Developer-Guide.md)

> **How this list was built (read once):** every paper below was opened on arXiv (record + full-text HTML) and the words "Flexiv" / "Rizon" / "Noematrix" were located in the text to confirm the hardware or affiliation. The general web-search budget for this run was exhausted, so discovery relied on the arXiv catalogue, Flexiv's own site and GitHub, and project pages. **Not covered:** papers that exist only on IEEE Xplore / Chinese journals, patents, and anything that does not name Flexiv in its arXiv text. Treat the list as "verified but not exhaustive".

## Research footprint

- **Flexiv publishes little under its own name.** The official site has no research or publications page; the only research-themed post found is a Nov 2026 blog about NVIDIA's GB300 assembly study. The research output sits with a tight academic circle instead.
- **The circle = Cewu Lu's group at Shanghai Jiao Tong University (SJTU) + Noematrix + Flexiv.** On 2026 papers, **Shiquan Wang** (Flexiv co-founder / CEO) and **Cewu Lu** are listed with *both* Noematrix and Flexiv affiliations, next to SJTU, "FORTE Lab" and Shanghai Innovation Institute. Noematrix (穹彻智能) is an embodied-AI software company ("Noematrix Brain", AnySkill, CoMiner data-collection suite). Its exact corporate relationship to Flexiv is ⚠️ unverified; Cewu Lu's formal role at Flexiv is ⚠️ unverified.
- **Since late 2025 Flexiv is a named affiliation on 4 papers** (History-aware policy, Force Policy, Visual Embodiment Dependence, FP2) — all about making learned policies control *force*, not just position. This is the research line behind "force control + physical AI" in Flexiv's marketing.
- **Recurring themes:** force-aware imitation learning and hybrid force-position policies · grasp perception (AnyGrasp) · low-cost data collection (AirExo exoskeletons, TactAR AR teleoperation, RH20T dataset) · almost every real-robot experiment runs on a **Rizon 4 / 4s**.
- **Open-source posture:** Flexiv's own SDKs are Apache-2.0 on GitHub (27 repos), but Flexiv has released **no dataset and no model weights** itself. The affiliated labs release code for most papers, plus a few Hugging Face checkpoints and datasets, under mixed licences (MIT, CC BY-NC-SA, CC BY-SA / CC BY-NC).

## Company-authored and company-affiliated papers

Legend for the second column: **[F]** Flexiv listed as an author affiliation · **[N]** Noematrix listed · **[S]** SJTU (Cewu Lu group) only. All experiments use Flexiv hardware unless noted. Newest first.

| Paper | Authors / organisation | Venue, year | What it contributes | Artifacts | Tracks |
|---|---|---|---|---|---|
| [FP2: Equipping Robotic Foundation Models with Force Control](https://arxiv.org/abs/2609.37433) | H. Fang, S. Tang, J. Hu, S. Zhang, D. Zhang, L. Chen, D. Li, M. Mei, W. Liu, C. Lu, **S. Wang** · **[F][N]** + SJTU, UPenn, Fudan, UIUC, ZJU | arXiv preprint, Sep 2026 | Add-on that gives a fine-tuned robot foundation model explicit force control: the big model plans actions, a small high-rate policy regulates contact. Tested with **4 backbones × 4 tasks** (Flip Box, **Insert EV Charger**, Insert Peg, Wipe Curve) on Rizon 4 + Flexiv GN-02 gripper + FT-03S sensor | [Project page](http://force-policy.github.io/fp2) (code release not confirmed) | T01 T03 T04 |
| [Rethinking Visual Embodiment Dependence in Visuomotor Policies](https://arxiv.org/abs/2609.16815) | H. Fang, Y. Lu, C. Wang, H. Qin, S. Tang, Z. He, S. Xia, J. Chen, W. Liu, **S. Wang**, C. Lu · **[F][N]** + SJTU | arXiv preprint, Sep 2026 | Shows policies use the *look of the robot* as a shortcut; replaces the arm in the 3D point cloud with a canonical end-effector shape so policies transfer across robot configurations. Rizon 4 + AG-95 gripper | [Project page](https://tonyfang.net/ved) | — |
| [Force Policy: Learning Hybrid Force-Position Control Policy under Interaction Frame for Contact-Rich Manipulation](https://arxiv.org/abs/2602.22088) | H. Fang, S. Tang, M. Mei, H. Qin, Z. He, J. Chen, Y. Feng, C. Wang, W. Liu, Z. He, C. Lu, **S. Wang** (corresponding) · **[F][N]** + SJTU, ZJU | **RSS 2026** | Global vision policy for free space + local high-rate force policy after contact, tied together by an "interaction frame" recovered from demonstrations. **3 tasks** in polishing and insertion on Rizon 4 + GN-02; demos via Flexiv arm-to-arm force-feedback teleoperation | [Project page](https://force-policy.github.io/) · [code](https://github.com/force-policy/ForcePolicy) | T02 T03 T04 |
| [ImplicitRDP: An End-to-End Visual-Force Diffusion Policy with Structural Slow-Fast Learning](https://arxiv.org/abs/2512.10946) | W. Chen, H. Xue, Y. Wang, F. Zhou, J. Lv, Y. Jin, S. Tang, C. Wen, C. Lu · **[N]** + SJTU | RA-L 2026 | One network that fuses slow vision and fast force tokens, so the policy reacts to contact at action rate. Rizon **4s**, kinesthetic teaching handle | [Project page](https://implicit-rdp.github.io/) · [code](https://github.com/Chen-Wendi/ImplicitRDP) · [weights](https://huggingface.co/WendiChen/ImplicitRDP_model) · [data](https://huggingface.co/datasets/WendiChen/ImplicitRDP_dataset) | T04 T03 |
| [History-Aware Visuomotor Policy Learning via Point Tracking](https://arxiv.org/abs/2509.17141) | J. Chen, H. Fang, C. Wang, **S. Wang**, C. Lu · **[F][N]** + SJTU | **ICRA 2026** | Gives a policy memory by tracking object points over time; fixes tasks with repeated or look-alike states. **7 real tasks** on Rizon 4 | [Project page](https://tonyfang.net/history/) · [code](https://github.com/rise-policy/HistRISE) | T01 |
| [Knowledge-Driven Imitation Learning: Enabling Generalization Across Diverse Conditions](https://arxiv.org/abs/2506.21057) | Z. Miao, J. Lv, H. Fang, Y. Jin, C. Lu · **[N]** + SJTU | IROS 2025 | Uses object templates / semantic keypoints so skills learned on one object transfer to new ones. Rizon 4 + Robotiq 2F-85 | [Project page](https://knowledge-driven.github.io/) · [code](https://github.com/mioam/KnowledgeIL) | T01 T03 |
| [ForceVLA: Enhancing VLA Models with a Force-aware MoE for Contact-rich Manipulation](https://arxiv.org/abs/2505.22159) | J. Yu, H. Liu, Q. Yu, J. Ren, C. Hao, H. Ding, G. Huang, G. Huang, Y. Song, P. Cai, C. Lu, W. Zhang · **[N]** (C. Lu) + Fudan, SJTU | NeurIPS 2025 | Feeds 6-axis force into a vision-language-action model through a mixture-of-experts module; data collected on a Rizon 7-DoF arm | See paper | T03 T04 |
| [SIME: Enhancing Policy Self-Improvement with Modal-level Exploration](https://arxiv.org/abs/2505.01396) | Y. Jin, J. Lv, W. Yu, H. Fang, Y.-L. Li, C. Lu · **[N]** + SJTU | arXiv preprint, May 2025 | Lets a policy explore different behaviour modes and learn from its own successful rollouts. Rizon 4 | [Project page](https://ericjin2002.github.io/SIME/) · [code](https://github.com/EricJin2002/SIME) | — |
| [Dense Policy: Bidirectional Autoregressive Learning of Actions](https://arxiv.org/abs/2503.13217) | Y. Su, X. Zhan, H. Fang, H. Xue, H.-S. Fang, Y.-L. Li, C. Lu, L. Yang · **[S]** | arXiv preprint, Mar 2025 | Coarse-to-fine autoregressive action head as an alternative to diffusion. Rizon + Robotiq 2F-85 | [Project page](https://selen-suyue.github.io/DspNet/) · [code](https://github.com/Selen-Suyue/DensePolicy) | — |
| [AirExo-2: Scaling up Generalizable Robotic Imitation Learning with Low-Cost Exoskeletons](https://arxiv.org/abs/2503.03081) | H. Fang, C. Wang, Y. Wang, J. Chen, S. Xia, J. Lv, Z. He, X. Yi, Y. Guo, X. Zhan, L. Yang, W. Wang, C. Lu, H.-S. Fang · **[N]** + SJTU | CoRL 2025 | Exoskeleton that records human demos *without a robot* and converts them to robot-view data; introduces the RISE-2 policy | [Project page](https://airexo.tech/airexo2/) · [hardware + code](https://github.com/AirExo/AirExo-2) · [RISE-2](https://github.com/rise-policy/RISE-2) | T02 T04 |
| [Reactive Diffusion Policy: Slow-Fast Visual-Tactile Policy Learning for Contact-Rich Manipulation](https://arxiv.org/abs/2503.02881) | H. Xue, J. Ren, W. Chen, G. Zhang, Y. Fang, G. Gu, H. Xu, C. Lu · **[S]** | RSS 2025 | Slow diffusion planner + fast tactile/force feedback loop; **TactAR** AR teleoperation shows force feedback in a headset. **Two Rizon 4 + Flexiv Grav grippers**; tasks: Peeling, Wiping, Bimanual Lifting | [Project page](https://reactive-diffusion-policy.github.io/) · [code (MIT)](https://github.com/xiaoxiaoxh/reactive_diffusion_policy) · [TactAR app](https://github.com/xiaoxiaoxh/TactAR_APP) · [weights](https://huggingface.co/WendiChen/reactive_diffusion_policy_model) · [data](https://huggingface.co/datasets/WendiChen/reactive_diffusion_policy_dataset) | T04 T01 T02 |
| [FoAR: Force-Aware Reactive Policy for Contact-Rich Robotic Manipulation](https://arxiv.org/abs/2411.15753) | Z. He, H. Fang, J. Chen, H.-S. Fang, C. Lu · **[S]** | RA-L (accepted) | Policy that decides *when* to trust force input (contact phase) and when to ignore it. Rizon + AG-95 + flange F/T sensor; includes peeling | [Project page](https://tonyfang.net/FoAR/) · [code](https://github.com/Alan-Heoooh/FoAR) | T04 T03 |
| [Motion Before Action: Diffusing Object Motion as Manipulation Condition](https://arxiv.org/abs/2411.09658) | Y. Su, X. Zhan, H. Fang, Y.-L. Li, C. Lu, L. Yang · **[S]** | arXiv 2024 (journal version linked on project page; venue ⚠️ unverified) | Predicts future object motion first, then conditions the action on it. Rizon + Robotiq 2F-85 | [Project page](https://selen-suyue.github.io/MBApage/) · [code](https://github.com/Selen-Suyue/MBA) | — |
| [CAGE: Causal Attention Enables Data-Efficient Generalizable Robotic Manipulation](https://arxiv.org/abs/2410.14974) | S. Xia, H. Fang, C. Lu, H.-S. Fang · **[S]** | arXiv 2024 (submitted to ICRA 2025) | Policy that generalises to new objects, backgrounds and camera views from few demos; cross-embodiment table (Flexiv vs RealMan arm, two grippers) | [Project page](https://cage-policy.github.io/) · [code](https://github.com/cage-policy/CAGE) | T01 |
| [ForceMimic: Force-Centric Imitation Learning with Force-Motion Capture System for Contact-Rich Manipulation](https://arxiv.org/abs/2410.07554) | W. Liu, J. Wang, Y. Wang, W. Wang, C. Lu · **[S]** (thanks Flexiv for F/T sensor hardware) | ICRA 2025 | Hand-held device records human force + motion; the robot replays it with Flexiv RDK **hybrid force-position primitives**. Demo: zucchini peeling on Rizon 4 (**438** skill segments) | [Project page](https://forcemimic.github.io/) · [capture device](https://github.com/ForceMimic/forcecapture) · [policy](https://github.com/ForceMimic/hybridil) | T04 T03 |
| [RISE: 3D Perception Makes Real-World Robot Imitation Simple and Effective](https://arxiv.org/abs/2404.12281) | C. Wang (Noematrix), H. Fang, H.-S. Fang, C. Lu · **[N]** + SJTU | IROS 2024 | End-to-end imitation policy that takes 3D point clouds and outputs continuous actions; the base that CAGE, HistRISE and RISE-2 build on. Rizon + AG-95 | [Project page](https://rise-policy.github.io/) · [code (CC BY-NC-SA 4.0)](https://github.com/rise-policy/rise) | T01 T03 |
| [UniFolding: Towards Sample-efficient, Scalable, and Generalizable Robotic Garment Folding](https://arxiv.org/abs/2311.01267) | H. Xue, Y. Li, W. Xu, H. Li, D. Zheng, C. Lu · **[S]** | CoRL 2023 | Dual-arm system that unfolds and folds many garment types; **two Rizon arms** with AG-95 grippers, uses Flexiv's contact-grasp function on a hard table | [Project page](https://unifolding.robotflow.ai/) · [code](https://github.com/xiaoxiaoxh/UniFolding) | T04 T01 |
| [AirExo: Low-Cost Exoskeletons for Learning Whole-Arm Manipulation in the Wild](https://arxiv.org/abs/2309.14975) | H. Fang, H.-S. Fang, Y. Wang, J. Ren, J. Chen, R. Zhang, W. Wang, C. Lu · **[S]** | arXiv 2023 (conference venue ⚠️ unverified) | 3D-printable exoskeleton for dual-arm teleoperation and robot-free demo collection; built around two Rizon arms, models also for Franka, KUKA, UR5 | [Project page](https://airexo.github.io/) · [CAD models](https://github.com/AirExo/airexo-models) · [collector](https://github.com/AirExo/collector) | T02 T04 |
| [Flexible Handover with Real-Time Robust Dynamic Grasp Trajectory Generation](https://arxiv.org/abs/2308.15622) | G. Zhang, H.-S. Fang, H. Fang, C. Lu · **[S]** | IROS 2023 | Robot takes objects from a moving human hand by planning grasp trajectories in real time. Rizon + wrist RealSense L515 | — | **T04** T01 |
| [RH20T: A Comprehensive Robotic Dataset for Learning Diverse Skills in One-Shot](https://arxiv.org/abs/2307.00595) | H.-S. Fang, H. Fang, Z. Tang, J. Liu, C. Wang, J. Wang, H. Zhu, C. Lu · **[S]** | RSS 2023 workshop; ICRA 2024 (per project-page citation) | **110,000+** contact-rich real-robot sequences with video, force, audio and action; Flexiv is one of **4 arm types** (2 of 7 platform configs) | [Project page + download](https://rh20t.github.io/) · [API (MIT)](https://github.com/rh20t/rh20t_api) | T01 T03 T04 |
| [AnyGrasp: Robust and Efficient Grasp Perception in Spatial and Temporal Domains](https://arxiv.org/abs/2212.08333) | H.-S. Fang, C. Wang, H. Fang, M. Gou, J. Liu, H. Yan, W. Liu, Y. Xie, C. Lu · **[S]** | IEEE T-RO (accepted 2023) | Dense 7-DoF grasp detection from one depth view, plus grasp tracking for moving objects; the dynamic-grasp experiments run on a Rizon via Flexiv RDK | [Project page](https://graspnet.net/anygrasp.html) · [SDK](https://github.com/graspnet/anygrasp_sdk) (licence terms ⚠️ unverified) | **T01 T03** T04 |
| [RFUniverse: A Multiphysics Simulation Platform for Embodied AI](https://arxiv.org/abs/2202.00199) | H. Fu, W. Xu, R. Ye, H. Xue, Z. Yu, T. Tang, Y. Li, W. Du, J. Zhang, C. Lu · **[S]** | arXiv 2022 | Unity-based simulator (rigid, cloth, fluid, cutting); example tasks use a *simulated* Flexiv arm (banana cutting, butter spreading) | [Project page](https://sites.google.com/view/rfuniverse) | T04 T03 |

## Datasets, models and benchmarks released

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| Flexiv Trainer | ✅ Data-collection + training app (Flexiv) | Apache-2.0 | [flexiv_trainer](https://github.com/flexivrobotics/flexiv_trainer) | Record force-feedback teleop demos as **LeRobot** episodes and train policies locally; includes an experimental **B-Spline Diffusion** action format and "step skill" practice on the robot |
| Flexiv TDK | ✅ Teleoperation SDK (Flexiv) | Apache-2.0 | [flexiv_tdk](https://github.com/flexivrobotics/flexiv_tdk) | Arm-to-arm teleop with force feedback — the system credited in Force Policy and FP2 |
| Flexiv robot models + Isaac Sim bridge | ✅ URDF / simulation (Flexiv) | Apache-2.0 | [flexiv_description](https://github.com/flexivrobotics/flexiv_description) · [isaac_sim_ws](https://github.com/flexivrobotics/isaac_sim_ws) | Simulate Rizon with the real force/torque controller in the loop |
| Flexiv AIDK ("Noema Edge") | ✅ on GitHub, last push **2024-03** (looks dormant) | Apache-2.0 | [flexiv_aidk](https://github.com/flexivrobotics/flexiv_aidk) | Confirms the "Noema" AI product name from earlier notes; not a current path for a 48-hour build |
| Flexiv dataset / foundation-model weights | — none released | — | — | Flexiv itself has published **no** dataset or pretrained model |
| RH20T | ✅ Dataset (SJTU) | RH20T-C: **CC BY-SA 4.0** · RH20T-NC: **CC BY-NC 4.0** | [rh20t.github.io](https://rh20t.github.io/) · [API (MIT)](https://github.com/rh20t/rh20t_api) | Pre-training with real force/torque streams recorded partly on Flexiv arms |
| AnyGrasp SDK | ✅ Grasp-detection model, binary SDK (SJTU) | Registration-based; terms ⚠️ unverified | [anygrasp_sdk](https://github.com/graspnet/anygrasp_sdk) | Drop-in grasp poses from an RGB-D camera for pick, sort and handover demos |
| Reactive Diffusion Policy + TactAR | ✅ Code, weights, dataset | Code **MIT**; weights / data licence not checked | [code](https://github.com/xiaoxiaoxh/reactive_diffusion_policy) · [weights](https://huggingface.co/WendiChen/reactive_diffusion_policy_model) · [dataset](https://huggingface.co/datasets/WendiChen/reactive_diffusion_policy_dataset) | Closest ready-made stack for peeling / wiping on **Rizon 4 + Grav** |
| ImplicitRDP | ✅ Code, weights, dataset | Not checked | [code](https://github.com/Chen-Wendi/ImplicitRDP) · [weights](https://huggingface.co/WendiChen/ImplicitRDP_model) · [dataset](https://huggingface.co/datasets/WendiChen/ImplicitRDP_dataset) | Visual-force policy on Rizon 4s |
| Force Policy | ✅ Code | Not checked | [ForcePolicy](https://github.com/force-policy/ForcePolicy) | Hybrid force-position policy for polishing / insertion |
| RISE family (RISE, RISE-2, HistRISE, CAGE) | ✅ Code | RISE: **CC BY-NC-SA 4.0**; others not checked | [rise](https://github.com/rise-policy/rise) · [RISE-2](https://github.com/rise-policy/RISE-2) · [HistRISE](https://github.com/rise-policy/HistRISE) · [CAGE](https://github.com/cage-policy/CAGE) | 3D point-cloud imitation policies trained from tens of demos on a Rizon |
| AirExo / AirExo-2 | ✅ Open hardware + code | Not checked | [airexo-models](https://github.com/AirExo/airexo-models) · [AirExo-2](https://github.com/AirExo/AirExo-2) | Printable exoskeleton for demo collection (has a Flexiv-specific model folder) |
| ForceMimic (ForceCapture + HybridIL) | ✅ Open hardware + code | Not checked | [forcecapture](https://github.com/ForceMimic/forcecapture) · [hybridil](https://github.com/ForceMimic/hybridil) | Record human force demos by hand, replay with RDK force primitives |
| FoAR, UniFolding, SIME, KnowledgeIL, MBA, Dense Policy | ✅ Code | Not checked | [FoAR](https://github.com/Alan-Heoooh/FoAR) · [UniFolding](https://github.com/xiaoxiaoxh/UniFolding) · [SIME](https://github.com/EricJin2002/SIME) · [KnowledgeIL](https://github.com/mioam/KnowledgeIL) · [MBA](https://github.com/Selen-Suyue/MBA) · [DensePolicy](https://github.com/Selen-Suyue/DensePolicy) | Reference implementations already wired to Flexiv arms |

Check each repo's LICENSE before reuse: several are non-commercial.

## Third-party papers using their hardware or software

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [VAMPS: Visual and Motor Policies from Sampling-Based Planning](https://arxiv.org/abs/2610.05331) | M. Y. Kabouri, P. N. Crestaz, Q.-N. Nguyen, Q. Cheng, L. Righetti, N. Mansard · LAAS-CNRS Toulouse / NYU Machines in Motion | arXiv, Oct 2026 | **Rizon 10s** (plus a Unitree Go2) | A sampling-based planner (MPPI) generates the training data, then an ACT policy is trained on it; demos: pick-and-place and **force-aware whiteboard erasing** | T01 T03 |
| [Devol-ONE: One Autoregressive Mixture of Transformers to Unify Vision-Language-Action and Latent World Modeling](https://arxiv.org/abs/2609.32193) | H. Cai, Y. H. Ong, T. C. Wu, C. H. Lim, H. Li, K. Guo, S. Y. Cheong · Devol Robots (San Francisco) | arXiv, Sep 2026 | **Two Rizon arms**, 3 RealSense cameras, Meta Quest VR teleoperation | A VLA + world model evaluated on single- and dual-arm Flexiv setups | T01 |
| [ADEPT: Accelerating Dexterity via Pre-Training and Post-Training using Reinforcement Learning](https://arxiv.org/abs/2608.19182) | J. Lee, J. Yin, A. Rana, N. Blauch, O. Zhang, S. Mady, M. Bhardwaj, N. Fazeli, N. Ratliff, K. Van Wyk, A. Handa · **NVIDIA** / Univ. of Michigan | CoRL 2026 | 7-DoF **Rizon + 22-DoF Sharpa hand** (29 DoF), 2 RGB cameras, 5 fingertip tactile sensors | Sim-to-real RL for dexterous grasp-reorient-insert; the Flexiv-Sharpa system solves peg insertion from vision + touch | T02 T04 |
| [Cooptimizing Safety and Performance Using Safety Value-Constrained Model Predictive Control](https://arxiv.org/abs/2604.23863) | H. Wang, N. Nguyen, A. Jordana, L. Righetti, S. Bansal · USC / Stanford and co-authors | arXiv, Apr 2026 | **Rizon 10s**, torque control, **6.8 kg** payload | MPC that keeps the arm inside safety limits (payload, obstacles) while still performing the task | T02 T04 |
| [A strictly predefined-time convergent and anti-noise fractional-order zeroing neural network for solving time-variant quadratic programming in kinematic robot control](https://arxiv.org/abs/2503.01857) | Y. Yang, X. Li, X. Wang, M. Liu, J. Yin, W. Li, R. M. Voyles, X. Ma | arXiv, Feb 2025 (accepted; venue not checked) | Rizon (real + simulated), Franka in simulation | Noise-tolerant redundancy resolution for 7-DoF path tracking | — |
| [A Predefined-Time Convergent and Noise-Tolerant Zeroing Neural Network Model for Time Variant Quadratic Programming With Application to Robot Motion Planning](https://arxiv.org/abs/2412.20477) | Y. Yang, X. Wang, R. M. Voyles, X. Ma | arXiv, Dec 2024 (accepted; venue not checked) | Rizon (real + CoppeliaSim) | Same line of work: cyclic motion planning on the Rizon | — |
| [RH20T-P: A Primitive-Level Robotic Dataset Towards Composable Generalization Agents](https://arxiv.org/abs/2403.19622) | Z. Chen, Z. Shi, X. Lu, L. He, S. Qian, Z. Yin, W. Ouyang, J. Shao, Y. Qiao, C. Lu, L. Sheng | NeurIPS 2024 workshop | Built on the RH20T dataset (no Flexiv-specific claim in the text) | Re-annotates RH20T at primitive-skill level for language-driven planners | T01 |
| [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://arxiv.org/abs/2310.08864) | Open X-Embodiment Collaboration (co-authors include C. Lu, H.-S. Fang, H. Fang) | arXiv 2023 | Pooled multi-lab datasets; inclusion of RH20T / Flexiv data ⚠️ not re-verified in this pass | Cross-robot pre-training; relevant if you fine-tune an open VLA for a Rizon | — |

Not listed because the arXiv text does not name Flexiv (checked): MOMA-Force, RoboNinja, ViTaMIn, TransCG, DeformPAM, AnyDexGrasp, TacDexGrasp, Human-Agent Joint Learning, Robot Cooking with Stir-fry.

## Reading list by track

### T01 Autonomous Urban Services
- **[AnyGrasp](https://arxiv.org/abs/2212.08333)** — fastest route to "pick up whatever is in front of the camera"; SDK available, already run on a Rizon.
- **[Flexible Handover](https://arxiv.org/abs/2308.15622)** — taking an item from a person's moving hand; template for a concierge / retail hand-over demo.
- **[RISE](https://arxiv.org/abs/2404.12281)** and **[CAGE](https://arxiv.org/abs/2410.14974)** — imitation policies trained from tens of demos; code targets the Rizon + RealSense setup you are likely to get.
- **[History-Aware Policy](https://arxiv.org/abs/2509.17141)** — read if your service task has repeated steps (stock three shelves, press a button twice).
- **[VAMPS](https://arxiv.org/abs/2610.05331)** — whiteboard erasing is a small-scale surface-cleaning task with force in the loop.

### T02 Resilient & Safe City
- **[AirExo](https://arxiv.org/abs/2309.14975)** / **[AirExo-2](https://arxiv.org/abs/2503.03081)** — low-cost exoskeleton teleoperation; the pattern for a hazardous-environment remote-handling demo.
- **[Reactive Diffusion Policy](https://arxiv.org/abs/2503.02881)** — the TactAR part: AR headset teleoperation with force feedback from the Rizon's joint torque sensors.
- **[Force Policy](https://arxiv.org/abs/2602.22088)** — connector / plug insertion with regulated force; maps to "mate a connector or turn a valve on damaged infrastructure".
- **[Safety Value-Constrained MPC](https://arxiv.org/abs/2604.23863)** — how to keep a torque-controlled Rizon 10s inside hard safety limits.
- **[ADEPT](https://arxiv.org/abs/2608.19182)** — dexterous-hand insertion on a Rizon, for teams that also have a multi-finger hand.
- No paper found on search-and-rescue, patrol or outdoor inspection with Flexiv hardware.

### T03 Sustainable City
- **[FP2](https://arxiv.org/abs/2609.37433)** — includes an **EV-charger insertion** task on a Rizon 4: the single most on-topic paper for an EV-charging demo.
- **[Force Policy](https://arxiv.org/abs/2602.22088)** — polishing and insertion; basis for refurbish / repair (circular-economy) demos.
- **[AnyGrasp](https://arxiv.org/abs/2212.08333)** — cluttered-bin grasping for waste sorting; add your own material classifier.
- **[ForceMimic](https://arxiv.org/abs/2410.07554)** and **[FoAR](https://arxiv.org/abs/2411.15753)** — peeling with controlled force; transferable to produce handling or label / coating removal.
- **[Knowledge-Driven IL](https://arxiv.org/abs/2506.21057)** — generalising one sorting skill to unseen object instances.
- No paper found on energy systems or environmental monitoring with Flexiv hardware.

### T04 Elderly Care & Rehabilitation
- **[Reactive Diffusion Policy](https://arxiv.org/abs/2503.02881)** — peeling, wiping and two-arm lifting on Rizon 4 + Grav: household assistance with gentle contact; code and weights are public.
- **[Flexible Handover](https://arxiv.org/abs/2308.15622)** — robot receives objects from a person; basis for medication or cup hand-over.
- **[UniFolding](https://arxiv.org/abs/2311.01267)** — laundry folding with two Rizon arms; a caregiver-relief task.
- **[ImplicitRDP](https://arxiv.org/abs/2512.10946)** — visual-force policy on the high-sensitivity Rizon 4s, relevant when contact with a person or soft object must stay light.
- **[Force Policy](https://arxiv.org/abs/2602.22088)** — sustained surface contact at a set force; the control idea closest to massage-style strokes.
- **No directly relevant paper found** on robotic massage, physiotherapy or rehabilitation using Flexiv arms. Mello (Flexiv's massage product) has no public paper that could be located in this pass.

## White papers, patents and technical reports

- **Flexiv blog, Nov 2026 — "What NVIDIA's GB300 Assembly Research Reveals About Force-Controlled Robotics".** Describes an NVIDIA Seattle Robotics Lab + Isaac team study that automated GB300 tester-tray work (busbar assembly with **16 screws**, four cable-connector insertions) using **two Rizon 4s** plus one conventional cobot, coordinated by NVIDIA's TALOS orchestration system, with hybrid position / force control and learned insertion policies. The blog's link to the NVIDIA paper is a broken placeholder; the underlying paper could **not** be located ⚠️ unverified.
- **IEEE Spectrum, 2024-02-06 — gecko-adhesive gripper cleaning station.** News article (not a paper) on Grav Enhanced: dry-adhesive pads reported to last **2 million** grip cycles, and a "tongue" station that wipes them clean, built after a recycling-sorting customer needed it. No associated publication is cited. Relevant to T03.
- **NVIDIA Isaac reference workflow (Rizon 4 + Grav, RL cable insertion, Sept 2026)** — see the [profile](Flexiv.md); no accompanying paper was found.
- **Patents:** not searched in this pass (search budget exhausted). Nothing to list.

## Sources

- [arXiv 2609.37433 — FP2](https://arxiv.org/abs/2609.37433)
- [arXiv 2609.16815 — Rethinking Visual Embodiment Dependence](https://arxiv.org/abs/2609.16815)
- [arXiv 2602.22088 — Force Policy](https://arxiv.org/abs/2602.22088)
- [arXiv 2512.10946 — ImplicitRDP](https://arxiv.org/abs/2512.10946)
- [arXiv 2509.17141 — History-Aware Visuomotor Policy Learning](https://arxiv.org/abs/2509.17141)
- [arXiv 2506.21057 — Knowledge-Driven Imitation Learning](https://arxiv.org/abs/2506.21057)
- [arXiv 2505.22159 — ForceVLA](https://arxiv.org/abs/2505.22159)
- [arXiv 2505.01396 — SIME](https://arxiv.org/abs/2505.01396)
- [arXiv 2503.13217 — Dense Policy](https://arxiv.org/abs/2503.13217)
- [arXiv 2503.03081 — AirExo-2](https://arxiv.org/abs/2503.03081)
- [arXiv 2503.02881 — Reactive Diffusion Policy](https://arxiv.org/abs/2503.02881)
- [arXiv 2411.15753 — FoAR](https://arxiv.org/abs/2411.15753)
- [arXiv 2411.09658 — Motion Before Action](https://arxiv.org/abs/2411.09658)
- [arXiv 2410.14974 — CAGE](https://arxiv.org/abs/2410.14974)
- [arXiv 2410.07554 — ForceMimic](https://arxiv.org/abs/2410.07554)
- [arXiv 2404.12281 — RISE](https://arxiv.org/abs/2404.12281)
- [arXiv 2311.01267 — UniFolding](https://arxiv.org/abs/2311.01267)
- [arXiv 2309.14975 — AirExo](https://arxiv.org/abs/2309.14975)
- [arXiv 2308.15622 — Flexible Handover](https://arxiv.org/abs/2308.15622)
- [arXiv 2307.00595 — RH20T](https://arxiv.org/abs/2307.00595)
- [arXiv 2212.08333 — AnyGrasp](https://arxiv.org/abs/2212.08333)
- [arXiv 2202.00199 — RFUniverse](https://arxiv.org/abs/2202.00199)
- [arXiv 2610.05331 — VAMPS](https://arxiv.org/abs/2610.05331)
- [arXiv 2609.32193 — Devol-ONE](https://arxiv.org/abs/2609.32193)
- [arXiv 2608.19182 — ADEPT](https://arxiv.org/abs/2608.19182)
- [arXiv 2604.23863 — Safety Value-Constrained MPC](https://arxiv.org/abs/2604.23863)
- [arXiv 2503.01857 — SPTC-AN-FOZNN](https://arxiv.org/abs/2503.01857)
- [arXiv 2412.20477 — PTC-NT-FOZNN](https://arxiv.org/abs/2412.20477)
- [arXiv 2403.19622 — RH20T-P](https://arxiv.org/abs/2403.19622)
- [arXiv 2310.08864 — Open X-Embodiment](https://arxiv.org/abs/2310.08864)
- [RH20T project page (dataset description, licence)](https://rh20t.github.io/)
- [RH20T API on GitHub (robot configs, MIT licence)](https://github.com/rh20t/rh20t_api)
- [AnyGrasp project page](https://graspnet.net/anygrasp.html)
- [Reactive Diffusion Policy project page](https://reactive-diffusion-policy.github.io/)
- [ImplicitRDP project page](https://implicit-rdp.github.io/)
- [Force Policy project page](https://force-policy.github.io/)
- [FP2 project page](http://force-policy.github.io/fp2)
- [RISE project page](https://rise-policy.github.io/)
- [RISE code and licence](https://github.com/rise-policy/rise)
- [CAGE project page](https://cage-policy.github.io/)
- [AirExo project page](https://airexo.github.io/)
- [AirExo-2 project page](https://airexo.tech/airexo2/)
- [ForceMimic project page](https://forcemimic.github.io/)
- [FoAR project page](https://tonyfang.net/FoAR/)
- [History-aware policy project page](https://tonyfang.net/history/)
- [UniFolding project page](https://unifolding.robotflow.ai/)
- [ADEPT project page](https://adept-dexterity.github.io/)
- [Noematrix — official site](https://www.noematrix.ai/en)
- [Flexiv — news and blog list](https://www.flexiv.com/news)
- [Flexiv blog — What NVIDIA's GB300 Assembly Research Reveals About Force-Controlled Robotics](https://www.flexiv.com/news/NVIDIA-GB300Assembly)
- [Flexiv — company history](https://www.flexiv.com/history)
- [GitHub — flexivrobotics organisation](https://github.com/flexivrobotics)
- [GitHub — flexiv_trainer README](https://github.com/flexivrobotics/flexiv_trainer)
- [GitHub — flexiv_aidk (Noema Edge)](https://github.com/flexivrobotics/flexiv_aidk)
- [IEEE Spectrum — Robotic Tongue Licks Gecko Gripper Clean (2024-02-06)](https://spectrum.ieee.org/flexiv-gecko-gripper)
