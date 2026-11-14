"""Skill library: the robot's verbs. Deterministic Python, every motion goes through Safety.

Each skill takes up to three string arguments (object, target, text) and returns a
SkillResult with ok / a failure code. The planner only ever composes these skills; it never
produces joint angles. The same SKILLS table drives the planner prompt and graph validation.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np

from autonomy.arm import PAD_OFFSET, Arm
from autonomy.geometry import grasp_rotation, ray_plane_z, tilted_approach
from autonomy.perception import label_matches
from autonomy.safety import EStopped, SafetyError
from autonomy.world import Obj, WorldModel
from teleop.rebot_model import GRIPPER_MAX

ANY = {"", "any", "anything", "all", "everything", "every object", "any object", "objects", "items"}


@dataclass
class SkillResult:
    ok: bool
    code: str = "ok"           # failure code the graph can branch on
    info: str = ""
    data: dict = field(default_factory=dict)


@dataclass
class SkillSpec:
    name: str
    description: str
    args: dict[str, str]                 # arg -> meaning (only object / target / text)
    required: tuple[str, ...] = ()
    failures: tuple[str, ...] = ()


SKILLS: dict[str, SkillSpec] = {s.name: s for s in [
    SkillSpec("look", "Refresh the scene from the fixed cameras. Optionally focus on one object name.",
              {"object": "optional name to look for"}, (), ("nothing_seen",)),
    SkillSpec("select_next", "Choose the next not-yet-handled object matching a category and bind it "
              "to $current. Skips objects already inside `target`. Use it to loop over many objects.",
              {"object": "category, e.g. 'can', 'red', 'any'", "target": "optional zone/bin to skip"},
              ("object",), ("none_left",)),
    SkillSpec("pick", "Grasp one object (fixed cameras for coarse position, wrist camera for fine "
              "alignment, gripper width to confirm the grasp) and lift it.",
              {"object": "object id, name or $current"}, ("object",),
              ("not_found", "too_big", "unreachable", "missed", "dropped")),
    SkillSpec("place", "Put the held object into a named zone/bin, or on top of another object.",
              {"target": "zone/bin name or object id/name"}, ("target",),
              ("not_holding", "unknown_target", "no_space", "unreachable")),
    SkillSpec("check", "Re-look and verify that `object` is inside/on `target`.",
              {"object": "object id, name or $current", "target": "zone/bin or object"},
              ("object", "target"), ("not_found", "not_there")),
    SkillSpec("open_gripper", "Open the gripper (drops whatever it holds).", {}, (), ()),
    SkillSpec("home", "Move out of the cameras' view (observe pose).", {}, (), ()),
    SkillSpec("say", "Tell the operator something (e.g. why the task cannot be done).",
              {"text": "message"}, ("text",), ()),
    SkillSpec("run_policy", "Run a learned LeRobot policy (ACT / SmolVLA / pi0.5) for a skill that "
              "scripting cannot do. Only available when configured.",
              {"text": "policy name or task sentence"}, ("text",), ("not_configured", "failed")),
]}


@dataclass
class GraspParams:
    hover: float = 0.10              # pre-grasp distance above the grasp point [m]
    max_open: float = GRIPPER_MAX    # per finger [m]
    open_margin: float = 0.02        # extra opening around the object [m]
    min_hold: float = 0.003          # finger opening below this after closing = missed
    tilts_deg: tuple = (0, 15, 30, 45)
    wrist_iters: int = 3
    wrist_tol: float = 0.003         # stop refining below this x/y correction [m]


class SkillContext:
    def __init__(self, arm: Arm, world: WorldModel, grasp: GraspParams | None = None,
                 policies: dict | None = None, log=print):
        self.arm, self.world = arm, world
        self.grasp = grasp or GraspParams()
        self.policies = policies or {}
        self.vars: dict[str, str] = {}
        self.holding: Obj | None = None
        self.grasp_offset = 0.0          # grasp point height above the held object's bottom
        self.pick_failures: dict[str, int] = {}
        self.log = log

    # ---- helpers ------------------------------------------------------------------
    def resolve(self, ref: str) -> str:
        return self.vars.get(ref, ref) if ref.startswith("$") else ref

    def _look(self, queries=None):
        """Moves the arm out of the fixed cameras' view if needed, then looks."""
        tcp, _ = self.arm.fk(self.arm.q_cmd if self.arm.q_cmd is not None else None)
        if tcp[0] > 0.02:
            self.arm.observe_pose()
        return self.world.look(queries)

    def _find(self, query: str) -> Obj | None:
        o = self.world.find(query)
        if o is None:
            self._look([query] if query.lower() not in ANY and not query.startswith("obj") else None)
            o = self.world.find(query)
        return o

    def _plan_grasp(self, p: np.ndarray, finger_yaw: float):
        """First tilt for which both the hover and the grasp pose are reachable."""
        az = float(np.arctan2(p[1], p[0]))
        fdir = np.array([np.cos(finger_yaw), np.sin(finger_yaw), 0.0])
        for t in self.grasp.tilts_deg:
            a = tilted_approach(az, np.radians(t))
            R = grasp_rotation(a, fdir)
            tcp = p - PAD_OFFSET * a
            pre = tcp - self.grasp.hover * a
            q_pre, ok1 = self.arm.solve_ik(pre, R)
            if not ok1:
                continue
            _, ok2 = self.arm.solve_ik(tcp, R, q_seed=q_pre)
            if ok2:
                return a, R, tcp, pre
        return None

    def _reachable_xy(self, z: float):
        def ok(xy):
            p = np.array([xy[0], xy[1], z])
            return self._plan_grasp(p, float(np.arctan2(xy[1], xy[0])) + np.pi / 2) is not None
        return ok

    def _wrist_refine(self, obj: Obj, grasp_pt: np.ndarray, finger_yaw: float, R, a):
        """Visual servoing with the wrist camera: re-centre over the object at hover height."""
        rig = self.world.rig
        if not rig.wrist:
            return grasp_pt, finger_yaw
        for _ in range(self.grasp.wrist_iters):
            img = rig.grab([rig.wrist])[rig.wrist]
            self.world.last_images[rig.wrist] = img
            cam = rig.model(rig.wrist)
            dets = self.world.detector.detect(img, [obj.label], rig.wrist)
            dets = [d for d in dets if label_matches(obj.label, d.label) > 0.99]
            expected = cam.project(grasp_pt)[0]
            if not dets or np.any(np.isnan(expected)):
                self.log("    wrist camera: object not seen, keeping the coarse estimate")
                break
            d = min(dets, key=lambda d: np.hypot(d.uv[0] - expected[0], d.uv[1] - expected[1]))
            hit = ray_plane_z(*cam.ray(d.uv), grasp_pt[2])
            if hit is None:
                break
            shift = hit[:2] - grasp_pt[:2]
            if d.angle is not None:
                yaw = self.world._image_angle_to_yaw(cam, d.uv, d.angle, grasp_pt[2])
                if yaw is not None and obj.width is not None and obj.length is not None and obj.length > 1.2 * obj.width:
                    finger_yaw = yaw + np.pi / 2
            if np.linalg.norm(shift) > 0.06:
                self.log(f"    wrist camera: implausible {np.linalg.norm(shift) * 100:.1f} cm jump, ignored")
                break
            grasp_pt = grasp_pt + np.array([shift[0], shift[1], 0.0])
            self.log(f"    wrist camera: corrected by {np.linalg.norm(shift) * 1000:.1f} mm")
            pre = grasp_pt - PAD_OFFSET * a - self.grasp.hover * a
            self.arm.move_tcp(pre, R, linear=True, speed=0.5)
            if np.linalg.norm(shift) < self.grasp.wrist_tol:
                break
        return grasp_pt, finger_yaw

    # ---- skills -------------------------------------------------------------------
    def look(self, object="", **_):
        q = object.strip()
        objs = self._look([q] if q and q.lower() not in ANY else None)
        if not objs:
            return SkillResult(False, "nothing_seen", "no objects detected")
        return SkillResult(True, info=f"{len(objs)} objects", data={"objects": [o.summary() for o in objs]})

    def select_next(self, object="any", target="", **_):
        self._look()
        zone = self.world.find_zone(target) if target else None
        cands = []
        for o in self.world.objects:
            if o.id in self.world.handled or self.pick_failures.get(o.id, 0) >= 2:
                continue
            if zone is not None and zone.contains(o.pos[:2]):
                continue
            if object.lower() not in ANY and label_matches(object, o.label) <= 0:
                continue
            cands.append(o)
        if not cands:
            return SkillResult(False, "none_left", f"no more '{object}' objects")
        o = min(cands, key=lambda o: np.linalg.norm(o.pos[:2]))
        self.vars["$current"] = o.id
        return SkillResult(True, info=f"$current = {o.id} ({o.label})", data=o.summary())

    def pick(self, object, **_):
        if self.holding is not None:
            self.arm.set_gripper(GRIPPER_MAX)
            self.holding = None
        obj = self._find(self.resolve(object))
        if obj is None:
            return SkillResult(False, "not_found", f"cannot see '{object}'")
        res = self._pick(obj)
        if not res.ok:
            self.pick_failures[obj.id] = self.pick_failures.get(obj.id, 0) + 1
        return res

    def _pick(self, obj: Obj) -> SkillResult:
        g = self.grasp
        if obj.width is not None and obj.width > 2 * g.max_open - 0.01:
            return SkillResult(False, "too_big", f"{obj.label} is {obj.width * 100:.0f} cm wide")
        az = float(np.arctan2(obj.pos[1], obj.pos[0]))
        elongated = obj.yaw is not None and obj.width is not None and obj.length is not None and obj.length > 1.2 * obj.width
        finger_yaw = obj.yaw + np.pi / 2 if elongated else az + np.pi / 2
        bottom = obj.pos[2] - obj.height / 2
        grasp_z = bottom + float(np.clip(obj.height * 0.5, 0.012, 0.045))
        p = np.array([obj.pos[0], obj.pos[1], grasp_z])
        plan = self._plan_grasp(p, finger_yaw)
        if plan is None:
            return SkillResult(False, "unreachable", f"{obj.label} at {np.round(obj.pos[:2], 2)} is out of reach")
        a, R, tcp, pre = plan
        open_w = g.max_open if obj.width is None else min(g.max_open, obj.width / 2 + g.open_margin)
        self.log(f"    pick {obj.id} ({obj.label}) at {np.round(p, 3)}")
        self.arm.set_gripper(open_w, settle=0.3)
        self.arm.move_tcp(pre, R)
        p, finger_yaw2 = self._wrist_refine(obj, p, finger_yaw, R, a)
        if finger_yaw2 != finger_yaw:
            plan = self._plan_grasp(p, finger_yaw2)
            if plan is not None:
                a, R, _, pre = plan
                self.arm.move_tcp(pre, R, linear=True, speed=0.5)
        tcp = p - PAD_OFFSET * a
        self.arm.move_tcp(tcp, R, linear=True, speed=0.4)
        width = self.arm.set_gripper(0.0, settle=0.8)
        lift = tcp + np.array([0, 0, g.hover + 0.02])
        if width < g.min_hold:
            self.arm.set_gripper(open_w, settle=0.3)
            self.arm.move_tcp(lift, R, linear=True, speed=0.6)
            return SkillResult(False, "missed", "gripper closed on nothing")
        self.arm.move_tcp(lift, R, linear=True, speed=0.6)
        if self.arm.gripper < g.min_hold:
            return SkillResult(False, "dropped", "object slipped out while lifting")
        self.holding = obj
        self.grasp_offset = p[2] - bottom
        self.world.objects = [o for o in self.world.objects if o.id != obj.id]
        return SkillResult(True, info=f"holding {obj.id} ({obj.label}), finger opening {width * 1000:.0f} mm")

    def place(self, target, **_):
        if self.holding is None or self.arm.gripper < self.grasp.min_hold:
            self.holding = None
            return SkillResult(False, "not_holding", "nothing in the gripper")
        held = self.holding
        tgt = self.resolve(target)
        zone = self.world.find_zone(tgt)
        table_z = self.world.cfg.table_z
        if zone is not None:
            foot = max(held.width or 0.04, held.length or 0.04) / 2
            spot = self.world.free_spot(zone, foot, self._reachable_xy(table_z + self.grasp_offset + 0.01))
            if spot is None:
                return SkillResult(False, "no_space", f"no free reachable spot in {zone.name}")
            p = np.array([spot[0], spot[1], table_z + zone.drop_height + self.grasp_offset])
            where = zone.name
        else:
            base = self.world.find(tgt)
            if base is None:
                self._look()
                base = self.world.find(tgt)
            if base is None:
                return SkillResult(False, "unknown_target", f"no zone or object called '{target}'")
            top = base.pos[2] + base.height / 2
            p = np.array([base.pos[0], base.pos[1], top + 0.015 + self.grasp_offset])
            where = f"{base.id} ({base.label})"
        az = float(np.arctan2(p[1], p[0]))
        plan = self._plan_grasp(p, az + np.pi / 2)
        if plan is None:
            return SkillResult(False, "unreachable", f"cannot reach {where}")
        a, R, tcp, pre = plan
        self.log(f"    place {held.id} -> {where} at {np.round(p, 3)}")
        self.arm.move_tcp(pre, R)
        self.arm.move_tcp(tcp, R, linear=True, speed=0.4)
        self.arm.set_gripper(GRIPPER_MAX, settle=0.5)
        self.arm.move_tcp(pre, R, linear=True, speed=0.6)
        held.pos = np.array([p[0], p[1], p[2] - self.grasp_offset + held.height / 2])
        self.world.objects.append(held)
        self.world.handled.add(held.id)
        self.holding = None
        return SkillResult(True, info=f"placed {held.id} in/on {where}")

    def check(self, object, target, **_):
        ref = self.resolve(object)
        label = next((o.label for o in self.world.objects if o.id == ref), ref)
        self._look()
        o = self.world.find(ref) or self.world.find(label)
        if o is None:
            return SkillResult(False, "not_found", f"cannot see {object} any more")
        zone = self.world.find_zone(target)
        if zone is not None:
            ok = zone.contains(o.pos[:2], margin=0.01)
        else:
            base = self.world.find(target)
            ok = base is not None and np.linalg.norm(base.pos[:2] - o.pos[:2]) < 0.05 and o.pos[2] > base.pos[2]
        return SkillResult(ok, "ok" if ok else "not_there", f"{o.label} at {np.round(o.pos[:2], 3)}")

    def open_gripper(self, **_):
        self.arm.set_gripper(GRIPPER_MAX)
        self.holding = None
        return SkillResult(True)

    def home(self, **_):
        self.arm.observe_pose()
        return SkillResult(True)

    def say(self, text="", **_):
        self.log(f"  ROBOT SAYS: {text}")
        return SkillResult(True, info=text)

    def run_policy(self, text="", **_):
        runner = self.policies.get(text) or self.policies.get("default")
        if runner is None:
            return SkillResult(False, "not_configured",
                               "no learned policy configured (see autonomy/README.md, 'Learned skills')")
        ok = bool(runner(self.arm, self.world.rig, text))
        return SkillResult(ok, "ok" if ok else "failed")

    # ---- dispatch -----------------------------------------------------------------
    def run(self, name: str, args: dict[str, str]) -> SkillResult:
        fn = getattr(self, name, None)
        if name not in SKILLS or fn is None:
            return SkillResult(False, "unknown_skill", name)
        kwargs = {k: self.resolve(v) if k == "object" else v for k, v in args.items() if v != ""}
        t0 = time.perf_counter()
        try:
            res = fn(**kwargs)
        except EStopped:
            raise
        except SafetyError as e:
            res = SkillResult(False, "unreachable" if "reach" in str(e) else "safety", str(e))
        res.data["seconds"] = round(time.perf_counter() - t0, 2)
        return res
