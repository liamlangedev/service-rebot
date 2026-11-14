---
type: challenge-brief
company: "SKYLANDX"
slug: SKYLANDX
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# SKYLANDX × T01 Autonomous Urban Services — Brief

**Fit: 3/5** — Not a robot: it is the map, localization and digital-twin layer that makes someone else's delivery or maintenance robot find its way; strong as one part of a multi-vendor build.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **MetaCam Air 2** ✅ (handheld or robot-mounted via MetaCam Hub; **982 g** with battery, **150 min**, LiDAR 40 m @ 10 %, built-in RTK) · **C01 LiDAR** ✅ if a unit is on site (**420 g**, **IP67**, UDP) |
| Strongest proof point | **No named urban-service deployment is public.** Best evidence: official robotics page (2026) offering payload / live-perception / navigation integration on wheeled, quadruped and humanoid robots; C01 brochure targets service robots and AMRs; 5,000+ scanners shipped (company claim, Oct 2026) |
| Fastest credible 48-hour demo | Walk a hotel / clinic route with the Air 2 (minutes) → export PCD → 2D occupancy map → another vendor's robot runs a delivery on that prior map |
| Biggest risk | Developer access: Rosbridge / API details are not public ("contact SKYLANDX"); Air 2 is only **IP5X** (no water rating) for snow or rain |
| Pairs well with | Unitree (Go2 / B2 carrier) · AGIBOT, Galaxea, Galbot (wheeled manipulators) · D-Robotics (RDK bridge compute) · XREAL (twin / wayfinding view) |

## Why
- Removes the slowest part of a navigation demo: a **centimetre-level map** in one walk, no tripod.
- Works where GNSS fails (corridors, garages, tunnels) and adds **RTK** outdoors (0.8 cm + 1 ppm horizontal).
- Live pose, point cloud, images, IMU over a **Rosbridge WebSocket** — no custom driver (details from staff).
- Standard exports (**PCD / PLY / LAS / E57**, OBJ, 3DGS PLY) for Nav2, Open3D and simulators.
- Cold-rated: Air 2 and C01 both operate from **−20 °C to +55 °C**.

## Not a fit for
- Single-vendor builds: SKYLANDX has no actuators, payload bay or manipulator.
- Manipulation-heavy service tasks (cleaning, waste pick-up, handover) — it only tells the robot where it is.
- Teams unwilling to convert maps and bridge stacks themselves; no public SDK or sample code.

## Sources
- [MetaCam Air 2 brochure](https://skylandx.com/wp-content/uploads/MetaCam_Air_2_EN.pdf) · [C01 LiDAR brochure](https://skylandx.com/wp-content/uploads/EN_C01_LiDAR_BROCHURE.pdf) · [Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/) · [3D Mag, Oct 2026](https://www.3dmag.com/?p=14376)

⬆ [SKYLANDX profile](../SKYLANDX.md) · [Products and solutions](SKYLANDX-T01-2-Products-and-Solutions.md) · [Playbook](SKYLANDX-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
