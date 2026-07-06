# Sprint 02 — Mapa + Micro Loop

**Generated:** 2026-07-06 by Studio Director  
**Phase:** vertical_slice  
**Depends on:** Sprint 01 complete  
**Goal:** Explorar barrio mini, recoger materiales, inventario funcional.

---

## Prerequisites

- [ ] Sprint 01 exit criteria met
- [ ] `bevy_project: true`

---

## Tasks

| ID | Task | Agent | Feature | Deps | Done |
|---|---|---|---|---|---|
| S2-001 | Layout mapa tutorial 32×32 (JSON) | world_designer | race | S1-* | [ ] |
| S2-002 | POIs: plaza, callejón, taller, cancha | world_designer | race | S2-001 | [ ] |
| S2-003 | Tilemap renderer desde manifest | technical_director | — | S2-001, S1-004 | [ ] |
| S2-004 | Player movement isométrico | technical_director | — | S1-005 | [ ] |
| S2-005 | `PlayerInventory` Resource + UI mínima | technical_director | inventory | S1-007 | [ ] |
| S2-006 | Pickup entities + collect system | technical_director | inventory | S2-005 | [ ] |
| S2-007 | 3 spawn points materiales (callejón) | world_designer | economy | S2-002 | [ ] |
| S2-008 | QA: movement + pickup acceptance | qa_director | inventory | S2-006 | [ ] |

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

- [ ] Jugador camina plaza → callejón → recoge 3 items
- [ ] Inventario muestra materiales
- [ ] Mapa usa tiles environment pack
- [ ] features/inventory/tasks.md items checked

---

## Blockers watch

- Environment QA pending — no bloquea si tiles render OK
- No props pack — usar tiles only

---

## Next sprint preview

Sprint 03: craft ruedas, garage install, carrera cancha 1 lap.
