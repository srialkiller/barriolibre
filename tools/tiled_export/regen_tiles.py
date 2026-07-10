#!/usr/bin/env python3
"""Re-texture the isometric ground tiles with richer surfaces and subtle volume.

Each tile stays a 256x128 diamond and keeps its ORIGINAL geometry:
- the diamond alpha (anti-aliased edges) is preserved, so tiles still line up;
- road markings (bright pixels) and sidewalk seams (dark pixels) are re-imprinted
  from the original, so the street network reads exactly the same;
- only the base surface is swapped for a detailed painterly texture, plus a soft
  edge bevel (ambient-occlusion groove) that gives each tile a raised-slab feel.

Textures come from GenerateImage output (gen_tex_grass/asphalt/concrete.png) in
the Cursor project assets folder. IDs/paths are unchanged, so the runtime picks
up the new art with no code changes.

Usage:
    python tools/tiled_export/regen_tiles.py --all
    python tools/tiled_export/regen_tiles.py grass_clean_02 road_cross_01
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_tileset import CURATED_TUTORIAL_TILES, category_for_tile_id, tile_path  # noqa: E402

GEN_DIR = (
    Path.home() / ".cursor" / "projects" / "c-Users-tecnova-Desktop-barriolibre" / "assets"
)

TW, TH = 256, 128
BEVEL_PX = 6          # width of the dark edge groove
BEVEL_FACTOR = 0.78   # how much to darken that groove
MARK_LUM = 122        # >= this luminance in a road tile == painted marking

# per-grass-variant (brightness, (r,g,b) tint, roll offset) for natural variety
GRASS_VARIANTS = {
    "grass_clean_01": (1.00, (1.00, 1.00, 1.00), (0, 0)),
    "grass_clean_02": (0.94, (0.98, 1.00, 0.95), (90, 40)),
    "grass_clean_03": (1.06, (1.02, 1.00, 0.93), (40, 150)),
    "grass_clean_04": (0.90, (0.95, 1.00, 0.98), (170, 110)),
}


def load_texture(name: str) -> np.ndarray:
    path = GEN_DIR / f"gen_tex_{name}.png"
    img = Image.open(path).convert("RGB").resize((256, 256), Image.Resampling.LANCZOS)
    return np.asarray(img, dtype=np.float32)


def window(tex: np.ndarray, roll: tuple[int, int]) -> np.ndarray:
    """256x256 texture -> a 128x256 window, wrapped by the given roll offset."""
    ox, oy = roll
    rolled = np.roll(np.roll(tex, oy, axis=0), ox, axis=1)
    return rolled[64:192, 0:256, :].copy()


def luminance(rgb: np.ndarray) -> np.ndarray:
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def edge_ring(mask: np.ndarray, px: int) -> np.ndarray:
    m = Image.fromarray((mask * 255).astype("uint8"))
    eroded = np.asarray(m.filter(ImageFilter.MinFilter(px * 2 + 1))) > 128
    return mask & (~eroded)


def apply_bevel(base: np.ndarray, mask: np.ndarray) -> None:
    ring = edge_ring(mask, BEVEL_PX)
    base[ring] *= BEVEL_FACTOR


def regen(tile_id: str) -> None:
    src = tile_path(tile_id)
    if not src.exists():
        print(f"  ! {tile_id}: not found at {src}")
        return
    orig = Image.open(src).convert("RGBA")
    if orig.size != (TW, TH):
        orig = orig.resize((TW, TH), Image.Resampling.LANCZOS)
    orig_rgb = np.asarray(orig.convert("RGB"), dtype=np.float32)
    alpha = np.asarray(orig.getchannel("A"), dtype=np.uint8)
    mask = alpha > 8

    category = category_for_tile_id(tile_id)

    if category == "terrain":
        bright, tint, roll = GRASS_VARIANTS.get(tile_id, (1.0, (1, 1, 1), (0, 0)))
        base = window(GRASS_TEX, roll)
        base *= bright
        base *= np.array(tint, dtype=np.float32)
        apply_bevel(base, mask)
    elif category == "sidewalks":
        base = window(CONCRETE_TEX, (0, 0))
        apply_bevel(base, mask)
        # re-imprint slab seams: darken base by the original's relative luminance
        lum = luminance(orig_rgb)
        ref = np.percentile(lum[mask], 88) if mask.any() else 255.0
        factor = np.clip(0.55 + 0.45 * (lum / max(ref, 1.0)), 0.45, 1.05)
        base *= factor[..., None]
    else:  # roads / markings / everything asphalt-based
        base = window(ASPHALT_TEX, (0, 0))
        apply_bevel(base, mask)
        lum = luminance(orig_rgb)
        mark = mask & (lum >= MARK_LUM)
        base[mark] = orig_rgb[mark]

    base = np.clip(base, 0, 255).astype("uint8")
    out = np.dstack([base, alpha])
    Image.fromarray(out, mode="RGBA").save(src)
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
