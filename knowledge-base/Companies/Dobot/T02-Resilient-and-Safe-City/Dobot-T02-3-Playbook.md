---
type: challenge-playbook
company: "Dobot Robotics"
slug: Dobot
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Dobot Robotics × T02 — Hackathon Playbook

⬆ [Dobot Robotics profile](../Dobot.md) · [Brief](Dobot-T02-1-Brief.md) · [Products and solutions](Dobot-T02-2-Products-and-Solutions.md)

> **Fit 2/5.** Dobot gives you a reliable arm and a simple API, not a safety solution. Every concept below uses the arm as the **"hands"** of a resilience system. Concepts 1–2 work with Dobot kit alone; 3–4 need another vendor or less certain hardware.
> **First 15 minutes:** confirm at the Dobot booth which arms, grippers and cameras are available and that controller firmware is **V4.4.0.0 or above** (required by the Python V4 SDK).

## Solution approaches

### Concept 1 — Plant-room inspector that also acts (safest)

- **Problem → value:** Small utilities (thermal-water pumps, heating, cable-car drive rooms) rely on a person walking past panels. During storms or road closures nobody can get there. An arm with a camera reads gauges and indicator lamps on a schedule, flags anomalies, and performs a first response — press reset, flip a breaker, close a small valve.
- **Hardware:** Magician E6 or CR3A / CR5A / Nova 2 on a table; USB or RealSense camera on the wrist; simple gripper or 3D-printed finger; a mock panel (analogue gauge, LEDs, toggle switch, quarter-turn valve). Optional: D-Robotics RDK for on-robot inference.
- **Architecture / stack:**
  - Perception: wrist camera → gauge reading (classical needle detection or an open VLM) + lamp-state classification.
  - Planning: a fixed inspection tour of taught poses; a small rule engine or LLM turns readings into "OK / warn / act".
  - Control: `TCP-IP-Python-V4` — `MovJ` / `MovL` between poses taught by drag (`StartDrag`), `ToolDO` for the gripper, `SetCollisionLevel` for safe contact.
  - Compute: one laptop; dashboard in a browser showing readings, images and action log.
- **48-hour plan:**
  - H0–6: connect to the arm, teach 6–8 poses, build the mock panel, get camera frames.
  - H6–24: gauge and lamp reading working; inspection loop end to end; first actuation (toggle switch).
  - H24–40: anomaly → action logic, dashboard, alert message, valve turn; repeatability testing (50 loops).
  - H40–48: polish the story, record a backup video, rehearse.
- **3-minute demo script:** (0:00) the scenario — access road closed, nobody on site. (0:30) robot runs its tour; dashboard fills with readings. (1:15) a judge turns up the "pressure"; the robot detects it on the next pass, raises an alert and closes the valve. (2:15) show the action log and what a remote operator sees. (2:40) scaling: one arm on a rail or a mobile base per plant room.
- **Risks and fallbacks:** gauge reading unreliable under glare → add a ring light, or use fiducial-framed crops. Valve needs too much torque for E6 (750 g payload) → use a lever or low-friction mock valve, or a CR / Nova arm. VLM too slow → classical vision for gauges, VLM only for the summary.
- **Judging angles:** innovation — modest (inspect-and-act rather than inspect-only). Technical depth — closed loop from perception to physical action. Impact — retrofit for legacy analogue panels without replacing equipment. Leukerbad — thermal-water and lift infrastructure in a valley that can be cut off.

### Concept 2 — Remote hands with click-to-act teleoperation

- **Problem → value:** After a gas leak, flood or fire alarm, someone must operate equipment in a place people should not enter. Give the operator a camera view and let them **click the target** ("this breaker", "this valve"); the arm executes the motion with collision limits. Supervised autonomy tolerates poor network links better than joystick control.
- **Hardware:** CR5A or Nova 5 (reach 850–900 mm) with a depth camera (RealSense); gripper. If an **X-Trainer** is on site, add direct leader–follower mode for fine work. Optional: XREAL glasses as the operator display; OriginFlow EMG as an alternative input.
- **Architecture / stack:**
  - Perception: RGB-D → clicked pixel to 3D point (hand–eye calibration); open-vocabulary segmentation to snap to the object.
  - Planning: skill library (press, flip, grasp-and-turn, pick-and-place) parameterised by the 3D target; MoveIt (ROS 2 Humble package) for collision-aware paths, or straight `MovL` approaches for speed.
  - Control: `MovJ` / `MovL` for skills; `ServoP` streaming for manual jog mode; low `SetCollisionLevel` threshold as the contact guard. Force commands (`FC*`) only if a CRAF arm is available.
  - Compute: laptop next to the robot; operator UI on a second machine over Wi-Fi with injected latency to prove robustness.
- **48-hour plan:**
  - H0–6: arm + camera running; hand–eye calibration; click → move-above-point working.
  - H6–24: three skills (press, flip, turn); web UI with video and click targets; operator on a separate machine.
  - H24–40: latency and drop-out tests; add confirmation step and e-stop; optional X-Trainer direct mode; task board with 4–5 "hazard zone" tasks.
  - H40–48: timed runs, backup video, pitch.
- **3-minute demo script:** (0:00) "The room is unsafe. The operator is 2 km away." (0:20) operator — ideally a judge — clicks the emergency shut-off; the arm presses it. (1:00) clicks the valve; the arm grasps and turns. (1:40) pull the network cable for five seconds: the arm finishes the current skill safely and waits. (2:20) show the metrics: tasks per minute at 0 / 500 / 2,000 ms latency.
- **Risks and fallbacks:** calibration drift → re-calibrate with a fiducial at start-up. MoveIt integration eats time → skip it; use taught safe approach poses. ROS feedback is only 10 Hz → read the real-time port from Python instead. Streaming-servo behaviour unknown → keep manual mode as slow `MoveJog`.
- **Judging angles:** innovation — shared autonomy designed for bad links. Technical depth — calibration, skill library, latency evaluation. Impact — keeps responders out of danger. Leukerbad — mountain sites with thin connectivity and long travel times.

### Concept 3 — Mobile responder: Dobot arm on a partner base

- **Problem → value:** The inspector or remote hands must reach several places — along a tunnel, through a building, across a plant. Mount the arm on a mobile base that patrols, maps and stops at each point of interest to inspect and act.
- **Hardware:** **Nova 2** (11 kg arm, 1.3 kg controller, 30–60 V DC, 100 W typical / 250 W max) on a Unitree or Genisom quadruped or another vendor's wheeled base — **only if the base's payload and DC supply allow it; confirm with both vendors**. Simpler: Dobot's own **E6 ROS Mobile Platform** if one is on site (indoor, 2 LiDARs, ±5 cm navigation). Optional: SKYLANDX MetaCam scan as the prior map / digital twin.
- **Architecture / stack:**
  - Perception: base LiDAR SLAM for navigation; wrist camera for the task (reuse Concept 1 or 2).
  - Planning: waypoint mission ("go to cabinet A, inspect, act if needed"); the base and arm coordinate through ROS 2 or a simple state machine over sockets.
  - Control: the base's own SDK for locomotion; Dobot V4 Python API for the arm; arm parked and braked while moving.
  - Compute: base on-board computer or a strapped-on mini PC / RDK board; operator laptop for supervision.
- **48-hour plan:**
  - H0–6: decide the base; mechanical mount and power check (**go / no-go by H6**); arm task running on a bench in parallel.
  - H6–24: base navigation between two stations; arm task from the mounted position; stowed-pose transitions.
  - H24–40: full mission; re-localise at each station with a fiducial to absorb navigation error; mission dashboard.
  - H40–48: reliability runs, backup video, pitch.
- **3-minute demo script:** (0:00) map of the "facility" with two alarm points. (0:20) robot drives to station A, reads the gauge: normal. (1:10) drives to station B, finds the fault, closes the valve. (2:10) show the mission log pinned on the 3D map. (2:40) what changes for real deployment.
- **Risks and fallbacks:** mount or power not feasible → fall back to E6 ROS Mobile Platform, or put the arm on a cart and push it ("mobility simulated"), keeping Concept 1 / 2 intact. Base tips or struggles with the arm extended → restrict to a compact work envelope. Two-vendor integration slips → run the base and arm as two demos linked by a shared mission UI.
- **Judging angles:** innovation — cross-vendor mobile manipulation. Technical depth — navigation + manipulation + power integration. Impact — one robot covers many sites. Leukerbad — tunnels, galleries and lift stations spread over steep terrain (the base supplies the terrain capability, not Dobot).

### Concept 4 — Learned emergency skills from teleoperated demos (most ambitious)

- **Problem → value:** Many emergency tasks are contact-rich and vary each time: plugging in a backup power connector, coupling a hose, opening a latched cabinet. Record a few dozen teleoperated demonstrations and train a policy so the robot can do it without an operator when links are down.
- **Hardware:** **X-Trainer** (2 × Nova 2, leader handles) — required; cameras as supplied. Alternative: Atom Max with VR / MR teleoperation if Dobot offers real access. Optional: WUJI hand for dexterous grasps (integration effort high).
- **Architecture / stack:**
  - Data: `dobot_xtrainer` for teleoperation and recording (25 Hz interface).
  - Learning: an open imitation-learning implementation (for example ACT or diffusion policy) trained on a GPU laptop or cloud. Which formats and policies Dobot's tooling supports is **not documented** ⚠️ unverified — ask before choosing.
  - Control: policy outputs joint targets to the followers; a watchdog with collision limits and a human takeover button.
  - Compute: GPU for training (needed overnight), laptop for inference.
- **48-hour plan:**
  - H0–6: X-Trainer running; pick **one** task; fix camera positions; record 10 test episodes and verify replay.
  - H6–24: record 50–100 demonstrations; start training overnight.
  - H24–40: evaluate, collect corrective demos, retrain; add takeover and success detection.
  - H40–48: measure success rate over 20 trials; backup video; pitch.
- **3-minute demo script:** (0:00) operator teleoperates the task once — "this is how it is done today". (0:45) hands off; the policy performs it autonomously. (1:45) perturb the object position; the policy adapts. (2:20) show the success rate and the number of demos it took.
- **Risks and fallbacks:** no X-Trainer on site → concept is off; switch to Concept 2. Policy success too low → present teleoperation as the product and the policy as an assist with operator takeover. No GPU → reduce to a single short-horizon skill.
- **Judging angles:** innovation — highest of the four. Technical depth — full data → training → deployment loop. Impact — skills that keep working when the operator link fails. Leukerbad — weakest direct link; anchor it to a concrete local task (backup power hook-up at a lift station or clinic).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Dobot Nova 2 + Unitree or Genisom quadruped | Legged inspect-and-act robot for stairs and rough floors | **High** — mount, payload margin, DC power, two SDKs; verify feasibility first |
| Dobot arm + SKYLANDX MetaCam | 3D scan of the site as a digital twin; inspection results and actions pinned to it | Low–medium — offline scan, shared coordinate frame via fiducials |
| Dobot arm + XREAL glasses | Operator sees the robot camera and overlays, hands-free, for teleoperation | Medium — video stream and UI on Android XR |
| Dobot arm + D-Robotics RDK board | On-robot vision inference without a laptop | Low–medium — camera pipeline on the board, socket to the arm |
| Dobot arm + OriginFlow EMG capture | Muscle-signal input for teleoperation or demonstration capture | Medium–high — signal mapping is research-grade |
| Dobot arm + WUJI Hand | Dexterous manipulation of handles, connectors, knobs | High — mechanical adapter, separate hand control |
| Dobot arm + Binabik AI or coprod stack | Agentic task layer or modular hardware interface over the Dobot API | Unknown — ask those teams whether a Dobot driver exists |
| Dobot E6 ROS Mobile Platform alone | Indoor patrol + light manipulation with one vendor | Low — if a unit is on site |

For force-controlled contact tasks without add-ons, Flexiv Rizon or ROKAE xMate (joint torque sensing) are the more natural arms; pick Dobot when ease of programming matters more than force control.

## Questions to ask the Dobot Robotics engineers on site

1. Which arms are here, how many, and which firmware — is every controller on **V4.4.0.0 or above**?
2. Which grippers and cameras come with them, and is there a wrist-mount plate for a RealSense?
3. Is an **X-Trainer** available to teams, and which training pipeline (data format, policy type) does it support out of the box?
4. Is an **E6 ROS Mobile Platform** here? Which ROS version and navigation stack does it ship with?
5. What cycle time do `ServoJ` / `ServoP` expect, and what is the update period of the real-time feedback port (30004)?
6. Has a Nova arm been run from a mobile robot's battery before — recommended voltage, peak current, and a controller enclosure for IP20?
7. Is a **CRAF** (force-sensor) or **CRA-IP68** unit on site? If not, what is the safest way to do contact tasks on a standard arm (collision level, speed limits)?
8. Can teams get hands-on time with Atom / Atom Max VR teleoperation, or is it demo-only?

## Decision rule

- **Pick Dobot Robotics for T02 if** your idea is a stationary or base-mounted "inspect-and-act" or remote-hands system, you want an arm working within the first hours via a simple Python API, and you have (or can borrow from another vendor) the mobility and sensing that make it a city-resilience story.
- **Avoid if** your concept needs the robot to move through terrain, work outdoors in cold or wet conditions, map hazards, or do force-controlled contact without extra sensors — choose a quadruped, mapping or force-controlled-arm vendor as the lead instead and use Dobot, at most, as the manipulator.

## Sources

- [Dobot Nova series](https://www.dobot-robots.com/products/nova-series/dobot-nova-series.html)
- [Dobot CRA series](https://www.dobot-robots.com/products/cra-series/dobot-cra-series.html)
- [Dobot CRA-IP68 series](https://www.dobot-robots.com/products/cra-series/dobot-cra-ip68-series.html)
- [Dobot CRAF series](https://www.dobot-robots.com/products/cra-series/dobot-craf-series.html)
- [Dobot E6 ROS Mobile Platform](https://www.dobot-robots.com/products/education/ros-mobile-platform.html)
- [Dobot X-Trainer](https://www.dobot-robots.com/products/humanoid-robots/x-trainer.html)
- [Dobot Atom](https://www.dobot-robots.com/products/humanoid-robots/atom.html)
- [GitHub: TCP-IP-Python-V4](https://github.com/Dobot-Arm/TCP-IP-Python-V4)
- [GitHub: DOBOT_6Axis_ROS2_V4](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V4)
- [GitHub: dobot_xtrainer](https://github.com/Dobot-Arm/dobot_xtrainer)
- [Dobot Robotics company profile (this vault)](../Dobot.md)
