#!/usr/bin/env python3
"""Convert a flat texture into a frame-filling isometric 2:1 diamond tile.

Deterministic postprocessor (NOT an art generator): it takes a raw texture
produced by image generation, resizes it to the 256x128 tile frame, and
applies a 2:1 diamond alpha mask so the visible content is a perfect
isometric diamond that snaps to the map grid with no gaps and no overhang.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
TILE_WIDTH = 256
TILE_HEIGHT = 128
MAGENTA = np.array([255, 0, 255], dtype=np.float32)
CHROMA_THRESHOLD = 90.0


def category_for_tile_id(tile_id: str) -> str:
    if tile_id.startswith("road_"):
        return "roads"
    if tile_id.startswith("sidewalk_"):
        return "sidewalks"
    if tile_id.startswith("curb_"):
        return "curbs"
    if tile_id.startswith("marking_"):
        return "markings"
    if tile_id.startswith("transition_"):
        return "transitions"
    return "terrain"


def diamond_coverage(width: int, height: int, supersample: int = 4) -> np.ndarray:
    """Antialiased 2:1 diamond mask in [0, 1] via supersampling."""
    high_width = width * supersample
    high_height = height * supersample
    center_x = (high_width - 1) / 2.0
    center_y = (high_height - 1) / 2.0
    half_width = high_width / 2.0
    half_height = high_height / 2.0

    xs = np.arange(high_width, dtype=np.float32)
    ys = np.arange(high_height, dtype=np.float32)
    grid_x, grid_y = np.meshgrid(xs, ys)

    manhattan = np.abs(grid_x - center_x) / half_width + np.abs(grid_y - center_y) / half_height
    inside = (manhattan <= 1.0).astype(np.float32)

    coverage = inside.reshape(height, supersample, width, supersample).mean(axis=(1, 3))
    return coverage


def strip_magenta_alpha(rgba: np.ndarray) -> np.ndarray:
    rgb = rgba[:, :, :3].astype(np.float32)
    distance = np.sqrt(np.sum((rgb - MAGENTA) ** 2, axis=2))
    keep = distance > CHROMA_THRESHOLD
    rgba[:, :, 3] = np.where(keep, rgba[:, :, 3], 0).astype(np.uint8)
    return rgba


def trim_to_content(source: Image.Image) -> Image.Image:
    """Crop to the bounding box of visible content (alpha or non-black)."""
    data = np.array(source)
    alpha = data[:, :, 3]
    if int(alpha.min()) < 250:
        mask = alpha > 16
    else:
        luminance = data[:, :, :3].max(axis=2)
        mask = luminance > 24
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any() or not cols.any():
        return source
    top, bottom = np.where(rows)[0][[0, -1]]
    left, right = np.where(cols)[0][[0, -1]]
    return source.crop((int(left), int(top), int(right) + 1, int(bottom) + 1))


def build_tile(
    input_path: Path,
    fill_frame: bool = True,
    trim: bool = False,
) -> Image.Image:
    source = Image.open(input_path).convert("RGBA")

    if trim:
        source = trim_to_content(source)

    if fill_frame:
        # Squash whole texture into the tile frame; diamond mask defines shape.
        resized = source.resize((TILE_WIDTH, TILE_HEIGHT), Image.Resampling.LANCZOS)
    else:
        # Preserve source aspect via center-crop to 2:1, then resize.
        source_ratio = source.width / source.height
        target_ratio = TILE_WIDTH / TILE_HEIGHT
        if source_ratio > target_ratio:
            new_width = int(source.height * target_ratio)
            left = (source.width - new_width) // 2
            source = source.crop((left, 0, left + new_width, source.height))
        else:
            new_height = int(source.width / target_ratio)
            top = (source.height - new_height) // 2
            source = source.crop((0, top, source.width, top + new_height))
        resized = source.resize((TILE_WIDTH, TILE_HEIGHT), Image.Resampling.LANCZOS)

    data = np.array(resized)
    data = strip_magenta_alpha(data)

    coverage = diamond_coverage(TILE_WIDTH, TILE_HEIGHT)
    source_alpha = data[:, :, 3].astype(np.float32) / 255.0
    final_alpha = np.clip(source_alpha * coverage, 0.0, 1.0)
    data[:, :, 3] = (final_alpha * 255.0).astype(np.uint8)

    return Image.fromarray(data, "RGBA")


def write_meta(output_path: Path, tile_id: str) -> None:
    category = category_for_tile_id(tile_id)
    variant_token = tile_id.rsplit("_", 1)[-1]
    variant = int(variant_token) if variant_token.isdigit() else 1
    meta = {
        "id": tile_id,
        "category": category,
        "variant": variant,
        "pack": "environment_base_pack_01",
        "pivot": [0.5, 0.5],
        "size_pixels": [TILE_WIDTH, TILE_HEIGHT],
        "size_units": [1.0, 0.5],
        "projection": "isometric_2_1",
        "status": "qc_pass",
        "connections": {},
    }
    output_path.with_suffix(".meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )


def resolve_output(tile_id: str) -> Path:
    category = category_for_tile_id(tile_id)
    return REPO_ROOT / "assets" / "environment" / category / f"{tile_id}.png"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build isometric diamond tile")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--tile-id", required=True)
    parser.add_argument(
        "--no-fill-frame",
        action="store_true",
        help="Preserve source aspect (center-crop) instead of squashing to frame.",
    )
    parser.add_argument(
        "--trim",
        action="store_true",
        help="Crop to visible content bbox before resizing (for padded sources).",
    )
    parser.add_argument("--output", type=Path, help="Override output PNG path.")
    args = parser.parse_args()

    input_path = args.input if args.input.is_absolute() else REPO_ROOT / args.input
    tile = build_tile(input_path, fill_frame=not args.no_fill_frame, trim=args.trim)

    output_path = args.output or resolve_output(args.tile_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tile.save(output_path)
    write_meta(output_path, args.tile_id)

    print(f"Wrote {output_path} ({tile.width}x{tile.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
