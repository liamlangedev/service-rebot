---
type: challenge-brief
company: "SKYLANDX"
slug: SKYLANDX
challenge: T03
challenge_title: "Sustainable City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# SKYLANDX × T03 Sustainable City — Brief

**Fit: 3/5** — A measuring instrument, not a robot: excellent for turning buildings, stockpiles, snow and forest into centimetre-accurate 3D numbers, but the sustainability logic and any physical action must come from your team or another vendor.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **MetaCam Air 2** (619 g handheld, < 1 cm relative accuracy, RTK) + MetaCam Studio (volumes, alignment) + Skyland Cloud (3DGS, web viewer) |
| Strongest proof point | No named or dated T03 deployment is public. Official use-case pages (2026) list stockpile volume measurement, forestry / biomass surveys, Scan-to-BIM for renovation and plant retrofit planning; company claims **5,000+ units shipped** (Oct 2026) |
| Fastest credible 48-hour demo | Scan a pile, container yard or snow depot twice, compute the **volume difference**, and show a "collect / clear only when needed" dashboard |
| Biggest risk | No public SDK or docs; live API / Rosbridge access is "contact SKYLANDX" and offered to "eligible customers". Plan on file export (LAS / PLY / E57) as the safe path |
| Pairs well with | Unitree / Genisom AI / Magiclab quadrupeds (carrier for repeat scans) · D-Robotics RDK (edge compute) · XREAL (AR overlay of results) · Flexiv / Dobot / Galbot (act on what the scan found) |

## Why
- **Measurement is the base of resource saving:** volumes, areas and change over time are exactly what waste, snow, wood-chip, retrofit and forest decisions need.
- **Officially supported workflows match T03:** stockpile volumes in MetaCam Studio, repeat plot surveys in forestry, as-is scans for retrofit planning.
- **Fast capture:** walk-through scanning with live coverage check; up to **150 min** per battery (model-dependent).
- **Works without GNSS** (indoors, tunnels, under canopy) and with RTK outdoors.
- **Robot-mountable** via MetaCam Hub for autonomous repeat scans.

## Not a fit for
- Teams that need a robot that manipulates, sorts, picks litter or charges vehicles — SKYLANDX has no actuator.
- Thermal, gas, air-quality or water sensing — the scanner sees geometry and colour only.
- Projects that depend on a documented, open SDK from hour 0.

## Sources
- [MetaCam Air 2](https://skylandx.com/metacam-air-2/) · [Industrial facilities](https://skylandx.com/industry/industrial-facilities/) · [Surveying](https://skylandx.com/industry/surveying/) · [AEC](https://skylandx.com/industry/aec/) · [Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/) · [Software platforms](https://skylandx.com/software-platforms/)

⬆ [SKYLANDX profile](../SKYLANDX.md) · [Products and solutions](SKYLANDX-T03-2-Products-and-Solutions.md) · [Playbook](SKYLANDX-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
