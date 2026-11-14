---
type: challenge-playbook
company: "coprod Inc."
slug: coprod
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# coprod Inc. × T01 — Hackathon Playbook

⬆ [coprod Inc. profile](../coprod.md) · [Brief](coprod-T01-1-Brief.md) · [Products and solutions](coprod-T01-2-Products-and-Solutions.md)

**Read first:** coprod gives you controlled axes, power and an IMU — not a robot and not autonomy. Every concept below uses coprod for a **custom mechanism** and gets mobility and navigation from somewhere else. Before committing, confirm at the booth: how many axes and motors you can have, and that the `cosystem` SDK runs on your laptop. The four concepts are our proposals, not coprod reference designs.

## Solution approaches

### Concept 1 — Secure delivery hatch on a carrier robot (safest)
- **Problem → value:** hotels, clinics and pharmacies in a car-light resort need small items moved door to door; a locked compartment that opens only for the right recipient turns any mobile robot into a delivery service.
- **Hardware:** 1 × co:motion + motor (hatch axis), co:power, co:battery, a 3D-printed or laser-cut box. Carrier: a quadruped or wheeled robot from another vendor (Unitree Go2 / B2, AGIBOT D1 — check payload and mounting in their profiles).
- **Architecture / stack:** carrier robot's own SDK handles walking / driving and navigation → a small task script (laptop or mini-PC on the payload) decides "arrived, recipient verified" (QR code or PIN on a phone web page) → `cosystem` Python commands the hatch in position mode with a low torque limit so it cannot pinch. Power telemetry feeds a simple status page.
- **48-hour plan:**
  - H0–6: get one axis moving from Python; confirm carrier payload and mounting; sketch the box.
  - H6–24: build the box, open / close routine, torque-based obstruction stop, recipient check.
  - H24–40: mount on the carrier, run the route A → B (teleoperated first, then waypoint-based if the carrier supports it).
  - H40–48: rehearse, film a backup video, build the status page.
- **3-minute demo script:** load a parcel at "pharmacy" → robot walks to "hotel reception" → wrong QR code: hatch stays shut → right QR code: hatch opens → a hand blocks the lid: it stops and reverses → dashboard shows battery and delivery log.
- **Risks and fallbacks:** no SDK access in time → drive the hatch with any hobby servo and keep coprod for telemetry only (or drop coprod). Carrier cannot take the weight → put the box on a hand cart and demo the mechanism plus logic.
- **Judging angles:** modest innovation; solid real-world impact; technical depth comes from torque-limited safe closing; Leukerbad relevance: spa-hotel and clinic deliveries on pedestrian streets.

### Concept 2 — Self-levelling cargo tray for steep streets
- **Problem → value:** Leukerbad is steep; open loads (meals, drinks, lab samples, flowers) spill on slopes and stairs. An actively levelled tray lets a legged or wheeled carrier deliver liquids.
- **Hardware:** 2 × actuated axes (co:act if available, otherwise co:motion + motors) in a pitch / roll gimbal, 1 × co:sense on the tray, co:power, co:battery. Carrier from another vendor as in Concept 1.
- **Architecture / stack:** co:sense fused orientation (1 kHz) → levelling controller in Python (start with a simple PD on roll / pitch) → position or torque commands to the two axes over EtherCAT. No perception needed; the carrier handles locomotion. Compute: one real-time Linux host on the payload.
- **48-hour plan:**
  - H0–6: confirm two axes + IMU available; read orientation and move both axes from one script.
  - H6–24: build the gimbal; close the levelling loop on the bench (tilt it by hand).
  - H24–40: mount on the carrier; tune on a ramp and stairs; log tilt error.
  - H40–48: side-by-side comparison run (levelling on / off) and backup video.
- **3-minute demo script:** glass of water on the tray → carrier climbs a ramp with levelling off (spill) → same run with levelling on (dry) → live plot of carrier tilt vs tray tilt → close with the delivery use case.
- **Risks and fallbacks:** only one axis available → level pitch only (the slope direction). Loop rate from Python too slow → ask coprod whether the loop can run in the C++ core. Carrier vibration → add foam, lower gains.
- **Judging angles:** clear visual result; technical depth in closed-loop control at 1 kHz bus rate; uses coprod's real strength (deterministic sensing + actuation); Leukerbad relevance is direct (gradient, stairs, snow-roughened paths).

### Concept 3 — Swappable service-tool port (one robot, several city jobs)
- **Problem → value:** a small municipality cannot afford one robot per task. A standard powered tool port lets the same carrier deliver in the morning and grit an icy footpath or sweep in the evening.
- **Hardware:** co:power + co:battery as the port; 2 tools, each with its own co:motion axis — e.g. the delivery hatch from Concept 1 and a small rotary grit / salt spreader or sweeping brush. Carrier from another vendor.
- **Architecture / stack:** on tool change, the script re-scans the bus (`cs.scan_network()`), identifies which tool is attached by its device IDs and loads the matching behaviour → velocity control for the spreader / brush, position control for the hatch → motor torque read-back as a cheap "brush jammed / hopper empty" signal (confirm torque feedback is exposed). Task layer and carrier navigation as in Concept 1.
- **48-hour plan:**
  - H0–6: confirm at least 2 axes; test hot or cold re-scan behaviour with coprod staff.
  - H6–24: build tool A (hatch) and tool B (spreader or brush); common mechanical latch and connector.
  - H24–40: auto-detect logic, per-tool behaviours, mount on the carrier.
  - H40–48: timed tool-swap rehearsal and backup video.
- **3-minute demo script:** deliver a parcel → swap tool in under 30 seconds → system announces "spreader detected" → robot grits a marked "icy" strip → dashboard shows energy used per job.
- **Risks and fallbacks:** live re-plugging of EtherCAT may need a restart — demo with a clean restart between tools. Second tool not finished → present Concept 1 plus the port design.
- **Judging angles:** strongest innovation story; matches coprod's interoperability thesis, so their engineers will likely engage; real-world impact for small towns; Leukerbad relevance: winter path maintenance plus tourist-season deliveries.

### Concept 4 — Custom four-wheel service cart (most ambitious)
- **Problem → value:** a purpose-built low cart for indoor / arcade routes (hotel corridors, thermal-bath complexes) that carries towels, luggage or waste bins.
- **Hardware:** 4 × co:motion + wheel motors (this mirrors the wheel group in coprod's own API sample), co:sense, co:power, co:battery, a self-built chassis. Navigation compute and sensors from other vendors: D-Robotics RDK X5 with a camera / LiDAR; SKYLANDX MetaCam for a prior map.
- **Architecture / stack:** LiDAR / camera → open-source ROS 2 mapping and navigation on the RDK → velocity command → a thin Python bridge node that turns it into wheel velocities via `cosystem` (write it yourself; a ready ROS 2 bridge is ⚠️ unverified) → co:motion velocity loops. Wheel odometry + co:sense heading go back up for localisation.
- **48-hour plan:**
  - H0–6: **go / no-go** — do 4 axes, 4 suitable motors and wheels actually exist on site? If not, switch to Concept 1 or 2.
  - H6–24: chassis, wiring, teleoperated driving, odometry.
  - H24–40: bridge node, mapping of the demo area, waypoint navigation.
  - H40–48: one reliable A → B route, e-stop demo, backup video.
- **3-minute demo script:** call the cart from a phone → it drives a mapped corridor to the pick-up point → load → it returns → press the e-stop to show controlled braking → show the map and telemetry.
- **Risks and fallbacks:** highest risk of all four — mechanics, real-time host setup and navigation in 48 hours. Fallbacks: teleoperation or line following instead of full navigation; two driven wheels plus casters instead of four.
- **Judging angles:** highest technical depth; innovation is low (carts exist) unless the modular build is the story; honest answer to "why not use a finished robot?" is needed.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| coprod + Unitree (Go2 / B2) | Legged carrier for hatch or levelling tray on slopes and stairs | Medium — mechanical mount + two separate software stacks talking over the network |
| coprod + AGIBOT (D1) | Same as above with a different quadruped | Medium |
| coprod + D-Robotics (RDK X5) | Perception / navigation compute above coprod's motor layer | Medium–high — confirm whether the EtherCAT master can run on the RDK or needs a separate real-time PC |
| coprod + SKYLANDX (MetaCam) | Pre-scanned 3D map of the demo route for the carrier or cart | Low for a map as a visual; high for live localisation |
| coprod + Leadshine | Frameless motors / joint modules for co:motion to drive | High — electrical and encoder compatibility must be confirmed by both booths |
| coprod + Galaxea / Galbot wheeled manipulators | Add a coprod-driven locker or tray to a robot that can also hand over items | Medium–high — payload mounting and power on a third-party base |

## Questions to ask the coprod Inc. engineers on site

1. How many co:motion axes, motors, co:sense, co:power and co:battery units can one team get, and for how long?
2. How do we get the `cosystem` SDK today, and which host OS, kernel and network card does the EtherCAT master need? Can it run on an ARM board such as the D-Robotics RDK?
3. Is there a ROS 2 bridge now, or should we wrap the Python API ourselves?
4. Which motors and encoders are already tested with co:motion, and what are the current and voltage limits per axis?
5. Do you have a wheel-base example matching the API sample on your home page (four-wheel velocity group)?
6. What battery capacity and voltage are on site, and what runtime should we expect with two to four axes?
7. Can torque be read back per axis from Python, and at what rate can a Python loop realistically close?
8. What happens on e-stop and on unplugging a module from the bus — can the network be re-scanned without a restart?

## Decision rule

- **Pick coprod Inc. for T01 if** your idea hinges on a custom actuated mechanism (hatch, levelling tray, tool port) on top of someone else's mobile robot, your team has mechatronics and Linux skills, and coprod confirms kits and SDK access in the first hour.
- **Avoid if** you need a robot that navigates on day 1, cannot verify hardware availability at kickoff, or your concept's value is in autonomy and perception rather than in a mechanism.

## Sources
- [coprod — official site (home, API sample, system specs)](https://coprod.co/)
- [coprod — products](https://coprod.co/products.html)
- [coprod — systems](https://coprod.co/systems.html)
- [coprod — community](https://coprod.co/community.html)
- [coprod Inc. profile (general research)](../coprod.md)
