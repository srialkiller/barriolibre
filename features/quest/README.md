# Feature: Quest / Misiones

**Status:** qa  
**Phase:** vertical_slice  
**Owner:** `gameplay_programmer` + `technical_director`  
**Branch:** `feature/quest`  
**Sprint:** Sprint_03

## Resumen

Misiones data-driven con objetivos desacoplados por eventos. Sprint 03 entrega el tutorial **El primer carrito** con Pedro.

## MVP scope (Sprint 03)

- [x] `QuestPlugin` con estado de misión tutorial
- [x] Eventos `NpcInteracted` (player) e `ItemCollected` (inventory)
- [x] Diálogo por fases según progreso de misión
- [x] HUD de objetivo activo (esquina superior izquierda)
- [x] Completar misión emite `GarageUnlocked`

## Out of scope (Sprint 03)

- Cadena de misiones múltiples
- Guardado de progreso
- Marcadores 3D en el mapa
- Recompensas económicas

## Dependencias

- `player` — emite `NpcInteracted`
- `inventory` — emite `ItemCollected`
- `garage` — consume `GarageUnlocked`

## Datos

- `data/quests/tutorial_first_cart.json`

## Controles del flujo

1. Spawn en barrio → objetivo: hablar con Pedro
2. `[E]` con Pedro → acepta misión
3. Recoger cartón, alambre y chapitas → inventario `[I]`
4. Volver con Pedro → misión completa → garaje desbloqueado
