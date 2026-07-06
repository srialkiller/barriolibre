# Features — Funcionalidades del Juego

Cada feature vive **aislada** con todo lo necesario para diseñar, implementar, testear y producir assets.

## Estructura por feature

```
features/<name>/
├── README.md    ← Overview, status, fase, agente owner
├── design.md    ← Diseño (links a docs/ + spec local)
├── tasks.md     ← Backlog de la feature (sync con roadmap/)
├── qa.md        ← Criterios de aceptación
├── assets.md    ← Assets requeridos y estado
└── ecs.md       ← Components, resources, systems (Bevy)
```

## Índice

| Feature | Status | Fase | Owner agent |
|---|---|---|---|
| [garage](./garage/README.md) | spec | vertical_slice | vehicle_designer + technical_director |
| [crafting](./crafting/README.md) | spec | vertical_slice | economy_designer |
| [inventory](./inventory/README.md) | spec | vertical_slice | economy_designer |
| [race](./race/README.md) | spec | vertical_slice | race_designer |
| [economy](./economy/README.md) | spec | vertical_slice | economy_designer |
| [clans](./clans/README.md) | spec | alpha | game_designer |
| [events](./events/README.md) | spec | alpha | game_designer |

## Sync con roadmap

El **Studio Director** propaga tasks de `roadmap/Sprint_NN.md` → `features/*/tasks.md`.

## Sync con metrics

Post-implementación: actualizar `assets.md` y ejecutar `python scripts/studio_scan.py`.
