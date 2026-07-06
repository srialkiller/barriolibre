# Crafting — Design

## Referencias

- [ECONOMY_GUIDE §7](../../docs/systems/ECONOMY_GUIDE.md) — recetas, costos, reglas
- [VEHICLE_DESIGN_GUIDE §7](../../docs/systems/VEHICLE_DESIGN_GUIDE.md) — craft y desmontaje
- [GAMEPLAY_GUIDE §3](../../docs/game/GAMEPLAY_GUIDE.md) — micro loop recolección → craft
- [lore/why_build_cars.md](../../lore/why_build_cars.md)

## Flujo UX

```
Abrir recetas (taller o panel)
    ↓
Listar recetas desbloqueadas
    ↓
Seleccionar receta → preview costos
    ↓
Validar inventario (materiales + chapitas)
    ↓
Confirmar → instant craft → pieza a inventario
    ↓
Toast feedback + SFX cartoon
```

## Reglas

1. Craft **instantáneo** en v1 — sin fallo posible si hay recursos
2. Receta oculta hasta blueprint o rep mínima
3. Materiales se consumen atómicamente (todo o nada)
4. Tono: "armamos con lo que encontramos", no fábrica industrial

## Scene hooks

- `scene_hook: craft_open`
- `scene_hook: craft_complete`
- Integración en `poi_garage`
