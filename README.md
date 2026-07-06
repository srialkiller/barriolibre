# Carreras de Barrio

## Estudio virtual

```
@agents/studio_director.md Iniciar Sprint 01 — Foundation Runtime
python scripts/studio_scan.py
```

## Constituciones del estudio

| Dominio | Documento |
|---|---|
| Gameplay | [GAME_IDENTITY.md](docs/game/GAME_IDENTITY.md) |
| Arte | [ART_STYLE_GUIDE.md](docs/art/ART_STYLE_GUIDE.md) |
| **Runtime Bevy** | [**BEVY_ARCHITECTURE.md**](docs/systems/BEVY_ARCHITECTURE.md) ✅ |

## Sprint 01 — Foundation Runtime

**Gate BEVY_ARCHITECTURE:** ✅ passed — listo para abrir rama  
**Rama:** `feature/bevy-foundation-runtime`  
**DoD:** `cargo run` → **barrio renderizado**

| Rol | Agente |
|---|---|
| Cargo / CI | build_engineer |
| ECS / render / assets | technical_director |
| map_validator, F3 | tools_engineer |
| Git | release_manager |

## Studio Health

Ver [`metrics/studio_health.json`](metrics/studio_health.json) — Runtime 🔴 hasta Sprint 01.

## Vertical Slice

**15 min** flujo completo → [roadmap/MVP.md](roadmap/MVP.md)

**Regla:** cada sprint = `cargo run` + avance visible.
