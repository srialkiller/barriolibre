# ADR-004: Arquitectura ECS

**Status:** Accepted  
**Date:** 2026-07-06  
**Deciders:** Technical Director

---

## Context

El juego tiene entidades heterogéneas que comparten poco estado:

- Vehículos ensamblados dinámicamente
- Pickups de materiales en POIs
- NPCs rivales
- Checkpoints y triggers de carrera
- UI y estado de sesión

OOP profundo con herencia no escala bien. Bevy impone ECS.

## Decision

**ECS estricto** — toda lógica de juego como Systems operando sobre Components/Resources.

### Convenciones

| Concepto | Uso |
|---|---|
| **Component** | Datos por entidad (`VehicleAssembly`, `Transform`, `Pickup`) |
| **Resource** | Estado global (`PlayerEconomy`, `PartsCatalog`, `GameState`) |
| **System** | Lógica pura, preferir `Query` + `Changed<T>` filters |
| **Events** | Comunicación desacoplada (`RaceFinished`, `PartCrafted`) |

### Data-driven

Balance y contenido en JSON bajo `data/`:

```
data/vehicles/parts_catalog.json
data/economy/recipe_table.json
data/progression/unlock_table.json
data/races/*.json
```

Rust carga → Resources. **No hardcodear balance en systems.**

## Rationale

- Vehículos modulares = entidad + N piezas como componentes/hijos
- Mismo motor para exploración y carrera (swap systems por state)
- Testeable: systems aislados con mock Resources
- Alineado con Bevy idioms (ADR-001)

## Consequences

**Positivas:**
- Guías de diseño ya incluyen sketches ECS
- Hot reload de JSON sin recompilar balance
- Performance predecible (archetypes)

**Negativas:**
- Curva ECS para quien viene de OOP
- Debugging indirecto (queries)
- Disciplina estricta para no mezclar lógica en components

## Referencias

- `docs/game/GAMEPLAY_GUIDE.md`
- `docs/systems/VEHICLE_DESIGN_GUIDE.md` §9
- `agents/technical_director.md`
