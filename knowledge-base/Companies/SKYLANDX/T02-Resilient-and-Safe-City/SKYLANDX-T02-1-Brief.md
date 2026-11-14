---
type: challenge-brief
company: "SKYLANDX"
slug: SKYLANDX
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# SKYLANDX × T02 Resilient & Safe City — Brief

**Fit: 4/5** — Best mapping / situational-awareness sensor on site for this track (GPS-denied SLAM, cm-level scans, digital twins), but it is a sensor, not a robot, and its live API is undocumented.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **MetaCam Air 2** (619 g handheld LiDAR + panoramic vision + RTK, robot-mountable via MetaCam Hub) + MetaCam Studio / Skyland Cloud. On-site availability is a best guess — confirm at the booth |
| Strongest proof point (real deployment or demo + date) | No named, dated safety deployment is public. Closest: official case "Autonomous Scanning in High-Risk Zones" (robots re-scanning tanks, tunnels, boiler rooms; undated, customer unnamed) and facility mapping for Deluke Chemical (undated). Company claim: **5,000+ units shipped** (Oct 2026) |
| Fastest credible 48-hour demo | Scan a corridor / plant room / gallery **before and after** a staged incident, auto-detect what changed (debris, blocked exit, deformation) with open-source cloud-to-cloud comparison, show it in a 3D responder view. Needs only file exports (PLY / LAS / E57), no API |
| Biggest risk | Live data (Rosbridge WebSocket, pose / map APIs) is "on request" — no public SDK, docs or GitHub. IP rating, cold-weather limits and battery life are not public |
| Pairs well with (other vendors on site) | Unitree Go2 / B2, Genisom, Magiclab MagicDog or AGIBOT D1 (carrier quadruped) · XREAL (AR hazard overlay) · D-Robotics RDK (edge inference) |

## Why
- Official use cases match the track directly: GPS-denied tunnels / mines "with no human entry", indoor safety patrols (cracks, leaks, hazards), bridges, dams, substations, utility corridors.
- SLAM runs on the device in real time with no prior map; relocalization against an earlier scan enables repeat inspection.
- One capture gives point cloud + mesh (OBJ) + 3DGS (PLY) — a ready digital twin for responders or simulation.
- The safest demo path needs zero vendor API: export files, analyse with Open3D / CloudCompare.
- Leukerbad has real targets: road galleries, cable-car stations, thermal plant rooms, rockfall slopes.

## Not a fit for
- Teams that need a robot that moves or manipulates — SKYLANDX only supplies perception.
- Builds that depend on a documented open SDK from hour 0.
- Gas, thermal or radiation hazard sensing — LiDAR + RGB only.

## Sources
- [SKYLANDX — Spatial Perception Robots](https://skylandx.com/spatial-intelligence-robots/) · [Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/) · [MetaCam Air 2](https://skylandx.com/metacam-air-2/) · [MetaCam Pro](https://skylandx.com/metacam-pro/)
- [SKYLANDX — Case studies: Industrial inspection](https://skylandx.com/case-studies-industrial-inspection) · [Case studies: Surveying](https://skylandx.com/case-studies-surveying)
- [3D Mag — MetaCam Air 3 launch, 2026-10-07 (via company profile)](https://www.3dmag.com/?p=14376)

⬆ [SKYLANDX profile](../SKYLANDX.md) · [Products and solutions](SKYLANDX-T02-2-Products-and-Solutions.md) · [Playbook](SKYLANDX-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
