# Carreras de Barrio — Documentación

Guías técnicas del juego, organizadas por dominio para consumo automático por agentes.

**Estudio virtual:** [`../agents/`](../agents/README.md)  
**Decisiones:** [`../decisions/`](../decisions/README.md)  
**Lore:** [`../lore/`](../lore/README.md)

---

## Norte del proyecto

```
docs/game/GAME_IDENTITY.md    ← ADN — filtro de toda idea
docs/art/GAME_ART_BIBLE.md    ← Constitución artística
agents/creative_director.md   ← Evalúa coherencia antes de ejecutar
```

---

## Estructura

```
docs/
├── game/           ← Loops, identidad, carreras, clanes, progresión
├── art/            ← Estilo visual, QA, biblia de arte
├── world/          ← Barrios, POIs, layout
├── systems/        ← Vehículo (stats), economía
└── production/     ← Pipeline de assets, integración
```

---

## game/

| Documento | Rol |
|---|---|
| [GAME_IDENTITY.md](./game/GAME_IDENTITY.md) | ADN del juego |
| [GAMEPLAY_GUIDE.md](./game/GAMEPLAY_GUIDE.md) | Core/Micro/Race loops |
| [RACE_DESIGN_GUIDE.md](./game/RACE_DESIGN_GUIDE.md) | Circuitos, atajos, rivales |
| [CLAN_SYSTEM_GUIDE.md](./game/CLAN_SYSTEM_GUIDE.md) | Clanes cooperativos |
| [PROGRESSION_GUIDE.md](./game/PROGRESSION_GUIDE.md) | Desbloqueos, curva |

## art/

| Documento | Rol |
|---|---|
| [GAME_ART_BIBLE.md](./art/GAME_ART_BIBLE.md) | Constitución arte |
| [ART_STYLE_GUIDE.md](./art/ART_STYLE_GUIDE.md) | Cámara, paleta, luz |
| [VISUAL_LANGUAGE.md](./art/VISUAL_LANGUAGE.md) | Formas, siluetas |
| [ASSET_REVIEW_GUIDE.md](./art/ASSET_REVIEW_GUIDE.md) | QA visual, scoring |

## world/

| Documento | Rol |
|---|---|
| [NEIGHBORHOOD_DESIGN_GUIDE.md](./world/NEIGHBORHOOD_DESIGN_GUIDE.md) | Anatomía del barrio |

## systems/

| Documento | Rol |
|---|---|
| [VEHICLE_DESIGN_GUIDE.md](./systems/VEHICLE_DESIGN_GUIDE.md) | Slots, stats, compatibilidades |
| [ECONOMY_GUIDE.md](./systems/ECONOMY_GUIDE.md) | Materiales, chapitas, craft |

## production/

| Documento | Rol |
|---|---|
| [ASSET_PIPELINE.md](./production/ASSET_PIPELINE.md) | Naming, carpetas, Bevy |

---

## Routing: tarea → agente → docs

| Tarea | Agente | READ FIRST |
|---|---|---|
| ¿Idea encaja? | `agents/creative_director.md` | `game/GAME_IDENTITY` + `lore/` |
| Generar asset | `agents/art_director.md` | `art/GAME_ART_BIBLE` + `art/ART_STYLE` + `production/ASSET_PIPELINE` |
| QA asset | `agents/qa_director.md` | `art/ASSET_REVIEW` + pack manifest |
| Diseñar barrio | `agents/world_designer.md` | `world/NEIGHBORHOOD` + `lore/` |
| Balance gameplay | `agents/game_designer.md` | `game/GAME_IDENTITY` + `game/GAMEPLAY` |
| Stats vehículo | `agents/vehicle_designer.md` | `systems/VEHICLE_DESIGN` |
| Economía | `agents/economy_designer.md` | `systems/ECONOMY` |
| Circuito | `agents/race_designer.md` | `game/RACE_DESIGN` + `world/NEIGHBORHOOD` |
| Implementar | `agents/technical_director.md` | `decisions/` + `production/ASSET_PIPELINE` |

Para tareas multi-disciplina, el **Studio Director** orquesta primero:

```
@agents/studio_director.md <tarea>
```

Ver [`../agents/studio_director.md`](../agents/studio_director.md) · [`../features/`](../features/README.md) · [`../roadmap/`](../roadmap/README.md) · [`../metrics/`](../metrics/README.md)

---

## Precedencia

```
GAME_IDENTITY  >  GAME_ART_BIBLE  >  guía de dominio  >  ADR  >  agente  >  prompt
```

## Historial

| Versión | Cambios |
|---|---|
| 3.0 | Docs por dominio + agents |
| 3.1 | GitFlow + Release Manager + branch registry |

## Git del estudio

Ver [docs/production/GITFLOW_GUIDE.md](../docs/production/GITFLOW_GUIDE.md) — **POL-001: nunca trabajar en main.**

Sprint = feature branches dentro de `release/vertical-slice`.
