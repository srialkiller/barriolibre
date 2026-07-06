# Branch Registry — Registro de Ramas del Estudio

**Owner:** Release Manager  
**Formato:** JSON — una entrada por rama activa o histórica

## Uso

1. Release Manager **crea** entrada al abrir rama
2. Studio Director **lee** para orquestar
3. `studio_scan.py` incluye resumen en metrics

## Release activa

**`release/vertical-slice`** — MVP loop jugable

## Ramas planificadas (Sprint 01–03)

| Branch | Feature | Sprint | Status |
|---|---|---|---|
| `feature/bevy-scaffold` | bevy-scaffold | 01 | planned |
| `feature/environment-loader` | environment-loader | 01 | planned |
| `feature/player-controller` | player-controller | 02 | planned |
| `feature/inventory` | inventory | 02 | planned |
| `feature/crafting-system` | crafting | 03 | planned |
| `feature/garage` | garage | 03 | planned |
| `feature/race-ai` | race | 03 | planned |
| `feature/tutorial` | tutorial | 03 | planned |

## Archivo

Ver [`registry.json`](./registry.json) — fuente de verdad machine-readable.

## Estados válidos

`planned` · `draft` · `in_design` · `implementation` · `qa` · `ready_to_merge` · `merged` · `released` · `abandoned`

## Reglas

- GIT-001: ninguna rama activa sin entrada aquí
- Merge → actualizar `merged_to` + `merged_at`
- Abandon → status `abandoned` + reason en `notes`
