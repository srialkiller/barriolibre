# ART_STYLE_GUIDE.md
## Carreras de Barrio — Guía Artística Oficial

**Proyecto:** Carreras de Barrio  
**Motor:** Rust + Bevy Engine  
**Perspectiva:** 2.5D — cámara isométrica fija  
**Pipeline de assets:** Agent Sprite Forge (`generate2dsprite`, `generate2dmap`)  
**Versión del documento:** 1.0  
**Estado:** Estándar obligatorio para todos los assets del proyecto

---

> Este documento es la fuente de verdad visual del juego. Todo sprite, tileset, prop, vehículo, personaje y mapa generado durante el desarrollo **debe** cumplir estas especificaciones. Cualquier prompt de generación debe incluir una referencia explícita a este documento y a la sección **GLOBAL ART RULES**.

---

## Tabla de contenidos

1. [Dirección artística](#1-dirección-artística)
2. [Cámara isométrica](#2-cámara-isométrica)
3. [Iluminación](#3-iluminación)
4. [Escala y proporciones](#4-escala-y-proporciones)
5. [Paleta de colores](#5-paleta-de-colores)
6. [Materiales](#6-materiales)
7. [Nivel de detalle](#7-nivel-de-detalle)
8. [Pipeline técnico (Bevy + Agent Sprite Forge)](#8-pipeline-técnico-bevy--agent-sprite-forge)
9. [GLOBAL ART RULES](#9-global-art-rules)

---

## 1. Dirección artística

### 1.1 Identidad visual

**Carreras de Barrio** es un juego de carreras infantiles ambientado en un barrio popular latinoamericano. Los niños compiten con vehículos caseros construidos con materiales reciclados. El tono es alegre, optimista y lleno de inventiva — nunca violento, nunca sombrío, nunca realista-gritty.

| Pilar | Descripción |
|---|---|
| **Estilo cartoon** | Formas simplificadas, siluetas legibles, expresividad exagerada pero controlada. Inspiración: animación latinoamericana contemporánea (ej. estética de series infantiles regionales), no anime japonés ni estilo Disney clásico. |
| **Inspiración latinoamericana** | Arquitectura de vivienda popular, veredas irregulares, muros de ladrillo visto, rejas, toldos de colores, grafitis amistosos, murales comunitarios, cartelería pintada a mano. |
| **Barrio popular** | Calles estrechas, casas pegadas, patios compartidos, cables eléctricos visibles, poca simetría urbanística. Sensación de comunidad, no de suburbio ordenado ni de centro urbano. |
| **Ambiente alegre** | Colores cálidos dominantes, cielo despejado, vegetación viva, detalles que transmiten juego y convivencia (pelotas, cometas, ropa tendida, juguetes abandonados). |
| **Aventuras infantiles** | Protagonistas niños (8–12 años visuales). Escala, proporciones y expresiones orientadas a público infantil/familiar. Sin contenido adulto, sin ironía oscura. |
| **Competencia sana** | Expresiones de esfuerzo y alegría, no agresión. Los vehículos son ingeniosos, no armas. Polvo, chispas y efectos cómicos — nunca daño realista. |
| **Objetos reciclados** | Todo vehículo y muchos props muestran origen reutilizado: cajas de fruta, bidones, neumáticos, pallets, chapas, caños PVC, cinta adhesiva, sogas. |
| **Vehículos caseros** | Ningún vehículo parece de fábrica. Ruedas desparejadas, asientos improvisados, motores expuestos, paragolpes de madera, volantes de bicicleta. Cada uno tiene personalidad. |

### 1.2 Lo que SÍ es este juego

- Un barrio colorido donde los chicos inventan carros con lo que encuentran.
- Estética **clean HD hand-painted**: ilustración digital limpia, bordes definidos, colores planos con sombreado suave — **no pixel art retro**.
- Mundo reconocible para niños de América Latina (y universalmente accesible).
- Humor visual físico y gentil (un bidón que se tambalea, una rueda que patina).

### 1.3 Lo que NO es este juego

- Realismo fotográfico o estilo grunge sucio.
- Cyberpunk, post-apocalíptico, o distópico.
- Pixel art 16-bit / retro JRPG (salvo referencia explícita futura).
- Estilo norteamericano suburbial (casas grandes, jardines perfectos, pick-ups).
- Violencia, armas, sangre, o competencia agresiva.
- Vehículos de marca reconocible o diseños de fábrica pulidos.

### 1.4 Referencias de tono (no copiar)

- Inventiva de go-karts caseros y carros de carreras de soapbox derby, pero con sabor barrial latino.
- Calidez visual de animación infantil latinoamericana.
- Caos ordenado de dioramas isométricos tipo juego de estrategia casual, pero más orgánico e irregular.

---

## 2. Cámara isométrica

> **Regla absoluta:** Todos los sprites prerenderizados deben pintarse como si fueran fotografiados desde **una única cámara virtual fija**. No mezclar ángulos frontales, laterales puros, top-down puro ni perspectivas dramáticas.

### 2.1 Proyección

| Parámetro | Valor exacto | Notas |
|---|---|---|
| **Tipo de proyección** | Isométrica 2:1 (dimetric) | Ratio horizontal:vertical de la base del diamante = **2:1** |
| **Ángulo de elevación** | **30°** sobre el plano horizontal | Ángulo entre el rayo de cámara y el suelo |
| **Ángulo azimutal (rotación horizontal)** | **45°** | Cámara orientada hacia el **cuadrante noreste (NE)** del mundo |
| **Inclinación del horizonte** | **0°** (horizonte paralelo al borde superior del frame) | Sin dutch angle, sin inclinación dramática |
| **FOV efectivo** | Ortográfico / paralelo | Sin distorsión de perspectiva convergente; líneas paralelas permanecen paralelas |
| **Relación de aspecto del tile base** | **256 × 128 px** (2:1) | Tile diamante de referencia para suelos y cuadrícula |

### 2.2 Orientación del mundo

```
                    N (fondo del mapa, lejos de cámara)
                    ↑
                    |
         Oeste ←----+----→ Este
                    |
                    ↓
                    S (frente del mapa, cerca de cámara)

Cámara: posicionada al Suroeste (SW), mirando hacia Nordeste (NE)
```

| Eje del mundo | Dirección visible en pantalla |
|---|---|
| **Eje X+ (Este)** | Diagonal hacia abajo-derecha ↘ |
| **Eje Z+ (Norte)** | Diagonal hacia arriba-derecha ↗ |
| **Eje Y+ (Altura)** | Vertical ↑ en pantalla |

### 2.3 Convenciones de orientación para sprites

Todos los objetos direccionales (vehículos, personajes, puertas, carteles) usan **4 direcciones isométricas**:

| Dirección | Código | Descripción | Ángulo respecto al eje X+ del mundo |
|---|---|---|---|
| **Sur-Este (SE)** | `se` | Cara visible hacia la cámara — **vista frontal por defecto** | 135° |
| **Sur-Oeste (SW)** | `sw` | Perfil izquierdo isométrico | 225° |
| **Nor-Oeste (NW)** | `nw` | Vista trasera | 315° |
| **Nor-Este (NE)** | `ne` | Perfil derecho isométrico | 45° |

**Dirección por defecto para concept art y props únicos:** `se` (cara principal hacia el jugador).

### 2.4 Altura de cámara

| Parámetro | Valor |
|---|---|
| **Altura virtual de cámara** | **12 unidades** sobre el plano Y=0 (suelo) |
| **Punto de mira (look-at)** | Centro del tile a nivel Y=0 |
| **Distancia virtual al origen** | **~20.8 unidades** (calculada: 12 / tan(30°) ≈ 20.78) |
| **Altura visible de un tile** | 128 px = 1 unidad de mundo |

La cámara **no se mueve, no rota, no hace zoom** durante el gameplay. Todos los assets se prerenderizan con esta configuración.

### 2.5 Reglas de volumen en isométrico

- **Caras superiores (top faces):** visibles; ocupan ~40% de la silueta en objetos bajos, ~25% en objetos altos.
- **Caras laterales:** dos caras visibles siempre (izquierda y derecha isométrica); la cara frontal SE es la más iluminada.
- **Caras ocultas:** nunca se pintan; no hay "cutaway" salvo props específicos aprobados.
- **Sombras en suelo:** se proyectan hacia **SW** (abajo-izquierda en pantalla), alineadas con la luz principal.

### 2.6 Checklist de cámara para cada asset

- [ ] ¿La base del objeto es un diamante 2:1 o un rectángulo alineado a los ejes isométricos?
- [ ] ¿Se ven exactamente dos caras laterales + la cara superior (si aplica)?
- [ ] ¿La cara SE es la más iluminada?
- [ ] ¿La sombra cae hacia abajo-izquierda (SW)?
- [ ] ¿No hay perspectiva convergente (líneas de fuga)?
- [ ] ¿El objeto está orientado en una de las 4 direcciones isométricas?

---

## 3. Iluminación

> **Regla absoluta:** Una sola configuración de iluminación para todo el juego. No hay ciclo día/noche en assets base (reservado para posproceso futuro).

### 3.1 Configuración global

| Parámetro | Valor |
|---|---|
| **Horario narrativo** | **Media mañana soleada (~10:00 h)** |
| **Clima** | Despejado, cielo azul con pocas nubes blancas |
| **Temperatura de color** | **5800 K** (luz diurna neutra-cálida) |
| **Exposición general** | Alta; escena luminosa sin zonas de oscuridad profunda |
| **Contraste global** | Medio-bajo; no hay negros puros (#000000) en superficies iluminadas |

### 3.2 Luz principal (sol)

| Parámetro | Valor |
|---|---|
| **Tipo** | Luz direccional única (sol) |
| **Dirección** | Desde **Nor-Este (NE)**, elevación **55°** sobre el horizonte |
| **Vector de luz normalizado** | `(0.5, 0.82, -0.28)` en espacio mundo (X, Y, Z) |
| **Intensidad** | **1.0** (referencia) |
| **Color** | `#FFF5E6` (blanco cálido ligeramente amarillento) |

**Efecto en sprites isométricos:**
- Cara SE (frontal-derecha): **luz plena** — tono base del material.
- Cara SW (frontal-izquierda): **luz media** — tono base oscurecido ~15%.
- Cara superior: **luz alta** — tono base aclarado ~10%.
- Cara NW/NE (traseras): **luz baja** — tono base oscurecido ~25–30%.

### 3.3 Luz ambiente / rebotes

| Parámetro | Valor |
|---|---|
| **Luz ambiente (fill)** | **0.35** intensidad |
| **Color ambiente** | `#87CEEB` (cielo azul claro — rebote del cielo) |
| **Rebote en suelo** | `#E8DCC8` (tono arena/cemento cálido) afecta la parte inferior de objetos |
| **Rebote en paredes claras** | `#F5F0E8` sutil en caras SW de objetos junto a muros |

No hay luces puntuales adicionales en los assets base. Farolas, focos de garaje, etc. son detalle visual sin contribución de luz real (no emiten halo ni cambian iluminación de vecinos).

### 3.4 Sombras

| Parámetro | Valor |
|---|---|
| **Tipo** | Sombra proyectada dura-cartoon (hard-soft edge) |
| **Dirección de proyección** | Hacia **SW** (opuesta a la luz NE) |
| **Longitud de sombra** | ~**0.6×** la altura del objeto (en unidades de tile) |
| **Opacidad de sombra en suelo** | **35%** negro `#000000` |
| **Opacidad de sombra en objeto (AO)** | **15–20%** en uniones y contactos |
| **Borde de sombra** | Semi-suave: transición de 2–3 px (en resolución de referencia 256 px/tile) |
| **Color de sombra** | `#3A3A5C` con 35% opacidad — tinte azul-violeta (no gris neutro) |
| **Sombras bajo ruedas/contacto** | Elipse oscura compacta, opacidad 45%, bajo cada punto de contacto |

**Sombras de contacto (ambient occlusion):**
- Bajo objetos apoyados en suelo: franja oscura de 3–5 px.
- En esquinas internas de vehículos caseros: oscurecimiento sutil (cinta, uniones).
- Bajo alero de techos: franja de sombra de 4–6 px en la pared debajo.

### 3.5 Horario del día (política de assets)

| Fase | Uso |
|---|---|
| **Media mañana (default)** | **100% de los assets base.** Obligatorio. |
| **Atardecer / noche / lluvia** | Solo via postproceso de Bevy o variantes de mapa explícitamente solicitadas. **No generar assets base con otra iluminación.** |

---

## 4. Escala y proporciones

> **Unidad de referencia:** 1 unidad de mundo = 128 px de altura de tile isométrico.  
> **Referencia humana:** Niño protagonista promedio = **1.0 u** de altura total (de pies a coronilla).

### 4.1 Tabla maestra de escala

| Elemento | Altura (u) | Ancho aprox. (u) | Profundidad aprox. (u) | Notas |
|---|---|---|---|---|
| **Niño (8–12 años)** | **1.00** | 0.40 | 0.30 | Referencia base absoluta |
| **Vehículo casero (small)** | 0.55 | 0.90 | 0.70 | Go-kart de caja; niño sentado asoma |
| **Vehículo casero (medium)** | 0.70 | 1.20 | 0.85 | Carro de bidones + tabla |
| **Vehículo casero (large)** | 0.85 | 1.50 | 1.00 | Camioncito de chapa; máximo del juego |
| **Casa (1 piso)** | 2.20 | 2.00 | 1.80 | Incluye techo; base ocupa ~2×2 tiles |
| **Casa (2 pisos)** | 3.50 | 2.00 | 1.80 | Barrio popular, no torre |
| **Garaje / galpón** | 1.80 | 2.50 | 2.00 | Puerta baja, estructura simple |
| **Árbol (mediano)** | 2.50 | 1.60 (copa) | 1.60 (copa) | Tronco 0.60 u, copa redonda |
| **Árbol (grande)** | 3.50 | 2.20 (copa) | 2.20 (copa) | Sombra amplia |
| **Poste de luz** | 2.80 | 0.15 | 0.15 | Lámpara incluida |
| **Basurero / tacho** | 0.55 | 0.40 | 0.40 | Altura hasta la cintura del niño |
| **Vereda (ancho)** | — | 1.20 | — | A lo largo de la calle |
| **Calzada (ancho)** | — | 2.50 | — | Suficiente para 2 vehículos |
| **Cerca / reja (altura)** | 1.00 | — | — | Hasta pecho del niño |
| **Muro de ladrillo** | 1.20 | — | — | Muro de medianera típico |

### 4.2 Relaciones visuales clave

```
Casa (1 piso)     ████████████████████████  2.20 u
Árbol grande      ████████████████████████████████  3.50 u
Poste de luz      ██████████████████████████  2.80 u
Garaje            ██████████████████  1.80 u
Niño              ██████████  1.00 u
Basurero          █████  0.55 u
Vehículo small    █████  0.55 u (pero 0.90 u ancho)
```

- Un **vehículo small** es tan bajo como un basurero pero **casi tan ancho como un niño es alto**.
- Una **casa de 1 piso** es ~2.2× un niño; un niño le llega a la ventana baja.
- Un **garaje** es más bajo que una casa pero más ancho; entra 1 vehículo medium.
- Un **poste de luz** sobrepasa el techo de una casa de 1 piso por ~0.6 u.
- Un **árbol mediano** es similar en altura a un poste; un **árbol grande** supera la casa de 1 piso.

### 4.3 Escala de tiles

| Tile | Dimensiones px | Dimensiones mundo |
|---|---|---|
| **Tile de suelo base** | 256 × 128 | 1.0 × 0.5 u (diamante 2:1) |
| **Tile de pared (altura 1 u)** | 256 × 256 | 1.0 u alto × 1.0 u ancho isométrico |
| **Celda de sprite (personaje/vehículo)** | 384 × 384 | Área segura para objetos animados |
| **Celda de prop compacto** | 256 × 256 | Props estáticos pequeños |

### 4.4 Reglas de coherencia de escala

1. **Nunca** un vehículo casero más alto que 0.85 u (debe verse claramente más bajo que un niño de pie).
2. **Nunca** un niño más grande que 1.05 u ni más pequeño que 0.95 u entre sprites distintos.
3. **Casas** siempre ocupan mínimo 2×2 tiles de base.
4. **Props compactos** (basurero, caja, bidón) deben compartir la misma escala relativa en todos los packs.
5. Al colocar un niño junto a su vehículo: la cabeza del niño sentado queda ~0.15 u por encima del borde del vehículo.

---

## 5. Paleta de colores

> **Formato:** `#RRGGBB` — todos los valores son el **tono base en luz plena (cara SE)**. Aplicar las reglas de iluminación (§3) para caras en sombra.

### 5.1 Principios de color

- Paleta **cálida y saturada** pero no neón (excepto acentos puntuales).
- Máximo **6 colores dominantes** por escena; el resto son variantes ±15% luminosidad.
- Evitar blancos puros (#FFFFFF) en superficies grandes; usar `#F5F0E8` como blanco del barrio.
- Evitar negros puros (#000000) en sombras de superficie; mínimo `#3A3A5C`.
- Colores de acento (grafitis, toldos, vehículos): vivos pero armonizados con la paleta base.

### 5.2 Colores de terreno y suelo

| Material | Tono base (SE) | Tono sombra (SW) | Tono luz (top) | Uso |
|---|---|---|---|---|
| **Cemento / vereda** | `#B8B0A4` | `#8A8278` | `#D4CCC0` | Veredas, pilares, bordes |
| **Asfalto / calle** | `#6B6860` | `#4A4840` | `#858278` | Calzada, caminos |
| **Pasto** | `#6AAF4A` | `#4A8830` | `#82C860` | Jardines, canteros, plazas |
| **Tierra / barro** | `#A08058` | `#705840` | `#B89868` | Caminos de tierra, baldíos |
| **Arena / ripio** | `#C8B898` | `#988868` | `#DED0B0` | Estacionamientos, fondos |

### 5.3 Colores de construcción

| Material | Tono base (SE) | Tono sombra (SW) | Tono luz (top) | Uso |
|---|---|---|---|---|
| **Pared (blanca)** | `#F0E8D8` | `#C8C0B0` | `#FAF5EC` | Casas encaladas |
| **Pared (ocre/amarillo)** | `#E8C878` | `#B89848` | `#F0D890` | Casas coloridas |
| **Pared (ladrillo visto)** | `#B86848` | `#883828` | `#D08058` | Muros, medianeras |
| **Pared (celeste)** | `#78B8D8` | `#5090B0` | `#90C8E8` | Clásico barrio latino |
| **Pared (rosa/salmón)** | `#E8A090` | `#B87068` | `#F0B8A8` | Casas populares |
| **Techo (chapa)** | `#688898` | `#486070` | `#88A8B8` | Techo de zinc/chapa ondulada |
| **Tejo/teja** | `#A85840` | `#783028` | `#C07050` | Techo de barro |
| **Hormigón crudo** | `#989088` | `#706860` | `#B0A8A0` | Muros, veredas rotas |

### 5.4 Colores de materiales industriales

| Material | Tono base (SE) | Tono sombra (SW) | Tono luz (top) | Uso |
|---|---|---|---|---|
| **Madera (nueva)** | `#A87840` | `#784820` | `#C09858` | Estructuras recientes |
| **Madera (vieja)** | `#887048` | `#584828` | `#A08860` | Palets, tablas recicladas |
| **Metal (limpio)** | `#909098` | `#686870` | `#A8A8B0` | Caños, chapas nuevas |
| **Metal (oxidado)** | `#8B5A3C` | `#5A3820` | `#A87050` | Chapa vieja, rieles |
| **Plástico (reciclado)** | `#58A8C8` | `#388098` | `#70C0E0` | Bidones, botellas, canaletas |
| **Plástico (colorido)** | `#E85050` | `#B83030` | `#F07070` | Cajas, baldes (variar matiz) |
| **Óxido intenso** | `#7A4028` | `#502818` | `#985040` | Manchas, bordes corroídos |
| **Neumático (goma)** | `#383830` | `#202018` | `#504840` | Ruedas, colchones de goma |
| **Cartón** | `#B89868` | `#887048` | `#D0B080` | Cajas de fruta, asientos |

### 5.5 Colores de vegetación

| Material | Tono base (SE) | Tono sombra (SW) | Tono luz (top) | Uso |
|---|---|---|---|---|
| **Follaje (normal)** | `#5A9838` | `#387020` | `#72B050` | Árboles, arbustos |
| **Follaje (claro)** | `#78B848` | `#589028` | `#90D060` | Brotes, pasto soleado |
| **Follaje (sombra)** | `#406828` | `#284818` | `#588840` | Interior de copas |
| **Tronco** | `#685030` | `#483820` | `#806848` | Troncos, ramas gruesas |
| **Flores (acento)** | `#E84888` | `#B82868` | `#F068A0` | Buganvillas, macetas |

### 5.6 Colores de acento (uso limitado)

| Acento | Color | Uso máximo |
|---|---|---|
| **Amarillo señalética** | `#F0D020` | Señales, cinta, detalles |
| **Naranja vivo** | `#F08828` | Conos, banderas, toldos |
| **Rojo acento** | `#D84040` | Grafitis, carteles, faroles |
| **Celeste acento** | `#40A8D8` | Toldos, macetas, pintura |
| **Violeta acento** | `#8868B8` | Grafitis, murales |

No más de **2 colores de acento** por asset individual.

---

## 6. Materiales

> Cada material tiene un **lenguaje visual fijo**. Al generar prompts, nombrar el material y seguir su descripción.

### 6.1 Madera vieja

| Atributo | Especificación |
|---|---|
| **Color** | `#887048` base, vetas `#584828` |
| **Textura** | Vetas longitudinales cada 8–12 px; nudos ocasionales (círculos de 4–6 px, tono `#684830`) |
| **Bordes** | Irregulares, astillados en 1–2 px; no bordes perfectos |
| **Brillo** | Mate; sin reflejo especular |
| **Detalle extra** | Clavos oxidados (`#7A4028`), grietas finas (línea 1 px, `#584828`) |
| **Uso típico** | Palets, paragolpes, asientos, rampas |

### 6.2 Metal oxidado

| Atributo | Especificación |
|---|---|
| **Color base** | `#8B5A3C` con manchas `#7A4028` (óxido) y `#686870` (metal sano) |
| **Textura** | Manchas irregulares de óxido (manchas orgánicas, no ruido); rayado horizontal en chapas |
| **Brillo** | Mate con puntos de brillo tenue (`#A0A0A8`, 1–2 px) solo en bordes afilados |
| **Bordes** | Dentados, doblados; bordes superiores con óxido más intenso |
| **Detalle extra** | Tornillos (`#505050`, círculo 2–3 px), remaches, abolladuras suaves |
| **Uso típico** | Carrocerías, rieles, chapas de techo, bidones viejos |

### 6.3 Neumáticos

| Atributo | Especificación |
|---|---|
| **Color** | `#383830` base, `#202018` en surcos |
| **Textura** | Surcos circunferenciales cada 4–6 px; patrón de banda de rodadura simplificado |
| **Forma** | Cilindro isométrico; círculo elíptico visto en isométrico (ratio 2:1) |
| **Brillo** | Mate total |
| **Detalle extra** | Borde liso en la banda de rodadura (1 px `#504840`); desgaste irregular |
| **Uso típico** | Ruedas de vehículos, colchones de goma, decoración |

### 6.4 Cartón

| Atributo | Especificación |
|---|---|
| **Color** | `#B89868` base, `#887048` en pliegues |
| **Textura** | Pliegue central horizontal; línea de doblez (1 px, tono sombra) |
| **Brillo** | Mate; fibras sutiles (líneas finas `#A88858`, espaciadas 6 px) |
| **Bordes** | Esquinas ligeramente dobladas/arrugadas |
| **Detalle extra** | Etiquetas borrosas (rectángulos de color desaturado, **sin texto legible**), cinta adhesiva en uniones |
| **Uso típico** | Asientos, carrocería de go-kart, cajas apiladas |

### 6.5 Plástico reciclado

| Atributo | Especificación |
|---|---|
| **Color** | Variable según §5.4; base `#58A8C8` (bidón) o `#E85050` (balde) |
| **Textura** | Superficie lisa con brillo suave; costuras de molde (línea tenue horizontal) |
| **Brillo** | Semi-brillante: highlight elíptico 3–5 px, blanco 20% opacidad, en cara SE |
| **Bordes** | Redondeados; tapa/rosca con estrías (líneas finas radiales) |
| **Detalle extra** | Etiquetas parcialmente arrancadas (mancha clara), abolladuras |
| **Uso típico** | Bidones, botellas, canaletas, paneles de carrocería |

### 6.6 Telas

| Atributo | Especificación |
|---|---|
| **Color** | Variable; preferir colores desaturados o estampados simples |
| **Textura** | Pliegues suaves (curvas de 2 px, tono ±10%); costura visible en bordes (línea punteada 1 px) |
| **Brillo** | Mate; sin reflejo |
| **Bordes** | Ondulados, no rectos; flecos ocasionales |
| **Detalle extra** | Parches de otro color, remiendos, manchas tenues |
| **Uso típico** | Asientos, toldos, banderas, ropa tendida (decoración de fondo) |

### 6.7 Cinta adhesiva (duct tape / cinta aisladora)

| Atributo | Especificación |
|---|---|
| **Color plata/gris** | `#909088` (duct tape) |
| **Color negro** | `#383830` (cinta aisladora) |
| **Color amarillo** | `#E8C820` (cinta de embalaje, acento) |
| **Textura** | Banda diagonal o cruzada; bordes ligeramente despegados (1 px highlight) |
| **Brillo** | Semi-mate |
| **Regla** | Toda unión improvisada de vehículo casero **debe** mostrar al menos una cinta adhesiva |
| **Uso típico** | Uniones de carrocería, reparaciones, sujeción de accesorios |

---

## 7. Nivel de detalle

### 7.1 Filosofía

El juego usa estilo **clean HD hand-painted cartoon**: suficiente detalle para transmitir materiales reciclados y personalidad barrial, pero sin textura fotorrealista ni ruido visual. La legibilidad a tamaño de juego (tiles de 256 px, viewport ~1280×720) es prioritaria.

### 7.2 Cantidad de detalle

| Categoría | Nivel | Directriz |
|---|---|---|
| **Personajes** | Medio-alto | Cara expresiva (ojos, boca), ropa con 2–3 colores, manos simplificadas (4 dedos cartoon) |
| **Vehículos caseros** | Alto | Materiales visibles, uniones con cinta, ruedas diferenciadas, accesorios |
| **Casas / edificios** | Medio | Ventanas, puertas, techo con textura; sin ladrillo individual en paredes enteras |
| **Props compactos** | Bajo-medio | Silueta clara + 1–2 detalles identificativos |
| **Terreno / tiles** | Bajo | Textura sugerida, no tileada repetitiva obvia; grietas, manchas, hierba puntual |
| **Vegetación** | Medio | Copa con 2–3 tonos de verde; tronco simple; sin hojas individuales |
| **FX (polvo, chispas)** | Bajo | Formas simples, 3–5 colores, legibles en movimiento |

### 7.3 Grosor de líneas (outline)

| Contexto | Grosor | Color |
|---|---|---|
| **Personajes y vehículos** | **2 px** a resolución 384 px | `#2A2030` (morado-oscuro, no negro puro) |
| **Props compactos** | **1.5–2 px** a resolución 256 px | `#2A2030` |
| **Edificios y estructuras** | **1.5 px** a resolución 256 px | `#2A2030` o `#3A2830` |
| **Tiles de terreno** | **Sin outline** | Borde definido por cambio de color/sombra |
| **Vegetación** | **1 px** en tronco; **sin outline** en copa | Tronco: `#483820` |
| **FX y partículas** | **Sin outline** | Formas a color |

**Regla:** El outline es **consistente en todo el objeto**; no variar grosor dentro de un mismo sprite salvo transiciones suaves en curvas (anticráneo mínimo).

### 7.4 Texturas

| Tipo | Método | Prohibido |
|---|---|---|
| **Superficies planas** | Bloques de color + 1 banda de sombra | Ruido aleatorio, filtros de grano |
| **Superficies orgánicas** | Manchas suaves de 2–3 tonos | Texturas fotográficas |
| **Patrones repetitivos** | Cada 16–32 px máximo | Patrones obvios de tile (< 8 px) |
| **Materiales reciclados** | Combinación de sub-materiales con borde claro | Mezcla borrosa entre materiales |

### 7.5 Bordes y esquinas

- **Estilo cartoon:** esquinas ligeramente redondeadas (radio 2–4 px en props de 256 px).
- **Objetos improvisados:** esquinas irregulares, no geométricamente perfectas.
- **Edificios:** esquinas rectas isométricas (ángulos exactos de proyección).
- **Transición suelo/objeto:** sombra de contacto (§3.4), nunca borde duro sin sombra.

### 7.6 Sombras y volumen

| Técnica | Aplicación |
|---|---|
| **Cel-shading suave** | 2–3 niveles de tono por cara (luz, base, sombra); sin degradé fotorealista |
| **Sombra proyectada** | Elipse en suelo, dirección SW (§3.4) |
| **AO (ambient occlusion)** | Solo en uniones y contactos; 15–20% opacidad |
| **Highlight especular** | Solo en plástico (§6.5) y cristal; máximo 5 px, 20% opacidad |
| **Volumen general** | Formas construidas con caras isométricas planas; sensación 3D via tonos, no via perspectiva convergente |

### 7.7 Resolución de referencia

| Tipo de asset | Resolución mínima | Celda / canvas |
|---|---|---|
| **Tile de suelo** | 256 × 128 px | 1 tile |
| **Prop compacto** | 256 × 256 px | 1 celda |
| **Prop grande / edificio** | 512 × 512 px o multi-tile | Variable |
| **Personaje (por frame)** | 384 × 384 px | Celda de animación |
| **Vehículo (por frame)** | 384 × 384 px | Celda de animación |
| **Mapa base (foundation)** | Múltiplo de 256 px | Cuadrícula de tiles |

---

## 8. Pipeline técnico (Bevy + Agent Sprite Forge)

### 8.1 Estilo para prompts de generación

| Parámetro Agent Sprite Forge | Valor para Carreras de Barrio |
|---|---|
| `art_style` | `project-native` (referencia: este documento) |
| `view` | `3/4` (equivalente isométrico 2:1) |
| `perspective` (mapas) | `isometric-like` |
| `map_mode` | `tile_mode` o `scene_mode` según contexto |
| `visual_model` | `layered_raster` + props separados |
| Fondo de generación (sprites) | Sólido `#FF00FF` (magenta) para chroma-key |

### 8.2 Estructura de carpetas de assets

```
assets/
├── sprites/          # Personajes, vehículos, FX (generate2dsprite)
│   └── <slug>/
│       ├── raw-sheet.png
│       ├── sheet-transparent.png
│       └── prompt-used.txt
├── maps/             # Mapas base y capas (generate2dmap)
│   └── <slug>/
│       ├── <name>-base.png
│       └── <name>-base.prompt.txt
├── props/            # Props extraídos de packs o individuales
│   └── <prop>/
│       └── prop.png
└── tilesets/         # Tilesets de terreno
    └── <name>.png
```

### 8.3 Integración Bevy

- **Render order:** Y-sort por posición en eje Z del mundo (objetos más al sur se dibujan encima).
- **Sprites prerenderizados:** PNG con alpha; sin rotación en runtime.
- **Direcciones:** 4 sprites por dirección isométrica (`se`, `sw`, `nw`, `ne`) o hojas de animación por dirección.
- **Anclas:** Personajes y vehículos anclados en **pies/base** (centro inferior del diamante isométrico).
- **Escala en mundo:** 1 unidad = 128 px de altura de tile.

### 8.4 Texto bloque para prompts

Al generar cualquier asset, incluir este bloque al inicio del prompt:

```
Carreras de Barrio — art style guide v1.0.
Clean HD hand-painted cartoon, Latin American neighborhood, cheerful recycled aesthetic.
Fixed isometric 2:1 camera, 30° elevation, 45° azimuth NE, view direction SE default.
Mid-morning lighting from NE (55° elevation), warm #FFF5E6, shadows toward SW at 35% opacity #3A3A5C.
Outline 2px #2A2030 on characters/vehicles, 1.5px on buildings/props.
No pixel art, no photorealism, no text, no watermarks.
```

---

## 9. GLOBAL ART RULES

> **Estas reglas son OBLIGATORIAS en TODOS los prompts de generación de assets.** Copiar o referenciar esta sección completa al generar cualquier sprite, prop, tile o mapa.

### 9.1 Identidad y estilo

1. **G-001:** Todo asset pertenece al universo visual de **Carreras de Barrio**: barrio popular latinoamericano, estilo cartoon clean HD, ambiente alegre infantil.
2. **G-002:** **Prohibido pixel art retro** salvo decisión explícita futura documentada. Usar clean HD hand-painted.
3. **G-003:** **Prohibido fotorrealismo.** Formas simplificadas, colores planos con 2–3 niveles de sombra.
4. **G-004:** **Prohibido contenido violento, sangre, armas** o tono oscuro/horror.
5. **G-005:** **Prohibido texto legible** dentro de sprites (carteles, etiquetas, grafitis = manchas de color sin letras).
6. **G-006:** **Prohibido watermarks, bordes de presentación, fondos degradé** (excepto `#FF00FF` para chroma-key en sprites).
7. **G-007:** Todo vehículo es **casero y reciclado** — nunca de fábrica, nunca de marca real.

### 9.2 Cámara

8. **G-008:** Proyección isométrica **2:1 fija**. Ángulo **30°** elevación, azimut **45° NE**.
9. **G-009:** Dirección por defecto de render: **SE** (cara principal hacia cámara).
10. **G-010:** **Prohibida perspectiva convergente.** Líneas paralelas permanecen paralelas.
11. **G-011:** Todo objeto muestra **exactamente 2 caras laterales + cara superior** (si tiene volumen).
12. **G-012:** Sprites prerenderizados — **sin rotación 3/4 intermedia**; solo las 4 direcciones isométricas.

### 9.3 Iluminación

13. **G-013:** Luz principal desde **NE**, elevación **55°**, color `#FFF5E6`, intensidad 1.0.
14. **G-014:** Sombras proyectadas hacia **SW**, opacidad **35%**, color `#3A3A5C`.
15. **G-015:** Luz ambiente **0.35**, color `#87CEEB`.
16. **G-016:** Horario fijo: **media mañana soleada**. No generar assets con iluminación de atardecer, noche o lluvia salvo solicitud explícita.
17. **G-017:** Cara SE = luz plena; cara SW = −15%; caras traseras = −25–30%; cara superior = +10%.

### 9.4 Escala

18. **G-018:** Escala relativa al **niño = 1.0 u** de altura. Respetar tabla §4.1.
19. **G-019:** Vehículos caseros: altura máxima **0.85 u**, ancho máximo **1.50 u**.
20. **G-020:** Casas ocupan mínimo **2×2 tiles** de base.
21. **G-021:** Escala consistente entre assets del mismo tipo — un basurero siempre tiene la misma altura relativa.

### 9.5 Color

22. **G-022:** Usar exclusivamente la paleta definida en §5. Variaciones permitidas: **±15% luminosidad** del tono base.
23. **G-023:** Máximo **2 colores de acento** por asset individual.
24. **G-024:** No usar blanco puro `#FFFFFF` ni negro puro `#000000` en superficies.
25. **G-025:** Materiales reciclados muestran **sub-materiales visibles** (cinta, clavo, mancha de óxido) — mínimo 1 detalle de reciclaje por vehículo.

### 9.6 Línea, textura y volumen

26. **G-026:** Outline **2 px `#2A2030`** en personajes y vehículos; **1.5 px** en edificios y props.
27. **G-027:** Cel-shading suave: **2–3 tonos** por cara, sin degradé fotorealista.
28. **G-028:** Texturas sugeridas con manchas/bandas de color — **prohibido ruido aleatorio** y texturas fotográficas.
29. **G-029:** Sombras de contacto bajo todo objeto apoyado en suelo.
30. **G-030:** Esquinas cartoon redondeadas (2–4 px) en props; esquinas isométricas exactas en edificios.

### 9.7 Materiales reciclados

31. **G-031:** Todo vehículo casero incluye **mínimo 2 materiales distintos** de §6 (ej. cartón + neumático + cinta).
32. **G-032:** Toda unión estructural improvisada muestra **cinta adhesiva** visible.
33. **G-033:** Ruedas de vehículos = **neumáticos** (§6.3), desparejados permitidos; diámetros pueden variar ±20%.
34. **G-034:** Superficies de cartón, madera vieja y metal oxidado son los **materiales dominantes** del juego.

### 9.8 Pipeline y entrega

35. **G-035:** Sprites con fondo **`#FF00FF` sólido** para postproceso chroma-key (Agent Sprite Forge).
36. **G-036:** Mapas base = **foundation-only** (solo terreno/suelo); props y objetos son assets separados.
37. **G-037:** Guardar prompt usado en `<asset>.prompt.txt` junto a cada asset generado.
38. **G-038:** Ancla de personajes/vehículos: **centro inferior (pies/base)** del sprite.
39. **G-039:** Resolución mínima: tiles 256×128, props 256×256, personajes/vehículos 384×384 por frame.
40. **G-040:** Antes de aceptar un asset, verificar checklist de cámara (§2.6) y coherencia de escala (§4.4).

### 9.4 Bloque de prompt obligatorio

Al final de **todo prompt de generación**, incluir:

```
MANDATORY RULES (Carreras de Barrio v1.0):
- Isometric 2:1, 30° elevation, NE light, SW shadows
- Clean HD cartoon, Latin American neighborhood, recycled homemade aesthetic
- No pixel art, no photorealism, no readable text, no violence
- Palette and scale per ART_STYLE_GUIDE.md
- Character anchor: bottom-center feet
```

---

## Apéndice A — Glosario

| Término | Definición |
|---|---|
| **u (unidad)** | Unidad de escala del mundo; 1 u = 128 px |
| **SE/SW/NW/NE** | Cuatro direcciones isométricas del mundo |
| **Foundation-only** | Mapa base sin props ni objetos interactivos |
| **Clean HD** | Estilo hand-painted digital limpio, no pixel art |
| **Chroma-key** | Eliminación de fondo magenta `#FF00FF` en postproceso |
| **Prop compacto** | Objeto decorativo ≤ 1 tile (256×256 px) |
| **Y-sort** | Orden de renderizado por profundidad isométrica |

## Apéndice B — Historial de versiones

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-07-05 | Documento inicial — dirección artística, cámara, iluminación, escala, paleta, materiales, detalle, reglas globales |

---

*Fin de ART_STYLE_GUIDE.md*
