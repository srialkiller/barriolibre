# barrio_tutorial_01 — Mejoras de diseño

Rediseño del barrio tutorial para que **enseñe por el escenario**, no por ventanas
de ayuda. Mapa pequeño, memorable y fácil de leer, con un barrio latinoamericano
de clase media distribuido de forma lógica.

El `.tmx` es la **fuente de verdad** (editable en Tiled). Los cuatro `.json` se
generan con el pipeline existente (`tools/tiled_export/export_layout.py`) y el
mapa supera `map_validator`.

## Layout

- Grilla limpia de **2 avenidas horizontales + 2 verticales** (2 celdas de ancho)
  que enmarcan una **plaza central** y forman 4 intersecciones y 9 manzanas.
- **Plaza central** (punto visual principal, visible desde todo el mapa):
  fuente, bancas, faroles, árboles y caminos peatonales en diagonal (X).
- **Veredas completas** bordeando cada avenida.
- **Pasos peatonales** (cebras) en las 4 entradas de la plaza.

## Edificios (8 por manzana)

6 viviendas usan las 4 variantes de casa (rojo/azul/amarillo/madera) y 2 manzanas
son landmarks con **sprite propio**: la Tienda y el Garaje. La variedad se logra
por edificio, color, jardín, arbolado y mobiliario. Todo edificio tiene acceso
desde la vereda y bloquea colisión en 3x3.

Landmarks:

| Landmark        | Sprite       | Manzana | Rol de gameplay                          |
|-----------------|--------------|---------|------------------------------------------|
| Tienda          | `shop_01`    | Norte   | almacén del barrio (toldo, vitrina)      |
| Casa de Pedro   | `house_wood_01` | Sur  | junto al spawn — primer contacto         |
| Garaje          | `garage_01`  | Este    | meta bloqueada que se desbloquea al final |

## Vegetación y props

- Árboles **agrupados** en jardines dentro de cada manzana (no aleatorios).
- Mobiliario urbano distribuido con lógica: bancas y faroles hacia la plaza,
  grifos en las esquinas. Cada prop tiene footprint de colisión (sub-tile para
  árboles/faroles/bancas/grifos; celda completa para casas y fuente).

## Arte de props (volumen y detalle)

Los 9 props se **regeneraron** con un estilo isométrico coherente (perspectiva
2:1, luz cálida arriba-izquierda, oclusión ambiental suave, contorno oscuro
nítido, estilo pixel-art pintado tipo tileset isométrico de calidad) para darles
**cuerpo/volumen** en lugar del look plano anterior, siguiendo las referencias.

- Se generó cada pieza sobre fondo magenta plano (`#FF00FF`) y se limpió con
  chroma-key + recorte ajustado (`tools/tiled_export/regen_props.py`).
- Se conservan **los mismos IDs y rutas** (`assets/environment/props/<id>.png`),
  así que el runtime toma el arte nuevo **sin tocar código**.
- Props actualizados: `house_red_01`, `house_blue_01`, `house_yellow_01`,
  `house_wood_01`, `tree_01`, `fountain_01`, `lamp_01`, `bench_01`, `hydrant_01`.
- Props nuevos con identidad propia: `shop_01` (tienda/almacén) y `garage_01`
  (garaje bloqueado). Se registran en `PROP_TILES` (generate_tileset) y en
  `PROP_TARGET_HEIGHT` (build_barrio_reference); `build_barrio_reference.py`
  regenera `props_tutorial.tsx` para mantener el tileset sincronizado.

## Arte de tiles de suelo (textura y volumen)

Los 19 tiles isométricos se re-texturizan con **caras iso** (cara superior +
laterales inferior-izq / inferior-der), luz NW y sin el bevel perimetral que
generaba la grilla visible entre celdas. Script: `regen_tiles.py`.

## Flujo de gameplay (guiado por el escenario)

```
Spawn (plaza, [13,13])
  -> Pedro está al lado ([12,13]): hablar
  -> explorar la plaza: Cartón (N), Alambre (O), Chapitas (S)
  -> abrir inventario
  -> volver con Pedro
  -> se desbloquea el Garaje (Este)
```

## Contratos respetados (no romper runtime)

- Spawn fijo en `[13,13]`; NPC inicial `pedro_vecino`; exactamente 3 pickups,
  ninguno en el spawn (test en `src/world/map/resources.rs`).
- Materiales de pickup: `cardboard`, `wire`, `bottle_caps` — requeridos por la
  quest `tutorial_first_cart`. Los nombres visibles quedan en español
  (Cartón limpio / Alambre / Chapitas).
- Se mantienen los mismos IDs/rutas de props y tiles (el arte nuevo reemplaza
  in-place; no se agregan ni renombran assets).
- Capas de tiles: `ground`, `markings`, `overlay`, `collision`.
- Object layers: `props`, `spawn`, `npcs`, `pickups`, `collision_zones`.

## Validación realizada

- `map_validator` → OK (layout, hooks, collision, props).
- Reexportado con `export_layout.py` sin errores.
- BFS de caminabilidad: 100% de las celdas transitables son alcanzables desde
  el spawn (el jugador nunca queda bloqueado); Pedro y los 3 pickups accesibles.
- Sin props flotantes, sin celdas sin conectar, sin colisiones inválidas.

## Regenerar

```powershell
# (Opcional) regenerar arte de props desde imágenes magenta gen_<id>.png:
python tools/tiled_export/regen_props.py --all
# (Opcional) re-texturizar tiles de suelo desde gen_tex_*.png:
python tools/tiled_export/regen_tiles.py --all
# Reconstruir mapa + JSON + validar:
python tools/tiled_export/build_barrio_reference.py
python tools/tiled_export/export_layout.py data/maps/barrio_tutorial_01/barrio_tutorial_01.tmx
cargo run -p map_validator -- data/maps/barrio_tutorial_01
```

## Limitaciones / próximos pasos de arte

- Aún no hay sprites propios para cercos, arbustos, flores, basureros, buzones,
  señales PARE, conos, bicicletas, cajones, neumáticos o herramientas. Se pueden
  generar con `regen_props` + nuevos IDs (agregándolos a `PROP_TILES` y
  `PROP_TARGET_HEIGHT`) y colocar en el `.tmx` sin cambiar el runtime.
