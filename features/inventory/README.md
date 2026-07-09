# Feature: Inventory / Inventario

**Status:** QA
**Phase:** vertical_slice
**Owner:** `economy_designer` + `technical_director`
**Docs:** [ECONOMY_GUIDE §2–4](../../docs/systems/ECONOMY_GUIDE.md), [GAMEPLAY_GUIDE §3](../../docs/game/GAMEPLAY_GUIDE.md)

## Resumen

Almacén del jugador: **materiales**, **chapitas**, **piezas** y **blueprints**. Base de recolección, craft y taller.

## MVP scope

- [x] Resource `PlayerInventory` con stacks por `MaterialId`
- [x] Pickup mundo → inventario (tres materiales comunes)
- [x] UI mínima de materiales y cantidades
- [x] Integración data-driven con Object Layers de Tiled
- [x] NPC básico para validar interacción de exploración

## Out of scope (v1)

- Stack limits avanzados / peso inventario
- Intercambio entre jugadores
- Ordenar/filtrar avanzado
- Crafting, garage, vehículos, carreras y guardado avanzado

## Controles Sprint 02

- `WASD` / flechas — movimiento
- `E` — hablar o recoger el elemento cercano
- `I` — abrir/cerrar inventario
- `F3` — overlay técnico

## Datos del mapa

`scene_hooks.json` se genera desde las Object Layers `spawn`, `npcs` y
`pickups` de `barrio_tutorial_01.tmx`. Rust consume esos hooks mediante
`LoadedNeighborhood`; posiciones y contenido no están hardcodeados.

## Dependencias

- `crafting` — consume materiales
- `garage` — instala/desinstala piezas
- `economy` — chapitas y reputación (resource separado OK v1)
- Assets: iconos pickup + HUD contador
