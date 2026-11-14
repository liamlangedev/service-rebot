---
type: challenge-brief
company: "Flexiv Robotics"
slug: Flexiv
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# Flexiv Robotics × T04 Elderly Care & Rehabilitation — Brief

**Fit: 4/5** — Best hardware on site for safe, finely dosed physical contact with a body (massage, guided exercise, handover); no mobility, no care-specific software, no clinical deployments confirmed.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Rizon 4s** (4 kg, 919 mm, force sensing **0.03 N**) + Grav gripper, driven from Python via Flexiv RDK. Enlight L or a Mello unit only if actually on site ⚠️ unverified |
| Strongest proof point | **Mello** robotic massage system: first European showing at Hannover Messe, **April 2026**; release slated **Q4 2026** 🧪. A wellness / retail product, not a medical device. No clinic or care-home deployment found |
| Fastest credible 48-hour demo | Force-controlled contour-following "spa massage" on a mannequin or foam limb with a live pressure dial — or a teach-and-replay rehab exercise handle that assists or resists and logs force and range of motion |
| Biggest risk | Human-contact safety (robot-on-person contact may be restricted) and access: RDK needs a robot-side license and wired LAN |
| Pairs well with | OriginFlow (EMG effort signal) · XREAL (AR therapy guidance) · D-Robotics (edge pose estimation) · Galaxea / Unitree (mobile fetch to a fixed Flexiv station) |

## Why
- Force control is the product: sensing at **0.1 N** (0.03 N with wrist F/T), **1 kHz** loop, 7 DoF to keep the elbow clear of the person.
- Mello proves a body-contact application: contour following with real-time pressure adjustment, **15-minute** session.
- Fast developer path: `pip install flexivrdk`; Python examples for impedance and Cartesian motion-force control; free drive.
- Direct Leukerbad fit: thermal spa plus rehabilitation clinics.
- Teleop kit (TDK, force feedback, LAN or internet) and Flexiv Trainer (LeRobot-format data) enable tele-physio and learning from a therapist.

## Not a fit for
- Mobile home assistance, night rounds, fall detection — fixed-base arms unless an AICO is on site (unlikely).
- Companionship or conversation — no social robot, voice stack or foundation model.
- Patient lifting or transfer — payload **4–10 kg**.

## Sources
- [Flexiv — Robot System page (Mello)](https://www.flexiv.com/product/robot-system) · [Flexiv — Rizon](https://www.flexiv.com/product/rizon) · [Flexiv — Hannover Messe 2026 news](https://www.flexiv.com/news/Flexiv%20to%20Showcase%20the%20Future%20of%20Adaptive%20Robotics%20at%20Hannover%20Messe%202026) · [GitHub — flexiv_rdk](https://github.com/flexivrobotics/flexiv_rdk) · [GitHub — flexiv_tdk](https://github.com/flexivrobotics/flexiv_tdk)

⬆ [Flexiv Robotics profile](../Flexiv.md) · [Products and solutions](Flexiv-T04-2-Products-and-Solutions.md) · [Playbook](Flexiv-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
