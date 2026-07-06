# Production Phases — Ciclo de Vida del Proyecto

Organización por **fase de producción** — las prioridades cambian en cada etapa.

> **Nota:** `docs/production/` = documentación del pipeline de assets.  
> **`production/`** (esta carpeta) = fases del ciclo de vida del juego.

## Fases

| Fase | Carpeta | Objetivo | Status |
|---|---|---|---|
| Preproducción | [preproduction](./preproduction/README.md) | Docs, arte base, identidad | ✅ casi done |
| Vertical Slice | [vertical_slice](./vertical_slice/README.md) | **Un loop jugable completo** | 🔴 **ACTUAL** |
| Alpha | [alpha](./alpha/README.md) | Contenido core completo | ⬜ |
| Beta | [beta](./beta/README.md) | Balance, pulido, QA full | ⬜ |
| Release | [release](./release/README.md) | Ship Steam/itch | ⬜ |

## Fase actual

**`vertical_slice`** — detectada automáticamente por `studio_scan.py` (sin Cargo.toml aún).

## Exit criteria por fase

Ver README de cada subcarpeta.

## Studio Director

Al planificar sprints, leer fase actual y **solo priorizar work items válidos para esa fase**.
