# Phase: Vertical Slice

**Status:** 🔴 **FASE ACTUAL**

## Objetivo único

**15 minutos de juego continuo** — juego completo en versión mínima.

Ver [roadmap/MVP.md](../../roadmap/MVP.md).

---

## Flujo target

```
Menú → Barrio → Caminar → Recoger → Garaje → Construir
    → Carrera → Recompensas → Mejorar pieza → Guardar → Menú
```

---

## Regla estricta del estudio

> **Si un sprint no acerca al flujo de 15 min, no es prioritario.**

> **Cada sprint termina con `cargo run` + avance visible.**

---

## Sprints → Vertical Slice

| Sprint | Nombre | Avance visible |
|---|---|---|
| **01** | **Foundation Runtime** | `cargo run` → barrio renderizado |
| 02 | Player & Exploration | Caminar + recoger pickups |
| 03 | Craft, Garage, Race | Loop core jugable |
| 04 | Save + Menu polish | Flujo 15 min cerrado |

---

## Sprint 01 actual

**Branch:** `feature/bevy-foundation-runtime`  
**Feature:** [features/foundation-runtime](../../features/foundation-runtime/)

No es "scaffold" — es **runtime completo** (ECS, assets, render, map JSON).

---

## Features congeladas

- clans, events → alpha
- Brand → post-prototipo (ADR-005)

---

## Agentes

Studio Director → Release Manager → Build Engineer + Technical Director + Tools Engineer → QA
