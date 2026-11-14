---
type: roadmap
company: "OriginFlow"
slug: OriginFlow
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# OriginFlow — Roadmap and Strategy

⬆ [OriginFlow profile](OriginFlow.md) · [Product portfolio](OriginFlow-Products.md) · [Developer guide](OriginFlow-Developer-Guide.md)

> **In one line:** a 15-month-old, well-funded Beijing data-infrastructure start-up betting that **muscle signals (sEMG) + egocentric vision** are the cheapest way to capture human manipulation skill — including force — at very large scale.
> Research note: search-engine queries were unavailable for this pass, so news after August 2026 comes only from direct reads of official pages (site, Hugging Face, GitHub). A later funding round or partnership could exist and be missed.

## Company trajectory

| Date | Milestone | Source |
|---|---|---|
| 2025-08 | Founded in Beijing by Qin Shentao (born 2001, Tsinghua PhD candidate) | QbitAI / 36Kr |
| late 2025 – 2026-05 | Three rounds in about five months: angel (co-led by Lanchi / BlueRun China and VitalBridge / Oasis), strategic (58 Strategic Investment, Puhua Capital, Shuimu Tsinghua seed alumni fund), Pre-A1 (led by Monolith Capital) | TMTPost |
| 2026 (exact date ⚠️ unverified) | Strategic partnership with dexterous-hand maker LinkerBot (data acquisition, system adaptation, standards) | Gasgoo, via profile — page could not be re-opened |
| 2026-04 | Earliest visible activity in the `OriginFlow-AI` GitHub org (visual-odometry fork) ⚠️ affiliation unverified | GitHub |
| **2026-05-21** | Funding made public: **> RMB 500M** total; commercial focus named as industrial manufacturing and home services; 58 Group home-service data collaboration | TMTPost |
| 2026-07 | **PULSE 0.2** live demo at WAIC 2026: continuous hand tracking + fingertip force from the 16-channel wristband | QbitAI |
| 2026-08-22 | Founder interview: NeuroScale stack (PULSE, CHORD, ORACLE, Human Tokens), three-stage plan, PULSE 0.3 in development | QbitAI / 36Kr |
| about 2026-09 ⚠️ approximate | **OriginData preview sample** published on Hugging Face (gated): 100.62 h, 7,717 episodes | Hugging Face |
| 2026-10-20 | Dataset update: contact-masked force values | Hugging Face commit log |
| about 2026-10-30 | Dataset update: CHORD vs VLM annotation-quality report added | Hugging Face commit log |
| 2026-11-11 | Official website (re)published around **OriginKitGen 1.0** (Glass + Band + Space) | originflow.ai |
| 2026-11-12 | Field-capture force-calibration experiments logged (MAE 6.53 N → 3.26 N on one test set) ⚠️ affiliation unverified | GitHub |
| 2026-11-14 – 16 | Leukerbad Robotics Hackathon — **first European appearance found** | event context |

## Current focus projects

| Focus | What they are doing now | Evidence |
|---|---|---|
| Productising the capture kit | OriginKitGen 1.0 offered via enquiry; site rebuilt around kit + capture services three days before the hackathon | Official site |
| Scaling real-world capture | Task-based field capture ("wild" collection) in home-service and industrial settings; pipeline of clock sync, per-user calibration, artefact handling, segmentation, labelling, quality gates | QbitAI; GitHub ⚠️ |
| Force estimation quality | Active recalibration work to cut fingertip / grip force error; contact-masked force values pushed to the public dataset in October | Hugging Face; GitHub ⚠️ |
| Auto-annotation | Subtask and atomic-action language labels at scale (26,117 and 101,445 in the preview); contact-label F1 reported at 72.41 % against a provisional VLM reference | Hugging Face |
| Opening up to the research community | First public dataset in LeRobot v3.0 layout; 6,722 downloads in the last month, 25 likes | Hugging Face |
| Capture UX | Hands-free "capture gate" on the glasses (pose in range + two-hand OK gesture) | GitHub ⚠️ |

## Announced and upcoming products

| Item | Status | Date / timing | Notes |
|---|---|---|---|
| OriginKitGen 1.0 (Glass + Band + Space) | ✅ via enquiry | On site 2026-11 | Price not public; press figure of about RMB 1,000 per equipment set ⚠️ unverified |
| Data Capture Services | ✅ | Ongoing | Terms, volumes, licence not public |
| OriginData preview sample (100.62 h) | ✅ gated | Published about 2026-09, updated 2026-10 | Custom licence |
| OriginData full corpus (**28 domains, 1,170 tasks**) | 🧪 described on the dataset card | Release date and access model not public | Total hours not public |
| PULSE 0.2 | 🧪 demo only | WAIC, 2026-07 | No weights / API |
| PULSE 0.3 (tendon force, hand forward kinematics) | 🧪 in development | Stated 2026-08; no release date | — |
| CHORD (omni-modal alignment base) | 🧪 | No date | Used internally; referenced in the dataset's annotation report |
| ORACLE (auto-annotation) | 🧪 internal | No date | — |
| Raw sEMG / IMU release in the public dataset | 🔭 not announced | — | Capture pipeline uses them; not listed as released columns |
| Public SDK / developer programme | 🔭 not announced | — | Nothing public |
| Next-generation "always-on" AI hardware, including robots ("With Human" stage) | 🔭 | No date | Wristband described as a current capture terminal, not the final form |
| Capture via everyday wearables (glasses, watch, bracelet) | 🔭 | No date | — |
| "Enhance Human" stage | 🔭 | 10 – 30 year horizon | — |

## Strategic direction and markets

**Thesis**
- Robot learning is bottlenecked by data that includes **force and contact**, which video-only ("EgoScale") and handheld-gripper (UMI-style) collection miss or capture expensively.
- sEMG is positioned as a **non-intrusive complement** to those methods, not a replacement: hands stay bare, capture can happen during real work.
- Scale ambition (stated): from tens / hundreds of millions of hours toward trillions of hours of human data, with a smaller set of cross-embodiment robot data as alignment anchors.
- Representation play: "Human Tokens" over MotionSpace, TactileSpace and TendonSpace — an attempt to own the intermediate format between human data and any robot body.

**Business model (as visible)**

| Layer | Offer | Maturity |
|---|---|---|
| Hardware | Capture kit | ✅ early |
| Services | Task-based real-world data capture for robotics / Physical-AI teams | ✅ |
| Data | Curated datasets (OriginData) | ✅ preview |
| Models | PULSE / CHORD as reconstruction and alignment layer | 🧪 |

**Markets**

| Market | Status | Detail |
|---|---|---|
| Home services | Active | With strategic investor 58 Group: clothes organising, cleaning, kitchen tasks — skills database for domestic robots |
| Industrial manufacturing | Active | With unnamed "leading global high-end manufacturers" |
| Dexterous-hand ecosystem | Active ⚠️ date unverified | LinkerBot partnership |
| Medical rehabilitation | 🔭 named as a future application | No product, certification or deployment found |
| Smart hardware / spatial computing / next-gen HCI | 🔭 named as future applications | — |

**Funding**
- **> RMB 500M** across angel, strategic and Pre-A1 (public 2026-05-21). Valuation not public. No later round found.

**Europe / Switzerland**
- No entity, office, distributor, customer or research partner in Europe found.
- English-language surface is new: English website (2026-11), Hugging Face dataset with English card and licence, X and LinkedIn accounts.
- Reading (inference): Leukerbad looks like an **early international developer-outreach step**, not an established market presence. Expect the team to be looking for use cases, research contacts and data-capture partners rather than selling units.

**Competitive context**
- Meta is the reference point for wrist sEMG (CTRL-Labs acquisition 2019, Neural Band with its 2025 glasses), but aims at consumer input, not robot data.
- Chinese press lists several other start-ups using sEMG for embodied-AI data, so the niche is contested.
- Independent validation of OriginFlow's accuracy claims: none found.

## Research and open-source activity

| Area | Status |
|---|---|
| Peer-reviewed papers / arXiv preprints on PULSE, CHORD, NeuroScale | None found ⚠️ unverified (search unavailable) |
| Public model weights | None (Hugging Face org shows 0 models) |
| Public dataset | **1** — [OriginData preview sample](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample): 100.62 h, 7,717 episodes, 10.87M frames, 414 GB, LeRobot v3.0 Parquet + MP4, gated, custom licence |
| Dataset claim | Card describes it as the first large-scale real-world dataset combining hand pose and force annotations (company claim; force is model-estimated by "Fusion2Force") |
| Published quality metrics | Finger-contact labels: F1 72.41 %, precision 82.38 %, recall 64.59 % vs provisional VLM reference |
| GitHub | `OriginFlow-AI` org, 5 public repos (capture gate for glasses, RGB-D hand-object reconstruction, field calibration notes, DPVO fork, data cache) — ⚠️ affiliation unverified; no licences; reads as internal tooling made public, not a community SDK |
| Standards work | Joint standards effort mentioned in the LinkerBot partnership ⚠️ unverified |

Takeaway: openness is **recent and data-first**. They have released derived data (pose, force, language) but kept raw sEMG, models and device interfaces closed.

## What would impress this company at the hackathon

**All of this section is inference from their stated strategy — not company statements.**

What they appear to care about: (a) proof that sEMG-derived **force and intent** add something vision alone cannot; (b) **human-to-robot transfer** onto real hardware; (c) new **data-capture scenarios** outside factories and homes; (d) credible first steps toward **rehabilitation** and HCI markets; (e) external users of OriginData.

| Track | Idea that would land | Why it matters to them | Pairing |
|---|---|---|---|
| **T04 Elderly Care & Rehabilitation** (best fit) | Grip / pinch rehab coach: Band measures muscle effort and estimated finger force, a force-controlled arm or hand gives graded resistance or assistance, progress is logged per session | First concrete demo in a market they have only named; shows force estimation is useful even when imperfect | Flexiv Rizon or ROKAE xMate; WUJI Hand |
| T04 | Intent-driven assistance: weak grasp intent detected from sEMG triggers a mobile manipulator to fetch, hold or open something | "With Human" stage in miniature — hardware that works alongside a person | Galaxea R1, Galbot G1, UniX Wanda |
| T02 Resilient & Safe City | Force-aware teleoperation with occluded hands (gloves, smoke, behind a panel): valve turning or connector mating where vision-only hand tracking fails | Directly demonstrates their core argument against video-only capture | Unitree G1 + Dex hand, or any arm + WUJI Hand |
| T01 Autonomous Urban Services | "Show once, robot repeats": record a maintenance or delivery hand-over skill with the kit, retarget to a robot, replay | Human-to-robot cross-embodiment transfer on a new body | Any dual-arm mobile manipulator; LeRobot tooling |
| T03 Sustainable City | Capture expert sorting or repair skill (force-sensitive disassembly) as a small labelled dataset in their format | A new capture domain; weakest live-demo potential | Dobot or ROKAE arm for replay |
| Any | Use **OriginData** in the solution (pre-train a grasp-intent or task-segmentation model, or ground a VLM planner) and report what worked and what was missing | External validation and feedback on their first public dataset | D-Robotics RDK for on-edge inference |

What will count most (inference):
- **Quantified results** — latency, force-tracking error against a reference (for example a force-controlled arm's own sensor), success rate with vs without EMG.
- **A second user** — show it works after recalibrating on a teammate, not only on one trained operator.
- **Honest framing for care use** — research prototype, consent handled, no medical claims.
- **Data handed back** — a clean, labelled recording set from an alpine / clinic-like scenario is itself valuable to a data company.

What would not impress: discrete gesture recognition as a remote control (they explicitly contrast PULSE with that), or a demo where the wristband is decorative and vision does the real work.

## Sources

- [OriginFlow official site](https://www.originflow.ai/)
- [OriginFlow — About](https://www.originflow.ai/about)
- [OriginFlow — Portfolio](https://www.originflow.ai/portfolio)
- [Hugging Face org: OriginFlow-AI](https://huggingface.co/OriginFlow-AI)
- [Hugging Face dataset: OriginData preview sample (card)](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample)
- [Hugging Face dataset: file tree and commit messages](https://huggingface.co/datasets/OriginFlow-AI/origindata-preview-sample/tree/main)
- [GitHub org: OriginFlow-AI](https://github.com/OriginFlow-AI) (affiliation unverified)
- [GitHub: OriginFlow-AI/wild-few-shot](https://github.com/OriginFlow-AI/wild-few-shot)
- [GitHub: OriginFlow-AI/double_gesture_detect](https://github.com/OriginFlow-AI/double_gesture_detect)
- [TMTPost, 2026-05-21 — Tsinghua PhD student raises over 500 million yuan in five months](https://en.tmtpost.com/post/7997613)
- [QbitAI, 2026-08-22 — OriginFlow profile (Chinese)](https://www.qbitai.com/2026/08/477094.html)
- [36Kr Europe, 2026-08-24 — republished profile (English)](https://eu.36kr.com/en/p/3950735048031365)
- [Gasgoo — LinkerBot and OriginFlow partnership](https://autonews.gasgoo.com/articles/news/2089539854819147777) (could not be opened; details taken from the company profile in this folder)
