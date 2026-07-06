# Carreras de Barrio

Videojuego de carreras infantiles en barrio latinoamericano.  
**Rust + Bevy** · 2.5D isométrico · Sprites prerenderizados.

> *No trata sobre autos. Trata sobre creatividad.*

---

## Estudio virtual (empezar aquí)

Este repo funciona como un **estudio de desarrollo con agentes especializados**, no como un asistente genérico.

| Carpeta | Qué es |
|---|---|
| [`agents/`](./agents/README.md) | Equipo virtual — roles, límites, contexto |
| [`docs/`](./docs/README.md) | Guías del juego por dominio |
| [`decisions/`](./decisions/README.md) | ADRs — por qué elegimos X |
| [`lore/`](./lore/README.md) | Coherencia del mundo |

### Invocar un agente

```
@agents/world_designer.md Diseña un barrio con cancha y taller
@agents/creative_director.md ¿El nitro comprable encaja en el juego?
@agents/technical_director.md Modela VehicleAssembly en ECS
```

---

## Inicio rápido

| Necesito… | Ir a… |
|---|---|
| ADN del juego | [docs/game/GAME_IDENTITY.md](./docs/game/GAME_IDENTITY.md) |
| Elegir agente | [agents/README.md](./agents/README.md) |
| Por qué Bevy / 2.5D / ECS | [decisions/](./decisions/README.md) |
| Por qué los niños corren | [lore/why_kids_race.md](./lore/why_kids_race.md) |
| Nombre comercial (pendiente) | [decisions/ADR-005-brand-naming.md](./decisions/ADR-005-brand-naming.md) |

---

## Assets

```
assets/environment/     ← ENVIRONMENT_BASE_PACK_01 (155 tiles)
data/tilesets/          ← Manifiestos JSON
scripts/                ← Pipeline postproceso
```

Estado: [assets/environment/ENVIRONMENT_BASE_PACK_01.md](./assets/environment/ENVIRONMENT_BASE_PACK_01.md)

**Producción de assets pausada** — prioridad: estudio virtual + primer barrio jugable.

---

## Marca

| Concepto | Nombre actual |
|---|---|
| Juego (working title) | **Carreras de Barrio** |
| Repositorio | `barriolibre` |
| Decisión final | Pendiente → [ADR-005](./decisions/ADR-005-brand-naming.md) |
