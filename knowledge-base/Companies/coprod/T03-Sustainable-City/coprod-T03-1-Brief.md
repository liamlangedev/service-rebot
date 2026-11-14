---
type: challenge-brief
company: "coprod Inc."
slug: coprod
challenge: T03
challenge_title: "Sustainable City"
fit: 1
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# coprod Inc. × T03 Sustainable City — Brief

**Fit: 1/5** — Parts vendor with no sustainability product, deployment or demo; only sensible as the motor-control and power layer of a small custom mechanism (sorting gate, valve, tracker) that another vendor's perception drives.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **co:motion** motor controller + **co:power** (power distribution with EtherCAT telemetry and brake chopper), driven from the **cosystem** Python API. All 🧪 pre-order; on-site stock ⚠️ unverified |
| Strongest proof point (real deployment or demo + date) | None in this domain. Only public proof of the stack: in-house biped **co:dodo**, first motion **Dec 2025** |
| Fastest credible 48-hour demo | A **1–2 axis waste-sorting diverter** (flap or paddle on a chute / mini conveyor): camera classifier on a laptop or edge board picks the bin, co:motion moves the gate, co:power telemetry is logged per item |
| Biggest risk | **Access, not physics**: no public SDK, docs or code; kit quantity unknown; you need a real-time Linux EtherCAT host and a coprod engineer next to you |
| Pairs well with (other vendors on site) | **D-Robotics** (RDK X5 vision / edge AI) · **Leadshine** (motors for co:motion to drive) · **Dobot** or **Flexiv** (arm does the picking, coprod drives the auxiliary axis) |

## Why
- coprod sells **building blocks**, not robots: no arm, gripper, mobile base, camera or autonomy stack.
- What it does offer is clean low-level control: **EtherCAT 100 Mb/s, 1 kHz loop, < 20 µs jitter**, torque / velocity / position per axis from a few lines of Python.
- **co:power** reports telemetry on every submodule and has a **brake chopper** for regenerative energy — the one feature with a loose "resource-aware" angle. Which quantities are measured (current, power) is ⚠️ unverified.
- Likely founder presence on site (⚠️ unverified) is the real asset: fast answers, hands-on help.

## Not a fit for
- Teams that want a **working robot on hour 1** (litter picking, mobile monitoring, arm-based sorting) — pick an arm or quadruped vendor.
- Outdoor, snow or wet use: **no IP rating or temperature range is published**.
- Teams without mechatronics / EtherCAT experience.

## Sources
- [coprod — official site](https://coprod.co/) · [products](https://coprod.co/products.html) · [systems](https://coprod.co/systems.html) · [Venture Kick, 2 Apr 2026](https://www.venturekick.ch/coprod-receives-CHF-40000-from-Venture-Kick-to-build-scalable-interoperable-robotics-ecosystem)

⬆ [coprod Inc. profile](../coprod.md) · [Products and solutions](coprod-T03-2-Products-and-Solutions.md) · [Playbook](coprod-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
