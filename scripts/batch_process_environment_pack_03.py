#!/usr/bin/env python3
"""Process batch 3 raw environment tiles."""

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
SRC = Path(r"C:\Users\tecnova\.cursor\projects\c-Users-tecnova-Desktop-barriolibre\assets")

SINGLE = [
    ("road_tjunction_s_01_raw.png", "roads/road_tjunction_s_01.png", "road_tjunction_s_01", "roads", {"south": "road", "east": "road", "west": "road"}),
    ("road_narrow_01_raw.png", "roads/road_narrow_01.png", "road_narrow_01", "roads", {"east": "road", "west": "road"}),
    ("road_wide_01_raw.png", "roads/road_wide_01.png", "road_wide_01", "roads", {"east": "road", "west": "road"}),
    ("transition_grass_dirt_01_raw.png", "transitions/transition_grass_dirt_01.png", "transition_grass_dirt_01", "transitions", {"north": "grass", "south": "dirt"}),
]

GRIDS = [
    ("grass_dry_pack_raw.png", "terrain", [f"grass_dry_{i:02d}" for i in range(1, 10)]),
    ("gravel_pack_raw.png", "terrain", [f"gravel_{i:02d}" for i in range(1, 10)]),
]


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    processed = []
    for raw, out, tid, cat, conn in SINGLE:
        if (SRC / raw).exists():
            shutil.copy(SRC / raw, RAW / raw)
        rp = RAW / raw
        if not rp.exists():
            continue
        op = ENV / out
        process_single(rp, op, tid, cat, 1, conn)
        ps = PROMPTS / cat / f"{tid}.prompt.txt"
        if ps.exists():
            shutil.copy(ps, op.with_suffix(".prompt.txt"))
        processed.append(tid)
        print(f"OK {tid}")

    for raw, cat, ids in GRIDS:
        if (SRC / raw).exists():
            shutil.copy(SRC / raw, RAW / raw)
        rp = RAW / raw
        if not rp.exists():
            continue
        od = ENV / cat
        process_grid(rp, od, ids, cat, 3, 3)
        for tid in ids:
            ps = PROMPTS / cat / f"{tid}.prompt.txt"
            if ps.exists():
                shutil.copy(ps, od / f"{tid}.prompt.txt")
            processed.append(tid)
        print(f"OK grid {raw}")

    gp = ROOT / "data/tilesets/environment_base_pack_01_generated.json"
    existing = json.loads(gp.read_text()) if gp.exists() else {"generated": []}
    all_ids = sorted(set(existing["generated"] + processed))
    gp.write_text(json.dumps({"generated": all_ids, "count": len(all_ids)}, indent=2), encoding="utf-8")
    print(f"Total: {len(all_ids)}")


if __name__ == "__main__":
    main()
