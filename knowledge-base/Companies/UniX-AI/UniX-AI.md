---
type: company
company: "UniX AI"
slug: UniX-AI
hq: "Suzhou, China"
founded: 2024
website: https://www.unix-group.ai
categories: [humanoid, mobile-manipulator, components]
on_site_guess: "Wanda 2.0 and/or Panther wheeled dual-arm service humanoids with UniPicker grippers, run with vendor engineers (best guess)"
fit_t01: 4
fit_t02: 3
fit_t03: 2
fit_t04: 4
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# UniX AI

> **One-liner:** Suzhou-based maker of mass-produced wheeled dual-arm service humanoids (Wanda 2.0, Panther) plus a bipedal humanoid (Martian) and an adaptive gripper, aimed at hotel, retail, security and household work.
> **Why it matters at Leukerbad:** Its robots are built for exactly the indoor service chores a spa resort and its clinics run on (housekeeping, tea/food service, reception, patrol), with long battery life and 12 kg dual-arm payload. The catch: **no public SDK, docs or GitHub** — what you can build in 48 hours depends on what the on-site UniX team opens up.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Suzhou Industrial Park (SIP), Suzhou, China |
| Founded | **2024** per company site and press releases (36Kr Japan says 2023 — ⚠️ unverified discrepancy) |
| Founder / CEO | Fred Yang (Yang Fengyu), born 2000; CS bachelor at University of Michigan, paused a Yale PhD in 2024 |
| Size and funding | Headcount not public. About **CNY 300M** raised in late-2025 closes (36Kr Japan, Dec 2025; investors named: Sichuan Entrepreneur Fund, Wuzhong Financial Holdings). Data aggregators list a CNY 300M Series A (Mar 2026) and a strategic investment from Keli Sensing (Aug 2026) — ⚠️ unverified; totals conflict across aggregators |
| Core business | R&D, mass production and deployment of general-purpose service humanoids; in-house arms, grippers and core components |
| Production | Mass production since 2025; company claims **100+ units/month**, target **1,000/month** |
| Website | https://www.unix-group.ai (the believed address unixai.com does not resolve) |
| Docs / developer portal | not public |
| GitHub | no official org found |
| Contact | global@unix-group.ai · business@unix-group.ai |

## Portfolio at a glance

| Product | Type | Status | Key specs (verified on official pages) | Price | Img key |
|---|---|---|---|---|---|
| **Wanda 2.0** | Wheeled dual-arm humanoid (differential-drive base) | ✅ | Height **1.40–1.68 m** (280 mm torso lift) · **23 DoF**, 8-DoF arms · **12 kg** dual-arm payload, 982 mm reach, ±0.5 mm repeatability · **1.5 m/s** · **8–16 h** battery · up to 275 TOPS compute · 360° LiDAR, RGB + RGBD head cameras, base RGBD, ultrasonic, 6-mic array · min. passage 75 cm | not public | unix-ai-wanda-2 |
| **Panther** (3rd-gen series) | Full-size wheeled dual-arm humanoid (4WS + 4WD omnidirectional base) | ✅ (launched 8 Apr 2026, deliveries started) | Height **1.62–1.72 m**, **800 mm** torso lift, works down to floor level · **34 DoF**, 8-DoF arms · **12 kg** dual-arm payload, 982 mm reach, ±0.5 mm · **2 m/s** · **4–8 h** battery · 48 V platform · optional compute up to 2070 TOPS · front/rear 360° LiDAR, dual RGB head cameras, optional 3D LiDAR and RGBD · min. passage 65 cm · dexterous-hand compatible | not public | unix-ai-panther |
| **Martian** | Bipedal humanoid | ✅ listed ("contact us"); Martian 2.0 upgrade dated Mar 2026 on company timeline (⚠️ date pairing unclear) | **148 cm**, **40 kg** · arms 7 DoF each, legs 6 DoF each, waist 3, head 2, 11-DoF dexterous hand · max 4 m/s · 5 kg payload · 150 N·m peak joint torque · 48 V / 9 Ah · depth camera, 2 RGB, IMU · CAN FD · **high- and low-level APIs for secondary development**, OTA | not public | unix-ai-martian |
| **UniPicker Pro** | Underactuated adaptive gripper | ✅ | **100 N** max grip force · up to **10 kg** payload · 0.2 s open/close · 400 g / 600 g (variants not specified) · hybrid force / velocity / position control | not public | unix-ai-unipicker-pro |
| **Wanda 3.0** | Wheeled dual-arm humanoid | 🧪 shown at CES 2026 (Jan); no specs published; likely the generation later launched as Panther (⚠️ unverified) | not public | not public | unix-ai-wanda-3 |
| **UniFlex / UniTouch / UniCortex** | Algorithm stack (imitation learning · vision-tactile model · long-horizon task planner) | ✅ on-robot; not released separately | No public weights, code or benchmarks | not public | unix-ai-algorithm-stack |

## What they will most likely bring to the hackathon

**Best guess — not confirmed by the organisers or UniX AI.**

- **Most likely: Wanda 2.0** — the volume product, the one shown at every trade fair (CES 2026, WRC 2026), and the model the company lists for research and education use.
- **Plausible: Panther** — current flagship with global deliveries; demoed doing autonomous tea-making. Heavier and newer, so fewer units if any.
- **Less likely: Martian** — the only product whose page explicitly promises development APIs, but it is rarely shown in recent demos.
- **UniPicker Pro** grippers will come mounted on the robots.
- Expect **vendor engineers and pre-loaded skills** (tea service, tidying, wiping, guiding) rather than a self-serve SDK. Ask at the booth first: what interfaces are exposed (ROS 2? Python? teleop?), and can teams record demonstrations to teach a new skill?

## Developer platform (summary)

Public information is thin. Verified points only:

- **No public SDK, documentation portal or GitHub org** was found. One third-party humanoid database describes the control software as closed-source (⚠️ unverified, single source).
- **Martian**: official page states high-level and low-level API interfaces for secondary development, CAN FD bus, OTA updates. Languages not public.
- **Wanda 2.0 / Panther**: pages mention pre-loaded "L4-level" applications and "fast learning and rapid deployment"; no API, ROS 2 or language details are published.
- **Skill learning**: UniFlex is an imitation-learning framework using multimodal semantic keypoints and trajectory imitation — this implies demonstration-based teaching, but the teleoperation / data-collection tooling is not public.
- **Perception / planning**: UniTouch (vision-tactile model) and UniCortex (long-sequence task planner) run on the robots; no downloadable models.
- **On-board compute**: Wanda 2.0 up to 275 TOPS; Panther optional up to 2070 TOPS; Martian "40T" platform with 32 GB RAM. Chip vendors not public.
- **Sensors usable for your own stack (if raw access is granted)**: 360° LiDAR, RGB / RGBD cameras, 6-mic array, speakers.
- **ROS 2, simulation assets (URDF / MJCF / Isaac), datasets**: not public.
- Practical consequence: plan a project that composes **existing robot skills + navigation + your own perception / LLM layer on an external laptop**, and confirm the interface on site before committing.

## Current projects, deployments and customers

- **Aug 2025** — Wanda series won 2 golds and 1 silver (hotel room service, reception) at the World Humanoid Robot Games, Beijing ([36Kr Japan](https://36kr.jp/449686/), [About page](https://www.unix-group.ai/About-Unix-AI)).
- **Dec 2025** — Reported ~100 units/month shipped, order backlog above 1,000 units; customers in hotels, property management, security, retail, food and beverage ([36Kr Japan](https://36kr.jp/449686/)). Customer names not public.
- **Jan 2026** — CES 2026: Wanda 2.0 and 3.0 demos — drink mixing, tea-making, dishwashing, clothes organising, bed-making, amenity restocking, **waste sorting** ([press release](https://www.webull.com/news/14134140025406464)).
- **31 Mar 2026** — Autonomous tea-making demo at the Morgan Stanley China Summit, Shenzhen ([Panther release](https://technode.global/prnasia/unix-ai-introduces-panther-the-worlds-first-service-humanoid-robot-to-enter-real-household-deployment-powered-by-its-differentiated-wheeled-dual-arm-architecture/)).
- **8 Apr 2026** — Panther launched; company claims first real-household deployment of a mass-produced service humanoid (Suzhou) and orders worth "hundreds of millions of yuan" (same release; company claims, not independently verified).
- **20 Aug 2026** — WRC 2026, Beijing: four Wanda 2.0 robots played as a band; Panther brewed tea; Panther reported as deployed with **JD.com Seven Fresh Coffee** in a 24-hour unmanned store ([WRC report](https://www.itiger.com/news/1101359561); source is unreviewed event notes).
- **Elder care** — listed as a target application for Panther and Martian and as a (placeholder) menu item on the website; **no named elder-care deployment found**.
- **Europe / Switzerland** — no deployments found. Exhibitor listing for IFA Berlin (IFA Next, Hall 25) exists ([IFA](https://www.ifa-berlin.com/exhibitors/unix-ai)).

## Roadmap and future direction

- **2026** — Production target of **1,000 units/month** (Apr 2026 release). 🔭
- **2026** — Strategy stated as productisation, globalisation and ecosystem building; Panther "global deliveries" started (Apr 2026). ✅ / 🔭
- **2026** — Deliberate bet on **wheeled dual-arm** over bipedal for usability and deployment speed; household use is the headline next market. 
- **Mar 2026** — Martian 2.0 upgrade listed on the company timeline (⚠️ date pairing unclear). 🧪
- **Mar / Aug 2026** — Series A (CNY 300M) and Keli Sensing strategic investment reported by data aggregators only. ⚠️ unverified
- **Sep 2027** — Listed as IFA Berlin 2027 exhibitor (IFA Next). 🔭
- Developer programme, open SDK or model release: **nothing announced**.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | **4** | Proven in hotel housekeeping, reception, retail and food service; indoor flat floors only — not for Leukerbad's streets, slopes or snow | Wanda 2.0, Panther | [T01 brief](T01-Autonomous-Urban-Services/UniX-AI-T01-1-Brief.md) |
| T02 Resilient & Safe City | **3** | Security patrol is a claimed deployment; LiDAR + cameras + arms allow indoor inspection and simple interventions, but no rough-terrain or hazard capability | Wanda 2.0, Panther | [T02 brief](T02-Resilient-and-Safe-City/UniX-AI-T02-1-Brief.md) |
| T03 Sustainable City | **2** | Only a waste-sorting demo skill and long battery life; supporting role (sorting, restocking) in a multi-vendor system | Panther, UniPicker Pro | [T03 brief](T03-Sustainable-City/UniX-AI-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | **4** | Household chores, tea/meal service, floor-level pick-up and voice interaction map directly to assisted living; marketed for elder care but no proven care deployment | Panther, Wanda 2.0 | [T04 brief](T04-Elderly-Care-and-Rehabilitation/UniX-AI-T04-1-Brief.md) |

Scores assume the on-site team exposes a usable control interface; with skills-only access, drop each by about one point.

## Related docs
- [Product portfolio](UniX-AI-Products.md) · [Developer guide](UniX-AI-Developer-Guide.md) · [Roadmap and strategy](UniX-AI-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [UniX AI official site](https://www.unix-group.ai)
- [Wanda 2.0 product page](https://www.unix-group.ai/Wanda)
- [Panther product page](https://www.unix-group.ai/Panther)
- [Martian product page](https://www.unix-group.ai/Martian)
- [UniPicker Pro product page](https://www.unix-group.ai/UniPicker)
- [About UniX AI](https://www.unix-group.ai/About-Unix-AI)
- [Press release, 2 Jan 2026: Wanda 2.0 at CES 2026 (via Webull / PR Newswire)](https://www.webull.com/news/14134140025406464)
- [Press release, 8 Apr 2026: Panther launch (via TechNode Global / PR Newswire Asia)](https://technode.global/prnasia/unix-ai-introduces-panther-the-worlds-first-service-humanoid-robot-to-enter-real-household-deployment-powered-by-its-differentiated-wheeled-dual-arm-architecture/)
- [36Kr Japan, 21 Dec 2025: funding and shipments](https://36kr.jp/449686/)
- [WRC 2026 live report, 20 Aug 2026 (iTiger)](https://www.itiger.com/news/1101359561)
- [IFA Berlin exhibitor profile](https://www.ifa-berlin.com/exhibitors/unix-ai)
- [Preqin asset profile (funding rounds, seen via search summary only)](https://www.preqin.com/data/profile/asset/unix-ai/744996)
- [Humanoid.press database entry for Wanda 2.0 (closed-source note)](https://humanoid.press/database/humanoid-press-database-wanda-2-0/)
- [UniX AI on LinkedIn](https://www.linkedin.com/company/unix-ai/)
