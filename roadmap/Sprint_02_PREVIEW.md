# Sprint 02 — Preview (no implementar aún)

**Depends on:** Milestone 0 complete  
**Focus:** Player & Exploration + **Testing Pyramid**

---

## Features

- `feature/player-controller`
- `feature/inventory`

---

## Testing Pyramid (Bevy)

Incorporar desde Sprint 02 — no esperar al final del juego.

```
Unit Tests           ← pure functions, IDs, manifest parse
    ↓
System Tests         ← single system + mock resources
    ↓
Plugin Tests         ← plugin builds, registers resources
    ↓
Gameplay Tests       ← state transitions, event chains
    ↓
Golden Image Tests   ← render map / tile → PNG compare
```

### Golden Image Tests

Críticos con assets generados por IA:

- Snapshot de mapa renderizado
- Snapshot de style anchor tile
- CI falla si pixel diff > threshold sin aprobación

**Owner:** Build Engineer + QA Director  
**Tool:** `tests/golden/` + `tools/golden_compare/` (futuro)

---

## Visible deliverable Sprint 02

`cargo run` → caminar por barrio + recoger 1 pickup + inventario UI mínima.

---

## Studio rule

Sprint 02 no empieza hasta M0 merged + Runtime 🟢 en studio_health.
