---
type: challenge-brief
company: "AGIBOT"
slug: AGIBOT
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# AGIBOT × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — Good for a talking, gesturing companion / exercise coach / clinic guide; not for physical assistance, and no care deployment to point to.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **X2 Ultra** compact humanoid (1.31 m, ~39 kg, ROS 2 AimDK: TTS, mic stream, face screen, preset motions, upper-body control). Runner-up: **D1 Ultra** quadruped (5 kg payload, IP54) for carry / night rounds. |
| Strongest proof point (real deployment or demo + date) | No elderly-care or rehab deployment found. Closest: official **AgentSDK sample = hospital-guide robot** (GitHub, Oct 2026) and **30+ robots** doing visitor guidance at WAIC (2026-07-20). |
| Fastest credible 48-hour demo | X2 Ultra as seated-exercise coach: robot shows the movement, an external camera counts repetitions, robot gives spoken feedback and medication reminders. |
| Biggest risk | Docs say voice / screen interfaces and end-effectors are **not supported on X2 EDU** — if only EDU units are on site, the interaction path changes. Also: a 39 kg biped near frail people. |
| Pairs well with (other vendors on site) | OriginFlow (EMG effort feedback) · XREAL (AR therapy guidance) · D-Robotics RDK (off-board perception) · Flexiv / ROKAE (force-controlled contact that AGIBOT's humanoids cannot do safely) |

## Why
- X2 arm payload is only **≤ 1 kg** across the workspace (3 kg in one posture) — fine for gestures and light handover, not for lifting or transfers.
- The interaction stack is real and documented: TTS, raw mic stream, emoji / video on the face screen, LinkSoul cloud agents, AgentSDK with LLM function calling and a knowledge base.
- The hospital-guide sample is a near copy-paste start for a rehab-clinic concierge (Simplified Chinese and English only).
- Runtime about **2 h** walking at 0.5 m/s (421 Wh) — enough for demos, plan charging.
- G2 has force-controlled arms, but payload, SDK and on-site availability are not public.

## Not a fit for
- Patient lifting, transfer, gait support or anything load-bearing.
- Massage / physiotherapy with body contact (no certified force-controlled contact product).
- Exoskeleton, prosthetic or medical-device projects.

## Sources
- [AimDK_X2 — robot specifications](https://x2-aimdk.agibot.com/en/latest/about_agibot_X2/robot_specifications.html)
- [AimDK_X2 — interaction interfaces](https://x2-aimdk.agibot.com/en/latest/Interface/interactor/index.html)
- [AimDK_X2 — end-effector control](https://x2-aimdk.agibot.com/en/latest/Interface/control_mod/endeffector.html)
- [GitHub — agibot_agentsdk_sample_code](https://github.com/AgibotTech/agibot_agentsdk_sample_code)
- [AGIBOT — D1 Ultra product page](https://www.agibot.com/products/D1Ultra)
- [PR Newswire via AAP — WAIC 2026 (2026-07-20)](https://www.aap.com.au/aapreleases/cision20260719ae07639/)

⬆ [AGIBOT profile](../AGIBOT.md) · [Products and solutions](AGIBOT-T04-2-Products-and-Solutions.md) · [Playbook](AGIBOT-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
