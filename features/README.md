# Features — Funcionalidades del Juego

Cada feature es **autocontenida** — una IA puede entrar solo a esta carpeta.

## Estructura por feature (obligatoria)

```
features/<name>/
├── README.md       ← Overview, scope, dependencias
├── STATUS.md       ← Rama, lifecycle state, release target
├── CHANGELOG.md    ← Historial de cambios de la feature
├── TASKS.md        ← Backlog (sync roadmap/sprints)
├── QA.md           ← Criterios de aceptación
├── NOTES.md        ← Notas libres, decisiones, blockers
├── design.md       ← Spec de diseño (opcional detalle)
├── assets.md       ← Assets requeridos
└── ecs.md          ← ECS spec (si aplica)
```

## Lifecycle (STATUS.md)

```
Draft → In Design → Implementation → QA → Ready to Merge → Merged → Released
```

Ver [GITFLOW_GUIDE](../docs/production/GITFLOW_GUIDE.md).

## Índice — Vertical Slice

| Feature | Branch | STATUS |
|---|---|---|
| [bevy-scaffold](./bevy-scaffold/README.md) | `feature/bevy-scaffold` | planned |
| [environment-loader](./environment-loader/README.md) | `feature/environment-loader` | planned |
| [player-controller](./player-controller/README.md) | `feature/player-controller` | planned |
| [inventory](./inventory/README.md) | `feature/inventory` | planned |
| [crafting](./crafting/README.md) | `feature/crafting-system` | planned |
| [garage](./garage/README.md) | `feature/garage` | planned |
| [race](./race/README.md) | `feature/race-ai` | planned |
| [tutorial](./tutorial/README.md) | `feature/tutorial` | planned |
| [economy](./economy/README.md) | (shared en features) | planned |

## Alpha (futuro)

[clans](./clans/README.md) · [events](./events/README.md)

## Git

- Una feature = una rama — [production/branches/registry.json](../production/branches/registry.json)
- Release Manager es el único que opera git
- Studio Director asigna; Release Manager crea rama antes de trabajar
