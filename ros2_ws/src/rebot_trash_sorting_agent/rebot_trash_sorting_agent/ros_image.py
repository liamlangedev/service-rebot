"""Pure-NumPy ``sensor_msgs/Image`` <-> BGR ``ndarray`` helpers.

ROS Jazzy's system ``cv_bridge`` is compiled against NumPy 1.x and segfaults
when NumPy 2.x is installed in ``~/.local``. Converting ``bgr8``/``rgb8``
buffers directly with NumPy avoids that ABI mismatch completely.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def imgmsg_to_bgr(msg: Any) -> np.ndarray:
    enc = str(msg.encoding or "bgr8").lower()
    h, w = int(msg.height), int(msg.width)
    buf = np.frombuffer(msg.data, dtype=np.uint8)
    if enc in ("bgr8", "rgb8"):
        row_bytes = int(msg.step) or w * 3
        arr = buf.reshape((h, row_bytes))[:, : w * 3].reshape((h, w, 3))
        return arr[:, :, ::-1].copy() if enc == "rgb8" else arr.copy()
    if enc in ("bgra8", "rgba8"):
        row_bytes = int(msg.step) or w * 4
        arr = buf.reshape((h, row_bytes))[:, : w * 4].reshape((h, w, 4))
        return arr[:, :, 2::-1].copy() if enc == "rgba8" else arr[:, :, :3].copy()
    if enc == "mono8":
        row_bytes = int(msg.step) or w
        arr = buf.reshape((h, row_bytes))[:, :w]
        return np.repeat(arr[:, :, None], 3, axis=2)
    raise ValueError(f"unsupported Image encoding {msg.encoding!r}")


def bgr_to_imgmsg(bgr: np.ndarray, *, stamp: Any = None, frame_id: str = "") -> Any:
    from sensor_msgs.msg import Image

    arr = np.ascontiguousarray(bgr, dtype=np.uint8)
    msg = Image()
    if stamp is not None:
        msg.header.stamp = stamp
    if frame_id:
        msg.header.frame_id = frame_id
    msg.height = int(arr.shape[0])
    msg.width = int(arr.shape[1])
    msg.encoding = "bgr8"
    msg.is_bigendian = 0
    msg.step = int(arr.shape[1] * 3)
    msg.data = arr.tobytes()
    return msg
