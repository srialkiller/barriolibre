# NEIGHBORHOOD_DESIGN_GUIDE.md
## Carreras de Barrio — Guía de Diseño de Barrios

**Equipo:** WORLD DESIGN (Equipo 3)  
**Complementa:** [ART_STYLE_GUIDE.md](../art/ART_STYLE_GUIDE.md), [ASSET_REVIEW_GUIDE.md](../art/ASSET_REVIEW_GUIDE.md), [RACE_DESIGN_GUIDE.md](../game/RACE_DESIGN_GUIDE.md)  
**Versión:** 1.0  
**Estado:** Obligatorio antes de diseñar cualquier mapa o layout de barrio

---

> Un barrio de **Carreras de Barrio** nunca es un grid perfecto. Es un lugar vivido, irregular, con historia — optimista, cuidado y lleno de rincones donde los niños compiten, construyen y juegan.

---

## Tabla de contenidos

1. [Filosofía del barrio](#1-filosofía-del-barrio)
2. [Anatomía obligatoria](#2-anatomía-obligatoria)
3. [Geometría de calles](#3-geometría-de-calles)
4. [Topografía](#4-topografía)
5. [Puntos de interés (POI)](#5-puntos-de-interés-poi)
6. [Barrios nunca perfectos](#6-barrios-nunca-perfectos)
7. [Plantillas de barrio](#7-plantillas-de-barrio)
8. [Integración con tiles y Bevy](#8-integración-con-tiles-y-bevy)
9. [GLOBAL NEIGHBORHOOD RULES](#9-global-neighborhood-rules)

---

## 1. Filosofía del barrio

### 1.1 Principios

| Principio | Significado |
|---|---|
| **Vivido, no diseñado** | Parece que la gente vive ahí — no un plano urbanístico |
| **Irregular pero legible** | El jugador siempre sabe dónde va, aunque el camino no sea recto |
| **Cuidado, no abandono** | Las calles tienen desgaste pero la comunidad cuida el espacio |
| **Infantil, no infantilizado** | Los niños son protagonistas; el barrio es su territorio de juego |
| **Latinoamericano, universal** | Reconocible regionalmente pero accesible globalmente |

### 1.2 Lo que transmite un buen barrio

- Los chicos **conocen cada atajo**.
- Hay un lugar donde **siempre se arman las carreras**.
- Existe un **taller o garaje** donde se construyen los vehículos.
- Hay **subidas y bajadas** que hacen interesante la carrera.
- Una **esquina peligrosa** (en tono cartoon) genera emoción sin violencia.

---

## 2. Anatomía obligatoria

Todo barrio jugable debe incluir **como mínimo 8 de los 11 elementos** de la lista canónica:

| # | Elemento | Función en gameplay | Prioridad |
|---|---|---|---|
| 1 | **Plaza** | Punto de encuentro, meta alternativa, hub social | Alta |
| 2 | **Cancha** | Zona de competencia, circuito cerrado natural | Alta |
| 3 | **Almacén / despensa** | POI de recursos, props de cajas/bidones | Media |
| 4 | **Taller / garaje** | Hub de construcción de vehículos | Alta |
| 5 | **Sitio eriazo** | Terreno mixto (tierra/pasto), atajos, construcción | Media |
| 6 | **Callejón** | Atajo estrecho (`road_narrow`), tensión de maniobra | Alta |
| 7 | **Subida** | Desafío de velocidad/pendiente (metadata `slope: up`) | Alta |
| 8 | **Bajada** | Aceleración, riesgo cartoon de perder control | Alta |
| 9 | **Esquina peligrosa** | Curva cerrada + posible `road_damaged` o estrecho | Alta |
| 10 | **Atajo** | Camino más corto pero más difícil (dirt vs asphalt) | Alta |
| 11 | **Calle sin salida** | `road_deadend` — callejón sin salida, exploración | Media |

### 2.1 Distribución recomendada por tamaño

| Tamaño barrio | Tiles aprox. | POIs mínimos | Calles |
|---|---|---|---|
| **Pequeño** | 16×16 | 6 de 11 | 1 circuito + 1 callejón |
| **Mediano** | 32×32 | 8 de 11 | 2 circuitos conectados + atajos |
| **Grande** | 48×48+ | 11 de 11 | Red completa con subidas/bajadas |

---

## 3. Geometría de calles

### 3.1 Regla de oro

> **Los barrios nunca son perfectamente rectos.**

| Permitido | Evitar |
|---|---|
| Curvas con `road_corner_*` cada 3–8 tiles | Avenidas rectas >12 tiles sin interrupción |
| T-junctions desalineadas | Grid manhattan perfecto 90° |
| Calles de ancho variable (`narrow` / `wide`) | Todas las calles mismo ancho |
| Dead ends que invitan exploración | Calles que no llevan a ningún POI |
| Transiciones road→dirt en bordes | Calles flotando sin vereda/cordón |

### 3.2 Capas de una calle (de sur a norte en isométrico)

```
┌─────────────────────────────────────┐
│  pasto / edificio (fondo)           │
├─────────────────────────────────────┤
│  vereda (sidewalk)                  │
├─────────────────────────────────────┤
│  cordón (curb)                      │
├─────────────────────────────────────┤
│  calzada (road)                     │
├─────────────────────────────────────┤
│  cordón                             │
├─────────────────────────────────────┤
│  vereda                             │
├─────────────────────────────────────┤
│  pasto / edificio                   │
└─────────────────────────────────────┘
```

Ancho típico en tiles: vereda(1) + cordón(0.5) + calzada(2–3) + cordón(0.5) + vereda(1) = **5–6 tiles** por calle completa.

### 3.3 Vocabulario topológico (tiles disponibles)

Usar la familia ROAD de [ASSET_REVIEW_GUIDE §4](../art/ASSET_REVIEW_GUIDE.md#4-familia-road-calles):

- **Rectas:** `road_straight_h`, `road_straight_v`
- **Curvas:** `road_corner_ne/nw/se/sw`
- **Cruces:** `road_cross`
- **T:** `road_tjunction_n/s/e/w`
- **Sin salida:** `road_deadend`
- **Variación:** `road_narrow`, `road_wide`, `road_damaged`, `road_patched`

---

## 4. Topografía

### 4.1 Subidas y bajadas

El barrio no es plano. La topografía se expresa con:

| Mecanismo | Implementación |
|---|---|
| **Metadata de pendiente** | `"slope": "up" | "down" | "flat"` en tile/celda |
| **Transiciones visuales** | Cambio de material road→dirt en subidas empinadas |
| **Atajos por escalera/rampa** | `sidewalk_ramp` + metadata `shortcut: true` |
| **FX de polvo** | En bajadas largas (RACE_DESIGN) |

| Tipo | Longitud mínima | Longitud ideal | Gameplay |
|---|---|---|---|
| **Subida suave** | 3 tiles | 5–8 tiles | Reduce velocidad 10–15% |
| **Subida fuerte** | 5 tiles | 8–12 tiles | Reduce velocidad 20–30%; recompensa habilidad |
| **Bajada suave** | 3 tiles | 5–8 tiles | Aumenta velocidad 10–15% |
| **Bajada fuerte** | 5 tiles | 8–12 tiles | Aumenta velocidad 25–40%; riesgo de salirse |

### 4.2 Esquina peligrosa

Una esquina peligrosa combina **≥2** de:

- Curva cerrada (`road_corner` consecutivos)
- Calzada dañada (`road_damaged`)
- Calle angosta (`road_narrow`)
- Transición road→dirt sin vereda
- Marcador de pendiente en bajada entrando a curva

**Tono:** emocionante y cartoon — nunca fatal ni violento.

---

## 5. Puntos de interés (POI)

### 5.1 Ficha de POI

Cada POI se documenta en `<barrio>_pois.json`:

```json
{
  "id": "poi_plaza_central",
  "type": "plaza",
  "position": [16, 14],
  "size_tiles": [4, 4],
  "gameplay_role": "hub|start|finish|shop|workshop",
  "props": ["prop_bench_01", "prop_fountain_01"],
  "race_hooks": ["spawn_ring", "checkpoint_1"]
}
```

### 5.2 POI canónicos

#### Plaza
- **Superficie:** `concrete_clean` o `concrete_old`
- **Ubicación:** Centro del barrio o cruce de 3+ calles
- **Gameplay:** Hub, punto de partida, meta de carrera casual
- **Props:** bancos, macetas, mural (sin texto legible)

#### Cancha
- **Superficie:** `concrete_clean` delimitada por `curb_*`
- **Forma:** Rectángulo o trapecio irregular — nunca perfecto
- **Gameplay:** Circuito cerrado natural; ideal para tutoriales
- **Props:** arcos improvisados, líneas `marking_paint_*`

#### Almacén / despensa
- **Superficie:** `concrete` junto a `road_straight`
- **Gameplay:** Fuente de props reciclables (ECONOMY)
- **Props:** cajas apiladas, bidones, carretilla

#### Taller / garaje
- **Superficie:** `concrete_old` + `road_deadend` o callejón
- **Gameplay:** Hub de construcción de vehículos (VEHICLE_DESIGN)
- **Props:** herramientas, neumáticos, chassis en progreso
- **Metadata:** `scene_hook: vehicle_workshop`

#### Sitio eriazo
- **Superficie:** `dirt_soft`, `grass_dry`, `transition_grass_dirt`
- **Gameplay:** Atajo, zona de pruebas, terreno mixto
- **Sin edificios** — terreno abierto con props dispersos

#### Callejón
- **Tiles:** `road_narrow` × 3–6 + `road_deadend` opcional
- **Flanqueado por:** edificios (props altos) cuando existan
- **Gameplay:** Atajo de alto riesgo / baja visibilidad

---

## 6. Barrios nunca perfectos

### 6.1 Técnicas de irregularidad

| Técnica | Ejemplo |
|---|---|
| **Quiebre de eje** | Calle va recta 5 tiles → T-junction → cambia dirección 30° |
| **Ancho variable** | Avenida `road_wide` → estrecha a `road_narrow` en callejón |
| **Material mixto** | `road_patched` junto a `road_damaged` — historia de reparaciones |
| **Vereda interrumpida** | `transition_sidewalk_grass` donde la vereda se corta |
| **Calle sin terminar** | `road_deadend` en sitio eriazo — urbanización incompleta |
| **Plaza descentrada** | Plaza no en el centro geométrico del mapa |
| **Asimetría de POIs** | Taller en un extremo, cancha en otro — el barrio tiene flujo |

### 6.2 Anti-patrones (prohibidos)

| Anti-patrón | Por qué |
|---|---|
| Grid simétrico espejo | Parece nivel de puzzle, no barrio |
| Todas las calles mismo ancho y material | Monótono; no hay jerarquía |
| POIs equidistantes en patrón | Artificial |
| Sin dead ends ni callejones | No hay exploración ni atajos |
| Barrio 100% asfalto | No hay terreno mixto ni sitios eriazo |
| Calles que no conectan POIs | Callejones sin propósito |

### 6.3 Regla de los 3 caminos

Entre cualquier dos POIs importantes debe haber **al menos 3 rutas** con características distintas:

1. **Ruta segura** — calles anchas, asfalto bueno, más larga
2. **Ruta rápida** — atajo por eriazo o callejón, más difícil
3. **Ruta técnica** — subida/bajada + esquina peligrosa, recompensa skill

---

## 7. Plantillas de barrio

### 7.1 Barrio Residencial (template)

```
POIs: plaza + cancha + 2 casas + sitio eriazo
Calles: 1 loop principal irregular + 1 callejón + 1 dead end
Topografía: 1 subida suave + 1 bajada
Atajo: eriazo conecta cancha ↔ plaza
```

### 7.2 Barrio Industrial (template)

```
POIs: taller + almacén + sitio eriazo + cancha improvisada
Calles: T-junctions + calle angosta entre galpones
Topografía: plano con 1 bajada hacia cancha
Material: más road_damaged y road_patched
```

### 7.3 Barrio Mixto (template — default)

```
POIs: todos los 11 elementos distribuidos
Calles: red orgánica con 2 plazas pequeñas
Topografía: subida fuerte en un extremo, bajada hacia cancha
Carrera: circuito principal + 2 atajos + esquina peligrosa
```

---

## 8. Integración con tiles y Bevy

### 8.1 Archivos por barrio

```
data/maps/<barrio_id>/
├── layout.json           ← grid de tile IDs
├── pois.json             ← puntos de interés
├── collision.json        ← geometría sólida
├── scene_hooks.json      ← spawns, checkpoints, meta
├── slopes.json           ← metadata de pendiente
└── shortcuts.json        ← atajos y rutas alternativas
```

### 8.2 Layout JSON (ejemplo)

```json
{
  "barrio_id": "barrio_norte",
  "size": [32, 32],
  "layers": {
    "ground": [
      ["grass_clean_01", "grass_clean_02", "..."],
      ["transition_road_grass_01", "road_straight_h_01", "..."]
    ],
    "markings": [],
    "overlay": []
  }
}
```

### 8.3 Validación de barrio

Antes de aprobar un layout:

- [ ] ≥8 de 11 elementos canónicos presentes
- [ ] Ninguna calle recta >12 tiles sin quiebre
- [ ] ≥3 rutas distintas entre POIs principales
- [ ] ≥1 subida y ≥1 bajada
- [ ] ≥1 callejón o atajo
- [ ] ≥1 esquina peligrosa
- [ ] Todos los tiles existen en manifest y score ≥ B
- [ ] Escena compuesta pasa revisión ASSET_REVIEW en contexto

---

## 9. GLOBAL NEIGHBORHOOD RULES

| ID | Regla |
|---|---|
| **N-001** | Todo barrio incluye ≥8 de 11 elementos canónicos. |
| **N-002** | Calles nunca perfectamente rectas >12 tiles seguidos. |
| **N-003** | Entre 2 POIs principales existen ≥3 rutas distintas. |
| **N-004** | Todo barrio tiene subida, bajada, callejón y atajo. |
| **N-005** | Sitio eriazo usa terreno mixto — nunca 100% asfalto. |
| **N-006** | Taller/garaje conectado a red de calles (no aislado). |
| **N-007** | Esquina peligrosa en tono cartoon — nunca violencia. |
| **N-008** | Layout documentado en JSON — nunca solo imagen baked. |
| **N-009** | Props separados del terreno base (foundation-only). |
| **N-010** | Barrio debe sentirse cuidado — no postapocalíptico ni sucio. |

---

## Apéndice A — Checklist de diseño de barrio

```
BARRIO: _______________________  TAMAÑO: _______ tiles

ANATOMÍA (mín. 8/11):
□ Plaza          □ Cancha         □ Almacén
□ Taller         □ Sitio eriazo   □ Callejón
□ Subida         □ Bajada         □ Esquina peligrosa
□ Atajo          □ Calle sin salida

GEOMETRÍA:
□ Sin calles rectas >12 tiles
□ Ancho variable (narrow/wide)
□ ≥3 rutas entre POIs principales

PRODUCCIÓN:
□ layout.json escrito
□ pois.json escrito
□ Todos los tiles score ≥ B
□ Escena QA compuesta
```

## Apéndice B — Historial

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-07-06 | Documento inicial — anatomía, POIs, irregularidad, plantillas |

---

*Fin de NEIGHBORHOOD_DESIGN_GUIDE.md*
