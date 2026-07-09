from __future__ import annotations

import re
import xml.etree.ElementTree as ET

from tiled_mcp.server import MAPS_DIR
import tiled_mcp.tmx_io as io_mod
import export_layout as ex
import generate_tileset as gt


def _load(map_id: str) -> tuple:
    map_path = io_mod._tmx_path(map_id)
    text = map_path.read_text(encoding="utf-8")
    root = ET.fromstring(text)
    return map_path, text, root


def _save(map_path, text: str) -> None:
    map_path.write_text(text, encoding="utf-8")


def _reverse_maps(map_path, root) -> tuple[dict, dict, dict, dict]:
    gid_to_tile_id, gid_to_prop_id = ex.parse_tileset_sources(map_path, root)
    tile_id_to_gid: dict[str, int] = {}
    for gid, tid in gid_to_tile_id.items():
        tile_id_to_gid.setdefault(tid, gid)
    prop_id_to_gid: dict[str, int] = {}
    for gid, pid in gid_to_prop_id.items():
        prop_id_to_gid.setdefault(pid, gid)
    return tile_id_to_gid, prop_id_to_gid, gid_to_tile_id, gid_to_prop_id


def _layer_data_regex(layer_name: str):
    return re.compile(
        r'(<layer[^>]*name="' + re.escape(layer_name) + r'"[^>]*>.*?<data[^>]*>)([^<]*)(</data>)',
        re.DOTALL,
    )


def _replace_layer_data(text: str, layer_name: str, new_gids: list[int]) -> str:
    encoded = gt.encode_layer_data(new_gids)
    m = _layer_data_regex(layer_name).search(text)
    if not m:
        raise ValueError(f"Could not locate <data> for tile layer '{layer_name}'")
    return text[: m.start(2)] + encoded + text[m.end(2) :]


def _layer_gids(root: ET.Element, layer_name: str) -> list[int]:
    layer = next((l for l in root.findall("layer") if l.attrib.get("name") == layer_name), None)
    if layer is None:
        avail = [l.attrib.get("name") for l in root.findall("layer")]
        raise ValueError(f"Tile layer '{layer_name}' not found. Available: {avail}")
    return ex.parse_layer_grid(layer)


def _flat(grid: list[list[int]]) -> list[int]:
    return [gid for row in grid for gid in row]


def _bounds(root: ET.Element) -> tuple[int, int]:
    return int(root.attrib["width"]), int(root.attrib["height"])


def set_tile(map_id: str, layer: str, col: int, row: int, tile_id: str) -> dict:
    map_path, text, root = _load(map_id)
    w, h = _bounds(root)
    if not (0 <= col < w and 0 <= row < h):
        raise ValueError(f"Cell ({col},{row}) out of bounds for {w}x{h} map")

    tile_id_to_gid, _, _, _ = _reverse_maps(map_path, root)
    if tile_id in ("", "empty", "none", "null"):
        gid = 0
    else:
        if tile_id not in tile_id_to_gid:
            raise KeyError(
                f"Unknown tile_id '{tile_id}'. Known: {sorted(tile_id_to_gid)[:10]}..."
            )
        gid = tile_id_to_gid[tile_id]

    grid = _layer_gids(root, layer)
    prev = grid[row][col] & ex.GID_MASK
    grid[row][col] = gid
    text = _replace_layer_data(text, layer, _flat(grid))
    _save(map_path, text)
    return {
        "map_id": map_id,
        "layer": layer,
        "col": col,
        "row": row,
        "prev_gid": prev,
        "new_gid": gid,
        "tile_id": tile_id or "(empty)",
        "saved": True,
    }


def fill_region(
    map_id: str,
    layer: str,
    col_start: int,
    col_end: int,
    row_start: int,
    row_end: int,
    tile_id: str,
) -> dict:
    map_path, text, root = _load(map_id)
    w, h = _bounds(root)
    c0, c1 = sorted((col_start, col_end))
    r0, r1 = sorted((row_start, row_end))
    if not (0 <= c0 < w and 0 <= c1 < w and 0 <= r0 < h and 0 <= r1 < h):
        raise ValueError(f"Region cols[{c0},{c1}] rows[{r0},{r1}] out of bounds for {w}x{h} map")

    tile_id_to_gid, _, _, _ = _reverse_maps(map_path, root)
    if tile_id in ("", "empty", "none", "null"):
        gid = 0
    else:
        if tile_id not in tile_id_to_gid:
            raise KeyError(f"Unknown tile_id '{tile_id}'")
        gid = tile_id_to_gid[tile_id]

    grid = _layer_gids(root, layer)
    changed = 0
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if (grid[r][c] & ex.GID_MASK) != gid:
                grid[r][c] = gid
                changed += 1
    text = _replace_layer_data(text, layer, _flat(grid))
    _save(map_path, text)
    return {
        "map_id": map_id,
        "layer": layer,
        "region": [c0, c1, r0, r1],
        "tile_id": tile_id or "(empty)",
        "cells_in_region": (c1 - c0 + 1) * (r1 - r0 + 1),
        "cells_changed": changed,
        "saved": True,
    }


def _prop_dims(prop_id: str, root: ET.Element, map_path) -> tuple[float, float] | None:
    for ts in root.findall("tileset"):
        source = ts.attrib.get("source")
        if not source:
            continue
        ts_path = (map_path.parent / source).resolve()
        if not ts_path.exists():
            continue
        ts_root = ET.parse(ts_path).getroot()
        for tile in ts_root.findall("tile"):
            pid = None
            props = tile.find("properties")
            if props is not None:
                for p in props.findall("property"):
                    if p.attrib.get("name") == "prop_id":
                        pid = p.attrib.get("value")
            if pid == prop_id:
                img = tile.find("image")
                if img is not None:
                    return float(img.attrib["width"]), float(img.attrib["height"])
    return None


def _grid_to_obj_xy(col: float, row: float, tile_height: float) -> tuple[float, float]:
    return (col + 0.5) * tile_height, (row + 0.5) * tile_height


def _props_objectgroup_span(text: str) -> tuple[int, int]:
    m = re.search(r'(<objectgroup[^>]*name="props"[^>]*>)(.*?)(</objectgroup>)', text, re.DOTALL)
    if not m:
        raise ValueError("No <objectgroup name=\"props\"> found in map")
    return m.start(3), m.end(3)


def _next_object_id(text: str) -> int:
    m = re.search(r'nextobjectid="(\d+)"', text)
    if not m:
        raise ValueError("No nextobjectid attribute on <map>")
    return int(m.group(1))


def _bump_nextobjectid(text: str, new_id: int) -> str:
    return re.sub(r'nextobjectid="\d+"', f'nextobjectid="{new_id}"', text, count=1)


def add_prop(
    map_id: str,
    prop_id: str,
    col: float,
    row: float,
    width_px: float | None = None,
    height_px: float | None = None,
) -> dict:
    map_path, text, root = _load(map_id)
    _, prop_id_to_gid, _, _ = _reverse_maps(map_path, root)
    if prop_id not in prop_id_to_gid:
        raise KeyError(f"Unknown prop_id '{prop_id}'. Known: {sorted(prop_id_to_gid)}")
    gid = prop_id_to_gid[prop_id]

    if width_px is None or height_px is None:
        dims = _prop_dims(prop_id, root, map_path)
        if dims is None:
            raise ValueError(f"Could not determine default size for prop '{prop_id}' from tileset")
        if width_px is None:
            width_px = dims[0]
        if height_px is None:
            height_px = dims[1]

    tile_height = float(root.attrib["tileheight"])
    x, y = _grid_to_obj_xy(col, row, tile_height)

    new_id = _next_object_id(text)
    obj_line = f'\n  <object id="{new_id}" gid="{gid}" x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(width_px)}" height="{_fmt(height_px)}"/>'

    close_start, _ = _props_objectgroup_span(text)
    new_text = text[:close_start] + obj_line + "\n " + text[close_start:]
    new_text = _bump_nextobjectid(new_text, new_id + 1)
    _save(map_path, new_text)
    return {
        "map_id": map_id,
        "object_id": new_id,
        "prop_id": prop_id,
        "gid": gid,
        "col": col,
        "row": row,
        "x": _fmt(x),
        "y": _fmt(y),
        "width_px": _fmt(width_px),
        "height_px": _fmt(height_px),
        "saved": True,
    }


def _fmt(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s else "0"


def _find_object_line(text: str, object_id: int) -> tuple[int, int, str] | None:
    pattern = re.compile(rf'(<object id="{object_id}"[^>]*?/>)', re.DOTALL)
    m = pattern.search(text)
    if m:
        return m.start(1), m.end(1), m.group(1)
    pattern2 = re.compile(rf'(<object id="{object_id}".*?</object>)', re.DOTALL)
    m = pattern2.search(text)
    if m:
        return m.start(1), m.end(1), m.group(1)
    return None


def move_prop(map_id: str, object_id: int, col: float, row: float) -> dict:
    map_path, text, root = _load(map_id)
    found = _find_object_line(text, object_id)
    if not found:
        raise KeyError(f"Object id={object_id} not found in map")
    start, end, line = found

    tile_height = float(root.attrib["tileheight"])
    x, y = _grid_to_obj_xy(col, row, tile_height)
    new_line = re.sub(r'\sx="[^"]*"', f' x="{_fmt(x)}"', line, count=1)
    new_line = re.sub(r'\sy="[^"]*"', f' y="{_fmt(y)}"', new_line, count=1)
    _save(map_path, text[:start] + new_line + text[end:])
    return {
        "map_id": map_id,
        "object_id": object_id,
        "col": col,
        "row": row,
        "x": _fmt(x),
        "y": _fmt(y),
        "saved": True,
    }


def delete_prop(map_id: str, object_id: int) -> dict:
    map_path, text, root = _load(map_id)
    found = _find_object_line(text, object_id)
    if not found:
        raise KeyError(f"Object id={object_id} not found in map")
    start, end, line = found

    line_start = text.rfind("\n", 0, start)
    if text[line_start:start].strip() == "" and line_start != -1:
        new_text = text[:line_start] + text[end:]
    else:
        trailing = text[end:end + 1]
        new_text = text[:start] + text[end + (1 if trailing == "\n" else 0):]
    _save(map_path, new_text)
    return {"map_id": map_id, "object_id": object_id, "deleted": True, "removed_line": line.strip()}


def resize_map(map_id: str, width: int, height: int) -> dict:
    map_path, text, root = _load(map_id)
    old_w, old_h = _bounds(root)
    if width == old_w and height == old_h:
        return {"map_id": map_id, "width": width, "height": height, "changed": False}

    text = re.sub(r'\swidth="\d+"', f' width="{width}"', text, count=1)
    text = re.sub(r'\sheight="\d+"', f' height="{height}"', text, count=1)

    for layer in root.findall("layer"):
        name = layer.attrib.get("name", "")
        grid = ex.parse_layer_grid(layer)
        new_grid: list[list[int]] = []
        for r in range(height):
            src = grid[r] if r < len(grid) else []
            row = [src[c] if c < len(src) else 0 for c in range(width)]
            new_grid.append(row)
        text = _replace_layer_data(text, name, _flat(new_grid))
        text = re.sub(
            r'(<layer[^>]*name="' + re.escape(name) + r'"[^>]*?)\swidth="\d+"',
            rf'\1 width="{width}"',
            text,
            count=1,
        )
        text = re.sub(
            r'(<layer[^>]*name="' + re.escape(name) + r'"[^>]*?)\sheight="\d+"',
            rf'\1 height="{height}"',
            text,
            count=1,
        )

    _save(map_path, text)
    return {
        "map_id": map_id,
        "prev_size": [old_w, old_h],
        "new_size": [width, height],
        "layers_resized": len(root.findall("layer")),
        "changed": True,
    }
