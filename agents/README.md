# Estudio Virtual — Carreras de Barrio

**Punto de entrada:** [`studio_director.md`](./studio_director.md)

---

## Núcleo del estudio

```
Tú
 ↓
Studio Director        ← Orquesta
 ↓
Release Manager        ← Git, ramas, merge (ÚNICO con git)
 ↓
Especialistas → QA
 ↓
Merge → develop → release/* → main
```

---

## Invocación

```bash
python scripts/studio_scan.py
```

```
@agents/studio_director.md Agregar garage
@agents/release_manager.md Crear rama feature/bevy-scaffold
```

---

## Agentes

| Agente | Rol |
|---|---|
| [**studio_director**](./studio_director.md) | Orquestador — asigna, prioriza |
| [**release_manager**](./release_manager.md) | **Git exclusivo** — ramas, merge, tags |
| [creative_director](./creative_director.md) | ADN, filtro |
| [art_director](./art_director.md) | Visual |
| [world_designer](./world_designer.md) | Barrios |
| [game_designer](./game_designer.md) | Gameplay |
| [vehicle_designer](./vehicle_designer.md) | Vehículo sistemas |
| [economy_designer](./economy_designer.md) | Economía |
| [race_designer](./race_designer.md) | Carreras |
| [audio_director](./audio_director.md) | Audio |
| [technical_director](./technical_director.md) | Bevy/Rust |
| [qa_director](./qa_director.md) | QA |

---

## Infraestructura

| Carpeta | Propósito |
|---|---|
| [docs/production/GITFLOW_GUIDE.md](../docs/production/GITFLOW_GUIDE.md) | **Norma Git del estudio** |
| [production/branches/](../production/branches/README.md) | Registry de ramas |
| [features/](../features/README.md) | Features + STATUS/TASKS/QA |
| [roadmap/](../roadmap/README.md) | MVP + Sprints |
| [metrics/](../metrics/README.md) | Estado del repo |

---

## Reglas

- **POL-001:** Nunca trabajar en `main`
- **POL-002:** Toda feature = rama propia
- **GIT-001:** Ninguna tarea sin Release Manager
- Especialistas **nunca** ejecutan git
