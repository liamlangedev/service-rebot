---
type: challenge-brief
company: "Magiclab Robotics"
slug: Magiclab
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# Magiclab Robotics × T01 Autonomous Urban Services — Brief

**Fit: 4/5** — A small quadruped whose open SDK already ships SLAM, goal navigation, person-following and speech gives a direct 48-hour path to a delivery or guide robot; real but company-reported, mostly event-scale service proof exists (two-day campus food-delivery pilot with real orders in Apr 2026, a guided-tour product in museums and exhibition centres, traffic duty at the Wuxi Marathon), while long-running street delivery and any cleaning offer are absent — see the [register](Magiclab-T01-4-Solutions-Register-and-Papers.md).

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **MagicDog EDU** (16 kg, **5 kg** payload, 40° slope, 2D LiDAR + depth, SDK). Second choice **MagicDog-W** (wheel-legged, **10 kg**, 4G). On-site units are **not confirmed** — check edition first: PRO has no SDK. |
| Strongest proof point | Company-reported only: **IFA Berlin, Sep 2026** — MagicBot D1 parcel-sorting demo and an announced sorting partnership with **Pošta Slovenije** (no value or go-live date public). No street, hotel or municipal deployment found. |
| Fastest credible 48-hour demo | MagicDog EDU maps a corridor, takes a spoken or app request, carries a small parcel to a named waypoint via `/goal_pose`, announces arrival by TTS. |
| Biggest risk | ROS 2 SDK is thin (one commit, **Foxy / Ubuntu 20.04**, wired link to the control board) and may not match current firmware; small dogs have **no IP rating** — snow and wet streets are untested. |
| Pairs well with | D-Robotics (RDK X5 as on-dog ROS 2 computer), SKYLANDX (MetaCam prior map), XREAL (operator / tourist AR view), Flexiv or Dobot (fixed arm for load / unload). |

## Why
- Built-in stack covers the track's core loop: 2D LiDAR SLAM, saved-map localisation, goal-pose navigation, obstacle avoidance, tracking mode, TTS.
- Payload is enough for parcels, medicine bags, room-service items (**5–10 kg**, lab values).
- Legs handle Leukerbad's stairs, kerbs and slopes better than wheeled delivery carts.
- BSD-3 SDKs, URDFs and MuJoCo models are public — you can start before touching the robot.
- Company direction (postal sorting, hospital transport with MagicDog T1) matches the track, although mostly prospective.

## Not a fit for
- Manipulation-heavy services (cleaning, bin emptying, door opening): Z1 arms carry only **2–3 kg**; D1 is unlikely to be hackable on site.
- All-weather outdoor operation: only MagicDog-Y1 is **IP67 / −20 °C**, and it is unlikely to be available.
- Teams that need a mature, community-tested nav stack on day one.

⬆ [Magiclab Robotics profile](../Magiclab.md) · [Products and solutions](Magiclab-T01-2-Products-and-Solutions.md) · [Playbook](Magiclab-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)

## Sources
- [MagicDog product page](https://www.magiclab.top/en/dog)
- [MagicDog-W product page](https://www.magiclab.top/en/dog-w)
- [GitHub — magicdog_ros2_sdk](https://github.com/MagiclabRobotics/magicdog_ros2_sdk)
- [EqualOcean — MagicLab targets European logistics (IFA 2026)](https://equalocean.com/news/2026090822169-magiclab-targets-european-logistics-robotics-showcase-slovenia-postal)
- [Magiclab Robotics profile](../Magiclab.md)
