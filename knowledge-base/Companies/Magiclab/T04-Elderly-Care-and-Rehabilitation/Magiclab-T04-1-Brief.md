---
type: challenge-brief
company: "Magiclab Robotics"
slug: Magiclab
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# Magiclab Robotics × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — Good programmable *bodies* for companion, escort, delivery and exercise-coach demos, plus a declared non-clinical healthcare vertical and an **RMB 150M** home-health order (Apr 2026) — but no named care-facility deployment, no rehab, mobility-support or health-monitoring product and no safe physical-contact capability (details: [register](Magiclab-T04-4-Solutions-Register-and-Papers.md)).

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **MagicDog EDU** (16 kg quadruped; SDK with SLAM, navigation, audio; built-in person following) and **MagicBot Z1 Development Version** (1.37 m humanoid; SDK with TTS / dialog, RGB-D, LiDAR, SLAM / navigation). On-site units not confirmed. |
| Strongest proof point (real deployment or demo + date) | None in care. Closest: hospital sample / emergency-medicine transport with MagicDog T1 described as *prospective* at IFA Berlin, **Sep 2026** (company statement). |
| Fastest credible 48-hour demo | MagicDog EDU as **medication and item runner with spoken reminders**: map a corridor, navigate to "rooms", speak, wait for pick-up, report to a caregiver dashboard. |
| Biggest risk | Edition and safety: only **EDU / Development Version** units are programmable, and a 40 kg biped must not operate within reach of frail people. Arm payload is only **2–3 kg**. |
| Pairs well with (other vendors on site) | OriginFlow (EMG for rehab feedback) · XREAL (therapist / tele-care view) · D-Robotics (on-board perception) · Flexiv or ROKAE (force-controlled contact tasks Magiclab cannot do) |

## Why
- **SDK covers the care-demo basics**: both the Z1 and MagicDog SDKs ship Python examples for audio (TTS, dialog, wake-up), sensors, SLAM and navigation — little plumbing before you build the care logic.
- **MagicDog has person following, human recognition, voice and an "emotion engine" built in** (official page) — a head start for walking-escort and companion ideas.
- **Small, non-threatening form factors**: a 16 kg dog and a 1.37 m humanoid fit clinic corridors better than full-size machines.
- **Leukerbad angle**: rehab clinics and thermal baths need escorting, reminders and small-item logistics — tasks that need no physical contact.

## Not a fit for
- Anything that touches or supports a person: transfers, lifting, walking support, massage, feeding, dressing.
- Fine assistive manipulation, unless a Development Version Z1 with dexterous hands or a MagicArm R1 is actually on site.
- Teams wanting a ready-made care or rehab software stack — there is none.

⬆ [Magiclab Robotics profile](../Magiclab.md) · [Products and solutions](Magiclab-T04-2-Products-and-Solutions.md) · [Playbook](Magiclab-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
