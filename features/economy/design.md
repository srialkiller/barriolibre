# Economy — Design

## Referencias

- [ECONOMY_GUIDE](../../docs/systems/ECONOMY_GUIDE.md) — filosofía, capas, balance
- [PROGRESSION_GUIDE §4](../../docs/game/PROGRESSION_GUIDE.md) — desbloqueos por reputación
- [GAMEPLAY_GUIDE §2](../../docs/game/GAMEPLAY_GUIDE.md) — core loop macro
- [NEIGHBORHOOD_DESIGN_GUIDE](../../docs/world/NEIGHBORHOOD_DESIGN_GUIDE.md) — fuentes mapeadas a POI

## Flujo UX

```
Ganar chapitas (carrera / venta)
    ↓
Gastar en craft o inscripción
    ↓
Subir rep barrio (carreras, misiones)
    ↓
Desbloquear receta / comercio / circuito
    ↓
Feedback HUD + toast progreso
```

## Reglas

1. Chapitas no compran victoria directa (E-002)
2. Toda fuente mapeada a POI o actividad (E-007)
3. Sesión 30 min → 1–2 crafts posibles (balance §10)
4. Recetas y precios en JSON (E-004)

## Scene hooks

- `scene_hook: shop_open` (puesto barrio — post-MVP)
- `scene_hook: rep_level_up`
