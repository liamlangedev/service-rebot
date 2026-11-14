---
type: challenge-playbook
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Omnicor AI × T03 — Hackathon Playbook

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Brief](Omnicor-AI-T03-1-Brief.md) · [Products and solutions](Omnicor-AI-T03-2-Products-and-Solutions.md)

**Fit 2/5 — supporting role.** Omnicor AI has no robot and no public SDK, specs or docs. Every concept below uses another vendor's hardware and treats Omnicor as the on-device inference layer. **Each concept is designed to still work without Omnicor** (fallback compute named), so a "no" from their engineers does not sink the project. All Omnicor capabilities are ⚠️ unverified until confirmed on site.

**The one idea that makes Omnicor relevant to T03:** measure and cut **energy per decision** (joules per sorted item, per patrol, per answer) and show the number live.

## Solution approaches

### Concept 1 — Joule-metered waste-sorting station (safest)

- **Problem → value:** Mixed waste in hotels and clinics lowers recycling quality. A small sorting cell that classifies and separates items, running entirely on a low-power edge box, shows automation that does not add a data-centre footprint.
- **Hardware:** fixed RGB camera, one small arm (Dobot Magician or CR cobot; alternatives ROKAE xMate, Flexiv Rizon), bins, wall-plug power meter. Compute: **OC Node** if available; otherwise a D-Robotics RDK board, a Jetson-class board or a laptop.
- **Architecture / stack:** perception = small detector (YOLO-class, fine-tuned on TACO / TrashNet plus 100–200 photos of local items) → planning = class-to-bin lookup and fixed pick poses → control = the arm vendor's own SDK. Omnicor's part: optimise the detector for the target box and report latency and watts. Energy logging: wall-plug meter plus CodeCarbon or the board's own power readout.
- **48-hour plan:**
  - H0–6: confirm arm, camera and compute; collect local item photos; record baseline power of the unoptimised model.
  - H6–24: train the detector; hand-eye calibration; first pick-and-drop cycle; give the model to Omnicor for porting.
  - H24–40: swap in the optimised model; build the dashboard (items sorted, accuracy, joules per item, baseline vs optimised).
  - H40–48: tune reliability on 5–6 item types; rehearse; record a backup video.
- **3-minute demo script:** (0:00) the problem in one sentence, with a real bag of hotel waste. (0:30) judges drop items; the arm sorts them. (1:30) switch the dashboard between baseline and optimised model: same accuracy, fewer joules. (2:15) unplug the network cable — it keeps working. (2:40) scale-up arithmetic for one hotel, stated as an estimate.
- **Risks and fallbacks:** Omnicor cannot port in time → export the model to ONNX / TensorRT yourself and keep the energy comparison. Grasping fails on odd shapes → restrict to rigid items or use a suction tool. Savings look small → report them honestly and lead with offline operation.
- **Judging angles:** innovation — modest; technical depth — a measured energy claim, which is rare at hackathons; impact — recycling quality; Leukerbad — hotels, spas and clinics produce sorted-waste streams daily.

### Concept 2 — Offline energy-waste patrol for spa and hotel buildings

- **Problem → value:** Thermal resorts lose heat through tilted windows, propped doors and lights left on in unused rooms. A robot on a night round spots these and logs them for staff, with all inference on-board.
- **Hardware:** Unitree Go2 (or another quadruped / wheeled base on site) with its RGB camera; optional thermal camera only if one is available (not confirmed). Compute: OC Node or the robot's own computer.
- **Architecture / stack:** perception = detector for open window, open door, light on, radiator → planning = waypoint patrol with the robot vendor's navigation; findings list with location → interface = a local LLM (Apertus or Qwen, quantised) turns the log into a short staff report in German / French / English. Omnicor's part: run detector and LLM together inside the robot's power budget.
- **48-hour plan:**
  - H0–6: get permission for a corridor; teleoperate a round and record video; define 4 detection classes.
  - H6–24: label and train; waypoint patrol working; LLM running locally on a laptop.
  - H24–40: move both models on-board; findings map; report generation.
  - H40–48: full rounds, battery-per-round measurement, backup video.
- **3-minute demo script:** (0:00) one photo of a tilted window above a radiator. (0:20) robot walks a short loop past staged faults. (1:30) the findings list appears; ask the LLM "what should the night porter fix first?" (2:15) show compute watts on-board vs a GPU laptop. (2:40) estimated savings, clearly labelled as estimate.
- **Risks and fallbacks:** navigation takes too long → teleoperate the round and keep detection autonomous. Detector unreliable → reduce to two classes (window, light). On-board port fails → run on a laptop carried alongside and say so.
- **Judging angles:** innovation — monitoring instead of manipulation; depth — two models sharing one edge budget; impact — heating is a major cost for thermal resorts; Leukerbad — very direct.

### Concept 3 — On-board VLA litter and recyclables collector

- **Problem → value:** Litter on promenades and around thermal baths is collected by hand. A mobile manipulator that picks and pre-sorts recyclables, with the policy running on the robot, removes both the tether and the cloud dependency.
- **Hardware:** Galbot G1 or AGIBOT G1 / G2 (both vendors appear as Omnicor customers on its site, scope not public); alternative Galaxea R1. Compute: on-board, via Omnicor deployment or OC Node.
- **Architecture / stack:** perception + control = a VLA or imitation policy (ACT / SmolVLA trained with LeRobot on 50–100 teleoperated demos; or the vendor's own model such as GraspVLA or GO-1) → planning = simple state machine (find, approach, pick, drop in the right bin) → Omnicor's part: fit the policy on-board and hold a usable control rate. Compare energy and latency against the same policy served from a GPU workstation (OpenVLA ships a REST server script that suits this baseline).
- **48-hour plan:**
  - H0–6: confirm with Omnicor **which robot and which model already run together**; choose the policy accordingly; set up teleoperation.
  - H6–24: record demos for 3 object types (can, PET bottle, paper cup); train; first closed-loop picks off-board.
  - H24–40: on-board deployment; state machine; energy logging.
  - H40–48: success-rate runs, video, pitch.
- **3-minute demo script:** (0:00) scatter three item types. (0:20) robot picks and bins them, untethered. (1:40) side-by-side: off-board GPU vs on-board, watts and control rate. (2:20) success rate over N trials, read out honestly. (2:40) what a season of promenade cleaning would need.
- **Risks and fallbacks:** policy training does not converge → scripted grasp from a detector, keep the on-board story. Robot access limited → move the task to a fixed arm (becomes Concept 1). On-board rate too low → smaller policy, or state the gap as the finding.
- **Judging angles:** innovation — medium; depth — high (learned policy, on-board deployment, measured trade-off); impact — labour and litter; Leukerbad — tourist promenades, snow-free season.

### Concept 4 — Energy-aware model switching (most ambitious)

- **Problem → value:** Robots run their largest model all the time. Switching between small, medium and large model variants according to battery level and task difficulty extends runtime per charge and cuts charging cycles.
- **Hardware:** any battery robot from Concepts 2 or 3; OC Node or on-board computer.
- **Architecture / stack:** Omnicor's tooling produces **several variants** of one model for the same chip (if OC Agent can do this — ask) → a supervisor reads battery state and detector confidence and selects the variant → log energy per task for fixed-large vs adaptive.
- **48-hour plan:**
  - H0–6: confirm variant generation is possible; define the task and the switching rule.
  - H6–24: get two variants running; build the supervisor.
  - H24–40: paired runs, fixed vs adaptive; dashboard.
  - H40–48: polish and pitch.
- **3-minute demo script:** (0:00) the claim. (0:30) robot performs the task while the dashboard shows the active variant changing. (1:45) bar chart: tasks per charge, fixed vs adaptive. (2:30) how this generalises to a fleet.
- **Risks and fallbacks:** only one variant available → switch between two different open models. Gains masked by motor energy → use a compute-dominated task (static perception) and say so.
- **Judging angles:** innovation — highest of the four; depth — systems-level; impact — indirect but fleet-wide; Leukerbad — cold reduces battery capacity, so runtime matters in alpine winter.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Omnicor + Dobot (Magician / CR) | Concept 1 sorting cell with on-device vision | Low — arm SDK is independent of the inference box |
| Omnicor + D-Robotics RDK | Side-by-side edge boards, or RDK as fallback compute | Low to medium |
| Omnicor + Unitree Go2 | Concept 2 patrol with on-board detection and local LLM | Medium — power and mounting for an extra box |
| Omnicor + Galbot G1 | Concept 3; customer logo suggests prior integration (scope not public) | Medium to high — depends on what already runs |
| Omnicor + AGIBOT G1 / G2 | Concept 3 with GO-1 or a LeRobot policy | Medium to high — same caveat |
| Omnicor + SKYLANDX MetaCam | 3D scan of a building as the map for patrol findings | Medium — offline map only, not live SLAM on the robot |
| Omnicor + XREAL glasses | Staff see energy-waste findings in AR | Medium — adds a second interface to build |

## Questions to ask the Omnicor AI engineers on site

1. What hardware did you bring — OC Node units? How many, which chip, what power draw, which interfaces and supply voltage?
2. Which robots here already run an Omnicor deployment, and with which model (Galbot? AGIBOT?)?
3. If we give you a fine-tuned detector or an ACT / SmolVLA policy tonight, when do we get it back running on-device — hours or days?
4. Can we use OC Agent ourselves, or do you operate it? Can it output several size variants of one model?
5. Do you have measured before / after numbers (watts, latency, accuracy) for any model we could reproduce live?
6. How do we call the deployed model — ROS 2 node, HTTP / gRPC, Python binding?
7. Can the box report its own power draw, or do we need an external meter?
8. Can a local LLM (Apertus, Mistral, Qwen) and a vision model run at the same time on one unit?

## Decision rule

- **Pick Omnicor AI for T03 if** the engineers confirm at kickoff that they have hardware on site and can port your model within a day, and your pitch is built around a **measured** low-power, cloud-free result on another vendor's robot or arm.
- **Avoid if** you need a single-vendor platform with documentation, your model already runs comfortably on a laptop and energy is not your story, or you get no clear commitment on turnaround in the first hours.

## Sources

- [OmniCor AI official website](https://www.omnicorai.io/)
- [OpenVLA (GitHub)](https://github.com/openvla/openvla)
- [LeRobot (GitHub)](https://github.com/huggingface/lerobot)
- [Apertus-8B-Instruct-2509 model card (Hugging Face)](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
- [Ultralytics YOLO (GitHub)](https://github.com/ultralytics/ultralytics)
- [TACO dataset (GitHub)](https://github.com/pedropro/TACO)
- [TrashNet dataset (GitHub)](https://github.com/garythung/trashnet)
- [CodeCarbon (GitHub)](https://github.com/mlco2/codecarbon)
