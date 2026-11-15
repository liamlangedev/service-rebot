"""Client for the learned-grasp node (``grasp_policy_node``, ``~/grasp`` Trigger service).

The skill moves the arm to the handoff pose, calls :meth:`run`, and gets the arm back
once the node reports "gripped and lifted" (or a failure). See motion.yaml `learned_grasp`.
"""

from __future__ import annotations

import json
import threading
from typing import Any


class LearnedGraspClient:
    def __init__(self, node: Any, cfg: dict[str, Any]) -> None:
        from rclpy.callback_groups import ReentrantCallbackGroup
        from std_srvs.srv import Trigger

        self._Trigger = Trigger
        service = str(cfg.get("service", "/grasp_policy/grasp"))
        self._timeout = float(cfg.get("timeout_s", 15.0))
        group = ReentrantCallbackGroup()
        self._client = node.create_client(Trigger, service, callback_group=group)
        self._cancel = node.create_client(Trigger, service.rsplit("/", 1)[0] + "/cancel",
                                          callback_group=group)
        self._service = service

    def run(self) -> dict[str, Any]:
        """Blocking. Returns the node's JSON report plus ``success``."""
        if not self._client.wait_for_service(timeout_sec=2.0):
            return {"success": False, "reason": f"{self._service} not available"}
        done = threading.Event()
        future = self._client.call_async(self._Trigger.Request())
        future.add_done_callback(lambda _f: done.set())
        if not done.wait(self._timeout):
            self.cancel()
            return {"success": False, "reason": f"no answer within {self._timeout:.0f} s"}
        res = future.result()
        try:
            info = json.loads(res.message) if res.message else {}
        except ValueError:
            info = {"reason": res.message}
        info["success"] = bool(res.success)
        return info

    def cancel(self) -> None:
        if self._cancel.service_is_ready():
            self._cancel.call_async(self._Trigger.Request())
