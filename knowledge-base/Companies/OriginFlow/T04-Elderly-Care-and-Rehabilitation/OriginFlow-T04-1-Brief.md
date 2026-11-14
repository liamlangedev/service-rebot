---
type: challenge-brief
company: "OriginFlow"
slug: OriginFlow
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# OriginFlow × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — The only vendor on site that senses muscle activity, which is a real rehab signal, but it is a sensor and data company with no robot, no public SDK and no care deployment; usable as one part of a multi-vendor build.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Band** (16-channel sEMG wristband + wrist motion) with the **PULSE** model (hand pose + fingertip-force estimate) 🧪. Glass and Space are secondary here |
| Strongest proof point | No care or rehab deployment exists. Closest: **PULSE 0.2 live demo at WAIC 2026 (July 2026)** — continuous hand tracking and real-time fingertip force during pinch. Medical rehabilitation is only named as a **future market** (May 2026) |
| Fastest credible 48-hour demo | **EMG biofeedback grip / hand-exercise coach**: Band, laptop, effort bar, rep counter, fatigue trend. Needs only raw sEMG, no robot |
| Biggest risk | **No documented live data stream.** If the team on site cannot give you real-time sEMG or PULSE output, every interactive idea collapses to offline recording |
| Pairs well with | **Flexiv / ROKAE** (force-controlled arm for effort-aware assisted motion) · **WUJI / Unitree Dex hand** (EMG-driven assistive grasp) · **XREAL** (AR exercise feedback) · **D-Robotics RDK** (edge bridge node) |

## Why
- sEMG is an established signal for rehab biofeedback and myoelectric prosthesis control; the Band gives **16 channels** at the wrist in a watch-like form factor.
- PULSE outputs **continuous** hand pose and force estimates, not just discrete gestures — suited to intent-driven assistive control.
- Leukerbad's rehab clinics and elderly guests make a hand-rehab or weak-grip assistance demo locally credible.
- Low hardware cost (press-reported about RMB 1,000 per set ⚠️ unverified) supports a "take-home rehab" story.

## Not a fit for
- Teams that want a robot platform: OriginFlow has **no actuators**, mobility or manipulation.
- Any claim of clinical measurement: outputs are **estimates under calibration**, and this is **not a medical device**.
- Fall detection, night rounds, lifting or logistics — nothing here helps.

## Sources
- [OriginFlow official site](https://www.originflow.ai/)
- [TMTPost (EN), 2026-05-21 — funding and application areas](https://en.tmtpost.com/post/7997613)
- [QbitAI, 2026-08 — OriginFlow profile (Chinese)](https://www.qbitai.com/2026/08/477094.html)

⬆ [OriginFlow profile](../OriginFlow.md) · [Products and solutions](OriginFlow-T04-2-Products-and-Solutions.md) · [Playbook](OriginFlow-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
