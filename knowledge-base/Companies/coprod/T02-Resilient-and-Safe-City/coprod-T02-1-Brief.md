---
type: challenge-brief
company: "coprod Inc."
slug: coprod
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# coprod Inc. × T02 Resilient & Safe City — Brief

**Fit: 2/5** — Supporting role only: coprod sells EtherCAT building blocks (motor controller, IMU, power, battery), not a rescue, inspection or patrol robot, and has no track record in this domain.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **co:motion** (1 kHz torque / velocity / position axis with controlled e-stop braking) + **co:power** (e-stop logic, bus telemetry, **10–54.6 V**) + **co:sense** (dual-redundant 9-axis IMU). All 🧪 pre-order; **co:act** actuator 🧪 coming soon. |
| Strongest proof point | None in this domain. Only public demo: in-house biped **co:dodo** (6 DoF), first motion **Dec 2025**. No deployments, pilots or customers named. |
| Fastest credible 48-hour demo | One fail-safe actuated axis (barrier, valve or gate mock-up) that keeps working on battery during a simulated outage, with live power and tilt telemetry on a dashboard. |
| Biggest risk | Access: SDK is not public, kit quantity is unknown, and you need a real-time Linux EtherCAT master plus your own motor and mechanics. Without a coprod founder at your table, do not start. |
| Pairs well with | **Unitree** or **Genisom AI** quadruped (carrier) · **SKYLANDX** MetaCam (mapping payload) · **D-Robotics** RDK (perception compute) · **Leadshine** (motors) |

## Why
- **Deterministic low-level control:** EtherCAT **1 kHz**, **< 20 µs** jitter — good for a custom tool, gimbal or force-reflecting teleop joint that finished robots do not offer.
- **Safety-relevant primitives:** e-stop and fault supervision in co:power, controlled braking in co:motion, redundant IMU in co:sense.
- **Power telemetry over the bus:** every co:power submodule reports data — useful for "keep running during disruption" stories.
- **Founders on site (likely):** a three-person team means direct engineering help.

## Not a fit for
- Anything needing a mobile robot, autonomy, mapping or perception out of the box — coprod has none.
- Outdoor or wet deployments: **no IP or environmental rating** is published.
- Teams without mechatronics or EtherCAT experience.

## Sources
- [coprod — official site](https://coprod.co/) · [products](https://coprod.co/products.html) · [systems](https://coprod.co/systems.html) · [company profile](../coprod.md)

⬆ [coprod Inc. profile](../coprod.md) · [Products and solutions](coprod-T02-2-Products-and-Solutions.md) · [Playbook](coprod-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
