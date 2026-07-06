# Events — Design

## Referencias

- [GAMEPLAY_GUIDE §4–5](../../docs/game/GAMEPLAY_GUIDE.md) — race loop, modos, nuevos eventos
- [CLAN_SYSTEM_GUIDE §6](../../docs/game/CLAN_SYSTEM_GUIDE.md) — eventos clan
- [RACE_DESIGN_GUIDE](../../docs/game/RACE_DESIGN_GUIDE.md) — circuitos torneo
- [PROGRESSION_GUIDE §9](../../docs/game/PROGRESSION_GUIDE.md) — metas largo plazo
- [lore/tournament_organizers.md](../../lore/tournament_organizers.md), [lore/neighborhood_races.md](../../lore/neighborhood_races.md)

## Flujo UX

```
Completar carrera / subir rep
    ↓
Evento nuevo aparece en calendario barrio
    ↓
Jugador abre calendario (POI plaza / HUD)
    ↓
Inscribirse (chapitas / tag clan si aplica)
    ↓
Countdown día evento → transición a race/clan flow
    ↓
Premios + actualizar calendario siguiente slot
```

## Reglas

1. Eventos desbloqueados por progresión — no paywall
2. Torneo clan = entry fee 25 chapitas/miembro (ECONOMY §9)
3. Calendario visible en plaza — tono "hay carrera el sábado"
4. Fallar evento no penaliza rep permanentemente
5. Máx 1 evento activo crítico por día in-game (alpha)

## Scene hooks

- `scene_hook: event_calendar_open`
- `scene_hook: event_register`
- `scene_hook: event_start`
- `poi_plaza_calendario`
