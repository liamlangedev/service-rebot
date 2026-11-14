---
type: challenge-brief
company: "ROKAE Robotics"
slug: ROKAE
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# ROKAE Robotics × T02 Resilient & Safe City — Brief

**Fit: 2/5** — Supporting role only: a very good force-controlled "remote hand", but nothing from ROKAE moves over terrain, senses hazards or has a public track record in emergency or infrastructure work.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | Fixed-base **xMate SR3 / SR5** or **CR7** (arm body **IP67**) as a teleoperated contact arm; **AR5** (7-DoF, **10 kg**, 48 V DC) if another vendor's mobile base carries it; **Helios** only if one is on site (indoor floors) |
| Strongest proof point | None in this domain. Nearest: **five Helios at Schaeffler Taicang** doing handling, assembly and inspection (factory, Oct 2026); a teleoperated ultrasound robot on xMate ER7 Pro (undated integrator case) shows remote force-controlled contact |
| Fastest credible 48-hour demo | "Remote hands for a cut-off plant room": operator teleoperates the arm to turn a valve, flip a breaker and press a stop button on a mock utility panel, with Cartesian impedance capping contact force |
| Biggest risk | On-site hardware is unconfirmed; arms are rated **0–50 °C**, controller cabinet **IP54**, gripper and camera not confirmed — the arm cannot reach a hazard on its own |
| Pairs well with | Unitree / AGIBOT D1 / Genisom quadrupeds (mobility) · SKYLANDX MetaCam (3D map) · XREAL (operator view) · WUJI Hand or Flexiv Grav gripper (end-effector) · D-Robotics RDK (edge perception) |

## Why
- **Force control is the real asset:** adjustable Cartesian stiffness (SR 0–3000 N/m, CR up to 18000 N/m) and CR flange force accuracy of **0.5 N** make contact with unknown valves, doors and surfaces safe.
- **Open developer stack:** xCore SDK on GitHub (C++ / Python / C#, Apache-2.0) with real-time control up to **1 kHz** including impedance and torque modes; `rokae_ros2` for ROS 2 Humble with MoveIt 2 and Gazebo.
- **No T02 product:** no outdoor mobility, no hazard sensors, no rescue or infrastructure-inspection reference on ROKAE's site.
- **Mobility is factory-grade only:** Helios (**160 kg**, IP not listed) and CMR AMRs are for flat indoor floors.

## Not a fit for
- Outdoor, snow, slope or rubble scenarios; search-and-rescue mobility.
- Wide-area monitoring, patrol or mapping (no ROKAE sensing or autonomy stack for it).
- Teams that want a ready-made emergency-response application to extend.

⬆ [ROKAE Robotics profile](../ROKAE.md) · [Products and solutions](ROKAE-T02-2-Products-and-Solutions.md) · [Playbook](ROKAE-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)

## Sources
- [ROKAE — xMate CR series](https://www.rokae.com/en/product/show/545/xMateCR.html)
- [ROKAE — Humanoid Force-Controlled Arm AR](https://www.rokae.com/en/product/show/595/Humanoid-Force-Controlled-Arm-AR.html)
- [ROKAE — Wheeled Dual-Arm Robot Helios](https://www.rokae.com/en/product/show/596/Wheeled-Dual-Arm-Robot-Helios.html)
- [GitHub — RokaeRobot/xCoreSDK-CPP](https://github.com/RokaeRobot/xCoreSDK-CPP)
- [GitHub — RokaeRobot/rokae_ros2](https://github.com/RokaeRobot/rokae_ros2)
- [TechNode Global (PR Newswire) — 10,000th AR arm, Schaeffler deployment, Oct 2026](https://technode.global/?p=996114)
- [ROKAE Japan — teleoperated ultrasound robot case (ER7 Pro)](https://www.rokae.com/jp/case/show/1189/%E9%81%A0%E9%9A%94%E6%93%8D%E4%BD%9C%E5%9E%8B%E8%B6%85%E9%9F%B3%E6%B3%A2%E8%A8%BA%E6%96%AD%E3%83%BB%E6%B2%BB%E7%99%82%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88.html)
