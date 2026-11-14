---
type: challenge-brief
company: "WUJI"
slug: WUJI
challenge: T03
challenge_title: "Sustainable City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# WUJI × T03 Sustainable City — Brief

**Fit: 2/5** — Supporting role only: a 20-DoF hand and a tactile glove add value for *circular-economy* tasks made for human hands (disassembly, repair, cap / lid separation), but for ordinary waste sorting a simple gripper is cheaper, tougher and faster.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Wuji Glove + Wuji Hand** (gen 1 if you need published force numbers: **15 N** fingertip, **10 kg** static grasp; Hand 2 if you need compliant, back-drivable MIT control) — always on a partner arm |
| Strongest proof point (real deployment or demo + date) | **None in this domain.** No public WUJI sustainability, recycling or energy deployment found. Closest: glove-to-hand teleoperation quick start and `wuji-openpi` pi0 / pi0.5 pipeline (2026-06), both generic manipulation |
| Fastest credible 48-hour demo | Glove-teleoperated **disassembly / repair station**: operator wearing the glove drives the hand on a fixed arm to open a small device and separate parts into reuse bins, while every episode is logged to MCAP |
| Biggest risk | **IP40**, soft pads and exposed flex cables: no wet, dirty, sharp or dusty waste. Plus Hand 2 is beta with unpublished payload and wrist-load limits |
| Pairs well with (other vendors on site) | Flexiv (Rizon force-controlled arm) · ROKAE (xMate) · Dobot (CR cobots) · Galaxea / Galbot (mobile dual-arm) · D-Robotics (edge vision) · XREAL (operator view) |

## Why
- Only pure dexterous-hand vendor on site: useful where objects are **built for human fingers** (clips, caps, connectors, knobs, valve heads) and a parallel gripper fails.
- **Glove → hand teleoperation works in hours** (retargeting is inside the SDK), so a human-in-the-loop disassembly cell is realistic.
- Built-in **MCAP recording** turns every teleoperated episode into training data: a credible "today teleop, tomorrow autonomy" story.
- Gen 1 reports **per-joint current and bus voltage**, so you can show a measured energy-per-grasp figure (T03.3 "energy-efficient robotic systems").

## Not a fit for
- Bulk waste sorting, litter picking, anything outdoors, wet or abrasive: use a gripper or suction instead.
- Environmental monitoring, water / energy management, mobile inspection: WUJI has no mobile base, no perception stack and no on-board compute.
- Teams that want a single-vendor build: every WUJI idea needs someone else's arm.

⬆ [WUJI profile](../WUJI.md) · [Products and solutions](WUJI-T03-2-Products-and-Solutions.md) · [Playbook](WUJI-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
