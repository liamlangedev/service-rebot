---
type: challenge-brief
company: "WUJI"
slug: WUJI
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# WUJI × T01 Autonomous Urban Services — Brief

**Fit: 2/5** — Supporting role only: WUJI makes a 20-DoF hand and a data glove, not a robot that moves; it adds human-hand interaction (buttons, handles, key cards, handovers) to another vendor's platform.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Wuji Hand 2** (🧪 2.2 Beta): 20 DoF, back-drivable, force-position control at **1000 Hz**, **650 g**, Ethernet. Fallback **Wuji Hand** gen 1 (✅ 15 N fingertip, 10 kg static grasp, USB). **Wuji Glove** for teleop |
| Strongest proof point (real deployment or demo + date) | **None in urban services** (no public delivery, cleaning or concierge deployment). Closest: open-source glove → hand teleop and a pi0.5 fine-tuning pipeline for dual 7-DoF arms + two Wuji Hands (`wuji-openpi`, 2026-06) |
| Fastest credible 48-hour demo | Hand on a partner arm operates infrastructure built for humans: press a lift button, tap a key card, hand over an item. Canned hand poses, glove teleop as remote-assist fallback |
| Biggest risk | Arm + hand integration eats the weekend. **Indoor only** (gen 1 is IP40; Hand 2 rating and load limits not public). Shared beta hardware |
| Pairs well with (other vendors on site) | Galaxea R1 / Galbot G1 / AGIBOT G1 (mobile base + arms) · Flexiv Rizon / ROKAE xMate (force-controlled arm) · XREAL (operator view) |

## Why
- Hotels, clinics and lifts are built for hands; a five-finger hand needs no building retrofit.
- Joint-level Python / C SDK (`pip install wuji-sdk`) with built-in retargeting: glove or webcam drives the hand within hours.
- URDF / MJCF / USD models allow sim work while hardware is shared.
- Glove teleop gives a credible "operator takes over when autonomy is stuck" story for service fleets.

## Not a fit for
- Projects whose core is navigation, delivery routing or outdoor mobility — WUJI adds nothing there.
- Outdoor, wet or dirty tasks (street cleaning, waste, snow).
- Teams wanting a single-vendor robot or ready-made skills (no grasp planner, no pretrained model).

## Sources
- [WUJI profile](../WUJI.md) · [Hand 2 docs](https://docs.wuji.tech/docs/en/wuji-hand/latest/overview.md) · [Hand gen 1 docs](https://docs.wuji.tech/docs/en/wuji-hand/v1/overview.md) · [wuji-openpi](https://github.com/wuji-technology/wuji-openpi) · [SDK retargeting](https://docs.wuji.tech/docs/en/wuji-sdk/latest/retargeting.md)

⬆ [WUJI profile](../WUJI.md) · [Products and solutions](WUJI-T01-2-Products-and-Solutions.md) · [Playbook](WUJI-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
