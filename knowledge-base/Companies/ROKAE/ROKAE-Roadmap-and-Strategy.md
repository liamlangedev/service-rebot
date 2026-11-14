---
type: roadmap
company: "ROKAE Robotics"
slug: ROKAE
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# ROKAE Robotics — Roadmap and Strategy

⬆ [ROKAE Robotics profile](ROKAE.md) · [Product portfolio](ROKAE-Products.md) · [Developer guide](ROKAE-Developer-Guide.md)

> Research note: based on ROKAE's own news pages, its Oct 2026 press release, the IPO sponsor-side announcement and the official docs / GitHub. Open web search was not available for this pass, so trade-press coverage, pre-IPO funding rounds and European channel details are thin and marked where unconfirmed.

**In one line:** a force-control specialist that went public in July 2026 and is repositioning from "cobot maker" to **supplier of force-controlled arms, joints and controllers for other companies' humanoids**, with its own wheeled humanoid (Helios) as the reference platform.

## Company trajectory

| Date | Milestone |
|---|---|
| 2014 | Company founded (per Oct 2026 press release); founder and CEO **Tuo Hua** |
| 2014–2024 | Builds industrial arms (NB / XB) and xMate force-controlled cobots on its own xCore controller. Pre-IPO venture rounds: details not verified in this research |
| Aug 2024 | Python SDK v0.4.1 adds force-control interfaces (xCore 2.2.2) |
| Dec 2024 | SDK v0.5.0 for xCore 3.0.1 |
| Jan–Jun 2026 | SDK 0.7.0 → 0.7.2 for xCore 3.2.x; separate 0.7.x-AR docs branch for the humanoid arm; 0.8.x docs appear |
| 9 Jul 2026 | **Hong Kong Main Board listing (3752)** — about 23M shares at HKD 38, raising about **HKD 875M** |
| ~Jul 2026 | Human.X full-size bipedal humanoid launched 🧪 (date from a single secondary source — ⚠️ unverified) |
| Aug 2026 | Strategic partnership with **SHANTUI** (construction machinery) on intelligent construction equipment (news listed 10 Aug 2026) |
| 19 Aug 2026 | **World Robot Conference 2026, Beijing:** "full-stack development platform for embodied intelligence" — HSA joints + AR arms + Helios + **iNex** controller |
| Sep 2026 | **10,000th AR humanoid force-controlled arm** leaves the Shandong production base |
| 27 Oct 2026 | Press release: 10,000 arms, **80+ industrial partners**, five Helios robots running at **Schaeffler** Taicang |
| Nov 2026 (listing dates) | Bosch China supplier innovation award; Shandong Heavy Industry Group visit; **Northeast Intelligent Manufacturing Alliance** launched in Shenyang with three integrators |

Dates on ROKAE's English news list are posting dates and can trail the event by weeks.

## Current focus projects

| Focus | What they are doing now | Evidence |
|---|---|---|
| Humanoid arms as a component business | AR 7-DoF arms sold to other robot makers; counted separately from cobots | 10,000 units, 80+ partners (Oct 2026) |
| Reference humanoid in real factories | Helios wheeled dual-arm robots doing parts handling, assembly and inspection at Schaeffler's Taicang lighthouse factory | Five units deployed |
| Unified whole-body control | **iNex** 🧪: one real-time controller for arms, waist, head and chassis; whole-body control, impedance / admittance / hybrid force-position; hooks for teleoperation devices and model training | WRC 2026 news; no public API |
| Learned manipulation skills | Dual-arm AR5 USB insertion with imitation learning + human-in-the-loop RL, reported 95–99 % success | WRC 2026 demo; model not released |
| Teleoperation data collection | Demonstrated with third-party gear: IO-AI TeleXperience, Wuji Hand, motion capture, exoskeleton gloves | WRC 2026 demo |
| Welding | AI-assisted cobot welding packages, shown at several 2026 Chinese trade events | Aug and Nov 2026 news |
| Channel building in China | "ROKAE+" open ecosystem; regional integrator alliances (laser, grinding / polishing, general automation) | Nov 2026 alliance news |
| Wellness / therapy applications | Therapeutic massage robot with partner EaseFuture (acupoint detection in about 3 s) shown at WRC 2026 | WRC 2026 news |

## Announced and upcoming products

| Item | Status | Date | Notes |
|---|---|---|---|
| iNex embodied-AI / whole-body control platform | 🧪 | Shown Aug 2026 | Called an "open motion-control platform"; no public docs, SDK or pricing |
| Human.X bipedal humanoid | 🧪 | Mid-2026 | Product page exists; availability and price not public |
| Full-stack embodied development platform (HSA + AR + Helios + iNex) | 🧪 | Aug 2026 | Positioned as ready-to-use for partners; commercial terms not public |
| Larger AR arm (up to 20 kg payload) | 🧪 ⚠️ unverified | Aug 2026 | WRC news quotes an AR payload range of 3–20 kg; the product page lists AR3 / AR5 / AR10 |
| Helios with "43 DoF" configuration | 🧪 ⚠️ unverified | Aug 2026 | News says 43 DoF; product spec table says 23 (likely with vs without hands) |
| SDK 0.8.x | ✅ docs published | 2026 | Changes versus 0.7.x not checked |
| VLA / foundation model from ROKAE | 🔭 | — | Mentioned in Human.X marketing only; nothing downloadable |
| Dated product roadmap beyond 2026 | not public | — | — |

## Strategic direction and markets

- **Positioning:** "Robotics + AI" across three lines — industrial robots, flexible collaborative robots, embodied intelligent robots — and across three layers: core components (HSA joints), robot bodies (arms, Helios, Human.X), control systems (xCore, iNex). The stated aim is that partners build on ROKAE's platform instead of redeveloping force control.
- **Differentiator:** joint-torque-sensor force control developed in-house for over a decade; CEO messaging is that force control "has no shortcuts".
- **Market position (CIC data cited at IPO):** top six among cobot providers in China; top five in China's embodied robotic-arm market.
- **Customers:** **1,000+ enterprises in 40+ countries and regions**. Named industrial references in 2026: Schaeffler, Bosch (supplier award), SHANTUI, Shandong Heavy Industry Group (talks).
- **Funding:** IPO proceeds of about HKD 875M (Jul 2026). Use-of-proceeds breakdown not confirmed here. Earlier private rounds — not verified. A net loss was guided for 2026 (see profile).
- **Go-to-market:** integrator and distributor led. In China, regional alliances ("headquarters empowerment + platform distribution + specialised integration").
- **Europe / Switzerland:** sold through distributors (for example a Danish reseller, see profile). No Swiss entity, Swiss deployment or European R&D site found — **not public**. Participation in a Swiss hackathon is itself a signal of interest in European developers and research labs (inference).
- **Japan:** localised website with healthcare case studies (moxibustion, tele-ultrasound).
- **Risks to weigh as a builder:** public developer material covers arms only; Helios, Human.X and iNex have no open documentation; small open-source community; English docs are partly machine-translated.

## Research and open-source activity

| Area | Status |
|---|---|
| Open-source code | Official GitHub account `RokaeRobot` (8 public repos): xCoreSDK C++ / Python / C# / Android, `rokae_ros2`, two xCore plugin kits. Apache-2.0. Active in 2026 (plugin repos updated Oct–Nov 2026, SDKs Jul 2026) |
| Community size | Small — xCoreSDK-CPP about 46 stars, rokae_ros2 about 12 |
| Simulation assets | URDF / xacro + Gazebo + MoveIt 2 configs in `rokae_ros2`; no official MuJoCo or Isaac assets found |
| Models and datasets | None released |
| Publications | Not checked in this pass. xMate 7-DoF arms are used in university force-control research — ⚠️ unverified, no specific papers confirmed |
| Embodied-AI research shown publicly | Imitation learning + human-in-the-loop RL for precision assembly; teleoperation data capture with partners (WRC 2026) |

## What would impress this company at the hackathon

**Inference, not a statement from ROKAE.** It follows from what they promote: force control, arms as a platform for others, real industrial and wellness use cases.

| Track | Build that plays to their strategy | Why it would land |
|---|---|---|
| T04 Elderly Care & Rehabilitation | Compliant physiotherapy or thermal-spa assistant: guided limb mobilisation or massage stroke with adjustable Cartesian stiffness, force limits and logged force / range-of-motion data for the therapist | Mirrors their massage and therapy demos; shows force control doing something position control cannot; fits Leukerbad's rehab clinics |
| T04 | Teleoperated or demonstration-taught care task (drag-teach once, replay with force adaptation), ideally with a dexterous hand from another vendor on site | Matches their teleoperation + data-collection narrative and the Wuji Hand pairing they already showed |
| T01 Autonomous Urban Services | ROKAE arm mounted on another vendor's mobile base or quadruped for a contact task: pressing lift buttons, opening doors, handing over parcels with force-sensed release | Demonstrates the "arm as a component for other robots" business they are pushing |
| T02 Resilient & Safe City | Remote contact inspection or valve / switch operation with haptic-style force feedback from joint torque sensing | Uses torque sensing as a sensor, not just for safety |
| T03 Sustainable City | Force-guided disassembly or sorting (unscrewing, connector removal, pressing recyclables apart) learned from a few kinesthetic demos | Close to their USB-insertion / precision-assembly showcase, with a sustainability outcome |

Cross-cutting points likely to score:

- **Use the force data visibly** — plots of contact force, stiffness changes, collision reactions.
- **Stay on the public stack** (xCore SDK, `rokae_ros2`) and contribute something reusable: a LeRobot wrapper, an MJCF / USD model, a ROS 2 force-control node. Their open-source footprint is small, so a clean contribution stands out.
- **Show a path to a real customer** (clinic, hotel, municipal service) rather than a lab trick — their messaging is about deployment at scale.
- **Safety discipline** around people: low stiffness, speed limits, e-stop, dummy testing first.

## Sources

- [TechNode Global (PR Newswire) — ROKAE delivers its 10,000th humanoid force-controlled arm, 27 Oct 2026](https://technode.global/?p=996114)
- [Deloitte China — listing of Rokae Robotics on SEHK, Jul 2026](https://www.deloitte.com/cn/en/about/press-room/deloitte-china-assists-listing-of-rokae-robotics-on-sehk.html)
- [ROKAE news index](https://www.rokae.com/en/news/)
- [ROKAE news — WRC 2026 full-stack development platform for embodied intelligence](https://www.rokae.com/en/news/show/2604/WRC-2026:-ROKAE-Unveils-a-Ready-to-Use-Full-Stack-Development-Platform-for-Embodied-Intelligence,-Advancing-Physical-AI-Infrastructure-Development.html)
- [ROKAE news — Northeast Intelligent Manufacturing Alliance](https://www.rokae.com/en/news/show/2608/ROKAE-Robotics-Officially-Launches-Northeast-Intelligent-Manufacturing-Alliance-Under-Its-New-Ecosystem-to-Empower-Industrial-Collaboration.html)
- [ROKAE — Wheeled Dual-Arm Robot Helios](https://www.rokae.com/en/product/show/596/Wheeled-Dual-Arm-Robot-Helios.html)
- [ROKAE SDK introduction](https://docs.rokae.com/en/docs/SDK/SDK_Intro)
- [ROKAE C++ SDK introduction (version history)](https://docs.rokae.com/en/docs/SDK/cpp/cpp_Intro)
- [ROKAE Python SDK introduction (version history)](https://docs.rokae.com/en/docs/SDK/python/py_Intro)
- [Rokae xMate ROS 2 user manual](https://docs.rokae.com/en/docs/ROS2/rokae%20ros2%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C)
- [GitHub — RokaeRobot account](https://github.com/RokaeRobot)
- [ROKAE Robotics profile (this repo) — IPO, customers, Europe distributor and Human.X sources](ROKAE.md)
