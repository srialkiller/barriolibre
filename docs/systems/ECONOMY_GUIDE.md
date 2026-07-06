# ECONOMY_GUIDE.md
## Carreras de Barrio — Guía de Economía

**Equipo:** GAMEPLAY (Equipo 3)  
**ADN:** [GAME_IDENTITY.md](../game/GAME_IDENTITY.md)  
**Versión:** 2.0

---

> Define **materiales, dinero, reputación, clanes, crafting y comercio**. Toda regla económica debe reforzar reciclaje creativo — no pay-to-win.

---

## Tabla de contenidos

1. [Filosofía económica](#1-filosofía-económica)
2. [Capas de recursos](#2-capas-de-recursos)
3. [Materiales](#3-materiales)
4. [Basura reciclable](#4-basura-reciclable)
5. [Dinero (Chapitas)](#5-dinero-chapitas)
6. [Reputación](#6-reputación)
7. [Crafting](#7-crafting)
8. [Comercio](#8-comercio)
9. [Clanes y economía](#9-clanes-y-economía)
10. [Fuentes y sumideros](#10-fuentes-y-sumideros)
11. [Bevy ECS](#11-bevy-ecs)
12. [GLOBAL ECONOMY RULES](#12-global-economy-rules)

---

## 1. Filosofía económica

| Principio | Regla |
|---|---|
| **Reciclaje = valor** | Lo que encuentras en el barrio tiene uso |
| **Explorar paga** | Materiales en POIs, no solo carreras |
| **Craft > compra directa** | Las mejores piezas requieren materiales + chapitas |
| **Sin pay-to-win** | IAP futuro: solo cosmético |
| **Inflación controlada** | Sumideros en craft, comercio, eventos clan |

---

## 2. Capas de recursos

```
┌─────────────────────────────────────────────────┐
│  CAPA SOCIAL                                    │
│  Reputación (barrio, clan, rival)               │
├─────────────────────────────────────────────────┤
│  CAPA MONETARIA                                 │
│  Chapitas (dinero blando)                       │
├─────────────────────────────────────────────────┤
│  CAPA MATERIAL                                  │
│  Materiales reciclables + basura procesable     │
├─────────────────────────────────────────────────┤
│  CAPA PIEZAS                                    │
│  Componentes crafteados / drops de carrera      │
└─────────────────────────────────────────────────┘
```

---

## 3. Materiales

| ID | Nombre | Rareza | Fuentes | Uso craft |
|---|---|---|---|---|
| `mat_carton` | Cartón | Común | Almacén, eriazo | Chasis, asiento |
| `mat_chapa` | Chapa | Común | Eríaos, taller | Chasis, parachoques |
| `mat_madera` | Madera | Común | Taller, construcción | Parachoques, chasis |
| `mat_neumatico` | Neumático | Común | Taller, callejón | Ruedas |
| `mat_bidon` | Bidón | Común | Almacén | Tanque, asiento |
| `mat_cable` | Cable / caño | Poco común | Almacén, eriazo | Motor, escape |
| `mat_cinta` | Cinta adhesiva | Poco común | Cualquier POI | Uniones, cosmético |
| `mat_motor_viejo` | Motor recuperado | Raro | Taller (respawn lento) | Motor tier medium+ |
| `mat_engranaje` | Engranaje | Raro | Eventos, clan | Suspensión, especial |
| `mat_pintura` | Pintura reciclada | Poco común | Comercio, misión | Cosmético |

**Stack máximo:** 999 comunes, 99 raros.

---

## 4. Basura reciclable

En el mundo aparecen objetos interactuables — **basura limpia del barrio**, nunca sucia (GAME_IDENTITY).

| Objeto mundo | Al recoger | POI típico |
|---|---|---|
| Caja de fruta | +2 cartón | Almacén, vereda |
| Bidón vacío | +1 bidón | Patio, eriazo |
| Neumático viejo | +1 neumático | Taller, callejón |
| Chapa suelta | +1 chapa | Eríaos |
| Cables | +1 cable | Almacén |

**Respawn:** comunes 5 min por POI; raros 30 min; eventos únicos no respawnean.

**Micro loop:** ver → recoger → inventario → craft (GAMEPLAY_GUIDE §3).

---

## 5. Dinero (Chapitas)

| Propiedad | Valor |
|---|---|
| **ID** | `moneda_chapitas` |
| **Nombre UI** | Chapitas |
| **Función** | Comercio, craft parcial, inscripción carreras |
| **Visual** | Moneda metálica redonda — sin texto |

### Fuentes

| Fuente | Cantidad |
|---|---|
| Completar carrera | 8–15 |
| Ganar carrera | +15–30 |
| Vender materiales | 2–10 c/u |
| Misión barrio | 20–50 |
| Evento clan | 50–100 (pool compartido) |
| Atajo descubierto (1ª vez) | 5 |

### Sumideros

| Uso | Coste |
|---|---|
| Craft pieza small | 15–50 |
| Craft pieza medium | 80–150 |
| Craft pieza large | 200–350 |
| Inscripción torneo | 25 |
| Comprar material en puesto | 5–20 |
| Upgrade slot taller | 100+ |

**Regla:** ingreso promedio **≤35 chapitas/min** de gameplay activo.

---

## 6. Reputación

Tres tracks independientes:

| Track | ID | Cómo sube | Desbloquea |
|---|---|---|---|
| **Barrio** | `rep_barrio_*` | Carreras, misiones, exploración | Circuitos, comerciantes, barrios |
| **Clan** | `rep_clan_*` | Eventos clan, donaciones | Torneos, piezas clan |
| **Rival** | `rep_rival_*` | Carreras vs NPC específico | Rematches, piezas únicas |

### Rangos (barrio)

| Rango | Puntos | Desbloqueo |
|---|---|---|
| Desconocido | 0 | Tutorial |
| Vecino | 50 | Comercio básico |
| Corredor | 150 | Tier medium craft |
| Leyenda del barrio | 400 | Tier large, eventos |
| Ídolo | 800 | Barrio secreto, especiales |

Ver [PROGRESSION_GUIDE.md](../game/PROGRESSION_GUIDE.md).

---

## 7. Crafting

### 7.1 Flujo

```
Materiales (+ chapitas opcional)  →  [Taller / Receta]  →  Pieza
```

### 7.2 Recetas ejemplo

| Pieza | Materiales | Chapitas |
|---|---|---|
| `wheel_small_01` | 2× neumático, 1× cable | 20 |
| `engine_small_01` | 3× chapa, 2× cable, 1× cinta | 40 |
| `vehicle_chassis_small_01` | 5× cartón, 2× madera, 2× chapa | 50 |
| `engine_medium_01` | 1× motor_viejo, 4× chapa, 2× cable | 100 |
| `suspension_offroad_01` | 2× neumático, 1× engranaje, 3× madera | 80 |

**Datos:** `data/economy/recipe_table.json`

### 7.3 Reglas craft

1. Receta visible si tienes blueprint o reputación suficiente.
2. Craft toma **0 s** en v1 (instant) — animación en taller.
3. Fallo imposible — materiales siempre producen pieza.
4. Duplicados: desmontar o fusionar (VEHICLE_DESIGN §7).

---

## 8. Comercio

### 8.1 Tipos

| Tipo | Ubicación | Qué vende |
|---|---|---|
| **Puesto barrio** | Plaza, almacén | Materiales comunes, chapitas→material |
| **Taller NPC** | Taller POI | Piezas tier bajo, blueprints |
| **Intercambio clan** | Clan hub | Piezas donadas entre miembros |
| **Rival** | Post-carrera | Pieza única si rep_rival alto |

### 8.2 Precios dinámicos (suaves)

```
precio_compra = base × (1 + 0.1 × veces_comprado_esta_semana)
precio_venta  = base × 0.6
```

Anti-inflación: precios reset semanal.

---

## 9. Clanes y economía

| Mecánica | Descripción |
|---|---|
| **Banco clan** | Chapitas + materiales donados |
| **Proyecto clan** | Meta colectiva → pieza especial clan |
| **Torneo** | Entry fee 25 chapitas → premio pool |
| **Intercambio** | Miembros intercambian piezas/materiales |

Ver [CLAN_SYSTEM_GUIDE.md](../game/CLAN_SYSTEM_GUIDE.md).

---

## 10. Fuentes y sumideros

### Balance objetivo (sesión 30 min)

| Recurso | Ganancia típica | Gasto típico |
|---|---|---|
| Chapitas | 150–250 | 100–200 (1–2 crafts) |
| Materiales comunes | 30–50 unidades | 20–40 en craft |
| Rep barrio | +20–40 | — |

**Objetivo:** el jugador termina la sesión con **1–2 crafts posibles** y sensación de progreso.

---

## 11. Bevy ECS

```rust
#[derive(Resource)]
pub struct PlayerEconomy {
    pub chapitas: u32,
    pub materials: HashMap<MaterialId, u32>,
    pub reputation: HashMap<RepTrack, u32>,
    pub owned_parts: HashSet<PartId>,
    pub unlocked_recipes: HashSet<RecipeId>,
}
```

---

## 12. GLOBAL ECONOMY RULES

| ID | Regla |
|---|---|
| **E-001** | Nada se llama "basura inútil" — todo reciclable tiene craft o venta. |
| **E-002** | Chapitas no compran victoria directa — compran craft y acceso. |
| **E-003** | Reputación desbloquea contenido — no reemplaza skill. |
| **E-004** | Recetas y precios en JSON. |
| **E-005** | Clan economy = cooperación, no competencia destructiva. |
| **E-006** | IAP futuro: cosmético únicamente. |
| **E-007** | Toda fuente de recurso mapeada a POI (NEIGHBORHOOD_DESIGN). |

---

*Fin de ECONOMY_GUIDE.md*
