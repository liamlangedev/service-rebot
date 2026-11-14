---
type: challenge-brief
company: "D-Robotics"
slug: D-Robotics
challenge: T03
challenge_title: "Sustainable City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# D-Robotics × T03 Sustainable City — Brief

**Fit: 2/5** — Supporting role: a cheap, low-power vision "brain" (RDK X5) for a waste-sorting cell or a monitoring node; it has no actuator, robot or sustainability product of its own.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **RDK X5** (10 TOPS, 5 V supply, 2x MIPI CSI, PoE, CAN FD) + TogetheROS.Bot + Model Zoo. RDK S100 only if you need an on-board VLM / LLM or real-time motor control |
| Strongest proof point (real deployment or demo + date) | Official site lists the **GOAT G1 robotic lawn mower** as built on its chips (green-space care; date not public). Also an open-source ROS 2 **trash-detection node** (`mono2d_trash_detection`, PPYOLO, RDK X3 era; date not public). No sustainability-branded deployment found |
| Fastest credible 48-hour demo | Camera + RDK X5 running **YOLO-World open-vocabulary detection** (type the waste classes as text, no training) → publishes ROS 2 detections → another vendor's arm sorts PET / cans / paper into bins |
| Biggest risk | YOLO-World on the X5 looks words up in a local text-feature library, so arbitrary classes may not work (⚠️ unverified limits). Plan B is a custom model, which needs ONNX → INT8 conversion with the OpenExplorer toolchain (hours, not minutes) |
| Pairs well with (other vendors on site) | Dobot / Flexiv / ROKAE arms (sorting, disassembly) · Unitree Go2 or Genisom quadruped (litter patrol) · Galaxea / Galbot mobile manipulators · SKYLANDX MetaCam (site map) |

## Why
- **Low-power edge AI is the sustainability argument itself:** the X5 runs from a **5 V / 5 A** supply (so under 25 W by design) and can be powered over **PoE** (add-on module); inference stays on the device, no cloud GPU.
- **Zero-training start:** YOLO-World (X5 only) and DOSOD give open-vocabulary detection; the Model Zoo adds YOLO detect / segment, MobileSAM, CLIP and stereo depth, all pre-converted.
- **Standard ROS 2 Humble:** detections arrive as ROS 2 topics, so any ROS-capable arm or base on site can consume them.
- **Cheap enough to scale:** about **USD 100–190** per board makes "one node per bin / per street" arguments credible.

## Not a fit for
- Teams that want a turnkey robot: D-Robotics brings **no arm, gripper or mobile base**.
- Rugged outdoor deployment in November: boards are bare PCBs with no IP rating (S100P is rated **0–45 °C**).
- Heavy on-device VLA or large-VLM work: that is the S600, reported China-only.

## Sources
- [D-Robotics official site](https://en.d-robotics.cc/) · [RDK X5 page](https://en.d-robotics.cc/rdkx5) · [TROS docs](https://developer.d-robotics.cc/tros_doc/en/tros) · [hobot_yolo_world](https://github.com/D-Robotics/hobot_yolo_world) · [mono2d_trash_detection](https://github.com/D-Robotics/mono2d_trash_detection) · [rdk_model_zoo](https://github.com/D-Robotics/rdk_model_zoo) · [CNX Software: RDK X5](https://www.cnx-software.com/2025/06/30/d-robotics-rdk-x5-development-board-features-sunrise-x5-octa-core-soc-with-10-tops-bpu-for-ros-projects/)

⬆ [D-Robotics profile](../D-Robotics.md) · [Products and solutions](D-Robotics-T03-2-Products-and-Solutions.md) · [Playbook](D-Robotics-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
