# Feature: Events / Eventos del Barrio

**Status:** spec  
**Phase:** alpha  
**Owner:** `game_designer` + `technical_director`  
**Docs:** [GAMEPLAY_GUIDE §4–5](../../docs/game/GAMEPLAY_GUIDE.md), [CLAN_SYSTEM_GUIDE §6](../../docs/game/CLAN_SYSTEM_GUIDE.md), [RACE_DESIGN_GUIDE](../../docs/game/RACE_DESIGN_GUIDE.md)

## Resumen

**Calendario y orquestación** de eventos: carreras especiales, torneos de barrio, eventos clan y desbloqueos post-carrera. Motor de retención social.

## MVP scope (alpha)

- [ ] Resource `EventCalendar` con slots semanales
- [ ] 2 tipos: carrera especial barrio + torneo clan stub
- [ ] Desbloqueo evento tras rep/carrera previa
- [ ] UI calendario barrio (próximos eventos)
- [ ] Hooks a `race` y `clans` para ejecución

## Out of scope (alpha)

- Eventos estacionales live-ops
- Matchmaking online
- Fiesta post-torneo (solo placeholder)

## Dependencias

- `race` — ejecutar carreras de evento
- `clans` — torneos clan vs clan
- `economy` — entry fees y premios pool
- Assets: banners evento, UI calendario
