# GAME_IDENTITY.md
## Carreras de Barrio — Identidad del Juego (ADN)

**Equipo:** GAMEPLAY (Equipo 3)  
**Versión:** 1.0  
**Estado:** Documento fundacional — **leer antes que cualquier decisión de diseño**

---

> Este documento responde una sola pregunta: **¿Por qué existe Carreras de Barrio?**  
> No es un GDD. No es arte. No es pipeline. Es el **ADN del juego** — el filtro que toda idea nueva debe pasar antes de entrar al proyecto.

---

## Tabla de contenidos

1. [La verdad central](#1-la-verdad-central)
2. [Qué NO es este juego](#2-qué-no-es-este-juego)
3. [Los cinco pilares](#3-los-cinco-pilares)
4. [El vehículo no es el objetivo](#4-el-vehículo-no-es-el-objetivo)
5. [Fantasía del jugador](#5-fantasía-del-jugador)
6. [Emociones objetivo](#6-emociones-objetivo)
7. [Filtro de decisiones](#7-filtro-de-decisiones)
8. [Relación con otros documentos](#8-relación-con-otros-documentos)
9. [GLOBAL IDENTITY RULES](#9-global-identity-rules)

---

## 1. La verdad central

**Carreras de Barrio no trata sobre autos.**

Trata sobre **creatividad** — construir con lo que tienes, no con lo que compras.

| El juego ES | El juego NO ES |
|---|---|
| Inventiva infantil en un barrio latinoamericano | Simulador de conducción realista |
| Competir con ingenio, no con potencia | Carreras de autos de fábrica |
| Conocer cada rincón del barrio | Completar niveles genéricos |
| Mejorar tu creación pieza a pieza | Coleccionar vehículos prefabricados |
| Hacer amigos y pertenecer a un clan | Multijugador agresivo o tóxico |
| Reciclaje limpio, funcional, ingenioso | Basura, suciedad, postapocalíptico |

### Frase de una línea

> *"Los chicos del barrio convierten lo que encuentran en algo que compite — y en el camino, se conocen el lugar y se conocen entre sí."*

---

## 2. Qué NO es este juego

Si una feature hace que el juego se sienta como alguna de estas cosas, **no pertenece**:

| Anti-identidad | Por qué contradice el ADN |
|---|---|
| Need for Speed / simulador de carreras | Los autos no son el centro; son consecuencia |
| Minecraft puro (sandbox sin meta) | Hay competencia, carreras y progresión social |
| Battle royale / eliminación agresiva | Competencia sana, infantil, sin violencia |
| Pay-to-win / gacha de vehículos | Progresión por explorar, reciclar y construir |
| Suburbio norteamericano ordenado | Barrio popular latinoamericano, irregular, vivido |
| Juego de combate | Los vehículos compiten, no destruyen |
| Gestión pura / idle game | Hay conducción activa, exploración y carreras |

---

## 3. Los cinco pilares

Todo sistema, misión, asset y feature debe reforzar **al menos uno** de estos pilares:

```
┌─────────────────────────────────────────────────────────────┐
│                    CARRERAS DE BARRIO                         │
│                                                             │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│   │CREATIVIDAD│  │  INGENIO │  │ EXPLORAR │               │
│   │ Construir │  │ Competir │  │  Barrio  │               │
│   │ con lo que│  │  con lo  │  │  cada    │               │
│   │   tienes  │  │ que hiciste│ │ rincón  │               │
│   └──────────┘  └──────────┘  └──────────┘               │
│                                                             │
│        ┌──────────┐        ┌──────────┐                    │
│        │ COMUNIDAD│        │ MEJORAR  │                    │
│        │ Amigos,  │        │  tu      │                    │
│        │ clanes,  │        │ creación │                    │
│        │ barrio   │        │          │                    │
│        └──────────┘        └──────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

### Pilar 1 — Creatividad

- El jugador **construye** su vehículo con piezas encontradas.
- No hay vehículo perfecto de fábrica — hay **tu** vehículo.
- Cada build es una expresión de decisiones: ligero vs pesado, rápido vs estable.

### Pilar 2 — Ingenio

- Ganar no es tener el motor más grande — es **saber qué combinar** y **qué ruta tomar**.
- Los atajos del barrio recompensan conocimiento, no solo reflejos.
- Un auto feo pero bien pensado puede ganar a uno bonito mal armado.

### Pilar 3 — Explorar el barrio

- Cada barrio tiene **plazas, callejones, atajos, subidas, sitios eriazo**.
- Explorar no es optional — es cómo encuentras materiales y descubres rutas de carrera.
- El jugador debe sentir: *"conozco este barrio mejor que nadie"*.

### Pilar 4 — Comunidad

- Clanes de chicos del barrio — cooperación, intercambio, eventos compartidos.
- Rivales amistosos, no enemigos.
- Reputación social importa tanto como victorias.

### Pilar 5 — Mejorar tu creación

- El loop emocional central: *"mi auto era una caja — ahora es MI caja, y es más rápida"*.
- Cada carrera enseña algo sobre tu build.
- La satisfacción viene de ver tu creación mejorar, no de desbloquear un skin.

---

## 4. El vehículo no es el objetivo

```
        ┌─────────────────┐
        │   CREATIVIDAD   │  ← objetivo real
        │   INGENIO       │
        │   COMUNIDAD     │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    VEHÍCULO     │  ← herramienta de expresión
        │   (consecuencia)│
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    CARRERA      │  ← validación de la creación
        └─────────────────┘
```

| Capa | Rol | Pregunta que responde |
|---|---|---|
| **Creatividad / Ingenio** | Objetivo emocional | ¿Qué puedo construir con esto? |
| **Vehículo** | Medio de expresión | ¿Cómo se ve mi ingenio en metal, cartón y cinta? |
| **Carrera** | Prueba de fuego | ¿Funciona mi idea en la calle? |
| **Barrio** | Escenario de vida | ¿Dónde vivo, exploro y compito? |
| **Clan** | Red social | ¿Con quién comparto esto? |

**Regla de diseño:** Si una feature mejora el vehículo pero no la creatividad, el ingenio, la exploración, la comunidad o la mejora personal — **cuestionarla**.

---

## 5. Fantasía del jugador

> *"Soy un chico de barrio. Con lo que encuentro en la calle, armo un carro. Conozco un atajo que nadie más usa. Mi clan y yo organizamos carreras los sábados. Cada semana mi creación es un poco mejor."*

### Lo que el jugador dice (ideal)

- *"Mirá lo que le puse al motor."*
- *"Por acá es más rápido — confiá."*
- *"Nuestro clan ganó el torneo del barrio."*
- *"Encontré neumáticos nuevos detrás del almacén."*
- *"Mi auto era una caja de fruta — ahora le gana a la de Juan."*

### Lo que el jugador NUNCA dice

- *"Compré el auto legendario."*
- *"No importa qué piezas tenga, gana el que paga."*
- *"Este mapa podría ser cualquier ciudad."*
- *"Destruí al otro."*

---

## 6. Emociones objetivo

| Momento | Emoción | Ejemplo |
|---|---|---|
| Encontrar material raro | Curiosidad + emoción | "¡Un motor viejo en el taller!" |
| Construir / mejorar pieza | Orgullo creativo | "Le puse ruedas grandes y va mejor" |
| Descubrir atajo | Satisfacción secreta | "Nadie conoce este callejón" |
| Preparar carrera | Anticipación | "Esta vez sí le gano" |
| Carrera reñida | Tensión alegre | Derrape cartoon, casi ganas |
| Ganar | Alegría + validación | "Mi idea funcionó" |
| Perder | Ganas de mejorar (no frustración tóxica) | "Le falta agarre — le cambio las ruedas" |
| Evento de clan | Pertenencia | "Corremos juntos el sábado" |
| Desbloquear barrio nuevo | Asombro + curiosidad | "¿Qué hay en el barrio de al lado?" |

---

## 7. Filtro de decisiones

Antes de aprobar **cualquier** idea (feature, misión, pieza, circuito, UI, economía):

### Test de identidad (5 preguntas)

| # | Pregunta | Si "no" → |
|---|---|---|
| 1 | ¿Refuerza creatividad, ingenio, exploración, comunidad o mejora personal? | Replantear o descartar |
| 2 | ¿El vehículo sigue siendo consecuencia, no objetivo? | Rediseñar |
| 3 | ¿Se siente barrio latinoamericano infantil, no genérico? | Ajustar |
| 4 | ¿La competencia es sana, nunca agresiva? | Eliminar |
| 5 | ¿Un niño de 10 años entendería por qué esto es divertido? | Simplificar |

### Ejemplos de filtro en acción

| Idea propuesta | ¿Pasa? | Por qué |
|---|---|---|
| Tienda de autos prefabricados de fábrica | ❌ | Contradice creatividad y reciclaje |
| Atajo por sitio eriazo | ✅ | Exploración + ingenio en carrera |
| Sistema de clanes del barrio | ✅ | Comunidad |
| Combates con armas entre vehículos | ❌ | Anti-competencia sana |
| Pieza "motor legendario" sin craft | ❌ | Pay-to-win / sin construcción |
| Descubrir material en callejón | ✅ | Exploración + creatividad |
| Ranking global agresivo con insultos | ❌ | Comunidad tóxica |
| Torneo semanal del clan | ✅ | Comunidad + competencia sana |
| Skins cosméticos de cinta y color | ✅ | Creatividad (si no dan ventaja) |

---

## 8. Relación con otros documentos

```
docs/game/GAME_IDENTITY.md          ← ESTE DOCUMENTO
        │
        ├── docs/game/GAMEPLAY_GUIDE.md
        ├── docs/game/RACE_DESIGN_GUIDE.md
        ├── docs/game/CLAN_SYSTEM_GUIDE.md
        ├── docs/game/PROGRESSION_GUIDE.md
        ├── docs/systems/VEHICLE_DESIGN_GUIDE.md
        ├── docs/systems/ECONOMY_GUIDE.md
        ├── lore/                          ← Coherencia del mundo
        └── agents/creative_director.md      ← Filtro operativo
```

| Documento | Relación con identidad |
|---|---|
| docs/art/ART_STYLE_GUIDE | Visualiza el ADN — barrio cuidado, reciclaje limpio |
| docs/world/NEIGHBORHOOD_DESIGN | Materializa exploración — callejones, atajos, POIs |
| docs/art/GAME_ART_BIBLE | Constitución de producción — no contradice identidad |
| lore/ | Responde "por qué" del mundo sin contradecir pilares |

**Precedencia para gameplay:**

```
GAME_IDENTITY  >  GAMEPLAY_GUIDE  >  guías específicas  >  prompt / idea suelta
```

---

## 9. GLOBAL IDENTITY RULES

| ID | Regla |
|---|---|
| **I-001** | El juego no trata sobre autos — trata sobre creatividad e ingenio. |
| **I-002** | El vehículo es herramienta de expresión, no objetivo final. |
| **I-003** | Toda feature debe reforzar al menos un pilar (§3). |
| **I-004** | Competencia siempre sana — nunca violencia, agresión ni humillación. |
| **I-005** | Progresión por explorar, reciclar y construir — no por comprar poder. |
| **I-006** | El barrio es personaje — explorarlo es gameplay, no decoración. |
| **I-007** | Reciclaje = limpio, funcional, ingenioso — nunca basura sucia. |
| **I-008** | Comunidad (clanes, amigos) es pilar — no optional endgame. |
| **I-009** | Toda idea nueva pasa el test de identidad (§7) antes de implementarse. |
| **I-010** | Si dudas si algo pertenece al juego, vuelve a §1. |

---

## Apéndice — Mantra del equipo

```
Construí con lo que tenés.
Conocé cada rincón.
Competí con ingenio.
Mejorá tu creación.
Hacelo en comunidad.
```

---

*Fin de GAME_IDENTITY.md*
