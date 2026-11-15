"""200 Hz control thread for the real arm, decoupled from the recording rate.

The thread is the only user of the motor bus: every tick it computes the next
joint command (Leap -> clutch -> IK), sends it, and reads the joint feedback.
The lerobot record loop (e.g. 60 fps) just samples the latest values:
robot.get_observation() returns cached joints + fresh camera frames, and
robot.send_action() becomes a no-op (the thread already commanded the arm).
"""
import threading
import time

import numpy as np

from teleop.rebot_real import GRIPPER_OPEN_DEG, READY_QPOS, JOINT_NAMES, joint_space_path, q_to_action

from lerobot.cameras import DepthCamera


class FastLoop:
    current: "FastLoop | None" = None

    def __init__(self, robot, rate: float = 200.0, mit=None):
        self.robot, self.rate, self.mit = robot, rate, mit
        self._last_send = time.perf_counter()
        self._orig = dict(send=robot.send_action, get_obs=robot.get_observation,
                          disconnect=robot.disconnect)
        self._lock = threading.Lock()
        self._action = None
        self._joints = None
        self._stop = threading.Event()
        self._thread = None
        self._error = None
        self.hz = 0.0
        self._log = []
        self._dbg = []
        self._mode = "teleop"  # teleop | stopped | returning
        self._hold = None
        self._path, self._path_i = [], 0
        self._after, self._path_gripper = "teleop", GRIPPER_OPEN_DEG
        self._released = False
        self._frames = {}
        self._cam_warned = {}
        self._owner = None
        self._keys = None
        robot.send_action = self._send_action
        robot.get_observation = self._get_observation
        robot.disconnect = self._disconnect
        FastLoop.current = self

    # ---- thread ---------------------------------------------------------
    def start(self, step_fn):
        """step_fn(dt) -> action dict (degrees); called once per tick."""
        if self._thread is None:
            self._joints = self.robot._present_pos()
            self._owner = getattr(step_fn, "__self__", None)
            self._start_keys()
            self._thread = threading.Thread(target=self._run, args=(step_fn,), daemon=True)
            self._thread.start()

    # ---- keys: S = stop, G = resume, H = return to ready --------------------
    def _start_keys(self):
        try:
            from pynput import keyboard
        except Exception as e:
            print(f"[fast_loop] no keyboard listener, stop key unavailable: {e!r}")
            return

        def on_press(key):
            ch = getattr(key, "char", None)
            ch = ch.lower() if ch else ch
            if ch == "s":
                self.stop()
            elif ch == "g":
                self.resume()
            elif ch == "h":  # not R: lerobot uses R/N/Q to re-record/next/quit
                self.return_to_ready()

        self._keys = keyboard.Listener(on_press=on_press)
        self._keys.start()

    def stop(self):
        """Freeze at the current pose, instantly (checked every 5 ms)."""
        with self._lock:
            joints = dict(self._joints)
        self._hold = {f"{m}.pos": p for m, p in joints.items()}
        if self.mit is not None:
            self.mit.freeze(self._hold)
        self._mode = "stopped"
        print("[fast_loop] STOPPED. G = resume, H = return to the ready pose.")

    def resume(self):
        if self._mode == "stopped":
            self._resync()
            self._mode = "teleop"
            print("[fast_loop] resumed (release and re-press the clutch).")

    def return_to_ready(self):
        if self._mode == "returning":
            return
        self._go_to(READY_QPOS, 0.6, after="teleop", gripper_deg=GRIPPER_OPEN_DEG)
        print("[fast_loop] returning to the ready pose (S to stop).")

    def _go_to(self, q_target, speed, after, gripper_deg):
        with self._lock:
            joints = dict(self._joints)
        q = np.radians([joints[n] for n in JOINT_NAMES])
        self._path = list(joint_space_path(q, q_target, speed, self.rate))
        self._path_i, self._after, self._path_gripper = 0, after, gripper_deg
        self._mode = "returning"

    def park_and_release(self, speed: float = 0.4, rest_qpos=None) -> None:
        """Lower the arm slowly to the folded rest pose (all joints 0), then release torque.

        The control thread keeps holding the arm with gravity feed-forward until it arrives, so
        the arm is never dropped. Without this, exiting the process leaves the motors limp."""
        if self._thread is None or not self._thread.is_alive():
            return
        rest = np.zeros(6) if rest_qpos is None else rest_qpos
        with self._lock:
            grip = self._joints["gripper"]
        self._go_to(rest, speed, after="hold", gripper_deg=grip)
        print("[fast_loop] lowering to the rest pose...")
        t0 = time.time()
        while self._mode == "returning" and time.time() - t0 < 30.0:
            time.sleep(0.05)
        time.sleep(0.7)
        self._stop.set()
        self._thread.join(timeout=1.0)
        try:
            self.robot.bus.disable_all()
            self._released = True
            print("[fast_loop] at rest, torque released.")
        except Exception as e:
            print(f"[fast_loop] could not release torque: {e!r}")

    def _resync(self):
        """Make the teleoperator's IK state match where the arm actually is."""
        if self._owner is not None and hasattr(self._owner, "resync"):
            with self._lock:
                joints = dict(self._joints)
            self._owner.resync({f"{m}.pos": p for m, p in joints.items()})

    def _next_action(self, step_fn, dt):
        if self._mode == "stopped":
            return dict(self._hold)
        if self._mode == "returning":
            if self._path_i < len(self._path):
                q = self._path[self._path_i]
                self._path_i += 1
                return q_to_action(q, self._path_gripper)
            if self._after == "hold":
                self._hold = q_to_action(self._path[-1], self._path_gripper)
                if self.mit is not None:
                    self.mit.freeze(self._hold)
                self._mode = "stopped"
                return dict(self._hold)
            self._resync()
            self._mode = "teleop"
            print("[fast_loop] at the ready pose, teleop active.")
        return step_fn(dt)

    def _run(self, step_fn):
        period = 1.0 / self.rate
        nxt = last = time.perf_counter()
        hz_t, hz_n = last, 0
        try:
            while not self._stop.is_set():
                now = time.perf_counter()
                dt = float(np.clip(now - last, 1e-3, 0.05))
                last = now
                try:
                    action = self._next_action(step_fn, dt)
                except Exception as e:
                    # A bug in the teleop/IK layer must never stop the commands: freeze and keep holding.
                    import traceback
                    traceback.print_exc()
                    print(f"[fast_loop] control step failed ({e!r}); holding position. Press G to resume.")
                    self.stop()
                    action = dict(self._hold)
                self._send(action, dt)
                joints = self.robot._present_pos()
                with self._lock:
                    self._action, self._joints = action, joints
                row = getattr(getattr(step_fn, "__self__", None), "debug_row", None)
                self._dbg.append(row if row is not None else ())
                self._log.append((now, *(action[f"{m}.pos"] for m in joints),
                                  *(joints[m] for m in joints)))
                hz_n += 1
                if now - hz_t > 2.0:
                    self.hz = hz_n / (now - hz_t)
                    print(f"[fast_loop] {self.hz:.0f} Hz")
                    hz_t, hz_n = now, 0
                nxt += period
                sleep = nxt - time.perf_counter()
                if sleep > 0:
                    time.sleep(sleep)
                else:
                    nxt = time.perf_counter()
        except Exception as e:  # keep the error for the record loop to raise
            self._error = e
            print(f"[fast_loop] stopped: {e!r}")

    def latest_action(self):
        if self._error:
            raise RuntimeError(f"fast control loop died: {self._error!r}")
        with self._lock:
            return dict(self._action) if self._action else None

    def _save_log(self, path="/tmp/fast_loop_log.npz"):
        """Commanded vs measured joints (degrees), plus a lag summary."""
        if len(self._log) < 100:
            return
        a = np.array(self._log)
        t, n = a[:, 0] - a[0, 0], (a.shape[1] - 1) // 2
        cmd, meas = a[:, 1:1 + n], a[:, 1 + n:]
        names = list(self.robot.motors)
        dbg = np.array(self._dbg[:len(t)]) if self._dbg and len(self._dbg[0]) else np.zeros((len(t), 0))
        np.savez(path, t=t, cmd=cmd, meas=meas, names=names, dbg=dbg)
        k = max(1, int(0.1 * self.rate))  # speeds over 100 ms
        print(f"[fast_loop] log saved to {path}\n  joint            lag p95/max [deg]   peak speed cmd/meas [deg/s]")
        for j, name in enumerate(names):
            lag = np.abs(cmd[:, j] - meas[:, j])
            vc = np.abs(cmd[k:, j] - cmd[:-k, j]) / 0.1
            vm = np.abs(meas[k:, j] - meas[:-k, j]) / 0.1
            print(f"  {name:14s} {np.percentile(lag, 95):6.1f} / {lag.max():6.1f}        "
                  f"{vc.max():6.0f} / {vm.max():6.0f}")

    def _hold_in_place(self):
        """Command the measured pose so the motors stop instead of chasing the last setpoint."""
        if self._released:
            return
        try:
            pos = self.robot._present_pos()
            self._send({f"{m}.pos": p for m, p in pos.items()}, 0.01)
        except Exception as e:
            print(f"[fast_loop] could not send hold command: {e!r}")

    # ---- patched robot methods -------------------------------------------
    def _send(self, action, dt):
        if self.mit is None:
            self._orig["send"](action)
        else:
            joints = self._joints if self._joints is not None else self.robot._present_pos()
            self.mit.send(action, joints, dt)

    def _send_action(self, action):
        if self._thread:
            return action  # the control thread already commanded the arm
        now = time.perf_counter()
        dt, self._last_send = now - self._last_send, now
        self._send(action, dt)
        return action

    def gravity_check(self, seconds: float = 3.0) -> bool:
        """Hold the measured pose while ramping the gravity feed-forward 0 -> 1.
        With the right sign the tracking error of shoulder_lift/elbow shrinks;
        if it grows, the sign (or model) is wrong and we refuse to continue."""
        if self.mit is None:
            return True
        pos = self.robot._present_pos()
        hold = {f"{m}.pos": p for m, p in pos.items()}
        idx = ["shoulder_lift", "elbow_flex"]
        err, t0 = [], time.perf_counter()
        while (el := time.perf_counter() - t0) < seconds:
            self.mit.gravity_scale = min(1.0, el / (0.8 * seconds))
            self._send(hold, 0.01)
            now = self.robot._present_pos()
            err.append((el, max(abs(now[m] - hold[f"{m}.pos"]) for m in idx)))
            time.sleep(0.01)
        e = np.array(err)
        e0, e1 = e[e[:, 0] < 0.4, 1].mean(), e[e[:, 0] > seconds - 0.4, 1].mean()
        print(f"[gravity_check] hold error {e0:.1f} deg without feed-forward, {e1:.1f} deg with it")
        if e1 > e0 + 2.0:
            self.mit.gravity_scale = 0.0
            print("[gravity_check] FAILED: the feed-forward makes it worse (sign/model wrong).")
            return False
        return True

    def _get_observation(self):
        if not self._thread:
            return self._orig["get_obs"]()
        if self._error:
            raise RuntimeError(f"fast control loop died: {self._error!r}")
        with self._lock:
            obs = {f"{m}.pos": p for m, p in self._joints.items()}
        for key, cam in self.robot.cameras.items():
            if getattr(cam, "use_rgb", True):
                obs[key] = self._read_camera(key, cam)
            if isinstance(cam, DepthCamera) and cam.use_depth:
                obs[f"{key}_depth"] = cam.read_latest_depth()
        return obs

    def _read_camera(self, key, cam):
        """A camera hiccup must not kill the recording while the arm is in the air:
        reuse the last frame for up to 3 s, and only then raise."""
        now = time.time()
        try:
            frame = cam.read_latest()
        except TimeoutError as e:
            last = self._frames.get(key)
            if last is None or now - last[0] > 3.0:
                raise
            if now - self._cam_warned.get(key, 0) > 5.0:
                print(f"[camera] {key}: no fresh frame ({e}); reusing the last one")
                self._cam_warned[key] = now
            return last[1]
        self._frames[key] = (now, frame)
        return frame

    def _disconnect(self):
        self._stop.set()
        if self._keys is not None:
            self._keys.stop()
        if self._thread:
            self._thread.join(timeout=1.0)
            self._hold_in_place()
        self._save_log()
        self.robot.disconnect = self._orig["disconnect"]
        self.robot.send_action = self._orig["send"]
        self.robot.get_observation = self._orig["get_obs"]
        FastLoop.current = None
        self._orig["disconnect"]()
