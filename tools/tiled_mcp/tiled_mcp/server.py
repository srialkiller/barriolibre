from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

SERVER_NAME = "tiled-mcp"


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "Cargo.toml").exists() and (parent / "tools").is_dir() and (parent / "data").is_dir():
            return parent
    return here.parents[3]


REPO_ROOT = find_repo_root()
MAPS_DIR = REPO_ROOT / "data" / "maps"
TILED_EXPORT_DIR = REPO_ROOT / "tools" / "tiled_export"
TILESETS_DIR = REPO_ROOT / "data" / "tilesets"


def find_tiled_exe() -> str | None:
    env = os.environ.get("TILED_EXE")
    if env and Path(env).exists():
        return env
    candidates = [
        r"C:\Program Files\Tiled\tiled.exe",
        r"C:\Program Files (x86)\Tiled\tiled.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return None


server = Server(SERVER_NAME)


def _ok(payload: object) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps(payload, indent=2, ensure_ascii=False))]


def _err(message: str, **extra: object) -> list[types.TextContent]:
    payload = {"error": message, **extra}
    return [types.TextContent(type="text", text=json.dumps(payload, indent=2, ensure_ascii=False))]


def _tool(
    name: str,
    description: str,
    properties: dict,
    required: list[str],
) -> types.Tool:
    return types.Tool(
        name=name,
        description=description,
        inputSchema={
            "type": "object",
            "properties": properties,
            "required": required,
        },
    )


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        _tool(
            "tiled_ping",
            "Health check. Returns server identity, repo root, maps directory, "
            "and whether the Tiled executable was found.",
            {},
            [],
        ),
        _tool(
            "tiled_list_maps",
            "List all barrios under data/maps/ with their .tmx path, size, "
            "orientation and layer counts.",
            {},
            [],
        ),
        _tool(
            "tiled_get_map_info",
            "Get detailed info about a Tiled map: dimensions, orientation, "
            "tile size, all layers (tile + object), tilesets, and entity counts "
            "(props, spawn, npcs, pickups, collision cells).",
            {"map_id": {"type": "string", "description": "Barrio id, e.g. 'barrio_tutorial_01' (folder name under data/maps/)"}},
            ["map_id"],
        ),
        _tool(
            "tiled_get_layer_grid",
            "Get a 2D grid of tile_id strings for a tile layer (e.g. 'ground', "
            "'markings', 'overlay', 'collision'). Empty cells are ''. Unknown "
            "gids are reported as 'gid:<n>' and listed in 'unknown_gids'.",
            {
                "map_id": {"type": "string"},
                "layer": {"type": "string", "description": "Tile layer name, e.g. 'ground'"},
            },
            ["map_id", "layer"],
        ),
        _tool(
            "tiled_get_props",
            "Get the list of props from the 'props' object layer, resolved to "
            "prop_id, grid col/row and pixel size (matches props.json export).",
            {"map_id": {"type": "string"}},
            ["map_id"],
        ),
        _tool(
            "tiled_get_scene_hooks",
            "Get spawn points, npcs and pickups from the spawn/npcs/pickups "
            "object layers (matches scene_hooks.json export).",
            {"map_id": {"type": "string"}},
            ["map_id"],
        ),
        _tool(
            "tiled_get_collision",
            "Get blocked cells from the 'collision' tile layer and/or "
            "'collision_zones' object layer (matches collision.json export).",
            {"map_id": {"type": "string"}},
            ["map_id"],
        ),
        _tool(
            "tiled_list_tilesets",
            "List tilesets referenced by a map with their firstgid, source "
            "path, name and tile count.",
            {"map_id": {"type": "string"}},
            ["map_id"],
        ),
        _tool(
            "tiled_get_tileset_tiles",
            "Get all tiles in a .tsx tileset with their tile_id/prop_id "
            "properties and image source. Accepts an absolute path or a path "
            "relative to data/maps/.",
            {"tileset_path": {"type": "string", "description": "Absolute path or path relative to data/maps/"}},
            ["tileset_path"],
        ),
        _tool(
            "tiled_export_map",
            "Run export_layout.py on a .tmx to regenerate layout.json, "
            "props.json, scene_hooks.json and collision.json (the Bevy runtime "
            "inputs). Returns stdout/stderr/exit_code.",
            {
                "map_id": {"type": "string"},
                "no_props": {"type": "boolean", "default": False},
                "no_hooks": {"type": "boolean", "default": False},
                "no_collision": {"type": "boolean", "default": False},
                "barrio_id": {"type": "string"},
                "display_name": {"type": "string", "default": "Barrio Tutorial"},
                "default_tile_id": {"type": "string", "default": "grass_clean_01"},
            },
            ["map_id"],
        ),
        _tool(
            "tiled_validate_map",
            "Run the map_validator crate (cargo run -p map_validator) against "
            "data/maps/<map_id>/ and return stdout/stderr/exit_code.",
            {"map_id": {"type": "string"}},
            ["map_id"],
        ),
        _tool(
            "tiled_regenerate_tileset",
            "Regenerate the .tsx tileset and .tmx template for a map via "
            "generate_tileset.py. Use after adding new tiles to the repo.",
            {
                "map_id": {"type": "string"},
                "width": {"type": "integer"},
                "height": {"type": "integer"},
                "from_layout": {"type": "boolean", "default": False, "description": "Read tile IDs from the map's layout.json"},
                "ids": {"type": "array", "items": {"type": "string"}, "description": "Explicit tile IDs"},
            },
            ["map_id"],
        ),
        _tool(
            "tiled_build_reference_map",
            "DESTRUCTIVE: regenerate the barrio_tutorial_01 reference map from "
            "scratch via build_barrio_reference.py, overwriting its .tmx, "
            "layout/props/hooks/collision JSON and preview PNG. Requires "
            "confirm=true.",
            {"confirm": {"type": "boolean", "description": "Must be true to proceed (destructive overwrite)."}},
            ["confirm"],
        ),
        _tool(
            "tiled_render_reference_preview",
            "Render the hardcoded 8x8 reference scene via preview_barrio.py and "
            "return it as a PNG image. QC helper for the tutorial tile pack.",
            {},
            [],
        ),
        _tool(
            "tiled_render_map_preview",
            "Render an isometric PNG preview of a map from its layout.json + "
            "props.json (composites ground diamonds + upright props with depth "
            "sort) and return it as an image. Run tiled_export_map first if "
            "layout.json is missing.",
            {
                "map_id": {"type": "string"},
                "max_size": {"type": "integer", "default": 1600, "description": "Max dimension in px for the returned image."},
            },
            ["map_id"],
        ),
        _tool(
            "tiled_set_tile",
            "Set a single tile in a tile layer of a .tmx by tile_id. Use "
            "tile_id='' (empty) to clear the cell. Edits the .tmx in place.",
            {
                "map_id": {"type": "string"},
                "layer": {"type": "string", "description": "Tile layer name, e.g. 'ground'"},
                "col": {"type": "integer"},
                "row": {"type": "integer"},
                "tile_id": {"type": "string", "description": "Tile id from the tileset, or '' to clear"},
            },
            ["map_id", "layer", "col", "row", "tile_id"],
        ),
        _tool(
            "tiled_fill_region",
            "Fill a rectangular region of a tile layer with one tile_id. "
            "Ranges are inclusive. Edits the .tmx in place.",
            {
                "map_id": {"type": "string"},
                "layer": {"type": "string"},
                "col_start": {"type": "integer"},
                "col_end": {"type": "integer"},
                "row_start": {"type": "integer"},
                "row_end": {"type": "integer"},
                "tile_id": {"type": "string"},
            },
            ["map_id", "layer", "col_start", "col_end", "row_start", "row_end", "tile_id"],
        ),
        _tool(
            "tiled_add_prop",
            "Add a prop object to the 'props' object layer of a .tmx by "
            "prop_id at grid col/row. Width/height default to the prop's "
            "tileset image size. Edits the .tmx in place and returns the new "
            "object id.",
            {
                "map_id": {"type": "string"},
                "prop_id": {"type": "string", "description": "Prop id from the props tileset"},
                "col": {"type": "number"},
                "row": {"type": "number"},
                "width_px": {"type": "number", "description": "Override prop width (defaults to tileset image width)"},
                "height_px": {"type": "number", "description": "Override prop height (defaults to tileset image height)"},
            },
            ["map_id", "prop_id", "col", "row"],
        ),
        _tool(
            "tiled_move_prop",
            "Move an existing prop object to a new grid col/row by object id. "
            "Edits the .tmx in place.",
            {
                "map_id": {"type": "string"},
                "object_id": {"type": "integer"},
                "col": {"type": "number"},
                "row": {"type": "number"},
            },
            ["map_id", "object_id", "col", "row"],
        ),
        _tool(
            "tiled_delete_prop",
            "Delete a prop object from the 'props' object layer by object id. "
            "Edits the .tmx in place.",
            {
                "map_id": {"type": "string"},
                "object_id": {"type": "integer"},
            },
            ["map_id", "object_id"],
        ),
        _tool(
            "tiled_resize_map",
            "Resize a .tmx and all its tile layers to a new width/height. "
            "Existing tile data is kept (top-left aligned); new cells are "
            "filled with 0 (empty). Object layers are untouched. Edits the "
            ".tmx in place.",
            {
                "map_id": {"type": "string"},
                "width": {"type": "integer"},
                "height": {"type": "integer"},
            },
            ["map_id", "width", "height"],
        ),
        _tool(
            "tiled_is_editor_open",
            "Check if Tiled is running and which .tmx file is currently open. "
            "Uses Windows UI Automation (no Tiled scripting required).",
            {},
            [],
        ),
        _tool(
            "tiled_open_in_editor",
            "Launch Tiled (tiled.exe) to open a map's .tmx. Returns the pid "
            "and tmx path.",
            {"map_id": {"type": "string"}},
            ["map_id"],
        ),
        _tool(
            "tiled_get_open_map_state",
            "Query the currently open map in the running Tiled instance via "
            "UI Automation: file name, all layer names and which layer is "
            "currently selected/active. Requires Tiled running.",
            {},
            [],
        ),
        _tool(
            "tiled_focus_layer",
            "Set the active/current layer in the running Tiled instance by "
            "name (uses UI Automation SelectionItemPattern.Select). Requires "
            "Tiled running.",
            {"layer_name": {"type": "string", "description": "Layer name to activate, e.g. 'ground'"}},
            ["layer_name"],
        ),
        _tool(
            "tiled_save_in_editor",
            "Send Ctrl+S to the running Tiled instance to save the current "
            "map. Use before sync_from_editor to ensure Tiled has written "
            "changes to disk.",
            {},
            [],
        ),
        _tool(
            "tiled_mark_clean",
            "Record the current .tmx modification time for a map so that "
            "check_changed can detect future saves from Tiled. Call this "
            "after the MCP edits the .tmx (so the MCP's own writes don't "
            "register as 'changed').",
            {"map_id": {"type": "string"}},
            ["map_id"],
        ),
        _tool(
            "tiled_check_map_changed",
            "Check if a map's .tmx has changed on disk since the last "
            "mark_clean or check (detects when the user saved in Tiled).",
            {"map_id": {"type": "string"}},
            ["map_id"],
        ),
        _tool(
            "tiled_sync_from_editor",
            "Full sync cycle: send Ctrl+S to Tiled, check if the .tmx "
            "changed on disk, and optionally auto-export + auto-validate. "
            "This is the main 'Tiled → MCP' bridge tool.",
            {
                "map_id": {"type": "string"},
                "save": {"type": "boolean", "default": True, "description": "Send Ctrl+S before checking."},
                "auto_export": {"type": "boolean", "default": False, "description": "Run tiled_export_map if changed."},
                "auto_validate": {"type": "boolean", "default": False, "description": "Run tiled_validate_map if changed."},
            },
            ["map_id"],
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    arguments = arguments or {}

    if name == "tiled_ping":
        return _ok(
            {
                "server": SERVER_NAME,
                "status": "ok",
                "repo_root": str(REPO_ROOT),
                "maps_dir": str(MAPS_DIR),
                "maps_dir_exists": MAPS_DIR.exists(),
                "tiled_export_dir": str(TILED_EXPORT_DIR),
                "tiled_exe": find_tiled_exe(),
            }
        )

    try:
        import tiled_mcp.tmx_io as io

        if name == "tiled_list_maps":
            return _ok(io.list_maps())
        if name == "tiled_get_map_info":
            return _ok(io.get_map_info(arguments["map_id"]))
        if name == "tiled_get_layer_grid":
            return _ok(io.get_layer_grid(arguments["map_id"], arguments["layer"]))
        if name == "tiled_get_props":
            return _ok(io.get_props(arguments["map_id"]))
        if name == "tiled_get_scene_hooks":
            return _ok(io.get_scene_hooks(arguments["map_id"]))
        if name == "tiled_get_collision":
            return _ok(io.get_collision(arguments["map_id"]))
        if name == "tiled_list_tilesets":
            return _ok(io.list_tilesets(arguments["map_id"]))
        if name == "tiled_get_tileset_tiles":
            return _ok(io.get_tileset_tiles(arguments["tileset_path"]))
    except FileNotFoundError as e:
        return _err(str(e), tool=name)
    except (KeyError, ValueError) as e:
        return _err(str(e), tool=name)
    except Exception as e:
        return _err(f"{type(e).__name__}: {e}", tool=name)

    try:
        import tiled_mcp.runners as rn

        if name == "tiled_export_map":
            return _ok(
                rn.run_export_map(
                    arguments["map_id"],
                    no_props=arguments.get("no_props", False),
                    no_hooks=arguments.get("no_hooks", False),
                    no_collision=arguments.get("no_collision", False),
                    barrio_id=arguments.get("barrio_id"),
                    display_name=arguments.get("display_name", "Barrio Tutorial"),
                    default_tile_id=arguments.get("default_tile_id", "grass_clean_01"),
                )
            )
        if name == "tiled_validate_map":
            return _ok(rn.run_validate_map(arguments["map_id"]))
        if name == "tiled_regenerate_tileset":
            return _ok(
                rn.run_regenerate_tileset(
                    arguments["map_id"],
                    width=arguments.get("width"),
                    height=arguments.get("height"),
                    from_layout=arguments.get("from_layout", False),
                    ids=arguments.get("ids"),
                )
            )
        if name == "tiled_build_reference_map":
            return _ok(rn.run_build_reference_map(confirm=arguments.get("confirm", False)))
        if name == "tiled_render_reference_preview":
            res = rn.run_render_reference_preview()
            if not res.get("output_path"):
                return _err("preview_barrio.py produced no output PNG", details=res)
            img = rn.png_image_content(res["output_path"], max_size=1600)
            return [types.TextContent(type="text", text=json.dumps(res, indent=2)), img]
        if name == "tiled_render_map_preview":
            res = rn.render_map_preview(arguments["map_id"], max_size=arguments.get("max_size", 1600))
            img = rn.png_image_content(res["output_path"], max_size=res.get("max_size", 1600))
            return [types.TextContent(type="text", text=json.dumps(res, indent=2)), img]
    except FileNotFoundError as e:
        return _err(str(e), tool=name)
    except (KeyError, ValueError) as e:
        return _err(str(e), tool=name)
    except Exception as e:
        return _err(f"{type(e).__name__}: {e}", tool=name)

    try:
        import tiled_mcp.mutators as mu

        if name == "tiled_set_tile":
            return _ok(
                mu.set_tile(
                    arguments["map_id"],
                    arguments["layer"],
                    arguments["col"],
                    arguments["row"],
                    arguments["tile_id"],
                )
            )
        if name == "tiled_fill_region":
            return _ok(
                mu.fill_region(
                    arguments["map_id"],
                    arguments["layer"],
                    arguments["col_start"],
                    arguments["col_end"],
                    arguments["row_start"],
                    arguments["row_end"],
                    arguments["tile_id"],
                )
            )
        if name == "tiled_add_prop":
            return _ok(
                mu.add_prop(
                    arguments["map_id"],
                    arguments["prop_id"],
                    arguments["col"],
                    arguments["row"],
                    width_px=arguments.get("width_px"),
                    height_px=arguments.get("height_px"),
                )
            )
        if name == "tiled_move_prop":
            return _ok(mu.move_prop(arguments["map_id"], arguments["object_id"], arguments["col"], arguments["row"]))
        if name == "tiled_delete_prop":
            return _ok(mu.delete_prop(arguments["map_id"], arguments["object_id"]))
        if name == "tiled_resize_map":
            return _ok(mu.resize_map(arguments["map_id"], arguments["width"], arguments["height"]))
    except FileNotFoundError as e:
        return _err(str(e), tool=name)
    except (KeyError, ValueError) as e:
        return _err(str(e), tool=name)
    except Exception as e:
        return _err(f"{type(e).__name__}: {e}", tool=name)

    try:
        import tiled_mcp.ui_bridge as ui
        import tiled_mcp.live_bridge as fw

        if name == "tiled_is_editor_open":
            return _ok({
                "running": ui.is_tiled_running(),
                "fileName": ui.get_open_map_filename(),
            })

        if name == "tiled_open_in_editor":
            exe = find_tiled_exe()
            if not exe:
                return _err(
                    "Tiled executable not found. Set TILED_EXE or install Tiled "
                    "in the default Program Files location.",
                    tool=name,
                )
            tmx = io._tmx_path(arguments["map_id"])
            return _ok(ui.open_in_editor(str(tmx), exe))

        if name == "tiled_get_open_map_state":
            return _ok(ui.get_open_map_state())

        if name == "tiled_focus_layer":
            return _ok(ui.focus_layer(arguments["layer_name"]))

        if name == "tiled_save_in_editor":
            return _ok(ui.save_in_editor())

        if name == "tiled_mark_clean":
            return _ok(fw.get_watcher().mark_clean(arguments["map_id"]))

        if name == "tiled_check_map_changed":
            return _ok(fw.get_watcher().check_changed(arguments["map_id"]))

        if name == "tiled_sync_from_editor":
            return _ok(
                fw.get_watcher().sync_from_editor(
                    arguments["map_id"],
                    save=arguments.get("save", True),
                    auto_export=arguments.get("auto_export", False),
                    auto_validate=arguments.get("auto_validate", False),
                )
            )
    except FileNotFoundError as e:
        return _err(str(e), tool=name)
    except Exception as e:
        return _err(f"{type(e).__name__}: {e}", tool=name)

    return _err(f"Unknown tool: {name}")


async def main() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())
