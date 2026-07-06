# Carreras de Barrio

Videojuego de carreras infantiles en barrio latinoamericano.  
**Rust + Bevy** · 2.5D isométrico · Sprites prerenderizados.

---

## Estudio virtual — flujo

```
Tú → Studio Director → Release Manager → Especialistas → QA → Merge
```

```
@agents/studio_director.md <tarea>
python scripts/studio_scan.py
```

| Doc | Rol |
|---|---|
| [GITFLOW_GUIDE](docs/production/GITFLOW_GUIDE.md) | **Norma Git del estudio** |
| [release_manager](agents/release_manager.md) | **Único agente con git** |
| [studio_director](agents/studio_director.md) | Orquestador |
| [branch registry](production/branches/registry.json) | Ramas planificadas |

---

## Fase: Vertical Slice

**Release branch:** `release/vertical-slice`  
**Sprint 01:** `feature/bevy-scaffold` + `feature/environment-loader`  
**Estado:** GitFlow integrado ✅ — listo para abrir ramas

---

## Estructura

```
agents/       release_manager + 11 especialistas
features/     README + STATUS + TASKS + QA + CHANGELOG + NOTES
production/   fases + branches/registry.json
roadmap/      MVP + Sprints (branch per task)
metrics/      project_state.json
docs/         guías por dominio
```

---

## Blocker actual

**B-001** — Sin `Cargo.toml`. Resolver en `feature/bevy-scaffold` (Sprint 01).

**ADR-005** — Proposed. Naming post-prototipo.
