#!/usr/bin/env python3
"""Postprocess environment isometric tiles for Carreras de Barrio."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

TILE_WIDTH = 256
TILE_HEIGHT = 128
MAGENTA = np.array([255, 0, 255], dtype=np.uint8)
CHROMA_THRESHOLD = 100


def chroma_key_to_alpha(image: Image.Image, threshold: int = CHROMA_THRESHOLD) -> Image.Image:
    rgba = image.convert("RGBA")
    data = np.array(rgba)
    rgb = data[:, :, :3].astype(np.float32)
    dist = np.sqrt(np.sum((rgb - MAGENTA.astype(np.float32)) ** 2, axis=2))
    alpha = np.where(dist <= threshold, 0, data[:, :, 3])
    data[:, :, 3] = alpha.astype(np.uint8)
    return Image.fromarray(data, "RGBA")


def resize_to_tile(image: Image.Image) -> Image.Image:
    return image.resize((TILE_WIDTH, TILE_HEIGHT), Image.Resampling.LANCZOS)


def extract_grid(
    image: Image.Image,
    rows: int,
    cols: int,
    threshold: int = CHROMA_THRESHOLD,
) -> list[Image.Image]:
    width, height = image.size
    cell_width = width // cols
    cell_height = height // rows
    tiles: list[Image.Image] = []
    for row in range(rows):
        for col in range(cols):
            left = col * cell_width
            top = row * cell_height
            cell = image.crop((left, top, left + cell_width, top + cell_height))
            cell = resize_to_tile(cell)
            tiles.append(chroma_key_to_alpha(cell, threshold))
    return tiles


def write_meta(output_path: Path, tile_id: str, category: str, variant: int, connections: dict | None = None) -> None:
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
        "connections": connections or {},
    }
    meta_path = output_path.with_suffix(".meta.json")
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def process_single(input_path: Path, output_path: Path, tile_id: str, category: str, variant: int, connections: dict | None) -> None:
    image = Image.open(input_path)
    processed = chroma_key_to_alpha(resize_to_tile(image))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    processed.save(output_path)
    prompt_src = input_path.with_suffix(".prompt.txt")
    if prompt_src.exists():
        output_path.with_suffix(".prompt.txt").write_text(prompt_src.read_text(encoding="utf-8"), encoding="utf-8")
    write_meta(output_path, tile_id, category, variant, connections)


def process_grid(
    input_path: Path,
    output_dir: Path,
    tile_ids: list[str],
    category: str,
    rows: int,
    cols: int,
) -> None:
    image = Image.open(input_path)
    tiles = extract_grid(image, rows, cols)
    if len(tiles) != len(tile_ids):
        raise ValueError(f"Expected {len(tile_ids)} tiles, got {len(tiles)}")
    for tile_id, tile_image in zip(tile_ids, tiles):
        output_path = output_dir / f"{tile_id}.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tile_image.save(output_path)
        variant = int(tile_id.rsplit("_", 1)[-1])
        write_meta(output_path, tile_id, category, variant)


def main() -> int:
    parser = argparse.ArgumentParser(description="Process environment tiles")
    sub = parser.add_subparsers(dest="command", required=True)

    single = sub.add_parser("single")
    single.add_argument("--input", type=Path, required=True)
    single.add_argument("--output", type=Path, required=True)
    single.add_argument("--id", required=True)
    single.add_argument("--category", required=True)
    single.add_argument("--variant", type=int, default=1)
    single.add_argument("--connections", type=Path)

    grid = sub.add_parser("grid")
    grid.add_argument("--input", type=Path, required=True)
    grid.add_argument("--output-dir", type=Path, required=True)
    grid.add_argument("--ids", nargs="+", required=True)
    grid.add_argument("--category", required=True)
    grid.add_argument("--rows", type=int, required=True)
    grid.add_argument("--cols", type=int, required=True)

    args = parser.parse_args()
    if args.command == "single":
        connections = json.loads(args.connections.read_text()) if args.connections else None
        process_single(args.input, args.output, args.id, args.category, args.variant, connections)
    elif args.command == "grid":
        process_grid(args.input, args.output_dir, args.ids, args.category, args.rows, args.cols)
    return 0


if __name__ == "__main__":
    sys.exit(main())
