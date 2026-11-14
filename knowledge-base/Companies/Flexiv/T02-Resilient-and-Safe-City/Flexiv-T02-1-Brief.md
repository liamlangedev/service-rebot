---
type: challenge-brief
company: "Flexiv Robotics"
slug: Flexiv
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# Flexiv Robotics × T02 Resilient & Safe City — Brief

**Fit: 2/5** — Supporting role only: Flexiv gives you the best "hands" on site for contact tasks (turn a valve, mate a connector, probe a surface), but nothing that walks, flies, patrols or works outdoors.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Rizon 4s** (or Rizon 4) + **Grav** gripper, driven by RDK (Python) and, if two arms are available, **TDK** force-feedback teleoperation |
| Strongest proof point (real deployment or demo + date) | **None in public safety / emergency response.** Nearest: open-source TDK teleop with force feedback over LAN **and WAN** (v2.1, repo updated Nov 2026); mobile CNC tool changing and server-component insertion demos at Hannover Messe (Apr 2026) |
| Fastest credible 48-hour demo | "Remote hands": an operator closes a mock valve / flips a breaker / plugs a connector from another room, with the arm limiting contact force and stopping safely on link loss |
| Biggest risk | Fixed indoor arm: rated **0–45 °C**, controller **IP20**, no mobility unless an FMR 300 / AICO base is on site (unconfirmed). RDK / TDK need a robot-side licence |
| Pairs well with (other vendors on site) | Unitree or Genisom quadruped (scout), SKYLANDX MetaCam (3D map / twin), XREAL glasses (operator view), D-Robotics RDK X5 (edge vision) |

## Why
- Whole-arm force sensing (**0.03 N** on Rizon 4s, **0.1 N** on Rizon 4) makes unknown-contact tasks (stiff valves, misaligned plugs) forgiving — exactly what remote intervention needs.
- `flexiv_tdk` ships ready-made LAN and WAN teleop examples with force feedback; that is a real shortcut for a "hazardous-area teleoperation" story.
- On connection loss the robot decelerates, stops and holds — a built-in safety behaviour you can show to judges.
- Arm is **IP65** and force data is logged at up to **1 kHz**, so "inspection by touch" (stiffness, torque, looseness) is feasible.

## Not a fit for
- Search-and-rescue, patrol, avalanche / rockfall / flood monitoring, or anything on snow, stairs or rough terrain.
- Wide-area sensing, mapping or digital twins on Flexiv hardware alone (no perception stack or foundation model is public).
- Teams that want a single-vendor T02 solution.

⬆ [Flexiv Robotics profile](../Flexiv.md) · [Products and solutions](Flexiv-T02-2-Products-and-Solutions.md) · [Playbook](Flexiv-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)

## Sources
- [Flexiv — Rizon product page](https://www.flexiv.com/product/rizon)
- [Flexiv — Robot System page (Mico, AICO, Mello, Mobile Manipulator)](https://www.flexiv.com/product/robot-system)
- [GitHub — flexiv_tdk (teleoperation kit)](https://github.com/flexivrobotics/flexiv_tdk)
- [Flexiv RDK manual — Loss of connection](https://www.flexiv.com/software/rdk/manual/v2.x/loss_of_connection.html)
- [Flexiv — news list](https://www.flexiv.com/news)
- [Robotics 24/7 — Hannover Messe 2026: Flexiv showcases the future of adaptive robotics (via company profile)](https://www.robotics247.com/article/hannover-messe-2026-flexiv-showcases-the-future-of-adaptive-robotics)
