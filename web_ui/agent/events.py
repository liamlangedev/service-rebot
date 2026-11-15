"""Trace of every decision, on disk and (optionally) on a ROS topic.

One JSON object per line, so a failed demo can be replayed: what the planner saw,
what it chose, what the robot answered, how long it took.
"""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
import json
from pathlib import Path
import threading
import time
from typing import Any, Callable


class EventLog:
    def __init__(self, runs_dir: str | Path | None = None, echo: Callable[[dict[str, Any]], None] | None = None,
                 memory: int = 300, run_name: str | None = None) -> None:
        self._lock = threading.Lock()
        self._echo = echo
        self._tail: deque[dict[str, Any]] = deque(maxlen=memory)
        self._extra: dict[str, Any] = {}
        self.path: Path | None = None
        self.run_dir: Path | None = None
        if runs_dir:
            stamp = time.strftime("%Y%m%d-%H%M%S")
            self.run_dir = Path(runs_dir).expanduser() / (run_name or stamp)
            self.run_dir.mkdir(parents=True, exist_ok=True)
            self.path = self.run_dir / "trace.jsonl"
        self._t0 = time.monotonic()

    # ------------------------------------------------------------------ writing
    def bind(self, **fields: Any) -> None:
        """Attach fields (task, provider, model) to every later event."""
        self._extra.update(fields)

    def emit(self, kind: str, **fields: Any) -> dict[str, Any]:
        event = {
            "ts": round(time.monotonic() - self._t0, 3),
            "utc": datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3],
            "kind": kind,
            **self._extra,
            **fields,
        }
        event = json.loads(json.dumps(event, default=str))
        with self._lock:
            self._tail.append(event)
            if self.path is not None:
                with self.path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(event, separators=(",", ":"), default=str) + "\n")
        if self._echo is not None:
            try:
                self._echo(event)
            except Exception:  # noqa: BLE001 - a broken publisher must not stop the task
                pass
        return event

    def save_image(self, name: str, data: bytes) -> Path | None:
        """Keep the frames the planner actually saw, next to the trace."""
        if self.run_dir is None or not data:
            return None
        path = self.run_dir / name
        path.write_bytes(data)
        return path

    # ------------------------------------------------------------------ reading
    def tail(self, count: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._tail)[-count:]

    def last(self) -> dict[str, Any] | None:
        with self._lock:
            return self._tail[-1] if self._tail else None
