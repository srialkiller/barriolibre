# ENVIRONMENT_BASE_PACK_01

Primer paquete oficial de tiles modulares isométricos para **Carreras de Barrio**.

## Estado de producción

| Métrica | Valor |
|---|---|
| **Pack ID** | `environment_base_pack_01` |
| **Versión** | 1.0.0 |
| **Prompts preparados** | 155 |
| **Tiles generados (manifest)** | **155 / 155 ✅** |
| **Tiles totales en disco** | 187 (incluye variantes extra de packs 3×3) |
| **Style anchor** | `road_straight_h_01` |
| **Fase 2** | **Completada** |
| **Revisión** | Pendiente scoring formal — ver [docs/art/ASSET_REVIEW_GUIDE.md](../../docs/art/ASSET_REVIEW_GUIDE.md) |
| **Herramienta** | `generate2dsprite` (Agent Sprite Forge) |

## Estructura

```
assets/environment/
├── roads/           # Calles, esquinas, cruces, T, variantes
├── sidewalks/       # Veredas
├── curbs/           # Cordones
├── terrain/         # Pasto, tierra, concreto, ripio
├── transitions/     # Transiciones entre materiales
├── markings/        # Detalles de suelo (overlay)
├── _prompts/        # 155 prompts listos para generación
└── _raw/            # PNG crudos pre-chroma-key

data/tilesets/
├── environment_base_pack_01_manifest.json   # Registro completo del pack
└── environment_base_pack_01_generated.json  # Tiles ya producidos

scripts/
├── environment_tile_prompts.py              # Templates de prompt
├── export_environment_prompts.py            # Exporta los 155 prompts
├── process_environment_tile.py            # Chroma-key + resize 256×128
├── batch_process_environment_pack.py        # Lote 1
├── batch_process_environment_pack_02.py     # Lote 2
└── batch_process_environment_pack_03.py     # Lote 3
```

## Especificaciones técnicas

| Propiedad | Valor |
|---|---|
| Proyección | Isométrica 2:1 (dimetric) |
| Tamaño tile | 256 × 128 px |
| Unidad mundo | 1.0 × 0.5 u |
| Pivote | (0.5, 0.5) |
| Fondo generación | `#FF00FF` → alpha en postproceso |
| Outline | Ninguno (terrain tiles) |

## Categorías del pack

### Calles (`roads/`)
- `road_straight_h`, `road_straight_v`
- `road_corner_ne/nw/se/sw`
- `road_tjunction_n/s` (+ e/w pendientes en prompts)
- `road_cross`, `road_deadend`
- `road_narrow`, `road_wide`
- `road_damaged`, `road_patched`

### Veredas (`sidewalks/`)
- `sidewalk_straight`, `sidewalk_corner`, inner/outer corner, crossing, ramp

### Cordones (`curbs/`)
- `curb_straight`, `curb_corner`, `curb_ramp`

### Terreno (`terrain/`)
- `grass_clean`, `grass_dry`, `dirt_compact`, `dirt_soft`
- `concrete_clean`, `concrete_old`, `gravel`

### Marcas (`markings/`) — overlay
- Manhole, storm drain, cracks, repair, road paint

### Transiciones (`transitions/`)
- road↔dirt/grass, sidewalk↔grass, concrete↔grass/dirt, grass↔dirt

## Fase 2 — Completada ✅

Todos los tiles del manifiesto (`environment_base_pack_01_manifest.json`) están producidos:

- ✅ Variantes 02–03 de calles existentes
- ✅ T-junction E/W (variantes 01–03)
- ✅ Veredas: corner, inner/outer corner, crossing, ramp
- ✅ Cordones: corner, ramp (+ variantes straight)
- ✅ Terreno: `dirt_soft`, `concrete_old` (5 variantes c/u)
- ✅ Marcas: storm drain, cracks, repair, stop, crosswalk, arrow (+ variantes)
- ✅ Transiciones restantes (sidewalk↔grass, concrete↔grass/dirt, variantes 02–03)

### Scripts Fase 2

```powershell
python scripts/build_phase2_prompts.py          # 40 prompts de grid
python scripts/batch_process_environment_phase2.py  # postproceso
python scripts/list_missing_tiles.py            # verificar 0 missing
```

## Fase 1 — Tiles producidos

Lote fundacional con conectividad completa básica:

- ✅ Style anchor + calles rectas (9 variantes H)
- ✅ Calle vertical, 4 esquinas, cruce, dead end, T-junction N/S
- ✅ Calle estrecha, ancha, dañada, parcheada
- ✅ Vereda recta (9 variantes)
- ✅ Cordón recto
- ✅ Pasto limpio (9), pasto seco (9), tierra compacta (9)
- ✅ Concreto limpio (9), ripio (9)
- ✅ Transiciones road↔grass, road↔dirt, grass↔dirt
- ✅ Marcas: línea pintada, manhole

## Integración Bevy

Cada tile incluye `<name>.meta.json`:

```json
{
  "id": "road_straight_h_01",
  "pivot": [0.5, 0.5],
  "size_pixels": [256, 128],
  "size_units": [1.0, 0.5],
  "projection": "isometric_2_1",
  "connections": { "east": "road", "west": "road" }
}
```

Conversión grid → mundo (Bevy):

```rust
pub const TILE_W: f32 = 1.0;
pub const TILE_H: f32 = 0.5;

fn tile_to_world(x: i32, y: i32) -> Vec3 {
    Vec3::new(
        (x - y) as f32 * TILE_W * 0.5,
        0.0,
        (x + y) as f32 * TILE_H * 0.5,
    )
}
```

## Reglas cumplidas

- ✅ GAME_ART_BIBLE — invariantes, ECS, no assets aislados
- ✅ ART_STYLE_GUIDE — cámara, luz, paleta, escala ([docs/](../docs/))
- ✅ VISUAL_LANGUAGE — formas simples, sin basura, 70/20/10 en texturas
- ✅ ASSET_PIPELINE — naming, pivotes, carpetas, meta.json
- ✅ `generate2dsprite` — fondo magenta, postproceso chroma-key
- ❌ `generate2dmap` — no utilizado (solo sprites modulares)
- ❌ Casas, árboles, personajes, vehículos — no generados

## QA recomendado

1. Componer grilla 8×8 en escena Bevy con road_cross central
2. Verificar bordes sin huecos entre tiles adyacentes
3. Validar escala contra referencia niño (1.0 u) cuando exista
4. Comparar dirección de sombra SW en todos los tiles
