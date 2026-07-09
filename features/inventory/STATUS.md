# Inventory — Status

| Field | Value |
|---|---|
| **Branch** | `feature/inventory` |
| **Release** | `release/vertical-slice` |
| **Lifecycle** | `qa` |
| **Sprint** | Sprint_02 |
| **Started** | 2026-07-09 |

**Current:** `qa` — implementación completa; pendiente playtest manual y aprobación para merge.

## Implementado

- [x] Spawn del jugador desde Object Layer `spawn` de Tiled
- [x] NPC básico desde Object Layer `npcs` con interacción `[E]`
- [x] Tres pickups data-driven desde Object Layer `pickups`
- [x] `InventoryPlugin` pequeño con `PlayerInventory` y evento `PickupCollected`
- [x] Inventario mínimo `[I]` con cantidades actuales
- [x] Movimiento, cámara y colisión existentes integrados
- [x] Exportador Tiled y `map_validator` extendidos para hooks de exploración
- [x] `cargo clippy`, `cargo test` y arranque de `cargo run` verificados

## Pendiente de QA manual

- [ ] Recorrer el flujo completo en ventana: hablar con Tomás, recoger los 3 materiales y abrir inventario
- [ ] Confirmar legibilidad visual de NPC, pickups y panel en resolución objetivo
- [ ] Release Manager: aprobar y mergear a `develop`
