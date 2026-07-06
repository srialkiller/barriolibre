# BEVY_ARCHITECTURE.md
## Carreras de Barrio — Arquitectura Bevy del Estudio

**Versión:** 1.0  
**Owner:** Technical Director · Build Engineer  
**Estado:** **Constitución técnica** — leer antes de escribir Rust  
**Complementa:** [ADR-004](../../decisions/ADR-004-ecs-architecture.md) · [ADR-001](../../decisions/ADR-001-bevy-engine.md) · [ASSET_PIPELINE.md](../production/ASSET_PIPELINE.md)

---

> Este documento **no explica Bevy genérico**. Define **cómo ESTE estudio usa Bevy** — equivalente técnico de [ART_STYLE_GUIDE.md](../art/ART_STYLE_GUIDE.md).

Ningún agente improvisa estructura de carpetas, plugins o convenciones ECS sin cumplirlo.

---

## Tabla de contenidos

1. [Principios](#1-principios)
2. [Estructura del proyecto](#2-estructura-del-proyecto)
3. [Regla Feature = Plugin = Carpeta = Rama](#3-regla-feature--plugin--carpeta--rama)
4. [Plugins](#4-plugins)
5. [Estados del runtime](#5-estados-del-runtime)
6. [Components, Resources, Events](#6-components-resources-events)
7. [Systems](#7-systems)
8. [Asset Registry](#8-asset-registry)
9. [Manifests versionados](#9-manifests-versionados)
10. [Dependencias entre módulos](#10-dependencias-entre-módulos)
11. [Convenciones de nombres](#11-convenciones-de-nombres)
12. [Schedule y plugins de arranque](#12-schedule-y-plugins-de-arranque)
13. [GLOBAL BEVY RULES](#13-global-bevy-rules)

---

## 1. Principios

| # | Principio |
|---|---|
| 1 | **Feature = Plugin = Carpeta = Rama** — un nombre, un dueño |
| 2 | **Plugins pequeños** — nunca `GamePlugin` monolítico |
| 3 | **Assets por ID** — código nunca referencia `player.png` |
| 4 | **Resources con dueño** — cada Resource pertenece a un Plugin |
| 5 | **Comunicación por Events** — prohibidas llamadas directas entre dominios |
| 6 | **Systems ≤ 80 líneas** — dividir si supera |
| 7 | **Data-driven** — balance y contenido en JSON, no hardcoded |
| 8 | **Estados separados** — Boot/Loading/Menu/Gameplay/Pause/Debug nunca mezclados |

---

## 2. Estructura del proyecto

```
barriolibre/
├── Cargo.toml                 ← workspace root
├── rust-toolchain.toml
├── src/
│   ├── main.rs                ← App::new() + plugin registration only
│   │
│   ├── app/
│   │   ├── mod.rs
│   │   └── plugin.rs          ← AppPlugin: registra todos los plugins en orden
│   │
│   ├── core/                  ← Infraestructura compartida (sin gameplay)
│   │   ├── mod.rs
│   │   ├── states.rs          ← GameState enum
│   │   ├── events.rs          ← Event types globales re-export
│   │   ├── resources.rs       ← GameConfig, TimeScale (core-owned)
│   │   ├── schedule.rs        ← SystemSet labels, orden de ejecución
│   │   ├── time.rs
│   │   └── config.rs          ← Load data/config/game.toml
│   │
│   ├── game/                  ← Gameplay domains (1 subfolder = 1 plugin)
│   │   ├── mod.rs
│   │   ├── player/
│   │   ├── vehicle/
│   │   ├── garage/
│   │   ├── inventory/
│   │   ├── race/
│   │   └── clans/             ← alpha, stub OK
│   │
│   ├── world/                   ← Mapa y simulación del barrio
│   │   ├── mod.rs
│   │   ├── map/
│   │   ├── chunks/
│   │   ├── terrain/
│   │   └── poi/
│   │
│   ├── render/                  ← Presentación (sin lógica de juego)
│   │   ├── mod.rs
│   │   ├── camera/
│   │   ├── lighting/
│   │   ├── sprites/
│   │   └── atlas/
│   │
│   ├── assets/                  ← Asset pipeline runtime
│   │   ├── mod.rs
│   │   ├── loader/
│   │   ├── registry/            ← AssetRegistry: ID → Handle
│   │   └── manifest/            ← Parse + verify manifests
│   │
│   ├── ui/
│   │   ├── mod.rs
│   │   ├── hud/
│   │   └── menus/
│   │
│   ├── debug/
│   │   ├── mod.rs
│   │   ├── overlay/             ← F3 overlay
│   │   └── inspector/
│   │
│   ├── save/
│   │   ├── mod.rs
│   │   └── plugin.rs
│   │
│   └── network/                 ← Vacío Sprint 01 — reserved
│       └── mod.rs
│
├── tools/                       ← Workspace members (ver tools/README.md)
├── data/                        ← JSON/TOML data-driven
├── assets/                      ← PNG/audio (nunca referenciados por path en Rust)
├── mods/                        ← User mods (vacío, preparado Sprint 01)
└── features/                    ← Docs del estudio (no código)
```

### Reglas de carpetas

- `main.rs` **solo** construye `App` y registra `AppPlugin`
- Lógica de juego **nunca** en `render/` ni `assets/`
- `core/` **no importa** de `game/` (dependencia unidireccional)
- Cada subcarpeta con plugin tiene: `mod.rs`, `plugin.rs`, `components.rs`, `systems.rs`, `events.rs` (si aplica)

---

## 3. Regla Feature = Plugin = Carpeta = Rama

**Un nombre en los cuatro lugares.**

| Capa | Ejemplo: Inventory |
|---|---|
| Rama Git | `feature/inventory` |
| Docs estudio | `features/inventory/` |
| Código | `src/game/inventory/` |
| Plugin Bevy | `InventoryPlugin` |

```
feature/inventory
       ↓
features/inventory/          ← TASKS, QA, STATUS
       ↓
src/game/inventory/          ← InventoryPlugin
       ↓
agents: economy_designer + technical_director
```

**Prohibido:** `feature/inventory` con código en `src/game/items/` o plugin llamado `ItemsPlugin`.

---

## 4. Plugins

### ✅ Permitido — plugins pequeños por dominio

| Plugin | Módulo | Sprint | Owner Resource |
|---|---|---|---|
| `AppPlugin` | `app/` | 01 | — (orquestador) |
| `CorePlugin` | `core/` | 01 | `GameConfig` |
| `AssetPlugin` | `assets/` | 01 | `AssetRegistry` |
| `MapPlugin` | `world/map/` | 01 | `LoadedNeighborhood` |
| `CameraPlugin` | `render/camera/` | 01 | — |
| `SpritePlugin` | `render/sprites/` | 01 | — |
| `DebugPlugin` | `debug/` | 01 | `DebugOverlayState` |
| `PlayerPlugin` | `game/player/` | 02 | `PlayerInputConfig` |
| `InventoryPlugin` | `game/inventory/` | 02 | `PlayerInventory` |
| `VehiclePlugin` | `game/vehicle/` | 03 | `PartsCatalog` |
| `GaragePlugin` | `game/garage/` | 03 | — |
| `RacePlugin` | `game/race/` | 03 | `ActiveRace` |
| `MenuPlugin` | `ui/menus/` | 01 stub | — |
| `SavePlugin` | `save/` | 04 | `SaveManager` |
| `ClansPlugin` | `game/clans/` | alpha | `ClanRegistry` |

### ❌ Prohibido

```rust
// NUNCA
pub struct GamePlugin;      // monolito
pub struct GameplayPlugin;  // demasiado amplio
pub struct UtilsPlugin;     // cajón de sastre
```

### Anatomía de un plugin

```rust
// src/game/inventory/plugin.rs
pub struct InventoryPlugin;

impl Plugin for InventoryPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<PlayerInventory>()
            .add_event::<PickupCollected>()
            .add_systems(Update, (
                collect_pickup_system,
                sync_inventory_ui_system,
            ).run_if(in_state(GameState::Gameplay)));
    }
}
```

---

## 5. Estados del runtime

```rust
#[derive(States, Clone, Eq, PartialEq, Debug, Hash, Default)]
pub enum GameState {
    #[default]
    Boot,       // Init mínimo, registrar plugins
    Loading,    // Cargar assets + map JSON
    MainMenu,   // Menú (stub OK Sprint 01)
    Gameplay,   // Barrio activo
    Paused,     // Pausa in-game
    Debug,      // Overlay F3, dev only
}
```

### Reglas de estados

| Regla | Descripción |
|---|---|
| **BA-STATE-01** | Un system declara `run_if(in_state(...))` — nunca asume estado |
| **BA-STATE-02** | Transiciones solo vía `NextState<GameState>` en systems dedicados |
| **BA-STATE-03** | `Loading` → carga assets + map; emite `AssetsReady` event |
| **BA-STATE-04** | `Debug` overlay no muta gameplay state |
| **BA-STATE-05** | Sprint 01: Boot → Loading → Gameplay (MainMenu stub) |

### Flujo Sprint 01

```
Boot → Loading (manifest + map) → MainMenu (press Enter) → Gameplay (render barrio)
```

---

## 6. Components, Resources, Events

### Components

- Datos **por entidad** — sin lógica
- Nombre: sustantivo (`Pickup`, `VehicleAssembly`, `Checkpoint`)
- Viven en el módulo del dominio dueño

### Resources — todo recurso tiene dueño

| Resource | Owner Plugin | ❌ Huérfano |
|---|---|---|
| `GameConfig` | CorePlugin | — |
| `AssetRegistry` | AssetPlugin | — |
| `PlayerInventory` | InventoryPlugin | ✓ |
| `LoadedNeighborhood` | MapPlugin | ✓ |
| `PartsCatalog` | VehiclePlugin | ✓ |

**Regla BA-RES-01:** `app.init_resource::<T>()` solo dentro del plugin dueño.

**Regla BA-RES-02:** Prohibido `PlayerInventory` en `GaragePlugin` — Garage **lee** vía Query/Event, no posee el Resource.

### Events — prohibidas llamadas directas

```
Player recoge basura
    ↓  (collision / interaction system)
PickupCollected { material_id, quantity }
    ↓
InventoryPlugin     → actualiza PlayerInventory
    ↓
MaterialAdded       → (re-emitted si otros necesitan)
    ↓
AudioPlugin         → SFX
UIPlugin            → HUD update
```

**Regla BA-EVT-01:** Plugin A **nunca** llama función de Plugin B directamente.

**Regla BA-EVT-02:** Comunicación cross-domain = Events o Resources read-only en schedule ordenado.

### Eventos core (Sprint 01+)

```rust
// core/events.rs — re-exports
pub struct AssetsReady;
pub struct NeighborhoodLoaded { pub map_id: String };
pub struct GameStateChanged { pub from: GameState, pub to: GameState };

// game/inventory/events.rs
pub struct PickupCollected { pub material_id: MaterialId, pub amount: u32 };
pub struct MaterialAdded { pub material_id: MaterialId, pub new_total: u32 };
```

---

## 7. Systems

### Límites

| Regla | Valor |
|---|---|
| **BA-SYS-01** | Máximo **80 líneas** por system fn |
| **BA-SYS-02** | Un system = una responsabilidad |
| **BA-SYS-03** | Nombre: `{verbo}_{dominio}_system` — `collect_pickup_system` |
| **BA-SYS-04** | Side effects vía `EventWriter`, no globals mutables |

### Si supera 80 líneas

```
collect_pickup_system (120 líneas)
    ↓ dividir
detect_pickup_overlap_system   (30)
emit_pickup_event_system       (25)
despawn_collected_system       (20)
```

### SystemSets (schedule.rs)

```rust
#[derive(SystemSet, Debug, Hash, PartialEq, Eq, Clone)]
pub enum GameSet {
    Input,
    Movement,
    Interaction,
    Simulation,
    RenderPrep,
    UI,
}
```

Orden: `Input → Movement → Interaction → Simulation → RenderPrep → UI`

---

## 8. Asset Registry

**El código nunca conoce PNG. Solo conoce IDs.**

```
AssetRegistry
    ↓
Handle<IsoTileSprite>  /  AssetId("road_straight_h_01")
    ↓
Manifest entry
    ↓
assets/environment/roads/road_straight_h_01.png
```

### AssetRegistry API (conceptual)

```rust
#[derive(Resource)]
pub struct AssetRegistry {
    tiles: HashMap<TileId, Handle<Image>>,
    // future: props, vehicles, sfx
}

impl AssetRegistry {
    pub fn tile(&self, id: &TileId) -> Option<&Handle<Image>>;
    pub fn register_tile(&mut self, id: TileId, handle: Handle<Image>);
}
```

### Reglas

| ID | Regla |
|---|---|
| **BA-AST-01** | Rust usa `TileId`, `MaterialId`, `PartId` — newtypes sobre `String` o `SmolStr` |
| **BA-AST-02** | Load path resuelto en `AssetPlugin` desde manifest, no en game systems |
| **BA-AST-03** | Missing asset = log error + placeholder, no panic en release |
| **BA-AST-04** | Hot reload solo en `dev` feature flag |

---

## 9. Manifests versionados

Cada entry en manifest JSON:

```json
{
  "asset_id": "road_straight_h_01",
  "version": 1,
  "hash": "sha256:abc123...",
  "dependencies": [],
  "tags": ["road", "environment", "style_anchor"],
  "origin_pack": "environment_base_pack_01",
  "path": "assets/environment/roads/road_straight_h_01.png"
}
```

| Campo | Propósito |
|---|---|
| `asset_id` | ID canónico — único en todo el proyecto |
| `version` | Incrementar si cambia silueta/pivot |
| `hash` | Integridad CI + hot reload detect |
| `dependencies` | Otros asset_ids requeridos |
| `tags` | Queries, validation, packs |
| `origin_pack` | Trazabilidad producción |

**Verificación en load:** manifest version + hash opcional en dev.

Archivos:
- `data/tilesets/environment_base_pack_01_manifest.json` (extend schema)
- `data/assets/registry.json` (índice global futuro)

---

## 10. Dependencias entre módulos

### Grafo de dependencias (Studio Director usa esto)

```
                    CorePlugin
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         AssetPlugin  MapPlugin  CameraPlugin
              │          │
              └────┬─────┘
                   ▼
              Gameplay state
                   │
         ┌─────────┼─────────┐
         ▼         ▼         ▼
    PlayerPlugin  ...    DebugPlugin
         │
         ▼
   InventoryPlugin
         │
    ┌────┴────┐
    ▼         ▼
VehiclePlugin  Economy (data)
    │
    ▼
GaragePlugin
    │
    ▼
RacePlugin
```

### Matriz feature → prerequisitos

| Feature | Requiere ✅ | Bloqueado sin |
|---|---|---|
| **foundation-runtime** | — | — |
| **player-controller** | Runtime | AssetPlugin, MapPlugin |
| **inventory** | Runtime, Player | PlayerPlugin |
| **vehicle** | Runtime, Inventory (data) | PartsCatalog JSON |
| **garage** | Runtime, Inventory, Vehicle | InventoryPlugin, VehiclePlugin |
| **crafting** | Runtime, Inventory | InventoryPlugin |
| **race** | Runtime, Vehicle, Map | VehiclePlugin, MapPlugin |
| **tutorial** | Runtime, Map | MapPlugin |
| **save** | Runtime, Inventory | SavePlugin deps |
| **ui** (full) | Runtime | MenuPlugin stub OK |
| **clans** | Runtime, Save, Race | alpha |

### Respuesta Studio Director — ejemplo "Crear Garage"

```
Feature: garage
Dependencias:
  ✅ Runtime (foundation-runtime)
  ✅ Inventory
  ✅ Vehicle
  ❌ UI (HUD mínimo OK, no blocker)
  ❌ Save (post-MVP)

Orden recomendado:
  1. foundation-runtime
  2. inventory
  3. vehicle
  4. garage

Branch: feature/garage
Agents: vehicle_designer → game_designer → technical_director → qa
Bloqueado si: InventoryPlugin o VehiclePlugin no merged
```

---

## 11. Convenciones de nombres

| Elemento | Convención | Ejemplo |
|---|---|---|
| Plugin | `{Domain}Plugin` | `InventoryPlugin` |
| Component | sustantivo PascalCase | `VehicleAssembly` |
| Resource | sustantivo + `Resource` opcional | `PlayerInventory` |
| Event | verbo pasado / sustantivo | `PickupCollected` |
| System | `{verb}_{noun}_system` | `load_map_system` |
| ID type | `{Domain}Id` | `TileId`, `MaterialId` |
| Module folder | snake_case = feature name | `inventory/` |
| Rama Git | `feature/{kebab-name}` | `feature/crafting-system` |

---

## 12. Schedule y plugins de arranque

### Orden de registro en AppPlugin (Sprint 01)

```rust
app
    .add_plugins(DefaultPlugins)
    .add_plugins(CorePlugin)
    .add_plugins(AssetPlugin)
    .add_plugins(MapPlugin)
    .add_plugins(CameraPlugin)
    .add_plugins(SpritePlugin)
    .add_plugins(MenuPlugin)      // stub
    .add_plugins(DebugPlugin)
    // Sprint 02+
    // .add_plugins(PlayerPlugin)
    // .add_plugins(InventoryPlugin)
    ;
```

**Regla:** plugins se registran en orden de dependencia — dependiente después de dependencia.

---

## 13. GLOBAL BEVY RULES

| ID | Regla |
|---|---|
| **BA-001** | Leer BEVY_ARCHITECTURE antes de escribir Rust |
| **BA-002** | Feature = Plugin = Carpeta = Rama — mismo nombre |
| **BA-003** | No plugins monolíticos (GamePlugin prohibido) |
| **BA-004** | Assets por ID vía AssetRegistry — no paths PNG en game code |
| **BA-005** | Todo Resource tiene plugin dueño |
| **BA-006** | Cross-domain = Events, no function calls |
| **BA-007** | Systems ≤ 80 líneas |
| **BA-008** | GameState separados — run_if obligatorio |
| **BA-009** | Manifest entries con asset_id + version + origin_pack |
| **BA-010** | Studio Director verifica dependencias §10 antes de asignar sprint |
| **BA-011** | Conflicto con ADR-004 → ADR manda; actualizar este doc |

---

## Precedencia

```
GAME_IDENTITY  >  BEVY_ARCHITECTURE  >  ADR-004  >  feature/ecs.md  >  prompt
```

---

## Referencias

- [features/foundation-runtime/ecs.md](../../features/foundation-runtime/ecs.md)
- [GITFLOW_GUIDE.md](../production/GITFLOW_GUIDE.md)
- [agents/technical_director.md](../../agents/technical_director.md)
- [agents/build_engineer.md](../../agents/build_engineer.md)

---

*Fin de BEVY_ARCHITECTURE.md*
