#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "data/tilesets/environment_base_pack_01_manifest.json").read_text())
generated = set(json.loads((ROOT / "data/tilesets/environment_base_pack_01_generated.json").read_text())["generated"])

expected = []
for cat_name, cat in manifest["categories"].items():
    vdef = manifest["variants_per_tile"].get("terrain" if cat_name == "terrain" else "default", 3)
    for tile in cat["tiles"]:
        n = tile.get("variants", vdef)
        for i in range(1, n + 1):
            expected.append((f"{tile['id']}_{i:02d}", cat_name, tile["id"], i))

missing = [(tid, cat, base, var) for tid, cat, base, var in expected if tid not in generated]
print(f"Expected: {len(expected)}, Generated: {len(generated)}, Missing: {len(missing)}")
for tid, cat, _, _ in missing:
    print(f"{cat}|{tid}")

# Group by base tile type for batch generation
from collections import defaultdict
groups = defaultdict(list)
for tid, cat, base, var in missing:
    groups[(cat, base)].append((tid, var))
print("\n--- GROUPS ---")
for (cat, base), items in sorted(groups.items()):
    print(f"{cat}/{base}: {len(items)} variants")
