---
type: challenge-brief
company: "Unitree Robotics"
slug: Unitree
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# Unitree Robotics × T01 Autonomous Urban Services — Brief

**Fit: 4/5** — Best mobility base on site for stairs, slopes and snow, with a mature SDK; but navigation and delivery logic are yours to build, and Unitree has no confirmed delivery or municipal-service deployment.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Go2 EDU** (15 kg, ~7–8 kg payload, 4D LiDAR L2, full SDK, optional Orin). If on site: **Go2-W / As2-W** (wheel-legged, faster on pavement), **G1-D Flagship** (wheeled dual-arm, indoor service) |
| Strongest proof point | No confirmed delivery / city-service deployment found. Nearest: Unitree's official **autonomous inspection solution** (B2-class route patrol) and the **G1-D** page naming "Service" and "Retail" as target scenarios (2026). A 2024 Mount Tai cargo / waste-carrying trial with B2 is widely reported but ⚠️ unverified here |
| Fastest credible 48-hour demo | Go2 EDU maps a route with its LiDAR, then carries a parcel (≤ 7 kg) between named waypoints including a staircase, with QR or voice handover |
| Biggest risk | Wrong variant (**Go2 Air / Pro have no official SDK**), and no first-party open navigation stack — SLAM + Nav2 integration eats day 1 |
| Pairs well with | SKYLANDX (pre-scanned 3D map) · D-Robotics (extra edge compute) · XREAL (AR dispatcher view) · Flexiv / Dobot / ROKAE (fixed arm loading station) · Galbot / Galaxea (manipulation at endpoints) |

## Why
- **Terrain is the Leukerbad problem**, and legs solve it: Go2-W clears ~70 cm drops and 35° slopes; As2-W does 30 cm stairs, ~45°, IP54, −20 to 55 °C.
- **Fast start:** high-level velocity API via unitree_sdk2 (C++ / Python) and unitree_ros2 (Humble); LiDAR point cloud on a ROS 2 topic.
- **Community shortcut:** go2_ros2_sdk (unofficial, 1.1k stars) already wires slam_toolbox + Nav2 + COCO detection.
- **Useful payload for the size:** Go2 ~7–8 kg, As2-W ~16 kg walking, B2-W > 40 kg.
- **Largest code base** of any vendor on site (sim, RL, teleop) for fallbacks.

## Not a fit for
- Manipulation-heavy service tasks (opening doors, shelf picking) unless a G1-D or an arm is actually available.
- Long unattended shifts: Go2 runs **1–2 h** (2–4 h with the large battery).
- Teams wanting a turnkey delivery / fleet product — none exists here.

## Sources
[Go2-W](https://www.unitree.com/go2-w) · [As2-W](https://www.unitree.com/As2-W) · [B2-W](https://www.unitree.com/b2-w) · [G1-D](https://www.unitree.com/G1-D) · [Go2](https://www.unitree.com/go2) · [inspection solution](https://www.unitree.com/mobile/industry/electricity) · [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2) · [go2_ros2_sdk (community)](https://github.com/abizovnuralem/go2_ros2_sdk)

⬆ [Unitree Robotics profile](../Unitree.md) · [Products and solutions](Unitree-T01-2-Products-and-Solutions.md) · [Playbook](Unitree-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
