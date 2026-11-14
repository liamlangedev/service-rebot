---
type: challenge-brief
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T03
challenge_title: "Sustainable City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# Omnicor AI × T03 Sustainable City — Brief

**Fit: 2/5** — Supporting role only: an edge-AI deployment team (no robots, no public specs or SDK) that can make another vendor's robot run its model on-board at lower power; useful as the "low-power edge AI" layer of a T03 project, not as its core.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Model optimisation** service plus **OC Node** compute box (if units are on site — ⚠️ unverified); specs not public |
| Strongest proof point (real deployment or demo + date) | **None in this domain.** Site (2026, undated) only names use cases: on-board robot inference inside a power budget, and server inference where throughput per watt sets operating cost. No case study, no numbers |
| Fastest credible 48-hour demo | Camera + small arm waste-sorting station running a vision model fully on-device, with a live **joules-per-sorted-item** meter comparing baseline vs optimised model |
| Biggest risk | Nothing self-serve: no docs, SDK or published hardware. If the team cannot port your model within hours, you have no Omnicor component in the demo |
| Pairs well with (other vendors on site) | Galbot and AGIBOT (both shown as customers on Omnicor's site), Dobot (sorting arm), D-Robotics (RDK boards as comparison or fallback compute), Unitree Go2 (patrol / monitoring) |

## Why
- T03 explicitly rewards lower emissions and smarter resources; **energy per inference** is the one sustainability lever Omnicor can move, and it is measurable with a wall-plug meter.
- On-device inference removes the cloud round trip: works with patchy alpine connectivity and gives a clean "no data-centre" story.
- The site lists **OpenVLA** and **pi0.5 (LeRobot)** among deployed models, so a manipulation policy for sorting or litter picking is in their stated scope.
- Customer logos for **Galbot** and **AGIBOT** suggest an existing integration path to robots that are physically on site (scope not public).

## Not a fit for
- Teams that need a robot, sensors or a documented API from a single vendor — Omnicor provides none publicly.
- Projects whose value is physical (waste handling, EV charging) and whose model already runs on a laptop: the extra integration buys little.

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Products and solutions](Omnicor-AI-T03-2-Products-and-Solutions.md) · [Playbook](Omnicor-AI-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)

## Sources
- [OmniCor AI official website](https://www.omnicorai.io/)
