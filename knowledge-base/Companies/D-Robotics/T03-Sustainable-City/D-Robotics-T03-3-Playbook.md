---
type: challenge-playbook
company: "D-Robotics"
slug: D-Robotics
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# D-Robotics × T03 — Hackathon Playbook

⬆ [D-Robotics profile](../D-Robotics.md) · [Brief](D-Robotics-T03-1-Brief.md) · [Products and solutions](D-Robotics-T03-2-Products-and-Solutions.md)

**Framing:** D-Robotics gives you eyes and a brain (RDK X5 / S100 + TogetheROS.Bot), not a body. Concept 1 needs no other vendor; concepts 2–4 need one. What D-Robotics actually brings on site is not confirmed, so check the booth before committing.

## Solution approaches

### Concept 1 — Bin Coach: a smart recycling point that needs no robot

- **Problem → value:** resort guests from many countries do not know the Swiss separate-collection rules (PET, aluminium, glass, paper), so recyclables end up in residual waste. A camera node tells each person which bin to use and logs contamination, so the municipality sees where signage or extra bins are needed.
- **Hardware:** RDK X5 + MIPI or USB camera + small screen / speaker / LED strip on GPIO. Optional: PoE module for single-cable install, a servo flap on PWM as a minimal actuator. Optional other vendor: XREAL glasses as a staff view of the statistics.
- **Architecture / stack:**
  - Perception: `mipi_cam` → `hobot_yolo_world` with a text vocabulary (bottle, can, glass bottle, paper cup …), fallback to a stock YOLO model from the Model Zoo.
  - Decision: small `rclpy` node maps class → bin, counts items, debounces.
  - Output: TTS node for a spoken hint, GPIO for LEDs, a web page for counts. Optional `hobot_llamacpp` VLM for "unknown item" explanations.
  - Compute: everything on the X5, no cloud.
- **48-hour plan:**
  - H0–6: flash board, run the YOLO-World sample, test 10 real waste items, write down which words work.
  - H6–24: class → bin logic, LED / voice output, logging, simple dashboard.
  - H24–40: build the physical bin mock-up, measure power with a USB-C meter, tune thresholds under venue lighting.
  - H40–48: rehearse, record a backup video.
- **3-minute demo script:** (1) Hold up a PET bottle: the correct bin lights up and the node speaks. (2) Try a tricky item (coffee cup): show the VLM explanation. (3) Show the dashboard: items per class, contamination rate. (4) Show the power meter and the per-node cost.
- **Risks and fallbacks:** vocabulary does not cover an item → restrict the demo to classes that work, or use CLIP zero-shot classification on a cropped image. Lighting → add a cheap LED light and a plain background.
- **Judging angles:** innovation low to medium; technical depth medium (fully on-device); impact clear and measurable; Leukerbad relevance high (tourist resort, multilingual guests). Weak point: it is barely a robot.

### Concept 2 — Vision-guided sorting cell with another vendor's arm

- **Problem → value:** small municipalities cannot afford industrial sorting lines; a low-cost camera brain plus a cobot sorts mixed recyclables at a collection point or hotel back-of-house.
- **Hardware:** RDK X5 + overhead camera (stereo module if available) + **Dobot CR / Nova, Flexiv Rizon or ROKAE xMate** arm with a gripper or suction cup + three bins.
- **Architecture / stack:**
  - Perception: YOLO-World or YOLOv8-Seg for class and mask; pick point from the mask centre; depth from `hobot_stereonet`, or assume a flat table and use a one-time homography from four markers.
  - Planning: pick the highest-confidence item, choose the bin by class, simple state machine.
  - Control: the arm vendor's SDK or ROS 2 driver, running on the arm controller or a laptop; the X5 only sends target poses over ROS 2 / Ethernet.
- **48-hour plan:**
  - H0–6: confirm the arm's control interface with its vendor; get detections streaming from the X5.
  - H6–24: camera-to-arm calibration, first pick of one object class.
  - H24–40: three classes, bin placement, retry on failed grasp, throughput counter.
  - H40–48: stress test with random item layouts, demo polish.
- **3-minute demo script:** (1) Tip mixed items onto the table. (2) The arm clears them into the right bins while a screen shows detections. (3) A judge adds an item; change the vocabulary live by publishing to `/target_words`. (4) Show items per minute and watts used by the vision node.
- **Risks and fallbacks:** grasping transparent or crushed items fails → use suction and rigid items (cans, bottles, cartons). Calibration drifts → fixed camera mount and marker re-check script. Arm unavailable → fall back to Concept 1 with a servo flap.
- **Judging angles:** innovation medium; technical depth good (perception-to-action loop, two vendors integrated); impact credible; Leukerbad relevance medium (hotels, clinics and spas produce sortable waste).

### Concept 3 — Resource Patrol: a quadruped that finds litter and wasted energy

- **Problem → value:** litter on paths and wasted heat (open windows, doors left open, lights on in empty rooms) are found late or never. A patrol robot logs them on a map so staff fix what matters first.
- **Hardware:** RDK X5 + camera mounted on a **Unitree Go2** or Genisom quadruped (or any mobile base on site). Optional: SKYLANDX MetaCam scan as the reference map.
- **Architecture / stack:**
  - Perception: YOLO-World for litter classes; `hobot_llamacpp` VLM (SmolVLM2 or InternVL on X5) answering fixed questions such as "is a window open?" on key frames.
  - Planning: waypoint patrol using the robot's own navigation or teleoperation; the X5 tags each finding with the robot pose.
  - Output: map with pins and photos; daily "top 5 fixes" list.
  - Compute: perception on the X5 riding on the robot, powered from a USB-C power bank or the robot's supply.
- **48-hour plan:**
  - H0–6: mount and power the board, get the robot pose into ROS 2, test detection while walking.
  - H6–24: finding logger (class, pose, photo), VLM prompts for two or three energy-waste cases.
  - H24–40: patrol route in the venue, map view, false-positive filtering.
  - H40–48: timed patrol runs, backup video.
- **3-minute demo script:** (1) Robot walks a short loop with planted litter and one open window. (2) Pins appear live on the map. (3) Open a pin: photo, class, VLM explanation. (4) Close with the estimate method for avoided waste (state assumptions openly).
- **Risks and fallbacks:** VLM is slow (sample log shows about 20 tokens/s on X5) → run it only on key frames. Motion blur → stop-and-look behaviour. Outdoor cold and snow → demo indoors, state the −20 to 60 °C board rating and lack of IP protection.
- **Judging angles:** innovation medium to high (energy waste by VLM); technical depth good; impact depends on honest numbers; Leukerbad relevance high (thermal baths, hotels and clinics heat large spaces through winter).

### Concept 4 — Learned sort-and-disassemble skill running fully on-board

- **Problem → value:** circular-economy tasks (removing caps, separating battery from device, sorting deformable packaging) are too varied for scripted picking. A policy learned from demonstrations, running on an efficient edge board instead of a GPU workstation, shows a path to affordable reuse and repair cells.
- **Hardware:** **RDK S100** + two cameras + a teleoperable arm (LeRobot-style arm if D-Robotics brings one, otherwise an on-site vendor arm with a teleop mode). Optional: OriginFlow EMG capture or XREAL glasses for demonstration recording.
- **Architecture / stack:**
  - Data: record 50–100 teleoperated episodes of one short task.
  - Training: LeRobot **ACT** on a laptop or cloud GPU.
  - Deployment: convert and run the policy on the S100 BPU (path documented on the D-Robotics forum); real-time cores can host the motor loop.
  - Perception helper: X5-class detector to choose which item the policy handles next.
- **48-hour plan:**
  - H0–6: confirm with D-Robotics engineers that the ACT-on-S100 path works with the arm you have; set up teleoperation.
  - H6–24: collect data, first training run, start the conversion pipeline in parallel.
  - H24–40: on-board inference, iterate on data where it fails.
  - H40–48: lock one task that works more than half the time; prepare a scripted fallback.
- **3-minute demo script:** (1) Show 20 seconds of teleop data collection. (2) Run the learned policy on-board on a fresh item. (3) Show that no external GPU is connected. (4) Explain how one more task is added with new demonstrations only.
- **Risks and fallbacks:** the highest-risk concept: toolchain conversion, GPU access and arm compatibility can each consume a day → keep Concept 2's scripted pick as the guaranteed demo and present the policy as a stretch result.
- **Judging angles:** innovation high; technical depth highest; impact long-term rather than immediate; Leukerbad relevance low to medium unless tied to a local item (for example ski-rental or spa equipment repair).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| RDK X5 + Dobot CR / Nova or Magician | Low-cost sorting cell; Dobot arms have simple SDKs | Low to medium |
| RDK X5 + Flexiv Rizon or ROKAE xMate (force / torque sensing) | Contact-rich tasks: cap removal, disassembly, pressing items into bins | Medium |
| RDK X5 + Unitree Go2 / Genisom quadruped | Litter and energy-waste patrol with on-board vision | Medium (mount, power, pose bridge) |
| RDK X5 / S100 + Galaxea R1 or Galbot G1 mobile manipulator | Mobile pick-up of litter or sorting at several points | High (these robots already carry their own compute and models) |
| RDK X5 + SKYLANDX MetaCam | 3D site model to place findings and monitoring nodes | Low (offline map) |
| RDK X5 + XREAL glasses | Worker sees sorting hints or the patrol's findings in AR | Medium |
| RDK S100 + WUJI Hand or OriginFlow capture | Dexterous disassembly demonstrations for policy learning | High |
| RDK X5 + Leadshine drives / coprod modules | Custom conveyor or bin-flap mechanism under CAN / PWM control | Medium to high |

## Questions to ask the D-Robotics engineers on site

1. Which boards, cameras and PoE modules did you bring, how many per team, and which RDK OS version is flashed?
2. For YOLO-World on the X5: which words are in the text-feature library, and can we add our own classes during the event?
3. If we fine-tune a YOLO model tonight, who can help with OpenExplorer conversion, and how long does it realistically take?
4. What is the measured power draw of the X5 idle and under BPU load?
5. Which VLM do you recommend on the X5 for yes / no scene questions, and what latency per image should we expect?
6. Do you have a working ROS 2 example that sends detections to any of the arms on site (Dobot, Flexiv, ROKAE)?
7. Is the LeRobot ACT path on the S100 ready to use here, and with which arm?
8. Is the `mono2d_trash_detection` model available converted for the X5?

## Decision rule

- **Pick D-Robotics for T03 if** your idea is perception-led (recognise, count, monitor, guide), you want to argue low-power on-device AI, and you either need no actuator or have already secured another vendor's arm or robot.
- **Avoid if** you want a turnkey robot, need a rugged outdoor unit this weekend, or your waste classes require training and converting a custom model with no D-Robotics engineer available to help.

## Sources

- [D-Robotics official site (EN)](https://en.d-robotics.cc/)
- [RDK X5 product page](https://en.d-robotics.cc/rdkx5)
- [Accessories page](https://en.d-robotics.cc/accessories)
- [Introduction to TogetheROS.Bot](https://developer.d-robotics.cc/tros_doc/en/tros)
- [GitHub: rdk_model_zoo](https://github.com/D-Robotics/rdk_model_zoo)
- [GitHub: hobot_yolo_world](https://github.com/D-Robotics/hobot_yolo_world)
- [GitHub: hobot_llamacpp](https://github.com/D-Robotics/hobot_llamacpp)
- [GitHub: mono2d_trash_detection](https://github.com/D-Robotics/mono2d_trash_detection)
- [CNX Software: RDK X5](https://www.cnx-software.com/2025/06/30/d-robotics-rdk-x5-development-board-features-sunrise-x5-octa-core-soc-with-10-tops-bpu-for-ros-projects/)
- [D-Robotics company profile (S100 specs, LeRobot ACT on S100, on-site guess; see its source list)](../D-Robotics.md)
