# Sprint 03 — Primer flujo jugable

**Generated:** 2026-07-09 by Studio Director  
**Phase:** vertical_slice  
**Depends on:** Sprint 02 complete  
**Goal:** Tutorial completo — Pedro → materiales → misión → garaje desbloqueado.

---

## Scope (este sprint)

| In | Out |
|---|---|
| QuestPlugin MVP | Crafting |
| Objetivos por eventos | Vehículos |
| Diálogo por fases | Carreras |
| HUD objetivo activo | Economía |
| Garaje desbloqueado (sin fabricar) | Guardado avanzado |

---

## Tasks

| ID | Task | Agent | Feature | Done |
|---|---|---|---|---|
| S3-Q-001 | Manifest `tutorial_first_cart.json` | gameplay_programmer | quest | [x] |
| S3-Q-002 | `QuestPlugin` + stages + HUD | gameplay_programmer | quest | [x] |
| S3-Q-003 | `NpcInteracted` en PlayerPlugin | gameplay_programmer | player | [x] |
| S3-Q-004 | `ItemCollected` en InventoryPlugin | gameplay_programmer | inventory | [x] |
| S3-Q-005 | Pedro + pickups reubicados en mapa | world_designer | map | [x] |
| S3-Q-006 | `GaragePlugin` unlock gate | technical_director | garage | [x] |
| S3-Q-007 | QA flujo completo | qa_engineer | quest | [ ] |

---

## Historia del jugador

1. Aparece en el barrio
2. Habla con Pedro
3. Pedro pide materiales para el primer carrito
4. Recoge cartón, alambre y chapitas
5. Inventario refleja progreso
6. Vuelve con Pedro → misión completa
7. Garaje desbloqueado (sin fabricar aún)

---

## Criterios de aceptación

- [ ] Flujo completable sin reiniciar
- [ ] Estados de misión correctos
- [ ] Eventos desacoplan NPC, inventario y misiones
- [x] `cargo run`, `cargo clippy`, tests pasan
- [x] Documentación y `STATUS.md` actualizados

---

## Post-Sprint 03 (futuro)

Craft + garage UI + carrera permanecen en backlog MVP original (`S3-001`…`S3-010`).
