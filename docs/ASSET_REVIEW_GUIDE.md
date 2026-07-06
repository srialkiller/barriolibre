# ASSET_REVIEW_GUIDE.md
## Carreras de Barrio — Guía de Revisión y Calidad de Assets

**Equipo:** ART (Equipo 1) + PRODUCTION (Equipo 2)  
**Complementa:** [ART_STYLE_GUIDE.md](./ART_STYLE_GUIDE.md), [VISUAL_LANGUAGE.md](./VISUAL_LANGUAGE.md), [ASSET_PIPELINE.md](./ASSET_PIPELINE.md)  
**Versión:** 1.0  
**Estado:** Obligatorio antes de marcar cualquier asset como `qc_pass` o `integrated`

---

> Ningún asset entra al juego sin pasar por esta guía. La revisión es **objetiva**: checklist + score. Un REJECT no es negociable sin regeneración o excepción documentada en GAME_ART_BIBLE.

---

## Tabla de contenidos

1. [Checklist universal de aprobación](#1-checklist-universal-de-aprobación)
2. [Sistema QUALITY_SCORE](#2-sistema-quality_score)
3. [Flujo de revisión](#3-flujo-de-revisión)
4. [Familia ROAD (calles)](#4-familia-road-calles)
5. [Otras familias de assets](#5-otras-familias-de-assets)
6. [Artefactos de IA — detección y rechazo](#6-artefactos-de-ia--detección-y-rechazo)
7. [Registro de revisión](#7-registro-de-revisión)
8. [GLOBAL REVIEW RULES](#8-global-review-rules)

---

## 1. Checklist universal de aprobación

Todo asset — tile, prop, pieza modular, personaje, FX — debe pasar **los 10 criterios**. Un solo fallo en criterio crítico → **REJECT** automático.

| # | Criterio | Crítico | Fuente | Cómo verificar |
|---|---|:---:|---|---|
| □ 1 | **Cámara correcta** | ✅ | ART_STYLE §2 | Isométrica 2:1, 30° elevación, azimut NE, dirección SE default |
| □ 2 | **Escala correcta** | ✅ | ART_STYLE §4 | Coherente con referencia niño 1.0 u; tile 256×128 px |
| □ 3 | **Colores correctos** | ✅ | ART_STYLE §5 | Paleta oficial; ±15% luminosidad; sin blanco/negro puro |
| □ 4 | **Pivote correcto** | ✅ | ASSET_PIPELINE §5 | Según categoría; documentado en `.meta.json` |
| □ 5 | **Tileable** | ⚠️ | ASSET_PIPELINE §6 | Bordes alinean con tiles adyacentes del mismo tipo (tiles only) |
| □ 6 | **Sin artefactos IA** | ✅ | §6 abajo | Sin texto fantasma, duplicados, blur, halos, deformaciones |
| □ 7 | **Sombras correctas** | ✅ | ART_STYLE §3 | Luz NE 55°; sombras SW 35% `#3A3A5C` |
| □ 8 | **Outline correcto** | ⚠️ | ART_STYLE §7.3 | 2 px personajes/vehículos; 1.5 px edificios; **ninguno** en tiles terreno |
| □ 9 | **Consistencia con pack** | ✅ | Manifest del pack | Mismo estilo, escala y técnica que assets del mismo pack |
| □ 10 | **Consistencia con barrio** | ✅ | NEIGHBORHOOD_DESIGN | Limpio, cuidado, latinoamericano, infantil — nunca sucio/postapocalíptico |

**Leyenda:** ✅ = fallo → REJECT automático. ⚠️ = fallo → máximo score **C**; regenerar si el asset es de producción.

### 1.1 Regla de aprobación mínima

| Score | Checklist |
|---|---|
| **A** | 10/10 ✅ |
| **B** | 9/10 (solo fallo en criterio ⚠️ no crítico) |
| **C** | 8/10 (aceptable solo como placeholder temporal — no integrar) |
| **REJECT** | ≤7/10 o cualquier fallo en criterio ✅ |

---

## 2. Sistema QUALITY_SCORE

### 2.1 Definición de scores

| Score | Nombre | Significado | Acción |
|---|---|---|---|
| **A** | Production-ready | Listo para shipping. Cumple 10/10. Referencia para futuros assets. | `status: qc_pass` → integrar |
| **B** | Production-acceptable | Usable en juego. Fallo menor no visible a escala de gameplay. | `status: qc_pass` → integrar |
| **C** | Work-in-progress | Visible en contexto pero no cumple estándar final. | `status: draft` — **no integrar** |
| **REJECT** | No usable | Fallo crítico o múltiples fallos. | Regenerar o descartar |

### 2.2 Matriz de scoring por categoría

| Categoría | A requiere | B tolera | REJECT si |
|---|---|---|---|
| **Tile terreno** | Tileable perfecto + colores exactos | Borde con gap ≤2 px corregible | No tileable, color fuera de paleta, texto visible |
| **Pieza modular** | Snap perfecto + escala ±0% | Snap offset ≤2 px | No encaja en 2+ chassis del tier |
| **Personaje** | Silueta test 50% + outline 2 px | Expresión levemente inconsistente | Proporciones fuera de VISUAL_LANGUAGE §3.1 |
| **Vehículo / pieza** | 4+ materiales visibles + reciclado limpio | 1 detalle de cinta ausente | Parece de fábrica o basura sucia |
| **Prop** | Escala + pivote + barrio coherente | Detalle menor en capa 10% | Escala rota respecto a referencia |
| **FX** | Legible a 25% + sin outline | 1 frame con borde touch | Ilegible en movimiento |

### 2.3 Regla de referencia A

Todo pack debe tener **al menos 1 asset score A** como referencia del pack:

| Pack | Referencia A actual |
|---|---|
| ENVIRONMENT_BASE_PACK_01 | `road_straight_h_01` (style anchor) |

Los assets nuevos se comparan side-by-side con la referencia A del pack antes de puntuar.

---

## 3. Flujo de revisión

```
Asset generado + postprocesado
        │
        ▼
┌───────────────────┐
│ Escena validación │  ← 8×8 grid con style anchor + contexto barrio
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Checklist 10/10   │
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ QUALITY_SCORE     │
└─────────┬─────────┘
          │
    ┌─────┴─────┬─────────┬─────────┐
    ▼           ▼         ▼         ▼
    A           B         C      REJECT
    │           │         │         │
    ▼           ▼         ▼         ▼
integrate   integrate   draft   regenerate
```

### 3.1 Escena de validación estándar

Componer antes de puntuar:

| Elemento | Asset de referencia |
|---|---|
| Tile calle | `road_straight_h_01` |
| Tile pasto | `grass_clean_01` |
| Tile vereda | `sidewalk_straight_01` |
| Style anchor | `road_straight_h_01` |
| Asset bajo revisión | centrado en cruce 4 vías |

**Test visual:** ¿El asset nuevo parece del mismo juego que los de referencia?

---

## 4. Familia ROAD (calles)

> Familia de mayor prioridad del proyecto. Define el vocabulario visual de circulación del barrio.

### 4.1 Taxonomía de asfalto (material)

Cada estado de asfalto es una **variante de material**, no un tipo de topología distinto. La topología (straight, corner, etc.) se combina con el estado.

| ID material | Nombre | Descripción visual | Paleta base | Estado en pack |
|---|---|---|---|---|
| `asphalt_new` | Asfalto nuevo | Superficie uniforme, poco desgaste, bordes limpios | `#6B6860` / `#858278` | ✅ `road_straight_h` (default) |
| `asphalt_old` | Asfalto viejo | Textura más marcada, color ligeramente apagado, desgaste sutil | `#6B6860` −10% sat | ✅ Variantes 02–03 |
| `asphalt_patched` | Asfalto parchado | Parches rectangulares gris claro `#858278` sobre base | Base + parches | ✅ `road_patched_*` |
| `asphalt_broken` | Asfalto roto | Grietas visibles, baches cartoon (no peligrosos) | Base + `#4A4840` cracks | ✅ `road_damaged_*` |
| `asphalt_wet` | Asfalto húmedo | Brillo suave, reflejo tenue, tono ligeramente más oscuro | Base −8% + highlight 15% | 🔜 Pack futuro |
| `asphalt_dusty` | Asfalto polvoriento | Capa clara de polvo `#988868` en bordes y surcos | Base + polvo en SW | 🔜 Pack futuro |

**Reglas de material:**
- Nunca barro, aceite negro, charcos sucios → prohibido (NEIGHBORHOOD_DESIGN + VISUAL_LANGUAGE §8).
- Asfalto roto = **cuidado municipal abandonado**, no abandono total.
- Asfalto húmedo/polvoriento = variante estacional/evento, no default.

### 4.2 Taxonomía de topología (forma)

| ID topología | Nombre | Conexiones | Assets en pack |
|---|---|---|---|
| `straight_h` | Recta horizontal | E ↔ W | `road_straight_h_*` |
| `straight_v` | Recta vertical | N ↔ S | `road_straight_v_*` |
| `corner_ne` | Esquina NE | N + E | `road_corner_ne_*` |
| `corner_nw` | Esquina NW | N + W | `road_corner_nw_*` |
| `corner_se` | Esquina SE | S + E | `road_corner_se_*` |
| `corner_sw` | Esquina SW | S + W | `road_corner_sw_*` |
| `cross` | Cruce | N + S + E + W | `road_cross_*` |
| `t_n` / `t_s` / `t_e` / `t_w` | T-junction | 3 vías | `road_tjunction_*` |
| `deadend` | Calle sin salida | 1 vía + tapón | `road_deadend_*` |
| `narrow` | Calle angosta | E ↔ W (60% ancho) | `road_narrow_*` |
| `wide` | Calle ancha | E ↔ W (140% ancho) | `road_wide_*` |

### 4.3 Matriz material × topología (naming futuro)

Convención propuesta para expansiones:

```
road_<topology>_<material>_<nn>
road_straight_h_asphalt_new_01
road_corner_ne_asphalt_patched_02
road_cross_asphalt_wet_01
```

Pack actual usa material implícito en el ID (`road_patched`, `road_damaged`). Migración a naming explícito en v2 del pack.

### 4.4 Checklist específico ROAD

Además del checklist universal:

| # | Criterio ROAD | A | REJECT si |
|---|---|---|---|
| R1 | Bordes de calzada alinean con mismo topology en los 4 lados | Exacto ±1 px | Gap >3 px visible en grilla |
| R2 | Dirección de desgaste coherente con tráfico (horizontal o vertical) | Sí | Desgaste perpendicular al flujo |
| R3 | Ancho de calzada consistente entre straight_h del mismo tier | ±5% | >15% diferencia vs anchor |
| R4 | Marcas viales (si overlay) no cruzan borde del tile | Centradas | Tocan borde o salen del diamante |
| R5 | Material legible a 50% zoom | Identificable | Confundible con tierra o concreto |

### 4.5 Ejemplos de scoring ROAD

| Asset | Score | Motivo |
|---|---|---|
| `road_straight_h_01` | **A** | Style anchor; referencia del pack |
| `road_straight_h_04` | **B** | Variante extra; textura ligeramente más ruidosa pero tileable |
| `road_damaged_01` | **B** | Grietas cartoon correctas; borde NE levemente irregular |
| Tile con texto "STOP" legible | **REJECT** | Artefacto IA + G-005 (no texto legible) |
| Tile con perspectiva convergente | **REJECT** | Fallo cámara crítico |

---

## 5. Otras familias de assets

### 5.1 Familia SIDEWALK (veredas)

| Material | ID | Paleta |
|---|---|---|
| Cemento limpio | `sidewalk_clean` | `#B8B0A4` |
| Cemento gastado | `sidewalk_worn` | `#B8B0A4` −10% |

**Topologías:** straight, corner, inner_corner, outer_corner, crossing, ramp.

**Criterio extra:** borde sur debe alinear con cordón si se coloca junto a `curb_straight`.

### 5.2 Familia CURB (cordones)

| Tipo | Uso |
|---|---|
| straight | Separador vereda–calzada |
| corner | Giro de cordón |
| ramp | Accesibilidad (bajada de cordón) |

**Criterio extra:** altura visual del cordón = ~0.05 u; no bloquear lectura de la calzada.

### 5.3 Familia TERRAIN (suelos)

| Material | IDs | Variantes |
|---|---|---|
| Pasto limpio | `grass_clean` | 5 |
| Pasto seco | `grass_dry` | 5 |
| Tierra compacta | `dirt_compact` | 5 |
| Tierra suelta | `dirt_soft` | 5 |
| Concreto limpio | `concrete_clean` | 5 |
| Concreto viejo | `concrete_old` | 5 |
| Ripio | `gravel` | 5 |

**Criterio extra:** fill tiles deben ser **100% tileables** en las 4 direcciones.

### 5.4 Familia MARKING (overlays)

| Tipo | Overlay | Notas |
|---|---|---|
| Infraestructura | manhole, storm_drain | Centrados o en borde sur |
| Daño | crack_small, crack_large | Sobre asfalto base |
| Reparación | repair_asphalt | Parche sobre asfalto |
| Señalética | paint_straight, paint_stop, paint_crosswalk, paint_arrow | **Sin texto legible** |

**Criterio extra:** son capas overlay — deben tener alpha y no incluir el asfalto base completo (salvo marking tiles standalone del pack).

### 5.5 Familia TRANSITION

| Par | Uso en barrio |
|---|---|
| road ↔ dirt | Borde de calle sin pavimentar |
| road ↔ grass | Calle junto a cantero |
| sidewalk ↔ grass | Vereda que termina en pasto |
| concrete ↔ grass/dirt | Plazoleta, cochera |
| grass ↔ dirt | Sitio eriazo, terreno mixto |

**Criterio extra:** línea de transición limpia en eje N–S del diamante; sin zigzag aleatorio.

### 5.6 Familias futuras (no en pack actual)

| Familia | Equipo responsable | Documento |
|---|---|---|
| BUILDING | ART + WORLD | NEIGHBORHOOD_DESIGN |
| VEHICLE_PART | SYSTEMS + ART | VEHICLE_DESIGN |
| CHARACTER | ART | VISUAL_LANGUAGE §3.1 |
| FX | GAME + ART | RACE_DESIGN |

---

## 6. Artefactos de IA — detección y rechazo

### 6.1 Lista de rechazo automático (REJECT)

| Artefacto | Descripción | Acción |
|---|---|---|
| **Texto fantasma** | Letras, números, palabras parcialmente formadas | REJECT + regenerar |
| **Simetría rota** | Mitades del tile no coherentes en tileable | REJECT |
| **Halo magenta** | Borde verde/magenta no removido en postproceso | Reprocesar; si persiste REJECT |
| **Blur / mush** | Textura sin bordes definidos, aspecto borroso | REJECT |
| **Duplicación** | Dos objetos idénticos en un tile single | REJECT |
| **Perspectiva mixta** | Caras con ángulos distintos en un solo tile | REJECT |
| **Objeto prohibido** | Casa, árbol, personaje, vehículo en tile terreno | REJECT |
| **Suciedad excesiva** | Manchas marrones, moho, basura | REJECT (VISUAL_LANGUAGE §8) |
| **Ruido fotográfico** | Grano, noise filter visible | REJECT |
| **Watermark / firma** | Cualquier marca de generador | REJECT |

### 6.2 Defectos corregibles (puede ser B)

| Defecto | Corrección |
|---|---|
| Halo magenta leve | Re-ejecutar chroma-key con threshold ajustado |
| Escala 5% menor | Reescalar con `process_environment_tile.py` |
| Variante muy similar a otra | Aceptable como B si cumple anti-repetición mínima |
| Borde tileable ±2 px | Aceptable B; anotar para normalización futura |

---

## 7. Registro de revisión

### 7.1 Campos en `.meta.json`

Añadir tras revisión:

```json
{
  "review": {
    "score": "A",
    "checklist_passed": 10,
    "reviewer": "agent|human",
    "date": "2026-07-06",
    "notes": "",
    "reference_compared": "road_straight_h_01"
  }
}
```

### 7.2 Registro de pack

Archivo: `data/tilesets/<pack>_review.json`

```json
{
  "pack_id": "environment_base_pack_01",
  "reviewed_at": "2026-07-06",
  "summary": { "A": 12, "B": 143, "C": 0, "REJECT": 0 },
  "style_anchor": "road_straight_h_01",
  "rejected": []
}
```

### 7.3 Política de integración Bevy

| Score | `status` en meta.json | ¿Cargar en runtime? |
|---|---|---|
| A | `integrated` | ✅ Sí |
| B | `qc_pass` → `integrated` | ✅ Sí |
| C | `draft` | ❌ No |
| REJECT | `rejected` | ❌ No — mover a `_rejected/` |

---

## 8. GLOBAL REVIEW RULES

| ID | Regla |
|---|---|
| **R-001** | Todo asset pasa checklist 10/10 antes de score. |
| **R-002** | Score **A** o **B** obligatorio para integración en Bevy. |
| **R-003** | Fallo en criterio crítico (✅) → **REJECT** automático. |
| **R-004** | Comparar siempre con style anchor del pack antes de puntuar. |
| **R-005** | Tiles terreno deben ser tileables — fallo → máximo **C**. |
| **R-006** | Texto legible en sprite → **REJECT** sin excepción. |
| **R-007** | Documentar score en `.meta.json` → `review`. |
| **R-008** | Pack no se marca completo hasta `summary.REJECT == 0` en producción. |
| **R-009** | Familia ROAD: material + topología deben ser identificables a 50% zoom. |
| **R-010** | Consistencia con barrio > detalle artístico (prioridad del estudio). |

---

## Apéndice A — Checklist imprimible

```
ASSET: _______________________  PACK: _______________________
REVISOR: ____________________  FECHA: ____________________

□ 1. Cámara correcta          □ 6. Sin artefactos IA
□ 2. Escala correcta          □ 7. Sombras correctas
□ 3. Colores correctos        □ 8. Outline correcto
□ 4. Pivote correcto          □ 9. Consistencia con pack
□ 5. Tileable                 □ 10. Consistencia con barrio

SCORE:  A / B / C / REJECT
NOTAS: ___________________________________________________
```

## Apéndice B — Historial

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-07-06 | Documento inicial — checklist, scoring, familia ROAD |

---

*Fin de ASSET_REVIEW_GUIDE.md*
