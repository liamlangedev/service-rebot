---
type: challenge-brief
company: "Dobot Robotics"
slug: Dobot
challenge: T03
challenge_title: "Sustainable City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# Dobot Robotics × T03 Sustainable City — Brief

**Fit: 3/5** — Easy, low-power arms for a sorting / grading / reuse cell, but nothing purpose-built for sustainability: you bring the perception and the story.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Magician E6** (6-axis, **750 g**, 450 mm, 130 W) or **MG400** (4-axis, **500 g** rated, 440 mm) for a tabletop sorting cell; **Nova 2 / 5** (2 / 5 kg, **30–60 V DC** controller) for a kiosk; **X-Trainer** for learned disassembly. On-site inventory not confirmed |
| Strongest proof point | **Breezy (Poland)** — Nova cobots test, inspect and grade used electronics in a 600 m² refurbishment factory, with ASBIS Robotic Solutions (Dobot case study, undated, about 2025 ⚠️ unverified). |
| Fastest credible 48-hour demo | Camera + off-the-shelf detector + E6 / MG400 sorting mixed recyclables (PET, alu, batteries) into bins, with a live dashboard: items diverted, contamination rate, **Wh per item** |
| Biggest risk | Desktop arms are **IP20**, sub-1 kg payload, fixed-base; Dobot ships no waste-specific model or dataset; which arms and grippers are on site is unknown |
| Pairs well with | **D-Robotics** (RDK X5 edge inference), **Flexiv** or **ROKAE** (force-controlled disassembly step), **Unitree** / **Galaxea** (mobility for litter collection), **XREAL** (operator overlay) |

## Why
- One TCP/IP API (Python, ROS 2 Humble + MoveIt) across E6, Nova and CRA: robot part done on day 1.
- Real circular-economy reference (Breezy refurbishment grading) to cite to judges.
- Low, quotable power draw: **100–150 W** for Nova 2, CR3A, E6, MG400.
- X-Trainer offers a teleop-to-policy route for fiddly tasks (opening, unscrewing); training stack poorly documented.
- Swiss reference exists (CR20A palletizing at winery Cave du Rhodan) — local credibility, not a sustainability case.

## Not a fit for
- Outdoor, wet or mobile work (litter picking, green-space care) without another vendor's base.
- Heavy or bulky waste (bins, glass crates) unless a CR10A-class arm is actually on site.
- Environmental monitoring or building-energy projects — Dobot has no sensors or platform there.

## Sources
[Breezy case study](https://www.dobot-robots.com/insights/case-studies/dobot-powers-breezys-robotic-solutions-to-transform-refurbishment-in-poland.html) · [Cave du Rhodan case study](https://www.dobot-robots.com/insights/case-studies/wine-box-palletizing-automation-with-dobot-cr20a.html) · [Magician E6](https://www.dobot-robots.com/products/education/magician-e6.html) · [MG400](https://www.dobot-robots.com/products/desktop-four-axis/mg400.html) · [Nova series](https://www.dobot-robots.com/products/nova-series/dobot-nova-series.html) · [Dobot-Arm GitHub](https://github.com/Dobot-Arm?tab=repositories) — details in [Products and solutions](Dobot-T03-2-Products-and-Solutions.md)

⬆ [Dobot Robotics profile](../Dobot.md) · [Products and solutions](Dobot-T03-2-Products-and-Solutions.md) · [Playbook](Dobot-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
