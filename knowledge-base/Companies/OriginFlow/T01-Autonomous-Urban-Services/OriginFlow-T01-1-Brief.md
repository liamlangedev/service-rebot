---
type: challenge-brief
company: "OriginFlow"
slug: OriginFlow
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# OriginFlow × T01 Autonomous Urban Services — Brief

**Fit: 2/5** — Supporting role only: a wearable muscle-signal (sEMG) input and demonstration-capture kit for someone else's robot; it cannot move, deliver or maintain anything by itself.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Band** (16-channel sEMG wristband + wrist motion) from OriginKitGen 1.0 ✅; **PULSE** hand-pose / fingertip-force model 🧪 only if the team exposes it live |
| Strongest proof point | No urban-service deployment exists. Closest: **PULSE 0.2** live hand-tracking + fingertip-force demo at WAIC 2026 (2026-07), and home-service data capture with 58 Group (household cleaning, kitchen work; reported 2026-05-21) |
| Fastest credible 48-hour demo | "Muscle remote": 4–5 wrist / hand gestures from the Band command a delivery or porter robot (follow, stop, drop here, come back) while the worker's hands are gloved or full |
| Biggest risk | **No public SDK, API or live stream.** If the booth cannot give you raw sEMG or PULSE output in real time, there is no robot demo |
| Pairs well with | Unitree (Go2 / B2) or Genisom quadruped as carrier · WUJI Hand for EMG-driven grasp · Galaxea / Galbot / AGIBOT mobile manipulators as the service robot · XREAL for operator view · D-Robotics RDK for edge inference |

## Why
- Only vendor on site that senses **muscle activity and estimated grip force** — a hands-busy, glove-compatible, noise-proof command channel for outdoor service workers.
- Remote-assist is a real gap in service robotics: an operator wearing the Band can take over the one manipulation step the robot fails at (door handle, parcel handover).
- The kit records synchronised egocentric video + head / wrist motion + sEMG, i.e. demonstration data for service tasks such as housekeeping.
- Company's own stated scenarios (industrial, home services) are adjacent to T01, not inside it.

## Not a fit for
- Teams that need a robot, navigation stack, payload or autonomy from their main vendor — OriginFlow has none.
- Teams that cannot afford to lose half a day finding out whether a live data interface exists.
- Any claim of measured force: outputs are **estimates under calibration**.

⬆ [OriginFlow profile](../OriginFlow.md) · [Products and solutions](OriginFlow-T01-2-Products-and-Solutions.md) · [Playbook](OriginFlow-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
