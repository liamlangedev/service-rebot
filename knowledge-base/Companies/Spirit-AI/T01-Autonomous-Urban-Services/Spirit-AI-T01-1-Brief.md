---
type: challenge-brief
company: "Spirit AI"
slug: Spirit-AI
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# Spirit AI × T01 Autonomous Urban Services — Brief

**Fit: 3/5** — A capable **indoor** fetch-deliver-tidy mobile manipulator (Moz1) with a documented LiDAR navigation stack and Python SDK; strictly indoor (IP40, no rain or snow), and the company has no deployed urban-service case yet.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Moz1** ✅ — wheeled dual-arm humanoid, **26 DoF**, Livox MID-360S LiDAR + Nav2-based SLAM navigation, MozRobot Python SDK (ROS 2 Humble), Quest VR teleop. On-site presence ⚠️ unverified |
| Strongest proof point | No urban-service deployment. Closest: WAIC Shanghai, **July 2026** — Moz1 ran a one-instruction "tidy up the living room" task chain (cans, dishwasher, waste paper); **Moz2** 🧪 debuted there, aimed at hotel delivery, shelf stocking, building inspection and guiding. Real deployments are industrial (CATL line, Dec 2025) |
| Fastest credible 48-hour demo | Hotel / clinic **room-service runner**: map one floor, navigate to saved waypoints by ROS service, do one scripted or teleoperated pick-and-hand-over at each stop |
| Biggest risk | Access: probably **one** robot shared by many teams, Chinese-only docs, nav stack and SDK wheel come from the vendor, not a public repo. Spirit v1.5 fine-tuning needs **8× A100** — not a 48-hour path |
| Pairs well with | **D-Robotics** (announced partner; edge perception on RDK), **Unitree / Genisom / Magiclab** quadrupeds (outdoor leg, Moz1 takes over indoors), **SKYLANDX** (building scan), **XREAL** (operator view) |

## Why
- **Navigation is documented, not hypothetical:** mapping, saving and goal-sending scripts, plus a ROS service that takes a pose sequence.
- **Manipulation plus mobility in one unit:** two 7-DoF force-controlled arms, 6-DoF torso, omnidirectional base (**0.5 m/s** Cartesian limit).
- **Roadmap points here:** Moz2 targets retail, hospitality and office buildings — judges can see a product path.
- **Open model story:** Spirit v1.5 weights and code are MIT-licensed (useful for the pitch, less for the build).

## Not a fit for
- Anything **outdoors** in Leukerbad: streets, snow, slopes, stairs, kerbs.
- Teams that need guaranteed robot time or a fleet.
- Learning-based skills trained during the event.

## Sources
- [Docs: Moz1 SLAM navigation](https://docs.spirit-ai.com/zh/slam-nav/slam_navigation.html) · [Docs: Moz1 mechanical structure](https://docs.spirit-ai.com/zh/moz1/mechanics.html) · [Spirit AI news: WAIC 2026, Moz2](https://www.spirit-ai.com/en/news/48) · [GitHub: spirit-v1.5](https://github.com/Spirit-AI-Team/spirit-v1.5) · [Company profile](../Spirit-AI.md)

⬆ [Spirit AI profile](../Spirit-AI.md) · [Products and solutions](Spirit-AI-T01-2-Products-and-Solutions.md) · [Playbook](Spirit-AI-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
