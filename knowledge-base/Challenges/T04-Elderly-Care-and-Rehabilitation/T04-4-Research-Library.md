---
type: track-research-library
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, papers]
---
# T04 Elderly Care & Rehabilitation — Research Library

> Compiled 2026-11-14 15:57: papers relevant to this track, per company (company-authored and third-party work on their hardware).

[Start here](../../00-START-HERE.md) · [Track overview](T04-0-Track-Overview.md) · [Hardware shortlist](T04-2-Hardware-Shortlist.md)

## Dobot Robotics

**Reading list from the company papers doc:**

No directly relevant paper found (no physiotherapy, massage, rehabilitation or assistive-feeding paper on Dobot hardware surfaced in this pass, despite Dobot marketing Nova 5 for physiotherapy). Closest building blocks:
- [Human-robot shared control on CR10](https://arxiv.org/abs/2606.24629) — human-like, lower-jerk motion; relevant to any arm moving near a patient or to caregiver telepresence.
- [Video + speech + LLM HRI on Dobot Magician](https://arxiv.org/abs/2602.20219) — voice interface for "fetch / hand me" assistance.
- [DobotTrack](https://arxiv.org/abs/2611.09041) — follow a specific person described in words; basis for a companion or walking-escort robot.
- [Diff-ILC on CR3](https://arxiv.org/abs/2611.01220) — improves accuracy of repeated trajectories using only the position interface; applicable to repetitive guided-exercise paths.
- [GM-100](https://arxiv.org/abs/2601.11421) — household-style bimanual tasks and data on X-Trainer for assistive manipulation policies.

→ [All papers of Dobot Robotics](../../Companies/Dobot/Dobot-Papers-and-Research.md)

## Flexiv Robotics

**Reading list from the company papers doc:**

- **[Reactive Diffusion Policy](https://arxiv.org/abs/2503.02881)** — peeling, wiping and two-arm lifting on Rizon 4 + Grav: household assistance with gentle contact; code and weights are public.
- **[Flexible Handover](https://arxiv.org/abs/2308.15622)** — robot receives objects from a person; basis for medication or cup hand-over.
- **[UniFolding](https://arxiv.org/abs/2311.01267)** — laundry folding with two Rizon arms; a caregiver-relief task.
- **[ImplicitRDP](https://arxiv.org/abs/2512.10946)** — visual-force policy on the high-sensitivity Rizon 4s, relevant when contact with a person or soft object must stay light.
- **[Force Policy](https://arxiv.org/abs/2602.22088)** — sustained surface contact at a set force; the control idea closest to massage-style strokes.
- **No directly relevant paper found** on robotic massage, physiotherapy or rehabilitation using Flexiv arms. Mello (Flexiv's massage product) has no public paper that could be located in this pass.

→ [All papers of Flexiv Robotics](../../Companies/Flexiv/Flexiv-Papers-and-Research.md)

## Galaxea

**Reading list from the company papers doc:**

No care-home or clinical study found; the household-assistance literature is strong:

- [BEHAVIOR Robot Suite](https://arxiv.org/abs/2503.05652) — the reference for daily-living tasks on the R1 (T04.1), with open teleop hardware design.
- [G0.5](https://arxiv.org/abs/2608.11739) — household long-horizon results (BEHAVIOR Challenge) and R1 fine-tuning numbers.
- [Fast-WAM](https://arxiv.org/abs/2603.16666) — towel folding on R1 Lite in real time; laundry is a credible T04.6 demo.
- [EgoScale](https://arxiv.org/abs/2602.16710) — dexterous hands on the R1 Pro learned mostly from human video.
- [SafeBimanual](https://arxiv.org/abs/2508.18268) — safety layer for dual-arm motion near a person.
- [MoMaGen](https://arxiv.org/abs/2510.18316) — scale one demo of a multi-step home task into a training set.

→ [All papers of Galaxea](../../Companies/Galaxea/Galaxea-Papers-and-Research.md)

## AGIBOT

**Reading list from the company papers doc:**

- [ACoT-VLA](https://arxiv.org/abs/2601.11404) — real G1 tests on pouring water, wiping and picking unseen objects: the building blocks of assistive household help.
- [WholeBodyVLA](https://arxiv.org/abs/2512.11047) — X2 humanoid fetching across a room; relevant to "bring me the object" assistance.
- [Learning to Live (LIFE)](https://arxiv.org/abs/2611.00180) — day-long memory and event detection; basis for a companion that notices routines, missed medication or a fall-like event.
- [TrajBooster](https://arxiv.org/abs/2509.11839) — household manipulation at different heights (floor to shelf) transferred from AGIBOT data to a biped.
- [GigaBrain-0](https://arxiv.org/abs/2510.19430) — laundry folding and similar caregiver-relief chores on a G1.
- No paper found on rehabilitation, physiotherapy, exoskeleton / EMG interfaces or clinical elder-care trials with AGIBOT hardware.

→ [All papers of AGIBOT](../../Companies/AGIBOT/AGIBOT-Papers-and-Research.md)

## Binabik AI

**Reading list from the company papers doc:**

- [Shared Control of Holonomic Wheelchairs through Reinforcement Learning](https://arxiv.org/abs/2507.17055): assistive driving that keeps the user in control; first real-world RL shared control on an omnidirectional platform according to the authors (T04.4).
- [Follow-Me in Micro-Mobility with End-to-End Imitation Learning](https://arxiv.org/abs/2511.05158): comfort-first person following for people with reduced mobility; the metrics transfer to any follow-me robot (T04.4).
- [Benchmarking ML Approaches to UWB-Based Range-Only Posture Recognition](https://arxiv.org/abs/2408.15717): camera-free posture sensing, a privacy-friendly angle for monitoring (T04.7, T04.5).
- [ReGATE](https://arxiv.org/abs/2611.02871): humanoid handling of boxes in a medical-equipment cleaning and sterilisation project (T04.6).
- [Towards Embodied Agentic AI](https://arxiv.org/abs/2508.05294): patterns for a natural-language interface to a care robot (T04.5).

→ [All papers of Binabik AI](../../Companies/Binabik-AI/Binabik-AI-Papers-and-Research.md)

## D-Robotics

**Reading list from the company papers doc:**

- [Service robot for the elderly and disabled on RDK-X5](https://doi.org/10.1117/12.3095395): the only paper found that targets this track on this hardware; check the design before choosing yours.
- [RTPolicy](https://arxiv.org/abs/2610.41625): the D-Robotics answer to "can a learned arm policy run on the board"; yes on S100 at about 11.6 Hz and S600 at 32.9 Hz (T04.1).
- [VO-DP](https://arxiv.org/abs/2510.15530): one camera, 200 demos per task, pick-and-place and stacking at 87.9 % real-world success.
- [ISR](https://arxiv.org/abs/2606.22907): clean up shaky teleoperated demos; small tool, quick win for any imitation-learning build.
- [MODEST](https://arxiv.org/abs/2502.14616): drinking glasses and clear bottles are the classic failure of depth cameras in care settings.
- [RDK X3 + myCobot 320 study](https://doi.org/10.1109/telecom66943.2025.11304042): mobile manipulator with re-planning on the cheapest board (T04.6).

→ [All papers of D-Robotics](../../Companies/D-Robotics/D-Robotics-Papers-and-Research.md)

## Leadshine Technology

**Reading list from the company papers doc:**

- [Robot arm-assisted acupuncture system (Front. Bioeng. Biotechnol. 2025)](https://doi.org/10.3389/fbioe.2025.1563263) — how to bolt a small actuator to an arm flange and validate motion and force against a human therapist; method transfers to any care-procedure demo (T04.2, T04.6).
- [In vitro joint testing system (Bioengineering 2023)](https://doi.org/10.3390/bioengineering10091006) — force-profile tracking with a Leadshine motion card + stepper; useful for rehab-training force targets (T04.3).
- [Upright radiotherapy platform (Medical Physics 2025)](https://doi.org/10.1002/mp.17523) — patient-carrying rotation stage; safety margins, load assumptions and accuracy tests for moving a seated person (T04.4).
- [3D-printed multi-directional tactile sensor (Commun. Eng. 2023)](https://doi.org/10.1038/s44172-023-00131-x) — what normal / shear fingertip sensing enables on an anthropomorphic hand; context for the tactile DH116-M and DH2116 (T04.5).
- [Dexterous-hand survey (arXiv 2611.06724)](https://arxiv.org/abs/2611.06724) — general background for hand-over and assistive manipulation; does not mention Leadshine.

→ [All papers of Leadshine Technology](../../Companies/Leadshine/Leadshine-Papers-and-Research.md)

## Magiclab Robotics

No paper by Magiclab or by a third party on elderly care, rehabilitation, fall detection or care-setting safety with Magiclab hardware was found (an arXiv full-text query for "MagicBot", "MagicDog" and "Magiclab Robotics" returned no third-party result). The papers below are relevant by **task type** (household manipulation, smooth motion, exercise demonstration). All seven were opened on arXiv today. Company experiments run on table-top dual-arm rigs, not on MagicBot or MagicDog.

| Paper (title as a link) | Authors / organisation | Venue, year | Why it matters here | Code / data |
|---|---|---|---|---|
| [Toward Real-Time VLAs: Stage-Aware Two-Step Flow Denoising and System-Level Evaluation](https://arxiv.org/abs/2609.39822) | Di Wu, Rongtian Shen, Ping Liu, Yan Shen, Zhenhan Yin, Shun Zuo, Xuhua Chen, He Zheng, Lingfeng Zhang, Jianglin Zhang, Tao Zhang — Magiclab Robotics and university co-affiliations | arXiv preprint, Sep 2026 | T04.1: long-horizon **garment folding** with per-method success rates; shows which execution strategy gives smooth motion — relevant for anything moving near people | [Code (Apache-2.0)](https://github.com/MagiclabRobotics/Inference) |
| [Execution-Aligned Progressive Noise for Consistent Asynchronous Replanning in Generative Robot Policies](https://arxiv.org/abs/2610.06090) | Di Wu, Ping Liu, Xuhua Chen, He Zheng, Lingfeng Zhang, Tao Zhang — Magiclab Robotics | arXiv preprint, Oct 2026 | T04.1: explains why learned policies jerk or switch plan mid-task and one fix; tested on object storage and bimanual cloth folding | No code link found |
| [Magic-W0: A Structured World-Action Foundation Model for Physical Intelligence](https://arxiv.org/abs/2609.39870) | Xuhua Chen, Zhenhan Yin, Yuan Zhang, Lingfeng Zhang, He Zheng, … Tao Zhang (18 authors) — Magic-Lab Team, Magiclab Robotics | arXiv preprint, Sep 2026 | T04.1: open foundation model fine-tuned for household tasks (clothes folding, object and kitchen storage); a starting point if a team collects its own demonstrations | [Code (MIT)](https://github.com/MagiclabRobotics/Magic-W0) · [Weights](https://huggingface.co/XuhuaX/Magic-W0) |
| [Dual-Stream Memory for Vision-Language-Action Policies](https://arxiv.org/abs/2610.13262) | Yang Wang, Ping Liu, Ruiyu Wang, Xuhua Chen, Lingfeng Zhang, Tao Zhang — Magiclab Robotics; UCLA | arXiv preprint, Oct 2026 | T04.1 / T04.7: tasks that need "have I already done this?" — counting repetitions, remembering whether a medication step was completed | [Project page](https://embodied.magiclab.top/works/memory/index.html); no code |
| [Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking](https://arxiv.org/abs/2510.02252) | Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, C. Karen Liu — Stanford (third party; ported to Z1 by Magiclab) | arXiv preprint, Oct 2025 | T04.3: route to make a Z1 **demonstrate a physiotherapy movement** recorded from a human | [Magiclab_GMR (MIT)](https://github.com/MagiclabRobotics/Magiclab_GMR) |
| [BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion](https://arxiv.org/abs/2508.08241) | Qiayuan Liao, Takara E. Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, C. Karen Liu — UC Berkeley / Stanford (third party; ported to Z1 by Magiclab) | arXiv preprint, Aug 2025 | T04.3 / T04.5: tracking policy that lets Z1 execute retargeted gestures and exercise motions; needs simulation training | [magicbot-mimic (MIT)](https://github.com/MagiclabRobotics/magicbot-mimic) |
| [TWIST: Teleoperated Whole-Body Imitation System](https://arxiv.org/abs/2505.02833) | Yanjie Ze, Zixuan Chen, João Pedro Araújo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, C. Karen Liu — Stanford / SFU (third party; cited by Magiclab's retargeting repo) | arXiv preprint, May 2025 | T04.2: background for a tele-operated care-avatar concept | [pico_teleoperate (BSD-3)](https://github.com/MagiclabRobotics/pico_teleoperate) (Magiclab's own Gen1 teleoperation kit) |

- Not listed: *Conditional Trajectory Peaks* (generic manipulation speed-up, no care link) — see [Papers and research](../../Companies/Magiclab/Magiclab-Papers-and-Research.md).
- A company blog post mentions a 2026 UC Davis study of a humanoid companion robot in memory care, without a link and without saying a Magiclab robot was used — not opened, not counted.

**Reading list from the company papers doc:**

- [Toward Real-Time VLAs](https://arxiv.org/abs/2609.39822) — long-horizon **garment folding** with honest per-method success rates and open runtime code; shows which execution strategy to pick (Legato or VLASH, not naive async) for smooth motion near people.
- [Execution-Aligned Progressive Noise](https://arxiv.org/abs/2610.06090) — why generative policies jerk or switch plan mid-task, and one fix; smoothness matters for assistive use.
- [Magic-W0](https://arxiv.org/abs/2609.39870) — household tasks (clothes folding, object storage, kitchen storage, pen storage) at about 95% success after fine-tuning, company-reported.
- [Dual-Stream Memory](https://arxiv.org/abs/2610.13262) — tasks that need "have I already done this?" (for example, a medication-count or repeat-exercise step).
- [Retargeting Matters (GMR)](https://arxiv.org/abs/2510.02252) with [`Magiclab_GMR`](https://github.com/MagiclabRobotics/Magiclab_GMR) and [`magicbot-mimic`](https://github.com/MagiclabRobotics/magicbot-mimic) — the route to having Z1 **demonstrate a physiotherapy movement** recorded from a human.
- No company paper on elder care, rehabilitation, fall detection or human-safety evaluation was found.

→ [All papers of Magiclab Robotics](../../Companies/Magiclab/Magiclab-Papers-and-Research.md)

## Omnicor AI

**Reading list from the company papers doc:**

- [pi0.5](https://arxiv.org/abs/2504.16054) — the most relevant: household tasks in homes never seen in training (T04.1, T04.6).
- [Apertus](https://arxiv.org/abs/2509.14233) — open, compliance-oriented Swiss LLM; the argument for a private on-device assistant in local languages where no patient data leaves the room (T04.5, T04.7).
- [Real-time chunking](https://arxiv.org/abs/2506.07339) — smoother motion near people when inference is slow (T04.2).
- [OpenVLA-OFT](https://arxiv.org/abs/2502.19645) — bimanual, high-frequency fine-tuning recipe for assistive manipulation (T04.1).
- [SmolVLA](https://arxiv.org/abs/2506.01844) — lightest path to a working fetch-and-hand-over demo.

→ [All papers of Omnicor AI](../../Companies/Omnicor-AI/Omnicor-AI-Papers-and-Research.md)

## OriginFlow

**Reading list from the company papers doc:**

- [PiMForce — posture-informed muscular force](https://arxiv.org/abs/2410.23629) — recipe for grip / press force estimation from sEMG + hand pose; directly reusable for a rehab-exercise feedback demo (T04.3, T04.7).
- [emg2pose](https://arxiv.org/abs/2412.02725) — quantifies cross-user and band-placement generalisation; read before promising that a demo works on a second person.
- [Generic neuromotor interface (Meta, Nature 2025)](https://github.com/facebookresearch/generic-neuromotor-interface) — cross-user intent decoding without per-user training; basis for intent-triggered assistance (T04.1, T04.4).
- [ForceBand](https://arxiv.org/abs/2606.26093) — open training code for sEMG-to-finger-force; adapt for graded grip-strength tracking.
- [Dual-modality haptic feedback with EMG gripper](https://arxiv.org/abs/2209.15578) — feedback design for EMG-driven assistive or prosthetic grasping.
- [MI-DHMI](https://arxiv.org/abs/2609.07495) — from a medical-device lab; joint gesture + force + pose decoding under natural arm movement.
- Caveat: none of these is a clinical study on older adults, and OriginFlow hardware is not a medical device.

→ [All papers of OriginFlow](../../Companies/OriginFlow/OriginFlow-Papers-and-Research.md)

## Spirit AI

**Reading list from the company papers doc:**

- No paper addresses elder care, rehabilitation or medical use directly.
- **[OneTwoVLA](https://arxiv.org/abs/2505.11917)** — reasoning-while-acting for long household chores and for reacting to a person mid-task.
- **[Point-VLA](https://arxiv.org/abs/2512.18933)** — a user (or caregiver on a tablet) points at the object to fetch; low-effort interface for people who cannot give precise verbal descriptions.
- **[KineDex](https://arxiv.org/abs/2505.01974)** and **[FTP-1](https://arxiv.org/abs/2606.13102)** — tactile, force-controlled contact; background reading for any physical-contact task (wiping, pressing, massage-like motions).
- **[EgoTac](https://arxiv.org/abs/2608.15060)** — estimating contact force from egocentric video; useful idea for monitoring how hard a person or robot presses.
- **[CoPa](https://arxiv.org/abs/2403.08248)** — training-free assistive manipulation (open a drawer, pour, hand over) to prototype with.

→ [All papers of Spirit AI](../../Companies/Spirit-AI/Spirit-AI-Papers-and-Research.md)

## Unitree Robotics

**Reading list from the company papers doc:**

- **Guide-robot trio:** **[Kim et al. (AlienGo)](https://arxiv.org/abs/2306.14055)**, **[DeFazio et al. (A1)](https://arxiv.org/abs/2309.04370)**, **[Chen et al. (Laikago)](https://arxiv.org/abs/2203.03927)** — harness / leash interaction, tug sensing, comfort; the best-evidenced assistive use of Unitree quadrupeds.
- **[GentleHumanoid](https://arxiv.org/abs/2511.04679)** — compliant upper body for safe physical contact with people on a G1.
- **[H2-COMPACT](https://arxiv.org/abs/2505.17627)** — humanoid as a carrying partner guided by force cues.
- **[Learning Getting-Up Policies](https://arxiv.org/abs/2502.12152)** / **[HoST](https://arxiv.org/abs/2502.08378)** — robot fall recovery; relevant for safety arguments near frail users.
- **[Helpful DoggyBot](https://arxiv.org/abs/2410.00231)** — fetch-on-request in a home.
- Unitree's own data: **[Push_Wheelchair](https://huggingface.co/datasets/unitreerobotics/G1_WBT_Inspire_Push_Wheelchair)**, **[Adjust_Sickbed](https://huggingface.co/datasets/unitreerobotics/G1_WBT_Brainco_Adjust_Sickbed)**, **[Pick_Up_Medicine](https://huggingface.co/datasets/unitreerobotics/G1_WBT_Brainco_Pick_Up_Medicine)** — evidence of Unitree's planned care direction and usable for fine-tuning.
- No paper found on rehabilitation, physiotherapy, EMG or exoskeleton use of Unitree hardware.

→ [All papers of Unitree Robotics](../../Companies/Unitree/Unitree-Papers-and-Research.md)

## UniX AI

**Reading list from the company papers doc:**

- [UniTac](https://arxiv.org/abs/2606.31451) — tactile reasoning for **skin-safe material choice** (softer towel) and **force-aware grasping of deformable cups**: direct inspiration for gentle handling in T04.1 / T04.2 / T04.6. Shows that even touch *predicted from RGB* improves a π0.5-style policy.
- [Binding Touch to Everything (UniTouch)](https://arxiv.org/abs/2401.18084) — grasp-stability prediction and touch question answering; a ready-made "is this grip secure?" check before handing an object to a person.
- [The Potential of Haptic Foundation Models](https://arxiv.org/abs/2608.28664) — short survey with a benchmark on force, slip and pose; good for picking a tactile model for safe physical assistance.
- [Dexterous Tactile World Model](https://arxiv.org/abs/2609.34286) — background on why force history predicts what a hand does next (relevant to T04.3 rehab-glove ideas); too heavy to train during the event.

→ [All papers of UniX AI](../../Companies/UniX-AI/UniX-AI-Papers-and-Research.md)

## WUJI

**Reading list from the company papers doc:**

No directly relevant paper found (no rehabilitation, assistive or clinical study using the Wuji Glove or Hand was confirmed). Closest useful reading:
- [ContactPose](https://arxiv.org/abs/2007.09545) — reference contact maps of functional grasps; a comparison target for glove tactile maps in a grip-assessment demo.
- [HO-Cap](https://arxiv.org/abs/2406.06843) and [GRAB](https://arxiv.org/abs/2008.11200) — everyday-object grasp motions (cups, bottles, utensils) to retarget for assistive fetch or feeding.
- [TopoRetarget](https://arxiv.org/abs/2606.16272) — shows the Wuji Glove used as a capture device and the pipeline from caregiver demo to robot hand motion.
- [pi0.5](https://arxiv.org/abs/2504.16054) — home-task generalisation, relevant to assistive manipulation in a living space.
- [AnyTeleop](https://arxiv.org/abs/2307.04577) — basis for a telepresence / remote-caregiver hand.

→ [All papers of WUJI](../../Companies/WUJI/WUJI-Papers-and-Research.md)

## coprod Inc.

**Reading list from the company papers doc:**

No directly relevant paper found from coprod. Closest useful background:

- [Quasi-direct-drive hip exoskeleton](https://arxiv.org/abs/2004.00467) — the best single reference for a backdrivable torque-controlled assist joint (T04.3, T04.4); same actuator class as co:act.
- [Proprioceptive actuator design](https://doi.org/10.1109/TRO.2016.2640183) — why low gear ratio gives safe, transparent contact with a person; use it to justify torque caps in your demo.
- [ACT / low-cost bimanual manipulation](https://arxiv.org/abs/2304.13705) and the [LeRobot paper](https://arxiv.org/abs/2602.22818) — if your concept is a tele-operated or learned daily-living assistance task (T04.1, T04.6).

Reminder from the [developer guide](../../Companies/coprod/coprod-Developer-Guide.md): coprod has **no Safe Torque Off module and no safety certification**; demonstrate on a dummy limb.

→ [All papers of coprod Inc.](../../Companies/coprod/coprod-Papers-and-Research.md)

## Genisom AI

**Reading list from the company papers doc:**

- No directly relevant paper found (no assistive, rehabilitation or human-interaction research from Genisom or on its hardware).
- Nearest useful read: [UniGoal](https://arxiv.org/abs/2503.10630) — "find and go to" behaviours for a fetch-and-follow companion built on `genisom_vln`.

→ [All papers of Genisom AI](../../Companies/Genisom-AI/Genisom-AI-Papers-and-Research.md)

## SKYLANDX

**Reading list from the company papers doc:**

- **No directly relevant paper found.**
- Transferable only: the **Wanderland** pipeline (scan → 3DGS → USDZ → Isaac Sim) can be pointed at a care room or apartment to give another team's assistive robot a simulation scene. The paper's scenes are urban, not care settings.

→ [All papers of SKYLANDX](../../Companies/SKYLANDX/SKYLANDX-Papers-and-Research.md)
