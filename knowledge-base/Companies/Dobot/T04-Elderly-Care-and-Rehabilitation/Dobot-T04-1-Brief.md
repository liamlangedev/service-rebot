---
type: challenge-brief
company: "Dobot Robotics"
slug: Dobot
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# Dobot Robotics × T04 Elderly Care & Rehabilitation — Brief

**Fit: 4/5** — Light, low-voltage, drag-teachable cobots with a simple Python API give a clear 48-hour path to a bedside or therapy-table demo; the fit drops to 3 if only desktop arms are on site, and Dobot has no named care deployment.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Nova 5** (5 kg, 850 mm, 14 kg, 30–60 V DC controller) — the model Dobot itself labels "For Physiotherapy". For real contact work: **CRAF** (CR5AF, flange 6-axis force sensor). Budget option: Magician E6 |
| Strongest proof point (real deployment or demo + date) | Positioning only: official Nova page tags Nova 5 for physiotherapy (read 2026-11-14). Healthcare page shows lab-automation cases (IVD inspection, nucleic-acid pipetting with CR3), undated. **No named clinic or care-home deployment found** |
| Fastest credible 48-hour demo | Rehab motion coach: therapist drag-teaches an exercise once, arm replays it as a moving target, a webcam scores the patient's reps and range of motion — no human contact needed |
| Biggest risk | Hardware on site is unconfirmed; without a CRAF there is **no force control**, only 5-level collision detection — so massage / guided-limb demos are not safely doable |
| Pairs well with (other vendors on site) | OriginFlow (EMG feedback), XREAL (AR therapy guidance), D-Robotics (edge perception), Unitree / Galaxea (mobile base), WUJI (dexterous hand) |

## Why
- **Safe-by-design basics:** 5 adjustable collision levels, stop in 0.01 s, quiet-ish (65–70 dB(A)), IP54, any-angle mounting, 3 m cable to a 1.3 kg controller.
- **Fast developer path:** one TCP/IP API (`TCP-IP-Python-V4`, Python 3.6+) with `StartDrag`, `SetCollisionLevel`, `ServoP`, and force-control calls; ROS 2 Humble package with MoveIt and Gazebo for Nova 2 / Nova 5.
- **Teach-by-demonstration** fits therapy: a therapist, not a programmer, defines the motion.
- **Upgrade path:** CRAF adds constant-force and <2 N drag; X-Trainer adds dual-arm teleop for tele-care.

## Not a fit for
- Mobility support, fall detection, night rounds — Dobot arms are fixed-base (Atom / LUMO access unlikely; LUMO has no public SDK).
- Patient lifting or transfer.
- Anything needing a certified medical device.

⬆ [Dobot Robotics profile](../Dobot.md) · [Products and solutions](Dobot-T04-2-Products-and-Solutions.md) · [Playbook](Dobot-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)

## Sources
- [Dobot Nova series](https://www.dobot-robots.com/products/nova-series/dobot-nova-series.html)
- [Dobot CRAF series](https://www.dobot-robots.com/products/cra-series/dobot-craf-series.html)
- [Dobot Healthcare industry page](https://www.dobot-robots.com/industries/medical.html)
- [TCP-IP-Python-V4 (GitHub)](https://github.com/Dobot-Arm/TCP-IP-Python-V4)
- [DOBOT_6Axis_ROS2_V4 (GitHub)](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V4)
- [LUMO overview page](https://www.dobot-robots.com/insights/case-studies/1283.html)
