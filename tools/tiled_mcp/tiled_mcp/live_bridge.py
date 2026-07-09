from __future__ import annotations

import os
import time
from pathlib import Path

import tiled_mcp.tmx_io as io_mod


class FileWatcher:
    """Tracks .tmx file modification times to detect when Tiled saves.

    The MCP records the mtime after each edit (mark_clean). When the user
    edits in Tiled and saves (Ctrl+S), the mtime changes and check_changed
    reports it.
    """

    def __init__(self):
        self._clean_mtimes: dict[str, float] = {}

    def _tmx_path(self, map_id: str) -> Path:
        return io_mod._tmx_path(map_id)

    def _current_mtime(self, map_id: str) -> float:
        return os.stat(self._tmx_path(map_id)).st_mtime

    def mark_clean(self, map_id: str) -> dict:
        p = self._tmx_path(map_id)
        mtime = os.stat(p).st_mtime
        self._clean_mtimes[map_id] = mtime
        return {"map_id": map_id, "marked_clean": True, "mtime": mtime}

    def check_changed(self, map_id: str) -> dict:
        p = self._tmx_path(map_id)
        current = os.stat(p).st_mtime
        known = self._clean_mtimes.get(map_id)
        if known is None:
            layout_path = p.parent / "layout.json"
            if layout_path.exists():
                layout_mtime = os.stat(layout_path).st_mtime
                changed = current > layout_mtime
                self._clean_mtimes[map_id] = current
                return {
                    "map_id": map_id,
                    "changed": changed,
                    "mtime": current,
                    "layout_mtime": layout_mtime,
                    "note": "compared with layout.json (no in-memory baseline)",
                }
            self._clean_mtimes[map_id] = current
            return {"map_id": map_id, "changed": False, "mtime": current, "note": "first check (baseline set, no layout.json to compare)"}
        changed = current != known
        return {"map_id": map_id, "changed": changed, "mtime": current, "prev_mtime": known}

    def sync_from_editor(
        self,
        map_id: str,
        save: bool = True,
        auto_export: bool = False,
        auto_validate: bool = False,
    ) -> dict:
        import tiled_mcp.ui_bridge as ui

        result: dict = {"map_id": map_id, "steps": []}

        if save:
            if not ui.is_tiled_running():
                return {**result, "ok": False, "error": "Tiled is not running; cannot save"}
            save_res = ui.save_in_editor()
            result["steps"].append({"step": "save", "result": save_res})
            time.sleep(0.5)

        changed = self.check_changed(map_id)
        result["steps"].append({"step": "check_changed", "result": changed})
        result["changed"] = changed["changed"]

        if changed["changed"]:
            self.mark_clean(map_id)
            if auto_export:
                import tiled_mcp.runners as rn

                export_res = rn.run_export_map(map_id)
                result["steps"].append({"step": "export", "result": export_res})
            if auto_validate:
                import tiled_mcp.runners as rn

                val_res = rn.run_validate_map(map_id)
                result["steps"].append({"step": "validate", "result": val_res})

        result["ok"] = True
        return result

    def health(self) -> dict:
        return {
            "tracked_maps": list(self._clean_mtimes.keys()),
            "mechanism": "file_watcher (mtime-based, no scripting required)",
        }


_watcher: FileWatcher | None = None


def get_watcher() -> FileWatcher:
    global _watcher
    if _watcher is None:
        _watcher = FileWatcher()
    return _watcher
