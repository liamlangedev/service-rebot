---
type: challenge-brief
company: "Magiclab Robotics"
slug: Magiclab
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# Magiclab Robotics × T02 Resilient & Safe City — Brief

**Fit: 4/5** — Patrol and inspection is what Magiclab's quadrupeds are sold for, and the MagicDog ROS 2 SDK already ships SLAM and goal navigation; the catch is that the rugged models (Y1, T1) may not be the hackable units on site.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **MagicDog-Y1** (IP67, −20 to 55 °C, 45 kg payload, thermal / gas payload options) if a unit is available; otherwise **MagicDog EDU** (15.8 kg, 40° slope, ROS 2 SLAM + nav) as the realistic build base. On-site units are not confirmed ⚠️ unverified |
| Strongest proof point | Bipedal "traffic police" robot on duty with the **Wuxi Public Security Bureau at the 2026 Wuxi Marathon**; company also says **Y1 has inspected European energy facilities** (stated Sep 2026). Both company-sourced, no named site for the Y1 claim |
| Fastest credible 48-hour demo | MagicDog EDU maps a corridor or plant room, patrols saved waypoints, a vision model on a laptop flags an anomaly (person down, blocked exit, leak, heat source) and pushes an incident card with photo and map position |
| Biggest risk | Hardware edition: only **EDU** (MagicDog) and **Development Version** (Z1) allow SDK access; MagicDog EDU has **2D LiDAR only**, no stated IP rating or cold rating, so outdoor snow work is untested |
| Pairs well with | **SKYLANDX** MetaCam (3D baseline map / digital twin) · **D-Robotics** RDK X5 (on-dog edge inference) · **XREAL** glasses (operator view for teleop) |

## Why
- **Autonomy shortcut:** `magicdog_ros2_sdk` exposes mapping, map saving, localisation, `/goal_pose` navigation and a completion topic — no need to build a nav stack in 48 hours.
- **Purpose-built hardware exists:** Y1 is IP67 with expansion power and data ports and listed payloads such as infrared thermal imager, gas and acoustic sensors.
- **Public-safety track record:** "smart policing" solution shown at WRC (Aug 2026); provincial public-safety robot lab co-founded Jul 2026.
- **Open SDKs:** BSD-3-Clause C++ / Python SDKs per robot, including a Y1 SDK with a SLAM navigation service.
- **Leukerbad fit:** steep paths, tunnels, lift stations and spa plant rooms are natural legged-patrol targets.

## Not a fit for
- Manipulation-heavy response (opening valves, moving debris): arm payloads are small and T1 with arm is unlikely to be on site.
- Aerial or wide-area hazard monitoring (avalanche slopes, rockfall faces) — ground robots only.
- Teams that need certified outdoor ruggedness but only get a MagicDog EDU.

## Sources
- [MagicDog-Y1 product page](https://www.magiclab.top/en/dog-y) · [MagicDog product page](https://www.magiclab.top/en/dog) · [GitHub — magicdog_ros2_sdk](https://github.com/MagiclabRobotics/magicdog_ros2_sdk) · [GitHub — magicdog-y1_sdk](https://github.com/MagiclabRobotics/magicdog-y1_sdk)
- [QbitAI — MagicLab at WRC 2026 (Chinese)](https://www.qbitai.com/2026/08/477155.html) · [EqualOcean — IFA 2026](https://equalocean.com/news/2026090822169-magiclab-targets-european-logistics-robotics-showcase-slovenia-postal)

⬆ [Magiclab Robotics profile](../Magiclab.md) · [Products and solutions](Magiclab-T02-2-Products-and-Solutions.md) · [Playbook](Magiclab-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
