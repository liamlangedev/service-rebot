---
type: dev-guide
company: "coprod Inc."
slug: coprod
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# coprod Inc. — Developer Guide (hackathon edition)

⬆ [coprod Inc. profile](coprod.md) · [Product portfolio](coprod-Products.md) · [Roadmap and strategy](coprod-Roadmap-and-Strategy.md)

> **Read this first.** coprod sells robot **building blocks**, not a robot. There is **no public SDK download, no docs portal and no ROS 2 package** as of 2026-11-14. Everything you need to program the hardware has to come from the coprod team on site (or their Discord). Decide in the first 15 minutes whether they can hand you a working kit — if not, build on another vendor.
>
> Research note: this guide is based on direct reads of coprod's own site, its GitHub organisation, the simulator bundle, Venture Kick and startup.ch. General web search was not available for this pass, so third-party forum posts and videos were not checked.

## TL;DR — how you program it

- **One Python package, `cosystem`** (C++ core, Python bindings): scan the EtherCAT bus, get a handle per device, set a mode, write targets, read telemetry. 🧪 Preview only — not on PyPI, not on GitHub.
- **Low-level and joint-centric.** You command **torque, velocity or position per axis** and tune gains yourself. There is no navigation, manipulation, skill or behaviour layer.
- **Hard real time over EtherCAT:** **1 kHz** typical loop, **< 20 µs** jitter, distributed clocks, on a **real-time Linux** host that you (or coprod) supply.
- **Simulation = one browser demo.** The co:dodo simulator (MuJoCo in WebAssembly, **200 Hz** physics, **50 Hz** ONNX policy) runs with no install, but there is no published URDF / MJCF / USD and no training repo.
- **AI stack = none.** No pretrained manipulation policy, VLA, dataset or teleop pipeline. Bring your own brain (laptop, another vendor's robot, or a D-Robotics RDK board) and use coprod as the actuation layer.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| **cosystem API** 🧪 | Python (bindings) on a C++ core | All co:system devices: co:motion / co:act axes, co:sense IMU, co:power regulators, logging | [Home-page code sample](https://coprod.co/) | Only a ~15-line sample is public. `pip install cosystem` does **not** work (PyPI returned 404 on 2026-11-14). Get the package from the team. |
| C++ API 🧪 | C++ | Same as above, without the Python layer | not public | Existence stated ("C++ core"); no headers or examples published |
| ROS 2 interface | — | — | not public | Mentioned only in the startup.ch listing. ⚠️ unverified as existing code |
| Docs portal | — | — | not public | `coprod.co/docs/` returns 404. Blog is empty. |
| GitHub org **coprod-Inc** ✅ | C / C++ / Python | Supporting code only — no SDK | [github.com/coprod-Inc](https://github.com/coprod-Inc) | **9 public repos.** The website footer still links to `github.com/coprod-llc`, which is **404** — use `coprod-Inc`. |
| ↳ `SOES` (fork) | C | Open-source EtherCAT **slave** stack | [repo](https://github.com/coprod-Inc/SOES) | Last pushed 9 Nov 2026 — active firmware work |
| ↳ `modm` (fork) | C++ | Embedded HAL / library generator for ARM Cortex-M | [repo](https://github.com/coprod-Inc/modm) | Last pushed 11 Nov 2026 |
| ↳ `FreeRTOS-Cpp`, `tinycrypt` (forks) | C++ / C | RTOS wrapper, small crypto library | [org](https://github.com/coprod-Inc) | Firmware dependencies |
| ↳ `rsl_rl` (fork) | Python | GPU reinforcement-learning library (legged locomotion) | [repo](https://github.com/coprod-Inc/rsl_rl) | Last pushed Sep 2025 |
| ↳ `lerobot` (fork) | Python | Hugging Face LeRobot | [repo](https://github.com/coprod-Inc/lerobot) | Fork only; coprod-specific changes ⚠️ unverified |
| ↳ `kicad_project_manager` | Python | KiCad 9 / 10 plugin (PCB project templates, design rules) | [repo](https://github.com/coprod-Inc/kicad_project_manager) | MIT, v1.1.0. Useful for PCB designers, irrelevant for a 48 h build |
| co:dodo simulator ✅ | Browser (JS + WASM) | Simulated biped only | [coprod.co/simulator](https://coprod.co/simulator/) | Not an SDK — a playable demo |

**Inference from the forks (not stated by coprod):** device firmware is most likely built on modm + FreeRTOS + SOES on ARM microcontrollers, and co:dodo's walking policy was most likely trained with rsl_rl-style PPO. The public org contains **no** `cosystem` source, **no** robot description files and **no** examples.

## Control levels

| Level | Available? | What you get | Rate |
|---|---|---|---|
| High-level motion (walk, navigate, grasp, skills) | ❌ none | Nothing published. co:dodo walking runs coprod's own in-house policy, not an API you call | — |
| Joint-level targets | 🧪 via `cosystem` | Per-axis **position** (`.angle`), **velocity** (`control_vel([...])` on a controller group), gain setting (`.kp`), mode switch (`MotionMode.VELOCITY`) — all taken from the public sample | 1 kHz typical bus cycle |
| Torque control | 🧪 claimed | Site states simultaneous torque / velocity / position control on co:motion and co:act. The torque-command call is **not shown** in the sample — ask for it | 1 kHz+ |
| Sensor / power telemetry | 🧪 via `cosystem` | IMU orientation (`imu.euler`; module outputs quaternion, accel, gyro, mag), regulator voltage (`cs.power.get_regulator(id=0).voltage`) | IMU fusion at 1 kHz on-module |
| Firmware level | not public | No firmware source, no flashing tool published | — |

- **Editions / licences:** there is no EDU vs. standard split and no licence key mentioned anywhere. Low-level access is the *only* access. What you can do is limited by **which preview build the team gives you**, not by a paywall.
- **Python and real time:** the deterministic 1 kHz loop lives in the C++ / real-time layer. Whether your Python code runs *inside* that loop or just updates set-points asynchronously is **not documented** — ask before you write a Python torque loop.
- **Group vs. single axis:** the sample shows both single-device handles (`get_slave`) and grouped controllers (`motion.get_controllers`) with vector commands. Device IDs come from a project-specific `SlaveId` enum, so someone must define the bus layout first.

## ROS 2 and middleware

- **ROS 2:** no package, no message definitions, no `ros2_control` hardware interface published. The only mention is one line in the startup.ch company listing. Treat as **not available** unless the team shows you code. ⚠️ unverified
- **Native middleware is EtherCAT**, not DDS. The stack is: developer API → real-time control loop → EtherCAT master → devices (100 Mb/s, distributed clocks, hardware time-stamping).
- **Which EtherCAT master** (SOEM, IgH, EtherLab, custom) is used on the host: not public. The slave side appears to use SOES (inferred from the fork).
- **Practical bridge for a hackathon:** write a thin Python node yourself — subscribe to `cmd_vel` / joint targets from your own stack, call `cosystem`, publish IMU and joint state back. Budget **2–3 hours**, assuming the API behaves like the sample.
- **Mixing with other vendors:** run coprod on its own wired EtherCAT segment and talk to the other robot over your normal network (ROS 2 / UDP / HTTP). Do not expect any shared-bus integration.

## Simulation and digital twins

| Asset | Status | Detail |
|---|---|---|
| co:dodo browser simulator | ✅ | [coprod.co/simulator](https://coprod.co/simulator/). MuJoCo compiled to WebAssembly; **physics 200 Hz**, **control 50 Hz**; ONNX policy (encoder + actor); **6 DoF** — hip abduction, hip flexion, knee per leg (joint names `LHAA`, `LHFE`, `LKFE`, `RHAA`, `RHFE`, `RKFE`); observation shown as 30 × 10. Runs fully client-side. |
| Controls | ✅ | Keyboard: `W/A/S/D` or arrows to walk and turn, `Q/E` strafe, `C` chase camera, `B` spawn a ball. Gamepad and touch also supported. Velocity-command interface (forward, lateral, yaw). |
| URDF / MJCF / USD download | ❌ not public | The simulator loads an MJCF internally, but coprod publishes no robot-description repo and no licence for the model. Ask the team if you want it. |
| ONNX policy files | ⚠️ no licence stated | The web app fetches its policy files from the site. They are reachable, but nothing grants reuse rights — ask before using them outside the demo. |
| Isaac Lab / Isaac Sim / Gazebo assets | ❌ not public | None found |
| Training code / RL environment | ❌ not public | Only an unmodified-looking `rsl_rl` fork is visible |
| Simulation models of co:act / co:motion (actuator model, friction, torque-speed curve) | ❌ not public | Needed for serious sim-to-real; ask |

- coprod claims the simulator runs "the same trained policies" as the real robot. This is the only sim-to-real evidence published; no numbers, no paper.
- **Use for a hackathon:** the simulator is a fast way to *show* a biped in a pitch. It is not a development environment — you cannot load your own policy or scene through any documented interface.

## AI stack

| Item | Status |
|---|---|
| Pretrained manipulation / navigation policies | ❌ none |
| VLA / foundation model | ❌ none |
| Locomotion policy | co:dodo walking policy exists (ONNX, runs at 50 Hz in the browser sim and, per coprod, on the robot). Not released as a product. |
| Datasets | ❌ none |
| Teleoperation / data collection | ❌ none today. A dual-arm teleop platform with tactile end effectors is 🔭 planned, no date |
| LeRobot support | No official integration. The org holds a **fork of `huggingface/lerobot`**, which signals interest; whether it contains a co:system robot driver is ⚠️ unverified |
| On-device inference | Not addressed. Policies run on your host computer |

**What this means:** all perception and decision-making is yours. Good pairings on site: a laptop with a camera; a **D-Robotics RDK** board for edge vision; a VLA-capable robot from another vendor doing the "smart" part while a co:system axis does one custom motion.

## Compute, sensors and connectivity

| Topic | What is public | What to ask |
|---|---|---|
| Host computer | "Real-time Linux" running the EtherCAT master. No reference PC, no supported-OS list | Do they bring a pre-configured host? Which distro / kernel (PREEMPT_RT)? x86 or ARM? |
| Connecting a laptop | Not documented. EtherCAT masters in general need a **dedicated wired Ethernet port** with raw-socket (root) access — Wi-Fi and most USB-C docks are a risk. This is general EtherCAT practice, not a coprod statement | Can a stock Ubuntu laptop be the master? Does macOS / Windows / WSL work? (Assume **no** until shown.) |
| Network defaults | None published. EtherCAT does not use IP addresses for devices; nodes are found by `cs.scan_network()` | How are `SlaveId` values assigned — by bus position or configured alias? |
| Topology | Daisy-chain today. Junction modules for star / branch wiring are 🔭 planned | Cable type and connector; maximum nodes tested |
| Sensors | **co:sense**: 9-axis dual-redundant IMU, on-board fusion at 1 kHz, outputs quaternion / accel / gyro / mag. Encoders via co:motion (BiSS, SSI, SPI, Hall, incremental). **No cameras, LiDAR, force-torque or tactile** (tactile is 🔭 planned) | Which motors and encoders are pre-paired with the co:motion boards on site? |
| Power | **co:power**: **10–54.6 V** input, submodules for power logic / e-stop, precharge, isolated DC/DC, brake chopper; telemetry on the bus. **co:battery**: protected packs, capacity not public | Bench supply or battery? Voltage of the kit? Is the brake chopper fitted? |
| Actuators | **co:act** 🧪 coming soon: 10 Nm continuous / 25 Nm peak, 16:1, 60 mm, 420 g | Are any physically here? Otherwise: which third-party motors? |

## First 60 minutes checklist

Because nothing is downloadable, the checklist starts with people, not software.

1. **(0–10 min) Go to the coprod table and ask five questions:** How many axes can one team have? Is there a ready wheel base, arm or single-joint rig? Do you supply the host PC? Is the Python package installable on my laptop? Is there a ROS 2 bridge today? If two or more answers are "no", **stop here and pick another vendor** — keep coprod only as an add-on axis.
2. **(10–15 min) Join the Discord** via the button on [coprod.co/community](https://coprod.co/community.html) and ask for the SDK build, an example script and a wiring diagram in writing.
3. **(10–20 min, in parallel) Open the [simulator](https://coprod.co/simulator/)** on a second laptop. Walk co:dodo with `W/A/S/D`. This is your zero-risk demo asset.
4. **(15–25 min) Get the host ready.** Preferably use coprod's own pre-configured real-time Linux machine. If you must use your laptop: wired Ethernet port free, root access, package installed from the team's wheel / archive.
5. **(25–30 min) Power up safely.** Axis clamped to the table, nothing attached to the output, e-stop within reach, supply voltage confirmed with the team. Check the co:battery charge LEDs or the bench-supply current limit.
6. **(30–35 min) Verify the bus.** Run a scan and confirm every expected device appears. Pattern from the public sample (names may differ in the build you receive):
   ```python
   import cosystem as cs
   cs.scan_network()                      # discover EtherCAT devices
   imu = cs.get_slave(SlaveId.IMU)        # SlaveId enum is defined per project
   print(imu.euler)                       # tilt the board: values must change
   print(cs.power.get_regulator(id=0).voltage)
   ```
7. **(35–45 min) Hello-world motion on ONE axis, low gain.**
   ```python
   m = cs.get_slave(SlaveId.CAMERA_MOTOR) # single axis handle
   m.kp = 10.0                            # start low; value from the sample, not a recommendation
   m.angle = 3.14159 / 4                  # position target (rad)
   ```
   Then try velocity mode on a group: set `mode = cs.motion.MotionMode.VELOCITY` and call `control_vel([...])`.
8. **(45–50 min) Read back state.** Ask how to read joint position, velocity, torque / current and fault flags — these calls are **not in the public sample**. Log them at a known rate.
9. **(50–55 min) Test the stop path.** Trigger the e-stop once on purpose, observe the controlled braking, and learn the recovery sequence (how to clear the fault and re-enable).
10. **(55–60 min) Go / no-go.** You should have: bus scan OK, one axis moving, IMU and voltage reading, e-stop tested. If not, fall back to another vendor's robot and keep coprod as a stretch goal.

## Known gotchas and safety

- **Pre-order hardware, preview software.** co:motion, co:power, co:sense and co:battery are listed as pre-order; co:act is "coming soon". Expect prototype-grade firmware and API changes.
- **No Safe Torque Off yet.** co:motion offers *controlled braking* on emergency stop; a certified-style STO module is "coming". Do not treat the e-stop as a safety-rated function — add a physical power cut-off you control.
- **No safety certification of any kind is published** (no CE marking statement, no ISO 13849 / ISO 10218 / medical claims). For **T04**, never attach a co:system joint to a person's limb in a demo without a mechanical range limit, a low torque cap and a hand on the power switch. Demonstrate on a dummy limb.
- **25 Nm peak on a 60 mm actuator is enough to injure fingers.** Clamp everything; keep the first tests at low gain and low current.
- **Regenerative energy:** fast deceleration pushes energy back into the supply. Without the co:power brake-chopper submodule a bench supply may trip or over-volt. Ask which submodules are fitted.
- **Battery details unknown.** Chemistry, capacity and charge procedure are not public. Do not charge packs unattended; follow the team's instructions and the venue's battery rules.
- **Host requirements can kill your schedule.** If the master needs a PREEMPT_RT kernel or a specific NIC, a personal laptop may not work at all. Confirm before planning.
- **Dead links and locked shop.** Site GitHub link is 404 (real org: `coprod-Inc`); `shop.coprod.co` is password-protected; `docs` does not exist. Do not waste time hunting online.
- **Sample ≠ contract.** The only public API is a marketing snippet. Method names, units (radians assumed) and enum names may differ in the real build.
- **No bundled perception or autonomy.** Any team that needs mapping, vision or grasping must bring it from elsewhere.
- **Bus factor.** A three-founder company is your only support channel. If they are busy with another team, you are blocked — pair with them early.

## Community resources

| Resource | Link | Use |
|---|---|---|
| Discord ("co:builder" community) | Join button on [coprod.co/community](https://coprod.co/community.html) | Main support channel; site promises help "within hours". Described as opening with a first hand-picked cohort |
| Email | contact@coprod.ch | SDK access, kit requests, co:found applications |
| GitHub | [github.com/coprod-Inc](https://github.com/coprod-Inc) | Firmware-dependency forks, KiCad plugin. No SDK |
| YouTube | [youtube.com/@coprod-LLC](https://youtube.com/@coprod-LLC) | co:dodo film (content not reviewed for this guide) |
| LinkedIn / X / Instagram | [LinkedIn](https://www.linkedin.com/company/coprod-llc) · [X](https://x.com/coprod_Inc) | Announcements |
| co:ambassador / co:campus | [Community page](https://coprod.co/community.html) | Early hardware access for campus representatives, clubs and Formula Student teams |
| co:found | [coprod.co/cofound.html](https://coprod.co/cofound.html) | **75% off** the first CHF 25,000, then **33% off** up to CHF 100,000, if your hackathon project becomes a start-up |
| Forum / Stack Overflow / third-party tutorials | none found | — |

## Sources

- [coprod — home page (API sample, stack diagram, system numbers)](https://coprod.co/)
- [coprod — products](https://coprod.co/products.html)
- [coprod — systems (co:dodo, planned systems)](https://coprod.co/systems.html)
- [coprod — co:dodo simulator](https://coprod.co/simulator/)
- [coprod — community](https://coprod.co/community.html)
- [coprod — jobs (role descriptions mention API, tooling, simulation)](https://coprod.co/jobs.html)
- [coprod — co:found](https://coprod.co/cofound.html)
- [coprod — blog (empty)](https://coprod.co/blog/)
- [GitHub — coprod-Inc organisation](https://github.com/coprod-Inc)
- [GitHub — coprod-Inc/SOES](https://github.com/coprod-Inc/SOES)
- [GitHub — coprod-Inc/modm](https://github.com/coprod-Inc/modm)
- [GitHub — coprod-Inc/rsl_rl](https://github.com/coprod-Inc/rsl_rl)
- [GitHub — coprod-Inc/lerobot](https://github.com/coprod-Inc/lerobot)
- [GitHub — coprod-Inc/kicad_project_manager](https://github.com/coprod-Inc/kicad_project_manager)
- [startup.ch — coprod listing](https://www.startup.ch/coprod)
- [Venture Kick — coprod receives CHF 40,000 (2 Apr 2026)](https://www.venturekick.ch/coprod-receives-CHF-40000-from-Venture-Kick-to-build-scalable-interoperable-robotics-ecosystem)
