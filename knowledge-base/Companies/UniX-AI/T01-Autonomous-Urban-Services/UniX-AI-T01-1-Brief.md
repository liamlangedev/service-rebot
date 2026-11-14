---
type: challenge-brief
company: "UniX AI"
slug: UniX-AI
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# UniX AI × T01 Autonomous Urban Services — Brief

**Fit: 4/5** — Built and marketed for exactly the indoor service jobs in this track (hotel, reception / guiding, retail, in-building delivery), but **indoor-only** and with **no public SDK**; treat it as **3/5** if the on-site team offers pre-loaded skills only.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Wanda 2.0** (most likely on site ⚠️ unverified): **12 kg** dual-arm payload, **1.5 m/s**, **8–16 h** battery, 360° LiDAR. **Panther** if present: omnidirectional 4WS + 4WD base, **2 m/s**, reaches floor level |
| Strongest proof point | **Aug 2025** — 2 golds + 1 silver in hotel room service and reception, World Humanoid Robot Games, Beijing. **Aug 2026** — Panther reported working in JD.com Seven Fresh Coffee's 24-hour unmanned store (unreviewed event notes ⚠️) |
| Fastest credible 48-hour demo | Spa-hotel concierge: guest asks by voice or QR → your LLM layer on a laptop picks a pre-loaded skill → robot guides the guest or fetches and delivers an item |
| Biggest risk | Developer access: no public SDK, ROS 2 statement, docs or GitHub. Slope, threshold and IP ratings are not published |
| Pairs well with | Unitree (outdoor leg) · SKYLANDX (venue 3D map) · D-Robotics (edge perception node) · XREAL (operator / guest AR) · Binabik AI (agent layer) |

## Why
- Official application pages describe reception, exhibition guiding, **multi-floor delivery with elevator riding**, lobby patrol, pharmacy / store attendant work and order picking — the core T01 indoor list (vendor claims, no named sites).
- Company states Wanda 2.0 already operates in **hospitality, security and retail food service**, shipping **100+ units/month** — a product, not a prototype.
- Long battery life and dual arms let one robot both move and manipulate: deliver, restock, wipe, sort waste.
- The site mentions remote teleoperation and "open software and hardware interfaces" — a fallback path, details not public.
- Leukerbad's hotels, thermal baths and clinics are the same building type the robots are sold into.

## Not a fit for
- Outdoor streets, slopes, snow, stairs or kerbs — wheeled indoor base, no terrain or weather rating published.
- Teams that need low-level control, simulation assets or open models on day one.
- Heavy logistics: payload is **6 kg per arm**, with no cargo bay documented.

⬆ [UniX AI profile](../UniX-AI.md) · [Products and solutions](UniX-AI-T01-2-Products-and-Solutions.md) · [Playbook](UniX-AI-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)

## Sources
- [UniX AI — Reception & Guiding application page](https://www.unix-group.ai/Reception-Guiding)
- [UniX AI — Household & Hotel application page](https://www.unix-group.ai/Household-Hotel)
- [UniX AI — Wanda 2.0 product page](https://www.unix-group.ai/Wanda)
- [UniX AI — Panther product page](https://www.unix-group.ai/Panther)
- [Press release, 8 Apr 2026: Panther launch (TechNode Global / PR Newswire Asia)](https://technode.global/prnasia/unix-ai-introduces-panther-the-worlds-first-service-humanoid-robot-to-enter-real-household-deployment-powered-by-its-differentiated-wheeled-dual-arm-architecture/)
- [WRC 2026 live report, 20 Aug 2026 (iTiger)](https://www.itiger.com/news/1101359561)
