#!/usr/bin/env python3
"""Process all phase 2 environment grid packs."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from phase2_pack_definitions import GRID_PACKS, CONNECTIONS
from process_environment_tile import chroma_key_to_alpha, resize_to_tile, write_meta

RAW = ROOT / "assets/environment/_raw"
ENV = ROOT / "assets/environment"
PROMPTS = ROOT / "assets/environment/_prompts"
CURSOR_ASSETS = Path(r"C:\Users\tecnova\.cursor\projects\c-Users-tecnova-Desktop-barriolibre\assets")


def extract_grid_limited(image_path: Path, rows: int, cols: int, count: int):
    from PIL import Image
    import numpy as np

    image = Image.open(image_path)
    width, height = image.size
    cell_w = width // cols
    cell_h = height // rows
    tiles = []
    for row in range(rows):
        for col in range(cols):
            if len(tiles) >= count:
                break
            left = col * cell_w
            top = row * cell_h
            cell = image.crop((left, top, left + cell_w, top + cell_h))
            cell = resize_to_tile(cell)
            tiles.append(chroma_key_to_alpha(cell))
        if len(tiles) >= count:
            break
    return tiles


def copy_prompt(tile_id: str, category: str, dest: Path) -> None:
    src = PROMPTS / category / f"{tile_id}.prompt.txt"
    if src.exists():
        shutil.copy(src, dest.with_suffix(".prompt.txt"))


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    processed: list[str] = []

    for pack in GRID_PACKS:
        raw_path = RAW / pack.raw_name
        cursor_path = CURSOR_ASSETS / pack.raw_name
        if not raw_path.exists() and cursor_path.exists():
            shutil.copy(cursor_path, raw_path)
        if not raw_path.exists():
            print(f"MISSING {pack.raw_name}")
            continue

        tiles = extract_grid_limited(raw_path, pack.rows, pack.cols, len(pack.tile_ids))
        if len(tiles) != len(pack.tile_ids):
            print(f"FAIL {pack.raw_name}: got {len(tiles)} expected {len(pack.tile_ids)}")
            continue

        out_dir = ENV / pack.category
        connections = CONNECTIONS.get(pack.tile_base, {})
        for tile_id, tile_img in zip(pack.tile_ids, tiles):
            out_path = out_dir / f"{tile_id}.png"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            tile_img.save(out_path)
            variant = int(tile_id.rsplit("_", 1)[-1])
            write_meta(out_path, tile_id, pack.category, variant, connections)
            copy_prompt(tile_id, pack.category, out_path)
            processed.append(tile_id)

        print(f"OK {pack.raw_name} -> {len(pack.tile_ids)} tiles")

    gen_path = ROOT / "data/tilesets/environment_base_pack_01_generated.json"
    existing = json.loads(gen_path.read_text(encoding="utf-8"))
    all_ids = sorted(set(existing["generated"] + processed))
    gen_path.write_text(
        json.dumps({"generated": all_ids, "count": len(all_ids)}, indent=2),
        encoding="utf-8",
    )
    print(f"\nPhase 2 added: {len(processed)} | Total pack: {len(all_ids)}")


if __name__ == "__main__":
    main()
