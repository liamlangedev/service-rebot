---
type: roadmap
company: "SKYLANDX"
slug: SKYLANDX
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# SKYLANDX — Roadmap and Strategy

⬆ [SKYLANDX profile](SKYLANDX.md) · [Product portfolio](SKYLANDX-Products.md) · [Developer guide](SKYLANDX-Developer-Guide.md)

> **Read this in 30 seconds:** SKYLANDX is a survey / reality-capture company that is pushing into robotics. Its trajectory is handheld scanners (2023) → own LiDAR hardware (C01, Air 3 in 2026) → "spatial intelligence" for robots (perception kits, navigation APIs, Real2Sim). Public information on funding, customers and partnerships is thin; this page says so where it applies.
> **Research limit (2026-11-14):** fresh web searches for funding rounds, new partnerships and repositories could not be run today. Dated items come from the official site, official brochure files, one trade article and the earlier profile research.

## Company trajectory

| Date | Milestone | Confidence |
|---|---|---|
| 2020 | Starts building spatial perception, localization and path-planning technology (about page). Core team from the HKUST–DJI Joint Innovation Lab; first team incubated under Prof. Li Zexiang's HKCRC initiative | ✅ official |
| 2023 | First integrated handheld scanner ships — start of the MetaCam line | ✅ trade press quoting the company |
| 2025-05 | First-generation MetaCam Air brochure published on the official site | ⚠️ unverified — inferred from the file's upload path only |
| 2026-05 | GEOSURF begins distributing SKYLANDX products in Japan; MetaCam Lite introduced there; MetaCam Fly described as in development | ⚠️ from the profile's earlier research — the source page could not be re-read today |
| 2026-08 | C01 SLAM LiDAR and MetaCam Pro brochures issued (file dates 2026-08-13 and 2026-08-18) | ✅ official files (date from file metadata / name) |
| 2026-09 | MetaCam Air 2 brochure issued (2026-09-16); supplier listing on Unmanned Systems Technology; first official blog post (2026-09-20) | ✅ official files · UST listing per profile |
| 2026-10-07 | **MetaCam Air 3** unveiled at INTERGEO 2026, Munich — first handheld built around SKYLANDX's own LiDAR. Company states **5,000+ units shipped** and **1 billion+ m²** captured | ✅ trade press |
| 2026-11-14 to 16 | On site at the Leukerbad Robotics Hackathon | ✅ event context |

## Current focus projects

- **Launching MetaCam Air 3** 🧪 — commercial details (configurations, regions, price) still to be announced as of the October article.
- **Selling the current line** ✅ — MetaCam Air 2 (volume handheld), MetaCam Lite (entry, interiors), MetaCam Pro (survey-grade, multi-platform), each with the Go / Studio / Cloud software chain and 3DGS output.
- **Robotics & Physical AI offer** ✅ — three integration depths for third-party robots (scan payload → live perception layer → full navigation module), a MetaCam Hub mount, a Modular Perception Kit with raw-data and SLAM / navigation APIs, and "Real2Sim" environments (3DGS paired with measured point clouds and meshes).
- **C01 SLAM LiDAR** ✅ — a standalone LiDAR for teams that already have an autonomy stack (AMRs, service robots, quadrupeds, humanoids, forklifts).
- **Algorithm positioning** — the one blog post argues that SLAM algorithm quality, not hardware, separates scanners; the brand message is "built by the team behind VINS-Fusion".
- **Named customers or deployments:** none public.

## Announced and upcoming products

| Product | Status | Date | What is known | What is not public |
|---|---|---|---|---|
| MetaCam Air 3 | 🧪 announced | Unveiled 2026-10-07 (INTERGEO, Munich) | In-house LiDAR with **360° × 240°** FOV and a smaller laser spot · 2 × **50 MP** panoramic cameras + 48 MP forward camera + global-shutter VSLAM camera · RTK via NTRIP or magnetically attached UHF radio, PPK · removable RTK module · one-button start · "Mars Ring" status indicator showing SLAM accuracy | Price, weight, range, accuracy figures, ship date, regional availability, robot / API support |
| MetaCam Fly | 🔭 in development | No date (mentioned 2026-05; listed in the site inquiry form) | Autonomous-flight drone scanning platform | Everything else |
| Full navigation module for third-party robots | 🔭 per-partner | No date | Perception + localization + path planning, outputting navigation commands; tailored per platform for ecosystem partners | Supported platforms, pricing, timelines |
| Skyland / MetaCam Cloud third-party integration | ✅ claimed, undocumented | — | "Integration with third-party systems" on the software page | Public API, pricing, hosting region |

No other dated roadmap items are public.

## Strategic direction and markets

**Direction (stated or directly evidenced):**

- **Vertical integration into sensors.** The CTO's framing for Air 3 is that it was not designed around the limits of an existing sensor; C01 and the Air 3 LiDAR are the company's own hardware. *Inference:* earlier models relied on third-party LiDAR, and owning the sensor is now a differentiator against other handheld-SLAM brands.
- **From survey tool to robot perception supplier.** The official site title pairs "3D Scanners & Robotics for Spatial Intelligence"; robotics pages target drones, UGVs, quadrupeds and humanoids, GPS-denied sites (tunnels, mines) and 3D data for embodied-AI training.
- **Gated ecosystem model.** Deeper integrations are reserved for "eligible customers" and "ecosystem partners" — a partner-led rather than open-developer strategy. No public SDK or GitHub presence.
- **Software lock-in through the workflow.** Capture (Go) → process (Studio, Windows) → cloud 3DGS and sharing (Cloud), with broad export formats to stay compatible with Autodesk and survey tools.

**Markets named by the company:** AEC, surveying, industrial facilities / digital factory, robotics and physical AI, game / XR / media, cultural heritage, forestry, interior renovation.

| Topic | What is public |
|---|---|
| Europe | Presence at INTERGEO 2026 in Munich (Air 3 launch). No European office, subsidiary or named distributor found |
| Switzerland | No distributor, customer or deployment found — **not public**. The Leukerbad hackathon is the only Swiss touchpoint identified |
| Asia | Japan distribution through GEOSURF (May 2026, per profile research) |
| Channels | Direct sales via site forms; resellers and trade listings (UST, DirectIndustry — per profile) |
| Partnerships | None named beyond the HKCRC incubation link |
| Funding | "Top-tier investors" (about page). **Rounds, amounts and investor names: not public.** No 2026 round identified |
| Scale | 5,000+ units shipped since 2023; headcount not public |

## Research and open-source activity

- **Lineage:** the core team is credited with leading VINS-Mono, VINS-Fusion and A-LOAM — widely used open-source SLAM frameworks from the HKUST robotics community. This is the company's main technical credential.
- **Company open source:** none found. No official GitHub org, no released datasets, models or ROS packages. The production engine ("SOTA-SLAM", tightly coupled multi-sensor fusion with TimeSync 3.0 hardware sync) is closed.
- **Publications:** the about page shows a "top-tier publications and awards" counter without listing any — specific papers under the SKYLANDX name are not public.
- **Technical writing:** one blog post (2026-09-20) with a seven-point field test for SLAM scanners (accuracy over distance, loop closure, corridor, glass, indoor–outdoor, stairwell, real-time feedback).
- **Claimed performance:** "over 20× efficiency improvement" for GPS-denied localization and mapping (about page; no methodology given).

## What would impress this company at the hackathon

**Everything in this section is inference** from the positioning above — not something SKYLANDX has stated.

What they probably want to see: (1) a MetaCam as a **live perception layer on someone else's robot**, not just a handheld scan; (2) a **Real2Sim loop** — scan, simulate, deploy in the same space; (3) a **vertical application** built on the exported data that a survey customer would pay for; (4) honest handling of hard SLAM conditions (glass, stairs, indoor–outdoor) rather than a demo in an easy room.

| Track | Idea that plays to their strategy | Why it would land |
|---|---|---|
| T01 Autonomous Urban Services | Scan a village route or hotel corridor once, then have a quadruped or wheeled robot from another vendor **relocalize against that map** and run a delivery with no GNSS | Demonstrates the "perception layer for any robot" story and prior-map relocalization |
| T02 Resilient & Safe City | **Scan-to-scan change detection**: two captures of a retaining wall, tunnel section, stairwell or snow-loaded structure, with automatic difference maps and measurements; optionally robot-carried for places unsafe for people | Matches their core use cases (GPS-denied mapping, infrastructure inspection) and adds the analytics layer they do not sell |
| T03 Sustainable City | **Scan-to-BIM / retrofit audit** of an older alpine building: surface areas, window ratios, volumes from the point cloud; or stockpile / snow-volume measurement | Uses the RCP / E57 export path and shows value beyond pretty point clouds |
| T04 Elderly Care & Rehabilitation | **Digital twin of a clinic room or guest apartment** used for a fall-hazard and accessibility audit (thresholds, door widths, clearances) and as the simulation scene for an assistive robot | Shows the Real2Sim and "3D data for embodied AI" angle in a setting with local relevance |

Things likely to count against a team (inference): treating the scanner as a camera, showing only a raw point cloud, or ignoring privacy when scanning clinic and spa spaces.

## Sources

- [SKYLANDX — About](https://skylandx.com/about/)
- [SKYLANDX — Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/)
- [SKYLANDX — Spatial Perception Robots](https://skylandx.com/spatial-intelligence-robots/)
- [SKYLANDX — Software platforms](https://skylandx.com/software-platforms/)
- [SKYLANDX — MetaCam Air 2](https://skylandx.com/metacam-air-2/)
- [SKYLANDX — MetaCam Pro](https://skylandx.com/metacam-pro/)
- [SKYLANDX — C01 LiDAR](https://skylandx.com/c01-slam-lidar/)
- [SKYLANDX — MetaCam Air 2 brochure (PDF, 2026-09)](https://skylandx.com/wp-content/uploads/MetaCam_Air_2_EN.pdf)
- [SKYLANDX — MetaCam Pro brochure (PDF, 2026-08)](https://skylandx.com/wp-content/uploads/MetaCam_Pro_EN_260818.pdf)
- [SKYLANDX — C01 LiDAR brochure (PDF, 2026-08)](https://skylandx.com/wp-content/uploads/EN_C01_LiDAR_BROCHURE.pdf)
- [SKYLANDX — Blog: What makes a SLAM scanner (2026-09-20)](https://skylandx.com/blog/slam-scanner-algorithm/)
- [3D Mag — SKYLANDX launches MetaCam Air 3 (2026-10-07)](https://www.3dmag.com/?p=14376)
- [SKYLANDX profile (earlier research: GEOSURF Japan distribution, UST and DirectIndustry listings)](SKYLANDX.md)
