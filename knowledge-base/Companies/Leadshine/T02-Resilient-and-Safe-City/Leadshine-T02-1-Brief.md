---
type: challenge-brief
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# Leadshine Technology Co., Ltd. × T02 Resilient & Safe City — Brief

**Fit: 2/5** — Supporting role only: Leadshine supplies a strong, programmable hand (and joint modules) for someone else's robot; it has no mobility, sensing, autonomy or safety-domain product of its own.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **DH116 five-finger hand** (11 DoF, 6 active, **545 g**, hook-grip load **≤ 30 kg**, worm-gear self-locking, EtherCAT or CAN FD) mounted on another vendor's arm, humanoid or quadruped. PJ3 joint modules only for custom mechanisms. |
| Strongest proof point (real deployment or demo + date) | **None in this domain.** Closest: live hand and joint-module demos at CES (Jan 2026), FAIR plus (Apr/May 2026) and WAIC (Jul 2026) — generic handling, not rescue or inspection. |
| Fastest credible 48-hour demo | **Remote "hands in the hazard zone"**: DH116 on a cobot arm, teleoperated from a safe distance to turn a valve, flip a breaker and pull a lever, with finger current / tactile feedback on the operator screen. |
| Biggest risk | **Not ruggedised**: manual gives 0–40 °C operation and warns against dust, humidity and oil; no IP rating published. Plus half a day for flange, power (12–48 V) and bus bring-up. |
| Pairs well with (other vendors on site) | Flexiv / ROKAE / Dobot (arm), Unitree / AGIBOT (mobile base or humanoid), XREAL (operator view), OriginFlow (EMG hand control), D-Robotics (edge compute), SKYLANDX (3D map of the scene). |

## Why
- T02 tasks often end in a **manipulation step built for human hands** (valves, switches, door handles, tools) — a five-finger hand covers these without custom grippers.
- **Worm-gear drive is self-locking**: the hand keeps its grip without drawing holding current — useful for carrying or holding a load during a response task.
- **Developer access is real**: LHandProLib SDK (C++ / Python), ROS 2 Humble example workspace, URDF / MJCF, Windows jog tool.
- Tactile variant (-M) reports normal force, tangential force and proximity — usable as contact feedback for a remote operator.

## Not a fit for
- Teams that need a **complete platform** (patrol, mapping, search, autonomy) — Leadshine has none.
- Outdoor snow, wet or dusty demos with the hand exposed.
- Anything depending on PJ3 / HJ2 joint modules without Leadshine staff support — no public SDK or protocol found.

## Sources
- [DH116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh116-series.html) · [DH116 user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116_DH116P_Series_Dexterous_User_Manual.pdf) · [DH116S ROS 2 example note (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_LHandPro_ROS2_Example_Project_Description.pdf) · [FAIR plus 2026 recap](https://store.leadshine.com/blogs/news/leadshine-dexterous-hands-and-joint-modules-shine-at-the-shenzhen-fair-plus-2026) · [WAIC 2026 recap](https://en.leadshine.com/newsEvent/details/leadshine-successfully-concludes-waic-2026,-showcasing-next-generation-robotics-solutions.html) · [company profile](../Leadshine.md)

⬆ [Leadshine Technology Co., Ltd. profile](../Leadshine.md) · [Products and solutions](Leadshine-T02-2-Products-and-Solutions.md) · [Playbook](Leadshine-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
