#!/usr/bin/env python3
"""Turn a magenta-background prop render into a trimmed transparent PNG.

Deterministic postprocessor (NOT an art generator): it takes a raw upright
prop rendered on solid magenta (#FF00FF), soft-keys the magenta to alpha with
edge despill, crops to the visible bounding box, and scales it down so the
longest side fits a sane budget. Props keep their native aspect ratio and are
placed in Tiled as tile-objects anchored at the bottom-center pivot.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
# Magenta-ness is measured by hue, not distance to pure magenta, so that a
# darkened magenta shadow (e.g. #7A0A7A) is still recognised as background.
# metric = min(R, B) - G : high for any magenta shade, negative for reds/greens.
KEY_LOW = 25.0
KEY_HIGH = 70.0
MAX_LONG_SIDE = 640


def key_magenta(rgba: np.ndarray) -> np.ndarray:
    rgb = rgba[:, :, :3].astype(np.float32)
    orig_alpha = rgba[:, :, 3].astype(np.float32) / 255.0

    red = rgb[:, :, 0]
    green = rgb[:, :, 1]
    blue = rgb[:, :, 2]

    magentaness = np.minimum(red, blue) - green
    alpha_scale = np.clip(
        (KEY_HIGH - magentaness) / (KEY_HIGH - KEY_LOW), 0.0, 1.0
    )

    # Despill only on partially keyed edge pixels so interior reds survive.
    despill_weight = 1.0 - alpha_scale
    spill = np.clip((red + blue) / 2.0 - green, 0.0, 255.0) * despill_weight
    rgb[:, :, 0] = np.clip(red - spill, 0.0, 255.0)
    rgb[:, :, 2] = np.clip(blue - spill, 0.0, 255.0)

    rgba[:, :, :3] = rgb.astype(np.uint8)
    rgba[:, :, 3] = np.clip(orig_alpha * alpha_scale * 255.0, 0.0, 255.0).astype(
        np.uint8
    )
    return rgba


def trim_to_content(data: np.ndarray) -> np.ndarray:
    mask = data[:, :, 3] > 12
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any() or not cols.any():
        return data
    top, bottom = np.where(rows)[0][[0, -1]]
    left, right = np.where(cols)[0][[0, -1]]
    return data[int(top) : int(bottom) + 1, int(left) : int(right) + 1]


def build_prop(input_path: Path) -> Image.Image:
    source = Image.open(input_path).convert("RGBA")
    data = key_magenta(np.array(source))
    data = trim_to_content(data)
    prop = Image.fromarray(data, "RGBA")

    long_side = max(prop.width, prop.height)
    if long_side > MAX_LONG_SIDE:
        scale = MAX_LONG_SIDE / long_side
        new_size = (max(1, round(prop.width * scale)), max(1, round(prop.height * scale)))
        prop = prop.resize(new_size, Image.Resampling.LANCZOS)
    return prop


def write_meta(output_path: Path, prop_id: str, width: int, height: int) -> None:
    meta = {
        "id": prop_id,
        "category": "props",
        "pack": "environment_base_pack_01",
        "pivot": [0.5, 1.0],
        "size_pixels": [width, height],
        "projection": "isometric_2_1",
        "kind": "object",
        "status": "qc_pass",
    }
    output_path.with_suffix(".meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a transparent prop PNG")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--prop-id", required=True)
    parser.add_argument("--output", type=Path, help="Override output PNG path.")
    args = parser.parse_args()

    input_path = args.input if args.input.is_absolute() else REPO_ROOT / args.input
    prop = build_prop(input_path)

    output_path = (
        args.output
        or REPO_ROOT / "assets" / "environment" / "props" / f"{args.prop_id}.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prop.save(output_path)
    write_meta(output_path, args.prop_id, prop.width, prop.height)

    print(f"Wrote {output_path} ({prop.width}x{prop.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
