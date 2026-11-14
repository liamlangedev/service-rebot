# Quest end-effector teleop: setup and check steps

How to connect a Meta Quest 3 to the Linux PC and verify `quest_ee_teleop.py`,
which drives the simulated reBot B601 gripper with the right controller.

All commands run from `teleoperation/`.

## Controls

| Input (right controller) | Action |
|---|---|
| **A** | Arm robot control |
| **B** | Stop and disarm |
| **Hold grip** | Move the arm with your hand (position and rotation; `--no-hand-rotation` = position only) |
| **Release grip** | Hold the current pose |
| **Thumbstick ↑ / ↓** | Open / close the gripper (further = faster) |
| **Thumbstick ← / →** | Rotate (roll) the gripper left / right |
| **Index trigger** (hold) | Precision mode: hand motion and stick rates × 0.25 (`--precision-scale`) |
| **Home** key (viewer) | Send the arm home (also disarms) |

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
- [ ] After ~0.5 s `A: ARMED`, at 1 s `MOVING` and the arm starts moving/twisting.
- [ ] Around 3–4 s the gripper closes (`grip=` drops to 0 mm), around 6–7 s it opens.
- [ ] ~4.5–5.5 s `MOVING (precision)`: the motion gets small; at ~9.5 s grip released
      (`ARMED - hold grip to move`), at 10 s `B: DISARMED` and the arm holds still.

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
`A = arm, B = disarm, hold grip = move ...`. Status lines show `off`/`armed`/`MOVE`
(`MOVE*` = precision), target vs.
TCP position, IK error and gripper opening.

Stand behind the robot, facing the same way it faces (its +x). Then check:

- [ ] **Idle:** before pressing A the arm does not move when you move your hand.
- [ ] **Grip before A:** nothing moves.
- [ ] **A:** `ARMED`; nothing moves until you hold the grip.
- [ ] **Hold grip:** the arm follows; it does not jump when you press the grip.
- [ ] **Forward:** move hand away from you → gripper moves forward (+x).
- [ ] **Left:** move hand left → gripper moves left (+y).
- [ ] **Up:** raise hand → gripper rises (+z).
- [ ] **Rotation:** roll / pitch / yaw your wrist → gripper rotates the same way.
- [ ] **Release grip**, move your hand, grip again: the arm continues from where it was.
- [ ] **Trigger held** while moving: the arm moves ~4x less, no jump on press/release.
- [ ] **Thumbstick ↑** → gripper opens; **↓** → closes; centre → stays.
- [ ] **Thumbstick → / ←** → gripper rolls right / left.
- [ ] **B:** `DISARMED`; the arm stays put while you move your hand, even holding grip.
- [ ] **A again:** resumes from the arm's current pose, no jump.
- [ ] **Home** key in the viewer sends the arm home.
- [ ] `ik_err` stays at a few mm in the normal workspace.
- [ ] **Pick:** open gripper, move the green dot onto the red cube (level or
      pointing down both work), thumbstick down to close, lift: the cube comes up.

### If something is off

| Symptom | Fix |
|---|---|
| Arm moves along the wrong axis or rotates the wrong way | `uv run tools/calibrate_quest_axes.py` (writes `config/quest_calibration_oculus.json`) |
| Thumbstick up closes instead of opens (or roll is reversed) | flip the sign of `stick(s.joystick[1])` (or `[0]`) in `quest_ee_teleop.py` |
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
4. Same controls as step 6 (A arm, B disarm, hold grip to move, stick, trigger).
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

## 8. Velocity feed-forward (MIT) control in the sim (`--control mit`)

The real arm (dev/roboCrafy, `teleop/mit_ff.py` + `teleop/fast_loop.py`) runs the
Damiao motors in MIT mode at 200 Hz:

```
torque = kp (q_cmd - q) + kd (dq_cmd - dq) + tau_gravity(q)
```

`dq_cmd` is the commanded joint **velocity** (filtered finite difference of the
low-passed IK output), so the motors move *with* the setpoint instead of only
being pulled towards it. `teleop/mit_sim.py` simulates exactly that controller
(same gains, filters, error clamp, gravity feed-forward, imported from
`mit_ff.py`), with the torque law evaluated at every 1 ms physics step.

```bash
uv run quest_ee_teleop.py --vr --control mit                    # real-arm controller, in VR
uv run quest_ee_teleop.py --vr --control mit --no-velocity-ff   # same, dq_cmd = 0 (to compare)
uv run quest_ee_teleop.py --vr                                  # stiff sim servos (default)
```

The status line shows `lag=` (largest joint error between command and arm).
Measured in the sim (8 cm circle at ~0.25 m/s, 200 Hz):

| Controller | Joint lag (mean) | Fingertip error (mean) |
|---|---|---|
| sim position servos (`servo`) | 3.7 deg | 16.4 mm |
| MIT + velocity feed-forward (`mit`) | 3.3 deg | 16.0 mm |
| MIT without feed-forward (`--no-velocity-ff`) | 8.5 deg | 24.8 mm |

Checks: the arm holds still without sagging before you arm it; moving fast with
`--no-velocity-ff` visibly trails your hand more than with the feed-forward; the
red-cube pick still works.

## 9. Real robot (`--real-robot`)

Same controller, same controls, but it drives the real reBot B601-DM. It uses
dev/roboCrafy's hardware path (`teleop/real_teleop.py`):

1. connects through lerobot's `rebot_b601_follower` with the measured gripper
   range (`config/gripper_limits.json`), MIT arm mode, force-limited gripper and
   the team calibration (`../follower.json`); it never re-zeroes the motors;
2. starts the 200 Hz `FastLoop` with `MitFF` (velocity + gravity feed-forward);
3. runs `gravity_check` (the arm holds still while the gravity feed-forward ramps in);
4. moves to the ready pose (gripper pointing down), **after you press Enter**;
5. teleop: controller -> shared controller logic (`teleop/ee_control.py`) ->
   singularity-guarded IK on the fingertip point -> joint targets at 200 Hz.

```bash
# 0. rehearse the whole real path without hardware (simulated stand-in arm)
uv run quest_ee_teleop.py --real-robot --fake-hardware
# 1. the real arm (find the port with: ls /dev/ttyACM* /dev/serial/by-id/)
uv run quest_ee_teleop.py --real-robot --port /dev/ttyACM0
uv run quest_ee_teleop.py --real-robot --port /dev/ttyACM0 --passthrough   # see the arm through the headset
```

The controller comes from the OculusReader app (no VR scene). The headset must
be awake for the controller to be tracked: the script wakes it over adb and keeps
it awake off-head (proximity sensor overridden), and restores normal sleep on
exit (`--no-wake` to skip). Put it on a stand facing your hands, or wear it with
`--passthrough` to see the real arm. The MuJoCo window mirrors the measured pose;
the console prints `lag=` and the loop rate.

**Rotation (sim and real):** the reBot's wrist axes sit 12-23 cm behind the
fingertips, and `wrist_flex` is already at 78 deg (limit 90) in the ready pose.
Rotating the gripper about the fingertips therefore folded the shoulder/elbow
(real-arm log: `wrist_flex` pinned at +90 deg 45% of the time, elbow at -160
deg). Now (`teleop/arm_step.py`):

- hand rotations are turned into **wrist-joint** rotations (the fingertips
  sweep with the wrist, the shoulder/elbow keep their shape);
- at a wrist limit the rotation **waits** ("wrist_flex at its limit") until you
  rotate your hand back, instead of contorting the arm.

`--fingertip-pivot` and `--no-wrist-guard` restore the old behaviour.

Safety:

- Nothing moves until you press Enter for the ready move, then **A** and **hold grip**.
- Release the grip or press **B** and the arm holds where it is.
- The IK joint speed is limited to 1.0 rad/s on the real arm (`--max-joint-vel`).
- If the arm cannot follow (singularity guard, joint limit) the target is
  pulled back to within 5 cm of the arm instead of running away.
- **Ctrl-C** stops the loop and commands a hold. Torque stays ON after exit
  (so the arm does not drop): **support the arm before switching the power off.**
- The motors' MIT error clamp (`MAX_ERR_DEG` in `teleop/mit_ff.py`) bounds the
  force when the arm is blocked, e.g. against the table.
- The fast loop saves commanded vs measured joints to `/tmp/fast_loop_log.npz`
  and prints a lag summary on exit.

First run checklist:

- [ ] `--fake-hardware` run: gravity check passes, ready move, A / grip / stick work.
- [ ] Gripper range measured on this arm: `uv run tools/measure_gripper.py --port <port>`
      (the committed file comes from the arm dev/roboCrafy was tested on).
- [ ] `../follower.json` is this arm's calibration.
- [ ] First real run with `--precision-scale 0.25` and small motions, trigger held.
- [ ] Gentle tuning if needed: `--kp-scale` / `--kd-scale` (MIT gains), `--ready-speed`.

## 10. Wireless (optional)

With USB still plugged in:

```bash
adb tcpip 5555
adb shell ip route            # note the headset IP (e.g. 172.24.1.43)
```

Unplug, then `uv run quest_ee_teleop.py --ip <quest-ip>`. PC and Quest must be on
the same network.
