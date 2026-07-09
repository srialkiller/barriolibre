# Roadmap — Backlog Inteligente

Sprints generados por **Studio Director** a partir del estado real del repo.

## Regenerar estado

```bash
python scripts/studio_scan.py
```

## Archivos

| Archivo | Contenido |
|---|---|
| [MVP.md](./MVP.md) | Definición del vertical slice jugable |
| [Sprint_01.md](./Sprint_01.md) | Bevy scaffold + infraestructura |
| [Sprint_02.md](./Sprint_02.md) | Mapa + micro loop + inventory |
| [Sprint_03.md](./Sprint_03.md) | Garage + craft + carrera tutorial |

## Generar Sprint N+1

```
@agents/studio_director.md Generar Sprint 04
```

Protocolo en [studio_director.md](../agents/studio_director.md) — Pipeline C.

## Reglas

1. Cada sprint mapea a **feature branches** en `release/vertical-slice`
2. Release Manager abre ramas antes de trabajo
3. Post-sprint: merge → `studio_scan.py`

## Git

Ver [GITFLOW_GUIDE](../docs/production/GITFLOW_GUIDE.md). Sprint 01 listo tras integración GitFlow ✅.

## Historial

| Sprint | Fase | Focus | Status |
|---|---|---|---|
| 01 | vertical_slice | Bevy scaffold | ✅ |
| 02 | vertical_slice | Map + pickup + inventory | 🔴 |
| 03 | vertical_slice | Craft + garage + race v0 | ⬜ |
