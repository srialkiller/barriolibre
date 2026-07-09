#!/usr/bin/env python3
"""Author a barrio that resembles the reference image, end to end.

Deterministic map generator. Lays out a 3x3 block grid with WIDE 2-tile
avenues, crosswalks around the central plaza, diagonal plaza paths, and a
dense dressing of houses/trees/street furniture at proportional sizes.

Outputs:
  - layout.json  : ground layer (what Bevy renders today)
  - props.json   : prop instances (prop_id, cell, display size) for the engine
  - <map>.tmx    : ground + prop objects for hand editing in Tiled
  - _preview_barrio.png : QC composite
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_tileset import (  # noqa: E402
    CURATED_TUTORIAL_TILES,
    PROP_TILES,
    encode_layer_data,
    prop_path,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
MAP_ID = "barrio_tutorial_01"
MAP_DIR = REPO_ROOT / "data" / "maps" / MAP_ID
ENV = REPO_ROOT / "assets" / "environment"

SIZE = 24
TW, TH = 256, 128

# Wide 2-tile avenues split the map into a 3x3 block grid; centre block = plaza.
ROAD_ROWS = {7, 8, 15, 16}
ROAD_COLS = {7, 8, 15, 16}
PLAZA_MIN, PLAZA_MAX = 9, 14  # inclusive block bounds for the centre plaza

GROUND_FIRSTGID = 1
PROPS_FIRSTGID = len(CURATED_TUTORIAL_TILES) + 1  # 20
COLLISION_FIRSTGID = PROPS_FIRSTGID + len(PROP_TILES)  # 29

FOOTPRINTS_PATH = REPO_ROOT / "data" / "collision" / "prop_footprints.json"

GRASS = ["grass_clean_01", "grass_clean_02", "grass_clean_03", "grass_clean_04"]

# Proportional sizing: scale each prop so its on-screen HEIGHT matches a
# real-world size relative to the 128px tile diamond.
PROP_TARGET_HEIGHT = {
    "house_red_01": 320,
    "house_blue_01": 320,
    "house_yellow_01": 320,
    "house_wood_01": 320,
    "tree_01": 300,
    "fountain_01": 200,
    "lamp_01": 270,
    "bench_01": 95,
    "hydrant_01": 95,
}

_NATIVE_CACHE: dict[str, tuple[int, int]] = {}


def native_size(prop_id: str) -> tuple[int, int]:
    if prop_id not in _NATIVE_CACHE:
        with Image.open(prop_path(prop_id)) as image:
            _NATIVE_CACHE[prop_id] = image.size
    return _NATIVE_CACHE[prop_id]


def display_size(prop_id: str) -> tuple[float, float]:
    native_w, native_h = native_size(prop_id)
    scale = PROP_TARGET_HEIGHT.get(prop_id, 300) / native_h
    return native_w * scale, native_h * scale


def is_road(row: int, col: int) -> bool:
    return row in ROAD_ROWS or col in ROAD_COLS


def in_plaza(row: int, col: int) -> bool:
    return PLAZA_MIN <= row <= PLAZA_MAX and PLAZA_MIN <= col <= PLAZA_MAX


def plaza_ring_crosswalks() -> dict[tuple[int, int], str]:
    """Crosswalks on the avenue cells that border the central plaza."""
    overrides: dict[tuple[int, int], str] = {}
    for c in range(PLAZA_MIN, PLAZA_MAX + 1):
        overrides[(PLAZA_MIN - 1, c)] = "road_crosswalk_h_01"
        overrides[(PLAZA_MAX + 1, c)] = "road_crosswalk_h_01"
    for r in range(PLAZA_MIN, PLAZA_MAX + 1):
        overrides[(r, PLAZA_MIN - 1)] = "road_crosswalk_v_01"
        overrides[(r, PLAZA_MAX + 1)] = "road_crosswalk_v_01"
    return overrides


def plaza_diagonal(row: int, col: int) -> bool:
    """Diagonal 'X' pedestrian paths inside the plaza block."""
    if not in_plaza(row, col):
        return False
    local_r = row - PLAZA_MIN
    local_c = col - PLAZA_MIN
    span = PLAZA_MAX - PLAZA_MIN
    return local_r == local_c or local_r == (span - local_c)


def grass_variant(row: int, col: int) -> str:
    return GRASS[(col * 3 + row * 7) % len(GRASS)]


def build_ground() -> list[list[str]]:
    crosswalks = plaza_ring_crosswalks()
    grid: list[list[str]] = []
    for row in range(SIZE):
        line: list[str] = []
        for col in range(SIZE):
            if is_road(row, col):
                if (row, col) in crosswalks:
                    line.append(crosswalks[(row, col)])
                elif row in ROAD_ROWS and col in ROAD_COLS:
                    line.append("road_cross_01")
                elif col in ROAD_COLS:
                    line.append("road_straight_v_01")
                else:
                    line.append("road_straight_h_01")
            else:
                neighbours = [
                    (row - 1, col),
                    (row + 1, col),
                    (row, col - 1),
                    (row, col + 1),
                ]
                touches_road = any(
                    0 <= nr < SIZE and 0 <= nc < SIZE and is_road(nr, nc)
                    for nr, nc in neighbours
                )
                if touches_road or plaza_diagonal(row, col):
                    line.append("sidewalk_straight_01")
                else:
                    line.append(grass_variant(row, col))
        grid.append(line)
    return grid


def default_footprint_offsets(prop_id: str) -> list[list[int]]:
    if prop_id.startswith("house_"):
        return [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]]
    if prop_id == "fountain_01":
        return [[0, 0], [1, 0], [0, 1], [1, 1]]
    if prop_id in {"tree_01", "lamp_01"}:
        return [[0, 0]]
    return []


def load_footprint_templates() -> dict[str, list[list[int]]]:
    if not FOOTPRINTS_PATH.exists():
        return {}
    data = json.loads(FOOTPRINTS_PATH.read_text(encoding="utf-8"))
    return data.get("footprints", {})


def bake_collision_cells(props: list[dict]) -> list[list[int]]:
    templates = load_footprint_templates()
    blocked: set[tuple[int, int]] = set()
    for prop in props:
        prop_id = prop["prop_id"]
        offsets = templates.get(prop_id) or default_footprint_offsets(prop_id)
        if not offsets:
            continue
        anchor_col = int(prop["col"] // 1)
        anchor_row = int(prop["row"] // 1)
        for offset in offsets:
            blocked.add((anchor_col + offset[0], anchor_row + offset[1]))
    return sorted([[col, row] for col, row in blocked], key=lambda cell: (cell[1], cell[0]))


def write_collision_json(cells: list[list[int]]) -> None:
    payload = {
        "barrio_id": MAP_ID,
        "version": 1,
        "cells": cells,
        "metadata": {"baked_from_prop_footprints": True},
    }
    out = MAP_DIR / "collision.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(cells)} blocked cells)")


def collision_layer_gids(cells: list[list[int]]) -> list[int]:
    grid = [0] * (SIZE * SIZE)
    for col, row in cells:
        if 0 <= col < SIZE and 0 <= row < SIZE:
            grid[row * SIZE + col] = COLLISION_FIRSTGID
    return grid


def is_grass(ground: list[list[str]], row: int, col: int) -> bool:
    return (
        0 <= row < SIZE
        and 0 <= col < SIZE
        and ground[row][col].startswith("grass")
    )


# Block ranges (inclusive) for the 3x3 grid; centre is the plaza.
BLOCK_RANGES = [(0, 6), (PLAZA_MIN, PLAZA_MAX), (17, 23)]
HOUSE_CYCLE = [
    "house_red_01",
    "house_blue_01",
    "house_yellow_01",
    "house_wood_01",
]


def build_props(ground: list[list[str]]) -> list[dict]:
    props: list[dict] = []

    def add(prop_id: str, col: float, row: float) -> None:
        props.append({"prop_id": prop_id, "col": col, "row": row})

    house_index = 0
    for br in BLOCK_RANGES:
        for bc in BLOCK_RANGES:
            r0, r1 = br
            c0, c1 = bc
            if (r0, r1) == (PLAZA_MIN, PLAZA_MAX) and (c0, c1) == (PLAZA_MIN, PLAZA_MAX):
                continue  # plaza handled separately
            cr = (r0 + r1) // 2
            cc = (c0 + c1) // 2
            house_id = HOUSE_CYCLE[house_index % len(HOUSE_CYCLE)]
            house_index += 1
            add(house_id, cc, cr)

            tree_spots = [
                (r0 + 1, c0 + 1),
                (r0 + 1, c1 - 1),
                (r1 - 1, c0 + 1),
                (r1 - 1, c1 - 1),
                (cr, c0 + 1),
                (cr, c1 - 1),
            ]
            added = 0
            for rr, ccc in tree_spots:
                if added >= 4:
                    break
                if is_grass(ground, rr, ccc) and (rr, ccc) != (cr, cc):
                    add("tree_01", ccc, rr)
                    added += 1

    # Central plaza: fountain focal point, furniture behind it, diagonal X paths.
    mid = (PLAZA_MIN + PLAZA_MAX) / 2.0  # 11.5
    add("fountain_01", mid, mid)
    add("tree_01", PLAZA_MIN + 1, PLAZA_MIN + 1)
    add("tree_01", PLAZA_MAX - 1, PLAZA_MIN + 1)
    add("bench_01", PLAZA_MIN + 1, mid)
    add("bench_01", mid, PLAZA_MIN + 1)
    for rr, ccc in [
        (PLAZA_MIN, PLAZA_MIN),
        (PLAZA_MIN, PLAZA_MAX),
        (PLAZA_MAX, PLAZA_MIN),
        (PLAZA_MAX, PLAZA_MAX),
    ]:
        add("lamp_01", ccc, rr)

    # Street furniture: lamps at outer block corners nearest the avenues.
    lamp_spots = [
        (6, 6), (6, 17), (17, 6), (17, 17),
        (6, 9), (6, 14), (17, 9), (17, 14),
        (9, 6), (14, 6), (9, 17), (14, 17),
    ]
    for rr, ccc in lamp_spots:
        if ground[rr][ccc] == "sidewalk_straight_01":
            add("lamp_01", ccc, rr)
    for rr, ccc in [(6, 6), (17, 17), (6, 17)]:
        if ground[rr][ccc] == "sidewalk_straight_01":
            add("hydrant_01", ccc, rr)

    return props


def write_layout_json(ground: list[list[str]]) -> None:
    layout = {
        "barrio_id": MAP_ID,
        "display_name": "Barrio Tutorial",
        "size": [SIZE, SIZE],
        "tile_size_pixels": [TW, TH],
        "projection": "isometric_2_1",
        "layers": {"ground": ground, "markings": [], "overlay": []},
    }
    out = MAP_DIR / "layout.json"
    out.write_text(json.dumps(layout, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


def write_props_json(props: list[dict]) -> None:
    entries = []
    for prop in props:
        width, height = display_size(prop["prop_id"])
        entries.append(
            {
                "prop_id": prop["prop_id"],
                "col": round(prop["col"], 3),
                "row": round(prop["row"], 3),
                "width_px": round(width, 2),
                "height_px": round(height, 2),
            }
        )
    payload = {
        "barrio_id": MAP_ID,
        "tile_size_pixels": [TW, TH],
        "props": entries,
    }
    out = MAP_DIR / "props.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(entries)} props)")


# Player spawn on open plaza grass, clear of the fountain footprint.
SPAWN_COL, SPAWN_ROW = 13, 13


def write_scene_hooks_json() -> None:
    payload = {
        "barrio_id": MAP_ID,
        "version": 1,
        "spawn_points": [
            {
                "id": "tutorial_spawn",
                "position": [SPAWN_COL, SPAWN_ROW],
                "facing": "south",
            }
        ],
        "checkpoints": [],
        "poi_hooks": [
            {
                "id": "plaza_central",
                "position": [11, 11],
                "poi_type": "plaza",
            }
        ],
        "metadata": {
            "tutorial": True,
            "description": "Primer barrio del Foundation Runtime",
        },
    }
    out = MAP_DIR / "scene_hooks.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


def spawn_object_xml(object_id: int) -> tuple[str, int]:
    x = (SPAWN_COL + 0.5) * TH
    y = (SPAWN_ROW + 0.5) * TH
    line = (
        f'  <object id="{object_id}" name="tutorial_spawn" '
        f'x="{x:.2f}" y="{y:.2f}" width="0" height="0">'
        f'<properties><property name="facing" value="south"/></properties></object>'
    )
    return line, object_id + 1


def ground_gids(ground: list[list[str]]) -> list[int]:
    index_of = {tid: i for i, tid in enumerate(CURATED_TUTORIAL_TILES)}
    return [GROUND_FIRSTGID + index_of[tile_id] for row in ground for tile_id in row]


def prop_object_xml(props: list[dict]) -> tuple[list[str], int]:
    prop_index = {pid: i for i, pid in enumerate(PROP_TILES)}
    lines: list[str] = []
    object_id = 1
    for prop in props:
        prop_id = prop["prop_id"]
        gid = PROPS_FIRSTGID + prop_index[prop_id]
        width, height = display_size(prop_id)
        x = (prop["col"] + 0.5) * TH
        y = (prop["row"] + 0.5) * TH
        lines.append(
            f'  <object id="{object_id}" gid="{gid}" '
            f'x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}"/>'
        )
        object_id += 1
    return lines, object_id


def write_tmx(ground: list[list[str]], props: list[dict], collision_cells: list[list[int]]) -> None:
    encoded_ground = encode_layer_data(ground_gids(ground))
    empty_layer = encode_layer_data([0] * (SIZE * SIZE))
    encoded_collision = encode_layer_data(collision_layer_gids(collision_cells))
    object_lines, next_object_id = prop_object_xml(props)
    spawn_line, next_object_id = spawn_object_xml(next_object_id)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<map version="1.10" tiledversion="1.10.2" '
            'orientation="isometric" renderorder="right-down" '
            f'width="{SIZE}" height="{SIZE}" '
            f'tilewidth="{TW}" tileheight="{TH}" infinite="0" '
            f'nextlayerid="8" nextobjectid="{next_object_id}">'
        ),
        ' <tileset firstgid="1" source="environment_tutorial.tsx"/>',
        f' <tileset firstgid="{PROPS_FIRSTGID}" source="props_tutorial.tsx"/>',
        f' <tileset firstgid="{COLLISION_FIRSTGID}" source="collision_tutorial.tsx"/>',
        f' <layer id="1" name="ground" width="{SIZE}" height="{SIZE}" x="0" y="0">',
        f'  <data encoding="base64">{encoded_ground}</data>',
        " </layer>",
        f' <layer id="2" name="markings" width="{SIZE}" height="{SIZE}" x="0" y="0">',
        f'  <data encoding="base64">{empty_layer}</data>',
        " </layer>",
        f' <layer id="3" name="overlay" width="{SIZE}" height="{SIZE}" x="0" y="0">',
        f'  <data encoding="base64">{empty_layer}</data>',
        " </layer>",
        (
            f' <layer id="6" name="collision" width="{SIZE}" height="{SIZE}" '
            f'x="0" y="0" opacity="0.55">'
        ),
        f'  <data encoding="base64">{encoded_collision}</data>',
        " </layer>",
        ' <objectgroup id="4" name="props">',
    ]
    lines.extend(object_lines)
    lines.append(" </objectgroup>")
    lines.append(' <objectgroup id="5" name="spawn">')
    lines.append(spawn_line)
    lines.append(" </objectgroup>")
    lines.append(' <objectgroup id="7" name="collision_zones">')
    lines.append(" </objectgroup>")
    lines.append("</map>")

    out = MAP_DIR / f"{MAP_ID}.tmx"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(props)} props)")


def category(tile_id: str) -> str:
    if tile_id.startswith("road_"):
        return "roads"
    if tile_id.startswith("sidewalk_"):
        return "sidewalks"
    return "terrain"


def render_preview(ground: list[list[str]], props: list[dict]) -> None:
    side_margin = 64
    top_margin = 820
    bottom_margin = 96
    canvas_w = (SIZE + SIZE) * (TW // 2) + side_margin * 2
    canvas_h = (SIZE + SIZE) * (TH // 2) + top_margin + bottom_margin
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (36, 38, 48, 255))

    origin_x = side_margin + SIZE * (TW // 2) - TW // 2
    origin_y = top_margin

    for gy in range(SIZE):
        for gx in range(SIZE):
            tile_id = ground[gy][gx]
            tile = Image.open(ENV / category(tile_id) / f"{tile_id}.png").convert("RGBA")
            screen_x = origin_x + (gx - gy) * (TW // 2)
            screen_y = origin_y + (gx + gy) * (TH // 2)
            canvas.alpha_composite(tile, (screen_x, screen_y))

    def cell_center(col: float, row: float) -> tuple[float, float]:
        cx = origin_x + (col - row) * (TW / 2) + TW / 2
        cy = origin_y + (col + row) * (TH / 2) + TH / 2
        return cx, cy

    for prop in sorted(props, key=lambda p: (p["col"] + p["row"], p["row"])):
        prop_id = prop["prop_id"]
        width, height = display_size(prop_id)
        image = Image.open(prop_path(prop_id)).convert("RGBA")
        image = image.resize((max(1, round(width)), max(1, round(height))), Image.Resampling.LANCZOS)
        cx, cy = cell_center(prop["col"], prop["row"])
        canvas.alpha_composite(image, (round(cx - image.width / 2), round(cy - image.height)))

    out = MAP_DIR / "_preview_barrio.png"
    canvas.save(out)
    print(f"Wrote {out} ({canvas.size[0]}x{canvas.size[1]})")


def main() -> int:
    ground = build_ground()
    props = build_props(ground)
    collision_cells = bake_collision_cells(props)
    write_layout_json(ground)
    write_props_json(props)
    write_scene_hooks_json()
    write_collision_json(collision_cells)
    write_tmx(ground, props, collision_cells)
    render_preview(ground, props)
    return 0


if __name__ == "__main__":
    sys.exit(main())
