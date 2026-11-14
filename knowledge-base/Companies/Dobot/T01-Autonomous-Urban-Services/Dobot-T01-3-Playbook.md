---
type: challenge-playbook
company: "Dobot Robotics"
slug: Dobot
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Dobot Robotics × T01 — Hackathon Playbook

⬆ [Dobot Robotics profile](../Dobot.md) · [Brief](Dobot-T01-1-Brief.md) · [Products and solutions](Dobot-T01-2-Products-and-Solutions.md)

**Premise:** Dobot gives you a dependable arm, not a robot that travels. Every concept below either makes the *fixed service point* the hero, or pairs the arm with someone else's mobility. The on-site Dobot line-up is unconfirmed — the concepts are written so that a Magician E6, a Nova or a small CRA can be swapped in (scale the objects to the payload: **750 g / 2–5 kg / 3–5 kg**).

## Solution approaches

### Concept 1 — Alpine Service Point (unattended 24/7 pick-up kiosk)

- **Problem → value:** A resort town has peaks (arrival days, evenings) and closed counters at night. A robot cell hands out pre-ordered items — pharmacy parcel, rental key, spa kit, hot drink — at any hour with no staff. This is the use Dobot already markets (unmanned beverage and ice-cream kiosks).
- **Hardware:** Nova 2 / Nova 5 or Magician E6 on a table · gripper or suction cup · one RGB-D camera above the shelf · a few bins or lockers. Optional: D-Robotics RDK X5 for on-device vision.
- **Architecture / stack:**
  - *Perception:* camera → fiducial tags on bins first, open-vocabulary detector second → hand-eye transform (DobotCameraCalibrate).
  - *Planning:* order queue (web form + QR code) → simple state machine: locate → pick → present → confirm → retry.
  - *Control:* `TCP-IP-Python-V4` (MovJ / MovL, digital outputs for the gripper) or MoveIt via `DOBOT_6Axis_ROS2_V4` on Ubuntu 22.04 / Humble.
  - *Compute:* one laptop; LLM or speech in the cloud only for the order interface.
- **48-hour plan:**
  - **H0–6:** confirm firmware (V4), connect, run `main.py`, teach three poses by hand, mount camera.
  - **H6–24:** calibration, tag-based picking of 3–5 items, order web page, hand-over pose with "item taken" check.
  - **H24–40:** replace tags with learned detection for at least one item, add voice or multilingual ordering (DE / FR / EN), error recovery, usage log.
  - **H40–48:** freeze code, rehearse 10 runs, record a backup video.
- **3-minute demo script:** (0:00) the 22:00 problem: guest arrives, counters closed → (0:30) judge scans QR, picks an item on their phone → (1:00) arm finds, picks and presents it; judge takes it → (1:45) second order by voice in German, with a deliberately misplaced item to show recovery → (2:30) dashboard: orders served, time per order, staffing hours saved.
- **Risks and fallbacks:** detection unreliable → keep fiducial tags. Gripper missing → suction cup or a 3D-printed hook with hang-tag items. API trouble → drag-to-teach replay in DobotStudio Pro.
- **Judging angles:** *Innovation* low to medium (known pattern) · *Technical depth* medium · *Impact* clear staffing story · *Leukerbad relevance* high if the items are local (thermal-bath kit, pharmacy pick-up for clinic guests, ski-pass hand-out).

### Concept 2 — Dock-and-Load Hub (arm loads a delivery robot)

- **Problem → value:** Delivery robots still need a human to load them. A fixed arm at the "depot" (hotel back office, pharmacy, bakery) loads parcels into a legged or wheeled carrier, which then walks the steep last 300 m. Closes the loop to a fully unattended delivery.
- **Hardware:** Nova 5 or CR3A / CR5A as loader · carrier from another vendor: Unitree Go2 / B2, AGIBOT D1, Genisom M1 / L1 or Magiclab MagicDog with an open-top box · camera at the dock · fiducial tag on the carrier's box.
- **Architecture / stack:**
  - *Perception:* dock camera reads the tag on the carrier → box pose; second detection for parcels on the shelf.
  - *Planning:* dispatcher service: order → pick parcel → wait for "carrier docked" → place → release carrier → notify recipient.
  - *Control:* Dobot arm over TCP/IP; carrier through its own vendor SDK / navigation; the two talk through one small message bus (ROS 2 topics or HTTP).
  - *Compute:* laptop at the dock; carrier's onboard computer for navigation.
- **48-hour plan:**
  - **H0–6:** two sub-teams. Arm: pick-and-place into a static box. Carrier: drive a fixed route A → B → A.
  - **H6–24:** tag-based box localisation so the arm places correctly when the carrier stops ± 10 cm off; define the dock handshake.
  - **H24–40:** full loop with two different destinations; add recipient confirmation (QR at drop-off); handle "carrier not present" and "parcel dropped".
  - **H40–48:** rehearse on the real demo floor, tune stop positions, backup video.
- **3-minute demo script:** (0:00) map of Leukerbad: pharmacy to clinic, bakery to chalet, all uphill → (0:30) order placed → (0:50) carrier docks, arm loads the parcel → (1:30) carrier leaves, navigates to the "clinic" corner, recipient takes the parcel → (2:15) carrier returns and docks while the arm has already staged the next parcel → (2:40) numbers: loop time, hands-off rate.
- **Risks and fallbacks:** carrier navigation flaky → tele-operate the carrier and keep the loading autonomous (say so openly). Docking inaccurate → mechanical funnel / guide rails on the floor. Cross-vendor networking → agree the interface in hour 1 and mock both sides.
- **Judging angles:** *Innovation* medium to high (the unloved loading step) · *Technical depth* high (multi-robot handshake) · *Impact* direct for last-mile logistics · *Leukerbad relevance* high (steep, car-light streets; clinics and hotels).

### Concept 3 — Indoor Facility Runner (mobile manipulation for upkeep)

- **Problem → value:** Spa and clinic corridors need constant small jobs: collect left-behind items, restock towels or brochures, clear litter. One mobile manipulator does rounds between guests.
- **Hardware:** E6 ROS Mobile Platform if Dobot has one on site. Otherwise a Nova 2 (11 kg, DC-powered controller) on a partner wheeled base — only if both vendors' engineers agree on mounting and power. Optional: SKYLANDX MetaCam to build the reference map of the venue.
- **Architecture / stack:**
  - *Perception:* base LiDAR for localisation; arm- or mast-mounted camera for object detection.
  - *Planning:* patrol waypoints → detect target → approach pose → pick → carry to bin / shelf.
  - *Control:* the platform's ROS navigation (stack not documented publicly — confirm) plus the E6 over the V4 API.
  - *Compute:* platform's industrial PC (≥ 4 GB RAM) for navigation; laptop over Wi-Fi for vision.
- **48-hour plan:**
  - **H0–6:** verify the base maps and navigates out of the box; if not by H6, switch to Concept 1 or 2.
  - **H6–24:** waypoint patrol; stationary pick with the arm; base-to-arm transform.
  - **H24–40:** combined "see → stop → pick → deliver" for one object class under 750 g.
  - **H40–48:** rehearse, limit scope to what works 8 times out of 10.
- **3-minute demo script:** (0:00) the cost of small upkeep jobs in a spa → (0:30) robot starts its round, avoids a person → (1:15) spots a dropped item, stops, picks it up → (2:00) drives to the lost-and-found bin and drops it → (2:30) round log and what a fleet would cover.
- **Risks and fallbacks:** platform not on site (likely) → concept is off. ± 5 cm navigation accuracy vs 450 mm arm reach → always re-localise the object with the camera before grasping. Small arm payload → choose light objects.
- **Judging angles:** *Innovation* medium · *Technical depth* high (navigation + manipulation) · *Impact* medium · *Leukerbad relevance* high (thermal baths, rehabilitation clinics).

### Concept 4 — Teach-Once Service Skills (imitation learning on X-Trainer, or Atom as staff)

- **Problem → value:** Many service chores are too irregular to script — folding spa towels, bagging a mixed order, packing rental gear. Demonstrate the task 50–100 times by teleoperation and let a learned policy do it, so a non-programmer can add a new service.
- **Hardware:** X-Trainer (2 × Nova 2 with leader arms) and its cameras · GPU laptop or workstation. Stretch: Atom Max with VR teleop if Dobot allows hands-on use.
- **Architecture / stack:**
  - *Perception → control:* end-to-end visuomotor policy at the rig's **25 Hz** interface.
  - *Tooling:* `dobot_xtrainer` for teleop and collection, `Embodylink` for annotation and training management. Which policy architectures are supported is not stated publicly — confirm.
  - *Compute:* training on a local GPU or cloud; inference on the laptop.
- **48-hour plan:**
  - **H0–6:** teleop working, cameras fixed in place (do not move them again), choose one task with a clear success test.
  - **H6–24:** collect demonstrations, train a first policy overnight.
  - **H24–40:** evaluate, collect targeted recovery demos, retrain; wrap the skill behind the Concept 1 order interface.
  - **H40–48:** measure success rate over 20 trials, prepare a teleop fallback.
- **3-minute demo script:** (0:00) "this is how a hotel employee teaches the robot" — 20 s of live teleop → (0:40) policy performs the task autonomously → (1:40) change the object or position to show generalisation → (2:20) success-rate chart and time-to-teach.
- **Risks and fallbacks:** policy unreliable after 48 h (likely) → show teleoperated remote service as the product ("one operator, many kiosks") and autonomy as the upgrade path. No GPU → reduce to a single-arm, short-horizon task. X-Trainer not on site → drop to Concept 1.
- **Judging angles:** *Innovation* high · *Technical depth* high · *Impact* longer-term · *Leukerbad relevance* medium to high (seasonal staff shortage in hospitality).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Dobot arm (fixed) + Unitree Go2 / B2 or AGIBOT D1 | Unattended loading plus legged last-mile delivery on slopes (Concept 2) | **Medium** — separate SDKs, one handshake, tag-based docking |
| Dobot arm + D-Robotics RDK X5 / S100 | On-device detection, no laptop at the kiosk | **Low to medium** — camera pipeline on the board, arm over Ethernet |
| Dobot arm + WUJI Hand | Dexterous hand-over of odd-shaped items | **High** — mechanical adapter, power, separate hand SDK, payload budget |
| Dobot arm + XREAL glasses | Remote operator sees the kiosk and approves or corrects picks | **Medium** — video stream + simple command channel |
| Dobot arm + SKYLANDX MetaCam | 3D scan of the venue as a map or digital twin for the service story | **Low** for visuals, **medium** if used for navigation |
| Nova on a partner wheeled base (coprod modules or similar) | True mobile manipulation without the E6 platform | **High** — mounting, DC power (30–60 V), safety; only with both vendors' engineers |
| Dobot arm + OriginFlow EMG capture | Gesture or muscle-signal teleoperation of the service arm | **High** — experimental |

## Questions to ask the Dobot Robotics engineers on site

1. Which models and how many units can teams book — Magician E6, Nova 2 / 5, CR3A / CR5A, X-Trainer, E6 ROS Mobile Platform, Atom, Rover X1?
2. Which controller firmware is installed — is it **V4.4 or later**, so `TCP-IP-Python-V4` and `DOBOT_6Axis_ROS2_V4` work unchanged?
3. Which end-effectors and cameras are available (gripper, suction cup, wrist camera, VX500), and how are they triggered — digital output, RS485 or Modbus?
4. Can the Nova controller be powered from a partner robot's battery (30–60 V DC)? What peak current should we budget?
5. On the E6 ROS Mobile Platform: which ROS version and navigation stack ship on the industrial PC, and is there a ready mapping-and-navigation demo?
6. Is there a real-time streaming mode (ServoJ / ServoP) we may use for vision-guided or teleoperated motion, and at what rate?
7. For X-Trainer: which policy types does the supplied training code support, and how many demonstrations do you recommend for a short task?
8. Is there any SDK access to Rover X1 or LUMO, or to DobotWAM inference, during the event?

## Decision rule

- **Pick Dobot Robotics for T01 if** your idea is a service *point* (kiosk, pick-up, loading dock, counter task) and you want an arm that works in the first hours, with a second vendor supplying any movement through the town.
- **Avoid if** the core of your idea is autonomous navigation, outdoor delivery, cleaning or guiding people — start from a mobile platform vendor and add an arm only if time allows.

## Sources
- [Dobot company profile (this vault)](../Dobot.md)
- [Nova series](https://www.dobot-robots.com/products/nova-series/dobot-nova-series.html)
- [E6 ROS Mobile Platform](https://www.dobot-robots.com/products/education/ros-mobile-platform.html)
- [Magician E6](https://www.dobot-robots.com/products/education/magician-e6.html)
- [X-Trainer](https://www.dobot-robots.com/products/humanoid-robots/x-trainer.html)
- [Atom humanoid](https://www.dobot-robots.com/products/humanoid-robots/atom.html)
- [New Retail industry page](https://www.dobot-robots.com/industries/new-retail.html)
- [Automated milk tea machine](https://www.dobot-robots.com/insights/case-studies/automated-milk-tea-machine.html)
- [Automated ice cream booth](https://www.dobot-robots.com/insights/case-studies/automated-ice-cream-booth.html)
- [Dobot-Arm on GitHub](https://github.com/Dobot-Arm)
- [TCP-IP-Python-V4](https://github.com/Dobot-Arm/TCP-IP-Python-V4)
- [DOBOT_6Axis_ROS2_V4](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V4)
