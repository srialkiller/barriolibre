from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from tiled_mcp.server import MAPS_DIR, REPO_ROOT, TILED_EXPORT_DIR

if str(TILED_EXPORT_DIR) not in sys.path:
    sys.path.insert(0, str(TILED_EXPORT_DIR))

import export_layout as ex


GID_MASK = ex.GID_MASK


def _map_dir(map_id: str) -> Path:
    d = MAPS_DIR / map_id
    if not d.is_dir():
        raise FileNotFoundError(f"Map directory not found: {d}")
    return d


def _tmx_path(map_id: str) -> Path:
    d = _map_dir(map_id)
    conventional = d / f"{map_id}.tmx"
    if conventional.exists():
        return conventional
    tmxs = list(d.glob("*.tmx"))
    if not tmxs:
        raise FileNotFoundError(f"No .tmx file in {d}")
    if len(tmxs) > 1:
        raise ValueError(f"Multiple .tmx files in {d}; expected {conventional.name}")
    return tmxs[0]


def _parse_root(map_id: str) -> tuple[Path, ET.Element]:
    p = _tmx_path(map_id)
    return p, ET.parse(p).getroot()


def _tilesets_from_map(root: ET.Element, map_path: Path) -> list[dict]:
    out = []
    for ts in root.findall("tileset"):
        firstgid = int(ts.attrib["firstgid"])
        source = ts.attrib.get("source")
        abs_path = (map_path.parent / source).resolve() if source else None
        tile_count = None
        name = None
        if abs_path and abs_path.exists():
            ts_root = ET.parse(abs_path).getroot()
            name = ts_root.attrib.get("name")
            tile_count = len(ts_root.findall("tile"))
        out.append(
            {
                "firstgid": firstgid,
                "source": source,
                "abs_path": str(abs_path) if abs_path else None,
                "name": name,
                "tile_count": tile_count,
            }
        )
    return out


def list_maps() -> dict:
    maps = []
    if not MAPS_DIR.exists():
        return {"maps": [], "maps_dir": str(MAPS_DIR)}
    for d in sorted(p for p in MAPS_DIR.iterdir() if p.is_dir()):
        tmx = None
        conventional = d / f"{d.name}.tmx"
        if conventional.exists():
            tmx = conventional
        else:
            tmxs = list(d.glob("*.tmx"))
            tmx = tmxs[0] if len(tmxs) == 1 else None
        entry = {"map_id": d.name, "has_tmx": tmx is not None}
        if tmx:
            entry["tmx_path"] = str(tmx)
            try:
                root = ET.parse(tmx).getroot()
                entry["size"] = [int(root.attrib["width"]), int(root.attrib["height"])]
                entry["orientation"] = root.attrib.get("orientation")
                entry["tilesets"] = len(root.findall("tileset"))
                entry["tile_layers"] = len(root.findall("layer"))
                entry["object_layers"] = len(root.findall("objectgroup"))
            except ET.ParseError as e:
                entry["error"] = f"parse error: {e}"
        maps.append(entry)
    return {"maps": maps, "maps_dir": str(MAPS_DIR), "count": len(maps)}


def get_map_info(map_id: str) -> dict:
    map_path, root = _parse_root(map_id)
    layers = []
    for layer in root.findall("layer"):
        layers.append(
            {
                "name": layer.attrib.get("name"),
                "type": "tile",
                "visible": layer.attrib.get("visible", "1") != "0",
                "width": int(layer.attrib["width"]) if "width" in layer.attrib else None,
                "height": int(layer.attrib["height"]) if "height" in layer.attrib else None,
                "opacity": float(layer.attrib.get("opacity", "1")),
            }
        )
    for group in root.findall("objectgroup"):
        layers.append(
            {
                "name": group.attrib.get("name"),
                "type": "object",
                "visible": group.attrib.get("visible", "1") != "0",
                "object_count": len(group.findall("object")),
            }
        )

    gid_to_tile_id, gid_to_prop_id = ex.parse_tileset_sources(map_path, root)

    prop_layer = next(
        (g for g in root.findall("objectgroup") if g.attrib.get("name") == ex.PROPS_LAYER_NAME),
        None,
    )
    props_count = len(prop_layer.findall("object")) if prop_layer is not None else 0

    spawn_count = npc_count = pickup_count = 0
    for g in root.findall("objectgroup"):
        n = g.attrib.get("name")
        if n == ex.SPAWN_LAYER_NAME:
            spawn_count = len(g.findall("object"))
        elif n == ex.NPC_LAYER_NAME:
            npc_count = len(g.findall("object"))
        elif n == ex.PICKUP_LAYER_NAME:
            pickup_count = len(g.findall("object"))

    collision_payload = ex.export_collision(root, map_id)
    collision_cells = len(collision_payload["cells"]) if collision_payload else 0

    return {
        "map_id": map_id,
        "tmx_path": str(map_path),
        "size": [int(root.attrib["width"]), int(root.attrib["height"])],
        "tile_size_pixels": [int(root.attrib["tilewidth"]), int(root.attrib["tileheight"])],
        "orientation": root.attrib.get("orientation"),
        "renderorder": root.attrib.get("renderorder"),
        "infinite": root.attrib.get("infinite", "0") == "1",
        "tiledversion": root.attrib.get("tiledversion"),
        "layers": layers,
        "tilesets": _tilesets_from_map(root, map_path),
        "known_tile_ids": len(gid_to_tile_id),
        "known_prop_ids": len(gid_to_prop_id),
        "counts": {
            "props": props_count,
            "spawn_points": spawn_count,
            "npcs": npc_count,
            "pickups": pickup_count,
            "collision_cells": collision_cells,
        },
    }


def get_layer_grid(map_id: str, layer: str) -> dict:
    map_path, root = _parse_root(map_id)
    gid_to_tile_id, _ = ex.parse_tileset_sources(map_path, root)

    layer_el = next(
        (l for l in root.findall("layer") if l.attrib.get("name") == layer), None
    )
    if layer_el is None:
        available = [l.attrib.get("name") for l in root.findall("layer")]
        raise ValueError(f"Tile layer '{layer}' not found. Available: {available}")

    gid_grid = ex.parse_layer_grid(layer_el)
    unknown: list[dict] = []
    grid: list[list[str]] = []
    for row_idx, row in enumerate(gid_grid):
        out_row: list[str] = []
        for col_idx, gid in enumerate(row):
            if gid == 0:
                out_row.append("")
            else:
                tile_id = gid_to_tile_id.get(gid & GID_MASK)
                if tile_id is None:
                    out_row.append(f"gid:{gid & GID_MASK}")
                    unknown.append(
                        {"col": col_idx, "row": row_idx, "gid": gid & GID_MASK, "flags": gid >> 29}
                    )
                else:
                    out_row.append(tile_id)
        grid.append(out_row)

    return {
        "map_id": map_id,
        "layer": layer,
        "width": int(layer_el.attrib["width"]),
        "height": int(layer_el.attrib["height"]),
        "encoding": layer_el.find("data").attrib.get("encoding", "csv") if layer_el.find("data") is not None else "csv",
        "grid": grid,
        "unknown_gids": unknown,
        "unknown_count": len(unknown),
    }


def get_props(map_id: str) -> dict:
    map_path, root = _parse_root(map_id)
    _, gid_to_prop_id = ex.parse_tileset_sources(map_path, root)
    if not any(g.attrib.get("name") == ex.PROPS_LAYER_NAME for g in root.findall("objectgroup")):
        return {"map_id": map_id, "props": [], "note": "No 'props' object layer found"}
    return ex.export_props(root, gid_to_prop_id, map_id)


def get_scene_hooks(map_id: str) -> dict:
    _, root = _parse_root(map_id)
    payload = ex.export_scene_hooks(root, map_id)
    if payload is None:
        return {
            "map_id": map_id,
            "spawn_points": [],
            "npcs": [],
            "pickups": [],
            "note": "No spawn/npcs/pickups object layers found",
        }
    return payload


def get_collision(map_id: str) -> dict:
    _, root = _parse_root(map_id)
    payload = ex.export_collision(root, map_id)
    if payload is None:
        return {"map_id": map_id, "cells": [], "note": "No collision layer found"}
    return payload


def list_tilesets(map_id: str) -> dict:
    map_path, root = _parse_root(map_id)
    return {"map_id": map_id, "tilesets": _tilesets_from_map(root, map_path)}


def get_tileset_tiles(tileset_path: str) -> dict:
    p = Path(tileset_path)
    if not p.is_absolute():
        candidate = (MAPS_DIR / tileset_path).resolve()
        if candidate.exists():
            p = candidate
        else:
            raise FileNotFoundError(f"Tileset not found: {tileset_path}")
    ts_root = ET.parse(p).getroot()
    name = ts_root.attrib.get("name", p.stem)
    tile_width = ts_root.attrib.get("tilewidth")
    tile_height = ts_root.attrib.get("tileheight")
    tiles = []
    for tile in ts_root.findall("tile"):
        local_id = int(tile.attrib["id"])
        tile_id = None
        prop_id = None
        props_node = tile.find("properties")
        if props_node is not None:
            for prop in props_node.findall("property"):
                n = prop.attrib.get("name")
                v = prop.attrib.get("value")
                if n == "tile_id":
                    tile_id = v
                elif n == "prop_id":
                    prop_id = v
        image = tile.find("image")
        image_source = image.attrib.get("source") if image is not None else None
        if tile_id is None and image_source:
            tile_id = Path(image_source).stem
        if prop_id is None and image_source:
            prop_id = Path(image_source).stem
        all_props = {}
        if props_node is not None:
            for prop in props_node.findall("property"):
                all_props[prop.attrib.get("name")] = prop.attrib.get("value")
        tiles.append(
            {
                "local_id": local_id,
                "tile_id": tile_id,
                "prop_id": prop_id,
                "image": image_source,
                "properties": all_props,
            }
        )
    return {
        "tileset": name,
        "path": str(p),
        "tile_width": int(tile_width) if tile_width else None,
        "tile_height": int(tile_height) if tile_height else None,
        "tile_count": len(tiles),
        "tiles": tiles,
    }
