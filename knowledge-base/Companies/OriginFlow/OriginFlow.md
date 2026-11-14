---
type: company
company: "OriginFlow"
slug: OriginFlow
hq: "Beijing, China"
founded: 2025
website: https://www.originflow.ai/
categories: [data, sensors, software]
on_site_guess: "OriginKitGen 1.0 capture kits (Glass + Band + Space) and a live PULSE hand-pose / fingertip-force demo from the 16-channel sEMG wristband"
fit_t01: 2
fit_t02: 2
fit_t03: 1
fit_t04: 3
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# OriginFlow

> **One-liner:** Beijing start-up (Chinese name 渊澈太初) that captures human manipulation data with a wearable kit built around a **16-channel surface-EMG wristband**, and turns it into pose / force / contact data for training robots.
> **Why it matters at Leukerbad:** It is not a robot vendor. It is the one company on site that senses **muscle activity and estimated hand force**, which makes it an input device or a data source for someone else's arm, hand or humanoid — and the only vendor with a natural link to rehabilitation sensing (T04).

**Read this first:** public information is thin. There is **no public SDK, docs portal, GitHub org, open dataset or downloadable model** as of 2026-11-14. What you can build depends entirely on what interface the OriginFlow team exposes on site. Ask them before committing.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Beijing, China |
| Founded | **August 2025** (official site says "founded in 2025") |
| Founder / CEO | Qin Shentao (秦深涛), born 2001; PhD candidate, Tsinghua University School of Vehicle and Mobility; BSc Harbin Institute of Technology (mechatronics) |
| Size and funding | Headcount not public. **> RMB 500M** over angel, strategic and Pre-A1 rounds, announced 2026-05-21. Investors: BlueRun Ventures China (Lanchi), Oasis Capital (VitalBridge), 58 Strategic Investment, Puhua Capital, Shuimu Tsinghua seed alumni fund, Monolith Capital (Pre-A1 lead) |
| Core business | Multimodal human-interaction capture hardware + data-capture services + models that reconstruct pose, force and contact from sEMG ("NeuroScale" approach, "Human Tokens" representation) |
| Website | https://www.originflow.ai/ (single-page site; contact: contact@originflow.ai) |
| Docs / developer portal | not public |
| GitHub | none found ⚠️ unverified (no official org located) |

## Portfolio at a glance

| Product | Type | Status | Key specs (verified) | Price | Img key |
|---|---|---|---|---|---|
| **OriginKitGen 1.0** (full kit) | Wearable multimodal capture kit = Glass + Band + Space | ✅ offered via enquiry (official site) | Three devices; synchronised first-person video, head motion, wrist motion and **16-channel sEMG** on one timeline; local recording; 5-step workflow (setup, calibration, capture, status, preview) | Not public. Press reports capture equipment at roughly **RMB 1,000 per set** ⚠️ unverified | originflow-originkit-gen1 |
| **Band** (part of OriginKitGen 1.0) | sEMG wristband + wrist motion (IMU) | ✅ | **16 channels**, microvolt-level surface EMG; data stream about **96 KB/s**; strap slightly wider than an Apple Watch band, lighter overall. Sampling rate not public | not public | originflow-band |
| **Glass** (part of OriginKitGen 1.0) | Head-worn first-person camera + head motion | ✅ | Egocentric video + head motion. Resolution, FoV, frame rate not public | not public | originflow-glass |
| **Space** (part of OriginKitGen 1.0) | Control and local-recording unit | ✅ | Device status, capture workflow control, local storage, operator feedback. Compute, storage, battery not public | not public | originflow-space |
| **Data Capture Services** | Service: real-world task capture for robotics / Physical-AI teams | ✅ (listed on official site) | Outputs span video, semantics, pose and force. Volumes, formats, licence not public | not public | originflow-data-services |
| **PULSE** | Foundation model: sEMG to hand pose, contact force, actuation force | 🧪 v0.2 demoed at WAIC 2026; v0.3 in development | v0.2: continuous hand tracking + fingertip-force estimation from 16-channel sEMG. No public weights or API | not public | originflow-pulse |
| **CHORD** | Omni-modal base model aligning sEMG, vision, IMU, language, robot state | 🧪 described in press only | No public specs | not public | originflow-chord |
| **ORACLE** | Auto-annotation system (action, force, semantics, task segments) | 🧪 internal data infrastructure | No public specs | not public | originflow-oracle |

Notes:
- "NeuroScale" is the name of the overall method (capture, physical-quantity reconstruction, action representation, cross-embodiment transfer), not a product you can buy.
- "Human Tokens" = their representation in three spaces: **MotionSpace** (hand pose, trajectory), **TactileSpace** (normal / tangential force, contact), **TendonSpace** (muscle-tendon drive force, joint torque).
- The official site states that pose, intent, force and contact are **estimated** "under defined algorithms, calibration and task conditions" — treat force output as an estimate, not a measurement.
- No data glove, no robot, no dexterous hand of their own.

## What they will most likely bring to the hackathon

**Best guess (not confirmed by the company):**

| Likely item | Confidence | Reasoning |
|---|---|---|
| Several **OriginKitGen 1.0** kits (Glass + Band + Space) | High | It is their only hardware product and the whole site is built around it |
| Live **PULSE** demo: hand tracking + fingertip force from the wristband | Medium-high | This is exactly what they showed at WAIC 2026 |
| Staff-run **data capture / export** of your recorded sessions | Medium | Their business is capture services; self-service tooling is not documented |
| A real-time stream API (hand pose / force) for teams to drive a robot | **Unknown** | Nothing public. This is the single most important question to ask at their booth |
| Teleoperation of a dexterous hand via EMG | Low-medium | Plausible given the LinkerBot partnership, but LinkerBot is not on the vendor list; would need mapping onto WUJI / Unitree Dex hands on site |

Questions to ask in the first five minutes:
1. Can we get a **live stream** (UDP / WebSocket / ROS 2 topic) of raw sEMG and of PULSE outputs? At what rate and latency?
2. How long is **per-user calibration**?
3. What **export format** do recordings use, and can we take the data away?
4. Does the Band work standalone (without Glass and Space)?

## Developer platform (summary)

- **SDK / languages:** not public. No documented Python, C++ or ROS 2 interface.
- **Control level:** not applicable — sensing and data, no actuators. Any robot control is your own bridge code to another vendor's SDK.
- **ROS 2:** not public ⚠️ unverified. Plan to write a small bridge node yourself if a stream is available.
- **Simulation assets:** none public.
- **Teleoperation / data collection:** this is the core use. Kit records synchronised egocentric video, head and wrist motion and 16-channel sEMG; Space handles device status, local recording and timeline preview.
- **Pretrained models:** PULSE (pose + force from sEMG), CHORD, ORACLE exist per press coverage; **no public weights, API or model card**.
- **Datasets:** company describes large-scale human data plus smaller cross-embodiment robot data; **nothing openly released**.
- **On-board compute:** Space unit specs not public. Assume you need your own laptop or an edge board (for example a D-Robotics RDK) for inference and robot control.
- **Fallback if no API is offered:** use the kit as a demonstration recorder (video + motion + EMG) and train or script from exported files — only feasible if export is possible within the 48 hours.
- **Links:** official site https://www.originflow.ai/ — docs and GitHub: not public.

## Current projects, deployments and customers

- **2026-05-21** — Announced > RMB 500M across three rounds within about five months of operation; stated commercial focus on two scenarios: **industrial manufacturing** and **home services** ([TMTPost](https://en.tmtpost.com/post/7997613)).
- **2026-05-21** — **58 Group** (strategic investor) partnering on home-service data capture: clothes organising, household cleaning, kitchen work, aimed at a skills database for housekeeping robots ([TMTPost](https://en.tmtpost.com/post/7997613)).
- **2026-05-21** — Industrial data capture with unnamed "leading global high-end manufacturers"; names not public ([TMTPost](https://en.tmtpost.com/post/7997613)).
- **2026 (exact date ⚠️ unverified)** — Strategic partnership with **LinkerBot** (dexterous hands): joint work on data acquisition, system adaptation, commercial operation and standards; EMG-decoded motion and tactile data intended to map onto dexterous hands ([Gasgoo](https://autonews.gasgoo.com/articles/news/2089539854819147777) — page could not be opened directly; details from search summary).
- **2026-07 (WAIC 2026)** — Demoed **PULSE 0.2**: continuous hand tracking and fingertip-force readout during pinch gestures from the 16-channel wristband ([QbitAI](https://www.qbitai.com/2026/08/477094.html)).
- **Europe / Switzerland:** no public activity found before this hackathon.
- **Independent validation:** none found. Performance claims are company-sourced.

## Roadmap and future direction

- **Three-stage plan (stated 2026-08):** (1) *From Human* — capture and distil human motor skill into machine-learnable data (current); (2) *With Human* — next-generation always-on AI hardware, including robots 🔭; (3) *Enhance Human* — 10 to 30 year horizon 🔭 ([QbitAI](https://www.qbitai.com/2026/08/477094.html)).
- **PULSE 0.3** 🧪 in development: tendon force and hand forward kinematics (2026-08).
- **Two long-term priorities:** scale up human data (stated ambition: from tens or hundreds of millions of hours toward a trillion hours) and human-to-robot cross-embodiment transfer.
- **Hardware direction:** the wristband is described as a current capture terminal, not the final form; future capture through everyday devices such as glasses, watches or bracelets 🔭.
- **Future markets named:** robotics, smart hardware, **medical rehabilitation**, spatial computing 🔭 ([TMTPost](https://en.tmtpost.com/post/7997613)).
- **Positioning:** sEMG presented as a complement to UMI-style and egocentric-video data collection, not a replacement.
- **Funding:** Pre-A1 closed by May 2026; no later round found as of 2026-11-14.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | **2** | Supporting role: record human demonstrations or teleoperate another vendor's manipulator; no mobility or actuation of its own | OriginKitGen 1.0, PULSE | [T01 brief](T01-Autonomous-Urban-Services/OriginFlow-T01-1-Brief.md) |
| T02 Resilient & Safe City | **2** | Hands-busy gesture / force input for remote operation of a robot in a hazard zone, if a live stream is available | Band, Glass | [T02 brief](T02-Resilient-and-Safe-City/OriginFlow-T02-1-Brief.md) |
| T03 Sustainable City | **1** | Only indirect: capture sorting / repair skills as training data; no clear 48-hour demo | Data Capture Services | [T03 brief](T03-Sustainable-City/OriginFlow-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | **3** | sEMG + estimated grip force suits rehab-exercise feedback or intent-driven assistive control; company names rehabilitation as a future market, but it is not a medical device and has no proven care deployment | Band, PULSE | [T04 brief](T04-Elderly-Care-and-Rehabilitation/OriginFlow-T04-1-Brief.md) |

Cross-vendor pairings worth considering: Band + PULSE driving a **WUJI Hand** or Unitree Dex hand (EMG teleoperation); Band as muscle-effort feedback next to a **Flexiv / ROKAE** force-controlled arm for assisted rehab motion; Glass + **XREAL** for operator view. All depend on a live data interface being available.

## Related docs
- [Product portfolio](OriginFlow-Products.md) · [Developer guide](OriginFlow-Developer-Guide.md) · [Roadmap and strategy](OriginFlow-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [OriginFlow official site](https://www.originflow.ai/)
- [OriginFlow on LinkedIn](https://www.linkedin.com/company/originflow/) (identity reference given by organisers; not opened)
- [TMTPost (EN), 2026-05-21 — Tsinghua PhD student raises over 500 million yuan in five months](https://en.tmtpost.com/post/7997613)
- [QbitAI, 2026-08-22 — interview / profile of OriginFlow (Chinese)](https://www.qbitai.com/2026/08/477094.html)
- [36Kr Europe (EN), 2026-08-24 — republished QbitAI profile](https://eu.36kr.com/en/p/3950735048031365)
- [BAAI Community, 2026-08-24 — republished QbitAI profile (Chinese)](https://hub.baai.ac.cn/view/57413)
- [Gasgoo — LinkerBot and OriginFlow build new data foundation for embodied intelligence](https://autonews.gasgoo.com/articles/news/2089539854819147777) (search summary only)
- [Gasgoo — OriginFlow closes over 500 million yuan financing](https://autonews.gasgoo.com/articles/news/seeds-originflow-closes-over-500-million-yuan-financing-2057790878016532480) (search summary only)
