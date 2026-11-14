---
type: challenge-brief
company: "Galbot"
slug: Galbot
challenge: T03
challenge_title: "Sustainable City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# Galbot × T03 Sustainable City — Brief

**Fit: 3/5** — Strong pick-sort-restock robot with no sustainability deployments of its own; usable for indoor sorting, reuse and waste-reduction builds if you do the integration yourself.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Galbot G1** (wheeled dual-arm, **5 kg per arm**, wrist reach floor to 2.1 m, **8 h** runtime, AGX Orin 64 GB) + GalbotSDK (C++ / Python) + open GraspVLA |
| Strongest proof point | Not in this domain. Closest: G1 picks, packs and restocks 24/7 in **~100 instant-retail warehouses** (official site, 2026); S1 works in CATL battery module and pack lines (announced **2026-06-24**) |
| Fastest credible 48-hour demo | Table-top **recyclables sorting station**: camera + vision-language model labels each item, G1 grasps and drops it in the right bin, a dashboard counts kg diverted |
| Biggest risk | Galbot's own "material sorting" kit is still **coming soon** 🧪; public GraspVLA code targets Franka-format data, so on-robot grasping depends on what the Galbot team has preloaded |
| Pairs well with | Unitree / Genisom / Magiclab quadruped (outdoor collection) · D-Robotics RDK X5 (low-power bin camera) · SKYLANDX MetaCam (building map) · Flexiv Rizon (force-controlled disassembly) |

## Why
- **Sorting is grasping.** G1's commercial record is open-vocabulary picking of thousands of different retail items; waste, returns and reuse sorting are the same skill with different bins.
- **Shelf work reduces waste.** Inventory check and restocking are listed G1 uses; near-expiry audits and reuse shelves are a short step.
- **Real developer access.** Free SDK tier, URDF / MJCF / USD models, high- and low-level control, wrist force sensors and depth cameras.
- **Energy link exists but is thin.** CATL is investor, customer and battery supplier; Sinopec invested in 2026. No energy-service product announced.

## Not a fit for
- **Outdoor work**: litter picking on streets, snow, slopes, green-space care (wheeled, IP54, 0–40 °C, flat floors only).
- **Environmental sensing or building automation as the core**: no air, water or energy sensors and no such product; the "site inspection" kit is only planned 🔭.
- **EV-charging automation**: nothing announced by Galbot.

## Sources
- [Galbot G1 product page](http://www.galbot.com/g1/) · [Galbot developer portal](https://developer.galbot.com/?lang=en) · [GraspVLA repo](https://github.com/PKU-EPIC/GraspVLA) · [CnEVPost, 2026-06-24: CATL and Galbot](https://cnevpost.com/2026/06/24/catl-galbot-scale-humanoid-robots-battery-factories/) · [TechNode, 2026-08-27](https://technode.com/2026/08/27/how-far-are-robots-from-actually-working-on-production-lines-galbots-industrial-ai-journey/)

⬆ [Galbot profile](../Galbot.md) · [Products and solutions](Galbot-T03-2-Products-and-Solutions.md) · [Playbook](Galbot-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
