# Inventory — Design

## Referencias

- [ECONOMY_GUIDE §2–4](../../docs/systems/ECONOMY_GUIDE.md) — capas de recursos, materiales
- [GAMEPLAY_GUIDE §3](../../docs/game/GAMEPLAY_GUIDE.md) — micro loop recolección
- [NEIGHBORHOOD_DESIGN_GUIDE](../../docs/world/NEIGHBORHOOD_DESIGN_GUIDE.md) — spawn materiales en POIs
- [lore/why_build_cars.md](../../lore/why_build_cars.md)

## Flujo UX

```
Ver material en mundo (highlight)
    ↓
Interactuar (E) → pickup
    ↓
Toast "+1 Cartón" + contador HUD
    ↓
Abrir inventario (I) → tabs materiales / piezas
    ↓
Seleccionar pieza → contexto (instalar en garage)
```

## Reglas

1. Materiales stackean por `MaterialId`; piezas son entradas únicas por `PartId`
2. Pickup idempotente — no duplicar si animación interrumpida
3. Todo ítem tiene uso (ECONOMY E-001) — no basura pura
4. Feedback inmediato en pickup (visual + sonoro)

## Scene hooks

- `scene_hook: inventory_open`
- `scene_hook: item_pickup`
- Pickup entities tagged `Collectible`
