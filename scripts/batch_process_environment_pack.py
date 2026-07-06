#!/usr/bin/env python3
"""Batch process generated raw environment tiles into production pack."""

from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from process_environment_tile import process_single, process_grid  # noqa: E402

RAW = ROOT / "assets/environment/_raw"
ENV = ROOT / "assets/environment"
PROMPTS = ROOT / "assets/environment/_prompts"

SINGLE_TILES = [
    ("road_straight_h_01_raw.png", "roads/road_straight_h_01.png", "road_straight_h_01", "roads", 1,
     {"east": "road", "west": "road"}),
    ("road_straight_v_01_raw.png", "roads/road_straight_v_01.png", "road_straight_v_01", "roads", 1,
     {"north": "road", "south": "road"}),
    ("road_corner_ne_01_raw.png", "roads/road_corner_ne_01.png", "road_corner_ne_01", "roads", 1,
     {"north": "road", "east": "road"}),
    ("road_cross_01_raw.png", "roads/road_cross_01.png", "road_cross_01", "roads", 1,
     {"north": "road", "south": "road", "east": "road", "west": "road"}),
    ("road_deadend_01_raw.png", "roads/road_deadend_01.png", "road_deadend_01", "roads", 1,
     {"south": "road"}),
    ("road_tjunction_n_01_raw.png", "roads/road_tjunction_n_01.png", "road_tjunction_n_01", "roads", 1,
     {"north": "road", "east": "road", "west": "road"}),
    ("sidewalk_straight_01_raw.png", "sidewalks/sidewalk_straight_01.png", "sidewalk_straight_01", "sidewalks", 1,
     {"east": "sidewalk", "west": "sidewalk"}),
    ("transition_road_grass_01_raw.png", "transitions/transition_road_grass_01.png", "transition_road_grass_01", "transitions", 1,
     {"north": "road", "south": "grass"}),
]

GRID_PACKS = [
    {
        "raw": "grass_clean_pack_raw.png",
        "output_dir": "terrain",
        "category": "terrain",
        "ids": [f"grass_clean_{i:02d}" for i in range(1, 10)],
        "rows": 3,
        "cols": 3,
    },
    {
        "raw": "road_straight_h_variants_raw.png",
        "output_dir": "roads",
        "category": "roads",
        "ids": [f"road_straight_h_{i:02d}" for i in range(1, 10)],
        "rows": 3,
        "cols": 3,
    },
]


def copy_prompt(tile_id: str, category: str, output_png: Path) -> None:
    prompt_src = PROMPTS / category / f"{tile_id}.prompt.txt"
    if prompt_src.exists():
        shutil.copy(prompt_src, output_png.with_suffix(".prompt.txt"))


def main() -> None:
    processed = []
    for raw_name, out_rel, tile_id, category, variant, connections in SINGLE_TILES:
        raw_path = RAW / raw_name
        if not raw_path.exists():
            print(f"SKIP missing: {raw_name}")
            continue
        out_path = ENV / out_rel
        process_single(raw_path, out_path, tile_id, category, variant, connections)
        copy_prompt(tile_id, category, out_path)
        processed.append(tile_id)
        print(f"OK single: {tile_id}")

    for pack in GRID_PACKS:
        raw_path = RAW / pack["raw"]
        if not raw_path.exists():
            print(f"SKIP missing grid: {pack['raw']}")
            continue
        out_dir = ENV / pack["output_dir"]
        process_grid(raw_path, out_dir, pack["ids"], pack["category"], pack["rows"], pack["cols"])
        for tile_id in pack["ids"]:
            copy_prompt(tile_id, pack["category"], out_dir / f"{tile_id}.png")
            processed.append(tile_id)
        print(f"OK grid: {pack['raw']} -> {len(pack['ids'])} tiles")

    print(f"\nProcessed {len(processed)} tiles total.")
    manifest_path = ROOT / "data/tilesets/environment_base_pack_01_generated.json"
    manifest_path.write_text(json.dumps({"generated": processed, "count": len(processed)}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
