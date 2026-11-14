---
type: challenge-brief
company: "Galbot"
slug: Galbot
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# Galbot × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — Best robot on site for "find the right medication or item, bring it, hand it over"; not built for physical support, rehab contact or outdoor use, and it has no documented care deployment.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Galbot G1** (wheeled dual-arm, **5 kg per arm**, wrist reach floor to **2.1 m**, **8 h** runtime, wrist F/T sensors) + **GalbotSDK V1.10.0** (Python / C++) |
| Strongest proof point | G1 pharmacy picking in daily commercial use: Laobaixing Pharmacy, Shanghai (**Sep 2026**, 400-500 orders/day, ~68 s per order, company data) and a 24/7 drugstore in Haidian, Beijing (**Mar 2026**, ~5,000 SKUs) |
| Fastest credible 48-hour demo | Medication and item round: G1 picks the correct box from a shelf, drives to a seated "resident", confirms identity, hands over with force-triggered release, logs the event |
| Biggest risk | What is unlocked on the on-site robot (SDK level, grasp model) is unknown; no public safety certification for close contact with frail people |
| Pairs well with | D-Robotics (edge fall / pose detection) · XREAL (caregiver AR, tele-care) · OriginFlow (EMG for rehab feedback) · Flexiv (force-controlled contact tasks G1 should not do) |

## Why
- The pharmacy stack is the same task as a care-home medication round: identify, pick, verify, deliver, log.
- Wrist reach from the floor to 2.1 m covers dropped objects and high shelves, two things mobility-limited people struggle with.
- The SDK ships ready examples for navigation to goals, collision-aware arm planning, pick and place, audio, force-sensor reading and VLA execution.
- Leukerbad fit: rehab clinics and spa hotels with many elderly guests and few night staff; a fetch-and-deliver aide is easy to explain to judges.

## Not a fit for
- Lifting, transferring or steadying a person (arms are 5 kg class; no such use is documented).
- Massage, physiotherapy contact or exoskeleton-type rehab.
- Anything outdoors, on stairs or on snow (wheeled, IP54, 0-40 °C).

## Sources
- [Galbot G1 product page](http://www.galbot.com/g1/) · [GalbotSDK](https://github.com/GalaxyGeneralRobotics/GalbotSDK) · [The Paper, 2026-09-30](https://m.thepaper.cn/newsDetail_forward_34179567) · [CGTN, 2026-03-13](https://news.cgtn.com/news/2026-03-13/China-s-first-pharmacy-robot-goes-into-service-in-Beijing-1LtZ7juLcZ2/p.html)

⬆ [Galbot profile](../Galbot.md) · [Products and solutions](Galbot-T04-2-Products-and-Solutions.md) · [Playbook](Galbot-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
