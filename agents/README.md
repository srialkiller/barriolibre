# Estudio Virtual — Carreras de Barrio

Este directorio **no es documentación del juego**. Es el **equipo de desarrollo virtual**: especialistas con rol, límites y contexto preciso.

## Cómo invocar un agente

En Cursor u OpenCode, referencia el archivo del rol:

```
@agents/world_designer.md Diseña un nuevo barrio con cancha y taller
```

El agente **solo habla dentro de su disciplina**. Si la tarea cruza roles, invoca al Director Creativo primero.

## Routing — ¿Qué agente usar?

| Tarea | Agente |
|---|---|
| ¿Esta idea encaja en el juego? | `creative_director.md` |
| Color, composición, assets, iluminación | `art_director.md` |
| Barrio, POIs, layout, mapas | `world_designer.md` |
| Loops, diversión, balance, progresión | `game_designer.md` |
| Slots, stats, compatibilidades vehículo | `vehicle_designer.md` |
| Materiales, chapitas, craft, comercio | `economy_designer.md` |
| Circuitos, atajos, rivales, torneos | `race_designer.md` |
| Música, SFX, ambiente sonoro | `audio_director.md` |
| Bevy, Rust, ECS, performance | `technical_director.md` |
| QA visual, scoring, checklist | `qa_director.md` |

## Jerarquía

```
creative_director     ← Filtro de identidad + coherencia lore
        │
   ┌────┼────┬────────┬─────────┐
   │    │    │        │         │
  art world game   systems    tech
              │        │
         vehicle  economy
         race
              │
             qa
             audio
```

## Contexto automático por agente

Cada archivo `.md` incluye una sección **`READ FIRST`** con rutas exactas a leer antes de responder. No improvisar fuera de esos documentos.

## Otros directorios del estudio

| Carpeta | Propósito |
|---|---|
| [`docs/`](../docs/README.md) | Guías técnicas del juego (por dominio) |
| [`decisions/`](../decisions/README.md) | ADRs — por qué elegimos X |
| [`lore/`](../lore/README.md) | Coherencia del mundo (no historia larga) |

## Regla de oro

> Un agente **nunca** hace el trabajo de otro. Si necesitas código + arte, invoca dos agentes o el Director Técnico + Director de Arte por separado.
