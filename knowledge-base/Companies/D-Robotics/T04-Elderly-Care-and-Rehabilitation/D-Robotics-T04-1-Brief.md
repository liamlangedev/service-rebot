---
type: challenge-brief
company: "D-Robotics"
slug: D-Robotics
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# D-Robotics × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — Not a care robot, but the cheapest way to add private, on-device fall / pose / voice sensing to someone else's robot or to a fixed room sensor.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **RDK X5** (10 TOPS, about USD 100–190) + MIPI / USB camera for sensing; **RDK S100** (80 TOPS) if you add an on-board VLM or a learned arm policy |
| Strongest proof point (real deployment or demo + date) | No care or clinical deployment found. Closest: ready-made **fall detection app** in TogetheROS.Bot (RDK X3 / X5; repo last updated Jul 2024) and Sunrise chips inside the **TCL "hey AiMe" companion robot** shown at IFA, Sep 2026 |
| Fastest credible 48-hour demo | Camera + RDK X5 "guardian node": body keypoints → fall event (`ros2 launch hobot_falldown_detection ...`) → spoken check-in → alert to caregiver dashboard. No video leaves the room |
| Biggest risk | It only senses. Any physical help needs another vendor's robot plus ROS 2 glue. Stock fall demo is basic (docs test it by rotating the camera 90°); stock speech examples are Chinese |
| Pairs well with (other vendors on site) | Unitree Go2 or Genisom quadruped (night-round patrol) · Galaxea / Galbot / UniX AI mobile manipulators (fetch after a fall) · Flexiv / ROKAE arms (rehab with force control) · XREAL (therapist view) · OriginFlow (EMG + pose) |

## Why
- **Ready building blocks:** body + head + face + hand detection with keypoints at **125 FPS** inference on X5, a fall-detection app on top, hand-gesture nodes, person following (ReID), offline ASR and TTS, small on-device VLMs.
- **Privacy story fits care homes and clinics:** everything can run on the board at a few watts; publish events, not video.
- **Cheap and many:** an X5 per room is realistic; good "scales to every room in a Leukerbad clinic" argument.
- **Standard ROS 2 Humble:** events are plain topics, so any ROS 2 robot on site can react to them.
- **Momentum in home / companion robots** (IFA 2026), though nothing care-specific.

## Not a fit for
- Teams that want a robot out of the box: D-Robotics has no arm, base or body.
- Contact tasks (massage, transfer, physio with force): no actuation or force sensing here.
- Anything needing certified medical or safety functions: these are developer boards.

⬆ [D-Robotics profile](../D-Robotics.md) · [Products and solutions](D-Robotics-T04-2-Products-and-Solutions.md) · [Playbook](D-Robotics-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)

## Sources
- [TogetheROS.Bot docs: pose (fall) detection app](https://developer.d-robotics.cc/tros_doc/en/apps/fall_detection)
- [TogetheROS.Bot docs: human body detection and keypoints](https://developer.d-robotics.cc/tros_doc/en/boxs/body/mono2d_body_detection)
- [GitHub: hobot_falldown_detection](https://github.com/D-Robotics/hobot_falldown_detection)
- [GitHub: sensevoice_ros2](https://github.com/D-Robotics/sensevoice_ros2)
- [GitHub: hobot_llamacpp](https://github.com/D-Robotics/hobot_llamacpp)
- [OpenELAB: D-Robotics at IFA 2026](https://openelab.io/blogs/learn/d-robotics-ifa-2026-home-robot-ai-chips-rdk)
- [D-Robotics profile (general research)](../D-Robotics.md)
