---
type: challenge-brief
company: "Galaxea"
slug: Galaxea
challenge: T03
challenge_title: "Sustainable City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# Galaxea × T03 Sustainable City — Brief

**Fit: 3/5** — Good tool for learned dual-arm sorting, table clearing and disassembly demos indoors; no sustainability deployments of its own, and nothing for outdoor or sensing-heavy problems.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **LEMO** desktop dual-arm cell (if on site) for sorting / disassembly; **R1 Lite or R1 Pro** when the task needs to move between rooms. Model: **G0.5** (`g05-base`) or a small ACT / diffusion policy |
| Strongest proof point | No waste, recycling or energy deployment is public. Closest: **"industrial component sorting"** and a micro-fulfilment cell (**1,775 picks**, self-reported) at WRC, Aug 2026; **table bussing** learned from **20 demos** in the G0 paper, Sep 2025 |
| Fastest credible 48-hour demo | Recyclables sorting cell: teleoperate 50–100 picks of PET / cans / glass / paper into bins, train a small policy, run it live with a kg-diverted counter |
| Biggest risk | Policy training: full G0.5 fine-tune needs **more than 70 GB VRAM**; what is on site (LEMO? GPU?) is unconfirmed |
| Pairs well with | **D-Robotics** (low-power classifier), **Leadshine** (mini conveyor drive), **XREAL** (operator overlay), **SKYLANDX** (building map for an energy patrol), **WUJI** (dexterous hand for disassembly) |

## Why
- Sorting and clearing are pick-and-place problems, which is exactly what Galaxea's models, dataset (**500+ h**, 1,600+ objects) and teleop tooling are built for.
- Shortest data loop on site: leader arm or VR teleop → LeRobot-format data → fine-tune → deploy over ROS 2.
- Two arms plus force control make "hold with one, unscrew with the other" disassembly feasible; screw fastening is a published LEMO example.
- The open dataset already contains building-operation tasks (for example adjusting an air-conditioner temperature), a hook for an energy-saving patrol.

## Not a fit for
- Outdoor work: litter picking on streets, snow, slopes, green-space care (wheeled base, no public IP rating).
- Environmental monitoring or building-energy analytics — Galaxea sells no sensors or IoT stack.
- "Low-power edge AI" claims: the large models need a desktop GPU; only legacy G0 Tiny targets the on-board Orin.

## Sources
- [Galaxea blog — WRC 2026](https://galaxea-dynamics.com/blogs/robotics-insights-news/wrc-2026-embodied-ai-robotics) · [Galaxea blog — LEMO launch](https://galaxea-dynamics.com/blogs/robotics-insights-news/two-arms-one-platform-galaxea-launches-lemo) · [GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA) · [Open-World Dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset) · [arXiv 2509.00576](https://arxiv.org/html/2509.00576v1)

⬆ [Galaxea profile](../Galaxea.md) · [Products and solutions](Galaxea-T03-2-Products-and-Solutions.md) · [Playbook](Galaxea-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
