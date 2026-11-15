"""Single-key input from the terminal without Enter (Linux/macOS).

    with Keys() as keys:
        k = keys.poll()   # 'a', ' ', 'q', ... or None

Without a TTY (piped stdin, CI) `enabled` is False and poll() always returns None.
"""

from __future__ import annotations

import select
import sys


class Keys:
    def __init__(self) -> None:
        self.enabled = sys.stdin.isatty()
        self._old = None

    def __enter__(self) -> "Keys":
        if self.enabled:
            import termios
            import tty
            self._old = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, *exc) -> None:
        if self._old is not None:
            import termios
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old)

    def poll(self) -> str | None:
        if not self.enabled:
            return None
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1).lower()
        return None
