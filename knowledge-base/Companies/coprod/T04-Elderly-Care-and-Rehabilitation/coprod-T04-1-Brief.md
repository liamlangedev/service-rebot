---
type: challenge-brief
company: "coprod Inc."
slug: coprod
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# coprod Inc. × T04 Elderly Care & Rehabilitation — Brief

**Fit: 2/5** — Supporting role only: coprod sells joint-level building blocks (torque-controlled axis, IMU, power), not a care robot, and has no public work in care or rehab.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **co:motion** controller + motor (🧪 pre-order) or **co:act** actuator (**10 Nm** cont. / **25 Nm** peak, 🧪 coming soon), with **co:sense** IMU and **co:power** e-stop logic, driven from the `cosystem` Python API |
| Strongest proof point (real deployment or demo + date) | None in this domain. Only proof of the stack: in-house biped **co:dodo**, first motion **Dec 2025** |
| Fastest credible 48-hour demo | One-axis **rehab dial**: a motorised handle that resists, assists or guides wrist / forearm exercise and logs range of motion and effort to a therapist dashboard |
| Biggest risk | Kit availability and SDK access: hardware is pre-order, no public docs or code, **no Safe Torque Off module yet**, no medical certification |
| Pairs well with (other vendors on site) | **OriginFlow** (EMG intent → assist torque) · **XREAL** (AR exercise feedback) · **Flexiv** (finished force-controlled arm for anything that must touch a person) · **D-Robotics** (edge compute for vision / UI) |

## Why
- A quasi-direct-drive joint with simultaneous torque / velocity / position control at **1 kHz** is the right primitive for haptic exercise devices and assist-as-needed joints.
- The home-page API sample (wheel velocities + IMU angles + supply voltage) maps almost directly onto a **slope-aware rollator** — relevant to steep Leukerbad streets.
- **co:sense** (9-axis, dual-redundant, 1 kHz fusion) gives clean tilt / sway data for balance or tip-over detection.
- Three-founder Swiss start-up: if the founders are at the booth, their hands-on help is the real asset (kit count on site ⚠️ unverified).

## Not a fit for
- Any team that wants a finished robot (fetch-and-carry, feeding, companionship, night rounds) — coprod has no arm, no mobile base, no perception or AI stack.
- Anything that loads or lifts a real patient: 10 Nm class torque, no STO, no certification.
- Teams without mechatronics / EtherCAT / real-time Linux skills.

## Sources
- [coprod — products](https://coprod.co/products.html) · [coprod — home / API sample](https://coprod.co/) · [coprod — systems](https://coprod.co/systems.html) · [Venture Kick, 2 Apr 2026](https://www.venturekick.ch/coprod-receives-CHF-40000-from-Venture-Kick-to-build-scalable-interoperable-robotics-ecosystem)

⬆ [coprod Inc. profile](../coprod.md) · [Products and solutions](coprod-T04-2-Products-and-Solutions.md) · [Playbook](coprod-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
