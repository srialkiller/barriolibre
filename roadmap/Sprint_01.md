# Sprint 01 — Bevy Scaffold + Environment Loader

**Generated:** 2026-07-06 by Studio Director  
**Release branch:** `release/vertical-slice`  
**Status:** ⏸ **NO INICIAR** hasta GitFlow integrado ✅

---

## Pre-flight (Release Manager)

Antes de cualquier código:

```
1. @agents/studio_director.md Iniciar Sprint 01
2. @agents/release_manager.md
     - Crear develop desde main (si no existe)
     - Crear release/vertical-slice desde develop
     - Crear feature/bevy-scaffold
     - Registrar en production/branches/registry.json
     - features/bevy-scaffold/STATUS.md → Draft
3. git switch feature/bevy-scaffold
```

Ver [GITFLOW_GUIDE](../docs/production/GITFLOW_GUIDE.md).

---

## Feature branches (Sprint 01)

| Branch | Feature folder | Owner |
|---|---|---|
| `feature/bevy-scaffold` | [features/bevy-scaffold](../features/bevy-scaffold/) | technical_director |
| `feature/environment-loader` | [features/environment-loader](../features/environment-loader/) | technical_director |

**Orden:** bevy-scaffold primero → merge → environment-loader desde develop.

---

## Tasks

| ID | Task | Branch | Agent | Done |
|---|---|---|---|---|
| S1-001 | Cargo.toml + App | `feature/bevy-scaffold` | technical_director | [ ] |
| S1-002 | GameState enum | `feature/bevy-scaffold` | technical_director | [ ] |
| S1-003 | Cámara isométrica | `feature/bevy-scaffold` | technical_director | [ ] |
| S1-004 | cargo run window | `feature/bevy-scaffold` | technical_director | [ ] |
| S1-005 | data/ JSON loader | `feature/bevy-scaffold` | technical_director | [ ] |
| S1-006 | Tile manifest parse | `feature/environment-loader` | technical_director | [ ] |
| S1-007 | Render 1 tile | `feature/environment-loader` | technical_director | [ ] |

---

## Agent chain

```
Studio Director
    ↓
Release Manager (ramas)
    ↓
Technical Director (feature/bevy-scaffold)
    ↓
QA Director (features/bevy-scaffold/QA.md)
    ↓
Release Manager (merge → develop)
    ↓
Technical Director (feature/environment-loader)
    ↓
QA → Release Manager merge
    ↓
Studio Director (metrics + roadmap)
```

---

## Sprint exit

- [ ] `bevy_project: true` in metrics
- [ ] POL-001–007 satisfied per branch
- [ ] Both branches `Merged` in registry
- [ ] STATUS.md updated on both features

---

## Siguiente

Sprint 02: `feature/player-controller` + `feature/inventory` on `release/vertical-slice`
