---
type: challenge-brief
company: "AGIBOT"
slug: AGIBOT
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# AGIBOT × T02 Resilient & Safe City — Brief

**Fit: 3/5** — Capable quadruped line (D1 family) that AGIBOT itself positions for patrol, inspection and rescue, with an open C++ / Python SDK; but no public named safety deployment and no ready-made autonomy or perception stack, so expect integration work.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **D1 Edu / D1 Ultra** quadruped (5 kg payload, 40° slope, 16 cm stairs, open SDK). If on site: **D1 Max** (IP67, 25 kg, wheel-legged) or **D1 MaxPro** (IP67, 50 kg, −20 to 55 °C). On-site units are not confirmed. |
| Strongest proof point | Thin. AGIBOT lists "security inspection" among its production-ready solution areas (2026-04-17) and names security patrol / emergency rescue as D1 and D2 Max scenarios; **no named, dated safety deployment found**. |
| Fastest credible 48-hour demo | D1 with a companion computer + camera walks a patrol route (stairs, corridor, ramp), detects a hazard (person down, blocked exit, heat source) and pushes a geotagged alert to a dashboard. |
| Biggest risk | The D1 SDK gives motion + IMU only (`move(vx, vy, yaw_rate)`, joint commands); **camera, LiDAR, mapping and navigation are yours to add**. D1 Pro / Edu is rated **0–40 °C** — November outdoors in Leukerbad can be below that. |
| Pairs well with | D-Robotics (RDK X5 as perception brain) · SKYLANDX (MetaCam 3D baseline map) · XREAL (operator view) · Unitree / Genisom (mixed quadruped fleet) |

## Why
- D1 Ultra page names security patrol, inspection and emergency rescue as target uses; **IP54**, **3.7 m/s**, **6 ± 1 km** range.
- Open SDK (BSD-3-Clause, C++ / Python, x86_64 + aarch64) with high-level and low-level control; URDF for Isaac Sim and MuJoCo.
- Edu / Ultra expose Ethernet, USB, power, SBUS and UART for LiDAR, depth camera, RTK, 4G / 5G.
- Bigger siblings fit alpine rescue logistics: D1 Max **≥ 3.5 h** fully loaded, D1 MaxPro wades **20 cm** water and self-rights.
- X2 humanoid (documented ROS 2 SDK) can add an indoor "evacuation guide" role.

## Not a fit for
- Teams wanting turnkey autonomous inspection (maps, waypoints, anomaly models) out of the box.
- Aerial, underwater or heavy-manipulation hazard work; no fire- or explosion-rated product is public.
- D2 Max ("Level 3 autonomous" all-terrain) — announced April 2026, specs not public, unlikely on site.

## Sources
- [AGIBOT — D1 Ultra](https://www.agibot.com/products/D1Ultra) · [D1 Pro / Edu](https://www.agibot.com/products/D1_Pro) · [D1 Max](https://www.agibot.com/products/D1_Max) · [D1 MaxPro](https://www.agibot.com/products/D1_MaxPro)
- [AGIBOT — New generation of robots and models (2026-04-17)](https://www.agibot.com/article/231/detail/63.html)
- [GitHub — AgibotTech/agibot_D1_Edu-Ultra](https://github.com/AgibotTech/agibot_D1_Edu-Ultra)

⬆ [AGIBOT profile](../AGIBOT.md) · [Products and solutions](AGIBOT-T02-2-Products-and-Solutions.md) · [Playbook](AGIBOT-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
