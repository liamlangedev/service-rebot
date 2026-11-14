---
type: track-research-library
challenge: T03
challenge_title: "Sustainable City"
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, papers]
---
# T03 Sustainable City — Research Library

> Compiled 2026-11-14 15:57: papers relevant to this track, per company (company-authored and third-party work on their hardware).

[Start here](../../00-START-HERE.md) · [Track overview](T03-0-Track-Overview.md) · [Hardware shortlist](T03-2-Hardware-Shortlist.md)

## Dobot Robotics

**Reading list from the company papers doc:**

No directly relevant paper found (nothing on waste sorting, energy or environmental monitoring with Dobot hardware in the catalogues this pass could reach). Closest building blocks:
- [Video + speech + LLM HRI on Dobot Magician](https://arxiv.org/abs/2602.20219) — open-vocabulary detection driving a desktop arm; swap the prompt for waste classes to get a sorter.
- [Phone2Act](https://arxiv.org/abs/2605.01948) and [CR5A-Pick_Orange dataset + ACT checkpoint](https://huggingface.co/datasets/Dobot-Official/CR5A-Pick_Orange) — learned pick-and-place pipeline to adapt to sorting bins.
- [A0](https://arxiv.org/abs/2504.12636) — affordance (contact point) prediction that transfers across arms, shown on X-Trainer.

→ [All papers of Dobot Robotics](../../Companies/Dobot/Dobot-Papers-and-Research.md)

## Flexiv Robotics

**Reading list from the company papers doc:**

- **[FP2](https://arxiv.org/abs/2609.37433)** — includes an **EV-charger insertion** task on a Rizon 4: the single most on-topic paper for an EV-charging demo.
- **[Force Policy](https://arxiv.org/abs/2602.22088)** — polishing and insertion; basis for refurbish / repair (circular-economy) demos.
- **[AnyGrasp](https://arxiv.org/abs/2212.08333)** — cluttered-bin grasping for waste sorting; add your own material classifier.
- **[ForceMimic](https://arxiv.org/abs/2410.07554)** and **[FoAR](https://arxiv.org/abs/2411.15753)** — peeling with controlled force; transferable to produce handling or label / coating removal.
- **[Knowledge-Driven IL](https://arxiv.org/abs/2506.21057)** — generalising one sorting skill to unseen object instances.
- No paper found on energy systems or environmental monitoring with Flexiv hardware.

→ [All papers of Flexiv Robotics](../../Companies/Flexiv/Flexiv-Papers-and-Research.md)

## Galaxea

**Reading list from the company papers doc:**

No paper on waste sorting, recycling or environmental monitoring found. Useful for a sorting demo:

- [MobileVISTA](https://arxiv.org/abs/2610.07511) — category-based sorting into bins on the R1 Pro that tolerates imprecise base placement (T03.1, T03.6).
- [DemoGen](https://arxiv.org/abs/2502.16932) — one real demonstration expanded into many; cuts data collection time.
- [G0.5](https://arxiv.org/abs/2608.11739) — includes a language-following pick-and-place benchmark; start from `g05-base` or the legacy pick-and-place checkpoint.
- [DepthVLA](https://arxiv.org/abs/2510.13375) — why depth awareness helps grasp accuracy in cluttered bins.
- [NeSyPack](https://arxiv.org/abs/2506.06567) — reliable pick-and-pack of mixed objects with dual A1X arms.

→ [All papers of Galaxea](../../Companies/Galaxea/Galaxea-Papers-and-Research.md)

## Genisom AI

**Reading list from the company papers doc:**

- No directly relevant paper found (nothing from Genisom on waste, energy or environmental monitoring).
- Nearest useful read: [SmolVLM](https://arxiv.org/abs/2504.05299) — low-power on-board vision-language model, relevant to the "low-power edge AI" angle (for example litter or meter recognition on a patrolling robot).

→ [All papers of Genisom AI](../../Companies/Genisom-AI/Genisom-AI-Papers-and-Research.md)

## SKYLANDX

**Reading list from the company papers doc:**

- No paper on waste, recycling, water or energy was found. Closest transferable work:
- **LiVisSfM (arXiv 2024)** — accurate dense reconstruction of buildings from MetaCam data, the starting point for retrofit or volume measurements (T03.4).
- **Real-time dense stereo embedded in a UAV for road inspection (UAVision 2019)** — infrastructure condition monitoring that extends asset life (T03.4).
- **Wanderland dataset** — a worked example of large-scale environmental 3D data collection and release (T03.7), not an environmental-monitoring study.

→ [All papers of SKYLANDX](../../Companies/SKYLANDX/SKYLANDX-Papers-and-Research.md)

## Unitree Robotics

**Reading list from the company papers doc:**

- **[WildLMa](https://arxiv.org/abs/2411.15131)** — the only verified Unitree-hardware paper here with a litter task (trash clean-up with B1 + Z1).
- **[AgriVLN](https://arxiv.org/abs/2508.07406)** — language-guided navigation in agricultural scenes on a **Go2 Air** (the cheapest Unitree robot).
- **[UMI on Legs](https://arxiv.org/abs/2407.10353)** and **[ODYSSEY](https://arxiv.org/abs/2508.08240)** — manipulation from a Go2 with arm (pick, toss, long-horizon tasks) for litter picking or sorting.
- Unitree's own data: **[Take_Out_The_Rubbish](https://huggingface.co/datasets/unitreerobotics/G1_WBT_SMPL_Brainco_Take_Out_The_Rubbish)**, **[PickOutBatteries](https://huggingface.co/datasets/unitreerobotics/G1_Dex1_PickOutBatteries)**, **[ConveyorSorting](https://huggingface.co/datasets/unitreerobotics/G1_Dex1_ConveyorSorting)** + **[unitree_lerobot](https://github.com/unitreerobotics/unitree_lerobot)** for a G1 sorting policy.
- No directly relevant paper found for energy / building automation, EV charging or low-power edge AI on Unitree hardware.

→ [All papers of Unitree Robotics](../../Companies/Unitree/Unitree-Papers-and-Research.md)

## AGIBOT

**Reading list from the company papers doc:**

- [ALOE](https://arxiv.org/abs/2602.12691) — real multi-object sorting and packing improved by human-in-the-loop RL; the nearest published analogue to waste sorting.
- [SOP](https://arxiv.org/abs/2601.03044) — box assembly and restocking at fleet scale; shows how a few hours of on-robot correction lifts success.
- [Genie Centurion](https://arxiv.org/abs/2505.18793) — rewind-and-refine data collection reaches the same result with under half the demonstrations (less operator time, less energy).
- [AgiBot World Colosseo](https://arxiv.org/abs/2503.06669) plus the ICRA 2026 challenge set — includes package-sorting tasks to start from.
- No directly relevant paper found on energy, EV charging, environmental monitoring, agriculture or low-power edge AI.

→ [All papers of AGIBOT](../../Companies/AGIBOT/AGIBOT-Papers-and-Research.md)

## Binabik AI

**Reading list from the company papers doc:**

- [Gripper-aware Vision Language Action Models](https://arxiv.org/abs/2608.24603): the only directly useful paper; shows how grasp strategy must change between suction and jaw grippers, with an open dataset (T03.1, T03.6).
- [A Method for Multi-Robot Asynchronous Trajectory Execution in MoveIt2](https://arxiv.org/abs/2310.08597): two arms sorting in parallel without waiting on each other (T03.1).
- [ROSBag MCP Server](https://arxiv.org/abs/2511.03497): LLM-driven analysis of recorded sensor data, usable for an environmental data-collection demo (T03.7).
- No paper on energy, water or environmental monitoring was found.

→ [All papers of Binabik AI](../../Companies/Binabik-AI/Binabik-AI-Papers-and-Research.md)

## D-Robotics

**Reading list from the company papers doc:**

- [Debris detection on RDK X5](https://doi.org/10.3390/s26144386): closest published match to litter / waste detection on this hardware (T03.1, T03.7).
- [DOSOD](https://arxiv.org/abs/2412.14680): sort by prompt ("PET bottle", "aluminium can", "cardboard") before you have a labelled dataset (T03.1, T03.6).
- [InstaDA](https://arxiv.org/abs/2509.02973): generate extra labelled instances when you only have a few waste photos.
- [RTPolicy](https://arxiv.org/abs/2610.41625) or [VO-DP](https://arxiv.org/abs/2510.15530): learned pick-and-place for a sorting arm from RGB cameras only.
- [Ridge navigation on RDK X5](https://doi.org/10.1016/j.atech.2026.101797): latency reference for a pruned YOLO11 on the X5 (T03.2).

→ [All papers of D-Robotics](../../Companies/D-Robotics/D-Robotics-Papers-and-Research.md)

## Leadshine Technology

**Reading list from the company papers doc:**

- [Salt-marsh carbon-flux monitoring system (Sensors 2026)](https://doi.org/10.3390/s26102966) — full stack for unattended environmental sensing: sensor node, stepper-driven mast, cloud dashboard, data-fusion; a template for T03.2 / T03.7.
- [FGA-Corn precision application (Front. Plant Sci. 2025)](https://doi.org/10.3389/fpls.2025.1571228) — small detector → decision rule → stepper actuation; the same pattern fits sorting or targeted dosing demos (T03.1, T03.6).
- [Precast-concrete surface robot (Sensors 2024)](https://doi.org/10.3390/s24113336) — stepper-only 5-axis machine with brake motors for power-off safety; reference for a custom mechanism in construction / infrastructure (T03.4).

→ [All papers of Leadshine Technology](../../Companies/Leadshine/Leadshine-Papers-and-Research.md)

## Magiclab Robotics

**Reading list from the company papers doc:**

- [In-Context Visual Guidance with Magic-Brain](https://embodied.magiclab.top/works/brain/en.html) — a VLM draws the target and the drop zone onto the camera image as coloured masks; pick-and-place success rose from **41% to 84.7%** on MolmoSpaces-Bench. This is the most copyable idea for a **waste-sorting** demo: let a VLM decide "which item, which bin" and keep the low-level policy simple.
- [Magic-W0](https://arxiv.org/abs/2609.39870) — open weights and fine-tuning code for a pick / store / sort policy, if you have a GPU and can collect demos.
- [Dual-Stream Memory](https://arxiv.org/abs/2610.13262) — relevant when sorting needs counting or remembering what was already handled.
- No paper on energy, environmental monitoring or low-power edge AI was found. The two-step denoising result in [Toward Real-Time VLAs](https://arxiv.org/abs/2609.39822) (about 2.8 times faster model inference) is the nearest thing to an efficiency contribution.

→ [All papers of Magiclab Robotics](../../Companies/Magiclab/Magiclab-Papers-and-Research.md)

## Omnicor AI

**Reading list from the company papers doc:**

- [BitVLA](https://arxiv.org/abs/2506.07530) — hard numbers (11x less memory, 4.4x lower latency) for an energy-efficient-inference pitch (T03.3).
- [SmolVLA](https://arxiv.org/abs/2506.01844) — a VLA that runs on CPU / consumer GPU; a small sorting policy is feasible in a weekend (T03.1, T03.3).
- [EdgeVLA](https://arxiv.org/abs/2507.14049) and [TinyVLA](https://arxiv.org/abs/2409.12514) — design choices that cut compute per action (T03.3).
- No paper on waste, water or environmental monitoring is connected to OmniCor.

→ [All papers of Omnicor AI](../../Companies/Omnicor-AI/Omnicor-AI-Papers-and-Research.md)

## Spirit AI

**Reading list from the company papers doc:**

- No paper targets waste sorting, energy or environmental monitoring directly.
- **[Point-VLA](https://arxiv.org/abs/2512.18933)** — cluttered picking and slot placement with pointed targets; maps well onto sorting recyclables into bins.
- **[FP3](https://arxiv.org/abs/2503.08950)** — data-efficient pick-and-place from point clouds (80 demos per new task) if a depth camera is available.
- **[Spirit-v1.5 blog](https://www.spirit-ai.com/en/blog/spirit-v1-5)** + **[RoboChallenge](https://arxiv.org/abs/2510.17950)** — the repo ships a public fine-tuning example for the Table30 task "move objects into box", the closest ready-made analogue to bin sorting.
- **[Legato](https://arxiv.org/abs/2602.12978)** — smoother, faster chunked execution when throughput on a sorting line matters.

→ [All papers of Spirit AI](../../Companies/Spirit-AI/Spirit-AI-Papers-and-Research.md)

## UniX AI

**Reading list from the company papers doc:**

- [Binding Touch to Everything (UniTouch)](https://arxiv.org/abs/2401.18084) — zero-shot material classification with released weights; the fastest route to a "sort by material, not by looks" demo for T03.1 / T03.6 **if you have a GelSight-type sensor**.
- [Touch and Go](https://arxiv.org/abs/2211.12498) — CC BY 4.0 data with material labels; usable to train or sanity-check a small material classifier (also vision-only, from the paired RGB frames).
- [AnyTouch](https://arxiv.org/abs/2502.12191) — third-party successor encoder that covers more sensors; check it before committing to UniTouch.
- [Where to Generate Touch](https://arxiv.org/abs/2611.15834) — only if you plan to augment scarce tactile data synthetically.

→ [All papers of UniX AI](../../Companies/UniX-AI/UniX-AI-Papers-and-Research.md)

## WUJI

**Reading list from the company papers doc:**

No directly relevant paper found (nothing on sorting, disassembly or environmental tasks with WUJI devices). Closest useful reading:
- [pi0](https://arxiv.org/abs/2410.24164) / [pi0.5](https://arxiv.org/abs/2504.16054) with [wuji-openpi](https://github.com/wuji-technology/wuji-openpi) — learn a pick-and-sort skill from teleop demos instead of hand-coding grasps.
- [TACO](https://arxiv.org/abs/2401.08399) and [OAKINK2](https://arxiv.org/abs/2403.19417) — tool-use and multi-step human clips that `toporetarget` can import, for unscrewing or dismantling motions.

→ [All papers of WUJI](../../Companies/WUJI/WUJI-Papers-and-Research.md)

## coprod Inc.

**Reading list from the company papers doc:**

- [Design Principles for Energy-Efficient Legged Locomotion](https://doi.org/10.1109/TMECH.2014.2339013) — the one relevant item: an energy-loss breakdown and regeneration argument for low-ratio drives (T03.3). Pair it with co:power's on-bus voltage / power telemetry to measure and plot energy per motion cycle.

Otherwise: no directly relevant paper found (nothing on waste sorting, recycling, water or environmental monitoring).

→ [All papers of coprod Inc.](../../Companies/coprod/coprod-Papers-and-Research.md)

## OriginFlow

**Reading list from the company papers doc:**

- No directly relevant paper found.
- Nearest material: the [OriginData preview sample](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample) includes phone-repair, circuit-board-assembly and sorting / organising episodes that could seed a repair or sorting skill model (T03.1, T03.6); [UMI](https://arxiv.org/abs/2402.10329) is the standard reference for capturing such skills for robot replay.

→ [All papers of OriginFlow](../../Companies/OriginFlow/OriginFlow-Papers-and-Research.md)
