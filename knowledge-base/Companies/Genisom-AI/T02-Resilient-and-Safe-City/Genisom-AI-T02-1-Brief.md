---
type: challenge-brief
company: "Genisom AI"
slug: Genisom-AI
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# Genisom AI × T02 Resilient & Safe City — Brief

**Fit: 4/5** — Patrol, inspection and emergency response are the company's core markets and the robots are built for rain, slopes and cold; held below 5 because the on-site model is unknown and the SDK is high-level C++ with sensor-stream access unconfirmed.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | Outdoors: **Genisom M1** (IP67, −20 to 55 °C, 45° slope, about 30 kg payload) or **Genisom L2** (IP66, −20 to 55 °C, LiDAR + 5 cameras, built-in navigation). Most likely on site: **Genisom L1 EDU** (Orin NX, 3D LiDAR, depth camera, GNSS), rated **0–40 °C, IP54** only. |
| Strongest proof point | Official industry pages list case titles such as police patrols (Chengdu, Suzhou), substation and converter-station inspection, a State Grid flood drill and an air-ground rescue drill at the National Earthquake Rescue Base — **titles only, undated, no details**. Dated: M1 won the autonomous-navigation category at the 2026 Beijing Yizhuang challenge (company-stated). |
| Fastest credible 48-hour demo | Patrol dog walks a waypoint loop, a camera model on a laptop flags an anomaly (person down, blocked path), a geotagged alert with photo appears on a web dashboard. |
| Biggest risk | Camera / LiDAR access through the SDK is ⚠️ unverified; open RoamerX Lite lists hardware deployment as "TODO". Plan for your own camera. |
| Pairs well with | SKYLANDX (3D scan as map / digital twin) · D-Robotics (edge-AI payload) · XREAL (AR operator view) · Unitree (mixed fleet) |

## Why
- **Security patrol, industrial inspection, emergency response** are three of the five industry segments on the official site; the SP1 (Ex d IIC T6 Gb) targets petrochemical sites.
- M1 and L2 are rated to **−20 °C**; the M1 page shows snow / ice and shallow-water fording tests.
- **5–5.5 h** stated runtime (lab, no load) supports a real patrol loop.
- Open tooling: C++ SDKs, RoamerX Lite (ROS 2 Humble, patrol example), MATRiX simulator, `genisom_vln`.
- **7 (L1) to 15 (M1)** open hardware interfaces with 12 V / 24 V power for your own sensors.

## Not a fit for
- Manipulation (doors, valves, debris): the TA01 arm has no public specs and is unlikely to be on site.
- Joint-level or learned-locomotion work: low-level control and Python bindings are ⚠️ unverified.
- Teams needing a documented thermal or gas payload: none is published with specs.

## Sources
- [Genisom AI industry pages: emergency response](https://www.genisomai.com/en/industry/emergency-response) · [security patrol](https://www.genisomai.com/en/industry/security-patrol) · [industrial inspection](https://www.genisomai.com/en/industry/industrial-inspection)
- [Genisom M1](https://www.genisomai.com/en/product-robot/M1) · [Genisom L2](https://www.genisomai.com/en/product-robot/L2) · [GitHub zsibot](https://github.com/zsibot/)

⬆ [Genisom AI profile](../Genisom-AI.md) · [Products and solutions](Genisom-AI-T02-2-Products-and-Solutions.md) · [Playbook](Genisom-AI-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
