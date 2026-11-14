---
type: challenge-brief
company: "OriginFlow"
slug: OriginFlow
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# OriginFlow × T02 Resilient & Safe City — Brief

**Fit: 2/5** — Supporting role only: a wearable muscle-signal input and capture kit for the human operator, never the robot; useful in T02 only if the team exposes a live data stream on site.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Band** (16-channel sEMG wristband + wrist motion) as a hands-busy command or teleoperation input; **Glass** (egocentric video + head motion) as the operator's field record. Both are parts of **OriginKitGen 1.0** ✅ |
| Strongest proof point (real deployment or demo + date) | **None in this domain.** Closest: **PULSE 0.2** live demo of continuous hand tracking + fingertip-force estimation from the wristband, WAIC 2026 (July 2026). Stated commercial scenarios are industrial manufacturing and home services |
| Fastest credible 48-hour demo | Gloved responder steers a quadruped (stop / come / scan / go) with EMG wrist gestures while hands stay on tools; Glass video logs the mission. Needs a **live raw sEMG stream** ⚠️ unverified |
| Biggest risk | **No public SDK, API, ROS 2 driver or export format.** If no stream or file export is offered, there is no build |
| Pairs well with (other vendors on site) | Unitree / Genisom AI / Magiclab quadrupeds (gesture-commanded scout) · WUJI Hand or Unitree Dex hand on a Flexiv / ROKAE arm (force-aware remote manipulation) · XREAL (operator view) · D-Robotics RDK (edge inference) |

## Why
- The only vendor on site that senses **muscle activity and estimated grip force** — an input channel that does not need line of sight to the hand (inference: should keep working in darkness, smoke or with gloves on; not demonstrated by OriginFlow).
- PULSE outputs **continuous hand pose and fingertip force**, which is what remote manipulation of valves, breakers or debris actually needs — but the model is 🧪 with no public access.
- Glass + Band + Space record a synchronised first-person log of a task, a reasonable "black box" for inspections or drills.
- Zero mobility, actuation, mapping or hazard sensing: everything T02-specific must come from another vendor.

## Not a fit for
- Teams that want a robot, autonomy stack or mapping sensor from one vendor.
- Any build that needs a documented SDK on day 1.
- Safety-rated control: force and pose are **estimates under calibration**, not measurements.

## Sources
- [OriginFlow official site](https://www.originflow.ai/)
- [TMTPost (EN), 2026-05-21 — funding and commercial scenarios](https://en.tmtpost.com/post/7997613)
- [36Kr Europe (EN), 2026-08-24 — profile, PULSE / WAIC demo](https://eu.36kr.com/en/p/3950735048031365)

⬆ [OriginFlow profile](../OriginFlow.md) · [Products and solutions](OriginFlow-T02-2-Products-and-Solutions.md) · [Playbook](OriginFlow-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
