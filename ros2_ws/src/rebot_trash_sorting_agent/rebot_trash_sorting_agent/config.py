"""Configuration loading for the agent stack.

Everything the agent needs to be retuned lives in YAML under ``config/``:

    agent.yaml    planner provider/model, step limits, detector settings
    cameras.yaml  capture devices and their table maps (written by calibrate_table.py)
    motion.yaml   MoveIt action, frames, named poses, gripper, grasp knobs
    places.yaml   measured cell geometry (table, walls, bin, workspace)

The node reads these files directly rather than through ROS parameters: they are
nested, they are edited by hand, and the same files are used by the offline tests.
ROS parameters are limited to overrides (``config_dir``, ``dry_run``, ``provider``,
``model``) so the shipped defaults stay in one place.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import re
from typing import Any

import yaml

ENV_SEARCH = (
    "REBOT_AGENT_ENV",
    ".env",
    "ros2_ws/.env",
    "../.env",
)

DEFAULT_ENV_KEYS = ("GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY")


def load_env_files(start: Path | None = None) -> list[Path]:
    """Load ``KEY=VALUE`` files without ever printing values.

    Existing environment variables win, so a shell export always overrides a file.
    """
    start = (start or Path.cwd()).resolve()
    loaded: list[Path] = []
    candidates: list[Path] = []
    explicit = os.environ.get("REBOT_AGENT_ENV")
    if explicit:
        candidates.append(Path(explicit).expanduser())
    for parent in (start, *start.parents):
        for name in ENV_SEARCH[1:]:
            candidates.append(parent / name)
        if (parent / ".git").exists():
            break
    candidates.append(Path.home() / ".config" / "rebot_agent" / ".env")

    for path in candidates:
        try:
            if not path.is_file():
                continue
        except OSError:
            continue
        if path in loaded:
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value:
                os.environ.setdefault(key, value)
        loaded.append(path)
    return loaded


def _expand(value: Any) -> Any:
    """Expand ``~``, ``$VAR``, ``${VAR}`` in strings, recursively."""
    if isinstance(value, str):
        value = os.path.expanduser(os.path.expandvars(value))
        return re.sub(r"\$(?:\{)?(models|runs)(?:\})?", _path_placeholder, value)
    if isinstance(value, list):
        return [_expand(v) for v in value]
    if isinstance(value, dict):
        return {k: _expand(v) for k, v in value.items()}
    return value


def _path_placeholder(match: re.Match[str]) -> str:
    key = match.group(1)
    if key == "models":
        return os.environ.get("REBOT_AGENT_MODELS", str(Path.home() / ".cache" / "rebot_agent" / "models"))
    return os.environ.get("REBOT_AGENT_RUNS", str(Path.home() / ".cache" / "rebot_agent" / "runs"))


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"configuration file missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping at the top level")
    return _expand(data)


@dataclass(frozen=True)
class VLMSettings:
    provider: str
    model: str
    tool_mode: str = "native"
    api_key_env: str = "GEMINI_API_KEY"
    base_url: str | None = None
    thinking_level: str | None = None
    max_output_tokens: int = 2048
    temperature: float = 0.2
    timeout_s: float = 60.0
    retries: int = 2
    max_steps: int = 12
    history_images: int = 2

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "VLMSettings":
        provider = str(data.get("provider", "gemini")).strip().lower()
        if provider not in ("gemini", "openai", "mock"):
            raise ValueError(f"agent.yaml: unknown vlm.provider {provider!r}")
        tool_mode = str(data.get("tool_mode", "native")).strip().lower()
        if tool_mode not in ("native", "json"):
            raise ValueError(f"agent.yaml: unknown vlm.tool_mode {tool_mode!r}")
        thinking = data.get("thinking_level")
        return cls(
            provider=provider,
            model=str(data.get("model", "gemini-3.8-flash")),
            tool_mode=tool_mode,
            api_key_env=str(data.get("api_key_env", "GEMINI_API_KEY")),
            base_url=data.get("base_url") or None,
            thinking_level=str(thinking) if thinking else None,
            max_output_tokens=int(data.get("max_output_tokens", 2048)),
            temperature=float(data.get("temperature", 0.2)),
            timeout_s=float(data.get("timeout_s", 60.0)),
            retries=int(data.get("retries", 2)),
            max_steps=int(data.get("max_steps", 12)),
            history_images=int(data.get("history_images", 2)),
        )


class Config:
    """All four YAML files, resolved and validated on load."""

    def __init__(self, directory: Path, agent: dict, cameras: dict, motion: dict, places: dict,
                 calibration: dict | None = None):
        self.directory = directory
        self._agent = agent
        self._cameras = cameras
        self._motion = motion
        self._places = places
        self._calibration = calibration or {}
        self.vlm = VLMSettings.from_mapping(agent.get("vlm") or {})

    # ------------------------------------------------------------------ loading
    @classmethod
    def load(cls, directory: str | Path | None = None) -> "Config":
        directory = Path(directory).expanduser().resolve() if directory else default_config_dir()
        calibration_path = directory / "calibration.yaml"
        calibration: dict = {}
        if calibration_path.is_file():
            calibration = _read_yaml(calibration_path)
        return cls(
            directory=directory,
            agent=_read_yaml(directory / "agent.yaml"),
            cameras=_read_yaml(directory / "cameras.yaml"),
            motion=_read_yaml(directory / "motion.yaml"),
            places=_read_yaml(directory / "places.yaml"),
            calibration=calibration,
        )

    # ------------------------------------------------------------------ access
    @property
    def agent(self) -> dict[str, Any]:
        return self._agent

    @property
    def cameras(self) -> dict[str, Any]:
        return self._cameras

    @property
    def motion(self) -> dict[str, Any]:
        return self._motion

    @property
    def places(self) -> dict[str, Any]:
        return self._places

    @property
    def perception(self) -> dict[str, Any]:
        return dict(self._agent.get("perception") or {})

    @property
    def run(self) -> dict[str, Any]:
        return dict(self._agent.get("run") or {})

    @property
    def camera_list(self) -> list[dict[str, Any]]:
        cameras = self._cameras.get("cameras") or []
        if not isinstance(cameras, list) or not cameras:
            raise ValueError("cameras.yaml: 'cameras' must be a non-empty list")
        return cameras

    def camera(self, name: str) -> dict[str, Any]:
        for cam in self.camera_list:
            if str(cam.get("name")) == name:
                return cam
        raise KeyError(f"cameras.yaml: no camera named {name!r}")

    def capture_topic(self, name: str) -> str:
        cam = self.camera(name)
        return str(cam.get("topic", f"/{name}_cam")) + "/image_raw"

    def table_map(self, name: str) -> dict[str, Any] | None:
        """Homography for a camera: cameras.yaml first, then the calibration file.

        ``calibrate_table.py`` writes ``calibration.yaml`` instead of editing
        cameras.yaml, so the hand-written comments there survive every recalibration.
        """
        inline = self.camera(name).get("table_map")
        if inline:
            return dict(inline)
        entry = self._calibration.get(name)
        if isinstance(entry, dict) and entry.get("homography"):
            return dict(entry)
        return None

    def table(self) -> dict[str, Any]:
        return dict(self._places.get("table") or {})

    def bin_places(self) -> dict[str, Any]:
        return dict((self._places.get("bin") or {}).get("compartments") or {})

    def api_key(self, env_name: str | None = None) -> str | None:
        return os.environ.get(env_name or self.vlm.api_key_env) or None

    def describe(self) -> dict[str, Any]:
        return {
            "config_dir": str(self.directory),
            "vlm": {"provider": self.vlm.provider, "model": self.vlm.model, "tool_mode": self.vlm.tool_mode},
            "cameras": [str(c.get("name")) for c in self.camera_list],
            "dry_run": bool(self.run.get("dry_run", False)),
        }


def default_config_dir() -> Path:
    """Package share/config, falling back to the source tree."""
    try:
        from ament_index_python.packages import get_package_share_directory

        return Path(get_package_share_directory("rebot_trash_sorting_agent")) / "config"
    except Exception:  # noqa: BLE001 - ament raises different types depending on install state
        return Path(__file__).resolve().parents[1] / "config"
