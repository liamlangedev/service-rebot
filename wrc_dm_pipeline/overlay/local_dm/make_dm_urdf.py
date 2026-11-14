#!/usr/bin/env python
"""Generate WRC's kinematic URDF for the reBot B601-DM (added by the hackathon port; NOT upstream).

Source: Seeed's official DM URDF (steel_team/teleoperation/assets/reBot-DevArm/
Rebot_Arm_description/DM/urdf/ReBot_Arm_DM.urdf, fetched by that folder's
scripts/setup_assets.sh). WRC's planner/safety need an `gripper_end` tool frame;
the DM URDF ends at `end_link` (which sits at the fingertips, tool along +x), so
we add `gripper_end` 1.5 cm behind the fingertips -- the same "tip offset below
TCP" convention WRC uses for the RS arm (CLAUDE.md, insertion_depth_m).
Only kinematics are used (pinocchio.buildModelFromUrdf), so mesh paths are irrelevant.
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
TELEOP = Path(os.environ.get("STEEL_TEAM_TELEOP_DIR", HERE.parents[1] / "steel_team" / "teleoperation"))
SRC = TELEOP / "assets" / "reBot-DevArm" / "Rebot_Arm_description" / "DM" / "urdf" / "ReBot_Arm_DM.urdf"
OUT = HERE / "assets" / "ReBot_Arm_DM_wrc.urdf"
TIP_OFFSET_M = 0.015

EXTRA = f"""
  <!-- added by wrc/local_dm/make_dm_urdf.py: WRC tool frame -->
  <link name="gripper_end" />
  <joint name="gripper_end_joint" type="fixed">
    <origin xyz="{-TIP_OFFSET_M} 0 0" rpy="0 0 0" />
    <parent link="end_link" />
    <child link="gripper_end" />
  </joint>
</robot>"""

if __name__ == "__main__":
    if not SRC.exists():
        raise SystemExit(f"{SRC} not found: run scripts/setup_assets.sh in steel_team/teleoperation "
                         "(or set STEEL_TEAM_TELEOP_DIR)")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = SRC.read_text()
    assert text.rstrip().endswith("</robot>"), "unexpected URDF layout"
    OUT.write_text(text.rstrip()[: -len("</robot>")] + EXTRA + "\n")
    print(f"wrote {OUT}")
