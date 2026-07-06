# Estudio Virtual — Carreras de Barrio

**Punto de entrada:** [`studio_director.md`](./studio_director.md)

---

## Núcleo

```
Tú → Studio Director → Release Manager → Build/Tech/Tools → Especialistas → QA → Merge
```

**Regla:** Cada sprint termina con `cargo run` + avance visible.

---

## Agentes — núcleo técnico

| Agente | Rol |
|---|---|
| [studio_director](./studio_director.md) | Orquestador |
| [release_manager](./release_manager.md) | Git exclusivo |
| [build_engineer](./build_engineer.md) | **Cargo, CI, lints, Bevy version** |
| [technical_director](./technical_director.md) | Arquitectura ECS, runtime |
| [tools_engineer](./tools_engineer.md) | **Herramientas `tools/`** |

## Agentes — diseño y contenido

| Agente | Rol |
|---|---|
| [creative_director](./creative_director.md) | ADN |
| [art_director](./art_director.md) | Visual |
| [world_designer](./world_designer.md) | Barrios |
| [game_designer](./game_designer.md) | Gameplay |
| [vehicle_designer](./vehicle_designer.md) | Vehículo |
| [economy_designer](./economy_designer.md) | Economía |
| [race_designer](./race_designer.md) | Carreras |
| [audio_director](./audio_director.md) | Audio |
| [qa_director](./qa_director.md) | QA |

---

## Infraestructura

| Carpeta | Propósito |
|---|---|
| [tools/](../tools/README.md) | Herramientas internas |
| [BEVY_ARCHITECTURE.md](../docs/systems/BEVY_ARCHITECTURE.md) | **Constitución Bevy (gate Sprint 01)** ✅ |
| [features/foundation-runtime](../features/foundation-runtime/) | Sprint 01 |
| [metrics/studio_health.json](../metrics/studio_health.json) | Salud del estudio |
| [roadmap/Sprint_01.md](../roadmap/Sprint_01.md) | Foundation Runtime DoD |

---

## Studio Health

`python scripts/studio_scan.py` → `metrics/studio_health.json`

Prioridad automática: 🔴 Runtime → Sprint 01.
