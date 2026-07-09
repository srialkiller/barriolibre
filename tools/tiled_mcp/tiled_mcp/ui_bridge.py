from __future__ import annotations

import ctypes
import os
import subprocess
import time
from pathlib import Path

import uiautomation as ua
import win32con
import win32gui
import win32process


def _find_tiled_pid() -> int | None:
    try:
        out = subprocess.check_output(
            ["tasklist", "/FI", "IMAGENAME eq tiled.exe", "/FO", "CSV", "/NH"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return None
    for line in out.strip().splitlines():
        if "tiled.exe" in line.lower():
            try:
                return int(line.split(",")[1].strip('"'))
            except (IndexError, ValueError):
                pass
    return None


def _find_tiled_window() -> ua.Control | None:
    pid = _find_tiled_pid()
    if not pid:
        return None
    root = ua.GetRootControl()
    for win in root.GetChildren():
        if win.ControlType == ua.ControlType.WindowControl:
            try:
                _, wpid = win32process.GetWindowThreadProcessId(win.NativeWindowHandle)
            except Exception:
                continue
            if wpid == pid:
                return win
    return None


def is_tiled_running() -> bool:
    return _find_tiled_pid() is not None


def get_open_map_filename() -> str | None:
    win = _find_tiled_window()
    if not win:
        return None
    title = win.Name or ""
    if " - Tiled" in title:
        fname = title.rsplit(" - Tiled", 1)[0].strip()
        return fname
    return title or None


def _layer_tree(tiled_win: ua.Control) -> ua.Control | None:
    dock = tiled_win.PaneControl(ClassName="Tiled::LayerDock")
    if not dock.Exists(1, 0.3):
        return None
    tree = dock.TreeControl(ClassName="Tiled::LayerView")
    return tree if tree.Exists(1, 0.3) else None


def get_open_map_state() -> dict:
    win = _find_tiled_window()
    if not win:
        return {"open": False, "running": False, "fileName": None, "layers": [], "currentLayer": None}
    fname = get_open_map_filename()
    layers: list[dict] = []
    current = None
    tree = _layer_tree(win)
    if tree:
        for item in tree.GetChildren():
            name = item.Name
            if not name:
                continue
            pat = item.GetSelectionItemPattern()
            selected = bool(pat and pat.IsSelected)
            layers.append({"name": name, "selected": selected})
            if selected and not current:
                current = name
    return {
        "open": True,
        "running": True,
        "fileName": fname,
        "currentLayer": current,
        "layers": layers,
    }


def focus_layer(layer_name: str) -> dict:
    win = _find_tiled_window()
    if not win:
        return {"ok": False, "error": "Tiled is not running"}
    tree = _layer_tree(win)
    if not tree:
        return {"ok": False, "error": "Layer panel not found in Tiled UI"}
    for item in tree.GetChildren():
        if item.Name == layer_name:
            pat = item.GetSelectionItemPattern()
            if pat:
                pat.Select()
                time.sleep(0.3)
                return {"ok": True, "layer": layer_name}
            item.Click()
            time.sleep(0.3)
            return {"ok": True, "layer": layer_name, "method": "click"}
    visible = [i.Name for i in tree.GetChildren() if i.Name]
    return {"ok": False, "error": f"Layer '{layer_name}' not found", "visibleLayers": visible}


def _send_ctrl_s(hwnd: int) -> None:
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.4)
    User32 = ctypes.windll.User32
    User32.keybd_event(0x11, 0, 0, 0)
    User32.keybd_event(0x53, 0, 0, 0)
    User32.keybd_event(0x53, 0, 0x0002, 0)
    User32.keybd_event(0x11, 0, 0x0002, 0)


def save_in_editor() -> dict:
    win = _find_tiled_window()
    if not win:
        return {"ok": False, "error": "Tiled is not running"}
    hwnd = win.NativeWindowHandle
    _send_ctrl_s(hwnd)
    time.sleep(1.0)
    return {"ok": True, "action": "Ctrl+S sent to Tiled"}


def open_in_editor(tmx_path: str, tiled_exe: str) -> dict:
    proc = subprocess.Popen([tiled_exe, tmx_path])
    time.sleep(2.0)
    return {"launched": True, "pid": proc.pid, "tmx_path": tmx_path, "tiled_exe": tiled_exe}
