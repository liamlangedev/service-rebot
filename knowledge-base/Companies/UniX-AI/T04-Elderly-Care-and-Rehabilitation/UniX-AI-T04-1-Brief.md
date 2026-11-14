---
type: challenge-brief
company: "UniX AI"
slug: UniX-AI
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# UniX AI × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — The right body for assisted-living chores (fetch, serve, tidy, floor pick-up), but elder care is only a marketing label so far and there is no public SDK; rises to **4** if the on-site team opens teleoperation or a skill API.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Panther** (800 mm torso lift, reaches floor level, omnidirectional base, 65 cm passage) if on site; otherwise **Wanda 2.0** (8–16 h battery, 12 kg dual-arm payload) |
| Strongest proof point | No elder-care deployment. Closest: Panther shown in a real household (company video, **8 Apr 2026**); autonomous tea-making demo (**31 Mar 2026**); household demos at CES (**Jan 2026**: tea, dishes, clothes) |
| Fastest credible 48-hour demo | Voice-requested "bring me tea / my glasses / pick that up" concierge for a rehab-clinic room: pre-loaded robot skills + your own speech / LLM / reminder layer on a laptop |
| Biggest risk | Interface unknown: no public SDK, docs, ROS 2 or sim. No published arm force control, collision detection or safety certification — keep the robot **out of physical contact** with people |
| Pairs well with | XREAL (caregiver tele-care view) · D-Robotics RDK (fall-detection camera node) · OriginFlow (EMG rehab input) · Flexiv (force-controlled contact tasks UniX cannot do) |

## Why
- Household service is the company's headline market; skills shown publicly (tea-making, tidying, bed-making, wiping, restocking) are everyday care-home chores.
- Panther's **800 mm lift** lets it pick dropped objects off the floor — a real fall-prevention task; Wanda 2.0 reaches up to **1.8 m** shelves.
- **6-mic array** on both robots (Panther also lists dual speakers): voice interaction with elderly users is feasible if the audio streams are exposed.
- Official application page claims **real-time local/remote teleoperation** and open interfaces for customisation (⚠️ unverified in practice) — a tele-care path if confirmed.
- Long battery (Wanda **8–16 h**) suits day shifts and night rounds.

## Not a fit for
- Physical-contact care: transfers, lifting people, massage, physiotherapy with force control, feeding or dressing.
- Outdoor mobility support on Leukerbad's slopes or snow — indoor flat floors only.
- Wearables, exoskeletons, health sensing — nothing in the portfolio.

## Sources
- [Panther](https://www.unix-group.ai/Panther) · [Wanda 2.0](https://www.unix-group.ai/Wanda) · [Household & Hotel page](https://www.unix-group.ai/Household-Hotel) · [Applications](https://www.unix-group.ai/Applications)
- [CES release, 2 Jan 2026](https://www.webull.com/news/14134140025406464) · [Panther release, 8 Apr 2026](https://technode.global/prnasia/unix-ai-introduces-panther-the-worlds-first-service-humanoid-robot-to-enter-real-household-deployment-powered-by-its-differentiated-wheeled-dual-arm-architecture/)

⬆ [UniX AI profile](../UniX-AI.md) · [Products and solutions](UniX-AI-T04-2-Products-and-Solutions.md) · [Playbook](UniX-AI-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
