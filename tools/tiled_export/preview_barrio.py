#!/usr/bin/env python3
"""Compose an isometric preview of the barrio: ground diamonds + upright props.

QC helper only. Renders a small scene echoing the reference map so we can verify
the new road tiles, crosswalks and props read correctly together (depth sort,
bottom-center anchoring, clean alpha edges).
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV = REPO_ROOT / "assets" / "environment"
TW, TH = 256, 128

G1, G2, G3, G4 = ("grass_clean_01", "grass_clean_02", "grass_clean_03", "grass_clean_04")

# 8x8 ground grid: a cross of roads with crosswalks, grass quadrants elsewhere.
GROUND = [
    [G1, G2, G3, "road_straight_v_01", G4, G1, G2, G3],
    [G2, G3, G4, "road_straight_v_01", G1, G2, G3, G4],
    [G3, G4, G1, "road_crosswalk_v_01", G2, G3, G4, G1],
    ["road_straight_h_01", "road_straight_h_01", "road_crosswalk_h_01", "road_cross_01", "road_crosswalk_h_01", "road_straight_h_01", "road_straight_h_01", "road_straight_h_01"],
    [G1, G2, G3, "road_crosswalk_v_01", G4, G1, G2, G3],
    [G2, G3, G4, "road_straight_v_01", G1, G2, G3, G4],
    [G3, G4, G1, "road_straight_v_01", G2, G3, G4, G1],
    [G4, G1, G2, "road_straight_v_01", G3, G4, G1, G2],
]

# Props as (prop_id, col, row) placed on grass cells.
PROPS = [
    ("house_red_01", 1.0, 1.0),
    ("house_blue_01", 5.5, 1.0),
    ("house_yellow_01", 1.0, 5.5),
    ("house_wood_01", 6.0, 5.5),
    ("tree_01", 6.0, 1.0),
    ("tree_01", 1.0, 6.5),
    ("tree_01", 4.5, 4.5),
    ("fountain_01", 5.0, 5.0),
    ("bench_01", 4.5, 6.0),
    ("lamp_01", 2.2, 2.2),
    ("lamp_01", 2.2, 4.2),
    ("hydrant_01", 4.2, 2.2),
]


def category(tile_id: str) -> str:
    if tile_id.startswith("road_"):
        return "roads"
    if tile_id.startswith("sidewalk_"):
        return "sidewalks"
    return "terrain"


def ground_path(tile_id: str) -> Path:
    return ENV / category(tile_id) / f"{tile_id}.png"


def prop_path(prop_id: str) -> Path:
    return ENV / "props" / f"{prop_id}.png"


def main() -> int:
    rows = len(GROUND)
    cols = len(GROUND[0])
    side_margin = 64
    top_margin = 700
    bottom_margin = 96

    canvas_w = (cols + rows) * (TW // 2) + side_margin * 2
    canvas_h = (cols + rows) * (TH // 2) + top_margin + bottom_margin
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (36, 38, 48, 255))

    origin_x = side_margin + rows * (TW // 2) - TW // 2
    origin_y = top_margin

    def cell_center(col: float, row: float) -> tuple[float, float]:
        cx = origin_x + (col - row) * (TW / 2) + TW / 2
        cy = origin_y + (col + row) * (TH / 2) + TH / 2
        return cx, cy

    for gy, row in enumerate(GROUND):
        for gx, tile_id in enumerate(row):
            tile = Image.open(ground_path(tile_id)).convert("RGBA")
            screen_x = origin_x + (gx - gy) * (TW // 2)
            screen_y = origin_y + (gx + gy) * (TH // 2)
            canvas.alpha_composite(tile, (screen_x, screen_y))

    for prop_id, col, row in sorted(PROPS, key=lambda p: (p[1] + p[2], p[2])):
        prop = Image.open(prop_path(prop_id)).convert("RGBA")
        cx, cy = cell_center(col, row)
        paste_x = round(cx - prop.width / 2)
        paste_y = round(cy - prop.height)
        canvas.alpha_composite(prop, (paste_x, paste_y))

    out = REPO_ROOT / "data" / "maps" / "barrio_tutorial_01" / "_preview_barrio.png"
    canvas.save(out)
    print(f"Wrote {out} ({canvas.size[0]}x{canvas.size[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
