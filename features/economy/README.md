# Feature: Economy / Economía

**Status:** spec  
**Phase:** vertical_slice  
**Owner:** `economy_designer` + `technical_director`  
**Docs:** [ECONOMY_GUIDE](../../docs/systems/ECONOMY_GUIDE.md), [PROGRESSION_GUIDE §4](../../docs/game/PROGRESSION_GUIDE.md), [GAMEPLAY_GUIDE §2](../../docs/game/GAMEPLAY_GUIDE.md)

## Resumen

Capas de recursos del jugador: **chapitas**, **materiales**, **reputación** y reglas de fuentes/sumideros. Orquesta craft, carreras y comercio básico.

## MVP scope

- [ ] Resource `PlayerEconomy` (chapitas, materials, reputation)
- [ ] Fuentes v1: pickup, premio carrera, venta material
- [ ] Sumideros v1: craft, inscripción carrera tutorial
- [ ] HUD chapitas + rep barrio
- [ ] Tabla precios base en JSON

## Out of scope (v1)

- Comercio dinámico semanal
- Banco clan
- IAP / monetización

## Dependencias

- `inventory` — materiales y piezas (puede compartir resource v1)
- `crafting` — sumidero principal chapitas/materiales
- `race` — fuente chapitas + rep
- Assets: icono chapitas, UI rep bar
