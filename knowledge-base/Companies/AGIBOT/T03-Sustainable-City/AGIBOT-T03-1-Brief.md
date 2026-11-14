---
type: challenge-brief
company: "AGIBOT"
slug: AGIBOT
challenge: T03
challenge_title: "Sustainable City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# AGIBOT × T03 Sustainable City — Brief

**Fit: 2/5** — General-purpose robots with no sustainability product or deployment; useful as a mobile sensor carrier (D1) or a sorting manipulator (G2), not as a ready-made T03 solution.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **D1 Ultra / Edu** quadruped (IP54, **5 kg** payload, **40°** slopes, open SDK) as an environmental or energy-audit sensor carrier. **G2 / G2 Air** for waste sorting only if a unit and AGIBOT staff are on site. |
| Strongest proof point (real deployment or demo + date) | Nothing in sustainability. Closest: "logistics sorting" is a named solution area (2026-04-17), and six G2 robots completed **1,730 tasks** in a 24-hour store trial (2026-11-06). |
| Fastest credible 48-hour demo | D1 walks a route with a thermal / air-quality pod and produces a heat-loss and waste map of a building or street. |
| Biggest risk | What AGIBOT brings is unconfirmed; manipulation on the G series depends on Genie Studio access and staff; X2 vision interface is marked "to be enabled". |
| Pairs well with (other vendors on site) | D-Robotics (low-power edge AI), SKYLANDX (3D map), Flexiv / ROKAE / Dobot (arm for OmniPicker sorting cell), XREAL (operator view) |

## Why
- **Terrain match:** D1 Ultra handles slopes, **16 cm** stairs and splash (IP54) — fits Leukerbad streets and hotel back-of-house; expansion ports (Ethernet, USB, UART, power) take a custom sensor pod.
- **Sorting is plausible, not proven:** G-series arms plus GO-1 open weights (inference on about **7 GB** GPU) and Genie Sim (G2 is the maintained robot) give a path to a recyclables-sorting demo.
- **OmniPicker 3** (**140 N**, **5 kg** payload, 0.1 N tactile resolution, CAN-FD / RS485) can serve as the gripper on another vendor's arm.
- **C5** cleaning robot is the only "resource" product, but its page makes **no water- or energy-saving claims** and exposes no API.
- No AGIBOT statement on recycling, EV charging, energy or environment was found on official pages.

## Not a fit for
- Teams wanting a purpose-built waste, energy or EV-charging platform with reference code.
- Outdoor litter picking: no legged AGIBOT robot with an arm; wheeled G series is IP42 and indoor-oriented.
- Low-power edge-AI stories — AGIBOT sells robots, not efficient compute.

## Sources
- [AGIBOT profile (internal)](../AGIBOT.md) · [D1 Ultra](https://www.agibot.com/products/D1Ultra) · [G2](https://www.agibot.com/products/G2) · [C5](https://www.agibot.com/products/C5) · [OmniPicker 3](https://www.agilink-ai.com/omni-picker3.html) · [Partner conference 2026-04-17](https://www.agibot.com/article/231/detail/63.html) · [GO-1 / AgiBot World](https://github.com/OpenDriveLab/Agibot-World) · [Genie Sim](https://github.com/AgibotTech/genie_sim)
- Web search was unavailable for this pass; official pages were read directly.

⬆ [AGIBOT profile](../AGIBOT.md) · [Products and solutions](AGIBOT-T03-2-Products-and-Solutions.md) · [Playbook](AGIBOT-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
