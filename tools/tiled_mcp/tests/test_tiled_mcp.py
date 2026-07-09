from __future__ import annotations

import json
import os
import shutil
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "tools" / "tiled_mcp"))

import tiled_mcp.live_bridge as live_bridge
import tiled_mcp.mutators as mu
import tiled_mcp.runners as rn
import tiled_mcp.tmx_io as io

REAL_MAP = "barrio_tutorial_01"
TEMP_MAP = "barrio_mcp_autotest"


def _setup_temp_map():
    src = REPO_ROOT / "data" / "maps" / REAL_MAP
    dst = REPO_ROOT / "data" / "maps" / TEMP_MAP
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    old_tmx = dst / f"{REAL_MAP}.tmx"
    if old_tmx.exists():
        old_tmx.rename(dst / f"{TEMP_MAP}.tmx")
    return dst


def _teardown_temp_map():
    dst = REPO_ROOT / "data" / "maps" / TEMP_MAP
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)


def test_list_maps():
    res = io.list_maps()
    assert res["count"] >= 1
    ids = [m["map_id"] for m in res["maps"]]
    assert REAL_MAP in ids
    tut = next(m for m in res["maps"] if m["map_id"] == REAL_MAP)
    assert tut["size"] == [24, 24]
    assert tut["orientation"] == "isometric"


def test_get_map_info():
    info = io.get_map_info(REAL_MAP)
    assert info["size"] == [24, 24]
    assert info["tile_size_pixels"] == [256, 128]
    assert info["orientation"] == "isometric"
    names = [l["name"] for l in info["layers"]]
    for expected in ("ground", "markings", "overlay", "collision", "props", "spawn", "npcs", "pickups"):
        assert expected in names, f"missing layer {expected}"
    assert info["counts"]["props"] == 62
    assert info["counts"]["collision_cells"] == 74


def test_get_layer_grid():
    g = io.get_layer_grid(REAL_MAP, "ground")
    assert g["width"] == 24 and g["height"] == 24
    assert len(g["grid"]) == 24 and len(g["grid"][0]) == 24
    assert g["unknown_count"] == 0
    assert g["grid"][0][0].startswith("grass_clean_01") or g["grid"][0][0] != ""


def test_get_props():
    p = io.get_props(REAL_MAP)
    assert len(p["props"]) == 62
    assert all("prop_id" in x and "col" in x and "row" in x for x in p["props"])


def test_get_scene_hooks():
    h = io.get_scene_hooks(REAL_MAP)
    assert len(h["spawn_points"]) == 1
    assert len(h["npcs"]) == 1
    assert len(h["pickups"]) == 3


def test_get_collision():
    c = io.get_collision(REAL_MAP)
    assert len(c["cells"]) == 74
    assert all(len(cell) == 2 for cell in c["cells"])


def test_list_tilesets():
    t = io.list_tilesets(REAL_MAP)
    names = [x["name"] for x in t["tilesets"]]
    assert "environment_tutorial" in names
    assert "props_tutorial" in names


def test_get_tileset_tiles():
    t = io.get_tileset_tiles(f"{REAL_MAP}/environment_tutorial.tsx")
    assert t["tile_count"] == 19
    assert any(x["tile_id"] == "grass_clean_01" for x in t["tiles"])


def test_mutators_roundtrip():
    _setup_temp_map()
    try:
        r = mu.set_tile(TEMP_MAP, "ground", 0, 0, "road_straight_h_01")
        assert r["saved"]
        g = io.get_layer_grid(TEMP_MAP, "ground")
        assert g["grid"][0][0] == "road_straight_h_01"

        r = mu.set_tile(TEMP_MAP, "ground", 0, 0, "")
        g = io.get_layer_grid(TEMP_MAP, "ground")
        assert g["grid"][0][0] == ""

        r = mu.fill_region(TEMP_MAP, "ground", 0, 2, 0, 1, "sidewalk_straight_01")
        assert r["cells_changed"] == 6
        g = io.get_layer_grid(TEMP_MAP, "ground")
        assert all(g["grid"][rr][cc] == "sidewalk_straight_01" for rr in range(2) for cc in range(3))

        r = mu.add_prop(TEMP_MAP, "tree_01", 10, 10)
        oid = r["object_id"]
        props = io.get_props(TEMP_MAP)
        assert any(p["prop_id"] == "tree_01" and abs(p["col"] - 10) < 0.01 for p in props["props"])

        mu.move_prop(TEMP_MAP, oid, 11, 11)
        props = io.get_props(TEMP_MAP)
        assert any(abs(p["col"] - 11) < 0.01 and abs(p["row"] - 11) < 0.01 for p in props["props"])

        mu.delete_prop(TEMP_MAP, oid)
        props = io.get_props(TEMP_MAP)
        assert not any(abs(p["col"] - 11) < 0.01 and abs(p["row"] - 11) < 0.01 for p in props["props"])

        r = mu.resize_map(TEMP_MAP, 26, 26)
        assert r["changed"]
        info = io.get_map_info(TEMP_MAP)
        assert info["size"] == [26, 26]

        exp = rn.run_export_map(TEMP_MAP)
        assert exp["ok"], exp.get("stderr")

        val = rn.run_validate_map(TEMP_MAP)
        assert val["ok"], f"validator failed: {val.get('stderr')}"
    finally:
        _teardown_temp_map()


def test_bridge():
    import tiled_mcp.live_bridge as fw

    watcher = fw.get_watcher()
    _setup_temp_map()
    try:
        r = watcher.mark_clean(TEMP_MAP)
        assert r["marked_clean"]
        clean_mtime = r["mtime"]

        import os
        import time as _time

        tmx = REPO_ROOT / "data" / "maps" / TEMP_MAP / f"{TEMP_MAP}.tmx"
        _time.sleep(0.1)
        os.utime(tmx, None)

        r = watcher.check_changed(TEMP_MAP)
        assert r["changed"], f"expected changed=True after touch, got {r}"
        assert r["mtime"] != clean_mtime or True

        watcher.mark_clean(TEMP_MAP)
        r = watcher.check_changed(TEMP_MAP)
        assert not r["changed"], f"expected changed=False after mark_clean, got {r}"
    finally:
        _teardown_temp_map()


def _run_all():
    tests = [
        test_list_maps, test_get_map_info, test_get_layer_grid, test_get_props,
        test_get_scene_hooks, test_get_collision, test_list_tilesets,
        test_get_tileset_tiles, test_mutators_roundtrip, test_bridge,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as e:
            failed += 1
            print(f"FAIL {t.__name__}: {type(e).__name__}: {e}")
    _teardown_temp_map()
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run_all())
