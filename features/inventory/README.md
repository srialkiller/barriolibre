# Feature: Inventory / Inventario

**Status:** spec  
**Phase:** vertical_slice  
**Owner:** `economy_designer` + `technical_director`  
**Docs:** [ECONOMY_GUIDE §2–4](../../docs/systems/ECONOMY_GUIDE.md), [GAMEPLAY_GUIDE §3](../../docs/game/GAMEPLAY_GUIDE.md)

## Resumen

Almacén del jugador: **materiales**, **chapitas**, **piezas** y **blueprints**. Base de recolección, craft y taller.

## MVP scope

- [ ] Resource `PlayerInventory` con slots lógicos
- [ ] Pickup mundo → inventario (materiales comunes)
- [ ] UI panel inventario (tabs: materiales / piezas)
- [ ] Add/remove atómico para craft y garage
- [ ] Persistencia en save

## Out of scope (v1)

- Stack limits avanzados / peso inventario
- Intercambio entre jugadores
- Ordenar/filtrar avanzado

## Dependencias

- `crafting` — consume materiales
- `garage` — instala/desinstala piezas
- `economy` — chapitas y reputación (resource separado OK v1)
- Assets: iconos pickup + HUD contador
