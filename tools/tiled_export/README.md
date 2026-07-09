# Guía de edición de mapas con Tiled

Flujo operativo para crear y editar barrios isométricos de **Carreras de Barrio** en [Tiled](https://www.mapeditor.org/), exportarlos al formato del motor Bevy y probarlos en el juego.

**Mapa de referencia:** `data/maps/barrio_tutorial_01/`

---

## Requisitos

| Herramienta | Uso |
|-------------|-----|
| **Tiled 1.10+** | Editor visual del mapa (`.tmx`) |
| **Python 3.10+** | Scripts de exportación en `tools/tiled_export/` |
| **Rust / Cargo** | Ejecutar el juego |

Tiled instalado en Windows suele estar en:

`C:\Program Files\Tiled\tiled.exe`

---

## Archivos del mapa

Cada barrio vive en su propia carpeta bajo `data/maps/<barrio_id>/`:

```
data/maps/barrio_tutorial_01/
├── barrio_tutorial_01.tmx      ← abrir esto en Tiled
├── environment_tutorial.tsx    ← tileset de suelo (19 tiles)
├── props_tutorial.tsx            ← tileset de props (9 objetos)
├── collision_tutorial.tsx        ← tileset marcador rojo (1 tile)
├── layout.json                 ← exportado → suelo que renderiza Bevy
├── props.json                  ← exportado → casas/árboles/etc. en Bevy
├── scene_hooks.json            ← exportado → spawn del jugador (capa `spawn`)
├── collision.json              ← exportado → celdas bloqueadas (capa `collision`)
```

**Regla:** editá solo el `.tmx` en Tiled. Los `.json` los genera el script de exportación.

---

## 1. Abrir el mapa

1. Tiled → **File → Open**
2. Elegí:
   ```
   data/maps/barrio_tutorial_01/barrio_tutorial_01.tmx
   ```
3. Verificá que en el panel derecho aparezcan **tres tilesets**:
   - `environment_tutorial` — césped, calles, veredas, cebras
   - `props_tutorial` — casas, árboles, fuente, faroles, etc.
   - `collision_tutorial` — marcador rojo de colisión (solo para editar, no se ve en el juego)

Si Tiled muestra tiles rotos, no movas los `.tsx`: deben quedar junto al `.tmx` con rutas relativas a `assets/environment/`.

---

## 2. Capas de tiles (suelo)

El mapa usa orientación **isométrica** (diamante 256×128 px).

| Capa | Qué pintar | ¿Se ve en el juego? |
|------|------------|---------------------|
| **`ground`** | Césped, calles, veredas, cebras, cruces | **Sí** (capa principal) |
| **`markings`** | Detalles extra sobre calzada (opcional) | Guardado; render futuro |
| **`overlay`** | Decoración de suelo fina (opcional) | Guardado; render futuro |

### Pintar tiles

1. Panel **Layers** → seleccioná `ground` (o `markings` / `overlay`).
2. Herramienta **Stamp Brush** (sello / pincel).
3. Tileset `environment_tutorial` → elegí un tile.
4. Clic en el mapa para colocarlo.

**Consejo:** alterná variantes de césped (`grass_clean_01` … `04`) para evitar repetición visible.

### Tiles disponibles (suelo)

- **Césped:** `grass_clean_01` … `grass_clean_04`
- **Calles:** rectas H/V, esquinas NE/NW/SE/SW, cruce, T (N/S/E/W), asfalto liso
- **Cebras:** `road_crosswalk_h_01`, `road_crosswalk_v_01`
- **Vereda:** `sidewalk_straight_01`

---

## 3. Capa de objetos `props`

Los props **no** van en capas de tiles: van en la capa de objetos **`props`**.

### Colocar un prop

1. Panel **Layers** → seleccioná **`props`** (icono de objeto).
2. Herramienta **Insert Tile** (tile con flecha hacia abajo).
3. Tileset **`props_tutorial`** → elegí el prop.
4. Clic en el mapa.

Los props usan anclaje **inferior-centro** (`objectalignment="bottom"`): se apoyan sobre la celda donde los colocás.

### Mover, escalar y borrar

| Acción | Cómo |
|--------|------|
| Mover | **Select Objects** (flecha) → arrastrar |
| Escalar | Seleccionar → tirar de las esquinas del marco |
| Borrar | Seleccionar → **Supr** |

El tamaño que dejés en Tiled se exporta a `props.json` (`width_px`, `height_px`) y el juego lo respeta.

### Props disponibles

| ID | Descripción |
|----|-------------|
| `house_red_01` | Casa ladrillo rojo |
| `house_blue_01` | Casa azul |
| `house_yellow_01` | Casa amarilla |
| `house_wood_01` | Casa de madera |
| `tree_01` | Árbol |
| `lamp_01` | Farol |
| `bench_01` | Banco |
| `fountain_01` | Fuente / pileta |
| `hydrant_01` | Grifo / hidrante |

### Profundidad isométrica

En vista isométrica, lo que está más **abajo-derecha** tapa lo de arriba-izquierda. Si un árbol tapa una casa:

- Mové el prop un poco, o
- Usá el menú de capa de objetos para subir/bajar orden (si hace falta).

---

## 4. Capa de objetos `spawn`

El punto de aparición del jugador va en la capa de objetos **`spawn`**.

1. Panel **Layers** → **`spawn`**
2. Herramienta **Insert Point**
3. Clic en la celda deseada (plaza central en el tutorial)
4. Opcional: nombre `tutorial_spawn`, propiedad `facing` = `south`

El exportador escribe `scene_hooks.json` con `spawn_points[].position` en coordenadas de grilla.

---

## 5. Capa de tiles `collision` (colisiones del jugador)

Las celdas donde el jugador **no puede caminar** se pintan en la capa de tiles **`collision`**.

### Redimensionar colisiones (capa de objetos)

Los tiles de la capa **`collision`** tienen tamaño fijo (256×128): **W y H aparecen bloqueados** en Atributos porque no son objetos, son celdas de la grilla.

Para **rectángulos redimensionables** (arrastrar esquinas, editar W/H):

1. En **Layers**, seleccioná o creá la capa de objetos **`collision_zones`**
   - **Layer → Add Layer → Object Layer** → nombre exacto: `collision_zones`
2. Herramienta **Insert Rectangle** (rectángulo, no Insert Tile)
3. Dibujá un rectángulo sobre el área que debe bloquear (casa, árbol, etc.)
4. Herramienta **Select Objects** (flecha) → clic en el rectángulo
5. En **Atributos → Rectangle**, **W** y **H** ya se pueden editar, o arrastrá las esquinas
6. El exportador convierte cada rectángulo en las celdas de grilla que cubre

Podés usar **`collision`** (tiles, celda a celda) y **`collision_zones`** (rectángulos) a la vez; se combinan al exportar.

### Paso a paso — tiles (`collision`)

1. Abrí `data/maps/barrio_tutorial_01/barrio_tutorial_01.tmx`
2. En el panel **Layers** (capas), buscá la capa **`collision`**
   - Si no existe: **Layer → Add Layer → Tile Layer** → nombrala exactamente `collision`
3. Seleccioná la capa **`collision`** (debe quedar resaltada)
4. En **View → Show Tile Object Outlines** (opcional) para ver mejor la grilla
5. Para ver el mapa mientras pintás:
   - Dejá `ground` visible
   - Podés ocultar `markings` / `overlay` (icono del ojo)
   - La capa `collision` tiene opacidad ~55% para ver debajo
6. Herramienta **Stamp Brush** (sello / pincel de tiles)
7. Tileset **`collision_tutorial`** → elegí el tile rojo `collision_blocked_01`
8. Pintá cada celda donde el jugador debe **chocar**:
   - Base de casas (5 celdas en cruz suele alcanzar)
   - Tronco de árboles (1 celda)
   - Faroles / fuente (1–4 celdas según tamaño)
   - **No** pintes calles ni veredas transitables
9. Para borrar: herramienta **Eraser** (goma) sobre la capa `collision`
10. **Ctrl+S** guardar el `.tmx`

### Exportar colisiones al motor

Desde la raíz del repo:

```powershell
python tools/tiled_export/export_layout.py data/maps/barrio_tutorial_01/barrio_tutorial_01.tmx
```

Salida esperada:

```
Exported .../collision.json (N blocked cells)
```

### Probar en el juego

```powershell
cargo run
```

Enter → Gameplay. El jugador debe chocar con las celdas que pintaste.

### Reglas

| Hacé esto | Evitá esto |
|-----------|------------|
| Capa llamada exactamente **`collision`** | Renombrar a `collisions` u otro nombre |
| Usar tile de **`collision_tutorial`** | Pintar colisiones en la capa `ground` |
| Exportar después de editar | Editar `collision.json` a mano |
| Pintar solo donde bloquea el walk | Pintar toda la calle de rojo |

### Punto de partida automático

Si regenerás el mapa de referencia:

```powershell
python tools/tiled_export/build_barrio_reference.py
```

Eso crea una capa `collision` inicial desde `data/collision/prop_footprints.json`. Después ajustás a mano en Tiled.

---

## 6. Reglas importantes

| Hacé esto | Evitá esto |
|-----------|------------|
| Guardar como `barrio_tutorial_01.tmx` en su carpeta | Renombrar capas (`ground`, `markings`, `overlay`, `collision`, `props`, `spawn`) |
| Usar tiles de los tilesets del proyecto | Mover o renombrar `.tsx` fuera de la carpeta del mapa |
| Exportar con el script de Python | Exportar JSON manualmente desde Tiled |
| **Ctrl+S** después de editar | Borrar propiedades `tile_id` / `prop_id` de los tilesets |

### Ampliar el mapa

**Map → Resize Map** → aumentá width/height. Rellená con césped. Después exportá de nuevo.

---

## 7. Exportar al motor (layout + props + spawn + collision)

Desde la raíz del repo:

```powershell
cd c:\Users\tecnova\Desktop\barriolibre
python tools/tiled_export/export_layout.py data/maps/barrio_tutorial_01/barrio_tutorial_01.tmx
```

Salida esperada:

```
Exported .../layout.json
Size: 24x24
Ground layer rows: 24
Exported .../props.json (64 props)
Exported .../scene_hooks.json (1 spawn points)
Exported .../collision.json (N blocked cells)
```

### Qué genera cada archivo

| Archivo | Origen en Tiled | Uso en Bevy |
|---------|-----------------|-------------|
| `layout.json` | Capas `ground`, `markings`, `overlay` | Tilemap de suelo |
| `props.json` | Capa de objetos `props` | Sprites de casas, árboles, etc. |
| `scene_hooks.json` | Capa de objetos `spawn` | Posición inicial del jugador |
| `collision.json` | Capa de tiles `collision` | Celdas bloqueadas para el jugador |

### Editor in-game (F2) — opcional

El editor **F2** en el juego sigue disponible para ajustes rápidos. Si `collision.json` tiene celdas (exportado desde Tiled), **ese archivo manda** al cargar el mapa.

### Opciones del exportador

```powershell
# Solo suelo, sin tocar props.json
python tools/tiled_export/export_layout.py data/maps/.../mapa.tmx --no-props

# Sin exportar scene_hooks.json
python tools/tiled_export/export_layout.py data/maps/.../mapa.tmx --no-hooks

# Sin exportar collision.json
python tools/tiled_export/export_layout.py data/maps/.../mapa.tmx --no-collision

# Ruta custom de salida
python tools/tiled_export/export_layout.py data/maps/.../mapa.tmx --output data/maps/.../layout.json --props-output data/maps/.../props.json --hooks-output data/maps/.../scene_hooks.json
```

---

## 6. Probar en el juego

```powershell
cargo run
```

1. Menú → **Enter** para entrar al barrio.
2. Controles de cámara en **Gameplay**:

| Acción | Teclas |
|--------|--------|
| Mover cámara | `W A S D` o flechas |
| Alejar zoom | `Q`, `-`, rueda abajo |
| Acercar zoom | `E`, `+`, rueda arriba |

El zoom inicial está alejado para ver más mapa. Si cambiaste `layout.json` o `props.json`, reiniciá el juego para recargar.

---

## 7. Flujo completo (resumen)

```
┌─────────────┐     Ctrl+S      ┌──────────────────┐
│   Tiled     │ ──────────────► │  barrio.tmx      │
│  (editar)   │                 │  + tilesets .tsx │
└─────────────┘                 └────────┬─────────┘
                                       │
                          export_layout.py
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                         ▼
             layout.json                              props.json
                    │                                         │
                    └──────────────────┬──────────────────────┘
                                       │
                                   cargo run
                                       │
                                       ▼
                              Bevy (suelo + props)
```

1. Abrí el `.tmx` en Tiled.
2. Pintá suelo en `ground`; opcionalmente `markings` / `overlay`.
3. Colocá props en la capa `props` con **Insert Tile**.
4. Guardá (`Ctrl+S`).
5. Ejecutá `export_layout.py`.
6. `cargo run` y probá con Enter + WASD.

---

## 8. Scripts relacionados (mantenimiento)

Solo los necesitás si regenerás assets o un mapa desde cero:

| Script | Cuándo usarlo |
|--------|----------------|
| `generate_tileset.py` | Regenerar `.tsx` y plantilla `.tmx` tras agregar tiles al repo |
| `build_barrio_reference.py` | Generar mapa de ejemplo programáticamente (calles + props) |
| `build_tutorial_tiles.py` | Reprocesar PNGs de suelo a diamante isométrico |
| `make_prop.py` | Procesar un prop nuevo (magenta → PNG transparente) |
| `preview_barrio.py` | Vista previa PNG del mapa (QC visual) |

Regenerar tilesets (tras cambiar lista de tiles en código):

```powershell
python tools/tiled_export/generate_tileset.py --map-id barrio_tutorial_01 --width 24 --height 24
```

Luego reabrí el `.tmx` en Tiled si ya estaba abierto.

---

## 9. Solución de problemas

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Tiled: "Corrupt layer data" | `.tmx` dañado o capa mal formada | Regenerá con `generate_tileset.py` o restaurá desde git |
| Tiles rotos en Tiled | Rutas de `.tsx` rotas | No movas tilesets; mantené `../../../assets/environment/...` |
| Props no aparecen en el juego | No exportaste o capa mal nombrada | Capa debe llamarse **`props`**; corré `export_layout.py` |
| `Unknown prop gid=…` al exportar | Objeto de tileset que no es `props_tutorial` | Usá solo **Insert Tile** desde `props_tutorial` |
| Suelo desordenado en Bevy | Tiles no son diamante 2:1 | Reprocesá con `make_iso_diamond_tile.py` / `build_tutorial_tiles.py` |
| Mapa muy grande en pantalla | Zoom | En juego: `Q` / rueda para alejar |

---

## 10. Crear un barrio nuevo (checklist)

1. Copiá la carpeta `barrio_tutorial_01` → `barrio_mi_zona_01`.
2. Renombrá `barrio_mi_zona_01.tmx` y actualizá `barrio_id` en exports.
3. Ajustá `data/config/game.toml` → `default_map = "barrio_mi_zona_01"` (o cargá el mapa que corresponda).
4. Editá en Tiled, exportá, probá con `cargo run`.

---

**Ver también:** [NEIGHBORHOOD_DESIGN_GUIDE.md](../../docs/world/NEIGHBORHOOD_DESIGN_GUIDE.md) (diseño del barrio), [ASSET_PIPELINE.md](../../docs/production/ASSET_PIPELINE.md) (pipeline de assets).
