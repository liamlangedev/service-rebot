# Teleoperation TODO

Status of the reBot B601 Quest teleop work. `[x]` done and tested, `[~]` written but
not fully verified, `[ ]` open.

## Done
- [x] reBot B601-DM in MuJoCo from Seeed's official MJCF (servos, coupled gripper, gravity compensation)
- [x] 6-DoF damped-least-squares IK on the TCP (<1 mm across the workspace)
- [x] Clutch-relative teleop mapping (grip = follow, A = home, B = rotation on/off, trigger = gripper)
- [x] OculusReader input (APK + ADB), now the `--input oculus` fallback
- [x] Quest-axes calibration tool, stored per input source
- [x] Mouse teleop: double-click the arm, then Ctrl+drag (works around the target being hidden inside the gripper)
- [x] Wrist / front / overhead cameras in the sim
- [x] Sim joint ranges clipped to the real arm's LeRobot soft limits
- [x] Pushed to `main` (first version)
- [x] LeRobot dataset recording (`--record`), in the real arm's format (`shoulder_pan.pos` … `gripper.pos`, degrees, `robot_type=rebot_b601_follower`); recorded and loaded back with `LeRobotDataset`

## In progress
- [~] WebXR input through the vr-teleop-kit relay (default `--input quest`): tested with a fake relay, not yet with a headset
- [~] Real-arm mode (`--robot real`) via LeRobot `rebot_b601_follower` + `follower.json`: tested against a fake robot, **never run on hardware**
- [x] Commit and push this round of changes (with `tools/check_setup.py`)

## Needs the headset
- [ ] `uv run vr-teleop-relay` + `adb reverse`, open the page on the Quest, run `tools/quest_stream_check.py`
- [ ] `tools/calibrate_quest_axes.py`, then teleop in sim, position-only first, then with rotation
- [ ] Tune `--scale` and IK speed for comfort

## Needs the real arm
- [ ] Verify the joint mapping: put the arm in a few poses and check the MuJoCo mirror matches (signs and zero pose)
- [ ] Verify the gripper mapping (motor 0 to -270 deg vs. sim finger 0 to 50 mm)
- [ ] First real teleop at low speed (`--max-joint-vel 0.3 --scale 0.5`), with someone ready to support the arm (torque turns off on exit)
- [ ] Record real episodes with `lerobot-record` and check they line up with sim episodes

## Next / nice to have
- [ ] Recording runs slower than real time with 3 cameras at 640x480 (63 frames in 4 s instead of 100). Data stays consistent because frames are spaced in sim time, but try `--cameras front,wrist` or lower resolution
- [ ] Wrap our Quest IK as a LeRobot `Teleoperator`, so `lerobot-record` can drive the real arm with real cameras
- [ ] Rename sim cameras to match the real camera names before mixing datasets
- [ ] Randomize object positions between episodes for more varied data
- [ ] Publish IK state back to the relay for haptics (vr-teleop-kit page supports it)
- [ ] Optionally commit the reBot model into the repo (now fetched by `scripts/setup_assets.sh`)
- [ ] RS (RobStride) model variant if needed
