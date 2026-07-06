# Carreras de Barrio

Videojuego de carreras infantiles en barrio latinoamericano.  
**Rust + Bevy** · 2.5D isométrico · Sprites prerenderizados.

> *No trata sobre autos. Trata sobre creatividad.*

---

## Punto de entrada — Studio Director

```
@agents/studio_director.md <tu tarea>
```

El Studio Director **no diseña** — orquesta especialistas, detecta bloqueos, genera sprints.

```bash
python scripts/studio_scan.py   # estado del proyecto
```

---

## Arquitectura del estudio

```
agents/           ← Equipo virtual (11 roles)
features/         ← Funcionalidades aisladas (garage, race, craft…)
roadmap/          ← MVP + Sprints (generados por IA)
metrics/          ← Medición del repo (project_state.json)
production/       ← Fases: preproduction → release
docs/             ← Guías por dominio (game, art, world, systems)
decisions/        ← ADRs
lore/             ← Coherencia del mundo
```

| Necesito… | Ir a… |
|---|---|
| Orquestar trabajo | [`agents/studio_director.md`](./agents/studio_director.md) |
| Estado del proyecto | [`metrics/dashboard.md`](./metrics/dashboard.md) |
| Qué hacer ahora | [`roadmap/Sprint_01.md`](./roadmap/Sprint_01.md) |
| MVP definition | [`roadmap/MVP.md`](./roadmap/MVP.md) |
| ADN del juego | [`docs/game/GAME_IDENTITY.md`](./docs/game/GAME_IDENTITY.md) |
| Feature garage | [`features/garage/`](./features/garage/README.md) |
| Fase actual | [`production/vertical_slice/`](./production/vertical_slice/README.md) |

---

## Fase actual: Vertical Slice

**Objetivo:** loop jugable MVP (explorar → recoger → craft → garage → carrera).

**Blocker #1:** No existe proyecto Bevy → Sprint 01.

Producción de assets **pausada** excepto placeholders MVP.

---

## Marca

ADR-005 **Proposed** — decisión post-prototipo jugable + circuito 1.

---

## Assets existentes

```
assets/environment/     ← 155/155 tiles ✅
data/tilesets/          ← Manifiestos JSON
scripts/                ← studio_scan.py + pipeline
```
