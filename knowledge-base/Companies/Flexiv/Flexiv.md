---
type: company
company: "Flexiv Robotics"
slug: Flexiv
hq: "Santa Clara, California, USA (large operations in Shanghai, China)"
founded: 2016
website: https://www.flexiv.com
categories: [arm, mobile-manipulator, software]
on_site_guess: "Rizon 4 / 4s force-controlled 7-DoF arms with Grav gripper, possibly an Enlight L arm or a Mello massage demo"
fit_t01: 3
fit_t02: 2
fit_t03: 3
fit_t04: 4
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# Flexiv Robotics

> **One-liner:** Maker of 7-axis "adaptive" robot arms whose selling point is very fine whole-arm force control (down to **0.03 N**), plus grippers, a parallel robot, an AMR and dual-arm platforms built on those arms.
> **Why it matters at Leukerbad:** If your idea involves *touching* something safely and precisely — a human body, a fragile object, a plug, a surface — this is the strongest force-control hardware on site, with an open C++/Python SDK at **1 kHz**. Flexiv already sells a robot massage system (Mello), which maps directly onto a spa and rehabilitation town.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Santa Clara, California, USA (press-release dateline); offices in Silicon Valley, Shanghai, Beijing, **Munich** and Singapore |
| Founded | 2016 |
| Founders / CEO | Shiquan Wang, co-founder and CEO (Stanford background ⚠️ unverified in this pass) |
| Size and funding | Headcount not public. Series C about **USD 100M** (June 2025, about USD 1B valuation per trade press ⚠️ unverified); further round led by Invus on **2026-03-18**, amount not disclosed. Total raised: sources conflict (about USD 220M–320M) |
| Core business | Force-controlled industrial arms and turnkey cells for contact-rich work: polishing/sanding, insertion and assembly, CNC tending, lab automation, massage |
| Website | https://www.flexiv.com |
| Docs / developer portal | RDK manual: https://www.flexiv.com/software/rdk/manual/v2.x/index.html (also served at rdk.flexiv.com) |
| GitHub | https://github.com/flexivrobotics (27 public repos, actively updated in Nov 2026) |

## Portfolio at a glance

| Product | Type | Status | Key specs | Price | Img key |
|---|---|---|---|---|---|
| Rizon 4 | 7-DoF force-controlled arm | ✅ | **4 kg** payload · **876 mm** reach · 20 kg · force sensing **0.1 N** · max TCP force 200 N · ±0.05 mm · IP65 | not public | flexiv-rizon-4 |
| Rizon 4s (Rizon 4 + wrist F/T sensor) | 7-DoF arm, high-sensitivity | ✅ | 4 kg · 919 mm · 21 kg · force sensing **0.03 N** · max TCP force 150 N · IP65 | not public | flexiv-rizon-4s |
| Rizon 10 | 7-DoF force-controlled arm | ✅ | **10 kg** payload · 941 mm · 38 kg · force sensing 0.2 N · max TCP force 350 N · IP65 | not public | flexiv-rizon-10 |
| Rizon 10s (Rizon 10 + wrist F/T sensor) | 7-DoF arm, high-sensitivity | ✅ | 10 kg · 984 mm · 39 kg · force sensing 0.1 N · max TCP force 350 N · IP65 | not public | flexiv-rizon-10s |
| Enlight L | Next-gen compact 7-DoF arm (launched 2026) | ✅ launched June 2026; delivery status ⚠️ unverified | **5 kg** payload · **752 mm** reach · **15 kg** · force sensing 0.1 N · controllable force up to 400 N · whole-body touch sensing · four joints with 720° rotation · IP65 | not public | flexiv-enlight-l |
| Mico (Armor / Core / Plus / Ultra) | Dual-arm platform built from two Enlight arms | ✅ launched June 2026; delivery status ⚠️ unverified | 2×7 DoF · 2×5 kg · 752 mm reach per arm · 53–79 kg · RDK 1 kHz real-time control (Ultra specs not public) | not public | flexiv-mico |
| AICO (1, 2-4, 2-10) | Mobile single / dual-arm platform on Rizon arms, aimed at embodied-AI work | ✅ listed on site | AICO 1: 1×7 DoF, 4 kg, 4 h battery · AICO 2-4: 2×4 kg, 6 h · AICO 2-10: 2×10 kg, 4 h · laser SLAM · 185–395 kg | not public | flexiv-aico |
| FMR 300 | Autonomous mobile robot (AMR) | ✅ (launched Dec 2025) | payload **272 kg** · footprint 78.7 × 60.9 cm · laser SLAM · differential drive · 72 Ah battery, up to 8 h · auto-docking | not public | flexiv-fmr-300 |
| Mobile Manipulator | FMR 300 base + Rizon arm | ✅ listed on site | Arm uses force sensing to cancel AMR docking error (no vision needed); detailed specs not public | not public | flexiv-mobile-manipulator |
| Mello | Robotic massage system | 🧪 release slated Q4 2026 | 7 DoF · force sensing 0.1 N · **1000 Hz** force control · max output force 200 N · standardized 15-minute massage · 500 W | not public | flexiv-mello |
| Moonlight | 3-DoF force-controlled parallel (delta-style) robot | ✅ | working diameter 1200 mm · height 400 mm · 38 kg · 1.5 m/s · ±0.05 mm · IP65 (payload not stated on product page) | not public | flexiv-moonlight |
| Grav | 2-finger force-controlled gripper | ✅ | stroke 0–100 mm · grip force 1–100 N · force accuracy 1 N · 0.9 kg · IP67 | not public | flexiv-grav |
| Grav Enhanced | Gripper with parallel + V-mode and gecko-inspired adhesive pads | ✅ | stroke 0–100 mm / 120–160° · grip force 1–45 N · objects up to 5 kg · 1.3 kg · IP65 | not public | flexiv-grav-enhanced |
| Flexiv Elements / Elements Studio | Teach-pendant and desktop programming software | ✅ | Graphical programming with force-control primitives; Studio also drives simulated robots. Details ⚠️ unverified in this pass | not public | flexiv-elements |
| RDK / DRDK / TDK / PDK / AMR SDK / Trainer | Developer software | ✅ | See developer section | free (Apache-2.0 repos); robot-side RDK license required | flexiv-rdk |

Notes: controllers are the **Hesper** (Rizon: 12 kg, 500 W, 16 DI / 16 DO, Profinet, Modbus TCP) and the newer **Orion** control hub (10.5 kg, multi-robot, SIL 2) shown on the Enlight page. A "Noema" AI system from the starting notes could **not** be confirmed on current official pages ⚠️ unverified.

## What they will most likely bring to the hackathon

**Best guess (not confirmed by the organisers):**

- **Rizon 4 or Rizon 4s with a Grav gripper** — most likely. It is the model used in every public developer workflow (RDK examples, ROS 2, the NVIDIA Isaac reference workflow, Flexiv Trainer) and is light enough (20 kg + 12 kg controller) to ship to a mountain venue.
- **Enlight L** — plausible. It is the 2026 flagship, only 15 kg, and Flexiv has been pushing it at every 2026 show (ICRA, Automate, IROS).
- **Mello massage demo** — plausible given the elderly-care track and the European preview at Hannover Messe 2026, but it is a finished product, less hackable than a bare arm.
- **Less likely:** Mico / AICO dual-arm platforms and FMR 300 (heavy, 53–395 kg), Moonlight (industrial pick-and-place).
- **Ask at the booth first:** is the robot's **RDK license** activated, which RDK version is installed, is a real-time Ubuntu laptop provided, and which end-effector is mounted.

## Developer platform (summary)

- **Flexiv RDK** — C++ and Python; Linux, macOS, Windows, QNX. Gives both **low-level real-time control (1 kHz streaming)** and high-level non-real-time control (run built-in plans and primitives). Requires a license on the robot and "Remote mode" enabled; connection is by wired LAN.
- **Real-time caveat:** true 1 kHz torque / Cartesian streaming needs a real-time Linux kernel (Ubuntu 22.04 / 24.04). For a 48-hour build, Python + non-real-time primitives (move, contact, force-hold) is the fast path.
- **ROS 2** — `flexiv_ros2` (Humble and Jazzy branches) with ros2_control, MoveIt integration and demos; URDFs in `flexiv_description`. Includes a mock-hardware mode for RViz testing without a robot.
- **Simulation** — `isaac_sim_ws` / Flexiv-Isaac Bridge puts Flexiv robots in NVIDIA Isaac Sim driven by the same force controller as the real arm. Since Sept 2026 Rizon 4 is a supported robot in NVIDIA Isaac (Isaac Lab training, Isaac ROS deployment, FoundationPose, cuMotion); the first reference workflow is RL-trained cable insertion with Rizon 4 + Grav.
- **Teleoperation and data collection** — `flexiv_tdk` (leader-follower teleop with force feedback, C++/Python) and **Flexiv Trainer**: a local web UI to record teleop demos as **LeRobot**-format episodes (RealSense / Orbbec cameras, up to 3 cameras single-arm, 5 dual-arm), then train policies (B-Spline Diffusion named; plugin policy families).
- **Other kits** — `flexiv_drdk` (dual-arm, Linux), `flexiv_pdk` + Composer Studio (motion and scan-path planning), `flexiv_amr_sdk` (FMR base).
- **Pretrained foundation model** — none publicly released by Flexiv as of this pass; bring your own policy (LeRobot-compatible) or use classical force-control primitives.
- **On-board compute** — the controller runs the control stack; your AI runs on an external PC / GPU connected over Ethernet. No user-accessible GPU in the arm ⚠️ unverified.
- **Links** — manual: https://www.flexiv.com/software/rdk/manual/v2.x/index.html · code: https://github.com/flexivrobotics/flexiv_rdk · ROS 2: https://github.com/flexivrobotics/flexiv_ros2 · trainer: https://github.com/flexivrobotics/flexiv_trainer

## Current projects, deployments and customers

- **2026-11 (blog):** Flexiv highlights NVIDIA research on GB300 server assembly using two Rizon 4s arms alongside a conventional cobot. [flexiv.com](https://www.flexiv.com)
- **2026-09-24:** Rizon 4 supported in NVIDIA Isaac; contact-rich insertion reference workflow (DisplayPort cable, Rizon 4 + Grav). [Robotics 24/7](https://www.robotics247.com/article/flexix-rizon-4-adaptive-robot-now-supported-in-nvidia-isaac/Flexiv_Robotics)
- **2026-09 (approx.):** Force-control demos and keynote at IROS 2026, Pittsburgh. [flexiv.com](https://www.flexiv.com)
- **2026-07:** First entry into India at Automation India Expo 2026. [flexiv.com](https://www.flexiv.com)
- **2026-06:** Enlight arm and Mico dual-arm platform launched internationally at Automate 2026, Chicago. [Robotics & Automation News](https://roboticsandautomationnews.com/2026/06/26/flexiv-launches-new-adaptive-robots-for-industrial-automation/102857/)
- **2026-04:** Hannover Messe booth: Mello massage platform (first European showing), ball balancing, mobile CNC tool changing, server component insertion, car-body polishing, car-seat ironing and testing. [Robotics 24/7](https://www.robotics247.com/article/hannover-messe-2026-flexiv-showcases-the-future-of-adaptive-robotics)
- **2025-12:** FMR 300 AMR launched for lab automation, CNC tending and mobile polishing stations. [Automated Warehouse](https://www.automatedwarehouseonline.com/flexiv-launches-its-first-self-developed-amr/)
- **Earlier, from search summaries (⚠️ not re-verified at source):** EsVata window-shutter sanding with Rizon 4 (2024); Cardinal Machine (Michigan) as integrator; KURABO "KURAVIZON" partnership (Japan); Rizon 4 robotic masseur.
- **Starting-note claims not confirmed in this pass:** EV charging, agriculture and physiotherapy-clinic deployments ⚠️ unverified. No Swiss customer or partner found.

## Roadmap and future direction

- **2026-03-18:** Invus-led financing (amount undisclosed) earmarked for R&D and global sales / service build-out, with stated expansion in **Europe and Asia**. Munich is the European office.
- **2026 product shift:** from single arms to platforms — Enlight (whole-body touch sensing), Mico and AICO dual-arm systems, FMR 300 mobile base. No legged humanoid announced.
- **Mello:** 🧪 commercial release slated **Q4 2026** (retail massage, not a medical device per public material).
- **Physical AI:** strategy is to pair force control with learned policies — NVIDIA Isaac integration, open teleop + LeRobot data pipeline (Flexiv Trainer). An in-house foundation model is not public.
- **Mico Ultra:** 🔭 listed by name only, no specs.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 3 | Arms are stationary; useful as the manipulation half (plug-in, handover, button / door contact) of a mobile system, or on the FMR 300 base if present | Rizon 4 / 4s, Grav, Mobile Manipulator | [T01 brief](T01-Autonomous-Urban-Services/Flexiv-T01-1-Brief.md) |
| T02 Resilient & Safe City | 2 | No outdoor or rough-terrain mobility; supporting role for contact tasks (valve turning, inspection by touch, connector mating) | Rizon 4s, Rizon 10 | [T02 brief](T02-Resilient-and-Safe-City/Flexiv-T02-1-Brief.md) |
| T03 Sustainable City | 3 | Force-controlled sorting, disassembly, refurbishing or surface finishing is a credible 48-hour arm demo; needs your own perception | Rizon 4 / 10, Grav Enhanced, Moonlight | [T03 brief](T03-Sustainable-City/Flexiv-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 4 | Safe, finely controlled body contact is the core competence; massage is a shipping-soon product (Mello); assisted-movement or therapy demos are a short path | Rizon 4s, Enlight L, Mello | [T04 brief](T04-Elderly-Care-and-Rehabilitation/Flexiv-T04-1-Brief.md) |

## Related docs
- [Product portfolio](Flexiv-Products.md) · [Developer guide](Flexiv-Developer-Guide.md) · [Roadmap and strategy](Flexiv-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [Flexiv — official site (home, news list)](https://www.flexiv.com)
- [Flexiv — Rizon product page](https://www.flexiv.com/product/rizon)
- [Flexiv — Enlight product page](https://www.flexiv.com/product/enlight)
- [Flexiv — Moonlight product page](https://www.flexiv.com/product/moonlight)
- [Flexiv — Grav product page](https://www.flexiv.com/product/grav)
- [Flexiv — Robot Station / System page (Mico, AICO, Mello, Mobile Manipulator)](https://www.flexiv.com/product/robot-system)
- [Flexiv — "Flexiv Secures Capital from Leading Evergreen Investor" (2026-03-18)](https://www.flexiv.com/news/Flexiv_Secures_Capital_from_Leading_Evergreen_Investor)
- [Flexiv RDK manual v2.x](https://www.flexiv.com/software/rdk/manual/v2.x/index.html)
- [GitHub — flexivrobotics organisation](https://github.com/flexivrobotics)
- [GitHub — flexiv_rdk](https://github.com/flexivrobotics/flexiv_rdk/)
- [GitHub — flexiv_trainer](https://github.com/flexivrobotics/flexiv_trainer)
- [Robotics & Automation News — Flexiv launches new adaptive robots (2026-06-26)](https://roboticsandautomationnews.com/2026/06/26/flexiv-launches-new-adaptive-robots-for-industrial-automation/102857/)
- [Robotics 24/7 — Hannover Messe 2026: Flexiv showcases the future of adaptive robotics](https://www.robotics247.com/article/hannover-messe-2026-flexiv-showcases-the-future-of-adaptive-robotics)
- [Robotics 24/7 — Flexiv Rizon 4 now supported in NVIDIA Isaac (2026-09-24)](https://www.robotics247.com/article/flexix-rizon-4-adaptive-robot-now-supported-in-nvidia-isaac/Flexiv_Robotics)
- [Automated Warehouse — Flexiv launches its first self-developed AMR (2025-12-04)](https://www.automatedwarehouseonline.com/flexiv-launches-its-first-self-developed-amr/)
- [The Robot Report — Flexiv raises more than $100M for adaptive robots (search summary only)](https://www.therobotreport.com/flexiv-raises-more-than-100m-for-adaptive-robots/)
- [Robotics 24/7 — Flexiv deploys Rizon 4 for sanding window shutters (search summary only)](https://www.robotics247.com/article/flexiv_deploys_rizon_4_for_sanding_window_shutters/Flexiv_Robotics)
