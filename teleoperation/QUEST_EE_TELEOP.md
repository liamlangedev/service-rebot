# Quest end-effector teleop: setup and check steps

How to connect a Meta Quest 3 to the Linux PC and verify `quest_ee_teleop.py`,
which drives the simulated reBot B601 gripper with the right controller.

All commands run from `teleoperation/`.

## Controls

| Input (right controller) | Action |
|---|---|
| **A** | Start mimicking: gripper follows your hand position and rotation |
| **B** | Stop mimicking: the arm holds its pose |
| **Thumbstick left** | Close the gripper (hold; further = faster) |
| **Thumbstick right** | Open the gripper |
| **Home** key (viewer) | Send the arm home (also stops mimicking) |

---

## 1. One-time PC setup

```bash
sudo apt install android-tools-adb
./scripts/setup_assets.sh        # robot model + OculusReader + APK
uv sync

# Let normal users access the Quest over USB (vendor 2833)
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="2833", MODE="0666", GROUP="plugdev"' \
  | sudo tee /etc/udev/rules.d/51-oculus.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

## 2. One-time Quest setup

1. Install the **Meta Horizon** app on your phone and pair the headset
   (Menu → Devices → Pair new headset; same Meta account as the headset).
2. Create a free developer organization:
   <https://developers.meta.com/horizon/manage/organizations/create>
   (verify your account by phone if asked, accept the NDA, any name).
3. In the Horizon app: Devices → Quest 3 → Headset settings → **Developer Mode → On**.
4. **Restart** the headset.

## 3. Connect (every session)

1. Plug the Quest into the PC with a data-capable USB-C cable.
2. Put the headset on and accept **Allow USB debugging** (tick *Always allow*).
   The prompt appears *inside the headset*, and only after the udev rule exists.
3. Check:

   ```bash
   lsusb | grep 2833        # -> "Oculus VR, Inc. Quest 3"
   adb devices              # -> "<serial>  device"
   ```

   | `adb devices` shows | Fix |
   |---|---|
   | nothing | Developer Mode off or headset not rebooted since enabling it; replug cable |
   | `no permissions` | udev rule missing (step 1), then replug |
   | `unauthorized` | put the headset on and accept the USB debugging prompt |
   | `device` | ready |

## 4. Check the pipeline without the headset

```bash
uv run quest_ee_teleop.py --demo
```

- [ ] MuJoCo opens with the arm at home.
- [ ] After ~0.5 s the console prints `A: mimicking ON` and the arm starts moving/twisting.
- [ ] Around 3–4 s the gripper closes (`grip=` drops to 0 mm), around 6–7 s it opens.
- [ ] At 10 s `B: mimicking OFF` and the arm holds still.

## 5. Check the controller stream

Headset on, **controllers in hand** (you should see controller models, not hands):

```bash
uv run tools/quest_stream_check.py --source oculus
```

- [ ] ~30–70 Hz with `raw=` values changing as you move the right controller.
- [ ] `trig=` goes to ~1.0 when you squeeze the trigger.

If it prints `no 'r' controller pose yet`: the headset is asleep, a system dialog
(Guardian/boundary, consent) is in front, or hand tracking is active. Clear the
dialog, pick up the controllers and press a button. The OculusReader app shows a
**green background with a blue grid**; relaunch it with:

```bash
adb shell am start -n com.rail.oculus.teleop/com.rail.oculus.teleop.MainActivity
```

## 6. Live test of `quest_ee_teleop.py`

```bash
uv run quest_ee_teleop.py               # add --scale 0.5 for finer motion
```

The point you control is the **green dot between the fingertips** (the `grasp`
site), not the palm, so to pick an object bring the green dot to the object's
centre with the gripper open, then close it. If your hand's orientation can't be
reached at that spot (e.g. gripper held level right above the table), the tool
tilts a little so the fingertips still get there; `--strict-rotation` turns
that off.

The console prints `[quest] controller tracked`, then
`press A to start mimicking ...`. Status lines show `FOLLOW`/`paused`, target vs.
TCP position, IK error and gripper opening.

Stand behind the robot, facing the same way it faces (its +x). Then check:

- [ ] **Idle:** before pressing A the arm does not move when you move your hand.
- [ ] **A:** `mimicking ON`; the arm does not jump at the moment you press it.
- [ ] **Forward:** move hand away from you → gripper moves forward (+x).
- [ ] **Left:** move hand left → gripper moves left (+y).
- [ ] **Up:** raise hand → gripper rises (+z).
- [ ] **Rotation:** roll / pitch / yaw your wrist → gripper rotates the same way.
- [ ] **Thumbstick left** → gripper closes; **right** → opens; centre → stays.
- [ ] **B:** `mimicking OFF`; the arm stays put while you move your hand.
- [ ] **A again:** resumes from the arm's current pose, no jump.
- [ ] **Home** key in the viewer sends the arm home.
- [ ] `ik_err` stays at a few mm in the normal workspace.
- [ ] **Pick:** open gripper, move the green dot onto the red cube (level or
      pointing down both work), thumbstick left to close, lift: the cube comes up.

### If something is off

| Symptom | Fix |
|---|---|
| Arm moves along the wrong axis or rotates the wrong way | `uv run tools/calibrate_quest_axes.py` (writes `config/quest_calibration_oculus.json`) |
| Thumbstick left opens instead of closes | flip the sign of `np.sign(x)` in the gripper block of `quest_ee_teleop.py` |
| Motion too large / too jumpy | `--scale 0.5`, `--max-joint-vel 1.0` |
| Gripper too slow / fast | `--grip-speed 0.03` (default 0.06 m/s) |
| `(controller not tracked)` in status | see step 5 |
| Can't get low enough / gripper hits the cube | aim the green dot (fingertips) at the cube centre, gripper fully open; the palm is ~7 cm behind it |
| `could not connect over ADB` | see step 3 |

## 7. See the simulation inside the headset (`--vr`)

```bash
uv run quest_ee_teleop.py --vr                 # desktop MuJoCo window too
uv run quest_ee_teleop.py --vr --no-viewer     # headset only
uv run quest_ee_teleop.py --passthrough        # see-through headset: watch the PC screen
```

**Passthrough mode** (`--passthrough`): the headset page draws nothing. Press
**Start AR** and the headset is fully see-through, so you watch the normal
MuJoCo window on your monitor while the right controller drives the arm
(A / B / thumbstick as usual).

The script serves a WebXR page on port 8765, forwards it over USB
(`adb reverse`) and opens `http://localhost:8765/` in the Quest browser. In
this mode the controllers are read from that page, so the OculusReader app is
not used.

1. Put the headset on. The browser shows the robot, table and objects in a 2D
   window (status line: *connected: live scene*).
2. Press **Enter VR** for a full virtual scene, or **Start AR** to see the robot
   on top of your real room (passthrough).
3. The robot stands about 30 cm in front of you at table height, facing away
   from you, so your hand motions and the gripper's match. The panel above
   it shows *FOLLOWING* / *paused* and the gripper opening.
4. Same controls: **A** start, **B** stop, right thumbstick close/open.
   **Left thumbstick** moves the scene: up/down (Y), nearer/further (X).

Checks:

- [ ] The 2D page shows the robot before you enter VR.
- [ ] In VR the arm, table and cubes are in front of you, controllers visible as blue boxes.
- [ ] A / B / thumbstick work as in step 6; the robot in the headset moves live.
- [ ] Start AR shows the robot over the real room (no grey floor).

| Symptom | Fix |
|---|---|
| Page says *PC not reachable* | the script is not running, or `adb reverse tcp:8765 tcp:8765` failed (replug USB) |
| Blank page / no robot | the headset needs internet once to load three.js from cdn.jsdelivr.net |
| Robot too high/low or far | left thumbstick, or open `http://localhost:8765/?h=0.7&d=0.4` (metres) |
| Enter VR greyed out | the page must be opened as `localhost` (USB + adb reverse), not by the PC's IP |

## 8. Wireless (optional)

With USB still plugged in:

```bash
adb tcpip 5555
adb shell ip route            # note the headset IP (e.g. 172.24.1.43)
```

Unplug, then `uv run quest_ee_teleop.py --ip <quest-ip>`. PC and Quest must be on
the same network.
