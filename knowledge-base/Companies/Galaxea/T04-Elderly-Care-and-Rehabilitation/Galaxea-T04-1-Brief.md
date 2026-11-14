---
type: challenge-brief
company: "Galaxea"
slug: Galaxea
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# Galaxea × T04 Elderly Care & Rehabilitation — Brief

**Fit: 4/5** — Strong platform for assistive home manipulation (fetch, floor pick-up, hand-over, tidy, laundry) with a real teleop-to-policy path in 48 hours; zero care-sector track record and not safe for physical contact with patients.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **R1 Pro** or **R1 Lite** wheeled dual-arm robot (reach from **floor to about 2 m**, **5 kg per arm** ⚠️ unverified reseller data) + **G0.5** VLA. **LEMO** desktop dual-arm kit for tabletop care tasks (pill / meal tray) |
| Strongest proof point | **Stanford BEHAVIOR Robot Suite (Mar 2025)** on the Galaxea R1: learned whole-body household chores (shelving, laundry, trash out through a door, toilet cleaning, dishwasher) from about **100–140 teleop demos per task**; code and data open. Research, not a care deployment |
| Fastest credible 48-hour demo | Voice-requested **"fetch it / pick up what I dropped / hand it to me"** for a seated person: teleop first, then zero-shot G0.5 or a small policy trained on 50–100 demos |
| Biggest risk | Which robot is on site and whether fine-tuning GPUs come with it is **not confirmed**; full G0.5 fine-tune needs **more than 70 GB VRAM**. A 96 kg robot near frail people needs strict speed and distance limits |
| Pairs well with | **D-Robotics** (edge fall / pose detection) · **XREAL** (caregiver AR / tele-care view) · **OriginFlow** (EMG intent input) · **Unitree** Go2 (night-round scout) · **Flexiv** (force-controlled contact tasks Galaxea should not do) |

## Why
- Full-height working envelope: picks from the floor and reaches high shelves — the two things many elderly people cannot do safely.
- Open data in **residential and kitchen scenes** (500+ h, R1 Lite) and open G0.5 weights that target R1 Lite / R1 Pro directly.
- Teleoperation is first-class (leader arms, VR, JoyLo), so **tele-care works on hour 1** and doubles as training data.
- LEMO (from USD 7,699) gives a cheap second workstation for tabletop tasks.

## Not a fit for
- Patient lifting / transfer, massage, physiotherapy contact or gait support — no public safety certification, force-limit data or medical clearance.
- Outdoor, stairs, snow or steep Leukerbad terrain — wheeled indoor base only.
- Commercial pilots straight after the event — model licences are **non-commercial**.

## Sources
- [Galaxea blog — Stanford x Galaxea household robotics (BRS)](https://galaxea-dynamics.com/blogs/robotics-applications/stanford-galaxea-brs-household-robotics)
- [BEHAVIOR Robot Suite project page](https://behavior-robot-suite.github.io)
- [GitHub — OpenGalaxea/GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA)
- [Hugging Face — Galaxea Open-World Dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset)
- [RBTX reseller listing — R1 Pro](https://rbtx.de/en-GB/components/humanoid/galaxea-r1-pro-humanoid-robot-26-dof)

⬆ [Galaxea profile](../Galaxea.md) · [Products and solutions](Galaxea-T04-2-Products-and-Solutions.md) · [Playbook](Galaxea-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
