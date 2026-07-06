# Garage — Design

## Referencias

- [VEHICLE_DESIGN_GUIDE](../../docs/systems/VEHICLE_DESIGN_GUIDE.md) — slots, stats, compatibilidades
- [GAME_IDENTITY](../../docs/game/GAME_IDENTITY.md) — vehículo = consecuencia
- [lore/why_build_cars.md](../../lore/why_build_cars.md)

## Flujo UX

```
Entrar POI taller
    ↓
Vista slots (chasis base visible)
    ↓
Seleccionar slot → elegir pieza inventario
    ↓
Validar compatibilidad (motor↔chasis, peso)
    ↓
Confirmar → recalcular stats
    ↓
Probar / Salir
```

## Reglas

1. Incompatibilidad = mensaje claro, no crash
2. Stats visibles antes de confirmar
3. Desmontar devuelve pieza a inventario
4. Tono: taller del barrio, no simulador F1

## Scene hooks

- `scene_hook: garage_enter`
- `scene_hook: garage_exit`
- `poi_garage`
