---
type: challenge-brief
company: "D-Robotics"
slug: D-Robotics
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# D-Robotics × T02 Resilient & Safe City — Brief

**Fit: 3/5** — Good, cheap on-device perception "brain" for a hazard-watch node or a patrol / rescue robot, but it is a board, not a robot, and has no public safety-domain deployments of its own.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **RDK X5** (10 TOPS, 5 V / 5 A, PoE option, Wi-Fi 6, CAN FD, 2x MIPI for stereo) + RDK Stereo Camera + TogetheROS.Bot. **RDK S100** (80 TOPS) if you want an on-board VLM or LiDAR detection |
| Strongest proof point (real deployment or demo + date) | No safety / inspection deployment found. Closest: Sunrise chips inside shipping outdoor-capable consumer robots (Vbot SuperDog shown at IFA, **Sep 2026**) and official ROS 2 apps for SLAM, Navigation2, stereo depth and person following |
| Fastest credible 48-hour demo | PoE "sentinel" camera node: on-device person / obstacle detection + stereo distance in a closed zone, alert with snapshot pushed to a web dashboard, no cloud needed |
| Biggest risk | Custom models (fire, smoke, rockfall, snow) need training **and** INT8 conversion to the board format; bare boards have no IP rating (S100P rated 0–45 °C) |
| Pairs well with (other vendors on site) | Unitree / Genisom AI / Magiclab quadrupeds (carrier), SKYLANDX MetaCam (3D base map), XREAL (operator view) |

## Why
- **Edge-first fits disaster logic:** inference runs on the board, so detection keeps working when connectivity is down. X5 runs from 5 V, so a power bank or PoE is enough.
- **Ready-made perception blocks:** YOLO family up to YOLO26, open-vocabulary detection (YOLO-World, DOSOD), ByteTrack, stereo depth (`hobot_stereonet`), stereo occupancy, VIO, SLAM and Navigation2 are packaged for ROS 2 Humble.
- **Stereo depth claim:** under **1 % error within 10 m** (vendor figure, RDK X5 page) — enough to measure stand-off distance to a person or obstacle.
- **Hardware video codec** (H.264 / H.265 up to 4K60) helps low-bandwidth teleoperation streams.
- **Cheap enough to deploy several nodes** (X5 about USD 100–190 each).

## Not a fit for
- Teams that want a turnkey rescue or inspection robot: there is no D-Robotics robot, arm or drone.
- Thermal / gas / radar sensing out of the box: none found in the official accessory list.
- Projects that depend on CUDA / TensorRT / Isaac code: it will not run.

## Sources
- [RDK X5 product page](https://en.d-robotics.cc/rdkx5) · [Accessories](https://en.d-robotics.cc/accessories) · [TogetheROS.Bot feature table](https://developer.d-robotics.cc/tros_doc/en/tros) · [rdk_model_zoo](https://github.com/D-Robotics/rdk_model_zoo) · [hobot_stereonet](https://github.com/D-Robotics/hobot_stereonet) · [OpenELAB: IFA 2026](https://openelab.io/blogs/learn/d-robotics-ifa-2026-home-robot-ai-chips-rdk) · [Kyodo PR Wire: Series C](https://kyodonewsprwire.jp/release/202609176168)

⬆ [D-Robotics profile](../D-Robotics.md) · [Products and solutions](D-Robotics-T02-2-Products-and-Solutions.md) · [Playbook](D-Robotics-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
