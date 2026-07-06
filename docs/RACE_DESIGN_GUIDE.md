# RACE_DESIGN_GUIDE.md
## Carreras de Barrio — Guía de Diseño de Carreras

**Equipo:** GAMEPLAY (Equipo 3)  
**ADN:** [GAME_IDENTITY.md](./GAME_IDENTITY.md)  
**Complementa:** [NEIGHBORHOOD_DESIGN_GUIDE.md](./NEIGHBORHOOD_DESIGN_GUIDE.md), [GAMEPLAY_GUIDE.md](./GAMEPLAY_GUIDE.md), [VEHICLE_DESIGN_GUIDE.md](./VEHICLE_DESIGN_GUIDE.md), [PROGRESSION_GUIDE.md](./PROGRESSION_GUIDE.md)  
**Versión:** 2.0

---

## 0. Race Loop (contexto)

Este documento detalla la fase **Competir** del Core Loop. Ver [GAMEPLAY_GUIDE.md §4](./GAMEPLAY_GUIDE.md).

```
Preparación (build en taller, elegir circuito)
    ↓
Clasificación / calentamiento (opcional v1)
    ↓
Carrera (checkpoints, atajos, rivales)
    ↓
Premios (chapitas, materiales, blueprints)
    ↓
Reputación (barrio, rival, clan si aplica)
    ↓
Nuevos eventos desbloqueados (torneos, circuitos)
```

**Filtro identidad:** la carrera valida el **ingenio del build**, no la potencia de fábrica. Atajos premian conocer el barrio.

---

## 1. Filosofía de carrera

Las carreras ocurren **en el barrio**, no en pistas de fórmula. Un circuito es un recorrido por calles reales con atajos, subidas y esquinas peligrosas.

| Principio | Descripción |
|---|---|
| **Barrio como pista** | El layout del barrio define el circuito |
| **Rutas múltiples** | ≥3 caminos viables con trade-offs |
| **Riesgo/recompensa** | Atajos más difíciles pero más rápidos |
| **Duración ideal** | 90–150 segundos por carrera |
| **Tono cartoon** | Polvo, derrapes, emoción — sin violencia |

---

## 2. Tipos de carrera

| Tipo | Descripción | POI típico |
|---|---|---|
| **Circuito** | Laps en loop cerrado | Cancha, plaza |
| **Punto a punto** | Start → meta en barrio | Taller → plaza |
| **Eliminatoria suave** | Último en checkpoint elimina (cartoon) | Circuito largo |
| **Contrarreloj** | Solo vs tiempo | Cualquier ruta |
| **Desafío de piezas** | Solo vehículos con X pieza | Taller |

---

## 3. Anatomía de un circuito

### 3.1 Elementos obligatorios

| Elemento | Cantidad mínima | Metadata |
|---|---|---|
| **Línea de salida** | 1 | `scene_hook: race_start` |
| **Meta** | 1 | `scene_hook: race_finish` |
| **Checkpoints** | 3–8 por vuelta | `checkpoint_id`, `order` |
| **Sección técnica** | ≥1 | Esquina peligrosa o subida |
| **Sección rápida** | ≥1 | Bajada o recta `road_wide` |
| **Decisión de ruta** | ≥1 | Bifurcación con atajo |

### 3.2 Distribución de dificultad (curva)

```
Dificultad
    ▲
    │      ╭─╮           ╭──╮
    │    ╭─╯  ╰─╮     ╭─╯    ╰─╮
    │  ╭─╯        ╰───╯          ╰─
    │╭─╯
    └──────────────────────────────► Tiempo / % circuito
     Start    CP1    CP2    CP3   Finish
```

- **Inicio:** fácil (recta o curva suave)
- **Medio:** pico de dificultad (esquina + atajo)
- **Final:** emocionante pero justo

---

## 4. Superficies y gameplay

| Superficie tile | Efecto | Uso en diseño |
|---|---|---|
| `road_*` default | 100% grip | Línea racing principal |
| `road_damaged` | −5% grip, +FX | Zona técnica |
| `road_narrow` | Menos espacio | Callejón, atajo |
| `dirt_*` / `grass_*` | −15–25% speed | Atajo arriesgado |
| `transition_*` | Cambio gradual | Entrada/salida de atajo |

### Pendiente (metadata)

| `slope` | Efecto |
|---|---|
| `up` | −10–30% max speed según inclinación |
| `down` | +10–40% speed; riesgo de overshoot |
| `flat` | Normal |

---

## 5. Atajos

Todo circuito competitivo incluye **≥1 atajo** documentado en `shortcuts.json`:

```json
{
  "id": "shortcut_eriazo_plaza",
  "entry_checkpoint": "cp_2",
  "exit_checkpoint": "cp_4",
  "path_tiles": ["dirt_soft_01", "transition_grass_dirt_01"],
  "risk": "medium",
  "time_saved_sec": 3.5,
  "recommended_tier": "small"
}
```

| Riesgo | Características |
|---|---|
| **Low** | Tierra compacta, curva suave |
| **Medium** | Pasto + estrecho, sin baranda |
| **High** | Sin vereda, esquina + bajada |

---

## 6. Rivales (NPCs)

| Tipo | Comportamiento |
|---|---|
| **Rival amistoso** | Similar skill al jugador; errores cartoon |
| **Especialista curvas** | Fuerte en esquinas, débil en rectas |
| **Especialista rectas** | Motor large, mal en callejones |
| **Explorador** | Intenta atajos; a veces falla cómicamente |

- Rivales usan vehículos caseros con personalidad (VISUAL_LANGUAGE §7.3)
- Sin colisiones agresivas — bump cartoon, sin daño

---

## 7. FX de carrera

| FX | Trigger | Asset |
|---|---|---|
| Polvo | Tierra/pasto, derrape | `fx_dust_*` |
| Chispas cartoon | Golpe suave muro | `fx_spark_*` |
| Humo escape | Aceleración motor large | `fx_exhaust_*` |
| Confetti | Meta | `fx_confetti_*` |

---

## 8. Metadata de carrera

```json
{
  "race_id": "barrio_norte_circuito_01",
  "barrio_id": "barrio_norte",
  "type": "circuit",
  "laps": 3,
  "checkpoints": ["cp_1", "cp_2", "cp_3", "cp_4"],
  "start": { "position": [8, 12], "direction": "se" },
  "finish": { "position": [8, 12] },
  "shortcuts": ["shortcut_eriazo_plaza"],
  "recommended_duration_sec": 120
}
```

---

## 9. GLOBAL RACE RULES

| ID | Regla |
|---|---|
| **RC-001** | Toda carrera usa calles del barrio — no pistas abstractas. |
| **RC-002** | ≥3 checkpoints por vuelta en circuitos. |
| **RC-003** | ≥1 atajo documentado en carreras competitivas. |
| **RC-004** | Duración objetivo 90–150 s (ajustable por dificultad). |
| **RC-005** | Checkpoints y meta son metadata — no baked en tiles. |
| **RC-006** | Rivales nunca bloquean permanentemente al jugador. |
| **RC-007** | FX sin violencia, sangre ni humo negro tóxico. |
| **RC-008** | Premios alineados con ECONOMY_GUIDE — explorar sigue siendo viable. |
| **RC-009** | Builds small/medium/large tienen rutas viables (atajos documentados). |
| **RC-010** | Toda carrera pasa filtro GAME_IDENTITY §7 antes de implementarse. |

---

*Fin de RACE_DESIGN_GUIDE.md*
