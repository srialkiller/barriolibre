#!/usr/bin/env python3
"""Generate a placeholder player sprite atlas + animation JSON for Sprint 02.

Replace with generate2dsprite output when production art is ready.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
OUT_PNG = REPO / "assets" / "player" / "player.png"
OUT_JSON = REPO / "data" / "characters" / "player_animations.json"

CELL = 256
COLS = 4
ROWS = 6
WALK_FRAMES = 4
IDLE_FRAMES = 4

DIRECTIONS = [
    ("north", (90, 150, 220)),
    ("east", (90, 190, 120)),
    ("south", (230, 150, 80)),
    ("west", (170, 120, 210)),
]


def draw_character(
    draw: ImageDraw.ImageDraw,
    origin: tuple[int, int],
    color: tuple[int, int, int],
    frame: int,
    walking: bool,
) -> None:
    x0, y0 = origin
    cx = x0 + CELL // 2
    feet_y = y0 + CELL - 28
    bob = (frame % 2) * 4 if walking else (frame % 4) - 1
    head_r = 34
    body_h = 92
    body_w = 56

    head_cy = feet_y - body_h - head_r + bob
    draw.ellipse(
        (cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r),
        fill=(*color, 255),
        outline=(35, 35, 45, 255),
        width=3,
    )
    draw.rounded_rectangle(
        (
            cx - body_w // 2,
            head_cy + head_r - 10,
            cx + body_w // 2,
            feet_y,
        ),
        radius=16,
        fill=(min(color[0] + 20, 255), min(color[1] + 20, 255), min(color[2] + 20, 255), 255),
        outline=(35, 35, 45, 255),
        width=3,
    )

    stride = 14 if walking else 6
    phase = frame if walking else 0
    left_x = cx - 22 + (stride if phase % 2 == 0 else -stride)
    right_x = cx + 22 + (-stride if phase % 2 == 0 else stride)
    draw.line((left_x, feet_y - 8, left_x, feet_y), fill=(45, 45, 55, 255), width=8)
    draw.line((right_x, feet_y - 8, right_x, feet_y), fill=(45, 45, 55, 255), width=8)


def build_atlas() -> Image.Image:
    sheet = Image.new("RGBA", (CELL * COLS, CELL * ROWS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sheet)

    for row_index, (_name, color) in enumerate(DIRECTIONS):
        for frame in range(WALK_FRAMES):
            draw_character(
                draw,
                (frame * CELL, row_index * CELL),
                color,
                frame,
                walking=True,
            )

    south_color = DIRECTIONS[2][1]
    for frame in range(IDLE_FRAMES):
        col = frame % COLS
        row = 4 + (frame // COLS)
        draw_character(
            draw,
            (col * CELL, row * CELL),
            south_color,
            frame,
            walking=False,
        )

    return sheet


def write_json() -> None:
    payload = {
        "texture": "player/player.png",
        "cell_size": [CELL, CELL],
        "columns": COLS,
        "rows": ROWS,
        "display_height_px": 192,
        "idle": {
            "frame_start": 16,
            "frames": IDLE_FRAMES,
            "fps": 6,
        },
        "walk": {
            "frames_per_direction": WALK_FRAMES,
            "fps": 10,
            "direction_rows": {
                "north": 0,
                "east": 1,
                "south": 2,
                "west": 3,
            },
        },
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")


def main() -> int:
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    atlas = build_atlas()
    atlas.save(OUT_PNG)
    print(f"Wrote {OUT_PNG} ({atlas.size[0]}x{atlas.size[1]})")
    write_json()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
