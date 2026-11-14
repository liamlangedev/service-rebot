---
type: challenge-brief
company: "SKYLANDX"
slug: SKYLANDX
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# SKYLANDX × T04 Elderly Care & Rehabilitation — Brief

**Fit: 2/5** — Supporting role only: a centimetre-level 3D map / 3DGS twin of a clinic room or apartment; no care product, no care deployment, nothing that assists a person physically.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **MetaCam Air 2** ✅ (619 g handheld LiDAR + vision, < 1 cm relative accuracy, robot-mountable) — likeliest loaner; **MetaCam Lite** ✅ (interiors model) if on site. Plus MetaCam Studio + Skyland Cloud (3DGS). |
| Strongest proof point (real deployment or demo + date) | **None in care or rehab** (nothing public). Closest: official Robotics & Physical AI page (checked 2026-11-14) lists residential interiors for Real2Sim, robot training data and relocalization — no named customer. |
| Fastest credible 48-hour demo | Scan a rehab room / corridor → point cloud + 3DGS → automatic **fall-hazard and accessibility audit** (door widths, thresholds, clutter on walking routes) in a browser viewer. |
| Biggest risk | **No public SDK, docs or GitHub** — live pose / streams (Rosbridge WebSocket) depend on on-site staff; otherwise offline exports only. Privacy when scanning care rooms. |
| Pairs well with (other vendors on site) | Galaxea / Galbot / UniX AI / Spirit AI (prior map for fetch-and-carry) · Unitree / Genisom quadruped (night rounds) · XREAL (AR overlay) · D-Robotics (edge compute) |

## Why
- **Map-first shortcut:** one walk-through gives any assistive robot a metric prior map; relocalization without remapping is an official claim.
- **Standard exports** (PLY / PCD / LAS / E57, OBJ mesh, 3DGS PLY) make an offline pipeline possible with zero API access.
- **Accuracy fits the job:** < 1 cm is enough for wheelchair / rollator clearances and step heights.
- **Leukerbad angle:** rehab clinics and spa hotels are credible sites for a "ward / home safety twin".

## Not a fit for
- Physical assistance (lifting, feeding, massage, exoskeleton) — no actuator, arm or force control.
- Live person tracking or fall detection — it is a mapping scanner, not a people sensor.
- Teams needing a documented SDK in the first hour.

## Sources
- [SKYLANDX — Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/) · [MetaCam Air 2](https://skylandx.com/metacam-air-2/) · [MetaCam Lite](https://skylandx.com/metacam-lite/) · [Software platforms](https://skylandx.com/software-platforms/) · [Company profile](../SKYLANDX.md)

⬆ [SKYLANDX profile](../SKYLANDX.md) · [Products and solutions](SKYLANDX-T04-2-Products-and-Solutions.md) · [Playbook](SKYLANDX-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
