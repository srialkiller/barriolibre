# Sprint 01 — Foundation Runtime

**Status:** ✅ **COMPLETE** — merged 2026-07-09  
**Milestone:** [M0 — Foundation Runtime](../milestones/MILESTONE_0_FOUNDATION_RUNTIME.md)

---

## Pre-requisito (gate)

- [x] **`docs/systems/BEVY_ARCHITECTURE.md`** — constitución técnica ✅
- [x] Release Manager abre `feature/bevy-foundation-runtime`

---

## Objetivo

> **No es crear un Cargo.toml.**  
> Es construir el **runtime** sobre el que vivirá el juego.

### Resultado esperado (Milestone 0)

```bash
cargo run
```

| # | Visible |
|---|---|
| 1 | Ventana Bevy |
| 2 | Cámara isométrica 2:1 |
| 3 | Barrio desde `layout.json` |
| 4 | Tiles ENVIRONMENT_BASE_PACK_01 |
| 5 | F3 overlay: FPS, GameState, assets count |
| 6 | Mensaje: *Foundation Runtime operativo* |

Gameplay/jugador **no requerido** en M0.

---

## Misión (Technical Director)

> *"Construir la infraestructura mínima para que el primer barrio pueda cargarse, renderizarse y servir de base al Vertical Slice."*

**Colaboradores:** Build Engineer (CI/Cargo) · Tools Engineer (validators, F3) · QA Director

---

## Pre-flight (Release Manager)

```
1. @agents/studio_director.md Iniciar Sprint 01 — Foundation Runtime
2. @agents/release_manager.md
     - develop + release/vertical-slice (si no existen)
     - git switch -c feature/bevy-foundation-runtime develop
     - registry.json + features/foundation-runtime/STATUS.md → Draft
```

---

## Definition of Done (Sprint NO termina hasta ✅ todo)

### Proyecto
- [x] Proyecto Bevy inicializado (workspace)
- [x] Compila sin warnings críticos
- [x] CI local: `cargo fmt`, `cargo clippy`, `cargo test` — Build Engineer

### ECS
- [x] Estados: `Boot`, `Loading`, `MainMenu`, `Gameplay`
- [x] Plugins separados por dominio
- [x] Resources globales (`GameConfig`, etc.)
- [x] Event bus inicial

### Assets
- [x] `AssetManager` / loader unificado
- [x] Carga automática ENVIRONMENT_BASE_PACK_01
- [x] Verificación vs manifest JSON
- [x] Hot reload activo (dev)

### Render
- [x] Cámara isométrica 2:1 (ADR-002)
- [x] Primer mapa desde JSON
- [x] Tiles renderizados correctamente

### Mundo
- [x] `layout.json` leído
- [x] `collision.json` preparado (no usado aún OK)
- [x] `scene_hooks.json` cargado

### Herramientas
- [x] Logging (tracing)
- [x] Configuración (`config/` o `data/config/`)
- [x] Carpeta `mods/` preparada (vacía OK)
- [x] Debug overlay F3 — Tools Engineer

### QA
- [x] `cargo test` pasa
- [x] `cargo clippy` sin errores
- [x] FPS estable en mapa test
- [x] Assets cargados sin errores en log

### Visible (regla del estudio)
- [x] **`cargo run` → barrio visible en pantalla**

---

## Tasks

| ID | Task | Agent | Done |
|---|---|---|---|
| S1-BE-001 | Cargo workspace + Bevy pin | build_engineer | [x] |
| S1-BE-002 | CI script fmt/clippy/test | build_engineer | [x] |
| S1-TD-001 | App + GameState machine | technical_director | [x] |
| S1-TD-002 | Plugins: core, assets, render, world | technical_director | [x] |
| S1-TD-003 | AssetManager + manifest verify | technical_director | [x] |
| S1-TD-004 | Hot reload dev | technical_director | [x] |
| S1-TD-005 | Isometric camera + tilemap render | technical_director | [x] |
| S1-TD-006 | Load layout.json + scene_hooks | technical_director | [x] |
| S1-TD-007 | collision.json loader (stub use) | technical_director | [x] |
| S1-TD-008 | Logging + GameConfig | technical_director | [x] |
| S1-TD-009 | mods/ folder + placeholder | technical_director | [x] |
| S1-TE-001 | map_validator stub | tools_engineer | [x] |
| S1-TE-002 | debug_overlay F3 | tools_engineer | [x] |
| S1-WD-001 | data/maps/barrio_tutorial_01/ JSON | world_designer | [x] |
| S1-QA-001 | DoD checklist completo | qa_director | [x] |

Ver detalle: [features/foundation-runtime/TASKS.md](../features/foundation-runtime/TASKS.md)

---

## Agent chain

```
Studio Director
    ↓
BEVY_ARCHITECTURE.md ✅ (gate passed)
    ↓
Release Manager → feature/bevy-foundation-runtime
    ↓
Build Engineer (Cargo workspace §2)
    ↓
Technical Director (runtime per architecture)
    ↓
Tools Engineer (validators + F3)
    ↓
World Designer (map JSON)
    ↓
QA Director (DoD)
    ↓
Release Manager (merge → develop)
```

---

## Sprint exit

- [x] DoD 100% ✅
- [x] `metrics/studio_health.json` → Runtime 🟢
- [x] Demo: `cargo run` barrio renderizado
- [x] POL-001–007

---

## Siguiente

**Sprint 02 — Player & Exploration:** `feature/player-controller` + `feature/inventory`  
Debe acercar al [Vertical Slice 15 min](./MVP.md).
