"""Cut the grasp out of every rebot_sort_v1 episode and write two LeRobot datasets.

    teleoperation/.venv/bin/python training_gripper/make_dataset.py \
        --src <local copy of RoboCrafty/rebot_sort_v1> --out <dir> [--push]

Variant A (`<user>/rebot_grasp_keys_abs`): one clip per grasp, all three cameras,
absolute state and action (same as the source).

Variant B (`<user>/rebot_grasp_keys_rel`): several clips per grasp, each starting at a
different time before the close (handoff-timing augmentation), gripper camera only,
arm joints of state and action relative to the clip's first state (`anchor_state`, which
the policy does not see). The gripper stays absolute.

A clip runs from `pre` frames before the close until the TCP has risen `lift_m` above
its height at the close (forward kinematics in the MuJoCo model), plus `tail` frames.
That end is the same "grasped and lifted" condition the ROS node uses to hand back.

Episodes are rejected when the close is preceded by a fumble, when the gripper opens
again before the lift, or when the arm never lifts. The held-out episodes are written
last so `--dataset.eval_split` in lerobot-train holds out exactly those.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "teleoperation"))
sys.path.insert(0, str(HERE))

from relative import to_relative  # noqa: E402
from segments import episode_arrays, find_grasp, load_frames  # noqa: E402

CAMERAS = ["front_wide", "gripper", "high_oblique"]
TASK = "grasp the keys and lift them"


class Fk:
    def __init__(self):
        from teleop.rebot_model import RebotSim
        self.sim = RebotSim(scene="real")

    def z(self, q_deg: np.ndarray) -> float:
        import mujoco

        self.sim.data.qpos[self.sim.arm_qadr] = np.radians(q_deg[:6])
        mujoco.mj_forward(self.sim.model, self.sim.data)
        return float(self.sim.tcp_pose()[0][2])


def plan_clips(src: str, pre_a: int, pre_b: list[int], lift_m: float, tail: int,
               max_post: int, n_holdout: int) -> dict:
    eps = episode_arrays(load_frames(src))
    fk = Fk()
    kept, rejected = [], {}
    for ep, (state, action) in eps.items():
        g = find_grasp(ep, action)
        if g is None:
            rejected[ep] = "no sustained close"
            continue
        if g.n_closes_before:
            rejected[ep] = f"{g.n_closes_before} fumbled close(s) before the grasp"
            continue
        z0 = fk.z(state[g.t_close])
        t_lift = next((t for t in range(g.t_close, min(g.t_close + max_post, len(state)))
                       if fk.z(state[t]) >= z0 + lift_m), None)
        if t_lift is None:
            rejected[ep] = f"TCP never rose {lift_m * 100:.0f} cm within {max_post} frames"
            continue
        end = min(t_lift + tail, len(state))
        if g.t_release < end:
            rejected[ep] = "gripper reopened before the lift"
            continue
        kept.append(dict(ep=ep, t_close=g.t_close, t_lift=t_lift, end=end,
                         a=[max(g.t_close - pre_a, 0), end],
                         b=[[max(g.t_close - p, 0), end] for p in pre_b]))
    # held-out source episodes go last
    train, hold = kept[:-n_holdout], kept[-n_holdout:]
    return dict(train=train, holdout=hold, rejected=rejected, eps=eps,
                params=dict(pre_a=pre_a, pre_b=pre_b, lift_m=lift_m, tail=tail,
                            max_post=max_post))


def _features(src_meta, cameras: list[str], with_anchor: bool) -> dict:
    feats = {k: dict(v) for k, v in src_meta.features.items()
             if k in ("observation.state", "action")}
    for cam in cameras:
        feats[f"observation.images.{cam}"] = dict(src_meta.features[f"observation.images.{cam}"])
        feats[f"observation.images.{cam}"].pop("info", None)
    if with_anchor:
        feats["anchor_state"] = dict(feats["observation.state"])
    return feats


def write(plan: dict, src: str, out: Path, user: str, push: bool,
          variants: tuple[str, ...] = ("abs", "rel")) -> None:
    from lerobot.datasets.lerobot_dataset import LeRobotDataset

    source = LeRobotDataset("RoboCrafty/rebot_sort_v1", root=src, video_backend="pyav",
                            return_uint8=True)
    meta = source.meta
    ep_start = {int(e): int(s) for e, s in zip(meta.episodes["episode_index"],
                                               meta.episodes["dataset_from_index"])}

    specs = {
        "abs": dict(repo=f"{user}/rebot_grasp_keys_abs", cams=CAMERAS, anchor=False),
        "rel": dict(repo=f"{user}/rebot_grasp_keys_rel", cams=["gripper"], anchor=True),
    }
    specs = {k: v for k, v in specs.items() if k in variants}
    needed = sorted({c for s in specs.values() for c in s["cams"]})
    out.mkdir(parents=True, exist_ok=True)
    dsets = {}
    for name, s in specs.items():
        root = out / name
        if root.exists():
            shutil.rmtree(root)
        dsets[name] = LeRobotDataset.create(
            s["repo"], fps=meta.fps, features=_features(meta, s["cams"], s["anchor"]),
            root=root, robot_type=meta.robot_type, use_videos=True)

    frame_cache: dict[int, dict] = {}

    def frame(ep: int, t: int) -> dict:
        idx = ep_start[ep] + t
        if idx not in frame_cache:
            item = source[idx]
            frame_cache[idx] = {
                cam: item[f"observation.images.{cam}"].permute(1, 2, 0).numpy()
                for cam in needed
            }
        return frame_cache[idx]

    counts = {"abs": 0, "rel": 0}
    for clip in plan["train"] + plan["holdout"]:
        ep = clip["ep"]
        state, action = plan["eps"][ep]
        a0, a1 = clip["a"]
        for t in range(a0, a1) if "abs" in dsets else ():
            imgs = frame(ep, t)
            f = {"observation.state": state[t].astype(np.float32),
                 "action": action[t].astype(np.float32), "task": TASK}
            f.update({f"observation.images.{c}": imgs[c] for c in CAMERAS})
            dsets["abs"].add_frame(f)
        if "abs" in dsets:
            dsets["abs"].save_episode()
            counts["abs"] += 1
        for b0, b1 in clip["b"] if "rel" in dsets else ():
            anchor = state[b0].astype(np.float32)
            for t in range(b0, b1):
                dsets["rel"].add_frame({
                    "observation.state": to_relative(state[t], anchor),
                    "action": to_relative(action[t], anchor),
                    "anchor_state": anchor,
                    "observation.images.gripper": frame(ep, t)["gripper"],
                    "task": TASK,
                })
            dsets["rel"].save_episode()
            counts["rel"] += 1
        frame_cache.clear()
        print(f"episode {ep}: abs {a1 - a0} frames, rel {len(clip['b'])} clips", flush=True)

    n_hold = len(plan["holdout"])
    summary = dict(
        source="RoboCrafty/rebot_sort_v1", task=TASK, params=plan["params"],
        train_source_episodes=[c["ep"] for c in plan["train"]],
        holdout_source_episodes=[c["ep"] for c in plan["holdout"]],
        rejected={str(k): v for k, v in plan["rejected"].items()},
        episodes=counts,
        # lerobot holds out the last ceil(n * eval_split) episodes; pick a value just under
        # the exact fraction so the ceil lands on the held-out clips.
        eval_split={k: (n_hold * (1 if k == "abs" else len(plan["params"]["pre_b"])) - 0.5)
                    / counts[k] for k in dsets if counts[k]},
    )
    for name, ds in dsets.items():
        ds.finalize()
        (out / name / "meta" / "grasp_clips.json").write_text(json.dumps(summary, indent=2))
        if push:
            ds.push_to_hub(private=True, tags=["rebot", "grasp"])
            print("pushed", specs[name]["repo"], "(private)")
    print(json.dumps({k: v for k, v in summary.items() if k != "params"}, indent=2))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--src", required=True, help="local copy of RoboCrafty/rebot_sort_v1")
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--user", default="niru-5")
    p.add_argument("--pre-a", type=int, default=75, help="frames before the close (variant A)")
    p.add_argument("--pre-b", type=int, nargs="+", default=[75, 60, 45, 30],
                   help="start offsets in frames before the close (variant B)")
    p.add_argument("--lift-m", type=float, default=0.05, help="lift that ends the clip")
    p.add_argument("--tail", type=int, default=6, help="frames kept after the lift")
    p.add_argument("--max-post", type=int, default=75, help="max frames from close to lift")
    p.add_argument("--holdout", type=int, default=3, help="source episodes held out (last)")
    p.add_argument("--plan-only", action="store_true", help="print the clip plan and stop")
    p.add_argument("--save-plan", type=Path, help="write the clip plan as JSON (needs MuJoCo)")
    p.add_argument("--plan", type=Path,
                   help="use a saved plan instead of computing it (no MuJoCo needed)")
    p.add_argument("--push", action="store_true", help="push both datasets to the Hub, private")
    p.add_argument("--variants", nargs="+", default=["abs", "rel"], choices=["abs", "rel"])
    p.add_argument("--episodes", type=int, nargs="+", help="only these source episodes (tests)")
    a = p.parse_args()

    if not Path(a.src).exists():  # a Hub repo id: fetch it (used on HF Jobs)
        from huggingface_hub import snapshot_download
        a.src = snapshot_download(a.src, repo_type="dataset",
                                  local_dir=str(a.out / "_src"))

    if a.plan:
        plan = json.loads(a.plan.read_text())
        plan["rejected"] = {int(k): v for k, v in plan["rejected"].items()}
        plan["eps"] = episode_arrays(load_frames(a.src))
    else:
        plan = plan_clips(a.src, a.pre_a, a.pre_b, a.lift_m, a.tail, a.max_post, a.holdout)
    if a.save_plan:
        a.save_plan.write_text(json.dumps({k: v for k, v in plan.items() if k != "eps"},
                                          indent=1, default=int))
        print("wrote", a.save_plan)
    for c in plan["train"] + plan["holdout"]:
        tag = "HOLDOUT" if c in plan["holdout"] else ""
        print(f"ep {c['ep']:2d} close {c['t_close']:4d} lift {c['t_lift']:4d} "
              f"(+{(c['t_lift'] - c['t_close']) / 30:.2f}s) clip A {c['a']} {tag}")
    for ep, why in plan["rejected"].items():
        print(f"ep {ep:2d} rejected: {why}")
    if a.episodes:
        for key in ("train", "holdout"):
            plan[key] = [c for c in plan[key] if c["ep"] in a.episodes]
    if not (a.plan_only or a.save_plan):
        write(plan, a.src, a.out, a.user, a.push, tuple(a.variants))


if __name__ == "__main__":
    main()
