# Architecture Decision Records (ADR)

Registro de **decisiones irreversibles o costosas de cambiar**. Dentro de un año agradecerás tenerlas.

## Formato

Cada ADR sigue:

```
# ADR-NNN: Título
Status: Accepted | Proposed | Superseded
Date: YYYY-MM-DD
```

## Índice

| ID | Título | Status |
|---|---|---|
| [ADR-001](./ADR-001-bevy-engine.md) | Motor Bevy (Rust) | Accepted |
| [ADR-002](./ADR-002-2.5d-isometric.md) | Vista 2.5D isométrica | Accepted |
| [ADR-003](./ADR-003-prerendered-sprites.md) | Sprites prerenderizados vs 3D | Accepted |
| [ADR-004](./ADR-004-ecs-architecture.md) | Arquitectura ECS | Accepted |
| [ADR-005](./ADR-005-brand-naming.md) | Nombre comercial del juego | **Proposed** |

## Cuándo crear un ADR

- Elección de motor, framework, pipeline
- Decisiones que afectan a todo el equipo por meses
- Trade-offs con coste alto de revertir

## Precedencia

```
ADR Accepted  >  guía de docs/  >  opinión de agente
```

Si una guía contradice un ADR Accepted → la guía está desactualizada.
