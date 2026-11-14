---
type: challenge-brief
company: "XREAL"
slug: XREAL
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# XREAL × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — Useful human-interface add-on (therapist HUD, patient cueing, captions, tele-care view) for another vendor's robot; not a care robot and no care deployments of its own.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **One-series glasses (One Pro / 1S, 82–87 g) + XREAL Eye + Beam Pro** — plain USB-C display for zero-code use; Unity SDK 3.1.0 gives **6DoF head pose + RGB camera** only. Hand tracking needs **Air 2 Ultra** or **AURA** (if on site) |
| Strongest proof point (real deployment or demo + date) | **None from XREAL in care / rehab.** Closest: third-party live-captioning app XRAI Glass lists XREAL One and Air 2 series as supported glasses (page checked Nov 2026); academic ActiveGlasses robot-learning work on Air 2 Ultra (Apr 2026) |
| Fastest credible 48-hour demo | Therapist wears glasses as a **hands-free HUD**: live robot state, rep count, force / EMG trace and captions rendered on a laptop, shown in the glasses over USB-C — no SDK needed |
| Biggest risk | Hardware / SDK mismatch: One + Eye has **no hand, plane, image or anchor tracking**; AURA is not sold in Europe; SDK apps need a Samsung S24 / S25 or Beam Pro host (not Android 16) |
| Pairs well with (other vendors on site) | Flexiv / ROKAE (force-controlled rehab arm), OriginFlow (EMG biofeedback), Galaxea / AGIBOT / UniX AI (assistive mobile manipulators), Unitree (humanoid / quadruped companion) |

## Why
- **Light, see-through, glasses-shaped** — the wearer keeps the real room in view, which matters around frail patients (unlike a closed VR headset).
- **Zero-integration path**: every model is a USB-C external display, so any existing dashboard becomes a heads-up view in minutes.
- **6DoF head pose** (One + Eye, Air 2 Ultra) is a free motion signal for head / neck / balance exercises and for steering a robot camera.
- **Camera samples ship with the SDK**: RGB frame access, blended video recording and first-person-view streaming — a base for "see what the patient sees" tele-care.
- Leukerbad angle: rehab clinics and multilingual spa guests suit captions / translation and therapist-assist overlays.

## Not a fit for
- Teams that need the vendor to supply the robot, manipulation, force control or autonomy — XREAL has none.
- Hand-tracked or object-anchored AR on One-series hardware; ROS 2-native work (no official ROS package).
- Anything needing certified medical-device hardware (status not public) or untethered wear (cable to host is a trip hazard).

## Sources
- [XREAL docs — device and feature compatibility](https://docs.xreal.com/XREALDevices/Compatibility)
- [XREAL docs — Sample Code (SDK 3.1.0)](https://docs.xreal.com/Sample%20Code)
- [XREAL docs — Access RGB Camera](https://docs.xreal.com/Camera/Access%20RGB%20Camera)
- [XRAI Glass — compatible AR glasses](https://xrai.glass/ar-glasses/)
- [arXiv 2604.08534 — ActiveGlasses](https://arxiv.org/abs/2604.08534)

⬆ [XREAL profile](../XREAL.md) · [Products and solutions](XREAL-T04-2-Products-and-Solutions.md) · [Playbook](XREAL-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
