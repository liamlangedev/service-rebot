---
type: company
company: "coprod Inc."
slug: coprod
hq: "Prilly (Lausanne area), Switzerland"
founded: 2024
website: https://coprod.co/
categories: [components, software]
on_site_guess: "co:system EtherCAT modules (motion controller, IMU, power, battery), possibly the co:dodo biped as a demo, plus the cosystem Python API and browser simulator"
fit_t01: 2
fit_t02: 2
fit_t03: 1
fit_t04: 2
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# coprod Inc.

> **One-liner:** Very early-stage Swiss start-up (Prilly, VD) selling "co:system" — plug-together EtherCAT robot building blocks (motor controller, actuator, IMU, power, battery) with one Python / C++ API on top.
> **Why it matters at Leukerbad:** coprod is a **components and control-stack** vendor, not a robot vendor. It is relevant only if your idea needs a **custom mechanism** (a joint, a gripper axis, a wheel base, a rehab device) with deterministic 1 kHz torque / velocity / position control — otherwise build on a finished robot from another vendor.

**Read this first:** public information is thin. No prices, no public docs portal, no working public GitHub, no named customers. Most hardware is **pre-order**, the actuator is **coming soon**.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Prilly (near Lausanne), Vaud, Switzerland (startup.ch listing) |
| Founded | **July 2024** (startup.ch listing) |
| Founders / CEO | **Loïc Delineau** (CEO), **Vincent Nguyen** (CTO), **Matthias Schuller** (Chief Scientist) |
| Legal name | Inconsistent in public sources: site footer "coprod inc", LinkedIn slug "coprod-inc" / "coprod-llc", startup.ch "coprod SA" / "coprod LLC". Same company. |
| Size and funding | Team size not public (three named founders). **CHF 40,000** Venture Kick Stage 2 (2 Apr 2026). No other round public. Until spring 2026 the team worked from a garage. |
| University roots | Not stated publicly. Team describes 4+ years of prior robot building (rovers, arms, dogs). EPFL link is plausible given location but ⚠️ unverified. |
| Core business | Modular robotics hardware ("coproducts") on an EtherCAT bus + unified software stack; target customers are start-ups, research labs, hobbyists |
| Website | https://coprod.co/ (coprod.ch and coprod.ai redirect there) |
| Docs / developer portal | Not public. API is shown only as a code sample on the home page. Support via Discord (linked from the site) and contact@coprod.ch |
| GitHub | Site links to github.com/coprod-llc, but that URL returned **404** on 2026-11-14 — treat as no public code |

## Portfolio at a glance

All products belong to one platform, **co:system**. Shared system numbers: **EtherCAT, 100 Mb/s**, **1 kHz** typical control loop, **< 20 µs** jitter, distributed-clock sync with hardware time-stamping, real-time Linux master.

| Product | Type | Status | Key specs (verified on official site) | Price | Img key |
|---|---|---|---|---|---|
| **co:act** | Quasi-direct-drive actuator with built-in controller | 🧪 coming soon | **10 Nm** continuous / **25 Nm** peak · **16:1** reduction · **60 mm** diameter · **420 g** · hollow shaft · dual encoder (motor + output side) · torque / velocity / position control | not public | coprod-coact |
| **co:motion** | Motor / motion controller board | 🧪 pre-order | EtherCAT **1 kHz+** with DC sync · feedback: BiSS, SSI, SPI, Hall, incremental · several sizes incl. hollow-shaft · controlled braking for e-stop (Safe Torque Off module still to come) | not public | coprod-comotion |
| **co:power** | Modular power distribution module | 🧪 pre-order | Input **10–54.6 V** · up to **6 submodules** (power logic / e-stop, precharge, isolated DC/DC regulator, brake chopper) · telemetry over EtherCAT | not public | coprod-copower |
| **co:sense** | IMU module | 🧪 pre-order | **9-axis, dual-redundant** · on-board fusion at **1 kHz** · outputs quaternion, accel, gyro, mag · **30 × 50 mm** | not public | coprod-cosense |
| **co:battery** | Battery pack | 🧪 pre-order | Over-current / over- and under-voltage / short-circuit / temperature protection · 4 state-of-charge LEDs · latching interface · sizes and voltages on request (no capacity figures public) | not public | coprod-cobattery |
| **cosystem API** | Software: Python package with C++ core | 🧪 preview (not publicly downloadable) | Network scan, per-device handles, velocity / position / torque commands, IMU and power telemetry, logging · ROS 2 support claimed on startup.ch listing, not shown on the site | not public | coprod-cosystem-api |
| **co:dodo** | Reference biped built from co:system | 🧪 in-house demo robot, not sold | **6 DoF**, point-foot · 1 kHz whole-body control over EtherCAT · first "signs of life" Dec 2025 · browser simulator available | not for sale | coprod-cododo |
| **co:dodo simulator** | Browser simulator | ✅ available (web) | MuJoCo compiled to WebAssembly · ONNX policy inference at **50 Hz** · no install | free to use | coprod-cododo-sim |
| **co:found** | Founder discount programme | ✅ open for applications | **75% off** up to first CHF 25,000 spent (bootstrap) · **33% off** up to CHF 100,000 (funded) · no equity | n/a | coprod-cofound |

Roadmap items (EtherCAT junction, IO board, tactile sensor) are listed under Roadmap below.

## What they will most likely bring to the hackathon

**Best guess — not confirmed by any public source.**

- **Most likely:** a few co:system dev kits — **co:motion** controllers with motors, **co:sense** IMUs, **co:power** and **co:battery** — plus the founders themselves as hands-on support. For a three-person start-up, founder presence is the real asset.
- **Likely as a showpiece:** the **co:dodo** biped. It is their only complete robot and their proof that the stack works. Expect a demo, not a robot you can freely reprogram.
- **Possible:** early **co:act** actuators (listed "coming soon"), in small numbers.
- **Unlikely:** large quantities of anything. Stock is pre-order stage; ask at the booth how many kits exist before you plan around them.
- **Questions to ask in the first five minutes:** How many motor axes can one team get? Is there a ready wheel-base or arm example? Which host PC / OS does the EtherCAT master need? Is there a ROS 2 bridge today?

## Developer platform (summary)

- **API:** Python package `cosystem` on a C++ core with Python bindings. The home-page sample shows scanning the bus, fetching devices by ID, setting a velocity mode, commanding wheel velocities, reading IMU Euler angles and regulator voltage.
- **Control levels:** low-level, joint-centric — simultaneous torque, velocity and position control per axis, gains adjustable from the API. No high-level skills, navigation or manipulation layer is published.
- **Real-time layer:** stack is developer API → real-time control loop → EtherCAT master → devices, on real-time Linux; **1 kHz**, **< 20 µs** jitter per the site.
- **ROS 2:** the startup.ch listing describes a unified API for C++, Python and ROS 2; the official site does not show ROS 2 material. ⚠️ unverified as shipping.
- **Simulation:** in-browser co:dodo simulator (MuJoCo WASM + ONNX at 50 Hz). The site says simulated policies match the real robot. No downloadable URDF / MJCF found publicly.
- **Pretrained models / datasets:** none published. No foundation model, no VLA.
- **Teleoperation / data collection:** none today; a dual-arm teleop platform is a stated future system.
- **On-board compute:** not specified. You bring the host computer running the EtherCAT master.
- **Docs and code:** no public docs portal; GitHub link on the site is dead (404). Plan on getting SDK access and examples directly from the team or via their Discord.

## Current projects, deployments and customers

- **Dec 2025** — First coprod modules integrated into the in-house biped co:dodo, which showed first motion just before Christmas; built in about three months of evenings and weekends ([Venture Kick](https://www.venturekick.ch/coprod-receives-CHF-40000-from-Venture-Kick-to-build-scalable-interoperable-robotics-ecosystem)).
- **2 Apr 2026** — CHF 40,000 from Venture Kick. Team reports a partnership with an unnamed "global component supplier" ([Venture Kick](https://www.venturekick.ch/coprod-receives-CHF-40000-from-Venture-Kick-to-build-scalable-interoperable-robotics-ecosystem)).
- **2026** — Site invites "early adopters"; co:found discount programme open for hardware founders ([co:found](https://coprod.co/cofound.html)).
- **Customers / deployments:** none named publicly. No deployment in any of the four track domains. The company blog has no posts yet.

## Roadmap and future direction

- **Planned modules (no dates):** EtherCAT junction (passive and active, for star / branch wiring), general IO board (time-stamped digital / analog), high-bandwidth **tactile sensor** array, Safe Torque Off module, more co:act sizes ([products](https://coprod.co/products.html)). 🔭
- **Planned systems (no dates):** dual-arm teleoperation platform with tactile end effectors; full-body humanoid ([systems](https://coprod.co/systems.html)). 🔭
- **Strategy:** be the standard parts-and-control layer for young European robot companies; claim is "time to first step" under 6 months for a new robot. Positioning: "the Legos of robotics".
- **Use of funds (Apr 2026):** market outreach — travel, trade fairs, marketing — and moving into a proper workspace.

## Challenge fit

Scores are low across the board because coprod supplies parts, not a task-ready robot, and its software is not publicly available. A 48-hour build on raw actuators is high-risk unless the team has EtherCAT / mechatronics experience and coprod staff sit with you.

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 2 | Could drive a custom wheel base or add-on mechanism (lift, hatch, dispenser) on another vendor's robot; no navigation stack | co:motion, co:power, co:battery, co:sense | [T01 brief](T01-Autonomous-Urban-Services/coprod-T01-1-Brief.md) |
| T02 Resilient & Safe City | 2 | Redundant IMU, e-stop logic and power telemetry suit a rugged custom sensor mast or actuated tool; supporting role only | co:sense, co:power, co:motion | [T02 brief](T02-Resilient-and-Safe-City/coprod-T02-1-Brief.md) |
| T03 Sustainable City | 1 | Only generic use: an actuated sorting flap or valve with energy telemetry; nothing domain-specific | co:motion, co:power | [T03 brief](T03-Sustainable-City/coprod-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 2 | A backdrivable 10 Nm torque-controlled joint is the right primitive for a single-joint rehab or assist device, but co:act is not yet shipping and there is no safety certification | co:act (if available), co:motion, co:sense | [T04 brief](T04-Elderly-Care-and-Rehabilitation/coprod-T04-1-Brief.md) |

## Related docs
- [Product portfolio](coprod-Products.md) · [Developer guide](coprod-Developer-Guide.md) · [Roadmap and strategy](coprod-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [coprod — official site (home, API sample, system specs)](https://coprod.co/)
- [coprod — products](https://coprod.co/products.html)
- [coprod — systems (co:dodo, planned systems)](https://coprod.co/systems.html)
- [coprod — co:found founder programme](https://coprod.co/cofound.html)
- [coprod — blog (empty as of 2026-11-14)](https://coprod.co/blog/)
- [Venture Kick — coprod receives CHF 40,000 (2 Apr 2026)](https://www.venturekick.ch/coprod-receives-CHF-40000-from-Venture-Kick-to-build-scalable-interoperable-robotics-ecosystem)
- [startup.ch — coprod listing](https://www.startup.ch/coprod)
- [LinkedIn — coprod](https://www.linkedin.com/company/coprod-inc/)
