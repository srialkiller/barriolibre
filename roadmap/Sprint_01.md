# Sprint 01 — Foundation Runtime

**Generated:** 2026-07-06 by Studio Director  
**Release branch:** `release/vertical-slice`  
**Feature branch:** `feature/bevy-foundation-runtime`  
**Regla del estudio:** Todo sprint termina con `cargo run` mostrando **avance visible**.

---

## Objetivo

> **No es crear un Cargo.toml.**  
> Es construir el **runtime** sobre el que vivirá el juego.

### Resultado esperado

```bash
cargo run
```

→ Ventana Bevy con **primer barrio renderizado** (tiles isométricos).  
Gameplay opcional en Sprint 01 — **el runtime es obligatorio**.

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
- [ ] Proyecto Bevy inicializado (workspace)
- [ ] Compila sin warnings críticos
- [ ] CI local: `cargo fmt`, `cargo clippy`, `cargo test` — Build Engineer

### ECS
- [ ] Estados: `Boot`, `Loading`, `MainMenu`, `Gameplay`
- [ ] Plugins separados por dominio
- [ ] Resources globales (`GameConfig`, etc.)
- [ ] Event bus inicial

### Assets
- [ ] `AssetManager` / loader unificado
- [ ] Carga automática ENVIRONMENT_BASE_PACK_01
- [ ] Verificación vs manifest JSON
- [ ] Hot reload activo (dev)

### Render
- [ ] Cámara isométrica 2:1 (ADR-002)
- [ ] Primer mapa desde JSON
- [ ] Tiles renderizados correctamente

### Mundo
- [ ] `layout.json` leído
- [ ] `collision.json` preparado (no usado aún OK)
- [ ] `scene_hooks.json` cargado

### Herramientas
- [ ] Logging (tracing)
- [ ] Configuración (`config/` o `data/config/`)
- [ ] Carpeta `mods/` preparada (vacía OK)
- [ ] Debug overlay F3 — Tools Engineer

### QA
- [ ] `cargo test` pasa
- [ ] `cargo clippy` sin errores
- [ ] FPS estable en mapa test
- [ ] Assets cargados sin errores en log

### Visible (regla del estudio)
- [ ] **`cargo run` → barrio visible en pantalla**

---

## Tasks

| ID | Task | Agent | Done |
|---|---|---|---|
| S1-BE-001 | Cargo workspace + Bevy pin | build_engineer | [ ] |
| S1-BE-002 | CI script fmt/clippy/test | build_engineer | [ ] |
| S1-TD-001 | App + GameState machine | technical_director | [ ] |
| S1-TD-002 | Plugins: core, assets, render, world | technical_director | [ ] |
| S1-TD-003 | AssetManager + manifest verify | technical_director | [ ] |
| S1-TD-004 | Hot reload dev | technical_director | [ ] |
| S1-TD-005 | Isometric camera + tilemap render | technical_director | [ ] |
| S1-TD-006 | Load layout.json + scene_hooks | technical_director | [ ] |
| S1-TD-007 | collision.json loader (stub use) | technical_director | [ ] |
| S1-TD-008 | Logging + GameConfig | technical_director | [ ] |
| S1-TD-009 | mods/ folder + placeholder | technical_director | [ ] |
| S1-TE-001 | map_validator stub | tools_engineer | [ ] |
| S1-TE-002 | debug_overlay F3 | tools_engineer | [ ] |
| S1-WD-001 | data/maps/barrio_tutorial_01/ JSON | world_designer | [ ] |
| S1-QA-001 | DoD checklist completo | qa_director | [ ] |

Ver detalle: [features/foundation-runtime/TASKS.md](../features/foundation-runtime/TASKS.md)

---

## Agent chain

```
Studio Director
    ↓
Release Manager → feature/bevy-foundation-runtime
    ↓
Build Engineer (Cargo + CI)
    ↓
World Designer (map JSON)
    ↓
Technical Director (runtime)
    ↓
Tools Engineer (validators + F3)
    ↓
QA Director (DoD)
    ↓
Release Manager (merge → develop)
    ↓
Studio Director (metrics + studio_health)
```

---

## Sprint exit

- [ ] DoD 100% ✅
- [ ] `metrics/studio_health.json` → Runtime 🟢
- [ ] Demo: `cargo run` barrio renderizado
- [ ] POL-001–007

---

## Siguiente

**Sprint 02 — Player & Exploration:** `feature/player-controller` + `feature/inventory`  
Debe acercar al [Vertical Slice 15 min](./MVP.md).
