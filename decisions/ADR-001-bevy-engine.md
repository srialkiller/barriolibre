# ADR-001: Motor Bevy (Rust)

**Status:** Accepted  
**Date:** 2026-07-06  
**Deciders:** Technical Director, Creative Director

---

## Context

Necesitamos un motor para un juego 2.5D isométrico con:

- ECS para entidades modulares (vehículos ensamblados, POIs, pickups)
- Performance en hardware modesto (público infantil/familiar)
- Control total del pipeline de assets
- Desarrollo sostenible por un equipo pequeño o solo dev

Alternativas evaluadas: Unity, Godot, custom engine, Bevy.

## Decision

Usar **Rust + Bevy Engine** como stack principal.

## Rationale

| Criterio | Bevy |
|---|---|
| ECS nativo | Sí — alinea con vehículos modulares y mundo POI-based |
| 2D/2.5D | Soporte sólido sprites + cámara isométrica |
| Performance | Rust sin GC; predecible para target modesto |
| Data-driven | JSON → Resources encaja con guías de sistemas |
| Licencia | MIT/Apache — sin royalties |
| Curva aprendizaje | Rust es dura; Bevy API evoluciona — aceptable para proyecto largo plazo |

## Consequences

**Positivas:**
- Arquitectura ECS desde día 1 (ver ADR-004)
- Un solo lenguaje para gameplay + tools
- Builds nativos Windows/Linux sin runtime pesado

**Negativas:**
- Ecosistema Bevy aún madurando (breaking changes entre versiones)
- Menos assets store que Unity/Godot
- Requiere Technical Director con perfil Rust

## Referencias

- `agents/technical_director.md`
- `docs/game/GAMEPLAY_GUIDE.md` § ECS
