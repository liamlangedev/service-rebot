---
type: company
company: "Unitree Robotics"
slug: Unitree
hq: "Hangzhou, China"
founded: 2016
website: https://www.unitree.com
categories: [quadruped, humanoid, arm, mobile-manipulator, dexterous-hand, sensors, components, software, data]
on_site_guess: "Go2 EDU quadrupeds and G1 EDU humanoids (possibly with Dex3-1 hands); maybe R1 or a B2 / As2 as showpiece"
fit_t01: 4
fit_t02: 5
fit_t03: 3
fit_t04: 3
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# Unitree Robotics

> **One-liner:** Hangzhou-based, STAR-Market-listed maker of low-cost, high-performance legged robots — quadrupeds (Go2, As2, A2, B2) and humanoids (R1, G1, H2) — with the most widely used open SDK and RL / teleoperation tooling in the research community.
> **Why it matters at Leukerbad:** Unitree is the safest "it just walks" choice: legged mobility on stairs, slopes and snow out of the box, a mature SDK (C++ / Python / ROS 2), and more community code than any other vendor on site. Best base for patrol, inspection, carry and search tasks in steep alpine terrain.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Hangzhou, Zhejiang, China |
| Founded | 2016 |
| Founders / CEO | Wang Xingxing (founder, CEO) |
| Size and funding | Listed on Shanghai STAR Market, debut **19 Aug 2026**; IPO raised about **RMB 6.1 bn (~USD 910M)** at RMB 150.80/share. 2025 revenue about **RMB 1.70 bn** (reported, +335% YoY); H1 2026 revenue guided at RMB 1.05–1.13 bn. About **5,500 humanoids shipped in 2025**. Headcount: not confirmed here |
| Core business | Consumer / education / industrial quadrupeds, humanoids, robot arms, dexterous hands, 4D LiDAR, joint motors; embodied-AI models (UnifoLM) and data platform |
| Website | https://www.unitree.com |
| Docs / developer portal | https://support.unitree.com (developer docs, ⚠️ not re-fetched in this run) · https://www.unitree.com/opensource |
| GitHub | https://github.com/unitreerobotics |

## Portfolio at a glance

Prices are official-site list prices in USD, excluding tax and shipping, as shown on 2026-11-14. "EDU" variants are the ones with full secondary-development (SDK) access; their prices are "contact sales".

| Product | Type | Status | Key specs | Price | Img key |
|---|---|---|---|---|---|
| Go2 (Air / Pro / X / EDU) | Small quadruped | ✅ | **~15 kg**; payload ~7–8 kg (max 10–12 kg); up to 3.7 m/s (EDU ~5 m/s peak); **1–2 h** (EDU 15,000 mAh: 2–4 h); 4D LiDAR L2 (360°×96°); EDU: optional Orin module (40–100 TOPS) | Air **$1,600** · Pro **$2,800** · X **$4,500** · EDU contact sales | unitree-go2 |
| Go2-W | Wheel-legged small quadruped | ✅ | Wheeled version of Go2; detailed specs not checked ⚠️ unverified | not public | unitree-go2-w |
| As2 (Air / Pro / X / EDU) | Compact industrial quadruped (unveiled 24 Feb 2026) | ✅ | **~20 kg**; walking load ~15 kg (Air ~10 kg), standing up to ~65 kg; up to ~5 m/s; **>4 h / >13 km** unloaded (648 Wh); **IP54** (Pro / X / EDU); SDK on X and EDU; EDU: optional Orin NX dock | contact sales | unitree-as2 |
| As2-W | Wheel-legged version of As2 | ✅ | Specs not checked ⚠️ unverified | not public | unitree-as2-w |
| A2 / A2-PRO | Mid-size industrial quadruped | ✅ | **~42 kg** with battery; walking load ~25 kg, standing ~100 kg; up to ~5 m/s; **>5 h / ~20 km** unloaded; **IP56** (PRO: core parts IP67, dual LiDAR); i7 for user development | contact sales | unitree-a2 |
| A2-W | Wheel-legged version of A2 | ✅ | Specs not checked ⚠️ unverified | not public | unitree-a2-w |
| B2 | Large industrial quadruped | ✅ | **~60 kg**; walking load >40 kg, standing ≥120 kg; **IP67**; **4–6 h**, >20 km unloaded (2,250 Wh); slopes >45°, 40 cm steps; i5 + i7 on board, optional Orin NX | not public (contact sales) | unitree-b2 |
| B2-W | Wheel-legged large quadruped | ✅ | Wheeled B2; specs not checked ⚠️ unverified | not public | unitree-b2-w |
| B2-Ex | B2 variant listed on site (name suggests explosion-proof) | ✅ | Specs not checked ⚠️ unverified | not public | unitree-b2-ex |
| R1 (Air / R1 / EDU) | Lightweight humanoid | ✅ | **1.23 m**, **27–29 kg**; 20 / 26 / 26–40 DoF; **~1 h** battery; EDU: SDK, optional hands and Orin module (40–100 TOPS) | Air **$4,900** · R1 **$5,900** · EDU contact sales | unitree-r1 |
| G1 / G1 EDU | Compact humanoid | ✅ | **1.32 m**, **~35 kg**; 23 DoF (EDU 23–43); **~2 h**; depth camera + 3D LiDAR; EDU: SDK, optional Dex3-1 hands, Orin-class module | G1 **$13.5K** · EDU contact sales | unitree-g1 |
| G1+ / G1+ EDU | Upgraded G1 | ✅ | **1.34 m**, ~35 kg; 25 DoF (EDU 25–45), 2-DoF neck; stereo + wide camera, 6-mic array; stronger shoulder / waist motors; external power supported | G1+ **$15K** · EDU contact sales | unitree-g1-plus |
| G1-D (Standard / Flagship) | Wheeled dual-arm mobile manipulator + data platform | ✅ | G1 upper body on differential base with lift column (1.26–1.68 m); 17 / 19 DoF, 7-DoF arms, **~3 kg per arm**; ~90 kg; **~2 h / ~6 h**; head stereo + 2 wrist cameras; data-collection and training toolchain | not public | unitree-g1-d |
| H1 / H1-2 | Full-size humanoid (previous generation) | ✅ | Research platform; specs not checked ⚠️ unverified | not public | unitree-h1 |
| H2 / H2 EDU | Full-size humanoid | ✅ | **1.82 m**, **~70 kg**; 31 DoF; leg joints up to 360 N·m, arm 120 N·m; arm payload 7 kg rated / 15 kg peak; **~3 h** (0.97 kWh); i5 / i7 on board | H2 **$29,900** · EDU contact sales | unitree-h2 |
| H2-X / H2-X EDU | Next-gen full-size humanoid | ✅ | **~1.70 m**, **65+ kg**; 31 DoF; dual hot-swap batteries (1.15 kWh each), **~4 h walking**; optional Jetson Thor T5000 / AGX Orin | H2-X **$25,400** · EDU contact sales | unitree-h2-x |
| H2 Plus | NVIDIA Isaac GR00T reference humanoid (H2 + Sharpa Wave hands + Jetson Thor) | 🧪 (announced 1 Jun 2026, availability "late 2026") | 31 body DoF, **75 DoF** with 22-DoF hands; Jetson AGX Thor T5000, 128 GB | not public | unitree-h2-plus |
| GD01 | Pilotable transforming mecha | 🧪 / ✅ (unveiled May 2026; not hackathon-relevant) | Rideable biped / quadruped form | from **RMB 3.9M** (~USD 574K) | unitree-gd01 |
| Z1 | Light 6-axis robot arm (older line) | ✅ | Specs not checked ⚠️ unverified | not public | unitree-z1 |
| D1-T | Small servo arm (Go2 accessory class) | ✅ | Specs not checked ⚠️ unverified | not public | unitree-d1-t |
| D2 | 7-DoF arm + gripper, mountable on quadrupeds | ✅ | 7 DoF + 1-DoF gripper; **3 kg rated** (5 kg max); 612 mm arm, 760 mm working radius; **5.9 kg**; 500 Hz control; SDK + drag teaching | not public | unitree-d2 |
| R1-7a | Robot arm listed on site | ✅ | Specs not checked ⚠️ unverified | not public | unitree-r1-7a |
| Dex3-1 | 3-finger dexterous hand (G1 option) | ✅ | **7 DoF** per hand; optional tactile arrays | not public | unitree-dex3-1 |
| Dex5-1 | 5-finger dexterous hand | ✅ | **20 DoF (16 active + 4 passive)**; 1.1 kg; **94 tactile sensors**; 10 N fingertip force; grasp load 3.5–4.5 kg | not public | unitree-dex5-1 |
| Dex1-1 / Dex2/5 / Dex5-S | Gripper and further hand variants | ✅ | Listed on site; specs not checked ⚠️ unverified | not public | unitree-dex-other |
| 4D LiDAR L1 / L2 | Low-cost 3D LiDAR | ✅ | L2: **360° × 96°** field of view (as used on Go2) | not public | unitree-l2-lidar |
| Joint motors and components | Actuators (GO-M8010-6, B1-16, IM6014, servos), BA2 charging dock | ✅ | Catalogue items; specs not checked | not public | unitree-motors |
| UnifoLM (WMA-0, VLA-0) and UniPlatform / UniStore | Embodied-AI models, data and app platforms | ✅ open source (WMA-0, Sept 2025, CC BY-NC-SA 4.0) · 🧪 platforms | World-model-action and VLA models for manipulation | free (non-commercial licence for WMA-0) | unitree-unifolm |

Legacy lines still listed on the site: Go1, A1, B1, AlienGo.

## What they will most likely bring to the hackathon

**Best guess, not confirmed.** The organiser list names "Go2 / B2 quadrupeds, G1 / H1 / R1 humanoids, Z1 arm, Dex hands". Reasoning:

- **Go2 EDU** — near-certain. It is the standard developer-event quadruped: 15 kg, safe around people, full SDK, optional Orin. Check the variant: **Air and Pro have no real SDK access**; X is partial; only EDU is fully open.
- **G1 EDU** (likely with **Dex3-1** hands) — near-certain. It is the de-facto research humanoid and the one all Unitree teleoperation / RL repos target.
- **R1 / R1 EDU** — plausible as the newest low-cost humanoid; only ~1 h battery and manipulation needs the EDU version.
- **B2 or As2 / A2** — possible as a showpiece for outdoor / snow demos; heavy robots (42–60 kg) are less likely to be handed to teams freely.
- **H1 / H2** — possible as demo units; full-size humanoids are risky for 48-hour teams.
- **Z1 / D2 arm** — possible as an add-on for a quadruped.

Ask at the booth first: which variant (EDU or not), is the Orin / development PC fitted, which hands, how many batteries and chargers, and is a remote e-stop provided.

## Developer platform (summary)

- **unitree_sdk2** (C++) and **unitree_sdk2_python** — DDS-based (CycloneDDS) SDK for Go2, B2, G1, H1, R1 and newer robots. Works from a laptop over Ethernet or from the on-board development computer.
- **Two control levels:** high-level sport / locomotion services (velocity commands, postures, built-in gaits, obstacle avoidance) and low-level joint control (position / velocity / torque per motor). Start high-level; low-level disables the factory controller and is where robots fall.
- **ROS 2:** **unitree_ros2** talks to the same DDS topics natively; **unitree_ros** provides URDFs and ROS 1 simulation packages.
- **Simulation:** **unitree_mujoco** (sim-to-real with the same SDK interface, C++ / Python), **unitree_sim_isaaclab** (Isaac Lab scenes for G1 / H1-2), URDF / MJCF / USD robot models.
- **Reinforcement learning:** **unitree_rl_gym** (Isaac Gym; Go2, H1, G1) and **unitree_rl_lab** (Isaac Lab), both with deploy-to-robot paths.
- **Teleoperation and data collection:** **xr_teleoperate** (humanoid teleop from XR headsets), **teleimager** (multi-camera streaming via ZeroMQ / WebRTC); G1-D ships a full data-collection, training and one-click deployment toolchain.
- **Pretrained models:** **UnifoLM-WMA-0** (open-source world-model-action, non-commercial licence), **UnifoLM-VLA-0** (VLA for humanoid manipulation); G1-D platform states integration with open models such as Pi and GR00T; NVIDIA Isaac GR00T will support G1 as a reference workflow (announced June 2026).
- **On-board compute:** 8-core CPU for platform functions on small robots; EDU versions add an Orin-class module (40–100 TOPS on Go2 / R1); B2 / A2 / H2 carry an Intel i7 for user code; H2-X / H2 Plus can take Jetson Thor.
- **Sensors out of the box:** 4D LiDAR L2 on Go2; depth camera + 3D LiDAR on G1; stereo cameras on R1 / G1+ / H2.
- **Links:** docs https://support.unitree.com · open-source index https://www.unitree.com/opensource · GitHub https://github.com/unitreerobotics

## Current projects, deployments and customers

- **Industrial inspection (official solution line):** Unitree markets B2-class quadrupeds for power / substation inspection with thermal and acoustic payloads and a 3D route-planning workflow. [Unitree inspection solution](https://www.unitree.com/mobile/industry/electricity)
- **Fire rescue (official solution line):** quadrupeds with firefighting payloads; per Unitree, units were adopted by a Qingdao fire and rescue support team and used in drills (reported Nov 2025). [WinFuture](https://winfuture.de/news,150757.html)
- **Feb 2026 — Spring Festival Gala:** G1 robots performed an autonomous kung-fu routine; H2 and B2-W also shown. Signals strong whole-body control, mostly entertainment use. [eWeek](https://www.eweek.com/news/unitree-20000-humanoid-robots-2026-china/)
- **Shipments:** about **5,500 humanoids in 2025**; AGIBOT and Unitree together held close to 80% of ~13,000 global humanoid shipments. [eWeek](https://www.eweek.com/news/unitree-20000-humanoid-robots-2026-china/)
- **Apr 2026 — R1 sold internationally via AliExpress** at about USD 4K entry price (reported). [eWeek](https://www.eweek.com/news/china-unitree-4k-humanoid-robot-apac/)
- **Education and research:** the largest installed base of legged robots in universities; G1 and Go2 are the reference platforms in most open RL / teleoperation projects (see GitHub star counts). [GitHub](https://github.com/unitreerobotics)
- **Competitions:** Unitree runs its own UniBot World Challenge and a World Physical AI Competition, plus RoboCup (G1-Comp) and boxing (G1-Boxing) packages. [unitree.com](https://www.unitree.com)
- **Elderly care / rehabilitation, delivery, sustainability:** no confirmed commercial deployments found. Europe / Switzerland-specific activity: not found in this research.

## Roadmap and future direction

- **24 Feb 2026 — As2** compact industrial quadruped unveiled. [DigiTimes](https://www.digitimes.com/news/a20260225VL208.html)
- **Feb 2026 — target of 10,000–20,000 humanoid shipments in 2026** (Wang Xingxing); he named operation outside controlled environments as the main open problem. [eWeek](https://www.eweek.com/news/unitree-20000-humanoid-robots-2026-china/)
- **Mar 2026 — STAR Market filing** (initial target RMB 4.2 bn); filing points to a general-purpose humanoid embodied foundation model and household / elder-care use by about 2030. [Caixin](https://www.caixinglobal.com/2026-03-21/unitree-robotics-files-for-608-million-star-market-ipo-102425491.html) · [Notebookcheck](https://www.notebookcheck.net/Beyond-kung-fu-Unitree-plans-humanoid-robot-for-household-chores-and-elder-care-by-2030.1255707.0.html)
- **Apr 2026 — low-cost dual-arm platform** reported at about RMB 26,900 (~USD 4.3K); exact model name ⚠️ unverified (the site lists R1-A / R1-A-D "application plans"). [Startup Fortune](https://startupfortune.com/unitree-just-priced-a-dual-arm-humanoid-robot-at-4290-and-the-embodied-ai-experimentation-race-is-about-to-get-crowded/)
- **May 2026 — GD01** pilotable mecha, from RMB 3.9M. [CnTechPost](https://cntechpost.com/2026/05/12/unitree-unveils-worlds-first-mass-produced-manned-mecha-gd01/)
- **1 Jun 2026 — H2 Plus**, NVIDIA Isaac GR00T reference humanoid, availability late 2026; GR00T workflow for G1 to be published. [PR Newswire](https://tools.prnewswire.com/en-us/live/20823/release/20260601EN72140)
- **19 Aug 2026 — IPO completed**, about RMB 6.1 bn raised; shares rose several-fold on debut (reports differ: +460% to +629%). [Caixin](https://www.caixinglobal.com/2026-07-31/robotics-startup-unitree-launches-620-million-star-market-ipo-102469723.html) · [The Asset](https://www.theasset.com/article/56931/unitree-robotics-ipo-oversubscribed-8-200-times)
- **Aug 2026 — "Superman" humanoid prototype** reported; details ⚠️ unverified. [VnExpress](https://e.vnexpress.net/news/tech/enterprises/world-s-largest-humanoid-robot-maker-unveils-superman-robot-5110323.html)
- **Direction:** push prices down (R1 Air at $4,900), widen the line (G1+, H2-X, wheel-legged "-W" versions, G1-D wheeled manipulator), and build the data / model layer (UnifoLM, UniPlatform, UniStore).

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 4 | Legged and wheel-legged robots handle stairs, slopes and snow; Go2 with LiDAR gives patrol / carry / guide demos in 48 h, but no proven delivery deployments | Go2 EDU, Go2-W, As2, G1-D | [T01 brief](T01-Autonomous-Urban-Services/Unitree-T01-1-Brief.md) |
| T02 Resilient & Safe City | 5 | Official inspection and fire-rescue solution lines; IP67 B2 and IP54–56 As2 / A2 built for hazardous terrain; reported fire-service adoption | B2, A2, As2, Go2 EDU | [T02 brief](T02-Resilient-and-Safe-City/Unitree-T02-1-Brief.md) |
| T03 Sustainable City | 3 | Useful as a mobile sensing / monitoring platform (energy, waste, environment), but nothing purpose-built | Go2 EDU, As2, D2 arm on quadruped | [T03 brief](T03-Sustainable-City/Unitree-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 3 | G1 / R1 humanoids and Go2 can do companion, fetch, guide and fall-detection demos; no care deployments, limited arm payload, and falls near frail people are a safety concern | G1 EDU + Dex3-1, G1-D, Go2 EDU | [T04 brief](T04-Elderly-Care-and-Rehabilitation/Unitree-T04-1-Brief.md) |

## Related docs
- [Product portfolio](Unitree-Products.md) · [Developer guide](Unitree-Developer-Guide.md) · [Roadmap and strategy](Unitree-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources

- [Unitree official site (product navigation)](https://www.unitree.com)
- [Unitree Go2](https://www.unitree.com/go2)
- [Unitree As2](https://www.unitree.com/As2)
- [Unitree A2](https://www.unitree.com/A2)
- [Unitree B2](https://www.unitree.com/b2)
- [Unitree R1](https://www.unitree.com/R1)
- [Unitree G1](https://www.unitree.com/g1)
- [Unitree G1+](https://www.unitree.com/G1pl)
- [Unitree G1-D](https://www.unitree.com/G1-D)
- [Unitree H2](https://www.unitree.com/H2)
- [Unitree H2-X](https://www.unitree.com/H2-X)
- [Unitree D2 arm](https://www.unitree.com/D2)
- [Unitree Dex5-1](https://www.unitree.com/Dex5-1)
- [Unitree intelligent inspection solution](https://www.unitree.com/mobile/industry/electricity)
- [Unitree GitHub organisation](https://github.com/unitreerobotics)
- [PR Newswire — Unitree announces H2 Plus, NVIDIA Isaac GR00T reference humanoid (1 Jun 2026)](https://tools.prnewswire.com/en-us/live/20823/release/20260601EN72140)
- [eWeek — Unitree aims to ship 20,000 humanoids in 2026 (19 Feb 2026)](https://www.eweek.com/news/unitree-20000-humanoid-robots-2026-china/)
- [eWeek — Unitree to launch $4K humanoid globally](https://www.eweek.com/news/china-unitree-4k-humanoid-robot-apac/)
- [Caixin — Unitree files for STAR Market IPO (21 Mar 2026)](https://www.caixinglobal.com/2026-03-21/unitree-robotics-files-for-608-million-star-market-ipo-102425491.html)
- [Caixin — Unitree launches STAR Market IPO (31 Jul 2026)](https://www.caixinglobal.com/2026-07-31/robotics-startup-unitree-launches-620-million-star-market-ipo-102469723.html)
- [The Asset — Unitree IPO oversubscribed 8,200 times](https://www.theasset.com/article/56931/unitree-robotics-ipo-oversubscribed-8-200-times)
- [KrASIA — Unitree targets IPO after revenue quadruples](https://kr-asia.com/unitree-targets-ipo-after-revenue-quadruples-on-robotics-demand)
- [Yicai Global — Unitree open-sources world model (Sept 2025)](https://www.yicaiglobal.com/news/chinas-unitree-open-sources-world-model-to-advance-robotics-ecosystem)
- [DigiTimes — Unitree As2 unveiled (25 Feb 2026)](https://www.digitimes.com/news/a20260225VL208.html)
- [CnTechPost — Unitree GD01 mecha (12 May 2026)](https://cntechpost.com/2026/05/12/unitree-unveils-worlds-first-mass-produced-manned-mecha-gd01/)
- [Notebookcheck — Unitree household / elder-care humanoid plans](https://www.notebookcheck.net/Beyond-kung-fu-Unitree-plans-humanoid-robot-for-household-chores-and-elder-care-by-2030.1255707.0.html)
- [WinFuture — Unitree firefighting robot dogs](https://winfuture.de/news,150757.html)
- [VnExpress — Unitree "Superman" robot](https://e.vnexpress.net/news/tech/enterprises/world-s-largest-humanoid-robot-maker-unveils-superman-robot-5110323.html)
- [Startup Fortune — Unitree dual-arm robot at $4,290](https://startupfortune.com/unitree-just-priced-a-dual-arm-humanoid-robot-at-4290-and-the-embodied-ai-experimentation-race-is-about-to-get-crowded/)
