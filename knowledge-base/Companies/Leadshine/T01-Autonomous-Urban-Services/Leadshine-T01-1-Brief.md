---
type: challenge-brief
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# Leadshine Technology Co., Ltd. × T01 Autonomous Urban Services — Brief

**Fit: 3/5** — An add-on, not a platform: a Leadshine dexterous hand gives another vendor's arm or mobile manipulator the "open the door, press the button, hand over the parcel" skill; Leadshine supplies no mobility, navigation or autonomy.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **DH116** five-finger hand (11 DoF, 6 active, **545 g**, **30 kg** whole-hand load, CAN FD / RS485 / EtherCAT, C++/Python SDK + ROS 2 example). **DH116S** (< 380 g) if the host arm has little payload. |
| Strongest proof point | No service-robot deployment under Leadshine's name. Closest: its DC servo drives are positioned for **AGV & AMR** on its logistics solution page (undated, no named customers) and a low-voltage integrated wheel solution / **iW** wheel module was shown at Automate (Jun 2026) and WAIC (Jul 2026) — no specs published. |
| Fastest credible 48-hour demo | Hand on a host arm or wheeled dual-arm robot **presses a lift button, opens a lever door handle and hands a parcel to a person** — the "last 10 metres" of indoor delivery. |
| Biggest risk | Integration: flange adapter, power and CAN FD bring-up on a host robot you do not control. Whether hands are on site is a **best guess, not confirmed**. |
| Pairs well with | Galaxea R1, AGIBOT G1/G2, Galbot G1 (mobile hosts) · Flexiv, ROKAE, Dobot (arm hosts) · Unitree (mobile base / humanoid) · D-Robotics RDK (ARM compute) · XREAL (teleop view) |

## Why
- Indoor delivery fails at doors, lifts and hand-over; a five-finger hand addresses exactly that gap.
- Hands are the only Leadshine products with a usable stack: **LHandProLib** SDK (C++/Python, Windows/Linux, x86/ARM), ROS 2 example, URDF/MJCF.
- DH116 is robust for its size (rated 1 million grasp cycles, 5 kg per finger) and priced at **USD 2,199** (store), so teams can be less timid with it.
- AGV/AMR drive know-how is real (24–70 VDC ELD3 servo drives, iW wheel module) but not hackathon-programmable.

## Not a fit for
- Teams needing a robot that navigates or delivers out of the box.
- Outdoor, wet or snowy work: no IP rating is published for the hands.
- Building a custom drivetrain in 48 hours: PJ3 / HJ2 / iW have no public SDK or protocol document.

⬆ [Leadshine Technology Co., Ltd. profile](../Leadshine.md) · [Products and solutions](Leadshine-T01-2-Products-and-Solutions.md) · [Playbook](Leadshine-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
