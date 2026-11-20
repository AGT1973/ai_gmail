import ctypes
from ctypes import wintypes
import psutil

user32 = ctypes.windll.user32

def enum_windows():
    windows = []
    def enum_proc(hwnd, lParam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                try:
                    p = psutil.Process(pid.value)
                    pname = p.name()
                except Exception:
                    pname = "unknown"
                windows.append((pid.value, pname, buff.value))
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(enum_proc), 0)
    return windows

for pid, name, title in enum_windows():
    print(f"PID: {pid:6d} | Name: {name:15s} | Title: {title}")
