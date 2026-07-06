# Clans — Design

## Referencias

- [CLAN_SYSTEM_GUIDE](../../docs/game/CLAN_SYSTEM_GUIDE.md) — roles, economía, eventos
- [ECONOMY_GUIDE §9](../../docs/systems/ECONOMY_GUIDE.md) — banco e intercambio
- [PROGRESSION_GUIDE §7](../../docs/game/PROGRESSION_GUIDE.md) — desbloqueos clan
- [lore/why_clans_exist.md](../../lore/why_clans_exist.md)

## Flujo UX

```
POI clan hub / plaza
    ↓
Crear clan (nombre + colores) o unirse por invitación
    ↓
Hub: miembros, banco, proyecto activo
    ↓
Donar materiales/chapitas → progreso proyecto
    ↓
Proyecto completo → pieza clan a miembros
    ↓
Bandera visible en carreras
```

## Reglas

1. Un jugador, un clan activo (CL-002)
2. Donaciones voluntarias — nunca obligatorias solo (CLAN §5)
3. Rep clan no baja por derrotas — estanca
4. Cooperación > competencia interna (CL-003)
5. Toda mecánica pasa filtro [GAME_IDENTITY](../../docs/game/GAME_IDENTITY.md)

## Scene hooks

- `scene_hook: clan_hub`
- `scene_hook: clan_create`
- `scene_hook: clan_donate`
- `poi_clan_hub`
