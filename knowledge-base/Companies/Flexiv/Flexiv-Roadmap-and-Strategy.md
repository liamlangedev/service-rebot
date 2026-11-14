---
type: roadmap
company: "Flexiv Robotics"
slug: Flexiv
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# Flexiv Robotics — Roadmap and Strategy

⬆ [Flexiv Robotics profile](Flexiv.md) · [Product portfolio](Flexiv-Products.md) · [Developer guide](Flexiv-Developer-Guide.md)

**In one line:** Flexiv is moving from "a force-controlled arm" to "a force-controlled platform for physical AI" — new Enlight arm, MICO dual-arm systems, a mobile base, a consumer-facing massage product, and an open teleop-to-policy toolchain tied closely to NVIDIA Isaac.

## Company trajectory

| Date | Milestone |
|---|---|
| 2016 | Company founded (Shiquan Wang, CEO) |
| 2019 | Series A, **USD 22M** |
| 2020-12 | Series B, **more than USD 100M** (Meituan, Meta Capital, New Hope Group, Longwood, YF Capital, Gaorong, GSR Ventures, Plug and Play); total then **> USD 122M**; funds earmarked for scaling Rizon |
| 2025 (mid) | Series C of about USD 100M reported ⚠️ unverified — the trade-press article usually cited for it is in fact the 2020 Series B story |
| 2025-06-12 | NVIDIA collaboration: Flexiv-Isaac Bridge App puts force-control simulation into Isaac Sim; Tower of Hanoi demo code open-sourced |
| 2025-09 to 2025-11 | CIIF (Shanghai), IROS 2025, first Japan appearance at iREX 2025 (2025-11-28) |
| 2025-12 | FMR 300 — first in-house AMR |
| 2026-03-18 | New financing led by **Invus** (evergreen investor, > USD 12B AUM; offices New York, Paris, Hong Kong); amount not disclosed; for R&D and global sales / service build-out |
| 2026-04 | Hannover Messe 2026 — first European showing of the Mello massage platform; RDK **v2.0** released (2026-04-28) for the new robot software line v3E |
| 2026-05-29 | Preview of next-generation robots at ICRA |
| 2026-06-09 | South Korea debut (Smart Tech Korea) |
| 2026-06 | **Enlight** arm and **MICO** dual-arm platform launched internationally at Automate 2026; booth demos with Generalist AI, Industrial Next, Saint-Gobain and NVIDIA |
| 2026-07 | First India appearance (Automation India Expo) |
| 2026-09-21 | IROS 2026 force-control showcase |
| 2026-09-24 | Rizon 4 supported in **NVIDIA Isaac**; contact-rich insertion reference workflow (Isaac Lab + Isaac ROS) |
| 2026-11 | 27 public GitHub repos, most updated within the past month |

## Current focus projects

- **New hardware generation:** Enlight (15 kg, F/T sensing in all 7 joints, whole-body touch) and MICO (two Enlight arms, one control box, four configurations). A separate software line (robot software v3E, RDK v2.x) was created for it.
- **Physical-AI toolchain:** Flexiv Trainer (teleop → LeRobot data → training → rollout), TDK teleoperation, DDK data streaming, dual-arm DRDK — all open on GitHub and updated in Oct–Nov 2026.
- **NVIDIA alignment:** Isaac Sim bridge (2025) → Rizon 4 as a supported Isaac robot with an RL cable-insertion reference workflow (2026); data-centre hardware assembly is the showcase use case (GPU / server component insertion).
- **Mobile manipulation:** FMR 300 base, Mobile Manipulator, AICO platforms for lab automation, CNC tending and mobile polishing.
- **Mello:** productising robot massage for retail / wellness operators.
- **Geographic push:** new-market debuts in Japan, South Korea and India within 12 months; Europe served from Munich.

## Announced and upcoming products

| Product | Status | Timing | Notes |
|---|---|---|---|
| Mello robotic massage system | 🧪 | Release slated **Q4 2026** | Shown in Europe at Hannover Messe 2026; not positioned as a medical device in public material |
| Enlight L arm | ✅ / 🧪 | Launched June 2026; delivery status ⚠️ unverified | Software support (RDK 2.x, ROS 2, URDF, Isaac USD) already public |
| MICO Armor / Core / Plus | ✅ / 🧪 | Launched June 2026; delivery status ⚠️ unverified | Supported in `flexiv_ros2` and `flexiv_description` |
| MICO Ultra | 🧪 | No date | Appears in ROS 2 / URDF / Isaac assets with arms + torso + mobile base (base not yet in ros2_control); official specs not public |
| Enlight-LL (dual-arm on one controller) | 🧪 | No date | Listed as a robot type in the open-source repos; no product page seen ⚠️ unverified |
| NVIDIA Isaac insertion workflow + sim assets, Isaac ROS GEMs for Rizon 4 | 🧪 | Announced 2026-09-24, release "being rolled out" | Public repo location not confirmed |
| B-spline policy rollout in Flexiv Trainer | 🧪 | No date | README marks the converter experimental; executor adapter still missing |
| Legged humanoid | not announced | — | MICO is the "humanoid-style" answer: dual-arm torso, optional wheeled base |
| In-house foundation model / VLA | not public | — | Partners (e.g. Generalist AI demo at Automate 2026) fill this gap today |

## Strategic direction and markets

- **Positioning:** "adaptive robots" for contact-rich, variable tasks that position-controlled cobots handle poorly — polishing / sanding, insertion and assembly, machine tending, lab automation, and body contact (massage).
- **Bet:** force control is the missing layer for embodied AI. Flexiv supplies the hardware and low-level control (1 kHz open SDK) and lets customers and AI partners bring the policy.
- **Platform over component:** single arm → dual-arm (MICO, AICO) → mobile (FMR 300) → turnkey application (Mello).
- **Funding:** Series A USD 22M (2019), Series B > USD 100M (2020), Invus-led round (2026-03, undisclosed). Total raised and valuation: sources conflict — treat any single figure as ⚠️ unverified.
- **Regions:** established in North America and China; stated expansion in **Europe and Asia**. Offices: Silicon Valley, Shanghai, Beijing, **Munich**, Singapore.
- **Europe / Switzerland:** Munich office; Hannover Messe 2026 booth; a French industrial group (Saint-Gobain) among Automate 2026 demo partners; lead investor Invus has a Paris office. **No Swiss entity, distributor or customer found** — a Swiss reference in spa / rehab or precision manufacturing would be new ground for them (inference).
- **Named ecosystem partners (public):** NVIDIA (Isaac), Generalist AI, Industrial Next, Saint-Gobain (booth demos, June 2026). Nature of commercial terms not public.

## Research and open-source activity

- **Open-source footprint:** 27 public repos under `flexivrobotics`, Apache-2.0 for the main kits (RDK, TDK, Trainer). Release cadence is high: RDK v1.9.x (Rizon line) had six PyPI releases between Feb and Oct 2026; v2.0 and v2.1 (Enlight line) shipped April and June 2026.
- **Learning-from-demonstration:** Flexiv Trainer stores LeRobot-format data, records stiffness with each dataset, supports human takeover during rollout and paired checkpoint evaluation — a research-grade workflow rather than a demo script.
- **Teleoperation:** TDK supports LAN and internet teleop with force feedback; its README cites recognition on the Manipulation Net peg-in-hole leaderboard.
- **Sim-to-real:** Isaac Sim bridge runs the real force controller in the loop; NVIDIA's reference workflow trains insertion policies in Isaac Lab and deploys on Rizon 4.
- **Perception hints:** forks of ORB-SLAM3, Basalt, Pangolin and IMU tools in the org suggest internal visual-inertial SLAM work (inference, no product announced).
- **External research on Flexiv hardware:** NVIDIA server-assembly research with two Rizon 4s arms (Flexiv blog, 2026-11, via profile). Academic datasets using Flexiv arms exist in the literature ⚠️ unverified in this pass.
- **Conference presence:** ICRA and IROS booths / talks in both 2025 and 2026.

## What would impress this company at the hackathon

*Inference — based on the direction above, not on any statement from Flexiv.*

| Track | What would land | Why it matches their roadmap |
|---|---|---|
| **T04 Elderly Care & Rehabilitation** (best fit) | Force-limited, adaptive body contact that goes beyond a fixed massage routine: e.g. assisted range-of-motion exercise that measures resistance and logs progress, or a contact routine that adapts pressure to live force feedback | Extends Mello from wellness toward rehab; Leukerbad's clinics make it a credible European story |
| **T03 Sustainable City** | Contact-rich disassembly, sorting by stiffness / feel, or surface refurbishing where force replaces precise fixturing | Same value proposition as their polishing and insertion business, new sustainability angle |
| **T01 Autonomous Urban Services** | Arm as the "last-centimetre" on another vendor's mobile base: plug-in charging, door / button / handover with force-based error cancelling | Mirrors their Mobile Manipulator pitch (force cancels docking error) and their push to be the manipulation layer in other platforms |
| **T02 Resilient & Safe City** | Tele-operated contact tasks with force feedback (valve, connector, sampling) using TDK-style leader-follower control | Shows off remote teleoperation, including over WAN |

Cross-cutting points that would stand out:

- **Use force as a sensor, not only a safety limit** — detect contact, estimate stiffness, search for a hole, follow a surface. Vision-only pick-and-place undersells the hardware.
- **Close the data loop:** record demonstrations in LeRobot format, train a small policy, run it with a human-takeover fallback. That is exactly the Trainer workflow they are investing in.
- **Combine with an on-site AI or sensing vendor** (a VLA from another company, EMG input, AR glasses for supervision) while keeping Flexiv's controller as the compliant execution layer.
- **Show measured numbers** — contact force traces, success rate over N trials, peak force on a human-safe test — rather than a single lucky run.
- **Local relevance:** a spa / rehab scenario with a clear safety concept is a ready-made European reference case for a company that has no Swiss footprint yet.

## Sources

- [Flexiv — news list](https://www.flexiv.com/news)
- [Flexiv — "Flexiv Secures Capital from Leading Evergreen Investor" (2026-03-18)](https://www.flexiv.com/news/Flexiv_Secures_Capital_from_Leading_Evergreen_Investor)
- [Flexiv — "Flexiv to Unveil Next-Generation Adaptive Robots at Automate 2026"](https://www.flexiv.com/news/Flexiv_to_Unveil_Next-Generation_Adaptive_Robots_at_Automate_2026)
- [Flexiv — "Flexiv and NVIDIA Join Forces in Robotics Simulation" (2025-06-12)](https://www.flexiv.com/news/Flexiv_and_NVIDIA_Join_Forces_in_Robotics_Simulation)
- [The Robot Report — Flexiv raises more than $100M for adaptive robots (2020-12-30)](https://www.therobotreport.com/flexiv-raises-more-than-100m-for-adaptive-robots/)
- [Robotics 24/7 — Flexiv Rizon 4 now supported in NVIDIA Isaac (2026-09-24)](https://www.robotics247.com/article/flexix-rizon-4-adaptive-robot-now-supported-in-nvidia-isaac/Flexiv_Robotics)
- [GitHub — flexivrobotics organisation repositories](https://github.com/orgs/flexivrobotics/repositories?type=all)
- [GitHub — flexiv_ros2 README (supported robot types)](https://github.com/flexivrobotics/flexiv_ros2)
- [GitHub — flexiv_description README](https://github.com/flexivrobotics/flexiv_description)
- [GitHub — isaac_sim_ws README](https://github.com/flexivrobotics/isaac_sim_ws)
- [GitHub — flexiv_tdk README](https://github.com/flexivrobotics/flexiv_tdk)
- [GitHub — flexiv_trainer README](https://github.com/flexivrobotics/flexiv_trainer)
- [Flexiv RDK manual v2.x — Robot Software Compatibility](https://www.flexiv.com/software/rdk/manual/v2.x/robot_software_compatibility.html)
- [Flexiv RDK manual v1.x — Robot Software Compatibility](https://www.flexiv.com/software/rdk/manual/v1.x/robot_software_compatibility.html)
- [PyPI — flexivrdk release history](https://pypi.org/project/flexivrdk/)
- [Flexiv Robotics profile (this repo) — dates for FMR 300, Hannover Messe, India, Mello Q4 2026](Flexiv.md)
