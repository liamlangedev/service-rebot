---
type: challenge-brief
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# Leadshine Technology Co., Ltd. × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — A good *add-on* (human-like five-finger hand with SDK and optional touch sensing), not a platform: Leadshine has no robot, no care software and no care deployments.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **DH116S** compact hand (**359 g**, 11 DoF / 6 active, official ROS 2 Humble example) or **DH116-M** (tactile, **545 g**) on another vendor's arm; **DH2116** (21 DoF / 16 active) for finger-level therapy mirroring |
| Strongest proof point (real deployment or demo + date) | **None in care.** Closest: CES, 6–9 Jan 2026 — exoskeleton and medical-equipment makers "discussed cooperation" on its motors and joint modules; no deal named. Hands demoed live at CES, WAIC (Jul 2026), Automate (Jun 2026) |
| Fastest credible 48-hour demo | **Hand-rehab mirror coach:** webcam hand tracking → the robot hand shows and mirrors finger exercises, counts repetitions, scores range of motion. Needs no arm and no mobile base |
| Biggest risk | Hardware on site is unconfirmed; SDK comes as download archives (no GitHub); bus bring-up (EtherCAT / CAN FD / RS485) and mounting can eat half a day; not a medical device |
| Pairs well with (other vendors on site) | OriginFlow (EMG → hand control), XREAL (AR-guided therapy), Flexiv / ROKAE (force-controlled arm to carry the hand), Galaxea / AGIBOT / Unitree (host robots) |

## Why
- A five-finger hand is the most human-readable tool for care tasks: hand-overs, cups, pill boxes, door handles.
- Developer stack exists for the hands only: **LHandProLib** (C++ / Python, Windows / Linux, x86 / ARM), ROS 2 example, URDF / MJCF.
- DH116-M adds fingertip tactile sensors — useful for "gentle grip" and release-on-pull hand-overs.
- Cheap for its class: DH116 **USD 2,199**, tactile **USD 2,799** (store prices).
- PJ3 joint modules (USD 329–479) target exoskeleton-class joints, but no public SDK or protocol was found.

## Not a fit for
- Teams that want a ready robot, autonomy stack, or any mobility — Leadshine supplies none.
- Wearable exoskeleton or patient-contact force demos in 48 hours (no public joint-module SDK, no safety certification for body contact).
- Industrial servo / stepper / PLC builds — too much wiring and tuning for this event.

## Sources
- [Leadshine company profile](../Leadshine.md)
- [DH116S user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_Series_Dexterous_User_Manual.pdf) · [DH116 user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116_DH116P_Series_Dexterous_User_Manual.pdf) · [ROS 2 example (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_LHandPro_ROS2_Example_Project_Description.pdf)
- [CES 2026 release (PR Newswire Asia)](https://en.prnasia.com/releases/global/leadshine-achieves-great-success-at-ces-2026-entering-us-and-european-robotics-supply-chain-518892.shtml)

⬆ [Leadshine Technology Co., Ltd. profile](../Leadshine.md) · [Products and solutions](Leadshine-T04-2-Products-and-Solutions.md) · [Playbook](Leadshine-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
