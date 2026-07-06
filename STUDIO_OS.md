# BarrioLibre Studio OS

**Game Development OS** — el estudio es el producto principal; el juego es una aplicación que corre sobre él.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    APPLICATIONS                          │
│              Carreras de Barrio (v1)                     │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                      WORKERS                             │
│  Technical · Gameplay · Art · World · Audio              │
│  Economy · Vehicle · Race · Build · Tools                │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                     SERVICES                             │
│  Release Manager · Metrics · QA · Build · Roadmap        │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                      KERNEL                              │
│                 Studio Director                          │
└─────────────────────────────────────────────────────────┘
```

| Capa | Rol | Ubicación |
|---|---|---|
| **Kernel** | Orquestación, priorización, dependencias | `agents/studio_director.md` |
| **Services** | Git, métricas, QA gate, CI, sprints | `agents/release_manager.md`, `metrics/`, `roadmap/` |
| **Workers** | Especialistas por disciplina | `agents/*.md` |
| **Applications** | Productos que el estudio produce | Carreras de Barrio → `src/`, `features/` |

---

## Reglas del OS

1. **Cada sprint = entregable visible** — `cargo run` muestra progreso; no trabajo invisible
2. **Cada sprint = juego más jugable** que el anterior
3. **Feature = Plugin = Carpeta = Rama** — [BEVY_ARCHITECTURE.md](docs/systems/BEVY_ARCHITECTURE.md)
4. **Kernel decide; Services ejecutan políticas; Workers producen**
5. **Ningún Worker toca Git** — solo Release Manager (Service)

---

## Knowledge Base (evolución)

Migración futura de `docs/` → `knowledge/` con estructura:

```
knowledge/
├── art/          principles · rules · patterns · examples · anti_patterns
├── systems/
├── world/
├── production/
├── design/
├── lore/
└── architecture/
```

**Estado:** planificado post-Milestone 0.  
**Curator:** agente `knowledge_curator` — después del Vertical Slice.

Separar principios / reglas / ejemplos / anti-patrones mejora consumo por IA.

---

## Testing Pyramid (Sprint 02+)

```
Unit Tests
    ↓
System Tests
    ↓
Plugin Tests
    ↓
Gameplay Tests
    ↓
Golden Image Tests    ← mapas + sprite packs (anti-regresión IA)
```

Ver preview: [roadmap/Sprint_02_PREVIEW.md](roadmap/Sprint_02_PREVIEW.md)

---

## Milestones

| # | Nombre | Criterio |
|---|---|---|
| **M0** | Foundation Runtime | `cargo run` → barrio + overlay |
| M1 | Player & Exploration | Caminar + recoger |
| M2 | Core Loop | Craft + garage + carrera |
| M3 | Vertical Slice | 15 min flujo completo |

Ver [milestones/](milestones/README.md)

---

## Invocación

```
@agents/studio_director.md <tarea>
```

El Kernel lee: `metrics/studio_health.json`, `BEVY_ARCHITECTURE.md`, dependencias §10.
