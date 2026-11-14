---
type: company
company: "Galaxea"
slug: Galaxea
hq: "Beijing, China (some trackers list Suzhou; export entity in Hong Kong)"
founded: 2023
website: https://galaxea-dynamics.com
categories: [mobile-manipulator, arm, humanoid, software, data]
on_site_guess: "R1 Pro / R1 Lite wheeled dual-arm robots, possibly LEMO desktop dual-arm kits with A1Z-T teleop arms, running G0.5"
fit_t01: 4
fit_t02: 2
fit_t03: 3
fit_t04: 4
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# Galaxea

> **One-liner:** Galaxea (Galaxea AI / Galaxea Dynamics, Chinese name Xinghaitu) builds wheeled dual-arm mobile manipulators, low-cost force-controlled arms and its own open VLA foundation models (G0 / G0.5) as one "hardware + intelligence" stack.
> **Why it matters at Leukerbad:** It is the vendor with the shortest path from "teleoperate a task a few dozen times" to "robot does it autonomously": the R1 robots are a direct fine-tuning target of the public G0.5 checkpoints. Strong for indoor fetch / tidy / hand-over tasks (T01, T04); wheeled base only, so not for snow, stairs or steep terrain.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Beijing, China (press releases datelined Beijing; some databases list Suzhou — ⚠️ unverified which is the legal seat). International store operated by GALAXEA HK LIMITED, Hong Kong |
| Founded | **September 2023** |
| Founders / CEO | Founder and CEO **Jiyang Gao** (Tsinghua, USC PhD, ex-Waymo / Momenta). Co-founders reported as Hang Zhao, Huazhe Xu, Tianwei Li (⚠️ sources differ on the exact group) |
| Size and funding | Headcount not public. Series B about **CNY 1 bn** (Feb 2026); Series B+ about **CNY 2 bn / USD 291 M** (Apr 2026); valuation reported above **CNY 20 bn (about USD 2.9 bn)** |
| Core business | Robot hardware ("Galaxea Dynamics") plus embodied foundation models ("Galaxea Model"); sells to research labs, developers and industrial pilots |
| Website | https://galaxea-dynamics.com (store, USD prices) |
| Docs / developer portal | https://docs.galaxea-dynamics.com/home/en/ (LEMO, R1 Pro, R1 Lite, A1Z; latest SDK listed **V2.5.0**). Legacy guide for R1 / A1: https://userguide-galaxea.github.io/Product_User_Guide/ |
| GitHub | Models and tools: https://github.com/OpenGalaxea · Product docs / SDK: https://github.com/userguide-galaxea · Weights and data: https://huggingface.co/OpenGalaxea |

## Portfolio at a glance

| Product | Type | Status | Key specs | Price | Img key |
|---|---|---|---|---|---|
| R1 Pro | Wheeled dual-arm mobile manipulator ("wheeled humanoid") | ✅ | **26 DoF** (2 x 7-DoF arms, 3-DoF torso, 6-DoF omni chassis); **5 kg per arm**; 170 cm, 96 kg; **1.5 m/s**; about 7 h runtime; 7 cameras + 1 LiDAR; ROS 2 + Galaxea SDK. Hardware numbers from EU reseller listing ⚠️ unverified against official docs | R1 Series "from **USD 39,999**" (official); R1 Pro about USD 69,999 on third-party listings ⚠️ unverified | galaxea-r1-pro |
| R1 Lite | Lighter wheeled dual-arm mobile manipulator | ✅ | Dual 6-DoF arms with grippers, upgraded navigation, "high-compute" on-board platform (official docs, no numbers); 23 DoF ⚠️ unverified (aggregator) | Believed to be the USD 39,999 entry model ⚠️ unverified | galaxea-r1-lite |
| R1 (original) | Wheeled dual-arm mobile manipulator | ✅ legacy (not in the current docs portal) | **24 DoF** (6 chassis, 4 torso, 14 arms + grippers); **5 kg at 0.5 m**; arm reach 70 cm; working height 0–200 cm; 8 cameras, 360° LiDAR; up to 550 TOPS compute | not public | galaxea-r1 |
| Nexo | New-generation wheeled dual-arm robot | 🧪 unveiled Aug 2026 (WRC) | **30 DoF**; **20 kg dual-arm payload**; **8 h** runtime; coordinated force / position control | not public | galaxea-nexo |
| Kengo | Bipedal general-purpose humanoid | 🧪 listed in store | Specs not public; shown doing parkour training at WRC 2026 | USD 999,999 (store listing; reads as a placeholder / contact-sales price) | galaxea-kengo |
| LEMO | Desktop dual-arm development platform (2 x A1Z + grippers + 3 fisheye cameras + CCU controller) | ✅ shipping since 9 Nov 2026 | **5 kg peak payload per arm**; **±0.1 mm** repeatability; 3 synchronized camera views; teleop latency under 50 ms with A1Z-T; VR teleop (PICO / Meta); LEMO Studio for collect-train-deploy | from **USD 7,699** (up to about 11,049 by configuration) | galaxea-lemo |
| LEMO A1Z | Lightweight force-controlled desktop arm, open low-level stack | ✅ | 6-DoF (official title; the LEMO launch post also says 7 — ⚠️ inconsistent); 5 kg peak payload; ±0.1 mm | from **USD 2,999** | galaxea-a1z |
| A1Z-T | Leader arm for master-slave teleoperation | ✅ | Same kinematics as A1Z; under 50 ms latency | USD 1,499 (A1Z version) / 2,999 (LEMO version) | galaxea-a1z-t |
| A1 / A1X / A1Y | Earlier 6-DoF lightweight arms (A1X is the R1 Lite arm) | ✅ via resellers; no longer in the official store ⚠️ unverified | A1X: 6-DoF, about 4.2 kg, 3 kg rated / 5 kg max ⚠️ unverified (reseller data) | about USD 3,000–4,000 at resellers ⚠️ unverified | galaxea-a1x |
| G1Z gripper | Parallel gripper for A1Z / LEMO | ✅ | 1-DoF | USD 499 | galaxea-g1z |
| G0.5 (and legacy G0 Plus / G0 Tiny) | Vision-language-action foundation model | ✅ open weights, **non-commercial licence** | Single-weights VLA with action chain-of-thought; checkpoints about 11 GB; inference needs **more than 8 GB VRAM** (RTX 4090 recommended); full fine-tune more than 70 GB VRAM; targets R1 Lite, R1 Pro, SO-100/101, Franka (DROID). G0 Tiny (250 M) runs on the R1 Pro's Orin | free (non-commercial) | galaxea-g05 |
| Galaxea Open-World Dataset | Real-world mobile-manipulation dataset | ✅ | **500+ h**, 150+ tasks, 50 scenes, one embodiment (R1 Lite), subtask language labels; RLDS and LeRobot formats; CC BY-NC-SA 4.0 ⚠️ licence unverified | free | galaxea-open-world-dataset |

Also published as research: **Fast-WAM** (world action model, 🧪) and **GalaxeaDP** (diffusion-policy baseline, ✅ code).

## What they will most likely bring to the hackathon

**Best guess (not confirmed by the organisers):**

- **R1 Pro and/or R1 Lite** — most likely. They are the company's standard research and EDU platforms, the ones documented in the developer portal, and the direct zero-shot / fine-tune targets of G0.5. The event one-liner also lists the R1 family.
- **LEMO desktop dual-arm kit with A1Z-T leader arms** — plausible. Launched 9 Nov 2026 with a free-shipping promotion running through the hackathon dates; it is cheap, travels in a flight case and is built for exactly the "collect demos, train, deploy" loop.
- **Nexo** — possible as a showpiece, unlikely as a hackable platform (unveiled Aug 2026, no public docs).
- **Kengo biped** — unlikely.
- Expect a **VR headset or leader-arm teleop rig** and a GPU workstation for G0.5 inference to come with the robots. Ask the booth on arrival: which model, how many units, is fine-tuning compute provided.

## Developer platform (summary)

- **Middleware:** ROS 2 plus the "Galaxea SDK" on R1 Pro (official docs); SDK changelog at V2.5.0. The original R1 / A1 guides are ROS-based. Exact ROS distro per robot ⚠️ unverified — check the robot's docs page on site.
- **Control levels:** joint-space and whole-body-control interfaces on R1 Pro (both are exposed as G0.5 deployment variants); chassis, torso and arm topics; A1Z advertises an open low-level stack.
- **Languages:** Python throughout the model, data and deployment repos; ROS 2 nodes for robot I/O.
- **Teleoperation and data collection:** leader-follower arms (A1Z-T), VR (PICO / Meta) on LEMO, tabletop teleop guide for older arms. Recordings are rosbag / MCAP and convert to LeRobot format with **GalaxeaLeRobotToolkit**.
- **Pretrained models:** **G0.5** (`g05-base` for R1 Lite / R1 Pro, plus SO-101, DROID, LIBERO, RoboTwin checkpoints), legacy **G0 Plus 3B** (incl. a pick-and-place checkpoint) and **G0 Tiny 250M** for on-board Orin. Fine-tune with `scripts/run/finetune.sh` in **GalaxeaVLA**. Licence is **non-commercial** — fine for a hackathon, not for a product.
- **Deployment:** **EFMNode** is the on-robot node that runs a policy against the ROS interfaces.
- **Simulation:** **GalaxeaManipSim** (manipulation tasks with Galaxea robots), Isaac Sim / Isaac Lab tutorials for A1 and R1 in the legacy guide, a BEHAVIOR-1K fork, plus LIBERO and RoboTwin 2.0 evaluation.
- **On-board compute:** NVIDIA Orin on R1 Pro (per the model repo); original R1 lists up to 550 TOPS. Large VLA inference is normally done on an off-board RTX-class GPU.
- **48-hour reality check:** full G0.5 fine-tuning needs an 80 GB-class GPU. Without that, use zero-shot G0.5, the pick-and-place checkpoint, or a small diffusion / ACT policy (GalaxeaDP, LeRobot) trained on 30–100 teleop demos.
- **Links:** [Docs](https://docs.galaxea-dynamics.com/home/en/) · [GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA) · [OpenGalaxea org](https://github.com/OpenGalaxea) · [G0.5 project page](https://opengalaxea.github.io/G05/)

## Current projects, deployments and customers

- **2026-11-09** — LEMO desktop dual-arm platform goes on sale worldwide at USD 7,699. ([Galaxea blog](https://galaxea-dynamics.com/blogs/robotics-insights-news/two-arms-one-platform-galaxea-launches-lemo))
- **2026-08-23/24** — World Robot Conference, Beijing: 10+ demos. Closed-loop **dark-store fulfilment** taking live orders (900 full orders, 1,775 picks, 1,560 packing cycles during the show), **robot-on-robot assembly** (claimed 30%+ faster than manual teaching), **carton folding** (4,000 cycles per day), industrial part sorting, biped parkour. All figures self-reported. ([PR Newswire](https://en.prnasia.com/story/545003-0.shtml), [Galaxea blog](https://galaxea-dynamics.com/blogs/robotics-insights-news/wrc-2026-embodied-ai-robotics))
- **2026-08** — Company states "nearly 100" clients, naming **Stanford University, Physical Intelligence and Huawei**. No deployment sites or shipment volumes disclosed. ([PR Newswire](https://en.prnasia.com/story/545003-0.shtml))
- **2026-06-01 to 2026-08-12** — G0.5 announced, weights released 16 June, R1 Pro zero-shot entrypoint 11 July, paper 12 Aug. Reported results: 82.5% average zero-shot success on 10 DROID tabletop tasks and top score on BEHAVIOR-1K (self-reported). ([Galaxea blog](https://galaxea-dynamics.com/blogs/developer-hub/galaxea-g05-a-new-generation-embodied-foundation-model-for-robotics), [GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA))
- **2026-01 / 2026-02** — G0 Plus (3B) and G0 Tiny (250M, edge) released; a garment-folding G0 variant is also reported. ([GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA), [Gasgoo](https://autonews.gasgoo.com/articles/news/3-billion-yuan-raised-in-two-months-valuation-breaks-20-billion-yuan-what-is-galaxeas-edge-2040321874859307009))
- **2025-03** — Stanford's open-source household robotics work (BEHAVIOR Robot Suite) is built on the Galaxea R1: whole-body teleop and learning of everyday home tasks. Most relevant public reference for T04. ([Galaxea blog](https://galaxea-dynamics.com/blogs/robotics-applications/stanford-galaxea-brs-household-robotics))
- **Track relevance:** public demos are logistics, retail fulfilment, manufacturing and household research. **No public elderly-care, clinical, emergency-response or outdoor deployments found. No Europe- or Switzerland-specific activity found** beyond EU resellers.

## Roadmap and future direction

- **2026-08** — "**1+3+N**" strategy: one integrated hardware + intelligence stack; three product families (**Kengo** biped, **Nexo** wheeled, **LEMO** developer); N industries via partner programmes. Target sectors named: manufacturing, consumer electronics, parcel and warehouse logistics, e-commerce / retail, commercial services. ([PR Newswire](https://en.prnasia.com/story/545003-0.shtml))
- **2026-08** — Nexo announced; price and ship date not public. 🧪
- **2026-04** — Series B+ of about USD 291 M (nearly 20 investors, including hardware partner Lens Technology and state-backed funds), earmarked for scaling production; company said it would start several industry pilots globally in H1 2026. ([Caixin Global](https://www.caixinglobal.com/2026-04-02/robot-startup-galaxea-ai-raises-291-million-102430297.html), [Gasgoo](https://autonews.gasgoo.com/articles/news/3-billion-yuan-raised-in-two-months-valuation-breaks-20-billion-yuan-what-is-galaxeas-edge-2040321874859307009))
- **2026-06** — CEO publicly argues China could lead robotics foundation models within about three years; models remain the strategic centre. ([Caixin Global](https://www.caixinglobal.com/2026-06-17/galaxea-ai-chief-says-china-could-lead-robotics-models-within-three-years-102454837.html))
- **Model licensing trend:** Apache-2.0 (2025) to non-commercial community licences (since Jan 2026) — commercial use needs a separate agreement.
- **Developer funnel:** Education Discount and "Galaxea for Startups" programmes on the official store. IPO plans: not public.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 4 | Proven indoor pick / pack / deliver demos and a VLA that fine-tunes on teleop data; limited to flat indoor floors | R1 Pro, R1 Lite, G0.5 | [T01 brief](T01-Autonomous-Urban-Services/Galaxea-T01-1-Brief.md) |
| T02 Resilient & Safe City | 2 | No rough-terrain mobility or hazard-response record; useful only for indoor inspection or valve / switch manipulation alongside a quadruped | R1 Pro (manipulation), LEMO as a teleop station | [T02 brief](T02-Resilient-and-Safe-City/Galaxea-T02-1-Brief.md) |
| T03 Sustainable City | 3 | Dual-arm sorting of waste / recyclables or linen is a realistic learned-policy demo; no domain deployments | LEMO, R1 Lite, G0.5 pick-and-place checkpoint | [T03 brief](T03-Sustainable-City/Galaxea-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 4 | Household-task research pedigree (Stanford BRS), 0–2 m reach, fetch / hand-over / tidy / laundry tasks; not a medical device and no care deployments | R1 Pro, R1 Lite, G0.5 | [T04 brief](T04-Elderly-Care-and-Rehabilitation/Galaxea-T04-1-Brief.md) |

## Related docs
- [Product portfolio](Galaxea-Products.md) · [Developer guide](Galaxea-Developer-Guide.md) · [Roadmap and strategy](Galaxea-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [Galaxea Dynamics official site and store](https://galaxea-dynamics.com)
- [Galaxea — About us](https://galaxea-dynamics.com/pages/about-us)
- [Galaxea documentation centre](https://docs.galaxea-dynamics.com/home/en/)
- [Galaxea blog — LEMO launch (9 Nov 2026)](https://galaxea-dynamics.com/blogs/robotics-insights-news/two-arms-one-platform-galaxea-launches-lemo)
- [Galaxea blog — WRC 2026](https://galaxea-dynamics.com/blogs/robotics-insights-news/wrc-2026-embodied-ai-robotics)
- [Galaxea blog — G0.5](https://galaxea-dynamics.com/blogs/developer-hub/galaxea-g05-a-new-generation-embodied-foundation-model-for-robotics)
- [Galaxea blog — Stanford x Galaxea household robotics](https://galaxea-dynamics.com/blogs/robotics-applications/stanford-galaxea-brs-household-robotics)
- [PR Newswire — Galaxea AI at WRC 2026 (24 Aug 2026)](https://en.prnasia.com/story/545003-0.shtml)
- [GitHub — OpenGalaxea organisation](https://github.com/OpenGalaxea)
- [GitHub — OpenGalaxea/GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA)
- [G0.5 project page](https://opengalaxea.github.io/G05/)
- [Hugging Face — Galaxea Open-World Dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset)
- [arXiv 2509.00576 — Galaxea Open-World Dataset and G0 dual-system VLA](https://arxiv.org/html/2509.00576v1)
- [Galaxea legacy user guide — R1](https://userguide-galaxea.github.io/Product_User_Guide/Introducing_Galaxea_Robot/product_info/R1)
- [RBTX reseller listing — R1 Pro](https://rbtx.de/en-GB/components/humanoid/galaxea-r1-pro-humanoid-robot-26-dof)
- [Caixin Global — Galaxea AI raises USD 291 M (2 Apr 2026)](https://www.caixinglobal.com/2026-04-02/robot-startup-galaxea-ai-raises-291-million-102430297.html)
- [Caixin Global — Galaxea AI chief on robotics models (17 Jun 2026)](https://www.caixinglobal.com/2026-06-17/galaxea-ai-chief-says-china-could-lead-robotics-models-within-three-years-102454837.html)
- [Gasgoo — CNY 3 bn raised in two months](https://autonews.gasgoo.com/articles/news/3-billion-yuan-raised-in-two-months-valuation-breaks-20-billion-yuan-what-is-galaxeas-edge-2040321874859307009)
- [aiwiki — Galaxea R1 Lite (aggregator, used only for values marked unverified)](https://aiwiki.ai/wiki/galaxea_dynamics_r1_lite)
