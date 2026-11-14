---
type: challenge-brief
company: "UniX AI"
slug: UniX-AI
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# UniX AI × T02 Resilient & Safe City — Brief

**Fit: 3/5** — A credible **indoor building-safety** robot (patrol, fire-equipment and fire-door checks, teleoperated intervention), but no outdoor or hazard-terrain capability and an unconfirmed developer interface.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Wanda 2.0** (8–16 h battery, 360° LiDAR, RGB + RGBD, 12 kg dual-arm payload); **Panther** if on site (reaches floor level, 2 m/s, omnidirectional base) |
| Strongest proof point | Official **Security Service** solution page: autonomous multi-floor patrol, fire-cabinet checks, fire-door closing tests, corridor anomaly detection (live Nov 2026). Security listed as a shipping sector (36Kr Japan, Dec 2025). **No named customer** |
| Fastest credible 48-hour demo | "Fire-safety round": robot patrols a corridor, verifies extinguisher present and fire door closes, flags a blocked escape route, pushes a report to a dashboard |
| Biggest risk | **No public SDK / docs.** Site claims "fully open software and hardware interfaces" for Wanda — ⚠️ unverified in practice. Flat indoor floors only |
| Pairs well with | Unitree or Genisom quadruped (outdoor / stairs scout) · SKYLANDX MetaCam (3D map) · XREAL (operator view) · D-Robotics RDK (edge perception) |

## Why
- UniX AI publishes a **security and fire-safety inspection** use case that needs arms, not just cameras: the robot **operates fire doors** to test auto-closing.
- **Proprietary remote teleoperation** (local and remote) is marketed for hazardous-material handling, rescue and industrial inspection — a natural "human stays out of danger" story.
- **8–16 h** runtime suits overnight patrol in hotels and clinics; multi-robot cloud scheduling is claimed.
- Leukerbad fit: hotels, thermal baths and rehab clinics have many fire doors, escape routes and vulnerable guests; staff are thin at night.

## Not a fit for
- Outdoor hazards: avalanche, rockfall, flood, snow, slopes, stairs. Wheeled base; slope, obstacle-crossing and IP rating **not published**.
- Tunnel, bridge, cable-car or power-line inspection.
- Teams needing a documented low-level API on day 1.

⬆ [UniX AI profile](../UniX-AI.md) · [Products and solutions](UniX-AI-T02-2-Products-and-Solutions.md) · [Playbook](UniX-AI-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)

## Sources
- [UniX AI — Security Service application page](https://www.unix-group.ai/Security)
- [UniX AI — Applications page (teleoperation, open interfaces claim)](https://www.unix-group.ai/Applications)
- [Wanda 2.0 product page](https://www.unix-group.ai/Wanda)
- [Panther product page](https://www.unix-group.ai/Panther)
- [36Kr Japan, 21 Dec 2025: shipments and sectors](https://36kr.jp/449686/)
- [Panther launch release, 8 Apr 2026 (TechNode Global / PR Newswire Asia)](https://technode.global/prnasia/unix-ai-introduces-panther-the-worlds-first-service-humanoid-robot-to-enter-real-household-deployment-powered-by-its-differentiated-wheeled-dual-arm-architecture/)
