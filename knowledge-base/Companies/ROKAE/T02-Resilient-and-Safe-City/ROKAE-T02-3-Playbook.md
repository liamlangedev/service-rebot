---
type: challenge-playbook
company: "ROKAE Robotics"
slug: ROKAE
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# ROKAE Robotics × T02 — Hackathon Playbook

⬆ [ROKAE Robotics profile](../ROKAE.md) · [Brief](ROKAE-T02-1-Brief.md) · [Products and solutions](ROKAE-T02-2-Products-and-Solutions.md)

> **Read first:** fit is **2/5**. ROKAE gives you a force-controlled arm and an open SDK, not a resilience system. Every concept below uses the arm as the "hand that touches infrastructure" and gets mobility, mapping or operator interface elsewhere. Which ROKAE units are on site is **not confirmed** — settle that in the first 30 minutes.

## Solution approaches

### Concept 1 — Remote hands for a cut-off plant room (safest)

- **Problem → value:** when a road is closed by avalanche, rockfall or flood, nobody can reach a pump room, switch cabinet or cable-car drive room. A pre-installed arm lets an operator turn a valve, reset a breaker or press a stop button from far away, with contact force capped so nothing gets broken.
- **Hardware:** one fixed-base **xMate SR3 / SR5 or CR7**; any gripper available (ask ROKAE; otherwise Flexiv Grav or a 3D-printed valve key / finger); USB or depth camera; mock panel with a quarter-turn valve, rocker switch, e-stop button and a gauge. Operator input: gamepad or SpaceMouse; optional XREAL glasses for the camera view.
- **Architecture / stack:** camera → operator view (plus optional gauge reading with a small vision model) → teleop node maps input to Cartesian velocity targets → **xCore SDK real-time Cartesian impedance** (C++, up to 1 kHz) on a Linux PC wired to the controller. Force estimates from the arm drive a contact-force bar in the UI. Simple path if real-time mode is unavailable: non-real-time `MoveL` jog steps plus SDK force-control commands from Python.
- **48-hour plan:**
  - **H0–6:** confirm arm, controller version (**v3.2.1+** needed for SDK 0.7.1), gripper; run SDK example; jog from code; build the mock panel.
  - **H6–24:** teleop loop with impedance; camera stream; force display; pre-taught "macros" (approach valve, approach switch) recorded by drag teaching.
  - **H24–40:** latency and network-drop handling (watchdog → hold position); gauge reading; operator UI; rehearse.
  - **H40–48:** freeze code, record backup video, polish pitch.
- **3-minute demo script:** (0:00) "The road is closed, the pump room is flooding." (0:30) Operator, not looking at the arm, reads the gauge through the camera. (1:00) Triggers the "approach valve" macro, then closes the valve by hand control; force bar stays under the limit. (1:45) Flips the breaker, presses the stop button. (2:15) Pull the network cable: arm holds safely, resumes on reconnect. (2:40) Cost and deployment story.
- **Risks and fallbacks:** no real-time licence or mode → non-real-time jog. No gripper → printed tool fixed to the flange. Laggy video → macros do the approach, human only confirms.
- **Judging angles:** *Innovation* modest; *technical depth* in impedance teleop and fail-safe behaviour; *impact* clear for utilities; *Leukerbad relevance* strong — a mountain village with a single access road and thermal-water and cable-car plant rooms.

### Concept 2 — Force-controlled tap-test inspector

- **Problem → value:** hammer sounding (tapping and listening for hollow sounds) is still a standard manual check for concrete linings and bonded surfaces. A force-controlled arm can tap with repeatable energy and log results as a map, making inspections comparable over time.
- **Hardware:** **xMate SR5 or CR7 / CR12**; a small tapper (solenoid or spring hammer) and a contact microphone on the flange; test wall made of tiles or concrete slabs with hidden voids. Optional: SKYLANDX MetaCam scan of the test wall; D-Robotics RDK for on-edge audio classification.
- **Architecture / stack:** scan or hand-taught surface → grid of tap points → MoveIt 2 (`rokae_ros2`, Humble) or SDK `MoveL` for approach → impedance / force-guarded contact to find the surface → tap → audio features (spectral centroid, decay) → simple classifier (solid vs hollow) → heat map overlaid on a photo or point cloud. Compute on a laptop.
- **48-hour plan:**
  - **H0–6:** arm motion from code; build the tapper and test wall; record first audio.
  - **H6–24:** force-guarded touch-and-tap routine; collect labelled taps; train classifier.
  - **H24–40:** automatic grid scan; heat map; repeatability check; optional 3D overlay.
  - **H40–48:** blind test on a panel the team did not label; backup video.
- **3-minute demo script:** (0:00) Show a wall that looks intact. (0:30) Arm scans a 5 × 5 grid, tapping gently. (1:45) Heat map appears, red zone marked. (2:15) Open the panel to reveal the void. (2:40) Where it goes next: gallery, tunnel and retaining-wall checks from a vehicle or a mobile base.
- **Risks and fallbacks:** audio too noisy in the hall → use an accelerometer on the tapper or reduce to two clearly different materials. No scan → hand-taught plane. Classifier weak → show raw spectrograms side by side.
- **Judging angles:** *Innovation* good (contact sensing, not another camera demo); *technical depth* in force control plus signal processing; *impact* in ageing-infrastructure maintenance; *Leukerbad relevance* via road galleries, tunnels and retaining structures on alpine access routes.

### Concept 3 — Mobile first responder: go there and operate it

- **Problem → value:** after an incident, someone must enter a possibly unsafe building to shut off gas or water or open a door. A mobile base with a compliant arm does the first entry.
- **Hardware:** option A — **Helios** if on site (indoor, flat floors). Option B — **AR5** (10 kg, 48 V DC) or **SR3** mounted on another vendor's base (Unitree B2 / Go2, AGIBOT D1, Genisom M1 / L1, or a wheeled base). SKYLANDX MetaCam for the map; XREAL for the operator.
- **Architecture / stack:** base navigation from the base vendor's stack (or Helios ROS 2) → operator selects target → base parks → arm under impedance teleop or a scripted valve-turn → status back to operator. Compute: base computer for navigation, laptop or Jetson for arm control and video.
- **48-hour plan:**
  - **H0–6:** go / no-go on mounting: payload, 48 V supply, controller size, e-stop chain. If no-go by H6, switch to Concept 1.
  - **H6–24:** mechanical mount and power; arm control from the base computer; base teleop.
  - **H24–40:** combined mission in a mock corridor: drive, park, operate valve; map display.
  - **H40–48:** rehearse the single mission; backup video.
- **3-minute demo script:** (0:00) Alarm: gas smell in the utility corridor. (0:30) Robot drives in; map and video build up. (1:30) Parks at the valve; arm closes it with force shown. (2:20) Drives out; incident log displayed.
- **Risks and fallbacks:** mounting or power not feasible in time (highest risk); Helios absent; two SDKs to integrate. Fallback: base and arm as two cooperating robots — base scouts and maps, fixed arm operates the panel.
- **Judging angles:** *Innovation* and *impact* high; *technical depth* in cross-vendor integration; *Leukerbad relevance* for hotel, spa and clinic technical areas during an evacuation.

### Concept 4 — Click-to-act in a digital twin (most ambitious)

- **Problem → value:** teleoperating every centimetre is slow and needs a skilled operator. Let the operator click a valve or switch in a 3D twin; the robot plans and executes the contact itself and asks for help only when force readings look wrong.
- **Hardware:** xMate SR / CR arm (or AR on a base); depth camera; SKYLANDX MetaCam scan; XREAL glasses or a laptop viewer.
- **Architecture / stack:** scan → point cloud registered to the robot frame → operator click → open-vocabulary detector or VLM labels the object and chooses a skill (turn, push, pull) → MoveIt 2 plans a collision-free approach using the scan → skill runs under Cartesian impedance with force thresholds → anomaly (force too high, no motion) hands control back to manual teleop from Concept 1.
- **48-hour plan:**
  - **H0–6:** Concept 1 basics working; scan the mock panel; camera-to-robot calibration.
  - **H6–24:** three hand-written skills with force guards; MoveIt planning scene from the scan.
  - **H24–40:** click interface; detector / VLM for skill choice; hand-back to manual.
  - **H40–48:** limit to the two most reliable skills; backup video.
- **3-minute demo script:** (0:00) Show the twin of the plant room. (0:30) Click the valve → robot closes it. (1:15) Click the breaker → robot flips it. (1:45) Jammed valve: force limit reached, system asks the operator, who takes over. (2:30) Scaling story: one operator supervising many sites.
- **Risks and fallbacks:** calibration errors, planning failures, VLM latency. Fallback: fixed, pre-registered targets with the same UI; drop the VLM and use buttons.
- **Judging angles:** *Innovation* and *technical depth* highest; *impact* in operator productivity; *Leukerbad relevance* same as Concept 1 with a stronger "one operator for the whole valley" story.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| ROKAE arm (fixed) + XREAL glasses | Head-up camera view and status for the remote operator | Low — video stream and overlay only |
| ROKAE arm + SKYLANDX MetaCam | 3D scan as MoveIt planning scene and as the twin for click-to-act or heat maps | Medium — one-off registration of scan to robot frame |
| ROKAE arm + WUJI Hand or Flexiv Grav gripper | Real grasping of handles, plugs and tools | Medium — mechanical adapter, separate hand SDK |
| ROKAE AR5 / SR3 on Unitree, AGIBOT D1 or Genisom quadruped | Mobile manipulation beyond flat floors | High — mount, 48 V power, controller placement, e-stop, two SDKs |
| Quadruped scout (any vendor) + fixed ROKAE arm | Scout maps and finds the fault; arm acts at the panel — no mechanical coupling | Low to medium — shared map and messaging only |
| ROKAE arm + D-Robotics RDK X5 / S100 | On-edge gauge reading, audio or vision classification near the arm | Low to medium |
| ROKAE arm + OriginFlow EMG capture | Operator arm motion or gesture as teleop input | Medium to high — mapping and filtering, novelty value |
| Helios + Binabik AI or coprod stack | Higher-level task agent on a mobile dual-arm robot | High — depends on what each party exposes on site |

## Questions to ask the ROKAE Robotics engineers on site

1. Which models are here, with which controller and xCore version (is it **v3.2.1 or later**), and how many units can one team book?
2. Is real-time mode enabled on these units? Which modes work (Cartesian impedance, direct torque), and is it reachable from Python or only C++?
3. What grippers, tool flanges, tool IO (RS-485) and camera mounts are available to borrow?
4. How do we read estimated external force / torque at the tool through the SDK, at what rate, and can collision thresholds be set from code?
5. What happens when the control PC or network drops during real-time control — hold, brake, error state — and how do we recover from code?
6. For an AR arm on a third-party base: which controller is needed, its size, mass, power draw and whether it runs from a 48 V battery?
7. If Helios is here: what is exposed over ROS 2 (navigation goals, map, arm control, teleop), and what are its slope and threshold limits?
8. Does `rokae_ros2` run the Gazebo simulation without a robot, and is there a URDF for the exact models on site?

## Decision rule

- **Pick ROKAE Robotics for T02 if** your idea is about *touching* infrastructure — remote valve or switch operation, contact inspection, force-guarded intervention — and you are happy with a fixed-base arm or have a confirmed mobile base to pair it with.
- **Avoid if** your idea needs to move through terrain, snow or rubble, patrol or map large areas, or you want a vendor with existing emergency-response references; choose a quadruped or scanning vendor as the lead and add ROKAE only as the arm.

## Sources
- [ROKAE — xMate CR series](https://www.rokae.com/en/product/show/545/xMateCR.html)
- [ROKAE — SR cobots](https://www.rokae.com/en/product/show/349/SR-Cobots.html)
- [ROKAE — Humanoid Force-Controlled Arm AR](https://www.rokae.com/en/product/show/595/Humanoid-Force-Controlled-Arm-AR.html)
- [ROKAE — Wheeled Dual-Arm Robot Helios](https://www.rokae.com/en/product/show/596/Wheeled-Dual-Arm-Robot-Helios.html)
- [ROKAE — Mobile Manipulator CMR](https://www.rokae.com/en/product/show/599/Mobile-Manipulator-CMR.html)
- [ROKAE SDK documentation](https://docs.rokae.com/en/docs/SDK)
- [GitHub — RokaeRobot/xCoreSDK-CPP](https://github.com/RokaeRobot/xCoreSDK-CPP)
- [GitHub — RokaeRobot/rokae_ros2](https://github.com/RokaeRobot/rokae_ros2)
- [GitHub — RokaeRobot organization](https://github.com/RokaeRobot)
- [ROKAE company profile (this pack)](../ROKAE.md)
