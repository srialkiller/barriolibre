#!/usr/bin/env python3
"""Turn magenta-background generated prop art into game-ready transparent PNGs.

For each ``prop_id`` it takes a raw generated image (solid magenta #FF00FF
background), chroma-keys the background, tight-crops to the sprite bounds,
optionally downscales, and writes to ``assets/environment/props/<prop_id>.png``
(the exact path/ID the runtime already loads — no code change needed).

Usage:
    python tools/tiled_export/regen_props.py house_red_01 [house_blue_01 ...]
    python tools/tiled_export/regen_props.py --all

Raw art is read from ``assets/gen_<prop_id>.png`` by default.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_SCRIPTS = Path.home() / ".codex" / "skills" / "generate2dsprite" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
from generate2dsprite import remove_bg_magenta  # noqa: E402

PROPS_DIR = REPO_ROOT / "assets" / "environment" / "props"
# GenerateImage writes into the Cursor project assets folder, not the repo.
GEN_DIR = (
    Path.home()
    / ".cursor"
    / "projects"
    / "c-Users-tecnova-Desktop-barriolibre"
    / "assets"
)

PROP_IDS = [
    "house_red_01",
    "house_blue_01",
    "house_yellow_01",
    "house_wood_01",
    "tree_01",
    "lamp_01",
    "bench_01",
    "fountain_01",
    "hydrant_01",
    "garage_01",
    "shop_01",
]

MAX_DIM = 512  # cap the stored sprite so files stay light but crisp


def raw_path(prop_id: str) -> Path:
    return GEN_DIR / f"gen_{prop_id}.png"


def process(prop_id: str, threshold: int, edge_threshold: int, raw: Path | None = None) -> None:
    src = raw or raw_path(prop_id)
    if not src.exists():
        print(f"  ! {prop_id}: raw art not found at {src}")
        return
    img = Image.open(src).convert("RGBA")
    img = remove_bg_magenta(img, threshold=threshold, edge_threshold=edge_threshold)
    bbox = img.getbbox()
    if bbox is None:
        print(f"  ! {prop_id}: image is empty after chroma key")
        return
    img = img.crop(bbox)
    w, h = img.size
    if max(w, h) > MAX_DIM:
        scale = MAX_DIM / max(w, h)
        img = img.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.Resampling.LANCZOS)
    out = PROPS_DIR / f"{prop_id}.png"
    img.save(out)
    print(f"  ok {prop_id}: {out.name} ({img.size[0]}x{img.size[1]})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prop_ids", nargs="*", help="Prop IDs to (re)process")
    parser.add_argument("--all", action="store_true", help="Process every known prop id")
    parser.add_argument("--raw", type=Path, help="Explicit raw image path (single prop only)")
    parser.add_argument("--threshold", type=int, default=110)
    parser.add_argument("--edge-threshold", type=int, default=170)
    args = parser.parse_args()

    ids = PROP_IDS if args.all else args.prop_ids
    if not ids:
        parser.error("pass prop ids or --all")
    if args.raw and len(ids) != 1:
        parser.error("--raw can only be used with exactly one prop id")
    for prop_id in ids:
        process(prop_id, args.threshold, args.edge_threshold, raw=args.raw)
    return 0


if __name__ == "__main__":
    sys.exit(main())
