---
type: challenge-playbook
company: "D-Robotics"
slug: D-Robotics
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# D-Robotics × T04 — Hackathon Playbook

⬆ [D-Robotics profile](../D-Robotics.md) · [Brief](D-Robotics-T04-1-Brief.md) · [Products and solutions](D-Robotics-T04-2-Products-and-Solutions.md)

**Framing:** D-Robotics is the sensing / AI brain. Concepts 1–2 need only a board and a camera. Concepts 3–4 need another vendor's robot. Which boards and cameras are on site is not confirmed: check at the booth before committing.

## Solution approaches

### Concept 1 — Room Guardian (private fall and inactivity sensor)

- **Problem → value:** falls at night in clinic or hotel rooms go unnoticed; cameras streaming video are unacceptable. A node that keeps video on the device and sends only events gives fast alerts with privacy.
- **Hardware:** RDK X5 + MIPI or USB camera + small speaker. Optional second node to show scaling.
- **Architecture / stack:** camera → `mono2d_body_detection` (boxes, keypoints, track IDs; BPU) → `hobot_falldown_detection` (fall event, sensitivity 0–3) → your `rclpy` node (debounce, "on floor longer than N seconds", bed / chair zones) → check-in prompt (pre-recorded audio or `hobot_tts`) → reply by hand gesture (`hand_gesture_detection`: ThumbUp = fine, Palm = help) → alert to a caregiver web page over MQTT / HTTP. All compute on the board.
- **48-hour plan:**
  - H0–6: flash board, install TROS, run the stock fall demo, view it at `http://<IP>:8000`.
  - H6–24: event logic node, gesture reply, caregiver dashboard; record test clips (fall, sit, bend, lie on bed).
  - H24–40: tune false alarms, add stick-figure-only display, second node if hardware allows.
  - H40–48: rehearse; freeze code; record a backup video.
- **3-minute demo script:** show the dashboard with a stick figure, no video → teammate sits, bends, lies on a bench (no alarm) → teammate goes down on a mat (alarm within seconds) → speaker asks "are you OK?" → ThumbUp cancels; second fall with no reply escalates → close with cost per room.
- **Risks and fallbacks:** stock fall logic is simple (docs test by rotating the camera) → add your own rule on keypoint height and box aspect ratio. Occlusion by furniture → mount the camera high in a corner. Gesture misses → add a big physical button.
- **Judging angles:** impact and Leukerbad relevance are high (rehab clinics, elderly spa guests, wet floors); technical depth is moderate; innovation comes from the privacy design and the cancel-by-gesture loop.

### Concept 2 — Rehab Coach (automatic chair-stand test and exercise counter)

- **Problem → value:** therapists time and count standard mobility tests by hand (for example the 30-second chair-stand test) and patients do home exercises unsupervised. A camera node counts repetitions, measures range of motion and speaks feedback.
- **Hardware:** RDK X5 (or S100) + camera + speaker / screen. Optional: XREAL glasses as therapist or patient display; OriginFlow EMG for muscle-activation overlay.
- **Architecture / stack:** camera → keypoints (`mono2d_body_detection` on X5, `mono2d_yolo_pose` on S100) → your node computes joint angles in the image plane (hip / knee for sit-to-stand, shoulder for arm raises), a state machine counts reps and timing → feedback via audio and a web UI → session report (reps, tempo, asymmetry) as JSON / PDF. Optional VLM (`hobot_llamacpp`) for a plain-language session summary.
- **48-hour plan:**
  - H0–6: keypoints running; log them to a file; pick two exercises.
  - H6–24: angle maths, rep state machine, live UI with skeleton and counter.
  - H24–40: voice prompts, report export, optional XREAL / EMG integration.
  - H40–48: test with 5+ different people and clothing; rehearse.
- **3-minute demo script:** judge sits on a chair → "start" by raising a hand → 30 seconds of sit-to-stand with live count → spoken result and a one-page report → show a deliberately shallow rep being rejected.
- **Risks and fallbacks:** keypoints are 2D → fix the camera side-on and mark the floor. Keypoint jitter → smooth over a few frames. Voice language → pre-recorded German / French / English prompts.
- **Judging angles:** very strong local story (thermal-spa rehabilitation); clear measurable output; low hardware risk. Not medically validated: say so.

### Concept 3 — Night-Round Companion (sensor brain on a mobile robot)

- **Problem → value:** night staff walk corridors to check on residents. A robot that patrols, spots a person on the floor or out of bed, asks a question and calls staff saves rounds and shortens response time.
- **Hardware:** RDK X5 or S100 + camera, mounted on another vendor's base: Unitree Go2, Genisom or Magiclab quadruped, or a wheeled platform (Galaxea, UniX AI).
- **Architecture / stack:** robot's own SDK handles locomotion; RDK runs person / fall detection and `reid` person following; a bridge node sends velocity or waypoint commands to the robot over ROS 2 / network; optional `slam` + `navigation2` only if the base exposes odometry and lidar cleanly; alerts as in Concept 1.
- **48-hour plan:**
  - H0–6: confirm the robot's control interface and that an external computer may command it; get Concept 1 running on the bench.
  - H6–24: mount and power the board; teleop + detection together; simple patrol route.
  - H24–40: stop-and-approach on fall event; voice / gesture check-in; dashboard.
  - H40–48: full run-throughs in the demo area; backup video.
- **3-minute demo script:** robot walks a short loop → finds a person lying down → stops at a safe distance, asks, waits → no reply: alert with location on the dashboard → ThumbUp: robot resumes.
- **Risks and fallbacks:** robot availability and SDK access → fall back to a fixed node (Concept 1) plus teleoperated robot. Low camera angle on a quadruped changes how a fall looks → retune rules. Powering the board from the robot → use a USB-C power bank.
- **Judging angles:** best "robot on stage" factor of the low-risk options; relieves caregivers; fits clinics and hotels at night.

### Concept 4 — Fall-Response Fetch (sensor triggers a manipulator)

- **Problem → value:** after a fall or when a resident cannot get up, the first need is a phone, water or medication within reach. Room sensor detects, a mobile manipulator brings the item.
- **Hardware:** RDK X5 guardian node + a mobile manipulator from Galaxea, Galbot, UniX AI or Spirit AI; or, for a table-top version, RDK S100 + small LeRobot-style arms (⚠️ unverified that such arms are on site).
- **Architecture / stack:** Concept 1 pipeline publishes an event with a rough location → task node asks the manipulator (its own VLA / skill API) to pick a known item and deliver it → handover confirmed by gesture. Table-top variant: record teleop demos, train ACT on a GPU laptop (about 4 h in D-Robotics' post), convert to `.hbm` with the OpenExplorer Docker toolchain, run on S100.
- **48-hour plan:**
  - H0–6: secure robot time; define one item and one route; guardian node running.
  - H6–24: scripted pick-and-deliver on the robot; event trigger wired up.
  - H24–40: end-to-end runs; handover confirmation; (variant) data collection and training overnight.
  - H40–48: reliability runs; cut scope to what works three times in a row.
- **3-minute demo script:** person goes down on a mat → alert → robot picks the "emergency kit" from a shelf and brings it → ThumbUp ends the task → dashboard shows the timeline.
- **Risks and fallbacks:** two vendors' stacks in 48 hours is the main risk → keep the interface to one message ("deliver item to zone B"). Model conversion can eat a day → skip ACT and use the manipulator vendor's built-in skills.
- **Judging angles:** highest innovation and technical depth; shows a full sense-decide-act care loop; most likely to fail live, so carry a video.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| RDK X5 + Unitree Go2 (or Genisom / Magiclab quadruped) | Patrol robot with on-board fall / person detection | Medium: mount, power, command bridge |
| RDK X5 + Galaxea / Galbot / UniX AI / Spirit AI mobile manipulator | Room sensor that dispatches a fetch task | Medium–high: two stacks, one message interface |
| RDK X5 + Flexiv Rizon or ROKAE xMate | Camera-guided, force-controlled rehab or massage: RDK tracks the limb, the arm does compliant motion | High: safety around people, calibration |
| RDK X5 + XREAL glasses | Therapist sees live joint angles and rep counts; or patient sees guidance | Low–medium: web view or simple stream to the glasses |
| RDK X5 / S100 + OriginFlow EMG | Pose + muscle activation for rehab quality scoring | Medium: time sync of two data streams |
| RDK S100 + WUJI hand / Dobot or Unitree arm | Learned handover (ACT) on a single arm | High: data, training, model conversion |
| RDK + SKYLANDX MetaCam | Pre-scanned 3D map of a ward for zones and robot navigation | Medium: map export format ⚠️ unverified |

## Questions to ask the D-Robotics engineers on site

1. Which boards, cameras, microphones and speakers can teams borrow, and how many?
2. Does `hobot_falldown_detection` run on RDK S100 with `mono2d_yolo_pose` output, or only on X3 / X5?
3. What rule does the fall detector use, and what does the sensitivity parameter change?
4. Which languages do `sensevoice_ros2` and `hobot_tts` support on the board (English, German, French)?
5. Is there a ready image with TROS and the body / gesture / voice demos pre-installed?
6. What is the fastest path to run a custom ONNX model on X5 this weekend, and how long does conversion take?
7. Can the body keypoints be lifted to 3D with the stereo camera, and is there an example?
8. Has anyone here already bridged an RDK to a Unitree or Galaxea robot, and is that code shareable?

## Decision rule

- **Pick D-Robotics for T04 if** your idea is sensing-first (fall, activity, exercise, gesture, voice), privacy matters, you are comfortable in ROS 2 / Linux, and you either need no robot body or have secured one from another vendor.
- **Avoid if** your idea depends on physical contact or manipulation and you want one vendor to provide it, or nobody on the team has ROS 2 / embedded Linux experience.

## Sources
- [TROS: pose (fall) detection app](https://developer.d-robotics.cc/tros_doc/en/apps/fall_detection)
- [TROS: human body detection and keypoints](https://developer.d-robotics.cc/tros_doc/en/boxs/body/mono2d_body_detection)
- [TROS: hand gesture recognition](https://developer.d-robotics.cc/tros_doc/en/boxs/body/hand_gesture_detection)
- [TogetheROS.Bot docs index](https://developer.d-robotics.cc/tros_doc/en/tros)
- [GitHub: hobot_falldown_detection](https://github.com/D-Robotics/hobot_falldown_detection)
- [GitHub: hobot_llamacpp](https://github.com/D-Robotics/hobot_llamacpp)
- [GitHub: sensevoice_ros2](https://github.com/D-Robotics/sensevoice_ros2)
- [GitHub: rdk_model_zoo](https://github.com/D-Robotics/rdk_model_zoo)
- [Forum: LeRobot ACT policy on RDK](https://forum-en.d-robotics.cc/t/lerobot-act-policy-on-rdk/391)
- [D-Robotics profile (general research)](../D-Robotics.md)
