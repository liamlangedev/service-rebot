---
type: challenge-brief
company: "Genisom AI"
slug: Genisom-AI
challenge: T03
challenge_title: "Sustainable City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# Genisom AI × T03 Sustainable City — Brief

**Fit: 3/5** — A rugged, programmable **mobile sensing platform** for energy, water and waste audits; it cannot pick, sort or repair anything on its own, so the sustainability logic and any manipulation must come from your payload, your software or a second vendor.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **L2** if on site (IP66, −20 to 55 °C, **5.5 h / 20 km**, built-in navigation) for outdoor rounds; otherwise **L1 EDU** (Orin NX, 3D LiDAR, depth camera, GNSS) for indoor / dry work. Which models are on site is ⚠️ unverified. |
| Strongest proof point | Official inspection cases at a **wind farm (Guangxi)**, a converter station (Henan) and a State Grid EPRI pilot platform (case titles only, dates not public); power-inspection demo with visual + thermal + acoustic sensing at **WAIC, July 2026**. |
| Fastest credible 48-hour demo | "Energy-waste patrol": the dog walks a fixed loop, a thermal or RGB camera flags heat leaks, open windows and lights left on, and a dashboard shows geotagged findings. |
| Biggest risk | No thermal or gas sensor confirmed on site, C++-only SDKs (no Python found), and the L1 is rated **0–40 °C / IP54** — marginal outdoors in November. |
| Pairs well with | **D-Robotics** (low-power edge AI payload) · **SKYLANDX** (3D scan for map / twin) · **Galaxea / Galbot / AGIBOT G1** (the arms that pick what the dog finds) · **XREAL** (AR view of findings) |

## Why
- Inspection is the core business: energy, water-utility, orchard and grain-depot inspection are listed application areas.
- Legs handle stairs, snow and 40–45° slopes — relevant for a steep alpine village.
- Open rails (12 V / 24 V, Ethernet, USB) take your own sensors.
- Open tools shorten the build: MATRiX simulator, RoamerX Lite (ROS 2 / Nav2), vision-language navigation baseline.
- L2 carries 756 Wh for about 20 km — supports a "replace the van round" story.

## Not a fit for
- Waste sorting, litter picking, disassembly or EV-plug handling **as a single-vendor build** — no arm by default (TA01 arm is 🧪, specs not public).
- Teams that want a ready-made sustainability application or a Python-first SDK.

## Sources
[L2](https://www.genisomai.com/en/product-robot/L2) · [L1](https://www.genisomai.com/en/product-robot/L1) · [Industrial Inspection](https://www.genisomai.com/en/industry/industrial-inspection) · [Emerging Applications](https://www.genisomai.com/en/industry/emerging-applications) · [WAIC 2026 news](https://www.genisomai.com/en/newsdetail/GENISOM-AI-at-WAIC-2026) · [GitHub zsibot](https://github.com/zsibot/)

⬆ [Genisom AI profile](../Genisom-AI.md) · [Products and solutions](Genisom-AI-T03-2-Products-and-Solutions.md) · [Playbook](Genisom-AI-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
