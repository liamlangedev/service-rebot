---
type: challenge-brief
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
challenge: T03
challenge_title: "Sustainable City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# Leadshine Technology Co., Ltd. × T03 Sustainable City — Brief

**Fit: 2/5** — Supporting role only: Leadshine sells parts (hands, joint modules, motors), not a robot or a sustainability product; here it is the *gripper* in someone else's sorting or repair cell.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **DH116** five-finger hand (11 DoF, **545 g**, whole-hand load up to **30 kg**, optional tactile sensing) on another vendor's arm |
| Strongest proof point (real deployment or demo + date) | **None in this domain.** Closest: undated, unnamed logistics case studies on the Leadshine site (servo drives in AGV/AMR and cross-belt sorters; "low power consumption" claimed, no figures) |
| Fastest credible 48-hour demo | Bench-mounted DH116 "squeeze-to-sort": camera plus touch classifies PET / can / glass / carton and lights the right bin; add a host arm if integration goes well |
| Biggest risk | Needs a host arm, flange, power and bus bring-up — and a two-finger gripper sorts simple items just as well |
| Pairs well with (other vendors on site) | Flexiv, Dobot or ROKAE (arm) · D-Robotics (edge compute) · XREAL or OriginFlow (teleoperation) |

## Why
- **No domain product or deployment**: nothing public on waste, recycling, energy, EV charging or environmental monitoring.
- **Hands are the only quickly programmable item**: LHandProLib SDK (C++ / Python), ROS 2 example, URDF / MJCF.
- **Real value for irregular waste**: the tactile option reports normal and tangential force plus proximity.
- **Efficiency story is thin**: FM2 motor claims 20% lower loss (vendor claim); PJ3 / HJ2 joint modules have no public SDK or protocol.
- **Accessible price**: DH116 store price **USD 2,199** (USD 2,799 with tactile sensors).

## Not a fit for
- Teams wanting mobility, perception and autonomy in one platform.
- Monitoring, building-energy or EV-charging concepts.
- Wet, dirty or outdoor handling — no IP rating is published for the hands.

## Sources
- [DH116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh116-series.html) · [Logistics solution page](https://www.leadshine.com/solution/logistics-industry.html) · [Store: DH116 price](https://store.leadshine.com/products/dh116-r1-dexterous-hand) (via profile) · [Company profile](../Leadshine.md)

⬆ [Leadshine Technology Co., Ltd. profile](../Leadshine.md) · [Products and solutions](Leadshine-T03-2-Products-and-Solutions.md) · [Playbook](Leadshine-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
