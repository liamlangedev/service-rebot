---
type: challenge-brief
company: "coprod Inc."
slug: coprod
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# coprod Inc. × T01 Autonomous Urban Services — Brief

**Fit: 2/5** — Supporting role only: coprod sells motion-control building blocks, not a delivery or service robot, and has no navigation stack and no urban deployment.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **co:motion** motor controllers (wheel or mechanism axes) + **co:power** / **co:battery** (power, e-stop, telemetry) + **co:sense** IMU, driven from the **cosystem** Python API. All 🧪 pre-order — confirm on-site stock first. |
| Strongest proof point (real deployment or demo + date) | None in this domain. Only proof the stack works: in-house biped **co:dodo**, first motion **Dec 2025**. The only wheeled hint is the home-page API sample (a 4-wheel velocity group plus a camera motor). |
| Fastest credible 48-hour demo | An **actuated payload module** (locking delivery hatch, lift or dispenser) built on co:motion and mounted on another vendor's mobile robot, which does the navigation. |
| Biggest risk | **Availability and access**: hardware is pre-order, SDK is not publicly downloadable, GitHub link is dead. Without coprod engineers at your table you may not get an axis turning on day 1. |
| Pairs well with (other vendors on site) | Unitree (Go2 / B2 carrier), AGIBOT (D1 carrier), D-Robotics (RDK X5 for perception and navigation compute), SKYLANDX (MetaCam map), Leadshine (motors for co:motion to drive) |

## Why
- **Right primitive, wrong level**: 1 kHz EtherCAT torque / velocity / position control with **< 20 µs** jitter is ideal for a custom wheel base or mechanism, but T01 is judged on autonomy and service value, which coprod does not provide.
- **Clean custom-mechanism path**: one Python API covers motors, IMU and power telemetry, so an add-on (hatch, lift, pan mount) can be scripted quickly once hardware is in hand.
- **Power and safety blocks included**: co:power takes **10–54.6 V**, has e-stop logic and reports telemetry — useful for a credible "city-ready" payload story.
- **Founders on site** (three-person Swiss start-up) are likely the best support channel you will get from any vendor.

## Not a fit for
- Teams that want a ready robot to navigate streets or buildings on day 1.
- Teams without mechatronics / real-time Linux experience.
- Any concept needing weatherproofing or outdoor ratings — no IP rating is published.

## Sources
- [coprod — official site](https://coprod.co/) · [products](https://coprod.co/products.html) · [systems](https://coprod.co/systems.html) · [coprod Inc. profile](../coprod.md)

⬆ [coprod Inc. profile](../coprod.md) · [Products and solutions](coprod-T01-2-Products-and-Solutions.md) · [Playbook](coprod-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
