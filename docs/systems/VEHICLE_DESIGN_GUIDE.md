# VEHICLE_DESIGN_GUIDE.md
## Carreras de Barrio — Guía de Sistemas de Vehículo

**Equipo:** GAMEPLAY (Equipo 3) — sistemas, no arte  
**ADN:** [GAME_IDENTITY.md](../game/GAME_IDENTITY.md)  
**Arte visual de piezas:** [VISUAL_LANGUAGE.md](../art/VISUAL_LANGUAGE.md) + [ASSET_PIPELINE.md](../production/ASSET_PIPELINE.md)  
**Versión:** 2.0

---

> Este documento define **cómo funciona** el vehículo como sistema: slots, stats, compatibilidades, peso, craft. No define siluetas ni prompts — eso es Equipo ART.

---

## Tabla de contenidos

1. [Filosofía de sistema](#1-filosofía-de-sistema)
2. [Slots del vehículo](#2-slots-del-vehículo)
3. [Piezas por slot](#3-piezas-por-slot)
4. [Compatibilidades](#4-compatibilidades)
5. [Stats y fórmulas](#5-stats-y-fórmulas)
6. [Tiers](#6-tiers)
7. [Craft y desmontaje](#7-craft-y-desmontaje)
8. [Builds y presets](#8-builds-y-presets)
9. [Bevy ECS](#9-bevy-ecs)
10. [GLOBAL VEHICLE SYSTEM RULES](#10-global-vehicle-system-rules)

---

## 1. Filosofía de sistema

El vehículo es la **herramienta de expresión del ingenio del jugador** (GAME_IDENTITY §4).

| Regla | Implicación de sistema |
|---|---|
| Todo slot importa | Ninguna pieza es puramente cosmética |
| Compatibilidad lógica | Motor pequeño no va en chasis pesado sin penalización |
| Trade-offs claros | Más velocidad = menos agarre; más peso = peor aceleración |
| Builds diversos | No hay "meta único" obligatorio por tier |
| Construcción incremental | Empezar con 2–3 slots; desbloquear más con progresión |

---

## 2. Slots del vehículo

```
                    ┌─────────────┐
                    │  ESPECIAL   │  Bandera, turbo cartoon, item slot
                    └──────┬──────┘
              ┌────────────┼────────────┐
              │   ESCAPE   │  (lateral) │
              └────────────┼────────────┘
    ┌─────────┴────────────┴────────────┴─────────┐
    │              CHASIS (base)                   │
    │  ┌────────┐  ┌────────┐  ┌──────────────┐  │
    │  │ MOTOR  │  │ASIENTO │  │  SUSPENSIÓN  │  │
    │  └────────┘  └────────┘  └──────────────┘  │
    │  ┌────────┐  ┌────────┐                   │
    │  │PARACHO-│  │VOLANTE │                   │
    │  │ QUES   │  │        │                   │
    │  └────────┘  └────────┘                   │
    └───────────────────────────────────────────┘
         ○ RUEDA FL    ○ RUEDA FR
         ○ RUEDA RL    ○ RUEDA RR
```

| Slot | ID | Obligatorio | Cantidad |
|---|---|:---:|---|
| **Chasis** | `chassis` | ✅ | 1 |
| **Motor** | `engine` | ✅ | 1 |
| **Ruedas** | `wheels` | ✅ | 4 (par único o mixto) |
| **Suspensión** | `suspension` | ⚠️ | 1 (default básico incluido) |
| **Escape** | `exhaust` | ❌ | 0–1 |
| **Parachoques** | `bumper` | ❌ | 0–2 (delantero/trasero → 1 slot "bumper") |
| **Asiento** | `seat` | ❌ | 0–1 |
| **Volante** | `steering` | ❌ | 0–1 |
| **Especial** | `special` | ❌ | 0–1 |

**Slots desbloqueables:** suspensión avanzada, especial, segundo parachoques — vía PROGRESSION_GUIDE.

---

## 3. Piezas por slot

### 3.1 Motor

| Stat principal | Efecto |
|---|---|
| `acceleration` | u/s² |
| `max_speed` | u/s |
| `mass` | kg (afecta inercia) |
| `noise` | FX escape (visual) |

| Tier | Acel. | Max speed | Masa | Ejemplo |
|---|---|---|---|---|
| Small | +4 | +2 | +5 | Motor de lawnmower adaptado |
| Medium | +6 | +4 | +10 | Motor recuperado taller |
| Large | +8 | +5 | +18 | Motor de moto reforzado |

### 3.2 Ruedas

| Stat | Efecto |
|---|---|
| `grip` | Fricción en tierra/pasto |
| `turn_rate` | °/s adicional |
| `mass` | Por rueda |

| Tipo | Grip | Giro | Uso |
|---|---|---|---|
| Small | 0.90 | +10% | Asfalto, ágil |
| Large | 0.95 | -5% | Estable, off-road |
| Mixto | Variable | — | Build experimental (asimetría permitida) |

### 3.3 Chasis

| Stat | Efecto |
|---|---|
| `mass_base` | Peso total base |
| `slot_count` | Slots especiales desbloqueados |
| `max_engine_tier` | Tope de motor |
| `max_weight` | Peso máximo soportado |

| Tier | Masa base | Max peso | Max motor |
|---|---|---|---|
| Small | 20 | 45 | small |
| Medium | 35 | 70 | medium |
| Large | 50 | 95 | large |

### 3.4 Suspensión

| Stat | Efecto |
|---|---|
| `bounce` | Recuperación en baches |
| `offroad` | Penalización en tierra |
| `drift` | Facilidad de derrape cartoon |

### 3.5 Escape

| Stat | Efecto |
|---|---|
| `boost_trail` | FX visual |
| `accel_bonus` | +0–5% (menor que motor) |

### 3.6 Especial

| Tipo | Efecto | Ejemplo |
|---|---|---|
| `turbo_cartoon` | Burst velocidad 2 s cooldown | Botella presurizada |
| `shield_bumper` | 1 golpe sin perder speed | Almohada atada |
| `magnet_scrap` | Radio recolección +20% | Imán de almacén |
| `flag_clan` | Visual + rep clan en carrera | Bandera del clan |

---

## 4. Compatibilidades

### 4.1 Regla general

```
Motor pequeño  →  Chasis small/medium (ligero)
Motor medium   →  Chasis medium/large (si peso total ≤ max_weight)
Motor large    →  Solo chasis large con max_weight suficiente
```

### 4.2 Matriz de compatibilidad motor ↔ chasis

|  | Chassis Small | Chassis Medium | Chassis Large |
|---|---|---|---|
| **Motor Small** | ✅ Óptimo | ✅ OK | ⚠️ Subutilizado |
| **Motor Medium** | ❌ Sobrecarga | ✅ Óptimo | ✅ OK |
| **Motor Large** | ❌ | ❌ | ✅ Óptimo |

**Sobrecarga:** si motor tier > chasis max → penalización -30% aceleración, +20% masa efectiva.

### 4.3 Peso máximo

```
peso_total = chasis.mass_base
           + motor.mass
           + sum(ruedas.mass)
           + suspension.mass
           + sum(opcionales.mass)

SI peso_total > chasis.max_weight:
    penalización_velocidad = (peso_total - max_weight) × 0.02
    penalización_aceleración = (peso_total - max_weight) × 0.03
```

### 4.4 Ruedas

- **4× mismo set** → bonus grip +5% (build coherente)
- **2 small + 2 large** → permitido; handling impredecible cartoon (drift bonus)
- **Large en chassis small** → penalización giro -15%

### 4.5 Piezas opcionales

- Máximo **1 pieza por slot**
- **Especial** incompatible con otro **Especial**
- **Parachoques** delantero = slot `bumper` (un solo slot en v1)

---

## 5. Stats y fórmulas

### 5.1 Stats finales del vehículo

```
max_speed_final    = base_speed + motor.max_speed - penalización_peso
acceleration_final = base_accel + motor.acceleration - penalización_peso
grip_final         = promedio(ruedas.grip) + suspension.offroad_bonus
turn_rate_final    = base_turn + promedio(ruedas.turn_rate)
mass_final         = peso_total
```

### 5.2 Valores base (sin piezas)

| Stat | Valor |
|---|---|
| base_speed | 6 u/s |
| base_accel | 3 u/s² |
| base_turn | 140 °/s |

### 5.3 Límites (anti-exploit)

| Stat | Mín | Máx |
|---|---|---|
| max_speed | 5 | 14 u/s |
| acceleration | 2 | 12 u/s² |
| grip | 0.75 | 1.05 |
| turn_rate | 100 | 220 °/s |
| mass | 15 | 100 |

---

## 6. Tiers

| Tier | Desbloqueo | Perfil |
|---|---|---|
| **Small** | Tutorial | Ágil, atajos, drift |
| **Medium** | Reputación barrio 1 + chapitas | Balanceado |
| **Large** | Reputación barrio 2 + clan | Estable, rectas, peso |

Ver desbloqueos en [PROGRESSION_GUIDE.md](../game/PROGRESSION_GUIDE.md).

---

## 7. Craft y desmontaje

| Acción | Coste | Resultado |
|---|---|---|
| **Craft pieza** | Materiales + chapitas (ECONOMY) | Pieza nueva en inventario |
| **Desmontar pieza** | — | 60% materiales devueltos |
| **Upgrade slot** | Materiales raros | Mejora stat de pieza instalada |
| **Fusionar duplicados** | 3× misma pieza | 1× versión +1 tier stat |

---

## 8. Builds y presets

### 8.1 Archetypes (no clases rígidas)

| Build | Piezas clave | Estilo |
|---|---|---|
| **El Rayo** | Motor medium, ruedas small, chasis small | Atajos, aceleración |
| **El Tanque** | Motor large, ruedas large, chasis large | Rectas, empuje |
| **El Todoterreno** | Suspensión offroad, ruedas mixtas | Eríaos, dirt |
| **El Recolector** | Especial magnet, motor small | Farm + carrera casual |
| **El Show** | Accesorios, escape FX, bandera clan | Reputación social |

### 8.2 Presets JSON

`data/vehicles/default_builds.json`:

```json
{
  "starter": {
    "chassis": "vehicle_chassis_small_01",
    "engine": "engine_small_01",
    "wheels": ["wheel_small_01", "wheel_small_01", "wheel_small_01", "wheel_small_01"],
    "suspension": "suspension_basic_01"
  }
}
```

---

## 9. Bevy ECS

```rust
#[derive(Component)]
pub struct VehicleAssembly {
    pub chassis_id: PartId,
    pub slots: HashMap<SlotId, PartId>,
}

#[derive(Component)]
pub struct VehicleStats {
    pub max_speed: f32,
    pub acceleration: f32,
    pub grip: f32,
    pub turn_rate: f32,
    pub mass: f32,
}

// Sistema: recalcular stats al cambiar pieza
fn vehicle_stats_system(
    mut query: Query<(&VehicleAssembly, &mut VehicleStats), Changed<VehicleAssembly>>,
    catalog: Res<PartsCatalog>,
) { /* ... */ }
```

Datos: `data/vehicles/parts_catalog.json`, `data/vehicles/snap_points.json`

---

## 10. GLOBAL VEHICLE SYSTEM RULES

| ID | Regla |
|---|---|
| **VS-001** | Todo slot afecta al menos 1 stat jugable. |
| **VS-002** | Compatibilidad motor↔chasis enforced en UI y runtime. |
| **VS-003** | Peso máximo del chasis es hard cap con penalización. |
| **VS-004** | No hay pieza "strictly better" en todos los circuitos. |
| **VS-005** | Stats en JSON — balance sin recompilar Rust. |
| **VS-006** | Ensamblaje runtime desde piezas — no combos pre-renderizados. |
| **VS-007** | Desmontar devuelve materiales — experimentar es barato. |
| **VS-008** | Arte de piezas = Equipo ART; este doc solo define números y reglas. |

---

*Fin de VEHICLE_DESIGN_GUIDE.md*
