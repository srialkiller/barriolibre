# Knowledge Base — BarrioLibre Studio OS

**Status:** 📋 Planificado — migración post-Milestone 0 (Vertical Slice)  
**Curator futuro:** `agents/knowledge_curator.md` (post-M3)

---

## Por qué

Las IA aprenden mejor con conocimiento **separado por tipo**:

| Archivo | Contenido |
|---|---|
| `principles.md` | Por qué existe, filosofía |
| `rules.md` | Reglas duras, IDs (BA-001, POL-001) |
| `patterns.md` | Cómo hacer X correctamente |
| `examples.md` | Casos concretos |
| `anti_patterns.md` | Qué NO hacer |

Un Markdown monolítico mezcla todo → peor retrieval.

---

## Estructura target

```
knowledge/
├── art/
├── systems/
├── world/
├── production/
├── design/
├── lore/
└── architecture/
```

Cada dominio: `README.md` + principles · rules · patterns · examples · anti_patterns

---

## Migración (no ejecutar aún)

| Actual | Target |
|---|---|
| `docs/art/` | `knowledge/art/` |
| `docs/systems/` | `knowledge/systems/` + `knowledge/architecture/` |
| `docs/game/` | `knowledge/design/` |
| `docs/world/` | `knowledge/world/` |
| `docs/production/` | `knowledge/production/` |
| `lore/` | `knowledge/lore/` |
| `docs/systems/BEVY_ARCHITECTURE.md` | `knowledge/architecture/bevy/` |

**Durante M0:** seguir usando `docs/` — symlinks o redirects al migrar.

---

## Knowledge Curator (futuro)

Misiones:
- Detectar duplicados y contradicciones
- Proponer refactors de KB
- Actualizar referencias cruzadas
- Marcar obsoletos

Invocar post-Vertical Slice.
