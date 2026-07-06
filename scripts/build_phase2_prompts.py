#!/usr/bin/env python3
"""Build image_gen prompts for phase 2 grid packs."""

from __future__ import annotations

import json
from pathlib import Path

from environment_tile_prompts import TILE_SPECS, BASE_PROMPT
from phase2_pack_definitions import GRID_PACKS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/environment/_prompts_phase2"


def grid_prompt(pack) -> str:
    base = pack.tile_base
    spec = TILE_SPECS.get(base, "")
    ids = pack.tile_ids
    n = len(ids)
    variant_lines = "\n".join(f"Cell {i+1}: {tid}" for i, tid in enumerate(ids))

    return f"""{BASE_PROMPT}

{spec}

SPRITE SHEET: exactly {n} equal cells in {pack.rows} rows x {pack.cols} columns grid.
Each cell is one isometric diamond tile 256x128 aspect inside its cell.
ALL cells show the SAME tile connectivity/shape type: {base}
Only texture/detail/color varies between cells.

{variant_lines}

CRITICAL: identical camera, scale, lighting, edge alignment across all cells.
NO borders between cells. NO text. Solid magenta #FF00FF between cells and outside.
Do not make pixel art. Clean HD hand-painted cartoon Carreras de Barrio tileset.
"""


def main() -> None:
    manifest = []
    for pack in GRID_PACKS:
        prompt = grid_prompt(pack)
        path = OUT / f"{pack.raw_name.replace('.png', '.prompt.txt')}"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(prompt, encoding="utf-8")
        manifest.append({
            "raw_name": pack.raw_name,
            "category": pack.category,
            "tile_ids": pack.tile_ids,
            "rows": pack.rows,
            "cols": pack.cols,
            "prompt_file": str(path.relative_to(ROOT)),
        })
    (ROOT / "data/tilesets/phase2_generation_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(f"Wrote {len(manifest)} phase2 grid prompts")


if __name__ == "__main__":
    main()
