#!/usr/bin/env python3
"""Compose a small isometric preview to QC diamond tile fit (no gaps)."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV = REPO_ROOT / "assets" / "environment"
TW, TH = 256, 128

LAYOUT = [
    ["grass_clean_01", "grass_clean_02", "road_straight_h_01", "grass_clean_03"],
    ["grass_clean_02", "road_corner_ne_01", "road_cross_01", "road_corner_nw_01"],
    ["road_straight_v_01", "road_cross_01", "sidewalk_straight_01", "road_straight_v_01"],
    ["grass_clean_03", "road_corner_se_01", "road_straight_h_01", "road_corner_sw_01"],
]


def category(tile_id: str) -> str:
    if tile_id.startswith("road_"):
        return "roads"
    if tile_id.startswith("sidewalk_"):
        return "sidewalks"
    return "terrain"


def path_for(tile_id: str) -> Path:
    return ENV / category(tile_id) / f"{tile_id}.png"


def main() -> int:
    rows = len(LAYOUT)
    cols = len(LAYOUT[0])
    margin = 64
    canvas_w = (cols + rows) * (TW // 2) + margin * 2
    canvas_h = (cols + rows) * (TH // 2) + margin * 2
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (40, 40, 52, 255))

    origin_x = margin + rows * (TW // 2) - TW // 2
    origin_y = margin

    for gy, row in enumerate(LAYOUT):
        for gx, tile_id in enumerate(row):
            tile = Image.open(path_for(tile_id)).convert("RGBA")
            screen_x = origin_x + (gx - gy) * (TW // 2)
            screen_y = origin_y + (gx + gy) * (TH // 2)
            canvas.alpha_composite(tile, (screen_x, screen_y))

    out = REPO_ROOT / "data" / "maps" / "barrio_tutorial_01" / "_preview_iso.png"
    canvas.save(out)
    print(f"Wrote {out} ({canvas.size[0]}x{canvas.size[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
