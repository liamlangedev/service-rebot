---
type: company
company: "Galbot"
slug: Galbot
hq: "Beijing, China"
founded: 2023
website: https://www.galbot.com
categories: [mobile-manipulator, humanoid, software, data]
on_site_guess: "Galbot G1 wheeled dual-arm mobile manipulator with GalbotSDK (best guess); ET1 small biped possible"
fit_t01: 4
fit_t02: 2
fit_t03: 3
fit_t04: 3
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# Galbot

> **One-liner:** Beijing embodied-AI company (银河通用机器人) that builds wheeled dual-arm mobile manipulators (G1, S1), a small bipedal humanoid (ET1) and the AstraBrain family of robot foundation models trained largely on synthetic data.
> **Why it matters at Leukerbad:** The G1 is one of the few robots on site with a proven 24/7 commercial record in pick-fetch-hand-over work (pharmacies, retail kiosks, instant-retail warehouses), plus a public C++/Python SDK and URDF/MJCF/USD assets. It is the natural choice for "robot fetches the right item from a shelf and hands it to a person" builds.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Beijing, China (Chinese name 银河通用机器人; GitHub org name "GalaxyGeneralRobotics") |
| Founded | **May 2023** |
| Founders / CEO | Wang He (founder and CEO; Peking University faculty). Other co-founders: not confirmed here |
| Size and funding | Headcount not public. Rounds: RMB 1.1B (Jun 2025, CATL-led), **>US$300M at ~US$3B valuation (Dec 2025)**, **RMB 2.5B (Mar 2026)**. Reported cumulative: >RMB 6.96B (Chinese press) / ~US$1.15B (Sacra) ⚠️ unverified totals. Valuation reported >RMB 22B |
| Core business | General-purpose robots + embodied foundation models; sells hardware, vertical solutions (smart pharmacy, retail "Space Capsule", factory handling) and a tiered developer subscription |
| Website | https://www.galbot.com |
| Docs / developer portal | https://developer.galbot.com (Chinese and English) |
| GitHub | https://github.com/GalaxyGeneralRobotics (18 public repos). GraspVLA code lives at PKU-EPIC/GraspVLA |

## Portfolio at a glance

| Product | Type | Status | Key specs (verified on official pages unless marked) | Price | Img key |
|---|---|---|---|---|---|
| **Galbot G1** | Wheeled dual-arm mobile manipulator (semi-humanoid) | ✅ shipping | Height max **1,730 mm** · **92.5 kg** · **21 DoF** (2 neck, 7x2 arms, 3 waist, 2 leg/lift) · payload **5 kg per arm / 10 kg both** · wrist reach 0-2,100 mm vertical · 4-wheel omni base, **1.5 m/s** · **8 h** runtime, 3.5 h charge · NVIDIA AGX Orin 64 GB · 3D LiDAR, stereo head camera, 4 torso RGB, 2 wrist depth cameras, 2 wrist 6-axis F/T · swappable gripper / suction / dexterous hand · IP54, 0-40 °C | Not public (a reseller blog quotes ~US$87-97k ⚠️ unverified) | galbot-g1 |
| **Galbot G1 Lite** | Wheeled general-purpose robot (lighter G1 variant) | ✅ listed as supported on developer portal | Specs not public ⚠️ unverified | Not public | galbot-g1-lite |
| **Galbot S1** | Heavy-duty industrial wheeled dual-arm robot | ✅ shipping (in CATL production lines) | Height max **1,793 mm** · **320 kg** · **50 kg dual-arm payload** · 17 DoF (2 neck, 7x2 arms, 1 lift, 750 mm travel) · reach floor to ~2.3-2.4 m · 4-wheel-steer omni base, 1.5 m/s · 2 x 48 V 30 Ah hot-swap batteries, 8 h · AGX Orin 64 GB · 3 x 3D LiDAR | Not public | galbot-s1 |
| **Galbot ET1** ("银河星仔") | Small bipedal humanoid, agent-native, interaction / entertainment focus | ✅ pre-orders since 2026-09-03, "Buy now" via JD.com | Standing height **1,250 mm** · **32 kg** with battery · **26 DoF** Standard; **38 DoF** Pro / Flagship (adds 12 hand DoF) · stereo camera · RK3588 + RDK X5; Pro adds Orin Nano (40 TOPS), Flagship Orin NX (100 TOPS) | Not found (see JD.com listing) | galbot-et1 |
| **AstraBrain** (银河星脑): WAM, WBC, Dex, Agent | Embodied foundation-model family (brain + cerebellum) | ✅ in products / 🧪 partly open (WBC 0.5 code released as "Humanoid-GPT") | 3B-13B "cerebrum" at 5-10 Hz + 80-300M "cerebellum" at 100-250 Hz (company figures) | Not public | galbot-astrabrain |
| **GraspVLA / GroceryVLA / TrackVLA / NavFoM / UrbanVLA** | Task foundation models (grasping, retail picking, person following, navigation, urban micromobility) | ✅ GraspVLA open (model + sim playground + real-robot interface, Jul 2025); UrbanVLA repo public (ICRA 2026); others research / in-product | GraspVLA: pretrained on billion-scale synthetic grasp data, zero-shot open-vocabulary grasping | Free (open-source parts) | galbot-graspvla |
| **Galbot Space Capsule** (银河太空舱) | Robot-run retail kiosk built around G1 | ✅ operating | **170+ locations in 40+ cities** (official site, 2026) | Not public | galbot-space-capsule |
| **Smart pharmacy / instant-retail warehouse solution** | Vertical solution built around G1 | ✅ operating | **100+ instant-retail warehouses**, 7x24, 1.5+ years continuous operation (official site) | Not public | galbot-smart-pharmacy |

Notes: the SDK README badge also lists a "G3" model, with no public product page ⚠️ unverified. The public repo `galbot_one_golf_description` is a ROS 2 description package for "Galbot One Golf", which appears to be a G1-family code name ⚠️ unverified.

## What they will most likely bring to the hackathon

**Best guess, not confirmed by the organisers:**

- **Most likely: Galbot G1** with two-finger grippers and GalbotSDK. It is the company's volume product (reported 1,200+ units shipped in 2025), the main SDK target, and the robot behind every retail and pharmacy demo they show at trade fairs (WAIC 2026, CES 2026, Hannover Messe 2026).
- **Possible: Galbot ET1.** At 32 kg it is easy to ship, and it was launched in Aug-Sep 2026 as an "agent-native" interaction robot. Good for greeting / companionship demos, weak for manipulation in the Standard version (no dexterous hands).
- **Unlikely: Galbot S1.** 320 kg and built for factory lines.
- **Assume indoor, flat-floor use.** G1 is wheeled, IP54, rated 0-40 °C. It will not drive on snow, stairs or steep alpine paths. Plan outdoor legs with another vendor's quadruped.
- **Ask at the booth first:** which SDK / robot environment version is installed (SDK V1.10.0 expects robot environment V1.18), whether low-level control is unlocked, and whether GraspVLA or the retail picking stack is preloaded.

## Developer platform (summary)

- **GalbotSDK** (official, GitHub): **C++ and Python** (3.8-3.14), Ubuntu 20-24; current **V1.10.0 (2026-09-22)** for robot environment V1.18. Supports G1 and S1 (badge also lists G3). Docs ship inside the repo per model, in English and Chinese.
- **Two control levels:** high-level (built-in planning, navigation, whole-body control) and low-level (joint motors, chassis velocity, raw sensor streams). Five API areas: perception, planning, control, navigation, interaction. End-to-end model action commands can be passed through the SDK.
- **ROS 2:** official description packages built with colcon (`galbot_one_golf_description`, `galbot_s1_description`), Apache-2.0. A ROS 2 runtime bridge for the SDK is not documented publicly ⚠️ unverified.
- **Simulation assets:** G1 and S1 in **URDF, MJCF and USD**; SimReady scenes and objects on request. Browser-based online simulation is a paid-tier feature.
- **Pretrained models:** GraspVLA (open weights, simulation playground, real-robot control interface; Python 3.9 conda setup), Humanoid-GPT (AstraBrain-WBC 0.5), UrbanVLA, OpenTrack / Any2Track, HumanTracker. NavFoM, TrackVLA and GroceryVLA are named by the company; public code availability not confirmed here.
- **Teleoperation / data:** OpenWBT (open-source whole-body teleoperation, published for Unitree humanoids on ROS 2 Foxy). Galbot's own strategy is synthetic-data-first (AstraData); a public G1 teleop kit is not documented ⚠️ unverified.
- **On-board compute:** G1 and S1 use NVIDIA AGX Orin 64 GB (275 TOPS). ET1 uses RK3588 + D-Robotics RDK X5, with optional Orin Nano / Orin NX.
- **Developer portal tiers:** Free (SDK, docs, digital models, community, 5 AI-assistant queries/day) · Pro **¥50,000 per robot per year** (online sim, one-click real-robot deployment, remote debugging) · Enterprise **¥200,000 per robot per year** (on-site engineer). Ready-made "L2" kits: welcome / guide (live), material sorting (coming soon), site inspection (planned).
- **Links:** [developer portal](https://developer.galbot.com/?lang=en) · [GalbotSDK](https://github.com/GalaxyGeneralRobotics/GalbotSDK) · [GitHub org](https://github.com/GalaxyGeneralRobotics) · [GraspVLA paper](https://arxiv.org/abs/2505.03233)

## Current projects, deployments and customers

- **2026-09-28:** G1 goes into regular commercial operation at a Laobaixing Pharmacy store in Shanghai (human-robot collaborative retail, 24-hour drug sales). [Galbot news](https://www.galbot.com)
- **2026 (site figures):** Space Capsule retail kiosks at **170+ locations in 40+ cities**; G1 working 7x24 in **100+ instant-retail warehouses**, some running for 1.5+ years. [G1 page](http://www.galbot.com/g1/)
- **2026 (reported):** S1 passed acceptance at CATL's Ningde base in March and has worked on mass-production lines 24/7 since. Reported by Gasgoo (seen via search result, not read in full) ⚠️ unverified.
- **2026 (reported):** Orders of "several thousand units" from CATL, Bosch, Toyota, BAIC and SAIC; pharmacy partners include Neptunus (海王星辰) with a claimed 99.95% order accuracy. Company / press claims ⚠️ unverified.
- **2025-26:** Bowintec joint venture with Boyuan Capital (Bosch group investment arm), aimed at loading, assembly and inspection in Bosch's manufacturing network, including outside China. [Sacra](https://sacra.com/c/galbot/)
- **Healthcare:** joint research relationship with Xuanwu Hospital (Beijing) reported; **no elderly-care or rehabilitation deployment found**. [Sacra](https://sacra.com/c/galbot/)
- **Outside mainland China:** autonomous retail stores opened in Hong Kong (The Standard, seen via search result) ⚠️ unverified; trade-show presence at CES 2026 and Hannover Messe 2026. **No Europe or Switzerland deployment found.**
- **Research showcases 2026:** autonomous humanoid tennis ("AstraTennis", Aug 2026), three golds at a humanoid robot sports event (Aug 2026), IROS 2026 best-paper award for joint research (Oct 2026). [Galbot news](https://www.galbot.com)

## Roadmap and future direction

- **2026-01:** S1 heavy-duty industrial robot launched (reported). 🧪 to ✅ during 2026.
- **2026-03:** RMB 2.5B round; investors reported include the national AI industry fund, Sinopec and CITIC. Valuation reported above RMB 22B. [TechNode](https://technode.com/2026/08/27/how-far-are-robots-from-actually-working-on-production-lines-galbots-industrial-ai-journey/)
- **2026-08 (WRC Beijing):** ET1 unveiled, the first bipedal product; move from wheeled-only to a multi-form lineup under "one brain" (AstraBrain WAM / WBC / Dex / Agent).
- **2026-09-03:** ET1 pre-orders open; positioned as the "first native agent robot" for theme parks, shop greeting and stage performance.
- **Strategy:** synthetic-data-first training, sell full vertical solutions (pharmacy, retail, factory) and now a paid developer ecosystem with semi-finished kits (sorting, inspection still 🔭).
- **IPO:** Chinese press describes an IPO track; no official filing confirmed here ⚠️ unverified.
- **Europe:** route is industrial, through the Bosch joint venture. No announced European service, care or education programme.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | **4** | Proven 24/7 retail, pharmacy and kiosk service robot; clear 48 h path for indoor fetch, vend and hand-over; indoor only | G1, GraspVLA, Space Capsule concept, ET1 for greeting | [T01 brief](T01-Autonomous-Urban-Services/Galbot-T01-1-Brief.md) |
| T02 Resilient & Safe City | **2** | No safety or emergency deployments; wheeled, 0-40 °C; useful only for indoor supply handling or inspection (inspection kit still planned) | G1, HumanTracker / TrackVLA | [T02 brief](T02-Resilient-and-Safe-City/Galbot-T02-1-Brief.md) |
| T03 Sustainable City | **3** | Open-vocabulary grasping fits waste or returns sorting and restocking; sorting kit not yet released, so integration work needed | G1, GraspVLA | [T03 brief](T03-Sustainable-City/Galbot-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | **3** | Medication and item fetching maps directly onto the pharmacy stack; 5 kg arms and F/T wrists suit hand-over, not physical support; no care deployments | G1, GraspVLA, ET1 for companionship | [T04 brief](T04-Elderly-Care-and-Rehabilitation/Galbot-T04-1-Brief.md) |

## Related docs
- [Product portfolio](Galbot-Products.md) · [Developer guide](Galbot-Developer-Guide.md) · [Roadmap and strategy](Galbot-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [Galbot official site (home, news list, AstraBrain)](https://www.galbot.com)
- [Galbot G1 product page](http://www.galbot.com/g1/)
- [Galbot S1 product page](http://www.galbot.com/s1/)
- [Galbot ET1 product page](http://www.galbot.com/et1/)
- [Galbot About page](http://www.galbot.com/about/)
- [Galbot developer portal](https://developer.galbot.com/?lang=en)
- [GitHub org GalaxyGeneralRobotics](https://github.com/GalaxyGeneralRobotics)
- [GalbotSDK README](https://raw.githubusercontent.com/GalaxyGeneralRobotics/GalbotSDK/HEAD/README.md)
- [galbot_one_golf_description (ROS 2 description package)](https://github.com/GalaxyGeneralRobotics/galbot_one_golf_description)
- [GraspVLA paper (arXiv 2505.03233)](https://arxiv.org/abs/2505.03233)
- [TechNode, 2026-08-27: Galbot's industrial AI journey](https://technode.com/2026/08/27/how-far-are-robots-from-actually-working-on-production-lines-galbots-industrial-ai-journey/)
- [Sacra: Galbot company profile](https://sacra.com/c/galbot/)
- [The Robot Report: Galbot brings in $300M](https://www.therobotreport.com/galbot-brings-in-300m-to-scale-mobile-manipulator-deployments/) (search result summary only)
- [10jqka / Changjiang Business Daily, 2026-03-05: funding and shipments](https://stock.10jqka.com.cn/20260305/c675093674.shtml) (search result summary only)
- [Gasgoo: Galbot S1 begins operations at CATL's factory](https://autonews.gasgoo.com/articles/news/2070399392245612544) (search result summary only)
