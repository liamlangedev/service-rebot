"""rebot_sim: MuJoCo model of the team's real reBot B601 workspace.

Single source of truth: `real_setup.json` (measurements) + `scene.py` (builder).
Everything else (teleop `--scene real`, tests, exports) builds from these, so
pulling the repo always gives you the latest model.

    from rebot_sim import RealSetupEnv          # robot + scene + helpers (tests, scripts)
    from rebot_sim import build_real_setup_spec # MjSpec, to compile or edit yourself
    from rebot_sim import apply_real_setup      # add the scene to your own reBot MjSpec

CLI: python -m rebot_sim {info,view,render,export}
"""
from .scene import (DEFAULT_CONFIG, SceneInfo, Workspace, apply_real_setup,  # noqa: F401
                    build_real_setup_spec, camera_fovy, load_config, scene_version)
from .env import TOP_DOWN, RealSetupEnv  # noqa: F401

__version__ = scene_version()
