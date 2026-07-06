# Feature: Foundation Runtime

**Phase:** vertical_slice · **Sprint:** 01 — Foundation Runtime  
**Branch:** `feature/bevy-foundation-runtime`  
**Release:** `release/vertical-slice`

Runtime Bevy completo: ECS, assets, render isométrico, primer barrio cargado desde JSON.

**Objetivo visible:** `cargo run` → barrio renderizado.

## Owners

| Rol | Agente |
|---|---|
| Arquitectura ECS / runtime | `technical_director` |
| Cargo / CI / lints | `build_engineer` |
| map_validator, F3 debug | `tools_engineer` |
| Map JSON | `world_designer` |
| DoD QA | `qa_director` |

## Docs

- [**BEVY_ARCHITECTURE.md**](../../docs/systems/BEVY_ARCHITECTURE.md) — **constitución técnica (gate Sprint 01)**
- [Sprint_01.md](../../roadmap/Sprint_01.md) — Definition of Done
- [ADR-001](../../decisions/ADR-001-bevy-engine.md) · [ADR-004](../../decisions/ADR-004-ecs-architecture.md)

## Supersedes

Reemplaza `bevy-scaffold` + `environment-loader` como **una sola feature** unificada.
