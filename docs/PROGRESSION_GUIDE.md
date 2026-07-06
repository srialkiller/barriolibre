# PROGRESSION_GUIDE.md
## Carreras de Barrio — Guía de Progresión

**Equipo:** GAMEPLAY (Equipo 3)  
**ADN:** [GAME_IDENTITY.md](./GAME_IDENTITY.md)  
**Relacionado:** [GAMEPLAY_GUIDE.md](./GAMEPLAY_GUIDE.md), [ECONOMY_GUIDE.md](./ECONOMY_GUIDE.md), [VEHICLE_DESIGN_GUIDE.md](./VEHICLE_DESIGN_GUIDE.md), [CLAN_SYSTEM_GUIDE.md](./CLAN_SYSTEM_GUIDE.md)  
**Versión:** 1.0

---

> Define **metas a largo plazo, desbloqueos y curva de progresión**. La progresión debe sentirse como crecer en el barrio — no como grind infinito.

---

## Tabla de contenidos

1. [Filosofía de progresión](#1-filosofía-de-progresión)
2. [Capas de progresión](#2-capas-de-progresión)
3. [Arco del jugador nuevo](#3-arco-del-jugador-nuevo)
4. [Desbloqueos por reputación](#4-desbloqueos-por-reputación)
5. [Desbloqueos de vehículo](#5-desbloqueos-de-vehículo)
6. [Desbloqueos de mundo](#6-desbloqueos-de-mundo)
7. [Desbloqueos de clan](#7-desbloqueos-de-clan)
8. [Curva de dificultad](#8-curva-de-dificultad)
9. [Metas a largo plazo](#9-metas-a-largo-plazo)
10. [Bevy ECS](#10-bevy-ecs)
11. [GLOBAL PROGRESSION RULES](#11-global-progression-rules)

---

## 1. Filosofía de progresión

| Principio | Regla |
|---|---|
| **Explorar desbloquea** | POIs, atajos y barrios no se compran — se descubren |
| **Construir es progresar** | Mejorar el auto = avance tangible |
| **Competir valida** | Carreras prueban el build, no lo reemplazan |
| **Social opcional** | Clan acelera rep social, no bloquea contenido solo |
| **Sin paredes duras** | Si fallas, puedes farmear materiales y reintentar |

**Anti-pattern:** XP infinito sin metas, paywall de tiers, vehículos prefabricados como único camino.

---

## 2. Capas de progresión

```
┌─────────────────────────────────────────────┐
│  META (100+ h)                              │
│  Ídolo del barrio · Clan legend · Barrio 2  │
├─────────────────────────────────────────────┤
│  MEDIO (10–30 h)                            │
│  Tier large · Torneos · Proyectos clan      │
├─────────────────────────────────────────────┤
│  CORTO (1–3 h)                              │
│  Tutorial · Primer circuito · Build medium  │
├─────────────────────────────────────────────┤
│  SESIÓN (30 min)                            │
│  1–2 crafts · 1 carrera · exploración POI   │
└─────────────────────────────────────────────┘
```

---

## 3. Arco del jugador nuevo

| Fase | Duración | Hitos |
|---|---|---|
| **Tutorial** | 15–20 min | Moverse, recoger basura, craft wheel+chassis, micro carrera |
| **Primer barrio** | 1–2 h | 3 POIs, primer circuito, rep Vecino |
| **Corredor** | 3–8 h | Tier medium, atajos, rival 1, comercio |
| **Leyenda local** | 8–20 h | Tier large, torneo, clan opcional |
| **Ídolo** | 20+ h | Barrio secreto, especiales, eventos clan |

### Tutorial — secuencia

```
Spawn en plaza
    ↓
NPC explica: "Esto no es un auto de verdad — lo armamos nosotros"
    ↓
Recoger 3 objetos (micro loop)
    ↓
Taller: craft ruedas + chasis
    ↓
Carrera corta en cancha (sin rivales duros)
    ↓
Desbloqueo: mapa del barrio + primer POI
```

---

## 4. Desbloqueos por reputación

Ver rangos en [ECONOMY_GUIDE §6](./ECONOMY_GUIDE.md#6-reputación).

| Rango | Rep | Desbloqueo clave |
|---|---|---|
| Desconocido | 0 | Tutorial, craft tier small |
| Vecino | 50 | Comercio, circuito 1, mapa completo barrio 1 |
| Corredor | 150 | Blueprints medium, rival 1, inscripción torneo |
| Leyenda del barrio | 400 | Blueprints large, circuito difícil, slot especial |
| Ídolo | 800 | Barrio 2 (futuro), piezas únicas, eventos especiales |

**Rep rival** (independiente): desbloquea rematches y 1 pieza única por rival vencido 3×.

---

## 5. Desbloqueos de vehículo

| Contenido | Requisito |
|---|---|
| Slots: suspensión avanzada | Corredor + craft `suspension_offroad_01` |
| Slot especial | Leyenda del barrio |
| Tier medium craft | Corredor |
| Tier large craft | Leyenda + 1× motor_viejo |
| Builds preset "El Rayo" etc. | Blueprint en taller NPC o rep |

Ver [VEHICLE_DESIGN_GUIDE §6](./VEHICLE_DESIGN_GUIDE.md#6-tiers).

---

## 6. Desbloqueos de mundo

| Contenido | Requisito |
|---|---|
| POI Taller | Tutorial |
| POI Almacén | Explorar callejón norte |
| POI Eríaos | Vecino |
| Atajo eriazo→plaza | Descubrir (1ª vez +5 rep) |
| Circuito 1 (cancha) | Tutorial complete |
| Circuito 2 (plaza→taller) | Vecino |
| Barrio 2 | Ídolo (fase mundos futura) |

POIs mapeados en [NEIGHBORHOOD_DESIGN_GUIDE.md](./NEIGHBORHOOD_DESIGN_GUIDE.md).

---

## 7. Desbloqueos de clan

| Contenido | Requisito |
|---|---|
| Crear clan | Corredor + 100 chapitas |
| Proyecto clan 1 | Clan activo, 3+ miembros |
| Pieza especial clan | Proyecto completado |
| Torneo clan | Rep clan ≥ 100 |

Ver [CLAN_SYSTEM_GUIDE.md](./CLAN_SYSTEM_GUIDE.md).

---

## 8. Curva de dificultad

### Carreras

| Circuito | Skill esperado | Duración | Rivales |
|---|---|---|---|
| Cancha tutorial | Novato | 60 s | 0–1 fácil |
| Circuito 1 | Bajo | 90–120 s | 2–3 amistosos |
| Circuito 2 | Medio | 120–150 s | Especialistas mixtos |
| Torneo | Medio-alto | 150 s | Optimizados + atajos |

### Economía (sesión)

| Horas jugadas | Chapitas/h acumuladas | Crafts posibles/h |
|---|---|---|
| 0–2 | ~200 | 1 small |
| 2–10 | ~350 | 1 medium cada 2 h |
| 10+ | ~400 (techo suave) | 1 medium/h con exploración |

---

## 9. Metas a largo plazo

| Meta | Descripción | Tipo jugador |
|---|---|---|
| **Maestro del barrio** | Rep Ídolo + todos los atajos | Explorador |
| **Ingeniero del barrio** | 1 build optimizado por arquetipo | Constructor |
| **Campeón de cancha** | Ganar torneo barrio | Competitivo |
| **Corazón del clan** | Proyecto clan + 10 victorias clan | Social |
| **Rival definitivo** | Vencer a los 3 rivales NPC 3× cada uno | Narrativo |

Ninguna meta es obligatoria para "terminar" el juego — son aspiraciones.

---

## 10. Bevy ECS

```rust
#[derive(Resource)]
pub struct PlayerProgression {
    pub tutorial_flags: HashSet<TutorialFlag>,
    pub unlocked_pois: HashSet<PoiId>,
    pub unlocked_circuits: HashSet<CircuitId>,
    pub unlocked_blueprints: HashSet<BlueprintId>,
    pub discovered_shortcuts: HashSet<ShortcutId>,
    pub rival_wins: HashMap<RivalId, u32>,
}

// Sistema: al subir rep, evaluar desbloqueos
fn progression_unlock_system(
    mut progression: ResMut<PlayerProgression>,
    economy: Res<PlayerEconomy>,
    unlock_table: Res<UnlockTable>,
) { /* ... */ }
```

Datos: `data/progression/unlock_table.json`, `data/progression/tutorial_flow.json`

---

## 11. GLOBAL PROGRESSION RULES

| ID | Regla |
|---|---|
| **PR-001** | Tutorial enseña micro loop antes de carrera larga. |
| **PR-002** | Ningún contenido core bloqueado solo por clan. |
| **PR-003** | Desbloqueos en JSON — ajustables sin recompilar. |
| **PR-004** | Rep sube por jugar, no por tiempo real idle. |
| **PR-005** | Curva: fácil al inicio, pico en torneo, sin paredes. |
| **PR-006** | Metas largas = aspiracionales, no gate de "final". |
| **PR-007** | Toda progresión refuerza GAME_IDENTITY (creatividad, barrio, amigos). |

---

*Fin de PROGRESSION_GUIDE.md*
