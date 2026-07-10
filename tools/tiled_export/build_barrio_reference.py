#!/usr/bin/env python3
"""Author *barrio_tutorial_01* — a compact, readable tutorial neighbourhood.

Design goals (see ``data/maps/barrio_tutorial_01/README_MEJORAS.md``):

* Small, memorable barrio that teaches by layout, not by pop-ups.
* Clean 2x2 avenue grid framing a central plaza (the visual anchor).
* Full sidewalks (``veredas``) lining every avenue, plus pedestrian
  crossings (``pasos peatonales``) at the four plaza entrances.
* 8 house plots (one per surrounding block), each with a small garden and
  street furniture, every house reachable from a sidewalk.
* Named landmarks: Tienda (N), Casa de Pedro (S), Garaje bloqueado (E).
* A natural exploration loop: spawn -> Pedro -> gather 3 materials around
  the plaza -> return to Pedro -> the Garaje unlocks.

This script only *authors* the ``.tmx`` (the source of truth) plus a QC
preview. The canonical JSON files are produced by ``export_layout.py`` from
that ``.tmx`` so the map stays 100% compatible with the Tiled pipeline and
``map_validator``.

Hard runtime contracts respected (do NOT change without updating Rust):
* spawn at grid ``[13, 13]`` (``src/world/map/resources.rs`` test).
* first NPC id ``pedro_vecino`` and exactly 3 pickups, none at spawn.
* pickup materials ``cardboard`` / ``wire`` / ``bottle_caps`` — the
  ``tutorial_first_cart`` quest requires exactly those three.
* only tiles/props that exist on disk are used (no new art).
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
    write_props_tileset,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
MAP_ID = "barrio_tutorial_01"
MAP_DIR = REPO_ROOT / "data" / "maps" / MAP_ID
ENV = REPO_ROOT / "assets" / "environment"

SIZE = 24
TW, TH = 256, 128

# --- Street network ----------------------------------------------------------
# Two 2-wide horizontal avenues and two 2-wide vertical avenues form a clean
# 2x2 grid. Their crossings are the intersections; the middle block is the
# plaza. Everything on grass/sidewalk/road is walkable; only prop footprints
# block, so the player can never get stuck.
AVENUE_ROWS = {7, 8, 15, 16}
AVENUE_COLS = {7, 8, 15, 16}
PLAZA_MIN, PLAZA_MAX = 9, 14  # inclusive plaza block bounds

GROUND_FIRSTGID = 1
PROPS_FIRSTGID = len(CURATED_TUTORIAL_TILES) + 1  # 20
COLLISION_FIRSTGID = PROPS_FIRSTGID + len(PROP_TILES)  # 29

GRASS = ["grass_clean_01", "grass_clean_02", "grass_clean_03", "grass_clean_04"]

# Proportional on-screen height per prop (px), relative to the 128px tile.
PROP_TARGET_HEIGHT = {
    "house_red_01": 320,
    "house_blue_01": 320,
    "house_yellow_01": 320,
    "house_wood_01": 320,
    "garage_01": 300,
    "shop_01": 345,
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


# --- Ground classification ---------------------------------------------------


def is_avenue(row: int, col: int) -> bool:
    return row in AVENUE_ROWS or col in AVENUE_COLS


def in_plaza(row: int, col: int) -> bool:
    return PLAZA_MIN <= row <= PLAZA_MAX and PLAZA_MIN <= col <= PLAZA_MAX


def plaza_diagonal(row: int, col: int) -> bool:
    """The 'X' pedestrian paths crossing the plaza block."""
    if not in_plaza(row, col):
        return False
    local_r = row - PLAZA_MIN
    local_c = col - PLAZA_MIN
    span = PLAZA_MAX - PLAZA_MIN
    return local_r == local_c or local_r == (span - local_c)


def crosswalk_tile(row: int, col: int) -> str | None:
    """Zebra crossings on the avenue cells facing the four plaza entrances."""
    mid_cols = {11, 12}
    mid_rows = {11, 12}
    # North / South entrances: cross the horizontal avenues.
    if row in AVENUE_ROWS and col in mid_cols:
        return "road_crosswalk_h_01"
    # West / East entrances: cross the vertical avenues.
    if col in AVENUE_COLS and row in mid_rows:
        return "road_crosswalk_v_01"
    return None


def _hash2(a: int, b: int) -> int:
    h = (a * 73856093) ^ (b * 19349663)
    return (h ^ (h >> 13)) & 0x7FFFFFFF


def grass_variant(row: int, col: int) -> str:
    """Patch-based grass so nearby cells share a variant (organic gardens)."""
    base = _hash2(row // 2, col // 2) % len(GRASS)
    if _hash2(row, col) % 7 == 0:
        base = (base + 1) % len(GRASS)
    return GRASS[base]


def touches_avenue(row: int, col: int) -> bool:
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = row + dr, col + dc
        if 0 <= nr < SIZE and 0 <= nc < SIZE and is_avenue(nr, nc) and not in_plaza(nr, nc):
            return True
    return False


def build_ground() -> list[list[str]]:
    grid: list[list[str]] = []
    for row in range(SIZE):
        line: list[str] = []
        for col in range(SIZE):
            if in_plaza(row, col):
                line.append("sidewalk_straight_01" if plaza_diagonal(row, col) else grass_variant(row, col))
            elif is_avenue(row, col):
                line.append(crosswalk_tile(row, col) or "road_plain_01")
            elif touches_avenue(row, col):
                line.append("sidewalk_straight_01")  # full sidewalks lining streets
            else:
                line.append(grass_variant(row, col))
        grid.append(line)
    return grid


def is_grass(ground: list[list[str]], row: int, col: int) -> bool:
    return 0 <= row < SIZE and 0 <= col < SIZE and ground[row][col].startswith("grass")


def is_sidewalk(ground: list[list[str]], row: int, col: int) -> bool:
    return 0 <= row < SIZE and 0 <= col < SIZE and ground[row][col] == "sidewalk_straight_01"


# --- Props -------------------------------------------------------------------
# Each surrounding block gets one building (front toward the plaza), a small
# garden of trees and one piece of street furniture on the facing sidewalk.
# Landmarks (Tienda / Garaje) use their own dedicated building sprites.
BLOCK_PLOTS = [
    # name / role,      building,          anchor(col,row), trees (in-block grass),        accent (facing sidewalk)
    ("tienda",          "shop_01",         (11, 3),  [(10, 1), (13, 1), (10, 5)],   ("bench_01", 10, 6)),
    ("casa_pedro",      "house_wood_01",   (11, 20), [(10, 22), (13, 22), (10, 19)], ("bench_01", 10, 17)),
    ("garaje",          "garage_01",       (20, 11), [(22, 10), (22, 13), (18, 12)], ("hydrant_01", 17, 11)),
    ("casa_oeste",      "house_blue_01",   (3, 11),  [(1, 10), (3, 13), (5, 11)],    ("lamp_01", 6, 10)),
    ("casa_noroeste",   "house_blue_01",   (3, 3),   [(1, 1), (5, 1), (1, 5)],       ("lamp_01", 6, 6)),
    ("casa_noreste",    "house_yellow_01", (20, 3),  [(18, 1), (22, 1), (22, 5)],    ("hydrant_01", 17, 6)),
    ("casa_suroeste",   "house_wood_01",   (3, 20),  [(1, 18), (1, 22), (5, 22)],    ("lamp_01", 6, 18)),
    ("casa_sureste",    "house_red_01",    (20, 20), [(22, 18), (22, 22), (18, 22)], ("hydrant_01", 17, 18)),
]

# Plaza dressing (kept clear of spawn [13,13], Pedro [12,13] and the fountain).
FOUNTAIN = (11, 11)  # (col, row) plaza centrepiece
PLAZA_BENCHES = [(11, 9), (9, 11), (13, 11), (11, 14)]  # (col, row)
PLAZA_LAMPS = [(9, 9), (14, 9), (9, 14), (14, 14)]
PLAZA_TREES = [(14, 10), (10, 14), (13, 9)]


def build_props(ground: list[list[str]]) -> list[dict]:
    props: list[dict] = []
    occupied: set[tuple[int, int]] = set()

    def add(prop_id: str, col: int, row: int, *, want_grass=False, want_sidewalk=False) -> None:
        cell = (col, row)
        if cell in occupied:
            print(f"  ! skip {prop_id} at {cell}: cell already used")
            return
        if want_grass and not is_grass(ground, row, col):
            print(f"  ! skip {prop_id} at {cell}: not grass ({ground[row][col]})")
            return
        if want_sidewalk and not is_sidewalk(ground, row, col):
            print(f"  ! skip {prop_id} at {cell}: not sidewalk ({ground[row][col]})")
            return
        occupied.add(cell)
        props.append({"prop_id": prop_id, "col": col, "row": row})

    # Reserve gameplay cells so no prop lands on them.
    for reserved in ((13, 13), (12, 13), (12, 6), (6, 12), (12, 17)):
        occupied.add(reserved)

    for _name, house, (hc, hr), trees, accent in BLOCK_PLOTS:
        add(house, hc, hr, want_grass=True)
        for tc, tr in trees:
            add("tree_01", tc, tr, want_grass=True)
        acc_id, ac, ar = accent
        add(acc_id, ac, ar, want_sidewalk=True)

    # Plaza.
    add("fountain_01", *FOUNTAIN)
    for bc, br in PLAZA_BENCHES:
        add("bench_01", bc, br)
    for lc, lr in PLAZA_LAMPS:
        add("lamp_01", lc, lr)
    for tc, tr in PLAZA_TREES:
        add("tree_01", tc, tr, want_grass=True)

    return props


# --- Collision ---------------------------------------------------------------
# Sub-tile zones drive fine collision; houses/fountain also get full-tile
# cells baked into the collision layer so buildings are solid.
PROP_ZONE_SIZE = {
    "tree_01": 0.35,
    "lamp_01": 0.18,
    "hydrant_01": 0.15,
    "bench_01": 0.5,
}
HOUSE_ZONE_HALF = 1.5   # buildings block ~3x3 around their anchor
FOUNTAIN_ZONE = 1.2

# Solid buildings that block a full 3x3 footprint (houses + landmarks).
BUILDING_PROPS = {"garage_01", "shop_01"}


def is_building(prop_id: str) -> bool:
    return prop_id.startswith("house_") or prop_id in BUILDING_PROPS


def build_collision_zones(props: list[dict]) -> list[dict]:
    zones: list[dict] = []
    for prop in props:
        pid, col, row = prop["prop_id"], prop["col"], prop["row"]
        if pid in PROP_ZONE_SIZE:
            s = PROP_ZONE_SIZE[pid]
            zones.append({
                "col": round(col + 0.5 - s / 2, 4),
                "row": round(row + 0.5 - s / 2, 4),
                "width": round(s, 4),
                "height": round(s, 4),
            })
        elif is_building(pid):
            zones.append({
                "col": round(col + 0.5 - HOUSE_ZONE_HALF, 4),
                "row": round(row + 0.5 - HOUSE_ZONE_HALF, 4),
                "width": round(HOUSE_ZONE_HALF * 2, 4),
                "height": round(HOUSE_ZONE_HALF * 2, 4),
            })
        elif pid == "fountain_01":
            zones.append({
                "col": round(col + 0.5 - FOUNTAIN_ZONE / 2, 4),
                "row": round(row + 0.5 - FOUNTAIN_ZONE / 2, 4),
                "width": round(FOUNTAIN_ZONE, 4),
                "height": round(FOUNTAIN_ZONE, 4),
            })
    return zones


def build_collision_cells(props: list[dict]) -> list[list[int]]:
    """Full-tile blocked cells for solid buildings and the fountain base."""
    blocked: set[tuple[int, int]] = set()
    for prop in props:
        pid, col, row = prop["prop_id"], prop["col"], prop["row"]
        if is_building(pid):
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    c, r = col + dc, row + dr
                    if 0 <= c < SIZE and 0 <= r < SIZE:
                        blocked.add((c, r))
        elif pid == "fountain_01":
            blocked.add((col, row))
    return sorted(([c, r] for c, r in blocked), key=lambda cell: (cell[1], cell[0]))


def collision_layer_gids(cells: list[list[int]]) -> list[int]:
    grid = [0] * (SIZE * SIZE)
    for col, row in cells:
        if 0 <= col < SIZE and 0 <= row < SIZE:
            grid[row * SIZE + col] = COLLISION_FIRSTGID
    return grid


# --- Scene hooks -------------------------------------------------------------
SPAWN_COL, SPAWN_ROW = 13, 13
NPC_SPAWNS = [
    {
        "id": "pedro_vecino",
        "name": "Pedro",
        "dialogue": "¡Ey, compa! Necesito unas cosas para armar el primer carrito. ¿Me das una mano?",
        "position": [12, 13],
    }
]
# material_id values MUST stay cardboard/wire/bottle_caps (tutorial_first_cart quest).
PICKUP_SPAWNS = [
    {"id": "pickup_carton", "material_id": "cardboard", "display_name": "Cartón limpio",
     "quantity": 1, "position": [12, 6]},
    {"id": "pickup_alambre", "material_id": "wire", "display_name": "Alambre",
     "quantity": 1, "position": [6, 12]},
    {"id": "pickup_chapitas", "material_id": "bottle_caps", "display_name": "Chapitas",
     "quantity": 1, "position": [12, 17]},
]


# --- TMX authoring -----------------------------------------------------------


def ground_gids(ground: list[list[str]]) -> list[int]:
    index_of = {tid: i for i, tid in enumerate(CURATED_TUTORIAL_TILES)}
    return [GROUND_FIRSTGID + index_of[tile_id] for row in ground for tile_id in row]


def prop_object_xml(props: list[dict]) -> tuple[list[str], int]:
    prop_index = {pid: i for i, pid in enumerate(PROP_TILES)}
    # Back-to-front so nearer props occlude farther ones in Tiled too.
    ordered = sorted(props, key=lambda p: (p["row"] + p["col"], p["row"]))
    lines: list[str] = []
    object_id = 1
    for prop in ordered:
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


def point_object_xml(object_id: int, name: str, col: int, row: int, props: dict[str, object]) -> str:
    x = (col + 0.5) * TH
    y = (row + 0.5) * TH
    prop_lines = []
    for key, value in props.items():
        if isinstance(value, int):
            prop_lines.append(f'<property name="{key}" type="int" value="{value}"/>')
        else:
            prop_lines.append(f'<property name="{key}" value="{value}"/>')
    inner = f"<properties>{''.join(prop_lines)}</properties>" if prop_lines else ""
    return f'  <object id="{object_id}" name="{name}" x="{x:.2f}" y="{y:.2f}">{inner}</object>'


def zone_object_xml(object_id: int, zone: dict) -> str:
    x = zone["col"] * TH
    y = zone["row"] * TH
    w = zone["width"] * TH
    h = zone["height"] * TH
    return f'  <object id="{object_id}" x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"/>'


def write_tmx(ground, props, collision_cells, collision_zones) -> None:
    encoded_ground = encode_layer_data(ground_gids(ground))
    empty_layer = encode_layer_data([0] * (SIZE * SIZE))
    encoded_collision = encode_layer_data(collision_layer_gids(collision_cells))
    object_lines, next_id = prop_object_xml(props)

    spawn_line = point_object_xml(next_id, "tutorial_spawn", SPAWN_COL, SPAWN_ROW, {"facing": "south"})
    next_id += 1

    npc_lines = []
    for npc in NPC_SPAWNS:
        col, row = npc["position"]
        npc_lines.append(point_object_xml(next_id, npc["id"], col, row,
                                          {"display_name": npc["name"], "dialogue": npc["dialogue"]}))
        next_id += 1

    pickup_lines = []
    for pickup in PICKUP_SPAWNS:
        col, row = pickup["position"]
        pickup_lines.append(point_object_xml(next_id, pickup["id"], col, row, {
            "display_name": pickup["display_name"],
            "material_id": pickup["material_id"],
            "quantity": pickup["quantity"],
        }))
        next_id += 1

    zone_lines = []
    for zone in collision_zones:
        zone_lines.append(zone_object_xml(next_id, zone))
        next_id += 1

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<map version="1.10" tiledversion="1.10.2" '
            'orientation="isometric" renderorder="right-down" '
            f'width="{SIZE}" height="{SIZE}" tilewidth="{TW}" tileheight="{TH}" '
            f'infinite="0" nextlayerid="10" nextobjectid="{next_id}">'
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
        f' <layer id="6" name="collision" width="{SIZE}" height="{SIZE}" x="0" y="0" opacity="0.55">',
        f'  <data encoding="base64">{encoded_collision}</data>',
        " </layer>",
        ' <objectgroup id="4" name="props">',
        *object_lines,
        " </objectgroup>",
        ' <objectgroup id="5" name="spawn">',
        spawn_line,
        " </objectgroup>",
        ' <objectgroup id="8" name="npcs">',
        *npc_lines,
        " </objectgroup>",
        ' <objectgroup id="9" name="pickups">',
        *pickup_lines,
        " </objectgroup>",
        ' <objectgroup id="7" name="collision_zones">',
        *zone_lines,
        " </objectgroup>",
        "</map>",
    ]

    out = MAP_DIR / f"{MAP_ID}.tmx"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(props)} props, {len(collision_zones)} zones)")


# --- QC preview --------------------------------------------------------------


def category(tile_id: str) -> str:
    if tile_id.startswith("road_"):
        return "roads"
    if tile_id.startswith("sidewalk_"):
        return "sidewalks"
    return "terrain"


def render_preview(ground: list[list[str]], props: list[dict]) -> None:
    side_margin = 64
    top_margin = 420
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
    collision_cells = build_collision_cells(props)
    collision_zones = build_collision_zones(props)
    # Keep the props tileset in sync with PROP_TILES (picks up new buildings).
    write_props_tileset(MAP_DIR / "props_tutorial.tsx", PROP_TILES)
    write_tmx(ground, props, collision_cells, collision_zones)
    render_preview(ground, props)
    print(
        "Now run: python tools/tiled_export/export_layout.py "
        f"data/maps/{MAP_ID}/{MAP_ID}.tmx"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
