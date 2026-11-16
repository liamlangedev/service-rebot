"""Key input read from the terminal itself, as an alternative to pynput.

pynput needs an X11 session; under Wayland (Ubuntu's default) it sees no keys typed into the terminal. This reader puts
the terminal in cbreak mode (no echo, no line buffering; Ctrl-C still works) and dispatches key names to callbacks:
"right", "left", "up", "down", "esc", or the lower-case character ("s", "g", "h", ...).
The terminal running the script must have focus. Call stop() before any input() prompt, start() again after.
"""
import os
import select
import sys
import termios
import threading
import tty

_ARROWS = {b"A": "up", b"B": "down", b"C": "right", b"D": "left"}


def wayland() -> bool:
    return os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland" or (
        bool(os.environ.get("WAYLAND_DISPLAY")) and os.environ.get("XDG_SESSION_TYPE", "").lower() != "x11")


def pick_backend(name: str) -> str:
    """auto -> terminal under Wayland (or when pynput cannot load), else pynput."""
    if name != "auto":
        return name
    if wayland():
        return "terminal"
    try:
        import pynput  # noqa: F401
    except Exception:
        return "terminal"
    return "pynput"


def parse(data: bytes) -> list[str]:
    """Split a chunk read from the terminal into key names."""
    keys, i = [], 0
    while i < len(data):
        b = data[i:i + 1]
        if b == b"\x1b":
            nxt = data[i + 1:i + 2]
            if nxt in (b"[", b"O") and i + 2 < len(data):
                # CSI / SS3: skip parameters, the final byte names the key
                j = i + 2
                while j < len(data) and not (0x40 <= data[j] <= 0x7E):
                    j += 1
                final = data[j:j + 1]
                if final in _ARROWS:
                    keys.append(_ARROWS[final])
                i = j + 1
                continue
            keys.append("esc")
            i += 1
            continue
        try:
            keys.append(b.decode().lower())
        except UnicodeDecodeError:
            pass
        i += 1
    return keys


class TerminalKeys:
    _instance = None

    @classmethod
    def get(cls) -> "TerminalKeys":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._callbacks = []
        self._thread = None
        self._run = threading.Event()
        self._fd = sys.stdin.fileno() if sys.stdin and sys.stdin.isatty() else None
        self._saved = None

    def add_callback(self, fn):
        """fn(key_name) is called from the reader thread."""
        self._callbacks.append(fn)

    def start(self):
        if self._fd is None:
            print("[keys] stdin is not a terminal: keys unavailable")
            return
        if self._run.is_set():
            return
        self._saved = termios.tcgetattr(self._fd)
        tty.setcbreak(self._fd)
        self._run.set()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop reading and restore the terminal (call before input())."""
        if not self._run.is_set():
            return
        self._run.clear()
        if self._thread is not None:
            self._thread.join(timeout=0.5)
        if self._saved is not None:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
            self._saved = None

    def _loop(self):
        while self._run.is_set():
            r, _, _ = select.select([self._fd], [], [], 0.1)
            if not r:
                continue
            data = os.read(self._fd, 64)
            if data == b"\x1b":  # a lone Esc, or the first byte of an arrow sequence that arrived split
                r, _, _ = select.select([self._fd], [], [], 0.03)
                if r:
                    data += os.read(self._fd, 64)
            for key in parse(data):
                for fn in list(self._callbacks):
                    try:
                        fn(key)
                    except Exception as e:  # never kill the reader
                        print(f"[keys] callback error: {e!r}")


if __name__ == "__main__":  # key test: python -m teleop.term_keys   (Esc quits)
    import time

    done = threading.Event()
    tk = TerminalKeys.get()
    tk.add_callback(lambda k: (print(f"key: {k}", flush=True), done.set() if k == "esc" else None))
    print("press ->, S, G, H ... (Esc quits)")
    tk.start()
    try:
        while not done.is_set():
            time.sleep(0.05)
    finally:
        tk.stop()
