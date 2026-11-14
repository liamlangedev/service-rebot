---
type: challenge-playbook
company: "ROKAE Robotics"
slug: ROKAE
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# ROKAE Robotics × T03 — Hackathon Playbook

⬆ [ROKAE Robotics profile](../ROKAE.md) · [Brief](ROKAE-T03-1-Brief.md) · [Products and solutions](ROKAE-T03-2-Products-and-Solutions.md)

**Assumptions to verify in the first hour:** which arm is on site (SR / CR / AR), whether a gripper and camera come with it, which SDK version runs on its controller, and whether a Linux PC with GPU is available. Every concept below assumes **one fixed-base ROKAE arm + your own RGB-D camera + a simple gripper or suction cup + a laptop**.

## Solution approaches

### Concept 1 — "Sort-by-touch" hotel recycling cell (safest)

- **Problem → value:** Leukerbad's hotels, clinics and spa restaurants produce mixed recyclables (PET, aluminium, glass, paper) that are collected as separate fractions in Switzerland. Contamination ruins batches. A desk-sized cell sorts by vision and confirms by touch → cleaner fractions, less staff time.
- **Hardware:** xMate **SR5** or **CR7** (CR7 preferred for IP67 if items are wet) · RGB-D camera above the tray · two-finger or suction gripper · 4 bins · optional D-Robotics RDK X5 for edge inference.
- **Architecture / stack:**
  - Perception: open-vocabulary detector or a small fine-tuned classifier on the laptop / RDK → class + pick point from depth.
  - Planning: top-down grasp, fixed drop poses taught by drag teaching.
  - Control: xCore SDK **Python** motion commands + digital I/O for the gripper. Force step: lower until contact force threshold, squeeze / press and read the force response to separate rigid (glass, can) from soft (PET, carton) when vision is unsure.
  - Compute: laptop; robot controller only executes moves.
- **48-hour plan:**
  - H0–6: get SDK talking to the arm, jog from Python, wire gripper I/O, mount camera, hand-eye calibration.
  - H6–24: detection + pick-and-place loop for 4 classes; teach bin poses; log successes.
  - H24–40: add force "press test", contamination reject bin, dashboard (items sorted, estimated kg CO₂e avoided — state your factor and source).
  - H40–48: tune reliability on 30 real items from the venue, record backup video, rehearse.
- **3-minute demo script:** (0:00) show a real mixed bag from the venue kitchen → (0:30) robot sorts 6–8 items live → (1:30) hand it a tricky item (crushed can vs. foil-lined carton); robot presses, reclassifies → (2:15) dashboard: purity, items/hour, measured arm power draw → (2:40) scaling to hotels and the clinic.
- **Risks and fallbacks:** no gripper supplied → 3D-print a scoop or use a vacuum cup with a hobby pump · force readout not accessible from Python → use the controller's collision / contact detection as a binary touch signal, or drop the touch step · detector weak → restrict to 3 visually distinct classes.
- **Judging angles:** *Innovation* — tactile confirmation, not just vision. *Technical depth* — closed loop of vision + force. *Impact* — measurable purity and energy numbers. *Leukerbad* — hospitality waste in a car-light resort where collection trips are costly.

### Concept 2 — Repair-and-reuse station: compliant disassembly of small e-waste

- **Problem → value:** Small electronics and rental gear (e-bike batteries, ski-rental electronics, hotel devices) are shredded rather than repaired because opening them is manual. A force-controlled arm that unscrews and pries housings open makes reuse and battery recovery cheaper → circular economy.
- **Hardware:** **AR5** (7-DoF) or **SR5** · electric screwdriver or bit tool on the flange · fixture / vice · wrist or overhead camera · optional second arm or WUJI hand to hold the part.
- **Architecture / stack:**
  - Perception: screw-head detection (small model or classical circle detection) → 3D pose from depth.
  - Planning: per-device "disassembly recipe" (ordered screw list); an LLM can generate the recipe from a photo as a stretch goal.
  - Control: approach in position mode, then compliant insertion with low Cartesian stiffness so the bit seats itself; torque / force threshold to detect seated bit and loosened screw. C++ SDK if real-time impedance is needed; Python if the non-real-time force commands suffice.
- **48-hour plan:**
  - H0–6: confirm stiffness / force-control access from the SDK with the ROKAE engineers; build the fixture; pick ONE target device with 4–6 visible screws.
  - H6–24: screw detection + compliant seating + unscrew cycle on one screw type.
  - H24–40: full sequence, lid removal by prying or suction, part sorting into "reuse / recycle / hazardous (battery)".
  - H40–48: reliability runs, second device type if time, video backup.
- **3-minute demo script:** (0:00) the repair-vs-shred problem with one number → (0:30) robot finds and removes screws live, show force trace on screen as the bit seats → (1:45) lid off, battery placed in the safe bin → (2:20) show the recipe file: new device = new recipe, same skills.
- **Risks and fallbacks:** screw seating unreliable → enlarge compliance, use a magnetic bit, or pre-loosen screws and say so · no screwdriver tool → demonstrate prying / snap-fit opening only · lithium cells: use **discharged or dummy cells only** and never pierce.
- **Judging angles:** *Innovation* — force-controlled disassembly is rare at hackathons. *Technical depth* — contact-rich control. *Impact* — right-to-repair and battery recovery. *Leukerbad* — seasonal rental equipment and e-bike fleets.

### Concept 3 — Vertical-farm tender for spa-hotel kitchens

- **Problem → value:** Fresh herbs and greens are trucked up to 1,400 m all winter. A compact indoor rack tended by one arm (seed, inspect, water by need, harvest) cuts transport and water use. ROKAE lists tomato- and grape-harvesting cases, so the arm class is proven for produce handling (details not public).
- **Hardware:** **SR5** / **CR7** in front of a 2–3 shelf rack · RGB-D camera on the wrist · soft gripper or scissors tool · small pump and moisture sensor on a microcontroller · optional XREAL glasses for a grower's status overlay.
- **Architecture / stack:** Perception: plant segmentation + ripeness / health classification per tray → Planning: per-plant action list (water X ml, harvest, skip) → Control: Python SDK moves; gentle contact via low stiffness when gripping stems · Compute: laptop or RDK X5; log water and energy per harvested gram.
- **48-hour plan:** H0–6 rack, plants from a local shop, arm reach check · H6–24 scan routine + watering by measured need · H24–40 harvest motion with compliant grasp, resource dashboard · H40–48 polish and rehearse.
- **3-minute demo script:** scan sweep → robot waters only the two dry pots → harvests one basil stem and drops it into a kitchen box → dashboard compares water and transport against delivered produce (state assumptions).
- **Risks and fallbacks:** cutting tool unsafe or unavailable → pluck whole pots instead of stems · perception of real plants is fiddly → colour-tag pots · impact numbers are estimates → label them as such.
- **Judging angles:** *Innovation* moderate · *Technical depth* moderate · *Impact* clear resource story · *Leukerbad* strong (alpine supply chain, wellness cuisine).

### Concept 4 — Roaming resource butler: mobile collection + sorting (most ambitious)

- **Problem → value:** Collection is the expensive part of recycling in a pedestrian resort. A mobile robot collects from rooms, corridors or spa areas and hands over to the sorting cell — or sorts on board.
- **Hardware:** **Helios** if on site (two AR-class arms, omni base, on-board Jetson). Otherwise: another vendor's quadruped or wheeled base (Unitree Go2, Genisom, AGIBOT D1) carrying a basket, docking to the fixed ROKAE cell from Concept 1.
- **Architecture / stack:** Navigation on the base vendor's stack (or Helios ROS 2) → docking marker (AprilTag) at the cell → ROKAE arm unloads the basket and runs the Concept 1 sorter · task dispatch via a simple web app; optional SKYLANDX scan for the venue map.
- **48-hour plan:** H0–6 two sub-teams: base navigation / docking and arm sorting · H6–24 each works standalone · H24–40 integrate at the docking point · H40–48 end-to-end runs; cut scope to "base arrives, arm unloads 3 items" if unstable.
- **3-minute demo script:** tap "collect room 12" → base fetches a basket → docks → arm unloads and sorts → dashboard shows trips saved.
- **Risks and fallbacks:** two vendors' stacks double the integration risk → keep the interface to one message ("docked") · Helios access unlikely → never plan on it before seeing it · fallback is Concept 1 alone, which still stands as a complete demo.
- **Judging angles:** *Innovation* — system-level, multi-robot. *Technical depth* — high if it works live. *Impact* — collection logistics. *Leukerbad* — car-light village, steep streets (indoor demo only).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| ROKAE arm + **D-Robotics RDK X5** | Low-power on-edge perception; strong "watts per sorted item" story | Low–medium (camera + inference on RDK, results over network to the SDK host) |
| ROKAE arm + **WUJI Hand** | Dexterous handling of irregular waste or delicate disassembly | Medium–high (mounting, power, separate hand SDK) |
| ROKAE arm + **Unitree / Genisom / AGIBOT quadruped** | Mobile collection feeding a fixed sorting cell | Medium (only a docking handshake between stacks) |
| ROKAE arm + **SKYLANDX MetaCam** | Fast 3D model of the workspace or venue for planning and the pitch | Low (offline scan) |
| ROKAE arm + **Galbot / Galaxea / Spirit AI models** | Learned grasping instead of heuristics | High — model portability to a ROKAE arm is ⚠️ unverified; ask first |
| ROKAE arm + **OriginFlow EMG** or **XREAL** | Teleoperated demonstration capture or operator overlay for exception handling | Medium–high |
| ROKAE **HSA joints** + **coprod** / **Leadshine** | Custom low-cost mechanism (for example a bin-lid opener) | High for 48 hours; only with vendor help |

## Questions to ask the ROKAE Robotics engineers on site

1. Which exact models are here (SR3 / SR5 / CR7 / AR5 / Helios), how many, and do they come with a gripper, a camera and a mounting plate?
2. Which xCore SDK version matches the controllers on site, and can we get the package and examples offline right now?
3. From **Python**, can we read tool force / joint torque and set Cartesian stiffness, or is that C++ real-time only? What is the real-time rate?
4. Is there a working ROS 2 package for these units — which distro, with MoveIt config and URDF?
5. How do we drive a gripper: controller digital I/O, tool-flange I/O / RS485, or our own USB device?
6. What are the safe speed and force limits you want us to keep with people around the table, and how do we recover from a protective stop without you?
7. Can you share measured power draw (idle vs. moving) for the arm, or lend a power meter?
8. For the CR35 parcel-sorting and fruit-picking cases: which vision and grasp planning was used, and is any of it reusable here?

## Decision rule

- **Pick ROKAE Robotics for T03 if** your idea is a fixed-cell, contact-aware manipulation task (sorting, disassembly, produce handling) and you can supply perception, a gripper and compute yourself — and you confirmed in hour one that the SDK exposes what you need.
- **Avoid if** your idea needs mobility, outdoor or snow operation, environmental sensing, or a ready-made AI model — choose a quadruped, mobile-manipulator or VLA vendor and use ROKAE at most as the arm.

## Sources

- [ROKAE — SR cobots product page](https://www.rokae.com/en/product/show/349/SR-Cobots.html)
- [ROKAE — xMate CR product page](https://www.rokae.com/en/product/show/545/xMateCR.html)
- [ROKAE — Humanoid Force-Controlled Arm AR](https://www.rokae.com/en/product/show/595/Humanoid-Force-Controlled-Arm-AR.html)
- [ROKAE — Wheeled Dual-Arm Robot Helios](https://www.rokae.com/en/product/show/596/Wheeled-Dual-Arm-Robot-Helios.html)
- [ROKAE case — CR35 warehouse picking and sorting](https://www.rokae.com/en/case/show/2629/CR35-Advances-Large-Scale-Warehouse-Picking-&-Sorting.html)
- [ROKAE case — embodied intelligence in smart warehousing (JD Logistics, AR5)](https://www.rokae.com/en/case/show/2630/Embodied-Intelligence-in-Action:-Advancing-the-Future-of-Smart-Warehousin.html)
- [ROKAE — Commercial Services cases (fruit picking)](https://www.rokae.com/en/case/208/Commercial-Services.html)
- [ROKAE — General Industry cases (battery, sorting, catalyst)](https://www.rokae.com/en/case/343/General-Industry.html)
- [ROKAE SDK documentation index](https://docs.rokae.com/en/docs/SDK)
- [ROKAE ROS 2 package manual](https://docs.rokae.com/en/docs/ROS2)
- [ROKAE Robotics company profile (this vault)](../ROKAE.md)
