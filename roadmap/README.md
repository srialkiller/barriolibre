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

1. Cada sprint: 5–8 tasks, agente asignado, dependencias explícitas
2. Tasks propagadas a `features/*/tasks.md`
3. Post-sprint: `studio_scan.py` + update metrics
4. No incluir work de fase alpha mientras vertical_slice incompleto

## Historial

| Sprint | Fase | Focus | Status |
|---|---|---|---|
| 01 | vertical_slice | Bevy scaffold | ⬜ |
| 02 | vertical_slice | Map + pickup + inventory | ⬜ |
| 03 | vertical_slice | Craft + garage + race v0 | ⬜ |
