---
type: dev-guide
company: "SKYLANDX"
slug: SKYLANDX
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# SKYLANDX — Developer Guide (hackathon edition)

⬆ [SKYLANDX profile](SKYLANDX.md) · [Product portfolio](SKYLANDX-Products.md) · [Roadmap and strategy](SKYLANDX-Roadmap-and-Strategy.md)

> SKYLANDX is a **sensor + software vendor, not a robot vendor**. The headings below are adapted: "programming it" means getting pose, maps and 3D data out of a MetaCam scanner or C01 LiDAR and into your own stack.
> **Research limit (2026-11-14):** no public SDK, docs portal or GitHub org exists to read. Everything here comes from official product pages and the official PDF brochures. Anything about ports, topic names, message types or rates is **not public** — get it from SKYLANDX staff on site.

## TL;DR — how you program it

- **There is nothing to `pip install`.** No public SDK, API reference, ROS package or GitHub org. Your first task is to ask SKYLANDX staff for the API / Rosbridge document and a unit with the interface enabled.
- **Live path (robot integration):** the scanner exposes a **WebSocket interface that speaks the Rosbridge protocol** — point clouds, images, IMU and pose, no custom driver. Supported ROS versions, topics and message types: not public.
- **Offline path (always works, no API needed):** scan → process in MetaCam Studio (Windows) or MetaCam Cloud (browser) → export **LAS / PCD / PLY / RCP / E57** point cloud, **OBJ** mesh, **PLY** 3DGS, **JPEG** panoramas → load into your own tools. Plan around this path; treat the live path as a bonus.
- **C01 LiDAR = raw sensor:** UDP point packets + 200 Hz IMU, 12–30 V. You bring the SLAM (advertised as plug-and-play with mainstream open-source algorithms). No public driver or packet spec.
- **It never moves a robot.** Output is pose, map and (optionally) navigation commands; another vendor's robot does the motion. Scanning itself is one button; the engineering is in what you do with the data.

## SDKs and interfaces

| SDK / interface | Language | What it gives you | Link | Notes |
|---|---|---|---|---|
| Rosbridge-protocol WebSocket (MetaCam) | Any WebSocket + JSON client (e.g. roslibpy, roslibjs — generic third-party clients, not vendor tools) | Live point clouds, images, IMU, pose estimates | [Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/) | ✅ documented as existing. IP, port, topic names, message types, rates: **not public** |
| "Open APIs" (MetaCam) | Not public | Real-time pose, map generation, raw sensor streams; optional navigation-command output | [Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/) | Access tier matters — see Control levels |
| MetaCam Pro "Open API" | Not public | Raw data access, custom workflows with third-party software | [MetaCam Pro](https://skylandx.com/metacam-pro/) | One line on the product page; no reference |
| Modular Perception Kit APIs | Not public | Raw images / LiDAR / IMU / RTK plus "commercial-grade SLAM, navigation APIs, post-processing tools" | [Spatial perception robots](https://skylandx.com/spatial-intelligence-robots/) | Sold via sales; no model names or docs |
| C01 LiDAR data stream | UDP (parser language is yours) | Point cloud at **10 Hz typical, up to 30 Hz**; 6-axis IMU at **200 Hz** | [C01 LiDAR](https://skylandx.com/c01-slam-lidar/) · [brochure PDF](https://skylandx.com/wp-content/uploads/EN_C01_LiDAR_BROCHURE.pdf) | Packet format, default IP / ports, time-sync method: not public. No official ROS driver found |
| MetaCam Go | iOS / Android app | Start / stop scan, live colorized point cloud, coverage check, device status, loop-closure notices, cloud upload | [Software platforms](https://skylandx.com/software-platforms/) | The operator UI; not scriptable as far as published |
| MetaCam Studio | **Windows** desktop app | Optimization, editing, measurement, RTK / control-point calibration, merge of sessions, coordinate conversion, export | [Software platforms](https://skylandx.com/software-platforms/) | No CLI or scripting API published. Licence terms not public |
| MetaCam Cloud (also "Skyland Cloud") | Web | Cloud processing, **3DGS generation**, browser viewer, sharing | [Software platforms](https://skylandx.com/software-platforms/) | "Integration with third-party systems" is claimed; no public API. Access is by demo request |
| File exports | Any | Point cloud **LAS / PCD / PLY / RCP / E57** · 3DGS **PLY** · mesh **OBJ** · images **JPEG** | [Air 2 brochure PDF](https://skylandx.com/wp-content/uploads/MetaCam_Air_2_EN.pdf) | The dependable integration surface |

## Control levels

There is no joint or torque control — this is perception. The equivalent decision is **how deep the MetaCam sits in your robot's autonomy stack**. SKYLANDX describes three depths:

| Depth | MetaCam does | Your robot / code does | Who gets it (per official page) | Hackathon realism |
|---|---|---|---|---|
| 1. Scanning payload | Records a scan while riding on the robot (via MetaCam Hub mount) | Navigates by itself | "Eligible customers" | **High** — works even with zero API access |
| 2. Real-time perception layer | Streams localization and mapping live | Planning and motion control | "Eligible customers" | **Medium** — needs the Rosbridge interface enabled and documented by staff |
| 3. Full navigation module | Perception + localization + path planning; outputs navigation commands | Motion control only | Tailored per platform, **ecosystem partners** | **Low** — per-platform engineering; do not plan on it in 48 h unless staff bring a ready kit |

- **Rates and latency** of the live streams: not public. LiDAR scan rate is **10 Hz typical** (Air 2, C01) and **20 Hz** (Pro) per the brochures; pose output rate is not stated.
- **Relocalization:** a previous capture can become a "structured spatial model" (obstacles, navigable paths, waypoints) that a returning robot localizes against without remapping. How to load / query it: not public.
- **No EDU / developer edition** is advertised. Access is gated commercially ("eligible customers", "ecosystem partners") rather than by a product SKU — ask what the on-site units have unlocked.

## ROS 2 and middleware

- **Official statement:** Rosbridge protocol over WebSocket; ROS versions and message types are "contact us". **ROS 2 is not named anywhere** on the official pages — ⚠️ unverified.
- **Why that may not matter (inference):** the Rosbridge protocol is JSON over WebSocket, so a client needs no ROS install at all. A laptop script can subscribe directly and republish into ROS 2, a Unitree / AGIBOT SDK process, or a plain Python loop.
- **Skeleton client** (generic Rosbridge usage — every value in angle brackets is a placeholder you must get from staff; none of it is published by SKYLANDX):

```python
# pip install roslibpy   (third-party Rosbridge client, not a SKYLANDX package)
import roslibpy

ros = roslibpy.Ros(host="<SCANNER_IP>", port=<PORT>)          # not public
ros.run()
pose = roslibpy.Topic(ros, "<POSE_TOPIC>", "<POSE_MSG_TYPE>")  # not public
pose.subscribe(lambda m: print(m))
```

- **Bandwidth warning (inference):** point clouds serialized as JSON are heavy. Subscribe to **pose first**, then images / clouds, and throttle if the protocol options allow it.
- **Offline into ROS 2 / Nav2 (generic, not vendor-provided):** export **PCD** → load as a 3D map, or slice it at robot height into a 2D occupancy grid for a planner. This needs no SKYLANDX API.
- **C01 in ROS:** no official driver found. Expect to either get a driver from staff or write a small UDP-to-PointCloud2 + IMU publisher once you have the packet layout. Do not budget this unless staff hand you a working driver in hour one.

## Simulation and digital twins

SKYLANDX ships **no URDF / MJCF / USD assets and no Isaac Lab / MuJoCo / Gazebo repos** — it produces the *environment*, not a robot model.

| You want | Export to use | Notes |
|---|---|---|
| Collision geometry for a simulator | **OBJ** mesh | Import / convert yourself (USD or Isaac Sim export is not mentioned officially). Decimate first — scan meshes are heavy |
| Photoreal visuals | **3DGS (PLY)** from MetaCam Cloud | Official "Real2Sim" framing: pair the 3DGS with the measured point cloud / mesh for true scale. 3DGS rendering support depends on your simulator version — check before committing |
| Metric ground truth, change detection, measurements | Point cloud **PLY / PCD / LAS / E57** | CloudCompare, Open3D, PDAL (generic third-party tools) all read these |
| Autodesk / BIM workflow | **RCP** (native export from Studio), E57 | For scan-vs-BIM progress or retrofit ideas (T03) |
| Scene graph / task planner input | "Semantic model" at true scale (official claim) | Format and how to obtain it: not public — ask |

## AI stack

| Item | Status |
|---|---|
| Pretrained policies, VLA / foundation models | None — not a robot-learning vendor |
| Public datasets | None published. "Get Sample Data" is a request form on product pages |
| LeRobot support, teleoperation pipelines | None |
| On-device AI | "SOTA-SLAM" tightly coupled LiDAR + vision + IMU (+ RTK) fusion engine — closed source, runs in real time on the scanner |
| What it contributes to an AI pipeline | Metric, photoreal 3D scenes (3DGS + mesh + point cloud) as training / evaluation environments for other vendors' policies; ground-truth maps for localization |

Practical reading: pair it with someone else's model. Example — scan a clinic corridor, hand the mesh + 3DGS to a team running a Unitree, AGIBOT or Galaxea robot for simulation-first testing, and use the same scan as the localization map on the real robot.

## Compute, sensors and connectivity

Values from the official brochures (Air 2 brochure dated 2026-09, Pro 2026-08, C01 2026-08).

| | MetaCam Air 2 | MetaCam Pro | C01 LiDAR |
|---|---|---|---|
| Weight | **619 g** main unit · 363 g battery · **982 g** total | **1,160 g** (1,325 g with RTK) | **420 g** |
| LiDAR | 200,000 pts/s · 10 Hz · 0.1–40 m @ 10 % / 70 m @ 80 % · FOV 360° × 59° (-7° to +52°) · Class 1, 905 nm | 2.62 M pts/s (up to 5.24 M) · 20 Hz · 0.5–90 m @ 10 % / 170 m @ 80 % · FOV 360° × 42.4° · Class 1, 865 nm | 216,000 pts/s dual-line (108,000 single) · 10 Hz typical, up to 30 Hz · 5 cm–40 m @ 10 % / 70 m @ 80 % · FOV 360° × 65° (-20° to +45°) · non-repetitive pattern · Class 1, 905 nm |
| Cameras | 2 × 48 MP, 200° × 200° each (**default output 12 MP**) | 2 × 48 MP panoramic + 48 MP HD + 1.3 MP V-SLAM (default output 12 MP) | None |
| IMU / GNSS | RTK built in: 0.8 cm + 1 ppm (H), 1.5 cm + 1 ppm (V); raw observation logging | Same RTK figures; RTK / PPK / GCP | 6-axis IMU, **200 Hz** |
| Accuracy (post-processed, lab) | < 1 cm relative · < 1 cm thickness · **5 cm absolute** | 5 mm relative · 5 mm thickness · < 3 cm absolute | Range precision < 1 cm (1σ @ 10 m) |
| Storage / data out | TF card, **256 GB included** (up to 1 TB) | **1 TB** built-in SSD · USB 3.0 Type-C export | UDP stream |
| Wireless | **Wi-Fi 6**, 2.4 / 5 GHz, ~20 m · Bluetooth | Wi-Fi 6, 2.4 / 5 GHz, up to 20 m · Bluetooth | — |
| Power | < 20 W · 45.36 Wh battery · **150 min** runtime · USB-C PD 30 W, 120 min charge | < 26 W · 45.36 Wh · **60 min** runtime · USB-C PD 30 W | **12–30 V DC**, 15 W max |
| Environment | **IP5X** · -20 to +55 °C | IP5X · -20 to +55 °C | **IP67** · -20 to +55 °C · 100 klux ambient light |
| Robot mount | MetaCam Hub (optional accessory) | MetaCam Hub · backpack kit · vehicle mount | Direct integration |

- **On-board compute:** SLAM and the live colorized preview run on the scanner; processor not public. Final optimization, mesh and 3DGS happen in Studio (Windows PC) or Cloud.
- **Connecting:** phone ↔ scanner through MetaCam Go (Wi-Fi 6 and Bluetooth are listed; the pairing procedure, SSID and IP defaults are not public). Laptop ↔ scanner for data: TF card (Air 2) or USB-C (Pro). Laptop ↔ scanner for live streams: the Rosbridge WebSocket — address and port from staff.
- **Air 2 LiDAR note (inference, ⚠️ unverified):** its published LiDAR figures match a common off-the-shelf 360° non-repetitive sensor class, so expect that density and pattern rather than a spinning multi-beam look.
- **Spec discrepancy to be aware of:** the MetaCam Pro web page says "up to 200 m" range; the brochure spec table says 170 m @ 80 % reflectivity. Use the brochure figure.

## First 60 minutes checklist

1. **(0–5 min) Ask staff four questions:** Which units can we borrow and for how long? Is the Rosbridge / API interface enabled on them, and can we have the document? Do we get MetaCam Cloud accounts (needed for 3DGS)? Is there a Windows machine with MetaCam Studio, or a licence for ours?
2. **(5–10 min) Install MetaCam Go** on a phone (iOS / Android, download from the official Software platforms page) and pair with the scanner with staff help. Confirm battery level and free storage (Air 2: TF card present).
3. **(10–20 min) Hello-world scan:** one button to start, walk a **closed loop** through one room and a corridor at normal walking pace, return to the start point. Watch the live colorized point cloud and coverage view in the app; look for a loop-closure confirmation.
4. **(20–30 min) Get the data off:** TF card or USB-C to the Studio PC, or upload to MetaCam Cloud. **Start cloud / 3DGS processing now** — duration is not published, so do not leave it for Sunday.
5. **(30–40 min) Verify quality:** in Studio, measure one known distance (a door width, a corridor length measured by tape). No doubled walls, no bent corridor. If wrong, rescan now with a better loop.
6. **(40–50 min) Export and load in your own tool:** PLY or PCD into Open3D / CloudCompare; OBJ into your simulator. This proves the offline path end to end.
7. **(50–60 min) Read sensors live (only if API access was granted):** connect a WebSocket client to the scanner, subscribe to **pose** first, print it while walking, then add images / point cloud. If it is not working by minute 60, **commit to the offline path** and move on.
8. **Robot teams, in parallel:** ask to see the MetaCam Hub mount, check your robot's payload margin against **982 g** (Air 2 with battery), and fix a rigid mount position you can measure — you will need the scanner-to-robot transform.

## Known gotchas and safety

- **Access is the main risk.** Live perception integration is described as for "eligible customers" and full navigation for "ecosystem partners". Loaner units may be scan-only.
- **MetaCam Studio is Windows-only** (brochure). macOS / Linux teams need a Windows machine or must rely on MetaCam Cloud.
- **Cloud and privacy.** Panoramic cameras capture **faces in 360°**. In clinics, spa areas and around elderly guests, get permission, scan empty spaces, and ask where MetaCam Cloud data is hosted before uploading (hosting region is not public; the official app download links point to a `.cn` endpoint).
- **Weather.** The handhelds are **IP5X — dust-protected, no water rating**. Snow, sleet and thermal-bath humidity are a risk; the -20 °C lower limit itself is fine for Leukerbad in November. C01 is IP67.
- **SLAM-hostile places** (from SKYLANDX's own blog checklist): long featureless corridors (length stretches or shrinks), **floor-to-ceiling glass and reflective surfaces** (ghost walls — very relevant in a thermal spa), stairwells (floors collapse or separate), indoor ↔ outdoor transitions, dense vegetation, dusty or busy sites. Mitigation: close loops, return by a different route, avoid fast turns, heed in-app speed / tilt warnings.
- **Absolute vs relative accuracy.** < 1 cm is *relative*. Georeferenced accuracy (Air 2: **5 cm**) needs RTK or control points; RTK needs sky view and a correction source — a steep valley and indoor work both hurt. For most hackathon demos a local frame is enough.
- **RTK corrections:** which correction service / NTRIP credentials are available on site is unknown — ask staff rather than assume.
- **Camera resolution:** sensors are 48 MP but **default output is 12 MP**; 48 MP is a firmware configuration on request (Pro brochure).
- **Runtime:** Air 2 **150 min**, Pro **60 min** per battery. Scan resumption / merging across sessions is supported, so swap batteries rather than rush.
- **Data size:** dense clouds and 3DGS files are large. Bring fast storage and downsample before feeding planners or browsers.
- **Laser safety:** all listed LiDARs are **Class 1** (eye-safe under IEC 60825-1).
- **No e-stop of its own.** When mounted on a robot, the host robot's e-stop and safety rules apply; a badly secured ~1 kg scanner on a quadruped or humanoid is a falling-object hazard. If you ever use navigation-command output, keep a human on the host robot's stop control.
- **MetaCam Air 3** is announced only (Oct 2026): no public API, price or availability. Do not design around it unless staff put one in your hands.

## Community resources

- **No developer forum, Discord or public issue tracker** found. Support is direct: [contact form](https://skylandx.com/contact/) or info@skylandx.com (address printed in the official brochures).
- Official channels: [LinkedIn](https://www.linkedin.com/company/skylandx) · [YouTube @SkylandX-Global](https://www.youtube.com/@SkylandX-Global) (linked from the official site; workflow videos likely, not checked).
- Official blog (one post so far, 2026-09-20): [What makes a SLAM scanner](https://skylandx.com/blog/slam-scanner-algorithm/) — useful 7-point field test list.
- **Academic lineage, not SKYLANDX products:** the core team is credited with VINS-Mono, VINS-Fusion and A-LOAM, open-source SLAM frameworks published under the HKUST Aerial Robotics group. Useful background and a possible SLAM back end for a C01, but they are not the closed "SOTA-SLAM" engine and are not maintained by SKYLANDX (repositories not re-checked today).
- Best resource this weekend: the SKYLANDX engineers at the booth.

## Sources

- [SKYLANDX — Robotics & Physical AI (APIs, Rosbridge, integration depths, exports)](https://skylandx.com/industry/robotics-simulation/)
- [SKYLANDX — Spatial Perception Robots / Modular Perception Kit](https://skylandx.com/spatial-intelligence-robots/)
- [SKYLANDX — Software platforms (MetaCam Go, Studio, Cloud)](https://skylandx.com/software-platforms/)
- [SKYLANDX — MetaCam Air 2](https://skylandx.com/metacam-air-2/)
- [SKYLANDX — MetaCam Air 2 brochure (PDF, spec table)](https://skylandx.com/wp-content/uploads/MetaCam_Air_2_EN.pdf)
- [SKYLANDX — MetaCam Pro](https://skylandx.com/metacam-pro/)
- [SKYLANDX — MetaCam Pro brochure (PDF, spec table)](https://skylandx.com/wp-content/uploads/MetaCam_Pro_EN_260818.pdf)
- [SKYLANDX — C01 LiDAR](https://skylandx.com/c01-slam-lidar/)
- [SKYLANDX — C01 LiDAR brochure (PDF, spec table)](https://skylandx.com/wp-content/uploads/EN_C01_LiDAR_BROCHURE.pdf)
- [SKYLANDX — Blog: What makes a SLAM scanner (2026-09-20)](https://skylandx.com/blog/slam-scanner-algorithm/)
- [SKYLANDX — About (team background)](https://skylandx.com/about/)
- [SKYLANDX — Download page (only a gated brochure; no SDK or manuals)](https://skylandx.com/download/)
- [3D Mag — SKYLANDX launches MetaCam Air 3 (2026-10-07)](https://www.3dmag.com/?p=14376)
