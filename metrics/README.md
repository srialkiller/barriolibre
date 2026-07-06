# Metrics

```bash
python scripts/studio_scan.py
```

Genera:
- `project_state.json` — estado del repo
- `studio_health.json` — **salud del estudio** (priorización automática)
- `dashboard.md` — vista humana

## Studio Health

| Métrica | Sprint 01 target |
|---|---|
| Documentación | 🟢 |
| Arte | 🟢 |
| **Runtime** | 🔴 → 🟢 (Foundation Runtime) |
| Gameplay | 🔴 |
| Herramientas | 🟡 |
| QA | 🟢/🟡 |
| Producción | 🟢 |
| Riesgo técnico | 🟡 → 🟢 |

Studio Director usa `studio_health` para decidir prioridades.
