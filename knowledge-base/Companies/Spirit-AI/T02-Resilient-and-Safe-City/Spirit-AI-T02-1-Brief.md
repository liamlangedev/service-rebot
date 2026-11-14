---
type: challenge-brief
company: "Spirit AI"
slug: Spirit-AI
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# Spirit AI × T02 Resilient & Safe City — Brief

**Fit: 2/5** — Supporting role only: Moz1 is an indoor, flat-floor, **IP40** dual-arm manipulator with no safety or emergency track record; use it as "remote hands" in a plant room, not as the responder.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Moz1** ✅ — 26 DoF, two 7-DoF force-controlled arms, Livox MID-360S LiDAR + Nav2, Quest VR teleop, Python SDK (up to **120 Hz**) |
| Strongest proof point (real deployment or demo + date) | None in this domain. Nearest: CATL factory deployment (reported Dec 2025); "building inspection" named as a *future* Moz2 use (WAIC, July 2026) 🧪 |
| Fastest credible 48-hour demo | VR-teleoperated Moz1 closes a valve / flips a breaker in a mock unsafe technical room, after a waypoint patrol to get there |
| Biggest risk | No rain, snow, wet floors, stairs or outdoor use; probably one shared unit ⚠️ unverified; Chinese-only docs |
| Pairs well with (other vendors on site) | Unitree or Genisom quadruped (outdoor scout), SKYLANDX MetaCam (3D map), XREAL (operator view), D-Robotics RDK (edge perception) |

## Why
- **Manipulation is the differentiator:** most T02 robots can look; Moz1 can turn, press, pull and carry.
- **Teleop works on day 1** without training a model — but the documented setup is cabled and local; operator video is your job.
- **Indoor autonomy exists:** LiDAR SLAM + Navigation2, goals sent by ROS 2 service — enough for an inspection round.
- **Narrow operating range:** **-10 to 50 °C**, ≤ **75 % RH**, IP40, explicitly not for rain, snow or outdoors.
- **No domain evidence:** all confirmed work is factory and retail.

## Not a fit for
- Outdoor hazards: avalanche, rockfall, flood, snow, steep paths, stairs.
- Search and rescue, fire, wet or dusty scenes, anything needing an IP or ATEX rating.
- A trained VLA skill in 48 hours without cloud GPUs.

## Sources
- Docs: [Moz1 mechanics](https://docs.spirit-ai.com/zh/moz1/mechanics.html) · [SLAM navigation](https://docs.spirit-ai.com/zh/slam-nav/slam_navigation.html) · [Teleoperation](https://docs.spirit-ai.com/zh/teleop/get-started.html) · [SDK API](https://docs.spirit-ai.com/zh/sdk/api.html)
- [Spirit AI news: WAIC 2026, Moz2 debut](https://www.spirit-ai.com/en/news/48) (web search unavailable for this pass; official pages only)

⬆ [Spirit AI profile](../Spirit-AI.md) · [Products and solutions](Spirit-AI-T02-2-Products-and-Solutions.md) · [Playbook](Spirit-AI-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
