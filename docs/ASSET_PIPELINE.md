# ASSET_PIPELINE.md
## Carreras de Barrio — Pipeline de Assets y Convenciones Técnicas

**Proyecto:** Carreras de Barrio  
**Ubicación:** `docs/ASSET_PIPELINE.md`  
**Motor:** Rust + Bevy Engine  
**Herramientas:** Agent Sprite Forge (`generate2dsprite`, `generate2dmap`)  
**Complementa:** [ART_STYLE_GUIDE.md](./ART_STYLE_GUIDE.md), [VISUAL_LANGUAGE.md](./VISUAL_LANGUAGE.md)  
**Versión:** 1.0  
**Estado:** Estándar obligatorio para producción, organización e integración de assets

---

> Este documento define **cómo nombrar, generar, organizar, versionar e integrar** todos los assets del juego. No define estilo visual (ver `ART_STYLE_GUIDE.md`) ni lenguaje de formas (ver `VISUAL_LANGUAGE.md`).

---

## Tabla de contenidos

1. [Visión general del pipeline](#1-visión-general-del-pipeline)
2. [Convención de nombres](#2-convención-de-nombres)
3. [Estructura de carpetas](#3-estructura-de-carpetas)
4. [Resoluciones y canvas](#4-resoluciones-y-canvas)
5. [Pivotes y puntos de anclaje](#5-pivotes-y-puntos-de-anclaje)
6. [Modularidad de piezas](#6-modularidad-de-piezas)
7. [Versionado](#7-versionado)
8. [Flujo generate2dsprite](#8-flujo-generate2dsprite)
9. [Flujo generate2dmap](#9-flujo-generate2dmap)
10. [Integración en Bevy](#10-integración-en-bevy)
11. [Metadatos y manifiestos](#11-metadatos-y-manifiestos)
12. [Checklist de entrega](#12-checklist-de-entrega)

---

## 1. Visión general del pipeline

### 1.1 Flujo de producción

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Documentos     │     │  Agent Sprite    │     │  Postproceso    │
│  docs/ (guías)  │────▶│  Forge           │────▶│  chroma-key, QC │
│                 │     │  (image_gen)     │     │  ASSET_REVIEW   │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                        ┌──────────────────┐              │
                        │  Bevy Engine     │◀─────────────┘
                        │  ECS integration │
                        └──────────────────┘
```

### 1.2 Documentos de referencia obligatorios

| Documento | Contenido | Cuándo consultar |
|---|---|---|
| [GAME_ART_BIBLE.md](./GAME_ART_BIBLE.md) | Constitución, invariantes | Siempre primero |
| [ART_STYLE_GUIDE.md](./ART_STYLE_GUIDE.md) | Cámara, luz, color, materiales, escala | Todo prompt de generación |
| [VISUAL_LANGUAGE.md](./VISUAL_LANGUAGE.md) | Formas, siluetas, composición | Diseño visual |
| [ASSET_REVIEW_GUIDE.md](./ASSET_REVIEW_GUIDE.md) | QA, scoring A/B/C/REJECT | Antes de integrar |
| [ASSET_PIPELINE.md](./ASSET_PIPELINE.md) | Nombres, carpetas, pivotes, Bevy | Producción e integración |
| [NEIGHBORHOOD_DESIGN_GUIDE.md](./NEIGHBORHOOD_DESIGN_GUIDE.md) | Layout de barrios | Mapas y POIs |

### 1.3 Principios del pipeline

1. **Un asset = un nombre = una carpeta = un manifiesto.**
2. **Generar → postprocesar → validar → integrar.** No saltar pasos.
3. **Foundation-only** para mapas base; props siempre separados.
4. **Modularidad primero:** piezas de vehículo antes que vehículos completos preensamblados.
5. **Prompt guardado siempre** junto al asset final.

---

## 2. Convención de nombres

### 2.1 Reglas generales

| Regla | Especificación | Ejemplo |
|---|---|---|
| **Case** | `snake_case` exclusivamente | `vehicle_chassis_small_01` |
| **Idioma** | Inglés para nombres de archivo | `house_small_01`, not `casa_pequeña_01` |
| **Separador** | Guión bajo `_` | `wheel_small_01` |
| **Numeración** | `_01`, `_02`, … `_99` (2 dígitos) | `engine_medium_03` |
| **Dirección isométrica** | Sufijo `_se`, `_sw`, `_nw`, `_ne` | `player_idle_se` |
| **Animación** | `<sujeto>_<acción>_<dirección>` | `player_walk_sw` |
| **Variantes de tamaño** | `_small`, `_medium`, `_large` | `vehicle_chassis_large_01` |
| **Versionado** | Sufijo `_v1`, `_v2` solo en iteraciones del mismo diseño | `wheel_small_01_v2` |
| **Prohibido** | Espacios, mayúsculas, acentos, guiones medios | ❌ `Wheel-Small-01` |

### 2.2 Prefijos por categoría

| Prefijo | Categoría | Ejemplo |
|---|---|---|
| `player_` | Protagonista / jugador | `player_idle_se` |
| `npc_` | Personajes no jugables | `npc_rival_01_idle_se` |
| `vehicle_` | Vehículos completos o chassis | `vehicle_chassis_small_01` |
| `wheel_` | Ruedas modulares | `wheel_small_01` |
| `engine_` | Motores modulares | `engine_medium_02` |
| `bumper_` | Parachoques modulares | `bumper_small_01` |
| `seat_` | Asientos modulares | `seat_small_01` |
| `steering_` | Volantes modulares | `steering_01` |
| `exhaust_` | Escapes modulares | `exhaust_small_01` |
| `vehicle_accessory_` | Accesorios de vehículo | `vehicle_accessory_flag_01` |
| `road_` | Tiles de calle | `road_straight` |
| `sidewalk_` | Tiles de vereda | `sidewalk_straight` |
| `grass_` | Tiles de pasto | `grass_flat` |
| `house_` | Casas | `house_small_01` |
| `garage_` | Garajes | `garage_small_01` |
| `tree_` | Árboles | `tree_medium_01` |
| `prop_` | Props genéricos | `prop_trashcan_01` |
| `fx_` | Efectos visuales | `fx_dust_01` |
| `ui_` | Interfaz | `ui_button_play` |

### 2.3 Patrones de nombre por tipo

#### Personajes animados

```
player_<action>_<direction>
player_idle_se
player_idle_sw
player_walk_se
player_walk_sw
player_race_se
player_hurt_se
player_celebrate_se

npc_<id>_<action>_<direction>
npc_rival_01_idle_se
npc_rival_01_walk_sw
```

#### Piezas modulares de vehículo

```
vehicle_chassis_<size>_<nn>
vehicle_chassis_small_01
vehicle_chassis_small_02
vehicle_chassis_medium_01
vehicle_chassis_large_01

wheel_<size>_<nn>
wheel_small_01
wheel_small_02
wheel_large_01

engine_<size>_<nn>
engine_small_01
engine_medium_02

bumper_<size>_<nn>
seat_<size>_<nn>
steering_<nn>
exhaust_<size>_<nn>
vehicle_accessory_<name>_<nn>
```

#### Tiles de calle

```
road_<shape>
road_straight
road_corner
road_cross
road_deadend
road_tjunction

sidewalk_<shape>
sidewalk_straight
sidewalk_corner

grass_<variant>
grass_flat
grass_edge
```

#### Edificios y entorno

```
house_<size>_<nn>
house_small_01
house_medium_01

garage_<size>_<nn>
garage_small_01

tree_<size>_<nn>
tree_small_01
tree_medium_01
tree_large_01

prop_<name>_<nn>
prop_trashcan_01
prop_lamppost_01
prop_fence_01
```

#### Mapas

```
map_<zone>_<layer>
map_barrio_norte_base
map_barrio_norte_dressed_reference
map_barrio_norte_layered_preview
```

### 2.4 Nombres de archivos dentro de cada carpeta

| Archivo | Descripción | Obligatorio |
|---|---|---|
| `<name>.png` | Sprite final con alpha | Sí |
| `<name>.prompt.txt` | Prompt usado para generar | Sí |
| `<name>.meta.json` | Metadatos (pivote, snap points, escala) | Sí (modulares) |
| `raw-sheet.png` | Hoja cruda pre-chroma-key | Sí (si aplica) |
| `sheet-transparent.png` | Hoja procesada | Sí (animaciones) |
| `animation.gif` | Preview animado | Recomendado |
| `pipeline-meta.json` | QC del postproceso | Recomendado |

---

## 3. Estructura de carpetas

### 3.1 Árbol completo del proyecto

```
barriolibre/
├── ART_STYLE_GUIDE.md
├── VISUAL_LANGUAGE.md
├── ASSET_PIPELINE.md
│
├── assets/
│   ├── sprites/
│   │   ├── player/
│   │   │   ├── idle/
│   │   │   │   ├── se/
│   │   │   │   │   ├── player_idle_se.png
│   │   │   │   │   ├── player_idle_se.prompt.txt
│   │   │   │   │   └── frames/
│   │   │   │   └── sw/
│   │   │   └── walk/
│   │   ├── npc/
│   │   │   └── rival_01/
│   │   ├── vehicle/
│   │   │   ├── chassis/
│   │   │   │   ├── small/
│   │   │   │   │   ├── vehicle_chassis_small_01/
│   │   │   │   │   └── vehicle_chassis_small_02/
│   │   │   │   ├── medium/
│   │   │   │   └── large/
│   │   │   ├── wheels/
│   │   │   ├── engines/
│   │   │   ├── bumpers/
│   │   │   ├── seats/
│   │   │   ├── steering/
│   │   │   ├── exhausts/
│   │   │   └── accessories/
│   │   └── fx/
│   │
│   ├── props/
│   │   ├── prop_trashcan_01/
│   │   │   ├── prop_trashcan_01.png
│   │   │   ├── prop_trashcan_01.prompt.txt
│   │   │   └── prop_trashcan_01.meta.json
│   │   ├── houses/
│   │   │   └── house_small_01/
│   │   ├── garages/
│   │   ├── trees/
│   │   └── street/
│   │
│   ├── maps/
│   │   └── barrio_norte/
│   │       ├── map_barrio_norte_base.png
│   │       ├── map_barrio_norte_base.prompt.txt
│   │       ├── map_barrio_norte_dressed_reference.png
│   │       └── map_barrio_norte_layered_preview.png
│   │
│   ├── tilesets/
│   │   ├── road/
│   │   │   ├── road_straight.png
│   │   │   ├── road_corner.png
│   │   │   ├── road_cross.png
│   │   │   └── road_deadend.png
│   │   ├── sidewalk/
│   │   └── terrain/
│   │
│   └── atlases/
│       ├── player_atlas.json
│       ├── player_atlas.png
│       ├── vehicle_parts_atlas.json
│       └── vehicle_parts_atlas.png
│
├── data/
│   ├── maps/
│   │   ├── barrio_norte_props.json
│   │   ├── barrio_norte_collision.json
│   │   └── barrio_norte_scene_hooks.json
│   ├── vehicles/
│   │   ├── snap_points.json
│   │   └── default_builds.json
│   └── characters/
│       └── player_animations.json
│
└── src/
    └── (código Bevy)
```

### 3.2 Reglas de carpetas

1. **Un slug = una carpeta** con el mismo nombre: `vehicle_chassis_small_01/`.
2. **Subcategorías por tipo**, no por fecha ni por autor.
3. **Frames de animación** en subcarpeta `frames/` dentro de la carpeta de la acción.
4. **No mezclar** assets finales con raw sheets en el mismo nivel — raw en la misma carpeta pero con prefijo `raw-`.
5. **Atlases** generados en `assets/atlases/`; nunca editar a mano los PNG de atlas.

---

## 4. Resoluciones y canvas

### 4.1 Tabla de resoluciones

| Tipo de asset | Canvas (px) | Área segura (px) | Unidades mundo |
|---|---|---|---|
| **Tile de suelo** | 256 × 128 | 240 × 112 | 1.0 × 0.5 u |
| **Tile de pared (1 u alto)** | 256 × 256 | 232 × 232 | 1.0 u alto |
| **Prop compacto** | 256 × 256 | 216 × 216 (centro) | ≤ 1 tile |
| **Prop grande / edificio** | 512 × 512 | 480 × 480 | 2–4 tiles |
| **Pieza modular vehículo** | 256 × 256 | 200 × 200 (centro) | Ver §6 |
| **Personaje / vehículo (frame)** | 384 × 384 | 260 × 300 (centro 70%) | 1.0 u alto |
| **Mapa base (foundation)** | Múltiplo de 256 | — | Grid de tiles |
| **Hoja de animación 2×2** | 768 × 768 | 230 × 270 por celda | — |
| **Hoja de animación 2×3** | 768 × 1152 | 230 × 270 por celda | — |
| **Prop pack 3×3** | 768 × 768 | 216 × 216 por celda | — |

### 4.2 Reglas de canvas

- **Fondo de generación (sprites):** `#FF00FF` sólido, sin gradiente.
- **Fondo de generación (mapas):** sin transparencia; imagen opaca completa.
- **Margen mínimo en celda de animación:** 15% por lado (personajes/vehículos).
- **Nada toca el borde de celda** en animaciones — rechazar en QC.
- **Mismo scale** entre frames de una misma acción (usar `shared_scale` en postproceso).

---

## 5. Pivotes y puntos de anclaje

### 5.1 Sistema de coordenadas

```
Origen del sprite: esquina superior izquierda (0, 0)
Pivote: porcentaje (0.0 – 1.0) desde esquina superior izquierda

        (0,0) ──────────────── X+
          │
          │    ┌───────────┐
          │    │           │
          │    │     ·     │  ← pivote (0.5, 0.85)
          │    │           │
          │    └─────●──────┘  ← punto de contacto suelo
          │
          Y+
```

### 5.2 Pivotes estándar por categoría

| Categoría | Pivote (X, Y) | Punto de contacto | Notas |
|---|---|---|---|
| **Personaje (pie)** | `(0.5, 0.92)` | Centro de los pies | Ancla Y-sort |
| **Vehículo completo** | `(0.5, 0.88)` | Centro de ruedas en suelo | Ancla Y-sort |
| **Pieza modular** | `(0.5, 0.5)` | Centro geométrico | Encaje en snap point |
| **Rueda** | `(0.5, 0.75)` | Punto de contacto con suelo | Snap en chassis |
| **Prop compacto** | `(0.5, 0.90)` | Base del objeto | Ancla Y-sort |
| **Edificio** | `(0.5, 0.95)` | Centro de footprint isométrico | Ancla Y-sort |
| **Árbol** | `(0.5, 0.92)` | Base del tronco | Ancla Y-sort |
| **Tile de suelo** | `(0.5, 0.5)` | Centro del diamante | Grid snap |
| **FX** | `(0.5, 0.5)` | Centro | Spawn en posición |

### 5.3 Snap points (piezas modulares)

Definidos en `<name>.meta.json` como coordenadas normalizadas (0.0–1.0) relativas al **chassis**:

```json
{
  "id": "vehicle_chassis_small_01",
  "pivot": [0.5, 0.88],
  "size_units": [0.90, 0.55, 0.70],
  "snap_points": {
    "wheel_fl": [0.15, 0.82],
    "wheel_fr": [0.85, 0.82],
    "wheel_rl": [0.20, 0.88],
    "wheel_rr": [0.80, 0.88],
    "engine_snap": [0.50, 0.55],
    "seat_snap": [0.50, 0.45],
    "steering_snap": [0.55, 0.50],
    "bumper_snap": [0.50, 0.72],
    "exhaust_snap": [0.12, 0.65]
  }
}
```

### 5.4 Reglas de pivote

1. **Todos los objetos con Y-sort** usan pivote en la base (Y ≥ 0.88).
2. **Piezas modulares** usan pivote central (0.5, 0.5) para rotación/encaje.
3. **El pivote nunca cambia** entre variantes de la misma categoría.
4. **Documentar pivote** en `.meta.json` — Bevy lo lee en runtime.
5. **Validar visualmente:** superponer pieza sobre chassis; el snap point debe alinearse sin offset visible > 2 px.

---

## 6. Modularidad de piezas

### 6.1 Contrato técnico de compatibilidad

Toda pieza modular debe cumplir:

| Propiedad | Estándar | Fuente |
|---|---|---|
| Perspectiva | Isométrica 2:1, dirección SE | ART_STYLE_GUIDE §2 |
| Escala | Relativa a niño = 1.0 u | ART_STYLE_GUIDE §4 |
| Pivote | Según §5.2 de este documento | ASSET_PIPELINE §5 |
| Snap points | Según §5.3 de este documento | ASSET_PIPELINE §5 |
| Outline | 2 px `#2A2030` | ART_STYLE_GUIDE §7.3 |
| Canvas | 256 × 256 px | ASSET_PIPELINE §4 |
| Fondo | `#FF00FF` → alpha | ART_STYLE_GUIDE G-035 |

### 6.2 Tiers de compatibilidad

```
TIER SMALL                TIER MEDIUM              TIER LARGE
─────────────────         ─────────────────        ─────────────────
chassis_small_*           chassis_medium_*         chassis_large_*
engine_small_*            engine_medium_*          engine_large_*
wheel_small_*             wheel_small_* +          wheel_large_*
                          wheel_large_*
bumper_small_*            bumper_medium_*          bumper_large_*
seat_small_*              seat_medium_*            seat_large_*
exhaust_small_*           exhaust_medium_*         exhaust_large_*
```

**Regla:** piezas de un tier encajan en chassis del **mismo tier**. Ruedas small encajan en cualquier tier; ruedas large solo en medium y large.

### 6.3 Orden de producción modular

```
Fase 1 — Chassis (6–12 variantes, 3 tiers)
    ↓
Fase 2 — Ruedas (8–16 variantes)
    ↓
Fase 3 — Motores, asientos, volantes (6–10 c/u)
    ↓
Fase 4 — Parachoques, escapes, accesorios (4–10 c/u)
    ↓
Fase 5 — Validación de combinación (todos × todos del tier)
    ↓
Fase 6 — Vehículos preensamblados de referencia (opcional, para marketing/UI)
```

### 6.4 Test de combinación automatizable

Para cada lote de piezas nuevas, verificar:

1. Cargar `snap_points.json` + `.meta.json` de cada pieza.
2. Superponer en canvas 512 × 512 de prueba.
3. Verificar: sin solapamiento de alpha > 10% entre piezas no adyacentes.
4. Verificar: silueta combinada pasa Silhouette Test (VISUAL_LANGUAGE §6.1).
5. Exportar preview combinado como `<chassis>_<pieces>_combo_preview.png`.

---

## 7. Versionado

### 7.1 Esquema de versiones

| Nivel | Formato | Cuándo incrementar | Ejemplo |
|---|---|---|---|
| **Asset version** | `_v1`, `_v2` en carpeta | Rediseño visual del mismo slot | `wheel_small_01_v2/` |
| **Document version** | `1.0`, `1.1` en header MD | Cambio en guías | ART_STYLE_GUIDE v1.1 |
| **Manifest version** | `"version": "1.0"` en JSON | Cambio de schema o snap points | meta.json |
| **Atlas version** | `player_atlas_v1` | Regeneración de atlas | atlases/ |

### 7.2 Reglas de versionado

1. **No sobrescribir** assets aprobados — crear `_v2`.
2. **Mantener `_v1`** hasta que `_v2` pase QC y se integre en Bevy.
3. **Documentar cambio** en `CHANGELOG.md` del asset (1 línea).
4. **Snap points:** cambiar snap points = nueva versión de meta.json + re-validar combinaciones.
5. **Prompt siempre** corresponde a la versión activa.

### 7.3 Estados de un asset

```
draft → generated → processed → qc_pass → integrated → deprecated
  │         │           │           │           │            │
  │         │           │           │           │            └─ reemplazado por _v2
  │         │           │           │           └─ cargado en Bevy
  │         │           │           └─ pasa checklist §12
  │         │           └─ chroma-key + extract OK
  │         └─ raw sheet generado
  └─ prompt escrito, no generado aún
```

Registrar estado en `.meta.json`:

```json
{
  "status": "qc_pass",
  "version": "1.0",
  "created": "2026-07-05",
  "prompt_ref": "wheel_small_01.prompt.txt"
}
```

---

## 8. Flujo generate2dsprite

### 8.1 Cuándo usar

- Personajes, NPCs, piezas modulares, props, FX, animaciones.
- **No usar** para mapas base ni tilesets de terreno (usar generate2dmap).

### 8.2 Parámetros del proyecto

| Parámetro | Valor |
|---|---|
| `art_style` | `project-native` |
| `view` | `3/4` |
| `anchor` | `feet` (personajes/vehículos) o `center` (piezas modulares) |
| `margin` | `safe` (15%) |
| `background` | `#FF00FF` |
| `shared_scale` | `true` (animaciones) |
| `component_mode` | `largest` (body grids), `all` (FX/projectiles) |

### 8.3 Workflow por tipo de asset

#### Pieza modular (single)

```
1. Escribir prompt (incluir bloques de ART_STYLE_GUIDE + VISUAL_LANGUAGE)
2. image_gen → raw en fondo #FF00FF, canvas 256×256
3. generate2dsprite.py process → chroma-key, extract
4. QC: escala, pivote, snap points, Silhouette Test
5. Guardar: <name>.png + .prompt.txt + .meta.json
6. Test de combinación con ≥ 2 chassis
```

#### Personaje animado (hero_action_bundle)

```
1. Generar una hoja por acción/dirección (grid 2×2 mínimo, NO strip 1×4)
2. idle: 2×2 (4 frames) × 4 direcciones = 4 hojas
3. walk: 2×2 o 2×3 × 4 direcciones
4. Process cada hoja independientemente
5. QC: escala consistente entre acciones (±10-15% body height)
6. Ensamblar atlas de engine si Bevy lo requiere
7. Guardar frames/ + sheet-transparent.png + animation.gif
```

#### Prop compacto (prop pack 3×3)

```
1. Clasificar: solo compact_prop (VISUAL_LANGUAGE + generate2dmap rules)
2. Listar 9 props exactos en el prompt
3. Generar hoja 3×3 en #FF00FF
4. extract_prop_pack.py → 9 PNGs individuales
5. QC: ningún prop toca borde de celda
6. Guardar cada uno en assets/props/<name>/
```

### 8.4 Bloque de prompt estándar (sprites)

```
[INICIO — copiar en todo prompt generate2dsprite]

Carreras de Barrio — art style guide v1.0 + visual language v1.0.
Clean HD hand-painted cartoon, Latin American neighborhood, cheerful recycled aesthetic.
Fixed isometric 2:1 camera, 30° elevation, 45° azimuth NE, view direction SE default.
Mid-morning lighting from NE (55° elevation), warm #FFF5E6, shadows toward SW at 35% opacity #3A3A5C.
Outline 2px #2A2030 on characters/vehicles, 1.5px on buildings/props.
Shape language: squares, rectangles, trapezoids dominant; round heads/wheels/trees.
Composition: 70% primary shape, 20% secondary, 10% personality details.
Recycled = clean, functional, ingenious — never dirty trash.
Solid #FF00FF background. No pixel art, no photorealism, no readable text, no watermarks.

ASSET: <nombre_del_asset>
CATEGORY: <categoría>
CANVAS: <resolución>
PIVOT: <x, y>

[DESCRIPIÓN ESPECÍFICA DEL ASSET]

MANDATORY RULES (Carreras de Barrio v1.0):
- Isometric 2:1, 30° elevation, NE light, SW shadows
- Clean HD cartoon, Latin American neighborhood, recycled homemade aesthetic
- No pixel art, no photorealism, no readable text, no violence
- Palette and scale per ART_STYLE_GUIDE.md
- Shape language and composition per VISUAL_LANGUAGE.md
- Naming and pivot per ASSET_PIPELINE.md
```

---

## 9. Flujo generate2dmap

### 9.1 Cuándo usar

- Mapas base (foundation-only), tilesets de terreno/calle, previews de nivel.
- **No usar** para personajes, vehículos, piezas modulares (usar generate2dsprite).

### 9.2 Parámetros del proyecto

| Parámetro | Valor |
|---|---|
| `map_mode` | `tile_mode` (calles, veredas) o `scene_mode` (barrio con props) |
| `perspective` | `isometric-like` |
| `art_style` | `project-native` |
| `visual_model` | `layered_raster` + props separados |
| `collision_model` | `tile_collision` + `precise_shapes` |
| `engine_target` | project-native (Bevy) |

### 9.3 Workflow de mapa de barrio

```
Fase 1 — Foundation
  1. Generar map_<zone>_base.png (SOLO terreno: calles, veredas, pasto)
  2. Sin props, casas, árboles, vehículos
  3. Guardar prompt

Fase 2 — Dressed reference
  4. view_image del base
  5. Generar map_<zone>_dressed_reference.png (≤ 9 objetos candidatos)
  6. Sin anotaciones, labels, flechas

Fase 3 — Props
  7. Listar objetos del dressed reference
  8. Clasificar cada uno (compact / wide / tall / collision / strip)
  9. Generar props con generate2dsprite (uno a uno o packs)
  10. Guardar en assets/props/

Fase 4 — Metadata
  11. Escribir data/maps/<zone>_props.json (posiciones)
  12. Escribir data/maps/<zone>_collision.json
  13. Escribir data/maps/<zone>_scene_hooks.json (spawns, triggers)

Fase 5 — QA
  14. Componer map_<zone>_layered_preview.png
  15. Validar dimensiones, alpha, coherencia de escala
```

### 9.4 Workflow de tilesets de calle

```
1. Definir tiles necesarios: straight, corner, cross, deadend, tjunction
2. Generar cada tile como prop isométrico 256×128
3. Validar: bordes de calzada alinean con tiles adyacentes
4. Guardar en assets/tilesets/road/
5. Escribir data/tilesets/road_manifest.json con IDs y conexiones
```

### 9.5 Regla foundation-only

**El mapa base NUNCA contiene:**
- Casas, garajes, árboles, postes, basureros
- Vehículos, personajes, FX
- Props interactivos, señales, checkpoints

Estos son assets separados con placement JSON.

---

## 10. Integración en Bevy

### 10.1 Convenciones de código Rust

```rust
// Ruta de assets — constantes
pub const ASSET_PATH_SPRITES: &str = "sprites";
pub const ASSET_PATH_PROPS: &str = "props";
pub const ASSET_PATH_TILESETS: &str = "tilesets";
pub const ASSET_PATH_MAPS: &str = "maps";
pub const ASSET_PATH_DATA: &str = "data";
```

### 10.2 Carga de sprites

```rust
// Ejemplo: cargar pieza modular
#[derive(Component)]
pub struct VehiclePart {
    pub part_id: String,       // "wheel_small_01"
    pub category: PartCategory, // Wheel, Engine, Bumper, ...
    pub tier: PartTier,         // Small, Medium, Large
}

// Pivote desde meta.json
#[derive(Deserialize)]
pub struct SpriteMeta {
    pub pivot: [f32; 2],        // [0.5, 0.88]
    pub size_units: [f32; 3],   // [0.90, 0.55, 0.70]
    pub snap_points: HashMap<String, [f32; 2]>,
}
```

### 10.3 Y-sort (orden de renderizado)

```rust
// Objetos isométricos: mayor Y mundial (sur) = renderizado encima
#[derive(Component)]
pub struct IsoDepth {
    pub y_sort_key: f32,  // posición Z del mundo (eje sur-norte)
}

// Sistema
fn y_sort_system(mut query: Query<(&IsoDepth, &mut Transform)>) {
    for (depth, mut transform) in query.iter_mut() {
        transform.translation.z = -depth.y_sort_key;
    }
}
```

### 10.4 Animaciones

```rust
// Definición en data/characters/player_animations.json
{
  "idle": {
    "se": { "frames": ["player_idle_se_00", "..."], "fps": 8, "loop": true },
    "sw": { "frames": ["player_idle_sw_00", "..."], "fps": 8, "loop": true }
  },
  "walk": {
    "se": { "frames": ["player_walk_se_00", "..."], "fps": 12, "loop": true }
  }
}
```

### 10.5 Tilemap

```rust
// Tilemap isométrico 2:1
pub const TILE_WIDTH: f32 = 256.0;
pub const TILE_HEIGHT: f32 = 128.0;
pub const TILE_WORLD_WIDTH: f32 = 1.0;  // unidades mundo
pub const TILE_WORLD_HEIGHT: f32 = 0.5;

// Conversión grid → mundo
fn tile_to_world(tile_x: i32, tile_y: i32) -> Vec3 {
    Vec3::new(
        (tile_x - tile_y) as f32 * TILE_WORLD_WIDTH * 0.5,
        0.0,
        (tile_x + tile_y) as f32 * TILE_WORLD_HEIGHT * 0.5,
    )
}
```

### 10.6 Ensamblaje de vehículo modular

```rust
#[derive(Component)]
pub struct VehicleAssembly {
    pub chassis_id: String,
    pub parts: Vec<InstalledPart>,
}

#[derive(Clone)]
pub struct InstalledPart {
    pub part_id: String,
    pub snap_point: String,  // "wheel_fl", "engine_snap", etc.
}

// Al instalar pieza: leer snap_point del chassis meta.json,
// posicionar pieza en coordenada del snap, renderizar encima del chassis
```

### 10.7 Atlas (TextureAtlas)

Generar atlas por categoría cuando haya > 8 sprites de la misma categoría:

| Atlas | Contenido | Cuándo generar |
|---|---|---|
| `player_atlas` | Todas las animaciones del jugador | Fase de personajes |
| `vehicle_parts_atlas` | Todas las piezas modulares | Fase modular completa |
| `props_atlas` | Props compactos del barrio | Fase de entorno |
| `road_atlas` | Tiles de calle | Fase de tilesets |

Formato: PNG + JSON con frames (Bevy `TextureAtlasLayout`).

### 10.8 Estructura de datos en runtime

```
data/
├── maps/
│   └── barrio_norte_props.json      ← posiciones de props en mapa
├── vehicles/
│   ├── snap_points.json             ← snap points globales por chassis
│   └── default_builds.json          ← builds predeterminados
├── characters/
│   └── player_animations.json       ← definición de animaciones
└── tilesets/
    └── road_manifest.json           ← conexiones de tiles de calle
```

---

## 11. Metadatos y manifiestos

### 11.1 `.meta.json` — pieza individual

```json
{
  "id": "wheel_small_01",
  "category": "wheel",
  "tier": "small",
  "version": "1.0",
  "status": "qc_pass",
  "created": "2026-07-05",
  "pivot": [0.5, 0.75],
  "size_units": [0.25, 0.25, 0.10],
  "size_pixels": [256, 256],
  "direction": "se",
  "prompt_ref": "wheel_small_01.prompt.txt",
  "tags": ["round", "tire", "rubber", "modular"]
}
```

### 11.2 `.meta.json` — chassis con snap points

```json
{
  "id": "vehicle_chassis_small_01",
  "category": "chassis",
  "tier": "small",
  "version": "1.0",
  "status": "qc_pass",
  "pivot": [0.5, 0.88],
  "size_units": [0.90, 0.55, 0.70],
  "snap_points": {
    "wheel_fl": [0.15, 0.82],
    "wheel_fr": [0.85, 0.82],
    "wheel_rl": [0.20, 0.88],
    "wheel_rr": [0.80, 0.88],
    "engine_snap": [0.50, 0.55],
    "seat_snap": [0.50, 0.45],
    "steering_snap": [0.55, 0.50],
    "bumper_snap": [0.50, 0.72],
    "exhaust_snap": [0.12, 0.65]
  },
  "compatible_tiers": ["small"],
  "prompt_ref": "vehicle_chassis_small_01.prompt.txt"
}
```

### 11.3 `snap_points.json` — registro global

```json
{
  "version": "1.0",
  "chassis": {
    "vehicle_chassis_small_01": {
      "meta_ref": "assets/sprites/vehicle/chassis/small/vehicle_chassis_small_01/vehicle_chassis_small_01.meta.json"
    }
  },
  "part_categories": {
    "wheel": { "pivot": [0.5, 0.75], "tiers": ["small", "large"] },
    "engine": { "pivot": [0.5, 0.5], "tiers": ["small", "medium", "large"] },
    "bumper": { "pivot": [0.5, 0.5], "tiers": ["small", "medium", "large"] },
    "seat": { "pivot": [0.5, 0.5], "tiers": ["small", "medium", "large"] },
    "steering": { "pivot": [0.5, 0.5], "tiers": ["universal"] },
    "exhaust": { "pivot": [0.5, 0.5], "tiers": ["small", "medium", "large"] }
  }
}
```

### 11.4 `<zone>_props.json` — placement de mapa

```json
{
  "map_id": "barrio_norte",
  "props": [
    {
      "id": "house_small_01",
      "asset": "props/houses/house_small_01/house_small_01.png",
      "position": [12, 8],
      "pivot": [0.5, 0.95],
      "y_sort": true,
      "collision": { "type": "box", "size": [2.0, 1.8] }
    }
  ]
}
```

---

## 12. Checklist de entrega

### 12.1 Todo asset

- [ ] Nombre cumple convención §2 (`snake_case`, prefijo correcto, numeración)
- [ ] Carpeta creada según §3
- [ ] `<name>.png` con alpha correcto
- [ ] `<name>.prompt.txt` guardado
- [ ] Resolución según §4
- [ ] Pivote según §5
- [ ] Pasa GLOBAL ART RULES (ART_STYLE_GUIDE §9)
- [ ] Pasa GLOBAL VISUAL RULES (VISUAL_LANGUAGE §10)
- [ ] Pasa ASSET_REVIEW_GUIDE — score **A** o **B**, checklist 10/10
- [ ] Estado en `.meta.json` = `qc_pass` (campo `review.score` documentado)

### 12.2 Pieza modular (adicional)

- [ ] `.meta.json` con snap points (si es chassis) o tier (si es pieza)
- [ ] Test de combinación con ≥ 2 chassis del mismo tier
- [ ] Sin solapamiento incoherente (> 2 px offset en snap)
- [ ] Registrada en `data/vehicles/snap_points.json`

### 12.3 Animación (adicional)

- [ ] Grid multi-fila (no strip 1×N)
- [ ] `shared_scale` aplicado; body height ±10-15% entre acciones
- [ ] Ningún frame toca borde de celda
- [ ] `animation.gif` generado para preview
- [ ] Frames individuales en `frames/`
- [ ] Definición en `data/characters/<name>_animations.json`

### 12.4 Mapa (adicional)

- [ ] Base = foundation-only (sin props baked)
- [ ] Dressed reference con ≤ 9 candidatos
- [ ] Props generados por separado
- [ ] `_props.json`, `_collision.json`, `_scene_hooks.json` escritos
- [ ] Layered preview compuesto y validado
- [ ] Dimensiones consistentes entre base, reference y preview

### 12.5 Tile (adicional)

- [ ] 256 × 128 px (diamante 2:1)
- [ ] Bordes alinean con tiles adyacentes (straight ↔ corner ↔ cross)
- [ ] Registrado en `data/tilesets/<set>_manifest.json`

---

## Apéndice A — Relación entre los 3 documentos

| Pregunta | Documento |
|---|---|
| ¿Qué color tiene el pasto? | ART_STYLE_GUIDE §5 |
| ¿Qué forma tiene la cabeza del niño? | VISUAL_LANGUAGE §3.1 |
| ¿Cómo se llama el archivo del motor? | ASSET_PIPELINE §2 |
| ¿Desde dónde viene la luz? | ART_STYLE_GUIDE §3 |
| ¿Cuánto detalle en un vehículo? | VISUAL_LANGUAGE §5 (70/20/10) |
| ¿Dónde va el pivote de una rueda? | ASSET_PIPELINE §5.2 |
| ¿Puede un triángulo ser forma principal? | VISUAL_LANGUAGE §2.3 (NO) |
| ¿Cómo se genera un prop pack? | ASSET_PIPELINE §8.3 |
| ¿Qué snap points tiene el chassis? | ASSET_PIPELINE §5.3 + §11.2 |
| ¿Cómo se carga en Bevy? | ASSET_PIPELINE §10 |

## Apéndice B — Historial de versiones

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-07-05 | Documento inicial — nombres, carpetas, pivotes, modularidad, Bevy, flujos |

---

*Fin de ASSET_PIPELINE.md*
