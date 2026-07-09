#!/usr/bin/env python3
"""Generate the semi-transparent red collision marker tile for Tiled."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "assets" / "editor" / "collision_blocked_01.png"
WIDTH, HEIGHT = 256, 128


def diamond_mask(width: int, height: int) -> np.ndarray:
    center_x = (width - 1) / 2.0
    center_y = (height - 1) / 2.0
    half_w = width / 2.0
    half_h = height / 2.0
    ys, xs = np.mgrid[0:height, 0:width]
    manhattan = np.abs(xs - center_x) / half_w + np.abs(ys - center_y) / half_h
    return (manhattan <= 1.0).astype(np.float32)


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    mask = diamond_mask(WIDTH, HEIGHT)
    rgba = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    rgba[..., 0] = 255
    rgba[..., 1] = 40
    rgba[..., 2] = 40
    rgba[..., 3] = (mask * 170).astype(np.uint8)
    Image.fromarray(rgba, mode="RGBA").save(OUT)
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
