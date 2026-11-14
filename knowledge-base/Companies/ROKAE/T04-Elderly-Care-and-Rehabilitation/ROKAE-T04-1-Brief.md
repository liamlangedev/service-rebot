---
type: challenge-brief
company: "ROKAE Robotics"
slug: ROKAE
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# ROKAE Robotics × T04 Elderly Care & Rehabilitation — Brief

**Fit: 4/5** — Best pick if your idea involves a robot arm *touching or being held by a person* (rehab exercise, massage, tele-examination); weak if you need mobility, companionship or a ready-made AI model.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **xMate SR3 / SR5** (3 / 5 kg, Cartesian stiffness adjustable **0–3000 N/m**, 48 V, ~14–17 kg) or **AR5** 7-DoF arm (joint torque sensors, **10 kg** arm). What is actually on site is unconfirmed — check first |
| Strongest proof point | Integrator applications on ROKAE arms: **AI massage robot** (SR series), moxibustion therapy robot, remote ultrasound diagnosis, ward auscultation and ultrasound robot — all undated case pages on rokae.com, none a certified ROKAE medical device |
| Fastest credible 48-hour demo | **Assist-as-needed rehab arm**: therapist drag-teaches an exercise path, the arm replays it in low-stiffness impedance mode while the patient holds a handle; a screen shows range of motion and effort |
| Biggest risk | Hardware availability plus setup: 1 kHz real-time impedance needs a **Linux real-time kernel and a direct cable** to the controller. Human contact also needs strict force and speed limits |
| Pairs well with | **OriginFlow** (EMG effort / intent), **XREAL** (AR therapy guidance, remote therapist view), **D-Robotics** RDK (pose estimation at the edge), **WUJI** hand (handover), a mobile base from **Unitree / AGIBOT** |

## Why
- Force control is the core product: joint torque sensing, drag teaching, joint and Cartesian impedance, direct torque — all exposed in the SDK.
- Open developer path: official GitHub org with **C++ / Python SDK** and a **ROS 2 Humble + MoveIt 2** stack (URDF, Gazebo), Apache-2.0.
- A track record of contact-with-body applications (massage, ultrasound, moxibustion) makes the pitch credible.
- Leukerbad angle is direct: thermal spa plus rehab clinics equals massage, physiotherapy and therapist shortage.

## Not a fit for
- Mobility, fall detection, night rounds or delivery — unless a Helios (160 kg wheeled dual-arm) is on site.
- Companionship or cognitive-stimulation ideas — no speech, VLA or agent stack is public.
- Teams without a Linux PC, camera and end-effector of their own.

## Sources
- [ROKAE — SR cobots](https://www.rokae.com/en/product/show/349/SR-Cobots.html) · [AR humanoid arm](https://www.rokae.com/en/product/show/595/Humanoid-Force-Controlled-Arm-AR.html) · [Healthcare cases](https://www.rokae.com/en/case/206/Healthcare.html)
- [xCore SDK introduction](https://docs.rokae.com/en/docs/SDK/SDK_Intro) · [ROKAE GitHub org](https://github.com/RokaeRobot) · [rokae_ros2](https://github.com/RokaeRobot/rokae_ros2)

⬆ [ROKAE Robotics profile](../ROKAE.md) · [Products and solutions](ROKAE-T04-2-Products-and-Solutions.md) · [Playbook](ROKAE-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
