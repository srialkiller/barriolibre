# GAMEPLAY_GUIDE.md
## Carreras de Barrio — Guía de Gameplay

**Equipo:** GAMEPLAY (Equipo 3)  
**ADN del juego:** [GAME_IDENTITY.md](./GAME_IDENTITY.md) — **leer primero**  
**Versión:** 2.0  
**Estado:** Documento dedicado exclusivamente al gameplay — **no es un GDD**

---

> Este documento define **cómo se juega**: loops, acciones del jugador, estados y sensaciones. No define historia, arte, pipeline ni negocio. Para identidad filosófica → `GAME_IDENTITY.md`. Para carreras → `RACE_DESIGN_GUIDE.md`. Para piezas → `VEHICLE_DESIGN_GUIDE.md`.

---

## Tabla de contenidos

1. [Resumen en 30 segundos](#1-resumen-en-30-segundos)
2. [Core Loop (macro)](#2-core-loop-macro)
3. [Micro Loop (recolección)](#3-micro-loop-recolección)
4. [Race Loop (competencia)](#4-race-loop-competencia)
5. [Modos de juego](#5-modos-de-juego)
6. [Acciones del jugador](#6-acciones-del-jugador)
7. [Estados del juego (Bevy ECS)](#7-estados-del-juego-bevy-ecs)
8. [Controles](#8-controles)
9. [Física cartoon](#9-física-cartoon)
10. [Sensaciones por fase del loop](#10-sensaciones-por-fase-del-loop)
11. [GLOBAL GAMEPLAY RULES](#11-global-gameplay-rules)

---

## 1. Resumen en 30 segundos

Explorás tu barrio, recogés materiales reciclables, construís y mejorás tu vehículo casero en el taller, competís en carreras con chicos del barrio, ganás recompensas y reputación, y volvés a explorar con un auto mejor y un barrio más conocido.

**El auto no es el fin — es la prueba de tu ingenio.**

---

## 2. Core Loop (macro)

El loop que define la sesión de juego completa (15–45 minutos):

```
    ┌──────────┐
    │ EXPLORAR │  Caminar/conducir el barrio, descubrir POIs, atajos, materiales
    └────┬─────┘
         ▼
    ┌──────────┐
    │RECOLECTAR│  Recoger materiales, chapitas, piezas, completar objetivos locales
    └────┬─────┘
         ▼
    ┌──────────┐
    │ CONSTRUIR│  Taller/garage: armar, cambiar, mejorar piezas del vehículo
    └────┬─────┘
         ▼
    ┌──────────┐
    │ COMPETIR │  Carreras: validar tu build contra rivales y el barrio
    └────┬─────┘
         ▼
    ┌──────────┐
    │ MEJORAR  │  Con recompensas: piezas, materiales, reputación, desbloqueos
    └────┬─────┘
         │
         └──────────► REPETIR (barrio más profundo, auto mejor, eventos nuevos)
```

### 2.1 Detalle por fase

| Fase | Duración típica | Qué hace el jugador | Qué gana | Pilar reforzado |
|---|---|---|---|---|
| **Explorar** | 5–15 min | Camina, conduce libre, entra a POIs | Conocimiento del mapa, puntos de farm | Exploración |
| **Recolectar** | Integrado en explorar | Recoge materiales, habla con NPCs | Inventario, chapitas | Creatividad |
| **Construir** | 3–10 min | Taller: slots, craft, prueba | Vehículo actualizado | Creatividad + Mejora |
| **Competir** | 2–4 min/carrera | Corre, elige rutas, usa atajos | Posición, recompensas | Ingenio |
| **Mejorar** | 1–3 min | Gasta recompensas, sube reputación | Progresión, eventos nuevos | Mejora + Comunidad |

### 2.2 Reglas del Core Loop

1. **Ninguna fase es skippable permanentemente** — construir sin explorar = piezas limitadas; competir sin construir = perder siempre.
2. **Explorar siempre tiene algo nuevo** — material respawneable, atajo oculto, evento de clan.
3. **Competir es la validación** — no el 100% del tiempo de juego (ideal: 30–40% en sesión activa de carreras).
4. **Mejorar cierra el ciclo emocional** — el jugador debe sentir que su auto de ayer era peor que el de hoy.

---

## 3. Micro Loop (recolección)

El loop más pequeño y frecuente (10–30 segundos), repetido docenas de veces por sesión:

```
    ┌─────────────┐
    │ Veo material│  Basura limpia / pieza / chapitas en el barrio
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │  La recojo  │  Interacción: E / botón en POI o mundo
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │Obtengo pieza│  Inventario: materiales, chapitas, blueprint, pieza
    │  o recurso  │
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │Mejoro el   │  (Inmediato o en taller) slot upgrade, craft, trade
    │    auto     │
    └─────────────┘
```

### 3.1 Tipos de recolección

| Tipo | Fuente | Ejemplo | Frecuencia |
|---|---|---|---|
| **Material común** | Suelo, contenedor, POI | Cartón, chapa, neumático | Alta |
| **Material raro** | Taller, callejón, evento | Motor viejo, cable | Baja |
| **Chapitas** | Carrera, misión, venta | Moneda del barrio | Media |
| **Pieza directa** | Recompensa carrera, comercio | Rueda medium, escape | Media |
| **Blueprint** | Reputación, clan, exploración | Desbloqueo de receta | Baja |

### 3.2 Feedback de recolección

- **Visual:** objeto desaparece con pop cartoon + icono en HUD
- **Sonoro:** click satisfactorio, no realista
- **UI:** contador de inventario sube; toast "Cartón +1"
- **Emoción:** curiosidad → mini recompensa → ganas de seguir explorando

### 3.3 Reglas del Micro Loop

1. Recoger nunca se siente como "basurero" — es **tesoro del barrio** (GAME_IDENTITY §I-007).
2. Todo material tiene uso en craft — no hay ítems basura pura.
3. Respawn de materiales comunes en POIs — el barrio no se "vacía".
4. Materiales raros tienen ubicación lógica (taller → motor, almacén → cartón).

---

## 4. Race Loop (competencia)

El loop de una carrera individual (3–8 minutos total con prep y premios):

```
    ┌─────────────┐
    │ PREPARACIÓN │  Elegir vehículo/build, revisar circuito, consumibles
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │CLASIFICACIÓN│  (Opcional) Vuelta de prueba, posición de salida
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │   CARRERA   │  1–3 laps, checkpoints, atajos, rivales
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │   PREMIOS   │  Chapitas, materiales, piezas, XP reputación
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │ REPUTACIÓN  │  Subir rango local, clan, barrio
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │NUEVOS EVENTOS│  Desbloqueo carrera, torneo clan, invitación
    └─────────────┘
```

### 4.1 Detalle por fase

| Fase | Qué pasa | Decisión del jugador |
|---|---|---|
| **Preparación** | Garage rápido o pre-build; ver mapa del circuito | ¿Qué build para este circuito? |
| **Clasificación** | 1 vuelta cronometrada (modos avanzados) | Aprender línea, ganar posición de salida |
| **Carrera** | Gameplay de conducción activo | Ruta segura vs atajo, frenar vs arriesgar |
| **Premios** | Pantalla resultados + drops | Satisfacción o motivación para mejorar |
| **Reputación** | +rep barrio, clan, rival amistoso | Desbloqueos sociales y de contenido |
| **Nuevos eventos** | Calendario se actualiza | "Hay carrera el sábado" — retención |

### 4.2 Tipos de carrera en el loop

| Tipo | Cuándo | Race Loop completo |
|---|---|---|
| **Carrera casual** | Hub del barrio | Prep → Carrera → Premios |
| **Carrera de historia** | Misión | Prep → Carrera → Premios → Rep → Evento |
| **Torneo de clan** | Evento semanal | Clasificación → Carrera ×N → Premios clan |
| **Contrarreloj** | Desafío | Prep → Carrera → Premios (sin rivales) |
| **Exploración cronometrada** | Descubrir atajo | Carrera corta → Premio exploración |

Ver detalle de circuitos en [RACE_DESIGN_GUIDE.md](./RACE_DESIGN_GUIDE.md).

### 4.3 Reglas del Race Loop

1. Carrera dura **90–150 s** de conducción activa (ideal 120 s).
2. Perder debe enseñar — feedback: "tu auto patinó en tierra" no "game over".
3. Premios siempre positivos por completar — ganar es bonus.
4. Reputación no es grind infinito — hitos claros (ver PROGRESSION_GUIDE).

---

## 5. Modos de juego

| Modo | Core Loop | Descripción |
|---|---|---|
| **Barrio libre (Hub)** | Explorar + Recolectar | Sandbox con objetivos suaves |
| **Taller (Garage)** | Construir | Craft, slots, prueba en patio |
| **Carrera rápida** | Competir | Una carrera, premios, volver |
| **Modo historia** | Loop completo | Barrios secuenciales, rivales, clan |
| **Evento de clan** | Competir + Comunidad | Torneos, cooperación, ranking clan |

---

## 6. Acciones del jugador

### 6.1 En el barrio (exploración)

| Acción | Input | Resultado |
|---|---|---|
| Caminar | Stick / WASD | Mover por vereda y POIs |
| Conducir (libre) | Vehículo equipado | Recorrer calles, probar atajos |
| Recoger | E / A | Material → inventario |
| Interactuar POI | E en punto | Taller, almacén, cancha, NPC |
| Abrir mapa | M / Tab | Ver barrio, atajos descubiertos |
| Entrar a carrera | E en punto de carrera | Inicia Race Loop |

### 6.2 En el taller

| Acción | Input | Resultado |
|---|---|---|
| Instalar pieza | Drag / menú slot | Pieza en vehículo |
| Quitar pieza | Click slot | Pieza → inventario |
| Craft | Receta + materiales | Pieza nueva |
| Probar | Botón "Probar" | Conducción en patio del taller |
| Guardar build | Auto-save | Build persistido |

### 6.3 En carrera

| Acción | Input | Resultado |
|---|---|---|
| Acelerar / frenar | RT / LT | Velocidad |
| Girar | Stick | Dirección |
| Drift (opcional) | LT + giro | Curva cerrada cartoon |
| Item (futuro) | X | Boost, escudo cartoon, etc. |
| Pausa | Start | Menú pausa |

---

## 7. Estados del juego (Bevy ECS)

```rust
#[derive(States, Default, Clone, Eq, PartialEq, Hash, Debug)]
pub enum GameState {
    #[default]
    MainMenu,
    NeighborhoodHub,   // explorar + recolectar
    Garage,            // construir
    RacePreparation,   // prep + clasificación
    Race,              // carrera activa
    RaceResults,       // premios + reputación
    ClanHub,           // eventos clan
    Paused,
}
```

| Transición | Trigger |
|---|---|
| Hub → Garage | Interactuar taller POI |
| Hub → RacePreparation | Inscribirse a carrera |
| Garage → Hub | Salir del taller |
| RacePreparation → Race | Countdown 3-2-1 |
| Race → RaceResults | Cruzar meta / timeout |
| RaceResults → Hub | Continuar |

---

## 8. Controles

| Acción | Teclado | Gamepad |
|---|---|---|
| Mover (a pie) | WASD | Stick izquierdo |
| Acelerar | W / ↑ | RT |
| Frenar / reversa | S / ↓ | LT |
| Girar (vehículo) | A/D o stick | Stick izquierdo |
| Interactuar | E | A |
| Mapa | M | Select |
| Pausa | Escape | Start |

**Accesibilidad:** remapeo completo; asistencia de dirección opcional para público infantil.

---

## 9. Física cartoon

| Parámetro | Rango | Notas |
|---|---|---|
| Velocidad máxima | 8–14 u/s | Build + superficie |
| Aceleración | 4–10 u/s² | Motor + peso |
| Giro | 120–200 °/s | Ruedas + suspensión |
| Fricción | 0.80–0.95 | Por tile (ver RACE_DESIGN) |
| Colisión | Rebote suave | Sin daño, sin volcar permanente |
| Recuperación | Auto-upright | El auto se endereza cartoon |

**Regla:** la física sirve al **ingenio del build y la ruta**, no al realismo.

---

## 10. Sensaciones por fase del loop

| Fase | Sensación objetivo | Evitar |
|---|---|---|
| Explorar | Curiosidad, "¿qué hay ahí?" | Barrio vacío, repetitivo |
| Recolectar | Mini victoria, acumulación | Grind tedioso |
| Construir | Orgullo, experimentación | Menús confusos, builds invalidos |
| Competir | Tensión alegre, flow | Frustración, injusticia |
| Mejorar | Progreso visible | Paywall, RNG cruel |
| Repetir | "Una carrera más" | Fatiga, sameness |

---

## 11. GLOBAL GAMEPLAY RULES

| ID | Regla |
|---|---|
| **GP-001** | Leer GAME_IDENTITY antes de diseñar cualquier mecánica. |
| **GP-002** | Core Loop completo debe ser jugable en tutorial (30 min). |
| **GP-003** | Micro Loop ≤30 s; repetible sin fatiga. |
| **GP-004** | Race Loop ≤8 min total; conducción activa 90–150 s. |
| **GP-005** | Perder enseña — nunca castiga sin feedback. |
| **GP-006** | Construir y explorar son tan importantes como competir. |
| **GP-007** | Todo estado = `GameState` Bevy explícito. |
| **GP-008** | Controles aprendibles en <2 min. |
| **GP-009** | Física cartoon — nunca simulación realista. |
| **GP-010** | Si una mecánica no refuerza el ADN → no entra (GAME_IDENTITY §7). |

---

*Fin de GAMEPLAY_GUIDE.md — no es GDD; es gameplay puro.*
