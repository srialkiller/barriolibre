# Feature: Crafting / Recetas

**Status:** spec  
**Phase:** vertical_slice  
**Owner:** `economy_designer` + `technical_director`  
**Docs:** [ECONOMY_GUIDE §7](../../docs/systems/ECONOMY_GUIDE.md), [VEHICLE_DESIGN_GUIDE §7](../../docs/systems/VEHICLE_DESIGN_GUIDE.md), [GAMEPLAY_GUIDE §3](../../docs/game/GAMEPLAY_GUIDE.md)

## Resumen

Sistema de **recetas instantáneas** que convierten materiales (+ chapitas opcional) en piezas de vehículo. Puente entre exploración e inventario/taller.

## MVP scope

- [ ] Cargar `data/economy/recipe_table.json`
- [ ] Craft desde UI taller o panel simple
- [ ] Validar materiales + chapitas antes de craft
- [ ] Output pieza → inventario del jugador
- [ ] 3 recetas starter: `wheel_small_01`, `engine_small_01`, `vehicle_chassis_small_01`

## Out of scope (v1)

- Cola de craft / timers
- Fusionar duplicados
- Craft fuera del taller (solo POI taller v1)

## Dependencias

- `inventory` — consumir materiales, recibir piezas
- `economy` — chapitas, reputación para blueprints
- `garage` — UI host del craft en vertical slice
- Assets: iconos materiales/piezas (placeholder OK)
