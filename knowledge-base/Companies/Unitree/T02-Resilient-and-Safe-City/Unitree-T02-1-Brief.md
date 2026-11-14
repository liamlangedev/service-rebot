---
type: challenge-brief
company: "Unitree Robotics"
slug: Unitree
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 5
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# Unitree Robotics × T02 Resilient & Safe City — Brief

**Fit: 5/5** — Inspection and fire rescue are Unitree's two official industry solution lines, and its quadrupeds are the fastest way on site to get a sensor platform over stairs, slopes and snow.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Go2 EDU** (15 kg, 4D LiDAR L2, depth camera, optional Orin, full SDK) for the build; **B2 / A2 / As2** (IP67 / IP56 / IP54, 4–6 h) if a unit is released to teams |
| Strongest proof point | Official inspection solution with listed Chinese sites, including a power cable tunnel patrolled by **six B2 robots** (undated, per Unitree); **two B2 firefighting units** handed to the Qingdao fire and rescue support team and used in drills (per Unitree, reported **6 May 2025**) |
| Fastest credible 48-hour demo | Go2 EDU patrols a mapped indoor / outdoor route, detects a "hazard" (person down, heat source, blocked path) with a camera model on the Orin, and pushes an alert with position and photo to an operator dashboard |
| Biggest risk | Getting the wrong variant: **Go2 Air / Pro have no SDK access**, X is partial (fallback: unofficial community go2_ros2_sdk over WebRTC). No open navigation stack from Unitree — autonomy is your integration work |
| Pairs well with | SKYLANDX (MetaCam 3D scan / digital twin) · XREAL (AR operator view) · D-Robotics (RDK edge-AI board as payload computer) · Flexiv / ROKAE arms for a fixed "repair" station |

## Why
- **Terrain is the product:** Go2 climbs 40° slopes and ~16 cm steps; B2 handles >45° slopes, 40 cm steps, IP67, −20 to 55 °C — a match for Leukerbad's stairs, snow and steep paths.
- **Domain payloads exist:** thermal + zoom gimbal, gas sensor, acoustic imager, auto-charging dock, explosion-proof **B2-Ex** (Ex IIB T4 Gb) — whether any are on site is not confirmed.
- **Mature developer path:** unitree_sdk2 (C++ / Python), unitree_ros2, unitree_mujoco; LiDAR odometry and mapping via point_lio_unilidar.
- **Largest community code base** of any vendor on site, so most problems have a published answer.

## Not a fit for
- Manipulation-heavy response (opening valves, moving debris): arms are light (D2 **3 kg** rated) and may not be on site.
- Aerial or wide-area sensing (avalanche slopes, rockfall faces) — ground robots only.
- Teams wanting turnkey autonomous patrol: the commercial inspection software is not an open hackathon tool.

## Sources
- [Unitree — intelligent inspection solution](https://www.unitree.com/mobile/industry/electricity) · [Unitree — fire rescue solution](https://www.unitree.com/mobile/industry/fireRescue) · [Unitree B2](https://www.unitree.com/b2) · [Unitree B2-Ex](https://www.unitree.com/B2-Ex) · [Unitree Go2](https://www.unitree.com/go2) · [WinFuture, 6 May 2025](https://winfuture.de/news,150757.html) · [go2_ros2_sdk (community)](https://github.com/abizovnuralem/go2_ros2_sdk)

⬆ [Unitree Robotics profile](../Unitree.md) · [Products and solutions](Unitree-T02-2-Products-and-Solutions.md) · [Playbook](Unitree-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
