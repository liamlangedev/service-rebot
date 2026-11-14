---
type: challenge-brief
company: "WUJI"
slug: WUJI
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# WUJI × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — Useful sensing and dexterity building block for hand rehab and assistive manipulation, but no care track record, no robot of its own, nothing medically certified.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Wuji Glove** ✅ (526 tactile points at 120 FPS, fingertip 6-DoF pose, 67.5 g) — works alone. Second: **Wuji Hand 2** 🧪 (20 DoF, back-drivable) on a stand or partner arm |
| Strongest proof point (real deployment or demo + date) | **None in care or rehab.** Official docs list only teleoperation, tactile data collection, HCI and VR / AR. Closest asset: official glove → hand teleop example (SDK updated 2026-11-10) |
| Fastest credible 48-hour demo | Glove-only **hand-function check and exercise game**: live grip-pressure map + finger range of motion, scored against a baseline. Optional: a Wuji Hand mirrors the exercise |
| Biggest risk | Not a medical device; **one glove size**, no cleaning guidance, EMF tracking disturbed by metal (implant compatibility not stated). Hands scarce; Hand 2 is beta |
| Pairs well with (other vendors on site) | XREAL (AR-guided therapy) · OriginFlow (EMG) · Flexiv / ROKAE (force-controlled arm for the hand) · D-Robotics (edge host) |

## Why
- **Glove measures what hand therapy needs**: per-finger pressure zones (4 mm pitch) and a 21-keypoint hand skeleton with joint angles, via a free Python SDK. Caveat: pressure is **normalized 0–1, not newtons** — relative scores only.
- **Glove-only ideas need no partner robot** — the lowest-risk WUJI path in any track.
- **Hand 2 can run soft** (per-joint kp / kd, effort limit) for mirror-therapy or object handling at arm's length; the user notice says keep body away while it moves.
- **Fast tooling**: built-in retargeting (webcam + MediaPipe also works), MCAP recording, simulation models.
- **Leukerbad angle**: rehab clinics and older spa guests make hand rehab a believable local story.

## Not a fit for
- Mobility support, fall detection, lifting people, night rounds — no mobile robot, no arm.
- Force on a patient (massage, physio manipulation) — small fingertip force, no safety certification.
- Teams wanting ready-made assistive skills — SDK is joint-level, no grasp planner.

## Sources
[WUJI profile](../WUJI.md) · [Glove introduction](https://docs.wuji.tech/docs/en/wuji-glove/latest/introduction.md) · [Glove tactile reference](https://docs.wuji.tech/docs/en/wuji-glove/latest/sdk-data-reference/tactile.md) · [Hand 2 user notice](https://docs.wuji.tech/docs/en/wuji-hand/latest/user-notice.md)

⬆ [WUJI profile](../WUJI.md) · [Products and solutions](WUJI-T04-2-Products-and-Solutions.md) · [Playbook](WUJI-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
