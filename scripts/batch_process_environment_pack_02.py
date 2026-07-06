#!/usr/bin/env python3
"""Process batch 2 raw environment tiles."""

from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from process_environment_tile import process_single, process_grid

RAW = ROOT / "assets/environment/_raw"
ENV = ROOT / "assets/environment"
PROMPTS = ROOT / "assets/environment/_prompts"

SINGLE_TILES = [
    ("road_corner_nw_01_raw.png", "roads/road_corner_nw_01.png", "road_corner_nw_01", "roads", 1, {"north": "road", "west": "road"}),
    ("road_corner_se_01_raw.png", "roads/road_corner_se_01.png", "road_corner_se_01", "roads", 1, {"south": "road", "east": "road"}),
    ("road_corner_sw_01_raw.png", "roads/road_corner_sw_01.png", "road_corner_sw_01", "roads", 1, {"south": "road", "west": "road"}),
    ("curb_straight_01_raw.png", "curbs/curb_straight_01.png", "curb_straight_01", "curbs", 1, {"east": "curb", "west": "curb"}),
    ("marking_paint_straight_01_raw.png", "markings/marking_paint_straight_01.png", "marking_paint_straight_01", "markings", 1, {}),
    ("marking_manhole_01_raw.png", "markings/marking_manhole_01.png", "marking_manhole_01", "markings", 1, {}),
    ("road_damaged_01_raw.png", "roads/road_damaged_01.png", "road_damaged_01", "roads", 1, {"east": "road", "west": "road"}),
    ("road_patched_01_raw.png", "roads/road_patched_01.png", "road_patched_01", "roads", 1, {"east": "road", "west": "road"}),
    ("transition_road_dirt_01_raw.png", "transitions/transition_road_dirt_01.png", "transition_road_dirt_01", "transitions", 1, {"north": "road", "south": "dirt"}),
]

GRID_PACKS = [
    ("sidewalk_straight_variants_raw.png", "sidewalks", "sidewalks", [f"sidewalk_straight_{i:02d}" for i in range(1, 10)]),
    ("dirt_compact_pack_raw.png", "terrain", "terrain", [f"dirt_compact_{i:02d}" for i in range(1, 10)]),
    ("concrete_clean_pack_raw.png", "terrain", "terrain", [f"concrete_clean_{i:02d}" for i in range(1, 10)]),
]

SRC = Path(r"C:\Users\tecnova\.cursor\projects\c-Users-tecnova-Desktop-barriolibre\assets")


def copy_prompt(tile_id: str, category: str, output_png: Path) -> None:
    prompt_src = PROMPTS / category / f"{tile_id}.prompt.txt"
    if prompt_src.exists():
        shutil.copy(prompt_src, output_png.with_suffix(".prompt.txt"))


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for name, *_ in SINGLE_TILES:
        src = SRC / name
        if src.exists():
            shutil.copy(src, RAW / name)
    for raw, *_ in GRID_PACKS:
        src = SRC / raw
        if src.exists():
            shutil.copy(src, RAW / raw)

    processed = []
    for raw_name, out_rel, tile_id, category, variant, connections in SINGLE_TILES:
        raw_path = RAW / raw_name
        if not raw_path.exists():
            print(f"SKIP {raw_name}")
            continue
        out_path = ENV / out_rel
        process_single(raw_path, out_path, tile_id, category, variant, connections)
        copy_prompt(tile_id, category, out_path)
        processed.append(tile_id)
        print(f"OK {tile_id}")

    for raw, out_dir, category, ids in GRID_PACKS:
        raw_path = RAW / raw
        if not raw_path.exists():
            print(f"SKIP grid {raw}")
            continue
        process_grid(raw_path, ENV / out_dir, ids, category, 3, 3)
        for tile_id in ids:
            copy_prompt(tile_id, category, ENV / out_dir / f"{tile_id}.png")
            processed.append(tile_id)
        print(f"OK grid {raw}")

    gen_path = ROOT / "data/tilesets/environment_base_pack_01_generated.json"
    existing = json.loads(gen_path.read_text()) if gen_path.exists() else {"generated": []}
    all_ids = sorted(set(existing.get("generated", []) + processed))
    gen_path.write_text(json.dumps({"generated": all_ids, "count": len(all_ids)}, indent=2), encoding="utf-8")
    print(f"Total in pack: {len(all_ids)}")


if __name__ == "__main__":
    main()
