---
type: challenge-brief
company: "Dobot Robotics"
slug: Dobot
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# Dobot Robotics × T02 Resilient & Safe City — Brief

**Fit: 2/5** — Supporting role only: Dobot supplies the easy-to-program "hands" (arm + API) for an inspection or remote-intervention system, but has no mobility, no field ruggedness on the likely on-site kit, and no documented safety / emergency deployments.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Nova 2** (11 kg arm, 1.3 kg controller, **30–60 V DC**, 100 W typical) as the manipulator on someone else's mobile base; **CR5A / Magician E6** for a fixed inspection or teleop cell. **CRA-IP68** (CR5AP / CR10AP / CR20AP) is the rugged option but unlikely on site ⚠️ unverified |
| Strongest proof point | **None in this domain.** Closest: chemical-industry page (undated) pitching cobots to keep staff out of heat and toxic gas; **CRH** (Oct 2026) lists "inspection" as a use. No named safety or utility customer found |
| Fastest credible 48-hour demo | Arm + wrist camera that **inspects a mock control panel** (reads gauges, spots faults) and then **acts** (flips a breaker, closes a valve) — autonomously or by click-to-act teleoperation |
| Biggest risk | The robot never leaves the table: fixed base, **0–50 °C**, IP54 arm / IP20 controller (Nova). Judges may see a factory cell, not a city-resilience system |
| Pairs well with | Unitree or Genisom quadruped (mobility) · SKYLANDX MetaCam (3D map / digital twin) · XREAL (operator view) · D-Robotics RDK (edge perception) · WUJI hand (dexterous end-effector) |

## Why
- **Fast start:** Python V4 SDK (moves, ServoJ / ServoP streaming, drag-teach, collision levels, tool I/O) plus a ROS 2 Humble package with MoveIt + Gazebo.
- **Mobile-mount friendly:** Nova runs from a DC rail with a palm-size controller.
- **Teleop path exists:** X-Trainer leader–follower rig and Atom Max VR/MR teleop suit "remote hands in a hazard zone" — if on site.
- **Force sensing is not default:** needs CRAF (flange force sensor) or CRH.

## Not a fit for
- Search-and-rescue, outdoor patrol, snow or steep terrain — anything where the robot itself must move.
- Wide-area hazard monitoring (avalanche, rockfall, flood): no sensing or mapping products.
- Teams wanting a ready-made safety solution: none exists.

## Sources
[Nova series](https://www.dobot-robots.com/products/nova-series/dobot-nova-series.html) · [CRA-IP68](https://www.dobot-robots.com/products/cra-series/dobot-cra-ip68-series.html) · [Chemical industry page](https://www.dobot-robots.com/industries/chemical.html) · [CRH launch news](https://www.dobot-robots.com/insights/news/dobot-unveils-three-new-products-at-its-2026-robotics-ecosystem-conference.html) · [TCP-IP-Python-V4](https://github.com/Dobot-Arm/TCP-IP-Python-V4) · [DOBOT_6Axis_ROS2_V4](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V4)

⬆ [Dobot Robotics profile](../Dobot.md) · [Products and solutions](Dobot-T02-2-Products-and-Solutions.md) · [Playbook](Dobot-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
