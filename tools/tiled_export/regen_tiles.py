#!/usr/bin/env python3
"""Re-texture isometric ground tiles as proper 3-face iso blocks.

Reference geometry (scrabling-style):
  * top face  — chevron bounded by diagonals (left-mid, bottom) and (right-mid, bottom)
  * left side — bottom-left wedge (solid darker colour)
  * right side — bottom-right wedge (solid darkest colour)

The previous version split at a horizontal line (ny<=0), which is NOT how iso
blocks look — it left a flat band at the sides and the wrong proportions.

Usage:
    python tools/tiled_export/regen_tiles.py --all
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_tileset import CURATED_TUTORIAL_TILES, category_for_tile_id, tile_path  # noqa: E402

GEN_DIR = (
    Path.home() / ".cursor" / "projects" / "c-Users-tecnova-Desktop-barriolibre" / "assets"
)

TW, TH = 256, 128
MARK_LUM = 122

GRASS_VARIANTS = {
    "grass_clean_01": (1.00, (1.00, 1.00, 1.00), (0, 0)),
    "grass_clean_02": (0.96, (0.98, 1.00, 0.96), (90, 40)),
    "grass_clean_03": (1.04, (1.02, 1.00, 0.94), (40, 150)),
    "grass_clean_04": (0.92, (0.96, 1.00, 0.98), (170, 110)),
}

# Solid side-face colours per category (left, right) — no texture bleed.
SIDE = {
    "terrain": (np.array([58, 98, 42], dtype=np.float32), np.array([42, 72, 32], dtype=np.float32)),
    "sidewalks": (np.array([152, 148, 140], dtype=np.float32), np.array([122, 118, 110], dtype=np.float32)),
    "roads": (np.array([52, 54, 60], dtype=np.float32), np.array([36, 38, 42], dtype=np.float32)),
}


def load_texture(name: str) -> np.ndarray:
    path = GEN_DIR / f"gen_tex_{name}.png"
    img = Image.open(path).convert("RGB").resize((256, 256), Image.Resampling.LANCZOS)
    return np.asarray(img, dtype=np.float32)


def window(tex: np.ndarray, roll: tuple[int, int]) -> np.ndarray:
    ox, oy = roll
    rolled = np.roll(np.roll(tex, oy, axis=0), ox, axis=1)
    return rolled[64:192, 0:256, :].copy()


def luminance(rgb: np.ndarray) -> np.ndarray:
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def iso_block_faces(h: int, w: int, mask: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Split diamond into top / left-side / right-side using iso diagonals.

    Diagonals run from left-mid (0, h/2) and right-mid (w, h/2) to bottom (w/2, h).
    """
    cx, cy = w / 2, h / 2
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    # y boundary of top face at each x (V-shaped bottom edge of top face).
    slope = (h - cy) / cx  # 0.5 for 256x128
    boundary = np.where(xx <= cx, cy + slope * xx, cy + slope * (w - xx))

    in_d = mask
    top = in_d & (yy < boundary - 0.5)
    bottom = in_d & ~top
    left = bottom & (xx <= cx)
    right = bottom & (xx > cx)
    return top, left, right


def light_top(base: np.ndarray, top: np.ndarray, xx: np.ndarray, yy: np.ndarray, cx: float, cy: float) -> None:
    """NW highlight on the top face only."""
    nx = (xx - cx) / cx
    ny = (yy - cy) / cy
    light = 0.80 + 0.20 * np.clip((-nx - ny + 1.2) / 2.2, 0.0, 1.0)
    for ch in range(3):
        c = base[..., ch]
        c[top] *= light[top]
        base[..., ch] = c


def paint_solid_sides(
    base: np.ndarray,
    left: np.ndarray,
    right: np.ndarray,
    left_rgb: np.ndarray,
    right_rgb: np.ndarray,
) -> None:
    """Side faces are flat colour — no grass/asphalt texture on the walls."""
    base[left] = left_rgb
    base[right] = right_rgb


def regen(tile_id: str) -> None:
    src = tile_path(tile_id)
    if not src.exists():
        print(f"  ! {tile_id}: not found")
        return

    orig = Image.open(src).convert("RGBA")
    if orig.size != (TW, TH):
        orig = orig.resize((TW, TH), Image.Resampling.LANCZOS)
    orig_rgb = np.asarray(orig.convert("RGB"), dtype=np.float32)
    alpha = np.asarray(orig.getchannel("A"), dtype=np.uint8)
    mask = alpha > 8

    category = category_for_tile_id(tile_id)
    yy, xx = np.mgrid[0:TH, 0:TW].astype(np.float32)
    cx, cy = TW / 2, TH / 2
    top, left, right = iso_block_faces(TH, TW, mask)

    if category == "terrain":
        bright, tint, roll = GRASS_VARIANTS.get(tile_id, (1.0, (1, 1, 1), (0, 0)))
        base = window(GRASS_TEX, roll) * bright * np.array(tint, dtype=np.float32)
        light_top(base, top, xx, yy, cx, cy)
        paint_solid_sides(base, left, right, *SIDE["terrain"])
    elif category == "sidewalks":
        base = window(CONCRETE_TEX, (0, 0))
        light_top(base, top, xx, yy, cx, cy)
        paint_solid_sides(base, left, right, *SIDE["sidewalks"])
        lum = luminance(orig_rgb)
        ref = np.percentile(lum[mask], 88) if mask.any() else 255.0
        seam = np.clip(0.55 + 0.45 * (lum / max(ref, 1.0)), 0.45, 1.05)
        base[top] *= seam[top, None]
    else:
        base = window(ASPHALT_TEX, (0, 0))
        light_top(base, top, xx, yy, cx, cy)
        paint_solid_sides(base, left, right, *SIDE["roads"])
        lum = luminance(orig_rgb)
        mark = mask & (lum >= MARK_LUM)
        base[mark] = orig_rgb[mark]

    out = np.clip(base, 0, 255).astype("uint8")
    Image.fromarray(np.dstack([out, alpha]), mode="RGBA").save(src)
    print(f"  ok {tile_id} [{category}]")


GRASS_TEX: np.ndarray
ASPHALT_TEX: np.ndarray
CONCRETE_TEX: np.ndarray


def main() -> int:
    global GRASS_TEX, ASPHALT_TEX, CONCRETE_TEX
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tile_ids", nargs="*")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    ids = CURATED_TUTORIAL_TILES if args.all else args.tile_ids
    if not ids:
        parser.error("pass tile ids or --all")

    GRASS_TEX = load_texture("grass")
    ASPHALT_TEX = load_texture("asphalt")
    CONCRETE_TEX = load_texture("concrete")

    for tile_id in ids:
        regen(tile_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
