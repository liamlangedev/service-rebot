---
type: challenge-brief
company: "AGIBOT"
slug: AGIBOT
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# AGIBOT × T01 Autonomous Urban Services — Brief

**Fit: 4/5** — Real guiding, retail and cleaning deployments plus a documented ROS 2 SDK on the X2 give a clear 48-hour path for indoor service demos; outdoor / alpine delivery is unproven.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **X2 Ultra** (guide / concierge; AimDK ROS 2 SDK, navigation module is Ultra-only) · **X2 Edu** (voice + motion, no built-in navigation) · **D1 Ultra** quadruped (**IP54**, **5 kg** payload, **40°** slopes, open SDK) for carrying · **G2** for fetch-and-hand-over only with AGIBOT staff support · **C5** as showcase (no public API) |
| Strongest proof point | **2026-11-02/03:** six G2 robots completed **1,730 tasks** in 24 h in a live Shanghai convenience store (4 of 6 passed the assessment). Guiding robots in service at **Guangzhou Metro** and **Chimelong**; **30+** robots guided visitors at WAIC 2026 (July) |
| Fastest credible 48-hour demo | X2 "resort concierge": greets a guest, answers Leukerbad questions by voice (LLM + SDK TTS / microphone), points or walks them to a destination. Fallback: scripted waypoints with velocity commands |
| Biggest risk | Units and firmware on site are unconfirmed. X2 SLAM / navigation is an **optional** module (Ultra only, enabled via after-sales support); the vision interface is marked "to be enabled"; SDK must match firmware |
| Pairs well with | **D-Robotics** RDK X5 (add-on perception) · **SKYLANDX** MetaCam (fast venue map) · **XREAL** (operator / guest AR view) · **Unitree** Go2 / B2 (outdoor leg of a relay) |

## Why
- Widest single-vendor range on site: legs, wheels, four legs, hands, plus a commercial cleaning robot (C5, up to **1,980 m²/h**).
- Service work is the stated 2026 focus: guiding, retail, logistics sorting, security inspection, cleaning.
- X2 SDK exposes locomotion, TTS, microphone, screen, LiDAR and RGB-D in Python / C++; a public AgentSDK sample (hospital triage robot) is a ready template for a concierge.
- D1 Ultra is small (**630 × 360 × 420 mm**) and expandable (Ethernet, USB, UART, SBUS) — a cheap carrier for stairs and slopes.
- Free sim assets (X2 MuJoCo, D1 Isaac / MuJoCo, Genie Sim 3.0) let part of the team work without the robot.

## Not a fit for
- Street-scale last-mile delivery in snow: no public outdoor or alpine deployment; D1 range is **6 ± 1 km** and its SDK has no built-in navigation.
- Reprogramming the C5 or A2 Ultra: no public developer API beyond persona, dance and swarm tools.
- Heavy payloads: **2–5 kg** per arm on the humanoids.

## Sources
- [AGIBOT — G2 convenience-store trial (2026-11-06)](https://www.agibot.com/article/231/detail/134.html) · [AGIBOT Innovation Day / Worken (2026-10-28)](https://www.agibot.com/article/231/detail/131.html) · [AimDK_X2 perception module](https://x2-aimdk.agibot.com/en/latest/Interface/perception/index.html) · [D1 Ultra](https://www.agibot.com/products/D1Ultra) · [C5](https://www.agibot.com/products/C5)

⬆ [AGIBOT profile](../AGIBOT.md) · [Products and solutions](AGIBOT-T01-2-Products-and-Solutions.md) · [Playbook](AGIBOT-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
