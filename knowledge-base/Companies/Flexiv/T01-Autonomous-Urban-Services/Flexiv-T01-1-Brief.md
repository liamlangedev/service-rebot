---
type: challenge-brief
company: "Flexiv Robotics"
slug: Flexiv
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# Flexiv Robotics × T01 Autonomous Urban Services — Brief

**Fit: 3/5** — Excellent *hands*, no *legs*: use Flexiv as the contact-rich manipulation station (load, plug in, wipe, hand over) inside a multi-vendor urban-service system, not as the robot that moves through the city.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Rizon 4 / 4s + Grav gripper** (4 kg, 876–919 mm, force sensing 0.1 / **0.03 N**, IP65). FMR 300 AMR or AICO only if actually on site (unlikely, 185–395 kg) |
| Strongest proof point | **Mobile CNC tool changing** demo (arm on mobile base) at Hannover Messe, April 2026; FMR 300 AMR launched Dec 2025 for lab automation and machine tending. Both are factory / lab, **not** urban service |
| Fastest credible 48-hour demo | Fixed "service dock": the arm loads a parcel into, or plugs a charger into, an imprecisely parked mobile robot from another vendor, finding the target by touch |
| Biggest risk | No mobility and no navigation stack you can use on day 1; robot-side **RDK license** and RDK version (v1.x for Rizon vs v2.x for Enlight) must match your code |
| Pairs well with | Unitree (Go2 / B2 as carrier), D-Robotics (RDK X5 for vision), SKYLANDX (site scan), Galaxea / Galbot (roaming manipulator) |

## Why
- Force-guided primitives (Contact, SearchHole, InsertComp, Polish, GraspComp) tolerate centimetre-level parking error — exactly what a delivery robot produces when it docks.
- **IP65** arm and IP67 gripper suit wet wiping and cleaning tasks.
- Python RDK with non-real-time primitives gets a first contact motion running in hours; ROS 2 + MoveIt and Isaac Sim are available.
- Plug-insertion is a published NVIDIA Isaac reference workflow (Rizon 4 + Grav, Sept 2026).

## Not a fit for
- Street or building navigation, last-mile driving, stairs, snow, outdoor work below 0 °C.
- Teams that want one vendor to cover the whole "move + deliver" loop.
- Guide / concierge robots where conversation, not contact, is the value.

## Sources
- [Flexiv — Robot System page](https://www.flexiv.com/product/robot-system) · [Flexiv — primitives list](https://www.flexiv.com/software/primitives) · [GitHub — flexiv_ros2](https://github.com/flexivrobotics/flexiv_ros2)
- [Robotics 24/7 — Hannover Messe 2026](https://www.robotics247.com/article/hannover-messe-2026-flexiv-showcases-the-future-of-adaptive-robotics) · [Automated Warehouse — FMR 300 launch](https://www.automatedwarehouseonline.com/flexiv-launches-its-first-self-developed-amr/)
- Arm and gripper specs, and the Isaac workflow, are carried over from the [company profile](../Flexiv.md).

⬆ [Flexiv Robotics profile](../Flexiv.md) · [Products and solutions](Flexiv-T01-2-Products-and-Solutions.md) · [Playbook](Flexiv-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
