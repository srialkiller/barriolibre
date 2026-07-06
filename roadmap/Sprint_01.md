# Sprint 01 — Bevy Scaffold

**Generated:** 2026-07-06 by Studio Director  
**Phase:** vertical_slice  
**Previous sprint:** —  
**Goal:** Proyecto Rust/Bevy compilable con estados de juego base.

---

## Context (from metrics)

- `bevy_project: false` — **BLOCKER CRÍTICO**
- Docs + tiles listos; 0 archivos `.rs`
- ADR-001, ADR-004 vigentes

---

## Tasks

| ID | Task | Agent | Feature | Deps | Done |
|---|---|---|---|---|---|
| S1-001 | Crear `Cargo.toml` Bevy 0.15+ workspace | technical_director | — | — | [ ] |
| S1-002 | Crate `barriolibre` con App + plugins base | technical_director | — | S1-001 | [ ] |
| S1-003 | `GameState` enum (Exploring, Garage, Racing) | technical_director | race | S1-002 | [ ] |
| S1-004 | Asset loader tiles environment (1 tile test) | technical_director | — | S1-002 | [ ] |
| S1-005 | Cámara isométrica 2:1 fija | technical_director | — | S1-002 | [ ] |
| S1-006 | CI/local: `cargo check` + `cargo run` window | technical_director | — | S1-002 | [ ] |
| S1-007 | Folder structure `data/` + load JSON skeleton | technical_director | economy | S1-002 | [ ] |

---

## Agent assignments

```
@agents/technical_director.md
  Implement S1-001 through S1-007 per ADR-001 and ADR-004.
  Reference docs/game/GAMEPLAY_GUIDE.md §7 for GameState.
  Reference docs/production/ASSET_PIPELINE.md for asset paths.
```

---

## Dependencies graph

```
S1-001 → S1-002 → S1-003, S1-004, S1-005, S1-007
S1-002 → S1-006
```

---

## Sprint exit

- [ ] `cargo run` abre ventana Bevy
- [ ] 1 tile environment renderizado
- [ ] `GameState` cambia con tecla debug
- [ ] `studio_scan.py` reporta `bevy_project: true`

---

## Risks

| Risk | Mitigation |
|---|---|
| Bevy version API drift | Pin version in Cargo.toml + ADR note |
| Tile pivot incorrect | Test con `road_straight_h_01` anchor |

---

## Next sprint preview

Sprint 02: mapa tutorial + player movement + inventory pickups.
