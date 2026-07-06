# MVP — Vertical Slice

**Phase:** vertical_slice  
**Generated:** 2026-07-06 (Studio Director)  
**Goal:** Probar el ADN del juego en 15 minutos jugables.

---

## La pregunta que responde

> *¿Los chicos del barrio convierten lo que encuentran en algo que compite?*

Si el MVP no demuestra **creatividad + exploración + competencia sana** → pivot antes de alpha.

---

## Loop obligatorio

| # | Paso | Feature | Validación |
|---|---|---|---|
| 1 | Spawn en plaza tutorial | world | Mapa carga, controles OK |
| 2 | Caminar al callejón | world | 2.5D movement |
| 3 | Recoger 3 pickups | inventory | Inventario +3 materiales |
| 4 | Ir al taller POI | garage | Trigger `InGarage` |
| 5 | Craft `wheel_small_01` | crafting | Receta consume materiales |
| 6 | Instalar ruedas | garage | Stats cambian |
| 7 | Ir a cancha | race | Trigger carrera |
| 8 | Completar 1 lap | race | Checkpoints + meta |
| 9 | Recibir chapitas | economy | +8–15 chapitas |
| 10 | Volver a plaza | — | Loop cerrado |

**Duración target:** 10–15 min primera run.

---

## Scope IN

- 1 barrio pequeño (~32×32 tiles)
- 3 tipos material pickup
- 1 receta craft
- 3 slots vehículo (chasis, motor, ruedas) — placeholders visuales OK
- 1 circuito cancha, 1 rival fácil o sin rival
- JSON data-driven (parts, recipes, race metadata)

## Scope OUT

- Clanes, torneos, tier medium/large
- Comercio NPC
- Audio final (silence OK)
- Brand/logo (ADR-005 Proposed)
- Vehicle Parts Pack real (colored placeholders)

---

## Exit criteria (MVP done)

- [ ] `cargo run` → loop completable
- [ ] 0 crashes en loop happy path
- [ ] Creative Director: refuerza ≥3 pilares
- [ ] Playtest 1 persona ≥10 min

---

## Blockers actuales (ver metrics/)

1. **B-001** — No existe proyecto Bevy (`Cargo.toml`)
2. **B-002** — No hay mapas en `data/maps/`
3. **B-003** — No hay assets vehículo (placeholders planificados)

---

## Agentes para entregar MVP

```
Studio Director
    → Technical Director (scaffold, ECS, systems)
    → World Designer (mapa tutorial)
    → Economy Designer (pickups, 1 receta)
    → Vehicle Designer (stats placeholder build)
    → Race Designer (circuito cancha metadata)
    → QA Director (acceptance MVP)
```
