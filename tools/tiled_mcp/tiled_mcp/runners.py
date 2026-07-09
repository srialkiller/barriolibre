from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

from PIL import Image

from tiled_mcp.server import MAPS_DIR, REPO_ROOT, TILED_EXPORT_DIR
import tiled_mcp.tmx_io as io_mod

if str(TILED_EXPORT_DIR) not in sys.path:
    sys.path.insert(0, str(TILED_EXPORT_DIR))

import generate_tileset as gt


def _run(cmd: list[str], cwd: Path | None = None) -> dict:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    return {
        "command": cmd,
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "ok": proc.returncode == 0,
    }


def run_export_map(
    map_id: str,
    no_props: bool = False,
    no_hooks: bool = False,
    no_collision: bool = False,
    barrio_id: str | None = None,
    display_name: str = "Barrio Tutorial",
    default_tile_id: str = "grass_clean_01",
) -> dict:
    tmx = io_mod._tmx_path(map_id)
    cmd = [
        sys.executable,
        str(TILED_EXPORT_DIR / "export_layout.py"),
        str(tmx),
        "--display-name",
        display_name,
        "--default-tile-id",
        default_tile_id,
    ]
    if barrio_id:
        cmd += ["--barrio-id", barrio_id]
    if no_props:
        cmd.append("--no-props")
    if no_hooks:
        cmd.append("--no-hooks")
    if no_collision:
        cmd.append("--no-collision")
    res = _run(cmd)
    res["map_id"] = map_id
    res["tmx_path"] = str(tmx)
    return res


def run_validate_map(map_id: str) -> dict:
    map_dir = MAPS_DIR / map_id
    if not map_dir.is_dir():
        raise FileNotFoundError(f"Map directory not found: {map_dir}")
    cmd = ["cargo", "run", "-q", "-p", "map_validator", "--", str(map_dir)]
    res = _run(cmd)
    res["map_id"] = map_id
    if not res["ok"] and "4551" in res.stderr:
        res["policy_note"] = (
            "Windows app-control policy blocked map_validator.exe (os error 4551). "
            "Allowlist the target/ directory or run 'cargo build --release' with "
            "an appropriate policy exception."
        )
    return res


def run_regenerate_tileset(
    map_id: str,
    width: int | None = None,
    height: int | None = None,
    from_layout: bool = False,
    ids: list[str] | None = None,
) -> dict:
    cmd = [sys.executable, str(TILED_EXPORT_DIR / "generate_tileset.py"), "--map-id", map_id]
    if width is not None:
        cmd += ["--width", str(width)]
    if height is not None:
        cmd += ["--height", str(height)]
    if from_layout:
        cmd.append("--from-layout")
    if ids:
        cmd += ["--ids", *ids]
    res = _run(cmd)
    res["map_id"] = map_id
    return res


def run_build_reference_map(confirm: bool = False) -> dict:
    if not confirm:
        return {
            "ok": False,
            "error": (
                "build_barrio_reference is DESTRUCTIVE: it regenerates and overwrites "
                "the barrio_tutorial_01 .tmx, layout/props/hooks/collision JSON and "
                "preview PNG from scratch. Re-run with confirm=true to proceed."
            ),
        }
    cmd = [sys.executable, str(TILED_EXPORT_DIR / "build_barrio_reference.py")]
    res = _run(cmd)
    res["destructive"] = True
    res["note"] = "Reference map data was regenerated in place."
    return res


def run_render_reference_preview() -> dict:
    cmd = [sys.executable, str(TILED_EXPORT_DIR / "preview_barrio.py")]
    res = _run(cmd)
    out = MAPS_DIR / "barrio_tutorial_01" / "_preview_barrio.png"
    res["output_path"] = str(out) if out.exists() else None
    res["output_exists"] = out.exists()
    return res


def _tile_png(tile_id: str) -> Path:
    return REPO_ROOT / "assets" / "environment" / gt.category_for_tile_id(tile_id) / f"{tile_id}.png"


def _prop_png(prop_id: str) -> Path:
    return REPO_ROOT / "assets" / "environment" / "props" / f"{prop_id}.png"


def render_map_preview(map_id: str, max_size: int = 1600) -> dict:
    import json

    map_dir = MAPS_DIR / map_id
    layout_path = map_dir / "layout.json"
    props_path = map_dir / "props.json"
    if not layout_path.exists():
        raise FileNotFoundError(
            f"layout.json not found: {layout_path}. Run tiled_export_map first."
        )
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    props_payload = (
        json.loads(props_path.read_text(encoding="utf-8")) if props_path.exists() else {"props": []}
    )

    tw, th = layout["tile_size_pixels"]
    ground = layout["layers"]["ground"]
    rows = len(ground)
    cols = len(ground[0]) if ground else 0

    side_margin = 64
    top_margin = 256
    bottom_margin = 96
    canvas_w = (cols + rows) * (tw // 2) + side_margin * 2
    canvas_h = (cols + rows) * (th // 2) + top_margin + bottom_margin
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (36, 38, 48, 255))

    origin_x = side_margin + rows * (tw // 2) - tw // 2
    origin_y = top_margin

    missing_tiles: list[str] = []
    for gy, row in enumerate(ground):
        for gx, tile_id in enumerate(row):
            if not tile_id:
                continue
            tp = _tile_png(tile_id)
            if not tp.exists():
                missing_tiles.append(tile_id)
                continue
            tile = Image.open(tp).convert("RGBA")
            sx = origin_x + (gx - gy) * (tw // 2)
            sy = origin_y + (gx + gy) * (th // 2)
            canvas.alpha_composite(tile, (sx, sy))

    missing_props: list[str] = []
    props_sorted = sorted(
        props_payload.get("props", []), key=lambda p: (p["row"] + p["col"], p["row"])
    )
    for prop in props_sorted:
        pid = prop["prop_id"]
        pp = _prop_png(pid)
        if not pp.exists():
            missing_props.append(pid)
            continue
        img = Image.open(pp).convert("RGBA")
        cx = origin_x + (prop["col"] - prop["row"]) * (tw / 2) + tw / 2
        cy = origin_y + (prop["col"] + prop["row"]) * (th / 2) + th / 2
        px = round(cx - img.width / 2)
        py = round(cy - img.height)
        canvas.alpha_composite(img, (px, py))

    out = map_dir / "_preview_mcp.png"
    canvas.save(out)

    return {
        "map_id": map_id,
        "output_path": str(out),
        "size": list(canvas.size),
        "ground_cells": cols * rows,
        "props_rendered": len(props_sorted),
        "missing_tiles": missing_tiles,
        "missing_props": missing_props,
        "max_size": max_size,
    }


def png_image_content(path: str, max_size: int = 1600):
    import base64

    import mcp.types as types

    img = Image.open(path).convert("RGBA")
    if max_size and (img.width > max_size or img.height > max_size):
        img.thumbnail((max_size, max_size))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    data = base64.b64encode(buf.getvalue()).decode("ascii")
    return types.ImageContent(type="image", data=data, mimeType="image/png")
