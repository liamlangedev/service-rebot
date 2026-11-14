---
type: company
company: "XREAL"
slug: XREAL
hq: "Beijing, China"
founded: 2017
website: https://www.xreal.com
categories: [xr, sensors, software]
on_site_guess: "One-series AR glasses (One Pro / 1 Pro+ / 1S) with XREAL Eye camera and Beam Pro host; possibly AURA Android XR units and legacy Air 2 Ultra dev glasses"
fit_t01: 2
fit_t02: 3
fit_t03: 2
fit_t04: 3
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# XREAL

> **One-liner:** XREAL (formerly Nreal) makes lightweight tethered AR glasses — a see-through wearable display with head tracking, plus (on some models) 6DoF, hand tracking and an Android XR compute puck.
> **Why it matters at Leukerbad:** XREAL is not a robot — it is the **human interface layer**: an operator HUD, a hands-free instruction overlay for a patient or technician, or a head-pose / hand-pose input device for teleoperation. Pair it with another vendor's robot.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Beijing, China (per trade press; the official About page does not state HQ) |
| Founded | **2017** as Nreal; renamed XREAL in 2023 |
| Founders / CEO | Founder and CEO Dr. Chi Xu (Xu Chi), with co-founders |
| Size and funding | Headcount: not public. **USD 100M** round announced Jan 2026; about **USD 433M** raised in total (Crunchbase figure via GamesBeat). Reported valuation USD 0.83–1B ⚠️ unverified. 2025 revenue about **RMB 516M** (+30.8% YoY, >70% overseas) per IPO-filing coverage. HKEX main-board listing application filed **1 Apr 2026**; listing outcome not confirmed |
| Core business | Consumer AR / display glasses, own spatial chips (X1, X1S), Android XR glasses with Google. Claims No. 1 in global AR-glasses revenue 2022–2025 (iResearch, company-cited) |
| Website | https://www.xreal.com |
| Docs / developer portal | https://docs.xreal.com (XREAL SDK) · https://developer.xreal.com (downloads) · Android XR docs for AURA: https://developer.android.com/develop/xr |
| GitHub | https://github.com/nreal-ai (legacy Nreal-named org, linked from the official docs) |

## Portfolio at a glance

| Product | Type | Status | Key specs (verified unless marked) | Price (if public) | Img key |
|---|---|---|---|---|---|
| XREAL AURA (ex Project Aura) | Android XR optical see-through glasses + tethered compute puck | ✅ launched 28 Oct 2026; first batch ships mid-Nov 2026 (US, CA, JP, KR — **Europe later**) | **70° FOV** · 1920×1200 per eye, up to 120 Hz · **6DoF inside-out + hand tracking** · AI camera · glasses **<95 g** · puck: Snapdragon Reality Elite + X1S, 4,455 mAh · Gemini built in | **USD 1,279** (12/256) · USD 1,499 (16/512); launch promo USD 1,099 / 1,299 to Dec 2026 | xreal-aura |
| XREAL 1 Pro+ | Tethered AR display glasses (flagship One series) | ✅ since 15 Oct 2026 | **57° FOV** · **1,200 nits** peak · X1 chip, native 3DoF · 60 Hz 2D-to-3D conversion · weight not published | **USD 599** | xreal-1-pro-plus |
| XREAL One Pro | Tethered AR display glasses | ✅ (still listed; superseded by 1 Pro+) | **57° FOV** · 700 nits · X1 chip, native 3DoF, about 3 ms motion-to-photon · **87 g** · 6DoF only with XREAL Eye | USD 599 (launched at 649) | xreal-one-pro |
| XREAL 1S | Tethered AR display glasses (entry One series) | ✅ since Jan 2026 | 1920×1200 (16:10) · X1 chip, native 3DoF · about **82 g** · FOV ⚠️ unverified | **USD 449** (seen at 399 on sale) | xreal-1s |
| ROG XREAL R1 | Gaming AR glasses (with ASUS ROG) | ✅ pre-orders opened 2026; ship date ⚠️ unverified | **240 Hz** dual 1920×1080 micro-OLED · **57° FOV** · 91 g | about **USD 849** | xreal-rog-r1 |
| XREAL Eye | Clip-in camera module for One series | ✅ | Adds **6DoF** tracking to One-series glasses (SDK 3.1.0+) · POV photo / video · sensor resolution ⚠️ unverified | **USD 99** | xreal-eye |
| XREAL Beam Pro | Android handheld host / spatial camera (phone-like) | ✅ | Runs MyGlasses + XREAL SDK apps · one of the two officially tested SDK hosts · dual cameras for spatial capture | from **USD 199** | xreal-beam-pro |
| XREAL Neo | Battery + video hub accessory | ✅ since Feb 2026 | Power bank and display hub for the glasses (e.g. handheld consoles) | USD 119 (99 launch) | xreal-neo |
| xbx a01+ | Budget sub-brand display glasses | ✅ listed in site navigation; details ⚠️ unverified | Sub-brand "XBX" reported to start with a USD 299 A01; "a01+" specs not confirmed | not confirmed | xreal-xbx-a01-plus |
| XREAL Air 2 Ultra | Developer-oriented 6DoF AR glasses (legacy) | ✅ shipped Mar 2024; no longer in main site navigation | Native **6DoF** (two SLAM cameras) + hand tracking · the SDK "6DoF glasses" reference device | USD 699 at launch | xreal-air-2-ultra |

Quick capability map for builders:

| Need | Works on |
|---|---|
| Just a big private screen / HUD (USB-C DisplayPort) | Every model — plug into laptop, phone, Jetson-class board with DP Alt Mode ⚠️ check your host port |
| 3DoF head-locked / world-anchored screen without software | One Pro, 1 Pro+, 1S, R1 (X1 chip on glasses) |
| 6DoF + hand tracking + planes / anchors via XREAL SDK | Air 2 Ultra; One series **with XREAL Eye** (6DoF confirmed; hand-tracking support on One + Eye ⚠️ unverified) |
| Standalone Android XR apps, Gemini, Play Store | AURA only |

## What they will most likely bring to the hackathon

**Best guess (not confirmed):**

- **One-series glasses (One Pro / 1 Pro+ / 1S) + XREAL Eye + Beam Pro** — the volume products, cheap to hand out, and the combination the current SDK (3.1.0) explicitly targets for 6DoF.
- **A few AURA units** are plausible because it launched two weeks ago and XREAL / Google run an Android XR developer early-access programme — but AURA is not yet sold in Europe, so expect limited numbers if any.
- **Air 2 Ultra** may appear as the classic developer device (native 6DoF + hand tracking without add-ons).
- Ask at the booth first: (1) which glasses, (2) which host device (Beam Pro or Samsung S24 / S25 class phone), (3) whether camera frames are accessible, (4) whether a ready Unity sample is provided.

## Developer platform (summary)

- **XREAL SDK 3.1.0** (released 25 Nov 2025) — a **Unity** package (Unity 2021.3+), built on Unity XR Plugin, **AR Foundation**, **XR Interaction Toolkit** and **XR Hands**; replaces the older proprietary NRSDK (2.x). C# only; no official Unreal, native C++ or Python SDK found.
- **Features:** 6DoF tracking (two SLAM cameras + IMU), plane detection, image tracking, hand tracking (**26 joints**, OpenXR-aligned), depth mesh, spatial anchors (persistent and shareable), phone-as-3DoF-controller. MRTK3 integration is documented.
- **Hosts:** apps run on an **Android host** — officially tested on **Beam Pro and Samsung S25** (S24-and-later flagships listed). Docs warn **not to upgrade dev devices to Android 16** (compatibility issues under investigation).
- **AURA is a different stack:** Android XR. Unity 6.5 with the Android XR OpenXR package, XR Hands, AR Foundation; hand tracking, planes, anchors, marker tracking and puck-trackpad input supported; **no eye tracking**. Standard Android apps also run from the Play Store.
- **No-code path:** every model works as a plain USB-C external display — the fastest 48-hour route is to render your operator UI on a laptop / robot computer and show it in the glasses.
- **ROS 2:** no official ROS 2 package found. Realistic path: Unity app + a Unity-to-ROS bridge (e.g. ROS-TCP-Connector or a WebSocket / UDP pose stream) publishing head and hand poses. Community XR-teleop projects exist but target Quest / Pico, not XREAL.
- **Camera access caveat:** a 2026 research paper (ActiveGlasses) reports that XREAL did not expose raw camera frames on Air 2 Ultra, so the authors mounted a separate stereo camera. Whether XREAL Eye / AURA frames are available to apps: ⚠️ unverified — check on site.
- **Simulation assets / datasets / foundation models:** none published by XREAL for robotics. AURA ships Gemini on-device as the assistant.
- **On-board compute:** One-series glasses have only the X1 display / tracking co-processor (no app compute). AURA puck: Snapdragon Reality Elite (up to 48 TOPS).
- Links: [docs](https://docs.xreal.com/) · [SDK downloads](https://developer.xreal.com/download) · [GitHub](https://github.com/nreal-ai) · [Android XR + Unity](https://developer.android.com/develop/xr/unity)

## Current projects, deployments and customers

- **2026-10-28** — XREAL AURA, the first Android XR optical see-through glasses, launched; first batch ships mid-November in US, Canada, Japan, South Korea; 150+ XR apps at launch ([Road to VR](https://www.roadtovr.com/google-ar-glasses-xreal-aura-release-date-price/)).
- **2026-10-15** — XREAL 1 Pro+ on sale at USD 599 ([Road to VR](https://roadtovr.com/xreal-1-pro-plus-release-date-price/), [Android Authority](https://androidauthority.com/xreal-1-pro-plus-ar-glasses-launched-3723563)).
- **2026-06-16** — Unity announced AURA support (Unity 6.5, Android XR packages) ([Unity blog](https://unity.com/blog/unity-android-xr-wired-glasses-support)).
- **2026-05-19** — Google I/O: Android XR developer early-access programme for Project Aura hardware ([9to5Google](https://9to5google.com/2026/05/19/xreal-project-aura-android-xr-developers-2026-launch/)).
- **2026-04** — Research use in robotics: "ActiveGlasses" (arXiv 2604.08534) uses XREAL Air 2 Ultra 6DoF head pose plus a stereo camera to collect egocentric manipulation demonstrations and replay active vision on a 6-DoF arm ([arXiv](https://arxiv.org/pdf/2604.08534)). This is academic work, not an XREAL product.
- **2026-01 (CES)** — XREAL 1S, Neo hub and the ASUS co-developed ROG XREAL R1 announced ([Android Central](https://www.androidcentral.com/gaming/virtual-reality/xreal-1s-brings-1200p-visuals-and-a-lower-price-to-the-best-ar-glasses), [Engadget](https://www.engadget.com/gaming/pc/asus-and-xreal-teamed-up-at-ces-to-make-gaming-smartglasses-with-two-important-upgrades-190500897.html)).
- **Partners:** Google (Android XR), Qualcomm (AURA chipset), ASUS ROG (R1), Bose (audio), Unity.
- **Track-relevant deployments** (city services, safety, sustainability, elderly care): none found in public sources. The business is consumer entertainment / productivity.

## Roadmap and future direction

- **2026-01** — USD 100M funding round, stated purpose: accelerate AR glasses rollout ([GamesBeat](https://gamesbeat.com/xreal-raises-100m-to-accelerate-ar-glasses-rollout/)).
- **2026-04-01** — Hong Kong main-board IPO application (sponsors CICC, Citi); aims to be the first listed smart-glasses pure play. Listing completion not confirmed as of this writing ([UC Today](https://www.uctoday.com/devices-workspace-tech/xreal-files-for-hong-kong-ipo-as-smart-glasses-race-intensifies/)).
- **Late 2026 → 2027** — 🧪 AURA European availability "soon after" the first wave; 2027 retail expansion incl. select Google Store locations (US, Japan).
- **Strategy** — two lines: affordable display glasses with in-house spatial chips (One series, XBX budget brand) and a premium Android XR / Gemini line (AURA). CEO positions AI as the driver for smart glasses ([Caixin](https://www.caixinglobal.com/2026-06-03/xreal-founder-bets-ai-will-push-smart-glasses-beyond-hype-102450675.html)).
- **Robotics-specific roadmap:** not public. No announced robotics SDK, teleoperation product or embodied-AI data programme.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 2 | Supporting role: fleet-supervisor HUD or remote-takeover view for a delivery / maintenance robot | One Pro / 1 Pro+ as display; AURA for standalone app | [T01 brief](T01-Autonomous-Urban-Services/XREAL-T01-1-Brief.md) |
| T02 Resilient & Safe City | 3 | Hands-free operator view for a quadruped / drone in hazard response; head-pose camera control; remote-expert overlay | One series + Eye (6DoF), AURA | [T02 brief](T02-Resilient-and-Safe-City/XREAL-T02-1-Brief.md) |
| T03 Sustainable City | 2 | Supporting role: AR guidance for sorting / inspection or visualising sensor data on site | One series as display; AURA | [T03 brief](T03-Sustainable-City/XREAL-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 3 | Light glasses (82–95 g) suit therapist or patient: exercise cues, robot-status overlay, caregiver teleassist of an assistive robot | 1S / One Pro + Eye, AURA (hand tracking) | [T04 brief](T04-Elderly-Care-and-Rehabilitation/XREAL-T04-1-Brief.md) |

Decision note: choose XREAL as an **add-on**, never as the core platform. Fastest win = glasses as an external display for a UI you already have; budget at least half a day if you want 6DoF / hand tracking through Unity.

## Related docs
- [Product portfolio](XREAL-Products.md) · [Developer guide](XREAL-Developer-Guide.md) · [Roadmap and strategy](XREAL-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [XREAL — About](https://www.xreal.com/about)
- [XREAL developer docs (SDK 3.1.0)](https://docs.xreal.com/)
- [XREAL SDK 3.1.0 release note](https://docs.xreal.com/Release%20Note/XREAL%20SDK%203.1.0)
- [XREAL SDK 3.0.0 release note](https://docs.xreal.com/Release%20Note/XREAL%20SDK%203.0.0)
- [XREAL docs — Hand Tracking](https://docs.xreal.com/Input%20and%20Interactions/Hand%20Tracking)
- [XREAL developer downloads](https://developer.xreal.com/download)
- [XREAL US store — all products](https://us.shop.xreal.com/collections/all)
- [Road to VR — XREAL Aura launch and pricing (28 Oct 2026)](https://www.roadtovr.com/google-ar-glasses-xreal-aura-release-date-price/)
- [9to5Google — XREAL Aura starts at USD 1,279](https://9to5google.com/2026/10/07/xreal-aura-with-android-xr-start-at-1279/)
- [9to5Google — Project Aura developer programme (Google I/O 2026)](https://9to5google.com/2026/05/19/xreal-project-aura-android-xr-developers-2026-launch/)
- [Unity blog — Unity support for XREAL AURA](https://unity.com/blog/unity-android-xr-wired-glasses-support)
- [Android Developers — Develop with Unity for Android XR](https://developer.android.com/develop/xr/unity)
- [Road to VR — XREAL 1 Pro+ launch](https://roadtovr.com/xreal-1-pro-plus-release-date-price/)
- [Android Authority — XREAL 1 Pro+ launched](https://androidauthority.com/xreal-1-pro-plus-ar-glasses-launched-3723563)
- [Mixed News — XREAL 1 Pro+ details](https://mixed-news.com/en/xreal-1-pro-plus-599-dollars-1200-nits-one-pro-still-listed/)
- [Android Central — XREAL 1S](https://www.androidcentral.com/gaming/virtual-reality/xreal-1s-brings-1200p-visuals-and-a-lower-price-to-the-best-ar-glasses)
- [Ubergizmo — XREAL 1S review and specs](https://www.ubergizmo.com/reviews/xreal-1s-review-specs-weight-price-and-how-it-compares-to-the-xreal-one)
- [Engadget — ASUS and XREAL ROG R1 at CES 2026](https://www.engadget.com/gaming/pc/asus-and-xreal-teamed-up-at-ces-to-make-gaming-smartglasses-with-two-important-upgrades-190500897.html)
- [ASUS ROG — ROG XREAL R1 specs](https://rog.asus.com/glasses/rog-xreal-r1/spec/)
- [Road to VR — ROG XREAL R1 pre-orders](https://roadtovr.com/rog-xreal-r1-pre-orders-now-live-240hz-microoled-gaming-glasses-priced-at-850/)
- [Tom's Hardware — XREAL One series and X1 chip](https://www.tomshardware.com/peripherals/wearable-tech/hands-on-xreal-one-series-ar-glasses-announced-with-custom-x1-spatial-chip-more-customization-and-wider-fov)
- [GamesBeat — XREAL raises USD 100M](https://gamesbeat.com/xreal-raises-100m-to-accelerate-ar-glasses-rollout/)
- [UC Today — XREAL files for Hong Kong IPO](https://www.uctoday.com/devices-workspace-tech/xreal-files-for-hong-kong-ipo-as-smart-glasses-race-intensifies/)
- [Caixin Global — XREAL founder interview (Jun 2026)](https://www.caixinglobal.com/2026-06-03/xreal-founder-bets-ai-will-push-smart-glasses-beyond-hype-102450675.html)
- [arXiv 2604.08534 — ActiveGlasses](https://arxiv.org/pdf/2604.08534)
