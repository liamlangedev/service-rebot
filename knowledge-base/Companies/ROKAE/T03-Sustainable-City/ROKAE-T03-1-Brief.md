---
type: challenge-brief
company: "ROKAE Robotics"
slug: ROKAE
challenge: T03
challenge_title: "Sustainable City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# ROKAE Robotics × T03 Sustainable City — Brief

**Fit: 3/5** — A solid force-controlled arm for sorting, disassembly or picking cells, but ROKAE has no sustainability-specific product, model or dataset; you bring the perception and the idea.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **xMate SR5** (5 kg, 919 mm, 48 VDC, 16.5 kg) or **CR7** (7 kg, 988 mm, IP67) on a table with your own camera and gripper; **AR5** 7-DoF arm if that is what is on site |
| Strongest proof point | **CR35 parcel picking and sorting**: 13M+ real parcel-handling operations, 0.01% grasp-damage rate (ROKAE case page, listed 12 Nov 2026, customer not named). Adjacent: CR35 lithium-battery cell-module handling; tomato and grape harvesting cases (no details published) |
| Fastest credible 48-hour demo | Camera + open-vocabulary detector + SR/CR arm sorting mixed waste (PET, cans, glass, paper) into bins, with force-controlled "press test" to tell rigid from soft items |
| Biggest risk | Gripper, camera and compute are **not confirmed as supplied**; SDK real-time modes and ROS 2 details ⚠️ unverified — the first 6 hours decide everything |
| Pairs well with | D-Robotics (RDK X5 edge AI) · WUJI (dexterous hand) · SKYLANDX (3D scan) · Unitree / Genisom quadruped (mobile litter collection) · Galbot / Galaxea (grasp models) |

## Why
- **Force control is the differentiator**: adjustable Cartesian stiffness (SR: 0–3000 N/m) helps with unknown, deformable or fragile waste and with unscrewing / prying in repair and disassembly tasks.
- **Proven in sorting-like work at scale** (CR35 parcels; JD Logistics "Canglang" picking robot uses AR5 arms, 99.9% picking accuracy).
- **Low-power, portable hardware**: 48 VDC arms, 1.2 kg controller — fits a "low-energy automation" story and a desk-sized demo.
- **Documented SDK** in C++, Python and C# plus a ROS 2 package.

## Not a fit for
- Outdoor, mobile or environmental-monitoring builds (snow, air, water) — arms are fixed-base; Helios / CMR are unlikely to be on site.
- Teams that want a ready VLA or waste-sorting model — none is public from ROKAE.
- EV-charging automation as a ROKAE-proven use case — no public ROKAE deployment found.

⬆ [ROKAE Robotics profile](../ROKAE.md) · [Products and solutions](ROKAE-T03-2-Products-and-Solutions.md) · [Playbook](ROKAE-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
