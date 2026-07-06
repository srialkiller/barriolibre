# GAME_ART_BIBLE.md
## Carreras de Barrio — Biblia de Arte del Juego

**Proyecto:** Carreras de Barrio  
**Motor:** Rust + Bevy Engine (ECS)  
**Perspectiva:** 2.5D — cámara isométrica fija — sprites prerenderizados  
**Pipeline:** Agent Sprite Forge (`generate2dsprite`, `generate2dmap`)  
**Versión:** 1.0  
**Estado:** Documento maestro — **leer primero, siempre**

---

> Este documento es la **constitución artística y técnica** del proyecto. Ningún asset se genera, aprueba o integra sin cumplirlo. Antes de cualquier generación, es **obligatorio** leer los tres documentos de referencia listados abajo. Si una instrucción contradice cualquiera de ellos, **detenerse y preguntar** — no improvisar, no asumir, no romper reglas.

---

## Tabla de contenidos

1. [Jerarquía de documentos](#1-jerarquía-de-documentos)
2. [Protocolo obligatorio pre-generación](#2-protocolo-obligatorio-pre-generación)
3. [Los siete invariantes](#3-los-siete-invariantes)
4. [Pensamiento Bevy ECS](#4-pensamiento-bevy-ecs)
5. [Reutilización y modularidad](#5-reutilización-y-modularidad)
6. [Prohibición de assets aislados](#6-prohibición-de-assets-aislados)
7. [Pensamiento de proyecto completo](#7-pensamiento-de-proyecto-completo)
8. [Resolución de conflictos](#8-resolución-de-conflictos)
9. [Flujo de generación unificado](#9-flujo-de-generación-unificado)
10. [GLOBAL BIBLE RULES](#10-global-bible-rules)

---

## 1. Jerarquía de documentos

```
docs/README.md                 ← Índice por dominio
agents/README.md               ← Estudio virtual (routing)
decisions/                     ← ADRs
lore/                          ← Coherencia del mundo
        │
        ├── docs/game/GAME_IDENTITY.md     ← ADN gameplay
        │
        ├── docs/art/GAME_ART_BIBLE.md     ← ESTE DOCUMENTO
        │
        ├── docs/art/                  ← Equipo ART
        ├── docs/world/                ← Equipo WORLD
        ├── docs/game/                 ← Equipo GAMEPLAY (diseño)
        ├── docs/systems/              ← Equipo GAMEPLAY (sistemas)
        └── docs/production/           ← Pipeline assets
```

| Documento | Pregunta que responde | Equipo |
|---|---|---|
| **GAME_IDENTITY.md** | ¿Por qué existe el juego? ¿Esta idea encaja? | GAMEPLAY |
| **GAME_ART_BIBLE.md** | ¿Puedo generar esto? ¿Cómo encaja visualmente? | ART |
| **ART_STYLE_GUIDE.md** | ¿Cómo se ve visualmente? | ART |
| **VISUAL_LANGUAGE.md** | ¿Qué formas y personalidad? | ART |
| **ASSET_REVIEW_GUIDE.md** | ¿Pasa QA? ¿Score A/B/C/REJECT? | ART |
| **ASSET_PIPELINE.md** | ¿Cómo se nombra e integra? | ART |
| **NEIGHBORHOOD_DESIGN_GUIDE.md** | ¿Cómo se diseña un barrio? | WORLD |
| **GAMEPLAY_GUIDE.md** | ¿Cómo se juega? | GAMEPLAY |
| **RACE_DESIGN_GUIDE.md** | ¿Cómo se diseña una carrera? | GAMEPLAY |
| **VEHICLE_DESIGN_GUIDE.md** | ¿Cómo funciona el vehículo como sistema? | GAMEPLAY |
| **ECONOMY_GUIDE.md** | ¿Cómo fluyen recursos y recompensas? | GAMEPLAY |
| **CLAN_SYSTEM_GUIDE.md** | ¿Cómo funcionan los clanes? | GAMEPLAY |
| **PROGRESSION_GUIDE.md** | ¿Cómo progresa el jugador? | GAMEPLAY |

### 1.1 Regla de precedencia

En caso de duda o solapamiento:

```
GAME_IDENTITY.md   >  GAME_ART_BIBLE.md  >  documento específico  >  prompt  >  criterio agente
```

- **Gameplay / diseño de sistemas** → GAME_IDENTITY manda.
- **Arte / assets** → GAME_ART_BIBLE manda (siempre alineado con identidad).

Si el prompt del usuario contradice un documento → **detenerse y preguntar** (§8).

---

## 2. Protocolo obligatorio pre-generación

> **Ningún asset se genera sin completar los 6 pasos siguientes.**

### Paso 1 — Leer los tres documentos

Antes de escribir un prompt o llamar a `image_gen`, confirmar lectura de:

- [ ] `ART_STYLE_GUIDE.md` — al menos §2 (cámara), §3 (luz), §4 (escala), §9 (GLOBAL ART RULES)
- [ ] `VISUAL_LANGUAGE.md` — al menos §2 (shape language), §5 (70/20/10), §9 (modularidad), §10 (GLOBAL VISUAL RULES)
- [ ] `ASSET_PIPELINE.md` — al menos §2 (nombres), §5 (pivotes), §6 (modularidad), §10 (Bevy)
- [ ] `ASSET_REVIEW_GUIDE.md` — criterios de aprobación y scoring (si se va a integrar)
- [ ] Documento de equipo relevante (`NEIGHBORHOOD_DESIGN`, `VEHICLE_DESIGN`, `RACE_DESIGN`, etc.)

### Paso 2 — Identificar el asset en el sistema

Responder por escrito antes de generar:

| Pregunta | Respuesta obligatoria |
|---|---|
| ¿Qué es este asset? | Categoría + prefijo de nombre |
| ¿Para qué sirve en el juego? | Componente ECS / tile / prop / pieza modular |
| ¿Con qué otros assets se combina? | Lista de dependencias y compatibles |
| ¿Ya existen assets relacionados? | Sí/No — cuáles |
| ¿Es pieza modular o asset compuesto? | Modular / standalone / tile / animación |
| ¿Qué tier/tamaño? | small / medium / large / universal |

### Paso 3 — Verificar invariantes (§3)

Confirmar que el asset respetará los siete invariantes del proyecto.

### Paso 4 — Definir nombre, carpeta y metadatos

Según `ASSET_PIPELINE.md` §2 y §3 — **antes** de generar, no después.

### Paso 5 — Escribir prompt completo

Usar bloque estándar de `ASSET_PIPELINE.md` §8.4 + reglas de los tres documentos.

### Paso 6 — Revisión (Equipo ART)

Aplicar [ASSET_REVIEW_GUIDE.md](./ASSET_REVIEW_GUIDE.md): checklist 10/10 + QUALITY_SCORE. Solo **A** o **B** → integrar.

### Paso 7 — Detectar conflictos (§8)

Si algo del prompt o la solicitud contradice los documentos → **detenerse y preguntar**.

```
┌─────────────────────────────────────────────────────────────┐
│  SI HAY CONFLICTO → NO GENERAR → PREGUNTAR AL USUARIO       │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Los siete invariantes

> Estos siete valores **nunca cambian** entre assets. Son la garantía de coherencia visual y técnica del juego completo.

### Invariante 1 — Cámara

| Propiedad | Valor fijo | Fuente |
|---|---|---|
| Proyección | Isométrica 2:1 (dimetric) | ART_STYLE_GUIDE §2.1 |
| Elevación | 30° | ART_STYLE_GUIDE §2.1 |
| Azimut | 45° NE | ART_STYLE_GUIDE §2.1 |
| Dirección default | SE | ART_STYLE_GUIDE §2.3 |
| Direcciones válidas | `se`, `sw`, `nw`, `ne` | ART_STYLE_GUIDE §2.3 |
| Perspectiva convergente | **Prohibida** | ART_STYLE_GUIDE G-010 |

**Test:** ¿El asset fue pintado como si visto desde la misma cámara virtual fija que todos los demás?

### Invariante 2 — Escala

| Referencia | Valor | Fuente |
|---|---|---|
| Unidad mundo | 1 u = 128 px | ART_STYLE_GUIDE §4 |
| Niño | 1.00 u alto | ART_STYLE_GUIDE §4.1 |
| Vehículo max | 0.85 u alto × 1.50 u ancho | ART_STYLE_GUIDE §4.1 |
| Tile suelo | 256 × 128 px | ART_STYLE_GUIDE §4.3 |
| Tolerancia entre assets del mismo tipo | ±5% | ASSET_PIPELINE §6.1 |

**Test:** ¿Este asset convive en escena con un niño y un vehículo existentes sin verse desproporcionado?

### Invariante 3 — Iluminación

| Propiedad | Valor fijo | Fuente |
|---|---|---|
| Horario | Media mañana (~10:00) | ART_STYLE_GUIDE §3.5 |
| Luz principal | NE, 55° elevación, `#FFF5E6` | ART_STYLE_GUIDE §3.2 |
| Sombras | SW, 35% opacidad, `#3A3A5C` | ART_STYLE_GUIDE §3.4 |
| Luz ambiente | 0.35, `#87CEEB` | ART_STYLE_GUIDE §3.3 |
| Cara SE | Luz plena (base) | ART_STYLE_GUIDE §3.2 |
| Cara SW | −15% | ART_STYLE_GUIDE §3.2 |
| Caras traseras | −25–30% | ART_STYLE_GUIDE §3.2 |

**Test:** ¿Colocado junto a otro asset aprobado, la dirección de luz y sombra coincide?

### Invariante 4 — Lenguaje de formas

| Forma | Uso | Límite |
|---|---|---|
| □ ▭ ▱ | Dominantes | ≥ 60% de silueta |
| ○ ⬭ | Cabezas, ruedas, copas | ≤ 25% |
| △ puntiagudos | **Prohibidos** como dominante | 0% |
| Composición | 70% primary / 20% secondary / 10% detail | VISUAL_LANGUAGE §5 |
| Reciclado | Limpio, funcional, ingenioso | VISUAL_LANGUAGE §8 |

**Test:** ¿Pasa Silhouette Test al 50%? ¿Formas dominantes = cuadrados/rectángulos?

### Invariante 5 — Pivotes

| Categoría | Pivote (X, Y) | Fuente |
|---|---|---|
| Personaje | (0.5, 0.92) | ASSET_PIPELINE §5.2 |
| Vehículo completo | (0.5, 0.88) | ASSET_PIPELINE §5.2 |
| Pieza modular | (0.5, 0.5) | ASSET_PIPELINE §5.2 |
| Rueda | (0.5, 0.75) | ASSET_PIPELINE §5.2 |
| Prop / edificio / árbol | (0.5, 0.90–0.95) | ASSET_PIPELINE §5.2 |
| Tile | (0.5, 0.5) | ASSET_PIPELINE §5.2 |

**Test:** ¿El pivote coincide con la categoría? ¿Documentado en `.meta.json`?

### Invariante 6 — Modularidad

| Regla | Fuente |
|---|---|
| Piezas del mismo tier son intercambiables | ASSET_PIPELINE §6.2 |
| Snap points estándar por chassis | ASSET_PIPELINE §5.3 |
| Misma perspectiva, outline, canvas entre piezas | ASSET_PIPELINE §6.1 |
| Test de combinación antes de aprobar lote | VISUAL_LANGUAGE §9.6 |
| Máximo 1 pieza por snap point | VISUAL_LANGUAGE V-022 |

**Test:** ¿Esta pieza encaja en ≥ 2 chassis del mismo tier sin artefactos > 2 px?

### Invariante 7 — Naming

| Regla | Fuente |
|---|---|
| Formato | `snake_case`, inglés, `_01` numeración | ASSET_PIPELINE §2.1 |
| Prefijo de categoría | `vehicle_`, `wheel_`, `player_`, `road_`, etc. | ASSET_PIPELINE §2.2 |
| Dirección | Sufijo `_se`, `_sw`, `_nw`, `_ne` | ASSET_PIPELINE §2.1 |
| Carpeta = nombre del asset | ASSET_PIPELINE §3.2 |
| Prompt guardado | `<name>.prompt.txt` | ASSET_PIPELINE §2.4 |

**Test:** ¿El nombre sigue la convención? ¿La carpeta existe en la ruta correcta?

---

## 4. Pensamiento Bevy ECS

> Todo asset se diseña como **dato reutilizable** que un sistema ECS consume en runtime. No diseñar "imágenes"; diseñar **componentes del juego**.

### 4.1 Principio ECS-first

```
Asset visual  →  Resource / Component  →  System  →  Pantalla
     ↑                  ↑                    ↑
  PNG + meta.json    Datos tipados       Lógica sin
  en assets/         en Rust/JSON         hardcode de arte
```

Cada asset debe responder:

1. **¿Qué Component lleva?** — `VehiclePart`, `IsoDepth`, `AnimatedSprite`, `TileCollider`
2. **¿Qué Resource referencia?** — `SnapPointRegistry`, `AnimationLibrary`, `TileSetManifest`
3. **¿Qué System lo procesa?** — `y_sort_system`, `vehicle_assembly_system`, `tilemap_render_system`
4. **¿Qué Event lo modifica?** — `PartInstalled`, `VehicleSpawned`, `TileChanged`

### 4.2 Mapeo asset → ECS

| Tipo de asset | Component(s) Bevy | Resource / Data | System |
|---|---|---|---|
| Pieza modular vehículo | `VehiclePart`, `Sprite`, `Transform` | `snap_points.json` | `vehicle_assembly_system` |
| Chassis | `VehicleChassis`, `SnapPoints`, `Sprite` | `.meta.json` del chassis | `vehicle_assembly_system` |
| Personaje animado | `AnimatedSprite`, `IsoDepth`, `CharacterId` | `player_animations.json` | `animation_system`, `y_sort_system` |
| Prop de mapa | `MapProp`, `IsoDepth`, `Sprite`, `Collider` | `<zone>_props.json` | `y_sort_system`, `collision_system` |
| Tile de calle | — (parte de Tilemap) | `road_manifest.json` | `tilemap_system` |
| FX | `ParticleEffect` o `AnimatedSprite` | — | `fx_system` |
| Mapa base | `MapFoundation` (Resource) | — | `map_load_system` |

### 4.3 Reglas ECS para generación de assets

| ID | Regla |
|---|---|
| **E-001** | Todo asset tiene un **`id` string** que coincide con su nombre de archivo. |
| **E-002** | Todo asset modular tiene **`.meta.json`** parseable por Serde en runtime. |
| **E-003** | Snap points son **coordenadas normalizadas** (0.0–1.0), no píxeles. |
| **E-004** | Animaciones se definen en **JSON de data/**, no hardcodeadas en Rust. |
| **E-005** | Props de mapa se posicionan via **placement JSON**, no baked en el mapa base. |
| **E-006** | Colisiones son **shapes independientes** del PNG — metadata, no alpha scan. |
| **E-007** | Y-sort key = posición Z del mundo; pivote del sprite = base del objeto. |
| **E-008** | Un `VehicleAssembly` se construye combinando `InstalledPart` en runtime — no pre-renderizar todas las combinaciones. |

### 4.4 Lo que NO hacer en Bevy

| Prohibido | Alternativa ECS |
|---|---|
| Pre-renderizar cada combinación de vehículo | Ensamblar piezas modulares en runtime via snap points |
| Hardcodear posiciones de props en código | Cargar `<zone>_props.json` |
| Usar alpha del PNG como collision mask | Definir colliders en metadata JSON |
| Un sprite por cada estado del juego | Component states + misma textura/atlas |
| Duplicar assets por dirección en código | `TextureAtlas` + animación direction-aware |

---

## 5. Reutilización y modularidad

### 5.1 Principio de reutilización

> **Un asset generado debe servir en al menos 2 contextos distintos del juego.** Si solo sirve en uno, rediseñar antes de aprobar.

| Contexto | Ejemplo de reutilización |
|---|---|
| Mismo asset, distintos mapas | `prop_trashcan_01` en barrio_norte y barrio_sur |
| Misma pieza, distintos vehículos | `wheel_small_01` en 3 chassis diferentes |
| Mismo tile, distintas conexiones | `road_straight` en 4 orientaciones isométricas |
| Mismo personaje, distintas acciones | `player_*` con idle, walk, race, hurt, celebrate |
| Mismo prop, distintos estados (futuro) | `prop_trashcan_01` normal / volcado (variante `_v2`) |

### 5.2 Árbol de dependencias modular

```
                    ┌─────────────┐
                    │   NIÑO      │
                    │  (player)   │
                    └──────┬──────┘
                           │ conduce
                    ┌──────▼──────┐
                    │  VEHÍCULO   │ ← ensamblado en runtime
                    │ (assembly)  │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │   CHASSIS   │ │   RUEDAS    │ │   MOTOR     │
    │  (1 de N)   │ │  (4× de M)  │ │  (1 de P)   │
    └─────────────┘ └─────────────┘ └─────────────┘
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │  PARACHOQUE │ │   ASIENTO   │ │   ESCAPE    │
    │  VOLANTE    │ │  ACCESORIO  │ │   ...       │
    └─────────────┘ └─────────────┘ └─────────────┘
                           │
                    ┌──────▼──────┐
                    │    MAPA     │
                    │  (barrio)   │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │  TILES      │ │   PROPS     │ │  EDIFICIOS  │
    │  road_*     │ │  prop_*     │ │  house_*    │
    │  sidewalk_* │ │  tree_*     │ │  garage_*   │
    └─────────────┘ └─────────────┘ └─────────────┘
```

### 5.3 Reglas de reutilización

1. **Generar piezas, no productos finales.** Prioridad: chassis → ruedas → motor → resto.
2. **Parametrizar, no duplicar.** Un `wheel_small_01` sirve para cualquier chassis small.
3. **Metadata sobre variantes.** Diferencias de estado (sucio, roto) = variant `_v2`, no asset nuevo con otro nombre.
4. **Atlas por categoría.** Agrupar sprites reutilizables en `assets/atlases/` para batching en Bevy.
5. **Placement data sobre copias.** Un `house_small_01` se instancia N veces via JSON, no se generan N PNGs.

---

## 6. Prohibición de assets aislados

> **Nunca generar un asset que no tenga contexto, conexión y lugar definido en el proyecto.**

### 6.1 Qué es un asset aislado (PROHIBIDO)

| Asset aislado | Por qué está mal | Qué hacer en su lugar |
|---|---|---|
| Un vehículo completo preensamblado sin piezas | No es modular, no reutilizable | Generar chassis + piezas; ensamblar en Bevy |
| Un prop sin categoría ni prefijo | No encaja en pipeline | Definir `prop_<name>_<nn>` y carpeta |
| Un sprite sin dirección isométrica | No funciona en 4 direcciones | Generar al menos `_se`; planificar las 4 |
| Un mapa con props baked | No editable, no reusable | Foundation-only + props separados |
| Una animación sin JSON de definición | No cargable en Bevy | Escribir `data/characters/*.json` |
| Una pieza sin snap points | No combinable | Definir `.meta.json` con snaps |
| Un tile sin manifest de conexiones | No tileable | Registrar en `data/tilesets/*_manifest.json` |
| Un personaje sin escala relativa al niño | Rompe invariante 2 | Verificar contra referencia 1.0 u |

### 6.2 Contexto mínimo obligatorio

Todo asset debe declarar antes de generarse:

```yaml
asset_id: wheel_small_01
category: wheel
tier: small
part_of: vehicle_modular_system
combines_with:
  - vehicle_chassis_small_01
  - vehicle_chassis_small_02
used_in:
  - vehicle_assembly_screen
  - race_gameplay
  - garage_scene
bevy_component: VehiclePart
bevy_resource: snap_points.json
data_file: assets/sprites/vehicle/wheels/wheel_small_01/wheel_small_01.meta.json
folder: assets/sprites/vehicle/wheels/wheel_small_01/
depends_on: []          # assets que deben existir antes
blocks:                 # assets que dependen de este
  - vehicle_assembly_qc
```

### 6.3 Test de aislamiento

Antes de aprobar, responder:

- [ ] ¿Este asset tiene **al menos 1 padre** lógico en el árbol de dependencias?
- [ ] ¿Este asset tiene **al menos 1 hijo o consumidor** definido?
- [ ] ¿Existe **`.meta.json`** o placement JSON que lo conecta al runtime?
- [ ] ¿Se puede **instanciar más de una vez** en el juego?
- [ ] ¿Alguien del equipo (o un system ECS) **sabe cargarlo** sin preguntar?

Si alguna respuesta es "no" → **no aprobar**.

---

## 7. Pensamiento de proyecto completo

### 7.1 Principio

> Cada asset es un **ladrillo del barrio**, no un póster. Debe encajar con lo existente, lo futuro y el motor.

### 7.2 Las 5 preguntas de proyecto completo

Antes de generar, responder:

| # | Pregunta | Ejemplo de mala respuesta | Ejemplo de buena respuesta |
|---|---|---|---|
| 1 | **¿Qué hay already?** | "No sé qué chassis existen" | "Existen chassis_small_01 y _02; esta rueda debe encajar en ambos" |
| 2 | **¿Qué viene después?** | "Solo necesito este sprite" | "Después vendrán 8 ruedas más; este define el tier small" |
| 3 | **¿Cómo se ve en contexto?** | "Se ve bien solo" | "Se ve bien junto a un niño, un chassis y un tile de calle" |
| 4 | **¿Cómo lo carga Bevy?** | "Pongo el PNG en assets/" | "Component VehiclePart + meta.json + snap_points.json" |
| 5 | **¿Cuántas veces se usa?** | "Una vez en un mapa" | "En assembly, en race, en garage; instanciable N veces" |

### 7.3 Orden de producción del proyecto

```
FASE 0 — Documentación (COMPLETADA)
  ART_STYLE_GUIDE, VISUAL_LANGUAGE, ASSET_PIPELINE, GAME_ART_BIBLE

FASE 1 — Fundamentos
  Tiles de calle (road_*) → tilesets → tilemap Bevy
  Tiles de vereda, pasto

FASE 2 — Piezas modulares de vehículo
  Chassis (3 tiers) → ruedas → motores → resto de piezas
  Validación de combinación → snap_points.json

FASE 3 — Personajes
  Player (idle, walk, race) × 4 direcciones
  NPCs rivales

FASE 4 — Entorno
  Mapa base (foundation-only) → dressed reference → props
  Casas, garajes, árboles, props de calle

FASE 5 — Ensamblaje e integración
  Atlases, animaciones JSON, vehicle assembly en Bevy
  QA de escena completa
```

**Regla:** no saltar fases. No generar personajes (Fase 3) antes de tener escala definida con tiles (Fase 1) y piezas modulares (Fase 2).

### 7.4 Escena de validación global

Todo lote de assets nuevos se valida en una **escena de referencia** antes de aprobar:

```
Escena: validation_scene
Contiene:
  - 1 tile de calle (road_straight)
  - 1 tile de vereda
  - 1 niño (player_idle_se) de referencia
  - 1 chassis de referencia (vehicle_chassis_small_01)
  - 1 vehículo ensamblado (chassis + 4 ruedas + motor + asiento)
  - 1 casa (house_small_01)
  - 1 árbol (tree_medium_01)
  - 1 prop (prop_trashcan_01)
  - Iluminación: media mañana (invariante 3)
  - Cámara: isométrica fija (invariante 1)

Test: colocar el asset nuevo en esta escena.
  ✓ ¿Escala coherente?
  ✓ ¿Luz coherente?
  ✓ ¿Formas coherente?
  ✓ ¿Pivote correcto en suelo?
  ✓ ¿No rompe la estética del barrio?
```

---

## 8. Resolución de conflictos

### 8.1 Protocolo de stop-and-ask

```
┌──────────────────────────────────────────────────────────────┐
│                    DETECCIÓN DE CONFLICTO                     │
│                                                              │
│  Prompt / solicitud del usuario                              │
│         ↓                                                    │
│  ¿Contradice ART_STYLE_GUIDE?  ──SÍ──→  DETENER + PREGUNTAR  │
│         ↓ NO                                                 │
│  ¿Contradice VISUAL_LANGUAGE?  ──SÍ──→  DETENER + PREGUNTAR  │
│         ↓ NO                                                 │
│  ¿Contradice ASSET_PIPELINE?   ──SÍ──→  DETENER + PREGUNTAR  │
│         ↓ NO                                                 │
│  ¿Contradice GAME_ART_BIBLE?   ──SÍ──→  DETENER + PREGUNTAR  │
│         ↓ NO                                                 │
│  ¿Contradice otro asset existente? ──SÍ──→ DETENER + PREGUNTAR│
│         ↓ NO                                                 │
│  ✅ PROCEDER CON GENERACIÓN                                    │
└──────────────────────────────────────────────────────────────┘
```

### 8.2 Ejemplos de conflictos que requieren preguntar

| Solicitud | Conflicto con | Acción |
|---|---|---|
| "Genera un vehículo estilo pixel art" | ART_STYLE_GUIDE G-002 | Preguntar: ¿excepción documentada? |
| "Haz un auto con forma aerodinámica puntiaguda" | VISUAL_LANGUAGE V-003 | Preguntar: ¿variante especial? |
| "Pon la casa dentro del mapa base" | ASSET_PIPELINE §9.5 foundation-only | Preguntar: ¿baked scene mode? |
| "Genera solo un PNG sin meta.json" | ASSET_PIPELINE §11, GAME_ART_BIBLE E-002 | Preguntar: ¿placeholder temporal? |
| "Iluminación de atardecer" | ART_STYLE_GUIDE §3.5 | Preguntar: ¿variante de mapa o postproceso? |
| "Nombre: CarroRojo.png" | ASSET_PIPELINE §2.1 snake_case | Corregir o preguntar |
| "Un vehículo completo preensamblado" | GAME_ART_BIBLE §6 | Preguntar: ¿solo para marketing/reference? |
| "Triángulos en la carrocería" | VISUAL_LANGUAGE §2.3 | Preguntar: ¿detalle < 3% o rediseño? |

### 8.3 Formato de pregunta al detectar conflicto

```markdown
⚠️ CONFLICTO DETECTADO — no genero hasta resolver.

**Solicitud:** [lo que pidió el usuario]
**Conflicto con:** [documento + sección/regla]
**Regla:** [texto de la regla]
**Opciones:**
  A) Ajustar la solicitud para cumplir la regla
  B) Crear excepción documentada (requiere actualizar el documento)
  C) Cancelar la generación

¿Cómo procedemos?
```

### 8.4 Excepciones

Las excepciones a las reglas **solo son válidas** si:

1. El usuario las aprueba explícitamente.
2. Se documentan en el CHANGELOG del documento afectado.
3. Se incrementa la versión del documento (ej. 1.0 → 1.1).
4. No rompen los siete invariantes (§3) — los invariantes **no tienen excepción**.

---

## 9. Flujo de generación unificado

### 9.1 Diagrama completo

```
 SOLICITUD
     │
     ▼
 ┌─────────┐    NO    ┌──────────────┐
 │ ¿Leí los │────────→│ LEER docs    │
 │ 3 docs?  │         │ obligatorios │
 └────┬─────┘         └──────────────┘
      │ SÍ
      ▼
 ┌─────────┐    SÍ    ┌──────────────┐
 │¿Conflicto│────────→│ STOP +       │
 │ detectado│         │ PREGUNTAR    │
 └────┬─────┘         └──────────────┘
      │ NO
      ▼
 ┌─────────┐
 │ Definir │
 │ contexto│  (§6.2: id, category, combines_with, bevy_component)
 └────┬─────┘
      ▼
 ┌─────────┐
 │ Definir │
 │ nombre +│  (ASSET_PIPELINE §2, §3)
 │ carpeta │
 └────┬─────┘
      ▼
 ┌─────────┐
 │ Escribir│  (bloque §8.4 ASSET_PIPELINE + reglas 3 docs)
 │ prompt  │
 └────┬─────┘
      ▼
 ┌─────────┐
 │Generar  │  (generate2dsprite / generate2dmap)
 │ image   │
 └────┬─────┘
      ▼
 ┌─────────┐
 │Postpro- │  (chroma-key, extract, QC)
 │cesar    │
 └────┬─────┘
      ▼
 ┌─────────┐    NO    ┌──────────────┐
 │ ¿Pasa   │────────→│ REGENERAR o  │
 │QC +     │         │ REPROCESAR   │
 │invariant│         └──────────────┘
 │es?      │
 └────┬─────┘
      │ SÍ
      ▼
 ┌─────────┐
 │ Escribir│  (.meta.json, placement JSON, animation JSON)
 │metadata │
 └────┬─────┘
      ▼
 ┌─────────┐    NO    ┌──────────────┐
 │ ¿Pasa   │────────→│ REGENERAR    │
 │ escena  │         │ con contexto │
 │validación│        └──────────────┘
 └────┬─────┘
      │ SÍ
      ▼
 ┌─────────┐
 │ Marcar  │  (status: qc_pass → integrated)
 │aprobado │
 └─────────┘
```

### 9.2 Bloque de prompt maestro

Copiar al inicio de **todo** prompt de generación:

```
=== CARRERAS DE BARRIO — GAME ART BIBLE v1.0 ===
Read and comply with: ART_STYLE_GUIDE.md, VISUAL_LANGUAGE.md, ASSET_PIPELINE.md

INVARIANTS (never break):
- Camera: isometric 2:1, 30° elevation, 45° azimuth NE, direction SE
- Scale: 1u = 128px, child = 1.0u reference
- Lighting: mid-morning, NE sun #FFF5E6, SW shadows 35% #3A3A5C
- Shapes: squares/rectangles/trapezoids dominant; 70/20/10 composition
- Pivot: per ASSET_PIPELINE §5.2 for this category
- Modular: must combine with existing pieces of same tier
- Naming: snake_case per ASSET_PIPELINE §2

DESIGN: clean HD cartoon, Latin American neighborhood, recycled = clean/functional/ingenious
ECS: asset is a reusable Bevy component, not an isolated image
Background: solid #FF00FF (sprites) / opaque (maps)
No pixel art, no photorealism, no readable text, no violence, no pointy triangles

ASSET: <id>
CATEGORY: <category>
TIER: <small|medium|large|universal>
COMBINES_WITH: <list>
BEVY_COMPONENT: <component name>
```

### 9.3 Herramientas por tipo

| Tipo | Skill | Parámetros clave |
|---|---|---|
| Personajes, piezas, props, FX | `generate2dsprite` | `art_style: project-native`, `view: 3/4`, `anchor: feet` |
| Mapas, tilesets, terreno | `generate2dmap` | `map_mode: tile_mode/scene_mode`, `perspective: isometric-like` |
| Prop packs compactos | `generate2dsprite` | `prop_pack_3x3` solo para compact_prop |
| Tiles de calle | `generate2dmap` o `generate2dsprite` | 256×128, manifest de conexiones |

---

## 10. GLOBAL BIBLE RULES

> Reglas maestras. Prevalecen sobre instrucciones sueltas. Complementan (no reemplazan) las reglas de los otros tres documentos.

### 10.1 Lectura obligatoria

| ID | Regla |
|---|---|
| **B-001** | Antes de generar **cualquier** asset, leer `ART_STYLE_GUIDE.md`, `VISUAL_LANGUAGE.md` y `ASSET_PIPELINE.md`. |
| **B-002** | Si el prompt contradice cualquier documento → **detenerse y preguntar**. No improvisar. |
| **B-003** | Los siete invariantes (§3) **no tienen excepción**. |

### 10.2 Coherencia

| ID | Regla |
|---|---|
| **B-004** | Toda generación mantiene: **misma cámara, escala, iluminación, formas, pivotes, modularidad, naming**. |
| **B-005** | Todo asset se valida en **escena de referencia** (§7.4) antes de aprobar. |
| **B-006** | Todo asset nuevo debe ser **visualmente coherente** con los assets ya aprobados. |

### 10.3 ECS y reutilización

| ID | Regla |
|---|---|
| **B-007** | Toda generación piensa en **Bevy ECS**: Component + Resource + System. |
| **B-008** | Todo asset debe ser **reutilizable** en ≥ 2 contextos (§5.1). |
| **B-009** | **Nunca generar assets aislados** (§6). Todo asset tiene contexto, metadata y consumidor. |
| **B-010** | **Siempre pensar en el proyecto completo** (§7). Responder las 5 preguntas. |

### 10.4 Producción

| ID | Regla |
|---|---|
| **B-011** | Respetar **orden de fases** (§7.3). No saltar fases. |
| **B-012** | Generar **piezas modulares** antes que productos compuestos. |
| **B-013** | Mapas = **foundation-only**. Props siempre separados. |
| **B-014** | Guardar **prompt + meta.json + placement JSON** junto a cada asset. |
| **B-015** | No aprobar asset sin pasar **checklist de entrega** (ASSET_PIPELINE §12). |

### 10.5 Bloque final obligatorio en todo prompt

```
GLOBAL BIBLE RULES (Carreras de Barrio v1.0):
- Comply with ART_STYLE_GUIDE + VISUAL_LANGUAGE + ASSET_PIPELINE
- Seven invariants: camera, scale, lighting, shapes, pivots, modularity, naming
- Bevy ECS: reusable component with metadata, not isolated image
- Recycled = clean, functional, ingenious — kid built this
- If conflict with docs → STOP and ASK
```

---

## Apéndice A — Checklist rápida pre-generación

```
□ Leí ART_STYLE_GUIDE.md (cámara, luz, escala, reglas)
□ Leí VISUAL_LANGUAGE.md (formas, composición, modularidad)
□ Leí ASSET_PIPELINE.md (nombres, pivotes, Bevy)
□ Identifiqué categoría, tier, prefijo de nombre
□ Definí con qué assets se combina
□ Definí Component/Resource/System Bevy
□ Verifiqué que no hay conflicto con los documentos
□ Verifiqué que no hay conflicto con assets existentes
□ Escribí prompt con bloque maestro §9.2
□ Planifiqué meta.json y data JSON
□ Sé en qué fase de producción estoy (§7.3)
□ Tengo escena de validación para post-QC
```

## Apéndice B — Índice cruzado de reglas

| Tema | ART_STYLE_GUIDE | VISUAL_LANGUAGE | ASSET_PIPELINE | GAME_ART_BIBLE |
|---|---|---|---|---|
| Cámara | §2 | — | — | Invariante 1, B-004 |
| Iluminación | §3 | — | — | Invariante 3, B-004 |
| Escala | §4 | §4 | §4 | Invariante 2, B-004 |
| Paleta / materiales | §5–6 | — | — | vía ART_STYLE |
| Shape language | — | §2 | — | Invariante 4, B-004 |
| Composición 70/20/10 | — | §5 | — | Invariante 4 |
| Reciclado creativo | §1, G-025 | §8 | — | B-009 |
| Siluetas | — | §3 | — | vía VISUAL |
| Naming | — | — | §2 | Invariante 7, B-004 |
| Pivotes | G-038 | — | §5 | Invariante 5, B-004 |
| Modularidad | — | §9 | §6 | Invariante 6, B-008 |
| Bevy ECS | §8.3 | — | §10 | §4, B-007 |
| Foundation-only | G-036 | — | §9.5 | B-013 |
| GLOBAL RULES | §9 (G-001–040) | §10 (V-001–026) | §12 | §10 (B-001–015) |

## Apéndice C — Historial de versiones

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-07-05 | Documento inicial — constitución del proyecto, invariantes, ECS, anti-aislamiento |

---

*Fin de GAME_ART_BIBLE.md*
