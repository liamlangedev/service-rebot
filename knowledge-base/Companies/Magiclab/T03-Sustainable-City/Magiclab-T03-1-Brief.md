---
type: challenge-brief
company: "Magiclab Robotics"
slug: Magiclab
challenge: T03
challenge_title: "Sustainable City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# Magiclab Robotics × T03 Sustainable City — Brief

**Fit: 2/5** — No sustainability product or deployment; credible only as a **mobile sensor carrier** (MagicDog) or as one part of a multi-vendor sorting demo.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **MagicDog EDU** (16 kg quadruped, ~5 kg payload, ROS 2 SDK with Cartographer SLAM + navigation). Only the EDU edition has SDK access. On-site units not confirmed. |
| Strongest proof point | Nothing sustainability-specific. Nearest: company claim at IFA Berlin (**Sep 2026**) that MagicDog-Y1 has inspected European energy facilities (no sites named, not independently verified); MagicBot D1 parcel-sorting demo at the same show. |
| Fastest credible 48-hour demo | MagicDog EDU maps a building corridor, carries a thermal / CO2 / temperature sensor pack and outputs a **geo-tagged heat-loss and ventilation map** with a ranked fix list. |
| Biggest risk | Edition and access: PRO and base Z1 are **not programmable**. ROS 2 SDK targets Foxy / Iron, needs a wired link to the control board, and was last updated May 2025. No IP rating published for MagicDog — outdoor snow use is untested. |
| Pairs well with | D-Robotics (RDK X5 as low-power sensor brain), SKYLANDX (3D scan as base map), XREAL (AR overlay of findings), Flexiv / Dobot / ROKAE (fixed arm for the sorting step). |

## Why
- The quadruped gives T03 what fixed sensors cannot: **repeatable measurement routes** through hotels, spas and plant rooms, including stairs and slopes up to 40° (lab value).
- SLAM and goal-pose navigation already exist in `magicdog_ros2_sdk`, so team time goes into sensing and analytics, not locomotion.
- Open BSD-3 SDKs, URDFs and MuJoCo / RL repos lower the entry cost.
- Sustainability value must come from **your payload and software** — Magiclab supplies mobility only.

## Not a fit for
- Waste sorting or litter picking with Magiclab hardware alone: the Z1 arm carries **2–3 kg**, and the open VLA demo targets Gen1, not Z1.
- Outdoor winter monitoring unless a MagicDog-Y1 (IP67, −20 °C) is on site — unlikely as a hackable unit.
- Teams wanting a ready-made environmental or energy application: none exists.

## Sources
- [Company profile](../Magiclab.md) · [MagicDog page](https://www.magiclab.top/en/dog) · [MagicDog-Y1 page](https://www.magiclab.top/en/dog-y) · [MagicBot Z1 page](https://www.magiclab.top/en/z1) · [magicdog_ros2_sdk](https://github.com/MagiclabRobotics/magicdog_ros2_sdk) · [magicbot-gen1_pi0_demo](https://github.com/MagiclabRobotics/magicbot-gen1_pi0_demo) · [EqualOcean, Sep 2026](https://equalocean.com/news/2026090822169-magiclab-targets-european-logistics-robotics-showcase-slovenia-postal)

⬆ [Magiclab Robotics profile](../Magiclab.md) · [Products and solutions](Magiclab-T03-2-Products-and-Solutions.md) · [Playbook](Magiclab-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
