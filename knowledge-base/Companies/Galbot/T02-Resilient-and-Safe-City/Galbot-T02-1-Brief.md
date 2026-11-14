---
type: challenge-brief
company: "Galbot"
slug: Galbot
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# Galbot × T02 Resilient & Safe City — Brief

**Fit: 2/5** — Supporting role only: a strong indoor pick-and-hand-over robot with no safety, inspection or emergency track record and no outdoor capability.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Galbot G1** (wheeled dual-arm, 5 kg per arm, 3D LiDAR, wrist F/T, **8 h** runtime, IP54, **0–40 °C, flat indoor floors only**) + GalbotSDK V1.10.0 (C++ / Python) |
| Strongest proof point (real deployment or demo + date) | None in this domain. Closest: G1 running **7x24 in 100+ instant-retail warehouses** and 24-hour pharmacies (Laobaixing Shanghai, 2026-09-28) — proof of unattended reliability, not of safety work |
| Fastest credible 48-hour demo | Indoor "inspect and report" patrol: SDK waypoint navigation + camera snapshots + a VLM flagging blocked exits or missing extinguishers; or an unmanned emergency-supply point that picks first-aid items on request |
| Biggest risk | Wrong tool for the track: cannot leave the building, no thermal or gas sensing, and Galbot's own "site inspection" kit is still **planned**, so you build the application layer from zero |
| Pairs well with (other vendors on site) | Unitree / Genisom AI / AGIBOT D1 quadrupeds (outdoor scouting) · SKYLANDX MetaCam (3D map) · XREAL (remote operator view) · D-Robotics RDK (extra sensor node) |

## Why
- **No domain evidence:** no Galbot inspection, patrol, security or emergency deployment was found (searched English and Chinese sources, Nov 2026).
- **Real strengths transfer partly:** unattended 24/7 operation, open-vocabulary grasping and built-in mapping / localization / point-to-point navigation are useful for "keep services running during disruption".
- **A robot with hands is the differentiator:** quadrupeds can look; G1 can press, open, fetch and hand over (reach floor to 2.1 m).
- **Developer access is good:** free SDK with high- and low-level control, URDF / MJCF / USD assets.
- **Direction of travel:** site-inspection kit on the developer roadmap; Sinopec is an investor (Mar 2026) — hints, not products.

## Not a fit for
- Anything outdoors in Leukerbad: snow, slopes, stairs, rockfall or avalanche zones.
- Search-and-rescue, firefighting or hazardous-atmosphere work (no ratings, no sensors for it).
- Teams wanting a ready-made inspection or security stack.

## Sources
- [Galbot profile (this repo)](../Galbot.md) · [G1 product page](http://www.galbot.com/g1/) · [Developer portal](https://developer.galbot.com/?lang=en) · [GalbotSDK](https://github.com/GalaxyGeneralRobotics/GalbotSDK) · [TechNode, 2026-03-02](https://technode.com/2026/03/02/humanoid-robot-maker-galbot-raises-rmb-2-5-billion/)

⬆ [Galbot profile](../Galbot.md) · [Products and solutions](Galbot-T02-2-Products-and-Solutions.md) · [Playbook](Galbot-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
