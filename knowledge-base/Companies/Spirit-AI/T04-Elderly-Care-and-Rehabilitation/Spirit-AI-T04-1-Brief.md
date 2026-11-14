---
type: challenge-brief
company: "Spirit AI"
slug: Spirit-AI
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# Spirit AI × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — A capable indoor dual-arm "care chores" robot (fetch, tidy, medication logistics, tele-care), but no care deployment, no documented force API, and its own manual keeps vulnerable people out of the work area.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Moz1** ✅ (wheeled, **26 DoF**, two 7-DoF torque-sensed arms, two-finger grippers, LiDAR Nav2 stack) + **MozRobot SDK** + Quest VR teleop. On-site presence ⚠️ unverified |
| Strongest proof point | WAIC Shanghai, **July 2026**: Moz1 + Spirit v1.6 sorted several pill types and tidied a living room from one spoken instruction. Company-run demo with a closed model, not a care deployment |
| Fastest credible 48-hour demo | Voice-requested **bedside fetch**: Moz1 picks the right medication box and water bottle and places them on a hand-over table; caregiver takes over by VR teleop when it gets stuck |
| Biggest risk | Access and safety: probably one robot, Chinese-only docs, SDK exposes position / Cartesian targets only, and the manual asks for **≥ 2 m** distance during commissioning |
| Pairs well with | D-Robotics (edge perception, Spirit v1.5 port), Unitree Go2 (fall-detection scout), XREAL (caregiver AR view), OriginFlow (EMG intent trigger) |

## Why
- **Hardware suits care chores:** every joint has a torque sensor, collision detection with adjustable sensitivity, compliant mode per arm, three E-stops.
- **Teleop works on day 1:** Quest VR kit gives an instant tele-care story and a data-collection path.
- **Navigation is documented:** Livox MID-360S LiDAR SLAM + ROS 2 Nav2, waypoint goals by ROS service — enough for a room-to-room round.
- **Model story exists:** Spirit v1.5 is open (MIT); a Pi0.5 adaptation for Moz1 is documented (source via after-sales).
- **Company direction:** "industry first, commercial services next, home last" — care is not a current focus.

## Not a fit for
- Physical contact with patients: lifting, transfers, massage, guided physiotherapy, feeding, dressing.
- Wet spa areas, stairs, outdoor paths (**IP40**, flat dry floors, ≤ 75 % RH).
- Training a VLA from scratch in 48 hours (fine-tuning specified for **8× A100 80 GB**).

## Sources
- [Spirit AI news: WAIC 2026](https://www.spirit-ai.com/en/news/48) · [Docs: Moz1 mechanics](https://docs.spirit-ai.com/zh/moz1/mechanics.html) · [Docs: Moz1 safety](https://docs.spirit-ai.com/zh/moz1/safety.html) · [Docs: SDK API](https://docs.spirit-ai.com/zh/sdk/api.html) · [Docs: SLAM navigation](https://docs.spirit-ai.com/zh/slam-nav/slam_navigation.html) · [GitHub: spirit-v1.5](https://github.com/Spirit-AI-Team/spirit-v1.5)

⬆ [Spirit AI profile](../Spirit-AI.md) · [Products and solutions](Spirit-AI-T04-2-Products-and-Solutions.md) · [Playbook](Spirit-AI-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
