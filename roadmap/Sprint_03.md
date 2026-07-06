# Sprint 03 — Craft + Garage + Carrera

**Generated:** 2026-07-06 by Studio Director  
**Phase:** vertical_slice  
**Depends on:** Sprint 02 complete  
**Goal:** **MVP loop cerrado** — craft → garage → race → reward.

---

## Prerequisites

- [ ] Sprint 02 exit criteria met
- [ ] Inventario funcional con materiales

---

## Tasks

| ID | Task | Agent | Feature | Deps | Done |
|---|---|---|---|---|---|
| S3-001 | `recipe_table.json` + 1 receta wheel | economy_designer | crafting | S2-* | [ ] |
| S3-002 | Craft system + UI taller básica | technical_director | crafting | S3-001 | [ ] |
| S3-003 | `parts_catalog.json` + default starter build | vehicle_designer | garage | S3-001 | [ ] |
| S3-004 | VehicleAssembly + stats system | technical_director | garage | S3-003 | [ ] |
| S3-005 | Garage POI trigger + install UI | technical_director | garage | S3-004, S2-002 | [ ] |
| S3-006 | Circuito cancha metadata + checkpoints | race_designer | race | S2-002 | [ ] |
| S3-007 | Race state: countdown, lap, finish | technical_director | race | S3-006, S3-004 | [ ] |
| S3-008 | Premios chapitas post-carrera | technical_director | economy | S3-007 | [ ] |
| S3-009 | QA MVP full loop | qa_director | — | S3-008 | [ ] |
| S3-010 | Creative Director MVP playtest review | creative_director | — | S3-009 | [ ] |

---

## Agent chain

```
1. @agents/economy_designer.md — S3-001
2. @agents/vehicle_designer.md — S3-003
3. @agents/race_designer.md — S3-006
   Output: data/races/barrio_tutorial_cancha_01.json

4. @agents/technical_director.md — S3-002, S3-004, S3-005, S3-007, S3-008

5. @agents/qa_director.md — S3-009 (MVP.md exit criteria)

6. @agents/creative_director.md — S3-010 (pilares)
```

---

## Placeholder policy

Vehicle visuals = **colored sprites** hasta Vehicle Parts Pack. Documentado en features/garage/assets.md.

---

## Sprint exit = MVP DONE

- [ ] All MVP.md exit criteria ✅
- [ ] roadmap/MVP.md checkboxes complete
- [ ] `production/vertical_slice/` → ready for playtest
- [ ] Studio Director recommends: Sprint 04 = polish OR alpha prep

---

## Post-MVP decision point

| Option | Sprint 04 focus |
|---|---|
| A | Polish MVP + environment QA + 1 rival NPC |
| B | Alpha prep — progression tier medium |
| C | Brand workshop (ADR-005) — **solo post-playtest positivo** |

Studio Director recomienda **Option A** primero.

---

## Next: Sprint 04 generation

```
@agents/studio_director.md Generar Sprint 04
```
(Ejecutar solo después de completar Sprint 03)
