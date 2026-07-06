# Metrics — Medición del Estudio

El estudio se mide. Sin métricas, el Studio Director planifica a ciegas.

## Regenerar

```bash
python scripts/studio_scan.py
```

Genera:
- `metrics/project_state.json` — machine-readable
- `metrics/dashboard.md` — human-readable

## Qué mide

| Categoría | Métricas |
|---|---|
| **Assets** | PNGs environment, vehicle parts, props, QA scored/rejected |
| **Code** | Rust files, Bevy project exists, maps |
| **World** | Neighborhoods, circuits, POIs |
| **Features** | Status per feature, open tasks |
| **Blockers** | Critical path impediments |
| **Docs** | Agents, ADRs, lore coverage |

## Uso por Studio Director

1. Ejecutar scan antes de planificar sprint
2. Leer `blockers[]` — priorizar P0
3. Comparar `features.*.open_tasks` vs sprint capacity
4. Post-sprint: re-scan, verificar delta

## Targets (vertical slice)

| Metric | Target |
|---|---|
| bevy_project | true |
| maps | ≥1 |
| circuits | ≥1 |
| MVP loop | completable |
| environment_complete | true ✅ |
| vehicle_parts | ≥3 (or placeholders) |

## Historial

Guardar snapshots opcionales en `metrics/history/YYYY-MM-DD.json` post-sprint.
