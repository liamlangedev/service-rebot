---
type: challenge-brief
company: "Genisom AI"
slug: Genisom-AI
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# Genisom AI × T01 Autonomous Urban Services — Brief

**Fit: 4/5** — Rugged legged carriers plus an open ROS 2 navigation stack and simulator: strong for "carry, follow, guide" over stairs, slopes and snow; no arm by default and no proven delivery deployment. Drops to 3 if only a base L1 (no EDU sensor kit) is on site.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Genisom L2** if on site (16 kg payload, about 5.5 h, IP66, −20 to 55 °C, navigation + GLUE following built in). Otherwise **L1 EDU** (Orin NX, 3D LiDAR, depth camera, GNSS) + **RoamerX Lite** (ROS 2 Humble / Nav2). On-site models not confirmed. |
| Strongest proof point | M1 autonomously followed a runner through a half marathon (21 km, about 3 h, no remote control), Beijing Yizhuang, 2026. No named delivery or municipal customer is public. |
| Fastest credible 48-hour demo | "Carry-and-follow porter": the dog follows a guest with luggage or supplies, then returns alone to a saved waypoint. |
| Biggest risk | Access level: public SDKs are **C++ only**, high-level (velocity, modes, telemetry); navigation-goal and following APIs are undocumented; RoamerX Lite real-robot bring-up is marked TODO. L1 / L1-W are rated only **0–40 °C, IP54**. |
| Pairs well with | D-Robotics (extra perception compute) · SKYLANDX (pre-scan route into a map) · XREAL (operator / guest AR view) · Flexiv, Dobot or ROKAE arm as fixed loading station |

## Why
- **Terrain is the differentiator.** Leukerbad routes mean stairs, steep lanes, kerbs and snow, where wheeled delivery robots stop. L2 / M1 are rated to −20 °C and IP66 / IP67.
- **Vendor positioning matches.** The L2 page lists short-distance delivery; the WAIC 2026 release names communities, logistics and accessibility.
- **Start without hardware.** MATRiX simulator, URDFs, RoamerX Lite and a zero-shot vision-language navigation baseline are on GitHub.
- **Real payload.** 8 kg (L1), 10 kg (L1-W), 16 kg (L2), about 30 kg (M1) continuous.

## Not a fit for
- Manipulation tasks (doors, pick-and-place, cleaning, bins) unless an M1 + TA01 arm is on site; TA01 specs and API are not public.
- Python-only teams expecting a ready "go to room 12" API.
- Smooth-floor indoor hospitality service, where a wheeled platform is simpler.

## Sources
[L2 page](https://www.genisomai.com/en/product-robot/L2) · [M1 page](https://www.genisomai.com/en/product-robot/M1) · [WAIC 2026 news](https://www.genisomai.com/en/newsdetail/GENISOM-AI-at-WAIC-2026) · [RoamerX Lite](https://github.com/zsibot/genisom_roamerx_open) · [GEN2 SDK](https://github.com/zsibot/genisom_robot_sdk) · [L1 SDK](https://github.com/zsibot/genisom_L1_sdk)

⬆ [Genisom AI profile](../Genisom-AI.md) · [Products and solutions](Genisom-AI-T01-2-Products-and-Solutions.md) · [Playbook](Genisom-AI-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
