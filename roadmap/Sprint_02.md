# Sprint 02 — Exploration Loop

**Generated:** 2026-07-06 by Studio Director
**Phase:** vertical_slice
**Depends on:** Sprint 01 complete
**Goal:** Explorar barrio mini, recoger materiales, inventario funcional.
**Branch:** `feature/inventory`
**Status:** 🟡 QA

---

## Prerequisites

- [x] Sprint 01 exit criteria met
- [x] `bevy_project: true`

---

## Tasks

| ID | Task | Agent | Feature | Deps | Done |
|---|---|---|---|---|---|
| S2-001 | Spawn desde Object Layer de Tiled | world_designer | player | S1-* | [x] |
| S2-002 | Integrar NPC y pickups como scene hooks | world_designer | inventory | S2-001 | [x] |
| S2-003 | Tilemap renderer desde manifest | technical_director | — | S1-004 | [x] |
| S2-004 | Player movement, cámara y colisión | technical_director | player | S1-005 | [x] |
| S2-005 | `PlayerInventory` Resource + UI mínima | technical_director | inventory | S1-007 | [x] |
| S2-006 | Pickup entities + collect system | technical_director | inventory | S2-005 | [x] |
| S2-007 | NPC básico + diálogo | technical_director | player | S2-002 | [x] |
| S2-008 | QA automatizado: clippy, tests, validator, startup | qa_director | inventory | S2-006 | [x] |
| S2-009 | Playtest manual del exploration loop | qa_director | inventory | S2-008 | [ ] |

---

## Agent chain

```
1. @agents/world_designer.md — S2-001, S2-002, S2-007
   Output: data/maps/barrio_tutorial_01.json + POI metadata

2. @agents/technical_director.md — S2-003, S2-004, S2-005, S2-006
   Reference: features/inventory/ecs.md

3. @agents/qa_director.md — S2-008
   Reference: features/inventory/qa.md
```

---

## Creative gate

```
@agents/creative_director.md
  Validate micro loop reinforces pillars Creatividad + Explorar.
```

---

## Sprint exit

- [ ] Jugador habla con Tomás y recoge 3 materiales en playtest
- [ ] Inventario muestra Cartón limpio, Alambre y Chapitas
- [x] Spawn, NPC y pickups provienen de Object Layers de Tiled
- [x] Mapa usa tiles environment pack
- [x] Implementación y QA automatizado completos

---

## Blockers watch

- Environment QA pending — no bloquea si tiles render OK
- No props pack — usar tiles only

---

## Next sprint preview

Sprint 03: craft ruedas, garage install, carrera cancha 1 lap.
