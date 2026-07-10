#!/usr/bin/env python3
"""Generate a Tiled image-collection tileset (.tsx) from tile IDs."""

from __future__ import annotations

import argparse
import base64
import json
import os
import struct
import sys
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]


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


def tile_path(tile_id: str) -> Path:
    category = category_for_tile_id(tile_id)
    return REPO_ROOT / "assets" / "environment" / category / f"{tile_id}.png"


def relative_source(from_dir: Path, tile_id: str) -> str:
    absolute = tile_path(tile_id).resolve()
    return Path(os.path.relpath(absolute, from_dir.resolve())).as_posix()


def read_tile_ids_from_layout(map_id: str) -> list[str]:
    layout_path = REPO_ROOT / "data" / "maps" / map_id / "layout.json"
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    unique_ids = {
        tile_id
        for row in layout["layers"]["ground"]
        for tile_id in row
    }
    return sorted(unique_ids)


def write_tileset(output_path: Path, tile_ids: list[str]) -> None:
    from_dir = output_path.parent
    missing = [tile_id for tile_id in tile_ids if not tile_path(tile_id).exists()]
    if missing:
        raise FileNotFoundError(f"Missing PNGs: {', '.join(missing)}")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<tileset version="1.10" tiledversion="1.10.2" '
            f'name="{output_path.stem}" tilecount="{len(tile_ids)}" columns="0">'
        ),
    ]

    for index, tile_id in enumerate(tile_ids):
        source = relative_source(from_dir, tile_id)
        lines.extend(
            [
                f' <tile id="{index}">',
                f'  <image source="{source}" width="256" height="128"/>',
                f'  <properties>',
                f'   <property name="tile_id" type="string" value="{tile_id}"/>',
                f'  </properties>',
                f' </tile>',
            ]
        )

    lines.append("</tileset>")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def prop_path(prop_id: str) -> Path:
    return REPO_ROOT / "assets" / "environment" / "props" / f"{prop_id}.png"


def write_props_tileset(output_path: Path, prop_ids: list[str]) -> None:
    """Image-collection tileset for upright props (variable size each).

    Objects are anchored at bottom-center so they sit on the cell they overlap,
    which is what an isometric map expects for buildings, trees and street furniture.
    """
    from_dir = output_path.parent
    missing = [pid for pid in prop_ids if not prop_path(pid).exists()]
    if missing:
        raise FileNotFoundError(f"Missing prop PNGs: {', '.join(missing)}")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<tileset version="1.10" tiledversion="1.10.2" '
            f'name="{output_path.stem}" tilecount="{len(prop_ids)}" columns="0" '
            'objectalignment="bottom">'
        ),
    ]

    for index, prop_id in enumerate(prop_ids):
        absolute = prop_path(prop_id).resolve()
        source = Path(os.path.relpath(absolute, from_dir.resolve())).as_posix()
        with Image.open(absolute) as image:
            width, height = image.size
        lines.extend(
            [
                f' <tile id="{index}">',
                f'  <image source="{source}" width="{width}" height="{height}"/>',
                f'  <properties>',
                f'   <property name="prop_id" type="string" value="{prop_id}"/>',
                f'  </properties>',
                f' </tile>',
            ]
        )

    lines.append("</tileset>")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def encode_layer_data(gids: list[int]) -> str:
    raw = b"".join(struct.pack("<I", gid) for gid in gids)
    return base64.b64encode(raw).decode("ascii")


def write_map_template(
    output_path: Path,
    tileset_name: str,
    width: int,
    height: int,
    fill_gid: int = 1,
    props_tileset_name: str | None = None,
    props_firstgid: int = 0,
) -> None:
    def layer_block(layer_id: int, layer_name: str, gid: int) -> list[str]:
        gids = [gid] * (width * height)
        encoded = encode_layer_data(gids)
        return [
            f' <layer id="{layer_id}" name="{layer_name}" width="{width}" height="{height}" x="0" y="0">',
            f'  <data encoding="base64">{encoded}</data>',
            " </layer>",
        ]

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<map version="1.10" tiledversion="1.10.2" '
            'orientation="isometric" renderorder="right-down" '
            f'width="{width}" height="{height}" '
            'tilewidth="256" tileheight="128" infinite="0" '
            'nextlayerid="5" nextobjectid="1">'
        ),
        f' <tileset firstgid="1" source="{tileset_name}"/>',
    ]
    if props_tileset_name:
        lines.append(
            f' <tileset firstgid="{props_firstgid}" source="{props_tileset_name}"/>'
        )
    lines.extend(layer_block(1, "ground", fill_gid))
    lines.extend(layer_block(2, "markings", 0))
    lines.extend(layer_block(3, "overlay", 0))
    lines.append(' <objectgroup id="4" name="props"/>')
    lines.append("</map>")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


CURATED_TUTORIAL_TILES = [
    "grass_clean_01",
    "grass_clean_02",
    "grass_clean_03",
    "grass_clean_04",
    "sidewalk_straight_01",
    "road_straight_h_01",
    "road_straight_v_01",
    "road_corner_ne_01",
    "road_corner_nw_01",
    "road_corner_se_01",
    "road_corner_sw_01",
    "road_cross_01",
    "road_plain_01",
    "road_tee_n_01",
    "road_tee_s_01",
    "road_tee_e_01",
    "road_tee_w_01",
    "road_crosswalk_h_01",
    "road_crosswalk_v_01",
]

PROP_TILES = [
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Tiled tileset and map template")
    parser.add_argument("--map-id", default="barrio_tutorial_01")
    parser.add_argument("--width", type=int, default=16)
    parser.add_argument("--height", type=int, default=16)
    parser.add_argument(
        "--ids",
        nargs="+",
        help="Explicit tile IDs for the tileset (default: curated tutorial set).",
    )
    parser.add_argument(
        "--from-layout",
        action="store_true",
        help="Read tile IDs from the map's layout.json instead of the curated set.",
    )
    args = parser.parse_args()

    map_dir = REPO_ROOT / "data" / "maps" / args.map_id
    if args.ids:
        tile_ids = args.ids
    elif args.from_layout:
        tile_ids = read_tile_ids_from_layout(args.map_id)
    else:
        tile_ids = CURATED_TUTORIAL_TILES
    tileset_path = map_dir / "environment_tutorial.tsx"
    props_tileset_path = map_dir / "props_tutorial.tsx"
    map_path = map_dir / f"{args.map_id}.tmx"

    write_tileset(tileset_path, tile_ids)
    write_props_tileset(props_tileset_path, PROP_TILES)
    write_map_template(
        map_path,
        tileset_path.name,
        args.width,
        args.height,
        props_tileset_name=props_tileset_path.name,
        props_firstgid=len(tile_ids) + 1,
    )

    print(f"Tileset: {tileset_path} ({len(tile_ids)} tiles)")
    print(f"Props:   {props_tileset_path} ({len(PROP_TILES)} props)")
    print(f"Map:     {map_path} ({args.width}x{args.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
