---
type: company
company: "Genisom AI"
slug: Genisom-AI
hq: "Beijing, China"
founded: 2023
website: https://www.genisomai.com/en/
categories: [quadruped, humanoid, components, software]
on_site_guess: "L1 / L1 EDU small quadrupeds (possibly L1-W or L2), plus the open MATRiX simulator and RoamerX navigation stack"
fit_t01: 4
fit_t02: 5
fit_t03: 3
fit_t04: 2
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# Genisom AI

> **One-liner:** Beijing-based embodied-AI company (Chinese name 智身科技, GitHub org `zsibot`) that mass-produces rugged small and mid-size quadruped robots, builds its own joint modules, and publishes an open simulation and navigation stack.
> **Why it matters at Leukerbad:** Its robot dogs are built for outdoor patrol, inspection and emergency work (IP54 to IP67, slopes of 40–45°, M1 rated to −20 °C), which matches steep, snowy alpine terrain. The SDK, ROS 2 navigation stack and simulator are public on GitHub, so a team can start coding before touching the hardware.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Beijing (Haidian District), China; own factory in Suzhou, Jiangsu |
| Founded | **December 2023** (company timeline) |
| Founders / CEO | Not public in the sources used |
| Size and funding | **15,000+ robots produced** as of H1 2026 (company-stated, not audited) · 500+ ecosystem partners (company-stated) · Series B of "hundreds of millions of RMB" led by Stone Venture (UAE), per the company's October 2026 press release · headcount not public |
| Core business | Quadruped robots (L and M series, explosion-proof SP1), CHAMP joint modules and wheel-hub motors, a humanoid (NE01, coming soon), simulation / navigation / agent software, education programs |
| Website | [genisomai.com/en](https://www.genisomai.com/en/) |
| Docs / developer portal | [Official Open Source page](https://www.genisomai.com/en/opensource) · [Download Center](https://www.genisomai.com/en/download.html) · docs folders inside each SDK repo (English and Chinese) |
| GitHub | [github.com/zsibot](https://github.com/zsibot/) (10 public repos) |

## Portfolio at a glance

All specs are company-stated laboratory figures from the official product pages unless noted. Prices are not published officially (resellers such as Maverick Drone list L1 and M1, prices not checked).

| Product | Type | Status | Key specs | Price | Img key |
|---|---|---|---|---|---|
| Genisom L1 | Small industry-grade quadruped | ✅ | **8 kg** continuous walking payload · **40°** slope · 16 cm continuous stairs · **IP54** · 0–40 °C · 12 joints at 48 N·m peak · 7 open hardware interfaces + full SDK | not public | genisom-ai-l1 |
| Genisom L1 EDU | L1 research / development configuration | ✅ | NVIDIA Jetson **Orin NX (up to 100 TOPS)** · built-in 3D LiDAR (Livox Mid-360 per trade press) · depth camera · GNSS · 5G | not public | genisom-ai-l1-edu |
| Genisom L1-W | Small wheel-legged quadruped | ✅ | **10 kg** continuous payload · **>5.5 m/s** sprint · 65 cm max obstacle · 40° slope · IP54 · noise as low as 55 dB | not public | genisom-ai-l1-w |
| Genisom L1 Maker | Assemble-it-yourself educational quadruped (L1 platform) | 🧪 (debuted IROS 2026; availability date not public) | 12 DoF · 8 kg payload · 40° slope · component-level assembly, ≥30 assembly cycles · production calibration software · open APIs | not public | genisom-ai-l1-maker |
| Genisom L2 | Compact industrial quadruped with built-in navigation | ✅ ⚠️ unverified shipping date (launched WAIC, July 2026) | **16 kg** continuous payload (150 kg static) · **756 Wh**, about **5.5 h / 20 km** · **IP66** · −20 to 55 °C · **86 TOPS** on-board AI compute · 70 cm obstacle · 95 N·m peak joint torque · 720° sensor suite (stereo + 4 fisheye + LiDAR) · GLUE UWB + vision following | not public | genisom-ai-l2 |
| Genisom M1 (variants M1 Pro, M1 Ultra) | Mid-size industrial quadruped | ✅ | about **30 kg** body, about **30 kg** continuous payload · **45°** slope · 25 cm continuous stairs · 80 cm obstacle · **IP67** · **−20 to 55 °C** · dual hot-swap batteries, up to 5 h / 29 km no load · 15 open hardware interfaces · Pro: voice + UWB following · Ultra: 720° perception | not public | genisom-ai-m1 |
| Genisom SP1 | Explosion-proof wheel-legged quadruped | 🧪 (unveiled WAIC, July 2026) | Explosion-proof design for Zone 1 / Zone 2 gas environments · **50 kg** continuous payload · 35° slope · crawl, wheel and leg modes · visual, infrared, gas and acoustic payloads | not public | genisom-ai-sp1 |
| Genisom NE01 | Humanoid robot | 🧪 ("Coming soon" on official site; shown at WAIC and WRC 2026) | Specs not public | not public | genisom-ai-ne01 |
| TA01 robotic arm | Arm mounted on M1 for mobile manipulation | 🧪 (demoed at WRC 2026; no product page found) | Specs not public | not public | genisom-ai-ta01 |
| CHAMP joint modules (P55, P65, P65MAX-S, P85MAX-S) and wheel-hub motors (W150-S, W190-S) | Integrated actuators | ✅ | P85MAX-S: **180 N·m** peak torque, 86 mm diameter (used in M1) · other models: see product pages | not public | genisom-ai-champ-joints |
| MATRiX (2.0) | Open-source simulation and training platform | ✅ | MuJoCo physics at **500 Hz** + Unreal Engine 5 rendering (+ CARLA) · camera / LiDAR (Mid-360) / IMU / GPS simulation · multi-robot · 3DGS scene import · Linux and Windows · no ROS needed to start | free (BSD-3-Clause) | genisom-ai-matrix |
| RoamerX | Navigation stack (mapping, localisation, planning, multi-floor) | ✅ (open "Lite" community version; full version ships on robots) | ROS 2 Humble + Nav2 · NavFn planner + MPPI controller · behaviour trees · Gazebo / UE simulation | free community version | genisom-ai-roamerx |
| SomaMind | Physical-AI agent system (task understanding to skill execution) | 🧪 (announced December 2025; no public SDK found) | Skill orchestration on behaviour trees (trade press) · no public repo | not public | genisom-ai-somamind |

## What they will most likely bring to the hackathon

**Best guess, not confirmed by the organisers.**

- **Most likely: L1 / L1 EDU.** It is the company's volume product, the standard university and competition platform (winning team at the IROS 2025 legged challenge used it), small enough to ship and handle safely, and the EDU build carries Orin NX, LiDAR, depth camera and GNSS out of the box.
- **Plausible: L1-W or L2.** L2 is the product the company is currently promoting (built-in navigation, person-following, IP66) and suits outdoor demos in November mountain weather better than the L1 (L1 is rated 0–40 °C only).
- **Possible: M1.** It is the snow / ice / steep-slope machine and the IROS 2026 winning platform, but at about 30 kg it is a heavier and costlier demo unit. An M1 with the TA01 arm would be the only manipulation option.
- **Unlikely: SP1, NE01.** Explosion-proof unit has no use case at the venue; the humanoid is not yet released.
- **Certain regardless of hardware:** MATRiX simulator, URDF models, RoamerX and the SDKs are downloadable today.

Ask the Genisom booth first: which models, how many units, whether the EDU sensor kit and RoamerX full version are included, and whether an arm is available.

## Developer platform (summary)

- **Two SDK generations, both C++.** `genisom_L1_sdk` (MIT) for the L1 series: high-level API over UDP — stand, velocity commands, modes, plus IMU, odometry, joint and battery state. `genisom_robot_sdk` ("GEN2") for **M1 and L2**: C++17 client library, Ubuntu 22.04, x86_64 or aarch64, UDP port 8082 (WebSocket 8081 optional), sync / async examples, recharge and task control.
- **Python:** the legacy L1 SDK (`genisom_l1_sdk_old`, no longer maintained) shipped C++ and Python demos and both high-level and low-level interfaces. ⚠️ unverified whether the current L1 SDK exposes Python bindings or low-level joint control — check the repo docs before planning an RL / joint-level project.
- **Control ownership matters:** connecting does not grant control; the phone app and the SDK arbitrate. Read the "Control Ownership" doc in the GEN2 SDK before the first motion test.
- **ROS 2:** RoamerX Lite is a ROS 2 **Humble** / Nav2 stack (Ubuntu 22.04) that talks to the robot over UDP or LCM. The SDKs themselves are plain C++ libraries, not ROS packages.
- **Simulation:** MATRiX (MuJoCo + UE5, 451 GitHub stars, updated September 2026), `MATRiX_Python_SDK`, and URDF + meshes in `genisom_model` for RViz / Gazebo. The company states simulation policies can be deployed to L1 and M1.
- **AI / models:** `genisom_vln` (vision-language navigation with LLM / VLM, zero-shot baseline, runs against MATRiX) and `gawm` (lightweight JEPA-style world model). No general manipulation foundation model or public dataset found.
- **On-board compute:** L1 EDU — Orin NX, up to 100 TOPS. L2 — up to 86 TOPS. RoamerX Lite targets "NX / 3588" boards.
- **Hardware expansion:** 7 open interfaces on L1 (Ethernet, USB 3.0 / 2.0, 24 V / 12 V power), 15 on M1.
- **Teleoperation / data collection:** remote-control mode via SDK (JSON over UDP) and the app; no dedicated data-collection toolkit found.
- **Links:** [Open Source page](https://www.genisomai.com/en/opensource) · [github.com/zsibot](https://github.com/zsibot/) · [Download Center](https://www.genisomai.com/en/download.html)

## Current projects, deployments and customers

No individually named commercial customers were found; the company lists application sectors only.

- **2025-06** — L1 mass production started; 5,000th robot later in 2025 ([About Genisom](https://www.genisomai.com/en/aboutus.html)).
- **2025-10** — University of Manchester team won the IROS 2025 quadruped / legged robot challenge on an L1 ([technode.global](https://technode.global/prnasia/genisom-ai-showcases-embodied-intelligence-and-debuts-worlds-first-industry-grade-educational-quadruped-at-iros-2026/)).
- **2026 (Beijing Yizhuang)** — M1 acted as an autonomous-following pacer for a full half marathon (21 km, about 3 h, no remote control); M1 also won the quadruped autonomous-navigation category at the Yizhuang robot challenge, including water-crossing and pipe-traverse obstacles ([M1 product page](https://www.genisomai.com/en/product-robot/M1)).
- **2026-06** — First major international show at ICRA 2026 (Vienna): M1, L1, L1-W, L1 EDU, arm, CHAMP joints; 10,000-unit milestone claimed ([Robotics 24/7](https://www.robotics247.com/article/icra-2026-genisom-ai-showcases-mass-produced-robotics-platforms-and-deployment-stack)).
- **2026-07** — WAIC 2026 (Shanghai): application demos across power inspection, security, emergency response, industrial inspection, education, logistics and **accessibility** ([company news](https://www.genisomai.com/en/newsdetail/GENISOM-AI-at-WAIC-2026)).
- **2026-10** — NTU Singapore team won the fully autonomous category of the IROS 2026 Legged Robot Challenge on an M1 with arm tasks ([technode.global](https://technode.global/prnasia/genisom-ai-showcases-embodied-intelligence-and-debuts-worlds-first-industry-grade-educational-quadruped-at-iros-2026/)).
- **Sectors claimed:** security patrol, power infrastructure and petrochemical inspection, emergency response / firefighting, education and research, entertainment ([About Genisom](https://www.genisomai.com/en/aboutus.html)).
- **Europe / Switzerland:** no deployment or office found. ICRA Vienna is the only European activity identified.

## Roadmap and future direction

- **2026-07 (WAIC)** — Launched **L2**, unveiled explosion-proof **SP1** and first showing of the **NE01 humanoid** — expansion from quadrupeds into humanoids.
- **2026-08 (WRC Beijing)** — M1 + **TA01 arm** loco-manipulation demo; "dual-brain" architecture (high-level perception and decisions over real-time motion control); **GSD (Genisom Self-Driving)** data-driven navigation.
- **2026-10 (IROS Pittsburgh)** — **L1 Maker** educational kit and **MATRiX 2.0**; multi-robot collaborative transport demo.
- **Strategy** — four stated stages: locomotion, spatial, cognitive (interaction), swarm intelligence. Positions itself as a full-chain supplier from joints to complete robots, with ODM / component sales.
- **Funding and expansion** — Series B (hundreds of millions of RMB, led by Stone Venture, UAE) earmarked for platforms, embodied intelligence, applications and **international expansion**.
- **Education ecosystem** — EAI Academy (courses, competitions, certification) and the "Gravity" program giving researchers and developers access to robots and projects.
- ⚠️ unverified — Gasgoo reports an 800 million RMB cooperation agreement and a 2026 target of top quadruped sales with revenue above 1 billion RMB; the article could not be opened to confirm.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 4 | Autonomous navigation and person-following are built in; 8–30 kg payload suits short-distance delivery on stairs and slopes, but no manipulation by default | L2, L1-W, L1 EDU, RoamerX | [T01 brief](T01-Autonomous-Urban-Services/Genisom-AI-T01-1-Brief.md) |
| T02 Resilient & Safe City | 5 | Core market: security patrol, infrastructure inspection, emergency response; IP66 / IP67, snow and ice, −20 °C | M1, L2, L1 EDU | [T02 brief](T02-Resilient-and-Safe-City/Genisom-AI-T02-1-Brief.md) |
| T03 Sustainable City | 3 | Mobile sensing platform for energy and infrastructure inspection; sustainability logic must come from the team's payload and software | L1 EDU, L2, MATRiX | [T03 brief](T03-Sustainable-City/Genisom-AI-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 2 | Following, carrying and guiding companion roles are feasible (GLUE following, half-marathon pacer, "accessibility" demo), but no care-specific product or safe physical-assistance capability | L2, M1 Pro, L1 | [T04 brief](T04-Elderly-Care-and-Rehabilitation/Genisom-AI-T04-1-Brief.md) |

## Related docs
- [Product portfolio](Genisom-AI-Products.md) · [Developer guide](Genisom-AI-Developer-Guide.md) · [Roadmap and strategy](Genisom-AI-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [Genisom AI official site (English)](https://www.genisomai.com/en/)
- [About Genisom](https://www.genisomai.com/en/aboutus.html)
- [Genisom L1 product page](https://www.genisomai.com/en/product-robot/L1)
- [Genisom L1-W product page](https://www.genisomai.com/en/product-robot/L1-W)
- [Genisom L1 Maker product page](https://www.genisomai.com/en/product-robot/L1maker)
- [Genisom L2 product page](https://www.genisomai.com/en/product-robot/L2)
- [Genisom M1 product page](https://www.genisomai.com/en/product-robot/M1)
- [Genisom SP1 product page (Chinese)](https://www.genisomai.com/product-robot/sp1)
- [Genisom NE01 product page](https://www.genisomai.com/en/product-robot/NE01)
- [MATRiX product page](https://www.genisomai.com/en/product-robot/MATRiX)
- [Official Open Source page](https://www.genisomai.com/en/opensource)
- [Education and research ecosystem](https://www.genisomai.com/en/education-research)
- [GENISOM AI at WAIC 2026 (company news, 2026-07-19)](https://www.genisomai.com/en/newsdetail/GENISOM-AI-at-WAIC-2026)
- [GENISOM AI at WRC 2026 (company news, 2026-08-23)](https://www.genisomai.com/en/newsdetail/GENISOM-AI-at-WRC-2026)
- [GitHub organisation zsibot](https://github.com/zsibot/)
- [genisom_L1_sdk](https://github.com/zsibot/genisom_L1_sdk)
- [genisom_robot_sdk](https://github.com/zsibot/genisom_robot_sdk)
- [genisom_roamerx_open](https://github.com/zsibot/genisom_roamerx_open)
- [matrix (MATRiX simulator)](https://github.com/zsibot/matrix)
- [IROS 2026 press release via TNGlobal (2026-10-01)](https://technode.global/prnasia/genisom-ai-showcases-embodied-intelligence-and-debuts-worlds-first-industry-grade-educational-quadruped-at-iros-2026/)
- [Robotics 24/7 — ICRA 2026 coverage](https://www.robotics247.com/article/icra-2026-genisom-ai-showcases-mass-produced-robotics-platforms-and-deployment-stack)
- [The Robot Report — ICRA 2026 (sponsored content)](https://www.therobotreport.com/genisom-ai-debuts-deployable-robotics-platforms-icra-2026/)
- [Gasgoo — 10,000-unit milestone (search summary only, page not readable)](https://autonews.gasgoo.com/articles/news/genisom-ais-embodied-robots-surpass-10000-unit-production-milestone-2061438385384919041)
