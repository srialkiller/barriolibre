#!/usr/bin/env python3
"""Export all ENVIRONMENT_BASE_PACK_01 prompt files."""

from __future__ import annotations

import json
from pathlib import Path

from environment_tile_prompts import build_prompt

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/tilesets/environment_base_pack_01_manifest.json"
PROMPTS_DIR = ROOT / "assets/environment/_prompts"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    count = 0
    for category_name, category in manifest["categories"].items():
        variants_default = manifest["variants_per_tile"].get(
            "terrain" if category_name == "terrain" else "default", 3
        )
        for tile in category["tiles"]:
            tile_id = tile["id"]
            variant_count = tile.get("variants", variants_default)
            for variant in range(1, variant_count + 1):
                full_id = f"{tile_id}_{variant:02d}"
                prompt = build_prompt(tile_id, variant)
                path = PROMPTS_DIR / category_name / f"{full_id}.prompt.txt"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(prompt, encoding="utf-8")
                count += 1
    print(f"Exported {count} prompt files to {PROMPTS_DIR}")


if __name__ == "__main__":
    main()
