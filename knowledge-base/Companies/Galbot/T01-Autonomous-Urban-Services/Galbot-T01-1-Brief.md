---
type: challenge-brief
company: "Galbot"
slug: Galbot
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# Galbot × T01 Autonomous Urban Services — Brief

**Fit: 4/5** — Proven 24/7 robot shopkeeper and pharmacy picker with a real SDK; strong for indoor "fetch, vend, hand over, guide" services, not for streets, snow or stairs.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Galbot G1** (wheeled dual-arm, 5 kg per arm, 1.5 m/s, 8 h, 3D LiDAR, wrist F/T) + **GalbotSDK V1.10.0** (C++ / Python; mapping, point-to-point navigation, voice). Which robot is on site is unconfirmed ⚠️ |
| Strongest proof point | **Space Capsule** robot kiosks at **170+ locations in 40+ cities** (official site, 2026), incl. **10 tourism-retail capsules at Guiyang landmarks since 2025-12-31** (with China Mobile Guizhou; drinks, voice guide, 24/7); G1 7x24 in **100+ instant-retail warehouses** |
| Fastest credible 48-hour demo | "Robot concierge kiosk": guest asks by voice, G1 drives to a shelf, picks the named item (open-vocabulary grasp) and hands it over at a counter |
| Biggest risk | Indoor flat floor only (wheeled, IP54, 0-40 °C); grasp stack and SDK version on the demo unit unknown until you ask |
| Pairs well with | Unitree or Genisom quadruped (outdoor leg) · XREAL (staff / guest AR view) · SKYLANDX (fast 3D map of the venue) · D-Robotics (edge box at shelf or locker) |

## Why
- Retail, pharmacy and kiosk service is Galbot's core commercial business, not a side demo.
- SDK has built-in **mapping, localisation, obstacle avoidance and point-to-point navigation** — no need to bring a nav stack.
- A **welcome / guide kit** (knowledge base, persona, voice) is live on the developer portal.
- **GraspVLA** has open weights (~9 GB GPU, ~5 Hz) but targets a Franka-style arm; G1 port not documented. NavFoM / TrackVLA / UrbanVLA have **no usable public weights**.
- Leukerbad hotel, spa and clinic lobbies are the indoor, flat, people-facing setting G1 works in.

## Not a fit for
- Street delivery, snow, waste collection, slopes, stairs or wet ground.
- Loads above 10 kg (both arms).
- Teams that need a ROS 2 runtime bridge (only description packages are documented).

## Sources
- [Galbot G1 product page](http://www.galbot.com/g1/)
- [Galbot developer portal](https://developer.galbot.com/?lang=en)
- [GitHub org GalaxyGeneralRobotics](https://github.com/GalaxyGeneralRobotics)
- [Guiyang government: robotic tourism-retail capsules](https://fgw.english.guiyang.gov.cn/2026-01/26/c_1157846.htm)
- [GraspVLA repository (PKU-EPIC)](https://github.com/PKU-EPIC/GraspVLA)

⬆ [Galbot profile](../Galbot.md) · [Products and solutions](Galbot-T01-2-Products-and-Solutions.md) · [Playbook](Galbot-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
