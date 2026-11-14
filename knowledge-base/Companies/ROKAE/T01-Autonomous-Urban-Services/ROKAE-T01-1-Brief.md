---
type: challenge-brief
company: "ROKAE Robotics"
slug: ROKAE
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# ROKAE Robotics × T01 Autonomous Urban Services — Brief

**Fit: 3/5** — Strong force-controlled *manipulation* half of a service robot with an open SDK; the "moves through the city" half must come from Helios / CMR (if on site) or another vendor's base.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **xMate SR3 / SR5** (48 VDC, 13.8 / 16.5 kg, 1.2 kg controller, IP54) or **CR7** (IP67) as a fixed service station; **Helios** if one is on site (⚠️ unverified what ROKAE brings) |
| Strongest proof point | SR cobots in **unmanned catering, robotic coffee and ice-cream** kiosks (official case studies, undated); **5 Helios** at Schaeffler Taicang (Oct 2026) — factory, not city |
| Fastest credible 48-hour demo | Unattended service kiosk / hand-off dock: camera + SR arm picks an ordered item and hands it to a guest or loads it into another vendor's delivery robot, using Cartesian impedance for safe contact |
| Biggest risk | No mobility unless Helios / CMR is present; gripper, camera and PC are not confirmed as supplied; CMR / Helios developer interfaces are thinly documented |
| Pairs well with | Unitree / AGIBOT / Genisom quadruped (delivery leg) · D-Robotics RDK (edge vision) · WUJI hand or Flexiv Grav gripper (end effector) · SKYLANDX (site map) |

## Why
- **Open, real developer stack:** Apache-2.0 `xCoreSDK` (C++ / Python / C#) and `rokae_ros2` (ROS 2 Humble, MoveIt 2 configs, URDFs, Gazebo) on GitHub — rare among arm vendors here.
- **1 kHz real-time C++ control** with joint / Cartesian impedance and direct torque on cobots — enables contact tasks (button pressing, wiping, door handles, handover).
- **Proven public-facing service use** (coffee, ice cream, unmanned catering), i.e. arms already run unattended near customers.
- **Light, 48 VDC SR arms** can ride on a third-party mobile base — with integration work.

## Not a fit for
- Outdoor street navigation, snow, stairs or steep terrain — ROKAE has no outdoor mobile platform.
- Teams wanting an out-of-the-box delivery or cleaning robot, or a ready VLA model (none public).
- Pure navigation / fleet projects with no manipulation step.

## Sources
- [ROKAE — SR cobots](https://www.rokae.com/en/product/show/349/SR-Cobots.html) · [xMate CR](https://www.rokae.com/en/product/show/545/xMateCR.html) · [Helios](https://www.rokae.com/en/product/show/596/Wheeled-Dual-Arm-Robot-Helios.html)
- [ROKAE — Commercial Services cases](https://www.rokae.com/en/case/208/Commercial-Services.html)
- [GitHub — xCoreSDK-CPP](https://github.com/RokaeRobot/xCoreSDK-CPP) · [rokae_ros2](https://github.com/RokaeRobot/rokae_ros2)
- [TechNode Global (PR Newswire) — Schaeffler Helios deployment, Oct 2026](https://technode.global/?p=996114)

⬆ [ROKAE Robotics profile](../ROKAE.md) · [Products and solutions](ROKAE-T01-2-Products-and-Solutions.md) · [Playbook](ROKAE-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
