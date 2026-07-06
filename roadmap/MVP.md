# MVP — Vertical Slice (15 minutos)

**Phase:** vertical_slice  
**Regla estricta:** Si un sprint no acerca a este flujo → **no es prioritario**.

---

## Objetivo

**15 minutos de juego continuo** demostrando el juego completo (aunque mínimo).

---

## Flujo obligatorio (Vertical Slice)

| # | Paso | Sprint aprox |
|---|---|---|
| 1 | Entrar al barrio | 01 (runtime) + 02 |
| 2 | Caminar | 02 |
| 3 | Recoger piezas | 02 |
| 4 | Entrar al garaje | 03 |
| 5 | Construir vehículo simple | 03 |
| 6 | Correr una carrera | 03 |
| 7 | Ganar recompensas | 03 |
| 8 | Mejorar una pieza | 03–04 |
| 9 | Guardar partida | 04 |
| 10 | Volver al menú | 04 |

**Duración:** 10–15 min primera run.

---

## Sprint 01 contribuye

Foundation Runtime → pasos 1 parcial (**barrio visible**, sin gameplay aún).

**DoD Sprint 01:** `cargo run` → barrio renderizado.

---

## Regla del estudio

> Cada sprint termina con `cargo run` y **avance visible**.  
> No acumular trabajo invisible.

---

## Exit criteria (Vertical Slice done)

- [ ] Flujo 1–10 completable sin crashes
- [ ] Creative Director: ≥3 pilares reforzados
- [ ] Playtest ≥15 min positivo
- [ ] `studio_health` → Gameplay 🟢

---

## Blockers

Ver `metrics/project_state.json` — B-001 Foundation Runtime pendiente.
