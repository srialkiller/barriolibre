# ADR-003: Sprites Prerenderizados vs Modelos 3D

**Status:** Accepted  
**Date:** 2026-07-06  
**Deciders:** Art Director, Technical Director, Creative Director

---

## Context

Necesitamos producir cientos de assets (tiles, props, piezas de vehículo, personajes) con un equipo artístico mínimo (IA + revisión humana).

Alternativas:

1. **3D real-time** — modelar, riggear, renderizar en engine
2. **Sprites prerenderizados** — generar 2D isométrico, integrar en Bevy
3. **Pixel art manual** — dibujo frame a frame

## Decision

**Sprites prerenderizados 2D isométricos**, generados vía pipeline AI (`generate2dsprite`, `generate2dmap`) + postproceso + QA.

Ensamblaje de vehículos en **runtime** desde piezas modulares — no sprites pre-compuestos de vehículo completo.

## Rationale

| Criterio | Sprites prerenderizados |
|---|---|
| Velocidad producción | Alto con Agent Sprite Forge |
| Consistencia | Style anchor + ASSET_REVIEW |
| Identidad | Look "cartoon latino" controlado por prompts |
| Vehículos modulares | Piezas separadas → ECS assembly |
| Hardware target | 2D ligero vs 3D draw calls |
| Equipo | 1 dev + agentes IA viable |

## Consequences

**Positivas:**
- ENVIRONMENT_BASE_PACK_01 completado (155 tiles)
- Modularidad vehículo coherente con GAME_IDENTITY
- Iteración rápida de arte con QA gate

**Negativas:**
- No hay rotación 360° de vehículos (sprites por dirección)
- Dependencia de pipeline AI + chroma key
- Muchos PNG en disco — requiere asset loading strategy (Technical Director)

## Referencias

- `docs/production/ASSET_PIPELINE.md`
- `docs/art/GAME_ART_BIBLE.md`
- `decisions/ADR-002-2.5d-isometric.md`
