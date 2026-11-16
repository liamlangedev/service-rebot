"""Issue log for the operator dashboard: problems the guests must not see (failed or stuck hand-outs, items that ran out,
robot or assistant errors, staff requests from the concierge).

Kept in memory and persisted to logs/issues.json (+ logs/snapshots/<id>.jpg, the front camera when it happened), so a
restart of the web UI does not lose them. Thread-safe; on_change(event, issue) is called for every new or updated issue.
"""
import json
import threading
import time
from pathlib import Path

SEVERITIES = ("error", "warning", "info")
STATES = ("open", "acknowledged", "resolved")


class IssueLog:
    def __init__(self, directory: Path, on_change=None, keep: int = 300):
        self.dir = Path(directory)
        self.snap_dir = self.dir / "snapshots"
        self.snap_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / "issues.json"
        self.on_change = on_change
        self.keep = keep
        self._lock = threading.Lock()
        self._issues: list[dict] = []
        if self.file.is_file():
            try:
                self._issues = json.loads(self.file.read_text())[-keep:]
            except (json.JSONDecodeError, OSError):
                self._issues = []

    def _save(self):
        tmp = self.file.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._issues, indent=1))
        tmp.replace(self.file)

    def add(self, kind: str, severity: str, message: str, item: str | None = None, reason: str = "",
            suggestion: str = "", request: str = "", snapshot: bytes | None = None, dedupe_s: float = 0.0) -> dict:
        """New issue. dedupe_s > 0: an open issue of the same kind+item within that time is updated instead."""
        severity = severity if severity in SEVERITIES else "warning"
        now = time.time()
        with self._lock:
            if dedupe_s > 0:
                for old in reversed(self._issues):
                    if (old["kind"], old.get("item")) == (kind, item) and old["status"] == "open" \
                            and now - old["last"] < dedupe_s:
                        old["count"] += 1
                        old["last"] = now
                        old["reason"] = reason or old["reason"]
                        self._save()
                        issue = dict(old)
                        break
                else:
                    issue = None
                if issue is not None:
                    self._notify("issue_update", issue)
                    return issue
            iid = f"{int(now * 1000)}"
            if snapshot:
                (self.snap_dir / f"{iid}.jpg").write_bytes(snapshot)
            issue = {"id": iid, "t": now, "last": now, "count": 1, "kind": kind, "severity": severity,
                     "message": message, "item": item, "reason": reason, "suggestion": suggestion,
                     "request": request, "snapshot": bool(snapshot), "status": "open", "note": ""}
            self._issues = (self._issues + [issue])[-self.keep:]
            self._save()
            issue = dict(issue)
        self._notify("issue", issue)
        return issue

    def set_status(self, iid: str, status: str, note: str = "") -> dict | None:
        if status not in STATES:
            raise ValueError(f"status must be one of {STATES}")
        with self._lock:
            for it in self._issues:
                if it["id"] == iid:
                    it["status"], it["note"], it["changed"] = status, note or it.get("note", ""), time.time()
                    self._save()
                    issue = dict(it)
                    break
            else:
                return None
        self._notify("issue_update", issue)
        return issue

    def resolve_kind(self, kind: str, note: str = "") -> None:
        """Resolve all open issues of one kind (e.g. robot_offline once the robot is back)."""
        for it in self.list():
            if it["kind"] == kind and it["status"] != "resolved":
                self.set_status(it["id"], "resolved", note)

    def list(self) -> list[dict]:
        with self._lock:
            return [dict(i) for i in reversed(self._issues)]  # newest first

    def counts(self) -> dict:
        out = {s: 0 for s in SEVERITIES}
        for it in self.list():
            if it["status"] == "open":
                out[it["severity"]] += 1
        return out

    def snapshot_path(self, iid: str) -> Path | None:
        p = self.snap_dir / f"{iid}.jpg"
        return p if p.is_file() else None

    def _notify(self, event: str, issue: dict):
        if self.on_change:
            try:
                self.on_change(event, issue)
            except Exception as e:  # noqa: BLE001
                print(f"[issues] notify failed: {e!r}")
