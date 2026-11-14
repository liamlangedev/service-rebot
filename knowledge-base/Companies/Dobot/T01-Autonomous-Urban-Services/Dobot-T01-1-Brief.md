---
type: challenge-brief
company: "Dobot Robotics"
slug: Dobot
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# Dobot Robotics × T01 Autonomous Urban Services — Brief

**Fit: 3/5** — Strong for the "serve and hand over" half of urban services (kiosk, pick-up point, loading cell); weak for the "move through the city" half, which needs another vendor's mobile base.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Nova 2 / Nova 5** (2 / 5 kg, 11 / 14 kg, IP54, controller runs on **30–60 V DC**) or **Magician E6** on a table; **E6 ROS Mobile Platform** if it is on site (Dobot's only arm-on-wheels: dual LiDAR, ≥0.5 m/s, >2 h loaded). On-site line-up is unconfirmed |
| Strongest proof point | Dobot's "New Retail" industry page: cobots in unmanned coffee, ice-cream, noodle and beverage kiosks, with three kiosk case studies (undated, customers unnamed). No street-delivery, cleaning or municipal deployment found |
| Fastest credible 48-hour demo | Unattended **resort service point**: order by QR or voice → camera finds the item → arm picks it and hands it to a guest or loads it into a partner delivery robot |
| Biggest risk | No outdoor mobility or navigation stack of its own; a fixed cell can look like a factory demo unless the "city" story (24/7, unattended, hand-off to a mobile robot) is made explicit |
| Pairs well with | Unitree Go2 / B2 or AGIBOT D1 (carrier), D-Robotics RDK X5 (edge vision), SKYLANDX MetaCam (site map), XREAL (operator view), WUJI Hand (dexterous end-effector) |

## Why
- **Fastest arm to get moving:** one TCP/IP API, Python repo updated 2026-11-13, ROS 2 Humble package with MoveIt and Gazebo configs.
- **Service use is Dobot's own positioning:** Nova 2 is labelled "For Retail"; the Atom page names coffee-shop drinks and night-time pharmacy dispensing as scenarios.
- **Safe next to the public:** collision stop in 0.01 s, five protection levels, drag-to-teach.
- **Mobile-ready power:** the Nova controller (1.3 kg, DC input) can ride on a battery-powered base (integration is yours to do).
- **Local hook:** a Swiss winery palletizes wine boxes with a CR20A via Swiss integrator zmb.

## Not a fit for
- Outdoor last-mile delivery, snow or steep-street navigation, sweeping or cleaning robots.
- Guide / wayfinding robots, unless LUMO or Atom is actually handed to teams (no public LUMO SDK).
- Anything needing torque-level control or more than IP54 on the hardware likely on site.

## Sources
- [Nova series](https://www.dobot-robots.com/products/nova-series/dobot-nova-series.html) · [E6 ROS Mobile Platform](https://www.dobot-robots.com/products/education/ros-mobile-platform.html) · [New Retail page](https://www.dobot-robots.com/industries/new-retail.html) · [Atom](https://www.dobot-robots.com/products/humanoid-robots/atom.html) · [Swiss winery case study](https://www.dobot-robots.com/insights/case-studies/wine-box-palletizing-automation-with-dobot-cr20a.html) · [TCP-IP-Python-V4](https://github.com/Dobot-Arm/TCP-IP-Python-V4) · [DOBOT_6Axis_ROS2_V4](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V4)

⬆ [Dobot Robotics profile](../Dobot.md) · [Products and solutions](Dobot-T01-2-Products-and-Solutions.md) · [Playbook](Dobot-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
