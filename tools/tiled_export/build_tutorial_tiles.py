#!/usr/bin/env python3
"""Build the curated tutorial isometric tileset from raw textures.

Runs the deterministic diamond masker over freshly generated road/sidewalk
textures (full-bleed) and over the existing grass tiles (trimmed), producing
frame-filling isometric 2:1 diamonds that snap to the map grid.
"""

from __future__ import annotations

import sys
from pathlib import Path

from make_iso_diamond_tile import build_tile, resolve_output, write_meta

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = Path(
    r"C:/Users/tecnova/.cursor/projects/c-Users-tecnova-Desktop-barriolibre/assets"
)
TERRAIN_DIR = REPO_ROOT / "assets" / "environment" / "terrain"

# tile_id -> (source_path, trim)
GENERATED = {
    "road_straight_h_01": (RAW_DIR / "raw_road_straight_h.png", False),
    "road_straight_v_01": (RAW_DIR / "raw_road_straight_v.png", False),
    "road_corner_ne_01": (RAW_DIR / "raw_road_corner_ne.png", False),
    "road_corner_nw_01": (RAW_DIR / "raw_road_corner_nw.png", False),
    "road_corner_se_01": (RAW_DIR / "raw_road_corner_se.png", False),
    "road_corner_sw_01": (RAW_DIR / "raw_road_corner_sw.png", False),
    "road_cross_01": (RAW_DIR / "raw_road_cross.png", False),
    "road_plain_01": (RAW_DIR / "raw_road_plain.png", False),
    "sidewalk_straight_01": (RAW_DIR / "raw_sidewalk_straight.png", False),
}

GRASS = {
    "grass_clean_01": (TERRAIN_DIR / "grass_clean_01.png", True),
    "grass_clean_02": (TERRAIN_DIR / "grass_clean_02.png", True),
    "grass_clean_03": (TERRAIN_DIR / "grass_clean_03.png", True),
    "grass_clean_04": (TERRAIN_DIR / "grass_clean_04.png", True),
}


def process(tile_id: str, source: Path, trim: bool) -> None:
    if not source.exists():
        print(f"SKIP {tile_id}: missing source {source}")
        return
    tile = build_tile(source, fill_frame=True, trim=trim)
    output = resolve_output(tile_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    tile.save(output)
    write_meta(output, tile_id)
    print(f"OK  {tile_id} <- {source.name} (bbox {tile.getbbox()})")


def main() -> int:
    for tile_id, (source, trim) in {**GRASS, **GENERATED}.items():
        process(tile_id, source, trim)
    print(f"\nCurated tile IDs ({len(GRASS) + len(GENERATED)}):")
    for tile_id in [*GRASS, *GENERATED]:
        print(tile_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
