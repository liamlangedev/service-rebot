---
type: challenge-brief
company: "Unitree Robotics"
slug: Unitree
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# Unitree Robotics × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — Good general-purpose robots and the best open tooling on site, but nothing care-specific: build **no-contact** care demos (coach, night rounds, fetch, tele-care), not physical assistance.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **G1 EDU + Dex3-1** (1.32 m, ~35 kg, ~3 kg per arm, 4-mic array + speaker) for coaching and handover; **Go2 EDU** (~15 kg, LiDAR) for night rounds and fall response. G1-D wheeled manipulator is the safer form factor **if** it is on site (not confirmed) |
| Strongest proof point (real deployment or demo + date) | **No care deployment found.** Closest: UnifoLM-VLA-0 (code + weights 29 Jan 2026) runs 12 household manipulation tasks on G1 with open datasets, including "Pour Medicine" and "Fold Towel". Elder care is only a stated goal for ~2030 (IPO filing, Mar 2026) |
| Fastest credible 48-hour demo | G1 demonstrates seated physio exercises, a camera counts the patient's repetitions, the robot gives spoken feedback — robot stays in place, no contact |
| Biggest risk | Safety: Unitree's own product pages tell users to keep a safe distance from humanoids. A falling 35 kg biped next to a frail person is not acceptable; plus EDU-only SDK access |
| Pairs well with (other vendors on site) | OriginFlow (EMG feedback for rehab) · Flexiv (force-controlled contact tasks) · D-Robotics (edge perception box) · SKYLANDX (clinic map) · XREAL (therapist view) |

## Why
- **Fastest software path:** unitree_sdk2 (C++ / Python), xr_teleoperate, unitree_lerobot (ACT, Diffusion, Pi0, Pi05, GR00T) and 246 public datasets on Hugging Face.
- **Voice-ready hardware:** G1 and R1 ship with a 4-mic array and speaker; easy to add a speech + LLM layer.
- **Go2 is small and approachable** (~15 kg) — the least intimidating mobile robot for a clinic corridor.
- **Humanoid as exercise model:** a human-shaped robot can demonstrate movements, which arms and quadrupeds cannot.

## Not a fit for
- Physical support: lifting, transfers, walking aid, massage (arm payload ~2–3 kg; Dex3-1 grasp load 500 g; no certified human-contact safety).
- Any claim of medical-device readiness or existing clinical validation.
- Teams that only get non-EDU units (no SDK).

⬆ [Unitree Robotics profile](../Unitree.md) · [Products and solutions](Unitree-T04-2-Products-and-Solutions.md) · [Playbook](Unitree-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)

## Sources
- [Unitree G1 product page](https://www.unitree.com/g1)
- [Unitree G1-D product page](https://www.unitree.com/G1-D)
- [Unitree Dex3-1 product page](https://www.unitree.com/Dex3-1)
- [Unitree R1 product page](https://www.unitree.com/R1)
- [UnifoLM-VLA-0 repository](https://github.com/unitreerobotics/unifolm-vla)
- [unitree_lerobot repository](https://github.com/unitreerobotics/unitree_lerobot)
- [Unitree on Hugging Face](https://huggingface.co/unitreerobotics)
- [Notebookcheck — Unitree household / elder-care plans (20 Mar 2026)](https://www.notebookcheck.net/Beyond-kung-fu-Unitree-plans-humanoid-robot-for-household-chores-and-elder-care-by-2030.1255707.0.html)
