# Estudio Virtual — Carreras de Barrio

**Punto de entrada:** [`studio_director.md`](./studio_director.md) — orquesta todo el equipo.

---

## Flujo del estudio

```
Tú
 ↓
Studio Director        ← @agents/studio_director.md (SIEMPRE para tareas multi-rol)
 ↓
Creative Director      ← ¿Encaja en GAME_IDENTITY?
 ↓
Especialista(s)
 ↓
QA Director
 ↓
Technical Director     ← si hay implementación
 ↓
Resultado integrado
```

---

## Invocación

```bash
# Estado del proyecto
python scripts/studio_scan.py

# Orquestación
@agents/studio_director.md Crear un nuevo barrio
@agents/studio_director.md Generar Sprint 04
@agents/studio_director.md ¿Qué bloquea el MVP?
```

---

## Especialistas

| Agente | Rol |
|---|---|
| [**studio_director**](./studio_director.md) | **Orquestador — asigna, prioriza, integra** |
| [creative_director](./creative_director.md) | ADN, lore, filtro de ideas |
| [art_director](./art_director.md) | Color, composición, assets |
| [world_designer](./world_designer.md) | Barrios, POIs, mapas |
| [game_designer](./game_designer.md) | Diversión, balance, loops |
| [vehicle_designer](./vehicle_designer.md) | Slots, stats, compatibilidades |
| [economy_designer](./economy_designer.md) | Materiales, chapitas, craft |
| [race_designer](./race_designer.md) | Circuitos, atajos, torneos |
| [audio_director](./audio_director.md) | Música, SFX |
| [technical_director](./technical_director.md) | Bevy, Rust, ECS |
| [qa_director](./qa_director.md) | Scoring, checklists |

---

## Infraestructura del estudio

| Carpeta | Propósito |
|---|---|
| [`features/`](../features/README.md) | Funcionalidades aisladas (design, tasks, qa, ecs) |
| [`roadmap/`](../roadmap/README.md) | MVP + Sprints generados |
| [`metrics/`](../metrics/README.md) | Estado real del repo |
| [`production/`](../production/README.md) | Fases: preproduction → release |
| [`docs/`](../docs/README.md) | Guías por dominio |
| [`decisions/`](../decisions/README.md) | ADRs |
| [`lore/`](../lore/README.md) | Coherencia del mundo |

---

## Regla de oro

> Un especialista **nunca** hace el trabajo de otro.  
> El Studio Director **nunca** diseña ni codea — solo orquesta.
