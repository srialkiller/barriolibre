# Carreras de Barrio — Documentación del Proyecto

**Motor:** Rust + Bevy Engine  
**Género:** Carreras infantiles 2.5D isométricas en barrio latinoamericano  
**Pipeline de assets:** Agent Sprite Forge

---

## Norte del proyecto

Antes de cualquier decisión de diseño, leer **[GAME_IDENTITY.md](./GAME_IDENTITY.md)** — el ADN del juego.

```
GAME_IDENTITY.md     ← ¿Por qué existe este juego? (filtro de ideas)
GAME_ART_BIBLE.md    ← Constitución artística y de producción
```

Si una idea no refuerza la identidad → probablemente no pertenece al juego.

---

## Estructura por disciplinas — 3 equipos

El proyecto se organiza por **disciplinas**, no por cantidad de documentos.

```
                    ┌─────────────────────┐
                    │   GAME_IDENTITY     │  ← ADN gameplay (norte)
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
       ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
       │  EQUIPO 1   │  │  EQUIPO 2   │  │  EQUIPO 3   │
       │    ART      │  │   WORLD     │  │  GAMEPLAY   │
       │  ✅ Listo   │  │ 🟡 Casi     │  │ 🔴 En curso │
       └─────────────┘  └─────────────┘  └─────────────┘
```

---

### Equipo 1 — ART ✅ Terminado

**Misión:** Definir cómo se ve el juego y validar cada asset.

| Documento | Rol |
|---|---|
| [GAME_ART_BIBLE.md](./GAME_ART_BIBLE.md) | Constitución, invariantes, protocolo pre-generación |
| [ART_STYLE_GUIDE.md](./ART_STYLE_GUIDE.md) | Cámara, luz, escala, paleta, materiales |
| [VISUAL_LANGUAGE.md](./VISUAL_LANGUAGE.md) | Formas, siluetas, composición, reciclado creativo |
| [ASSET_PIPELINE.md](./ASSET_PIPELINE.md) | Nombres, carpetas, pivotes, flujos, Bevy |
| [ASSET_REVIEW_GUIDE.md](./ASSET_REVIEW_GUIDE.md) | QA visual, scoring, familias de assets |

---

### Equipo 2 — WORLD 🟡 Casi terminado

**Misión:** Definir cómo se construyen los barrios jugables.

| Documento | Rol |
|---|---|
| [NEIGHBORHOOD_DESIGN_GUIDE.md](./NEIGHBORHOOD_DESIGN_GUIDE.md) | Anatomía del barrio, POIs, calles, topografía |

**Pendiente:** primer barrio jugable, tutorial map, circuito 1 (Fase Mundos).

---

### Equipo 3 — GAMEPLAY 🔴 En construcción

**Misión:** Definir la experiencia jugable — loops, sistemas, economía, progresión.

| Documento | Rol | Estado |
|---|---|---|
| [GAME_IDENTITY.md](./GAME_IDENTITY.md) | ADN, pilares, filtro de decisiones | ✅ |
| [GAMEPLAY_GUIDE.md](./GAMEPLAY_GUIDE.md) | Core/Micro/Race loops, controles, ECS | ✅ |
| [VEHICLE_DESIGN_GUIDE.md](./VEHICLE_DESIGN_GUIDE.md) | Slots, stats, compatibilidades (sistemas) | ✅ |
| [ECONOMY_GUIDE.md](./ECONOMY_GUIDE.md) | Materiales, chapitas, craft, comercio | ✅ |
| [RACE_DESIGN_GUIDE.md](./RACE_DESIGN_GUIDE.md) | Circuitos, atajos, rivales, FX | ✅ |
| [CLAN_SYSTEM_GUIDE.md](./CLAN_SYSTEM_GUIDE.md) | Clanes, eventos, economía cooperativa | ✅ |
| [PROGRESSION_GUIDE.md](./PROGRESSION_GUIDE.md) | Desbloqueos, curva, metas largas | ✅ |

> **Nota:** GAMEPLAY_GUIDE ≠ GDD. Las guías definen reglas y loops; el GDD (futuro) integrará todo en visión de producto.

---

## Roadmap por fases

### FASE PREPRODUCCIÓN — casi terminada

| Entregable | Estado |
|---|---|
| Art Style | ✅ |
| Visual Language | ✅ |
| Asset Pipeline | ✅ |
| Asset QA | ✅ |
| Neighborhood Design | ✅ |

### FASE GAME DESIGN — en curso

| Documento | Estado |
|---|---|
| GAME_IDENTITY | ✅ |
| GAMEPLAY_GUIDE | ✅ |
| VEHICLE_DESIGN_GUIDE | ✅ |
| ECONOMY_GUIDE | ✅ |
| RACE_DESIGN_GUIDE | ✅ |
| CLAN_SYSTEM_GUIDE | ✅ |
| PROGRESSION_GUIDE | ✅ |

### FASE PRODUCCIÓN — pausada

Producción de assets **detenida temporalmente** hasta consolidar game design.

| Pack | Estado |
|---|---|
| Environment Base (tiles) | ✅ 155/155 |
| Props Pack | ⬜ |
| Garage Pack | ⬜ |
| Building Pack | ⬜ |
| Character Pack | ⬜ |
| Vehicle Parts Pack | ⬜ |
| Effects Pack | ⬜ |

### FASE MUNDOS — futuro

| Entregable | Estado |
|---|---|
| generate2dmap | ⬜ |
| Primer barrio jugable | ⬜ |
| Tutorial | ⬜ |
| Circuito 1 | ⬜ |

---

## Flujo entre disciplinas

```
WORLD      →  define POIs, calles, layout del barrio
ART        →  valida assets con ASSET_REVIEW (cuando se produzca)
GAMEPLAY   →  define loops, sistemas, economía, progresión
             ↓
         Integración Bevy (futuro)
```

## Lectura obligatoria por tarea

| Tarea | Documentos mínimos |
|---|---|
| Evaluar una idea nueva | **GAME_IDENTITY** |
| Generar cualquier asset | GAME_ART_BIBLE + ART_STYLE + VISUAL_LANGUAGE + ASSET_PIPELINE |
| Aprobar/rechazar asset | ASSET_REVIEW_GUIDE + ART_STYLE_GUIDE |
| Diseñar un barrio | NEIGHBORHOOD_DESIGN + GAME_IDENTITY |
| Diseñar una carrera | RACE_DESIGN + GAMEPLAY + GAME_IDENTITY |
| Diseñar sistema vehículo | VEHICLE_DESIGN + ECONOMY + GAME_IDENTITY |
| Balancear recompensas | ECONOMY + PROGRESSION + GAMEPLAY |
| Mecánica de clan | CLAN_SYSTEM + ECONOMY + GAME_IDENTITY |

## Precedencia de documentos

```
GAME_IDENTITY   >  GAME_ART_BIBLE  >  guía de disciplina  >  prompt  >  criterio agente
```

Si hay conflicto → **detenerse y preguntar**. No improvisar.

## Historial

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-07-06 | Estructura de 5 equipos, reorganización en `/docs` |
| 2.0 | 2026-07-06 | Reorganización a 3 disciplinas; GAME_IDENTITY como norte; Fase Game Design completa |
