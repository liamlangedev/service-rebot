---
type: challenge-brief
company: "Flexiv Robotics"
slug: Flexiv
challenge: T03
challenge_title: "Sustainable City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# Flexiv Robotics × T03 Sustainable City — Brief

**Fit: 3/5** — Excellent "hands" for sorting, repair, disassembly or plug-in tasks, but Flexiv has **no confirmed sustainability deployments** and you must bring your own perception and mobility.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Rizon 4 or 4s** (4 kg, 876–919 mm, force sensing 0.1 / **0.03 N**, IP65) + **Grav** gripper (1–100 N grip, IP67), driven from Python via Flexiv RDK |
| Strongest proof point (real deployment or demo + date) | Nothing in-domain. Nearest: EsVata **shutter sanding** cell, Rizon 4, sanding time **−80 %** (official case, 2024-05) and the **Rizon 4 + Grav cable-insertion** reference workflow in NVIDIA Isaac (2026-09-24) |
| Fastest credible 48-hour demo | **Touch-verified recyclables sorting**: camera proposes the class, the gripper's squeeze force / width confirms it (PET vs. glass vs. aluminium), arm drops into the right bin |
| Biggest risk | Access: RDK needs a **licence activated on the robot**, wired LAN and Remote mode; no camera or vision stack is included. Arm is rated **0–45 °C** and the controller is IP20 — indoor only |
| Pairs well with (other vendors on site) | D-Robotics (low-power edge vision), Unitree / Genisom quadruped (litter collection feeding the arm), SKYLANDX (3D scan of parts), XREAL (operator view), WUJI (dexterous disassembly) |

## Why
- Force control is the differentiator: sustainability tasks with **unknown, dirty, deformable or fragile objects** (waste, used parts, connectors) are exactly where position-only arms fail.
- **IP65 arm / IP67 gripper** tolerate wet and dusty waste streams better than most cobots on site.
- Built-in force primitives (contact, compliant insertion, constant-force surface following) shorten a 48-hour build; Python package installs with `pip install flexivrdk`.
- Surface finishing (sanding, polishing) is Flexiv's most proven application — it maps onto **repair and refurbish instead of replace**.

## Not a fit for
- Outdoor, snow, litter-picking on streets or anything mobile — no base likely on site, and the arm is not rated below 0 °C.
- Environmental monitoring, building-energy or data-only projects — an arm adds nothing.
- Teams wanting a ready-made vision / VLA model: Flexiv has released none.

## Sources
- [Flexiv — Rizon](https://www.flexiv.com/product/rizon) · [Grav](https://www.flexiv.com/product/grav) · [user cases](https://www.flexiv.com/partner/case) · [shutter sanding case](https://www.flexiv.com/partner/case/Flexiv's_Automated_Shutter_Sanding_Solution)
- [GitHub — flexiv_rdk](https://github.com/flexivrobotics/flexiv_rdk)
- [Robotics 24/7 — Rizon 4 supported in NVIDIA Isaac (2026-09-24)](https://www.robotics247.com/article/flexix-rizon-4-adaptive-robot-now-supported-in-nvidia-isaac/Flexiv_Robotics)

⬆ [Flexiv Robotics profile](../Flexiv.md) · [Products and solutions](Flexiv-T03-2-Products-and-Solutions.md) · [Playbook](Flexiv-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
