#!/usr/bin/env python3
"""Export a Tiled map (.tmx) to BarrioLibre layout.json, props.json, scene_hooks.json,
and collision.json.

Reads tile layers (ground, markings, overlay) for layout.json and the object
layer named ``props`` for props.json so manual edits in Tiled are reflected in
the Bevy runtime.
"""

from __future__ import annotations

import argparse
import base64
import json
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

LAYER_NAMES = ("ground", "markings", "overlay")
PROPS_LAYER_NAME = "props"
SPAWN_LAYER_NAME = "spawn"
NPC_LAYER_NAME = "npcs"
PICKUP_LAYER_NAME = "pickups"
COLLISION_LAYER_NAME = "collision"
COLLISION_ZONES_LAYER_NAME = "collision_zones"
# Tiled stores flip flags in the top bits of tile/object gids.
GID_MASK = 0x1FFFFFFF


def parse_tileset_sources(
    map_path: Path, root: ET.Element
) -> tuple[dict[int, str], dict[int, str]]:
    gid_to_tile_id: dict[int, str] = {}
    gid_to_prop_id: dict[int, str] = {}

    for tileset_ref in root.findall("tileset"):
        first_gid = int(tileset_ref.attrib["firstgid"])
        source = tileset_ref.attrib.get("source")
        if not source:
            continue

        tileset_path = (map_path.parent / source).resolve()
        tileset_root = ET.parse(tileset_path).getroot()

        for tile in tileset_root.findall("tile"):
            local_id = int(tile.attrib["id"])
            gid = first_gid + local_id
            tile_id: str | None = None
            prop_id: str | None = None

            properties = tile.find("properties")
            if properties is not None:
                for prop in properties.findall("property"):
                    name = prop.attrib.get("name")
                    value = prop.attrib.get("value")
                    if name == "tile_id":
                        tile_id = value
                    elif name == "prop_id":
                        prop_id = value

            if tile_id is None or prop_id is None:
                image = tile.find("image")
                if image is not None:
                    stem = Path(image.attrib["source"]).stem
                    if tile_id is None:
                        tile_id = stem
                    if prop_id is None:
                        prop_id = stem

            if tile_id:
                gid_to_tile_id[gid] = tile_id
            if prop_id:
                gid_to_prop_id[gid] = prop_id

    return gid_to_tile_id, gid_to_prop_id


def parse_layer_grid(layer: ET.Element) -> list[list[int]]:
    data = layer.find("data")
    if data is None:
        raise ValueError(f"Layer '{layer.attrib.get('name')}' has no <data>")

    width = int(layer.attrib["width"])
    height = int(layer.attrib["height"])
    encoding = data.attrib.get("encoding", "csv")

    if encoding == "base64":
        raw = base64.b64decode(data.text.strip())
        values = [
            struct.unpack_from("<I", raw, index * 4)[0]
            for index in range(len(raw) // 4)
        ]
    elif encoding == "csv":
        raw_text = data.text.replace("\n", ",").replace("\r", "")
        values = [int(value.strip()) for value in raw_text.split(",") if value.strip()]
    else:
        raise ValueError(f"Unsupported layer encoding: {encoding}")

    expected = width * height
    if len(values) != expected:
        raise ValueError(
            f"Layer '{layer.attrib.get('name')}' expected {expected} tiles, got {len(values)}"
        )

    return [values[row * width : (row + 1) * width] for row in range(height)]


def gid_grid_to_tile_ids(
    gid_grid: list[list[int]],
    gid_to_tile_id: dict[int, str],
    default_tile_id: str,
) -> list[list[str]]:
    output: list[list[str]] = []
    for row in gid_grid:
        output_row: list[str] = []
        for gid in row:
            if gid == 0:
                output_row.append(default_tile_id)
            else:
                tile_id = gid_to_tile_id.get(gid & GID_MASK)
                if tile_id is None:
                    raise KeyError(f"Unknown tile gid={gid}")
                output_row.append(tile_id)
        output.append(output_row)
    return output


def tiled_object_to_grid(x: float, y: float, tile_height: float) -> tuple[float, float]:
    """Convert Tiled isometric object coords to fractional grid col/row.

    Our generator places props with bottom-centre anchor at
    ``x = (col + 0.5) * tile_height``, ``y = (row + 0.5) * tile_height``,
    matching ``objectalignment="bottom"`` on the props tileset.
    """
    col = x / tile_height - 0.5
    row = y / tile_height - 0.5
    return col, row


def export_props(
    root: ET.Element,
    gid_to_prop_id: dict[int, str],
    barrio_id: str,
) -> dict:
    tile_width = int(root.attrib["tilewidth"])
    tile_height = int(root.attrib["tileheight"])
    props: list[dict] = []

    for group in root.findall("objectgroup"):
        if group.attrib.get("name") != PROPS_LAYER_NAME:
            continue
        for obj in group.findall("object"):
            gid_raw = obj.attrib.get("gid")
            if not gid_raw:
                continue

            gid = int(gid_raw) & GID_MASK
            prop_id = gid_to_prop_id.get(gid)
            if prop_id is None:
                raise KeyError(f"Unknown prop gid={gid} (object id={obj.attrib.get('id')})")

            width_px = float(obj.attrib.get("width", 0))
            height_px = float(obj.attrib.get("height", 0))
            if width_px <= 0.0 or height_px <= 0.0:
                raise ValueError(
                    f"Prop object id={obj.attrib.get('id')} has invalid size "
                    f"{width_px}x{height_px}"
                )

            col, row = tiled_object_to_grid(
                float(obj.attrib["x"]),
                float(obj.attrib["y"]),
                float(tile_height),
            )
            props.append(
                {
                    "prop_id": prop_id,
                    "col": round(col, 3),
                    "row": round(row, 3),
                    "width_px": round(width_px, 2),
                    "height_px": round(height_px, 2),
                }
            )

    props.sort(key=lambda entry: (entry["row"], entry["col"], entry["prop_id"]))

    return {
        "barrio_id": barrio_id,
        "tile_size_pixels": [tile_width, tile_height],
        "props": props,
    }


def object_properties(obj: ET.Element) -> dict[str, str]:
    properties: dict[str, str] = {}
    properties_node = obj.find("properties")
    if properties_node is None:
        return properties
    for prop in properties_node.findall("property"):
        name = prop.attrib.get("name")
        value = prop.attrib.get("value")
        if name and value is not None:
            properties[name] = value
    return properties


def export_scene_hooks(root: ET.Element, barrio_id: str) -> dict | None:
    tile_height = float(root.attrib["tileheight"])
    spawn_points: list[dict] = []
    npcs: list[dict] = []
    pickups: list[dict] = []

    for group in root.findall("objectgroup"):
        layer_name = group.attrib.get("name")
        for obj in group.findall("object"):
            col, row = tiled_object_to_grid(
                float(obj.attrib["x"]),
                float(obj.attrib["y"]),
                tile_height,
            )
            object_id = obj.attrib.get("id", "0")
            object_name = obj.attrib.get("name")
            position = [int(round(col)), int(round(row))]
            properties = object_properties(obj)

            if layer_name == SPAWN_LAYER_NAME:
                entry: dict = {
                    "id": object_name or f"spawn_{object_id}",
                    "position": position,
                }
                if properties.get("facing"):
                    entry["facing"] = properties["facing"]
                spawn_points.append(entry)
            elif layer_name == NPC_LAYER_NAME:
                npcs.append(
                    {
                        "id": object_name or f"npc_{object_id}",
                        "name": properties.get("display_name", object_name or "Vecino"),
                        "dialogue": properties.get(
                            "dialogue", "¡Qué bueno verte explorando el barrio!"
                        ),
                        "position": position,
                    }
                )
            elif layer_name == PICKUP_LAYER_NAME:
                material_id = properties.get("material_id")
                if not material_id:
                    raise ValueError(
                        f"Pickup object id={object_id} requires material_id property"
                    )
                pickups.append(
                    {
                        "id": object_name or f"pickup_{object_id}",
                        "material_id": material_id,
                        "display_name": properties.get("display_name", material_id),
                        "quantity": int(properties.get("quantity", "1")),
                        "position": position,
                    }
                )

    if not spawn_points and not npcs and not pickups:
        return None

    return {
        "barrio_id": barrio_id,
        "version": 1,
        "spawn_points": spawn_points,
        "npcs": npcs,
        "pickups": pickups,
        "checkpoints": [],
        "poi_hooks": [],
        "metadata": {"exported_from_tiled": True},
    }


def cell_center_tiled(col: int, row: int, tile_height: float) -> tuple[float, float]:
    """Map-pixel center of a grid cell (matches prop/spawn object placement)."""
    x = (col + 0.5) * tile_height
    y = (row + 0.5) * tile_height
    return x, y


def point_in_rect(px: float, py: float, rx: float, ry: float, rw: float, rh: float) -> bool:
    return rx <= px <= rx + rw and ry <= py <= ry + rh


def collision_cells_from_zones(
    root: ET.Element,
    map_width: int,
    map_height: int,
    tile_height: float,
) -> set[tuple[int, int]]:
    blocked: set[tuple[int, int]] = set()
    for group in root.findall("objectgroup"):
        if group.attrib.get("name") != COLLISION_ZONES_LAYER_NAME:
            continue
        for obj in group.findall("object"):
            width = float(obj.attrib.get("width", 0))
            height = float(obj.attrib.get("height", 0))
            if width <= 0.0 or height <= 0.0:
                continue
            rect_x = float(obj.attrib["x"])
            rect_y = float(obj.attrib["y"])
            for row in range(map_height):
                for col in range(map_width):
                    center_x, center_y = cell_center_tiled(col, row, tile_height)
                    if point_in_rect(center_x, center_y, rect_x, rect_y, width, height):
                        blocked.add((col, row))
    return blocked


def zones_from_tiled(
    root: ET.Element,
    tile_height: float,
) -> list[dict]:
    """Export collision_zones rectangles as raw sub-tile rects in grid coords.

    Each Tiled object (x, y, width, height in pixels) is converted to grid
    coordinates: col = x / tile_height, row = y / tile_height,
    width = w / tile_height, height = h / tile_height.
    """
    zones: list[dict] = []
    for group in root.findall("objectgroup"):
        if group.attrib.get("name") != COLLISION_ZONES_LAYER_NAME:
            continue
        for obj in group.findall("object"):
            width = float(obj.attrib.get("width", 0))
            height = float(obj.attrib.get("height", 0))
            if width <= 0.0 or height <= 0.0:
                continue
            rect_x = float(obj.attrib["x"])
            rect_y = float(obj.attrib["y"])
            col = rect_x / tile_height
            row = rect_y / tile_height
            w = width / tile_height
            h = height / tile_height
            zones.append(
                {"col": round(col, 4), "row": round(row, 4), "width": round(w, 4), "height": round(h, 4)}
            )
    return zones


def export_collision(root: ET.Element, barrio_id: str) -> dict | None:
    map_width = int(root.attrib["width"])
    map_height = int(root.attrib["height"])
    tile_height = float(root.attrib["tileheight"])
    blocked: set[tuple[int, int]] = set()
    has_tile_layer = False
    has_zone_layer = any(
        group.attrib.get("name") == COLLISION_ZONES_LAYER_NAME
        for group in root.findall("objectgroup")
    )

    for layer in root.findall("layer"):
        if layer.attrib.get("name") != COLLISION_LAYER_NAME:
            continue
        has_tile_layer = True
        gid_grid = parse_layer_grid(layer)
        for row_idx, row in enumerate(gid_grid):
            for col_idx, gid in enumerate(row):
                if (gid & GID_MASK) != 0:
                    blocked.add((col_idx, row_idx))

    blocked.update(
        collision_cells_from_zones(root, map_width, map_height, tile_height)
    )

    if not has_tile_layer and not has_zone_layer:
        return None

    cells = sorted([[col, row] for col, row in blocked], key=lambda cell: (cell[1], cell[0]))
    zones = zones_from_tiled(root, tile_height)
    return {
        "barrio_id": barrio_id,
        "version": 1,
        "cells": cells,
        "zones": zones,
        "metadata": {"exported_from_tiled": True},
    }


def export_layout(
    map_path: Path,
    barrio_id: str,
    display_name: str,
    default_tile_id: str,
) -> tuple[dict, dict | None, dict | None, dict | None]:
    root = ET.parse(map_path).getroot()
    if root.attrib.get("orientation") != "isometric":
        raise ValueError("Map must use isometric orientation")

    width = int(root.attrib["width"])
    height = int(root.attrib["height"])
    gid_to_tile_id, gid_to_prop_id = parse_tileset_sources(map_path, root)

    layers: dict[str, list[list[str]]] = {
        "ground": [],
        "markings": [],
        "overlay": [],
    }

    for layer in root.findall("layer"):
        layer_name = layer.attrib.get("name", "")
        if layer_name not in LAYER_NAMES:
            continue
        gid_grid = parse_layer_grid(layer)
        layers[layer_name] = gid_grid_to_tile_ids(gid_grid, gid_to_tile_id, default_tile_id)

    if not layers["ground"]:
        raise ValueError("Map must contain a 'ground' layer")

    layout = {
        "barrio_id": barrio_id,
        "display_name": display_name,
        "size": [width, height],
        "tile_size_pixels": [int(root.attrib["tilewidth"]), int(root.attrib["tileheight"])],
        "projection": "isometric_2_1",
        "layers": layers,
    }

    props_payload: dict | None = None
    if gid_to_prop_id and any(
        group.attrib.get("name") == PROPS_LAYER_NAME for group in root.findall("objectgroup")
    ):
        props_payload = export_props(root, gid_to_prop_id, barrio_id)

    spawn_payload = export_scene_hooks(root, barrio_id)
    collision_payload = export_collision(root, barrio_id)

    return layout, props_payload, spawn_payload, collision_payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export Tiled .tmx to layout.json (+ props.json from object layer)"
    )
    parser.add_argument("tmx", type=Path, help="Path to .tmx map file")
    parser.add_argument("--barrio-id", help="Override barrio_id (default: map folder name)")
    parser.add_argument("--display-name", default="Barrio Tutorial")
    parser.add_argument("--default-tile-id", default="grass_clean_01")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output layout.json path (default: same folder as .tmx)",
    )
    parser.add_argument(
        "--props-output",
        type=Path,
        help="Output props.json path (default: same folder as .tmx)",
    )
    parser.add_argument(
        "--no-props",
        action="store_true",
        help="Skip exporting props.json even if a props object layer exists.",
    )
    parser.add_argument(
        "--hooks-output",
        type=Path,
        help="Output scene_hooks.json path (default: same folder as .tmx)",
    )
    parser.add_argument(
        "--no-hooks",
        action="store_true",
        help="Skip exporting scene_hooks.json even if a spawn object layer exists.",
    )
    parser.add_argument(
        "--collision-output",
        type=Path,
        help="Output collision.json path (default: same folder as .tmx)",
    )
    parser.add_argument(
        "--no-collision",
        action="store_true",
        help="Skip exporting collision.json even if a collision tile layer exists.",
    )
    args = parser.parse_args()

    map_path = args.tmx if args.tmx.is_absolute() else REPO_ROOT / args.tmx
    barrio_id = args.barrio_id or map_path.parent.name
    output_path = args.output or map_path.parent / "layout.json"
    props_output_path = args.props_output or map_path.parent / "props.json"
    hooks_output_path = args.hooks_output or map_path.parent / "scene_hooks.json"
    collision_output_path = args.collision_output or map_path.parent / "collision.json"

    layout, props_payload, spawn_payload, collision_payload = export_layout(
        map_path=map_path,
        barrio_id=barrio_id,
        display_name=args.display_name,
        default_tile_id=args.default_tile_id,
    )

    output_path.write_text(json.dumps(layout, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Exported {output_path}")
    print(f"Size: {layout['size'][0]}x{layout['size'][1]}")
    print(f"Ground layer rows: {len(layout['layers']['ground'])}")

    if not args.no_props and props_payload is not None:
        props_output_path.write_text(
            json.dumps(props_payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Exported {props_output_path} ({len(props_payload['props'])} props)")
    elif not args.no_props:
        print("No props object layer found — props.json unchanged")

    if not args.no_hooks and spawn_payload is not None:
        hooks_output_path.write_text(
            json.dumps(spawn_payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(
            f"Exported {hooks_output_path} "
            f"({len(spawn_payload['spawn_points'])} spawn points)"
        )
    elif not args.no_hooks:
        print("No spawn object layer found — scene_hooks.json unchanged")

    if not args.no_collision and collision_payload is not None:
        collision_output_path.write_text(
            json.dumps(collision_payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(
            f"Exported {collision_output_path} "
            f"({len(collision_payload['cells'])} blocked cells)"
        )
    elif not args.no_collision:
        print("No collision layer found — collision.json unchanged")

    return 0


if __name__ == "__main__":
    sys.exit(main())
