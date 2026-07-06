# Race — Design

## Referencias

- [RACE_DESIGN_GUIDE](../../docs/game/RACE_DESIGN_GUIDE.md) — tipos, circuitos, rivales
- [GAMEPLAY_GUIDE §4](../../docs/game/GAMEPLAY_GUIDE.md) — race loop
- [NEIGHBORHOOD_DESIGN_GUIDE](../../docs/world/NEIGHBORHOOD_DESIGN_GUIDE.md) — calles como pista
- [lore/neighborhood_races.md](../../lore/neighborhood_races.md), [lore/why_kids_race.md](../../lore/why_kids_race.md)

## Flujo UX

```
Interactuar POI carrera / NPC organizador
    ↓
Preview circuito (mapa mini + laps)
    ↓
Confirmar build (desde garage o pre-build)
    ↓
Countdown → carrera (checkpoints, rival)
    ↓
Meta → resultados + premios + rep
    ↓
Volver a explorar
```

## Reglas

1. Duración objetivo 90–150 s (RC-004)
2. ≥3 checkpoints por vuelta (RC-002)
3. ≥1 atajo documentado en circuito competitivo (RC-003)
4. Sin colisiones agresivas — bump cartoon (RC-006)
5. Premios alineados con [ECONOMY_GUIDE](../../docs/systems/ECONOMY_GUIDE.md)

## Scene hooks

- `scene_hook: race_register`
- `scene_hook: race_start`
- `scene_hook: race_finish`
- `poi_race_start_plaza`
