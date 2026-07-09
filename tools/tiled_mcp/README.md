# tiled_mcp

Servidor MCP (Model Context Protocol) que integra el editor de mapas **Tiled** con BarrioLibre.

Permite a los agentes del Studio OS leer, editar, exportar y validar barrios `.tmx` de forma
**headless** (sin abrir Tiled) y controlar el editor **abierto en vivo** vía file-watcher
bidireccional + Windows UI Automation.

**Status:** ✅ Nivel 1 (headless) + Nivel 2 (puente vivo) implementados y verificados
**Owner:** tools_engineer

## Niveles

| Nivel | Descripción | Requiere Tiled abierto |
|-------|-------------|------------------------|
| **1 — Headless** | Lee/edita `.tmx`/`.tsx` y envuelve los scripts de `tools/tiled_export/` y `tools/map_validator/` | No |
| **2 — Puente vivo** | File-watcher bidireccional + UI Automation: focus_layer, save, sync, detección de cambios | Sí (solo algunas tools) |

> **Nota sobre scripting de Tiled:** Esta instalación de Tiled 1.12.2 no tiene soporte de
> scripting compilado (sin menú "Scripts and Console"). El Nivel 2 usa **UI Automation de
> Windows** + **file-watcher mtime** en lugar de la Scripting API, por lo que no requiere
> extensiones ni scripting habilitado.

## Registro en opencode

`opencode.jsonc` (raíz del repo):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "tiled": {
      "type": "local",
      "command": ["python", "-m", "tiled_mcp"],
      "cwd": "tools/tiled_mcp",
      "enabled": true,
      "timeout": 10000
    }
  }
}
```

## Instalación de dependencias

```powershell
cd tools/tiled_mcp
pip install -e .
```

Requiere Python 3.10+, Pillow, `uiautomation` y `pywin32` (instalados automáticamente).
Tiled debe estar en `C:\Program Files\Tiled\tiled.exe` o apuntado por la variable `TILED_EXE`.

## Variables de entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `TILED_EXE` | (auto-detect en Program Files) | Ruta a `tiled.exe` para `tiled_open_in_editor` |

## Herramientas

### Nivel 1 — Headless (sobre archivos)

**Lectura**

| Tool | Descripción |
|------|-------------|
| `tiled_ping` | Health check: repo root, maps dir, ruta de Tiled |
| `tiled_list_maps` | Lista barrios en `data/maps/` con tamaño, orientación y conteo de capas |
| `tiled_get_map_info` | Info detallada: dims, capas (tile + object), tilesets, conteos de entidades |
| `tiled_get_layer_grid` | Grilla 2D de `tile_id` de una capa tile; gids desconocidos listados |
| `tiled_get_props` | Lista de props (prop_id, col/row, tamaño px) |
| `tiled_get_scene_hooks` | spawn/npcs/pickups |
| `tiled_get_collision` | Celdas bloqueadas (capa `collision` + `collision_zones`) |
| `tiled_list_tilesets` | Tilesets del mapa con firstgid, source, tile_count |
| `tiled_get_tileset_tiles` | Tiles de un `.tsx` con tile_id/prop_id e imagen |

**Escritura** (editan el `.tmx` in place, diffs mínimos por cirugía de texto)

| Tool | Descripción |
|------|-------------|
| `tiled_set_tile` | Setea una celda por `tile_id` (`""` limpia) |
| `tiled_fill_region` | Rellena una región rectangular (rangos inclusivos) |
| `tiled_add_prop` | Agrega un prop por `prop_id` en col/row (devuelve el nuevo object id) |
| `tiled_move_prop` | Mueve un prop por object id |
| `tiled_delete_prop` | Borra un prop por object id |
| `tiled_resize_map` | Redimensiona el mapa y todas sus capas tile |

**Wrappers de scripts existentes**

| Tool | Script subyacente |
|------|--------------------|
| `tiled_export_map` | `export_layout.py` → `layout/props/scene_hooks/collision.json` |
| `tiled_validate_map` | `cargo run -p map_validator` |
| `tiled_regenerate_tileset` | `generate_tileset.py` |
| `tiled_build_reference_map` | `build_barrio_reference.py` (**destructivo**, requiere `confirm=true`) |
| `tiled_render_reference_preview` | `preview_barrio.py` (escena 8x8 hardcoded) → imagen PNG |
| `tiled_render_map_preview` | Render isométrico de un mapa desde `layout.json`+`props.json` → imagen PNG |

### Nivel 2 — Puente vivo (file-watcher + UI Automation)

| Tool | Descripción | Requiere Tiled |
|------|-------------|----------------|
| `tiled_is_editor_open` | ¿Tiled está corriendo? ¿Qué .tmx tiene abierto? | No |
| `tiled_open_in_editor` | Abre el `.tmx` en Tiled (`tiled.exe`) | No |
| `tiled_get_open_map_state` | Mapa abierto + capa activa + todas las capas (via UI Automation) | Sí |
| `tiled_focus_layer` | Setea la capa activa por nombre (UI Automation `Select()`) | Sí |
| `tiled_save_in_editor` | Envía Ctrl+S a Tiled para guardar el mapa actual | Sí |
| `tiled_mark_clean` | Registra el mtime del .tmx como baseline | No |
| `tiled_check_map_changed` | ¿El .tmx cambió en disco? (compara con baseline o `layout.json`) | No |
| `tiled_sync_from_editor` | Save + check + auto-export + auto-validate en un solo paso | Sí (save) |

**Flujo del puente vivo bidireccional:**

```
MCP → Tiled:  tiled_set_tile → edita .tmx en disco → Tiled recarga (file watcher nativo)
Tiled → MCP:  usuario guarda Ctrl+S → tiled_check_map_changed → changed=True → tiled_sync_from_editor(auto_export=True)
```

## Ejecución y tests

```powershell
python -m tiled_mcp                                   # servidor stdio (no imprime salvo MCP)
python tools/tiled_mcp/tests/test_tiled_mcp.py        # 10 tests (lectura + round-trip + file-watcher)
```

El test de mutators trabaja sobre una copia temporal (`barrio_mcp_autotest`) y la limpia al
final; no toca los mapas del commit.

## Estructura

```
tools/tiled_mcp/
├── pyproject.toml
├── README.md
├── tiled_mcp/
│   ├── __init__.py
│   ├── __main__.py        ← entrypoint stdio
│   ├── server.py          ← registro y dispatch de tools
│   ├── tmx_io.py          ← lectura TMX/TSX (Nivel 1 lectura)
│   ├── mutators.py        ← escritura TMX con cirugía de texto (Nivel 1 escritura)
│   ├── runners.py         ← wrappers de scripts + render isométrico
│   ├── ui_bridge.py       ← UI Automation: focus_layer, save, get_state (Nivel 2)
│   └── live_bridge.py     ← file-watcher mtime + sync_from_editor (Nivel 2)
└── tests/
    └── test_tiled_mcp.py
```

## Troubleshooting

| Problema | Causa / Solución |
|----------|------------------|
| `tiled_validate_map` falla con `os error 4551` | Una política de control de aplicaciones de Windows bloquea `target\debug\map_validator.exe`. Allowlist `target/` o ejecutá `cargo build --release` con una excepción de política. |
| `tiled_export_map` "pierde" el `poi_garage` de `scene_hooks.json` | Comportamiento preexistente: `export_layout.py` escribe `poi_hooks: []` siempre. Conservá los POI a mano o extendé `export_scene_hooks`. |
| `tiled_get_open_map_state` → `open: false` | Tiled no está corriendo o no tiene un mapa abierto. Usá `tiled_open_in_editor` primero. |
| `tiled_focus_layer` → `Layer not found` | La capa no existe o no es visible en el panel de capas. Verificá con `tiled_get_map_info` (Nivel 1). |
| `tiled_check_map_changed` → `changed: false` después de editar en Tiled | Asegurate de haber guardado en Tiled (Ctrl+S). El MCP compara el mtime del .tmx con el baseline o `layout.json`. |
| MCP → Tiled: Tiled no recarga el .tmx | Tiled por defecto pregunta al detectar cambios externos. Confirmá el diálogo de recarga, o activa auto-reload en las preferencias de Tiled. |
| `Unknown tile_id` al setear | El `tile_id` no existe en los tilesets del mapa. Listá con `tiled_get_tileset_tiles`. |

## Ver también

- [tiled_export/README.md](../tiled_export/README.md) — flujo de edición de mapas en Tiled
- [map_validator/README.md](../map_validator/README.md) — validación de `layout.json`
