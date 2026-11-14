---
type: challenge-brief
company: "D-Robotics"
slug: D-Robotics
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# D-Robotics × T01 Autonomous Urban Services — Brief

**Fit: 3/5** — Good on-board "brain" (vision, depth, voice, Nav2 host) for a delivery, guide or cleaning robot, but D-Robotics brings **no robot**: you need another vendor's base.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **RDK X5** (10 TOPS, 2x MIPI CSI, CAN FD, 5 V) + RDK stereo camera + TogetheROS.Bot; **RDK S100** (80 TOPS) if you want an on-device VLM or LiDAR 3D detection |
| Strongest proof point (real deployment or demo + date) | Sunrise chips inside consumer cleaning / mobile robots: xLean TR1 floor-washing robot and Vbot SuperDog shown at IFA Berlin (announced **4 Sep 2026**); **8M+** chips shipped. No city-scale delivery or municipal deployment found |
| Fastest credible 48-hour demo | "Follow-me porter": RDK X5 + camera runs the ready-made body-tracking / re-ID package and publishes `/cmd_vel` to a quadruped or wheeled base that carries luggage behind a guest |
| Biggest risk | Integration: bridging `/cmd_vel` to someone else's robot, and the Nav2 / SLAM examples are documented **only in Gazebo simulation**. Bare boards, no IP rating; S100P rated **0–45 °C** |
| Pairs well with (other vendors on site) | Unitree (Go2 / B2), AGIBOT D1, Genisom or Magiclab quadrupeds as the base · Galaxea / Galbot for a manipulation add-on · SKYLANDX MetaCam for mapping · Leadshine or coprod for a custom base |

## Why
- Ready ROS 2 packages cover most T01 perception needs: person following (re-ID), stereo depth and occupancy, open-vocabulary detection, garbage detection, offline speech (ASR + TTS), small VLMs.
- Standard ROS 2 Humble: `slam_toolbox` and Nav2 install with `apt` on X3 / X5 / S100.
- Cheap and low power (X5: **5 V / 5 A**), easy to strap on any robot or to use as a fixed smart sensor.
- Everything runs on-device: works without the venue Wi-Fi and keeps guest video local.

## Not a fit for
- Teams that want a finished mobile robot or a turnkey delivery / cleaning product.
- Ideas that depend on a custom-trained large model: conversion to the BPU format (INT8) costs hours.
- Rugged outdoor operation in snow without your own enclosure.

## Sources
- [D-Robotics RDK X5 product page](https://en.d-robotics.cc/rdkx5)
- [TogetheROS.Bot documentation index](https://developer.d-robotics.cc/tros_doc/en/tros)
- [TROS app: Navigation2](https://developer.d-robotics.cc/tros_doc/en/apps/navigation2)
- [GitHub: D-Robotics/body_tracking](https://github.com/D-Robotics/body_tracking)
- [OpenELAB: D-Robotics at IFA 2026](https://openelab.io/blogs/learn/d-robotics-ifa-2026-home-robot-ai-chips-rdk)
- [Kyodo PR Wire: Series C release (17 Sep 2026)](https://kyodonewsprwire.jp/release/202609176168)
- [CNX Software: RDK S100P review](https://www.cnx-software.com/2026/08/31/d-robotics-rdk-s100p-a-128-tops-alternative-to-nvidia-jetson-orin-nx-16gb-with-cortex-a78ae-r52-cores/)

⬆ [D-Robotics profile](../D-Robotics.md) · [Products and solutions](D-Robotics-T01-2-Products-and-Solutions.md) · [Playbook](D-Robotics-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
