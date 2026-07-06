# Feature: Race / Carreras

**Status:** spec  
**Phase:** vertical_slice  
**Owner:** `race_designer` + `technical_director`  
**Docs:** [RACE_DESIGN_GUIDE](../../docs/game/RACE_DESIGN_GUIDE.md), [GAMEPLAY_GUIDE §4](../../docs/game/GAMEPLAY_GUIDE.md), [VEHICLE_DESIGN_GUIDE](../../docs/systems/VEHICLE_DESIGN_GUIDE.md)

## Resumen

Loop de **competencia en el barrio**: preparación → carrera con checkpoints → premios y reputación. Valida el build del jugador.

## MVP scope

- [ ] 1 circuito tutorial (`barrio_norte_circuito_01`)
- [ ] Checkpoints + meta (metadata JSON)
- [ ] 1 rival NPC amistoso
- [ ] Pantalla resultados + drops (chapitas, material)
- [ ] Stats vehículo afectan conducción cartoon

## Out of scope (v1)

- Clasificación / eliminatoria
- Multijugador
- Torneos clan (feature `events`)

## Dependencias

- `garage` — build pre-carrera
- `inventory` — recibir premios
- `economy` — chapitas y rep barrio
- Assets: checkpoints, FX polvo/confetti
