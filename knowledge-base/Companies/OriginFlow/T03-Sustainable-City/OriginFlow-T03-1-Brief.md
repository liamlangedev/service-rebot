---
type: challenge-brief
company: "OriginFlow"
slug: OriginFlow
challenge: T03
challenge_title: "Sustainable City"
fit: 1
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# OriginFlow × T03 Sustainable City — Brief

**Fit: 1/5** — A wearable sensing and data company with no robot, no actuator and no sustainability track record; usable only as an add-on (skill recorder or operator input) to another vendor's sorting or disassembly robot.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **OriginKitGen 1.0** ✅ (Glass egocentric camera + Band **16-channel sEMG** wristband + Space recorder) |
| Strongest proof point | None in this domain. Closest: **PULSE 0.2** hand-tracking + fingertip-force demo at WAIC, **July 2026**; industrial data capture with unnamed manufacturers (reported **2026-05-21**) |
| Fastest credible 48-hour demo | Record a human sorting or dismantling items with the kit, then use the recording (video + estimated grip force) to teach or tune another vendor's arm. Only credible if data export or a live stream is offered on site |
| Biggest risk | **No public SDK, API, ROS 2 driver, dataset or model weights.** Everything depends on what the booth team hands you |
| Pairs well with | Flexiv or ROKAE (force-controlled arms), Dobot (cobots), WUJI (dexterous hand), Galaxea / Galbot (mobile manipulators), D-Robotics (edge compute) |

## Why
- **Nothing sustainability-specific exists publicly:** no recycling, waste, energy or environmental-monitoring deployment, demo or partner.
- **One indirect angle:** circular-economy tasks (sorting, repair, disassembly) are contact-rich; the Band estimates **grip force** that cameras cannot see, which could set force limits for a robot.
- **Second indirect angle:** a hands-busy operator input (pinch or wrist gesture) for resolving items a sorting robot is unsure about. Needs a live stream.
- **Force and pose are estimates** under calibration, not measurements; per-user calibration time is not public.
- **The judged output will be the other vendor's robot.** OriginFlow adds a data story, not the system.

## Not a fit for
- Any team that needs a robot, mobility, manipulation or autonomy from one vendor.
- Environmental monitoring, energy or building automation, EV charging, urban farming: no relevant sensor or actuator.
- Teams that cannot afford to lose hours waiting for an undocumented interface.

## Sources
- [OriginFlow official site](https://www.originflow.ai/)
- [TMTPost, 2026-05-21](https://en.tmtpost.com/post/7997613)
- [36Kr Europe, 2026-08-24](https://eu.36kr.com/en/p/3950735048031365)

⬆ [OriginFlow profile](../OriginFlow.md) · [Products and solutions](OriginFlow-T03-2-Products-and-Solutions.md) · [Playbook](OriginFlow-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
