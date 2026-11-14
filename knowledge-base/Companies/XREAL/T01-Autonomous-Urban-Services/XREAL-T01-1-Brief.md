---
type: challenge-brief
company: "XREAL"
slug: XREAL
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# XREAL × T01 Autonomous Urban Services — Brief

**Fit: 2/5** — Supporting role only: the glasses are the human-in-the-loop screen, head-pose input and POV camera for someone else's delivery or maintenance robot.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **One-series glasses (One Pro / 1 Pro+ / 1S) + XREAL Eye + Beam Pro** — plug-in HUD on any USB-C DisplayPort host; Unity SDK adds **6DoF head pose + RGB frames**. Air 2 Ultra or AURA only for world-anchored AR. |
| Strongest proof point (real deployment or demo + date) | **None in urban services.** Nearest: academic ActiveGlasses paper (arXiv, Apr 2026) using smart glasses for robot data collection. |
| Fastest credible 48-hour demo | **Supervisor HUD**: robot camera, map and status rendered on a laptop and shown in the glasses, so a walking operator supervises / takes over a delivery robot hands-free. No SDK needed. |
| Biggest risk | Plumbing: **no ROS 2 package**, Unity + Android host only (Beam Pro, Samsung S24 / S25; **not Android 16**); One + Eye has **no planes, anchors, image or hand tracking**. |
| Pairs well with (other vendors on site) | Unitree (Go2 / B2 delivery base) · Galaxea / Galbot / UniX AI (wheeled service robots) · D-Robotics (edge compute) · SKYLANDX (3D map for the HUD) |

## Why
- Autonomous robots in a real town still need **supervision and remote takeover**; glasses make that hands-free (87 g class, 57° FOV, up to 1,200 nits on 1 Pro+).
- **Zero-code path**: every model is a USB-C external display.
- One + Eye exposes **RGB frames (YUV_420_888)** and 6DoF pose — enough for "look at it, dispatch a robot to it".
- Cheap add-on (glasses USD 449–599, Eye USD 99) that does not block the core robot build.

## Not a fit for
- Teams expecting a robot body, navigation or autonomy from this vendor.
- World-locked AR on One-series hardware (needs Air 2 Ultra or AURA; on-site availability unconfirmed).
- ROS-only teams without Unity / Android skills who want more than a screen.

## Sources
- [XREAL docs — Compatibility](https://docs.xreal.com/XREALDevices/Compatibility) · [Access RGB Camera](https://docs.xreal.com/Camera/Access%20RGB%20Camera) · [arXiv 2604.08534](https://arxiv.org/abs/2604.08534) · [XREAL profile](../XREAL.md)

⬆ [XREAL profile](../XREAL.md) · [Products and solutions](XREAL-T01-2-Products-and-Solutions.md) · [Playbook](XREAL-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
