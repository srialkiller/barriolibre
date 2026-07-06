# VISUAL_LANGUAGE.md
## Carreras de Barrio — Lenguaje Visual e Identidad de Diseño

**Proyecto:** Carreras de Barrio  
**Complementa:** [ART_STYLE_GUIDE.md](./ART_STYLE_GUIDE.md) (cámara, color, iluminación, materiales)  
**Versión:** 1.0  
**Estado:** Estándar obligatorio para diseño de formas, siluetas y composición

---

> Este documento define **cómo pensar y diseñar** cada objeto del juego: qué formas usar, cómo exagerar, cómo componer un sprite y qué personalidad debe transmitir. No reemplaza la guía artística — la complementa. Para color, luz y cámara, consultar `ART_STYLE_GUIDE.md`.

---

## Tabla de contenidos

1. [Filosofía de diseño](#1-filosofía-de-diseño)
2. [Shape Language](#2-shape-language)
3. [Silhouette Language por categoría](#3-silhouette-language-por-categoría)
4. [Nivel de exageración](#4-nivel-de-exageración)
5. [Reglas de composición](#5-reglas-de-composición)
6. [Legibilidad](#6-legibilidad)
7. [Personalidad de los objetos](#7-personalidad-de-los-objetos)
8. [Filosofía del reciclado creativo](#8-filosofía-del-reciclado-creativo)
9. [Reglas de modularidad visual](#9-reglas-de-modularidad-visual)
10. [GLOBAL VISUAL RULES](#10-global-visual-rules)

---

## 1. Filosofía de diseño

### 1.1 Mantras del proyecto

| Mantra | Significado |
|---|---|
| **Ingenio sobre perfección** | Lo importante no es que el auto sea bonito, sino que se vea **pensado**. Cada vehículo cuenta una historia de construcción. |
| **Reciclado creativo** | Los materiales vienen del barrio, pero el resultado es **limpio, funcional e ingenioso** — nunca basura sucia. |
| **El niño construyó eso** | El jugador debe mirar un vehículo y pensar: *"ese niño armó ese auto"*. Conexión emocional entre personaje y máquina. |
| **Formas amables, competencia sana** | Nada agresivo, nada puntiagudo, nada que intimide. Competimos con ingenio, no con violencia visual. |
| **Cuadrados que sueñan** | El lenguaje de formas es angular y simple, pero la combinación es imaginativa y alegre. |

### 1.2 Pregunta de diseño obligatoria

Antes de aprobar cualquier asset, responder:

1. ¿Se reconoce la categoría del objeto en **menos de 0.5 segundos**?
2. ¿Las formas principales son **cuadrados, rectángulos o trapecios**?
3. ¿El objeto transmite **ingenio** (no abandono ni suciedad)?
4. ¿Un niño del juego **podría haber construido o tocado** este objeto?
5. ¿La composición respeta **70 / 20 / 10**?

Si alguna respuesta es "no", rediseñar.

### 1.3 Relación entre documentos

```
ART_STYLE_GUIDE.md     →  CÓMO se ve (color, luz, cámara, materiales)
VISUAL_LANGUAGE.md     →  QUÉ formas y QUÉ personalidad (este documento)
ASSET_PIPELINE.md      →  CÓMO se produce y organiza (nombres, pivotes, carpetas)
```

---

## 2. Shape Language

### 2.1 Formas primarias permitidas

El universo visual de Carreras de Barrio se construye con **formas ortogonales suavizadas**:

| Símbolo | Forma | Uso principal |
|---|---|---|
| **○** | Círculo / elipse | Cabezas, copas de árboles, ruedas, faros, macetas |
| **□** | Cuadrado | Carrocerías, cajas, ventanas, bloques de casas, chassis |
| **▭** | Rectángulo | Piernas, tablas, techos, paragolpes, muros, asientos |
| **▱** | Trapecio | Parabrisas inclinados, techos en perspectiva, rampas, aleros |
| **⬭** | Elipse achatada | Ruedas en isométrico, sombras en suelo, bidones vistos de frente |

### 2.2 Formas secundarias permitidas

| Forma | Uso | Límite |
|---|---|---|
| **Semicírculo** | Volantes, arcos de garaje, caños | Máximo 20% de la silueta |
| **Hexágono suavizado** | Tuercas, tornillos grandes (detalle) | Solo en capa de detalle (10%) |
| **Línea gruesa** | Cinta adhesiva, cables, sogas | Como conector, no como forma principal |

### 2.3 Formas PROHIBIDAS

```
BAD — NO USAR
─────────────────────────────────────────
  △        Triángulos puntiagudos como forma dominante
  ◇        Diamantes agudos (salvo base isométrica del tile)
  ↗        Picos, astillas, spires, garras
  ★        Estrellas puntiagudas como silueta principal
  ⚡       Formas de rayo / agresivas como cuerpo del objeto
```

| Prohibido | Por qué | Alternativa |
|---|---|---|
| **Triángulos agudos** | Transmiten agresión; rompen el tono infantil | Trapecio con ángulos ≥ 100° |
| **Puntas y spires** | Formas "malvadas" o peligrosas | Redondear punta a radio ≥ 4 px |
| **Siluetas afiladas** | Parecen armas o monstruos | Ensanchar base; usar rectángulos |
| **Curvas excesivas** | Rompen la identidad angular del barrio | Máximo 2–4 curvas suaves por sprite |
| **Formas orgánicas irregulares** (excepto vegetación) | Parecen amorfas o sucias | Bloques simples + 1 curva |

### 2.4 GOOD vs BAD — Referencia visual ASCII

```
GOOD — Niño                          GOOD — Auto casero
     ┌───┐                                ┌─────────────┐
    │  ○  │  cabeza grande                 │ □  □  □  □  │  bloques apilados
    │     │                                │ ├──────┤    │  trapecio parabrisas
     └──┬──┘  torso cuadrado                │ ▭▭▭▭▭▭▭▭▭▭  │  chasis rectangular
        │                                   ○           ○   ruedas (círculos)
       ▭ ▭   piernas cortas                └─────────────┘

GOOD — Casa                          GOOD — Árbol
   ┌──────────┐                           ╭─────╮
   │          │  pared = rectángulo        │  ○  │  copa redonda
   │    □     │  ventana = cuadrado       ╭┴─────┴╮
   └────┬─────┘                           │  ▭   │  tronco = rectángulo
     ▱▱▱▱▱▱▱    techo bajo = trapecio       └──┬───┘

BAD — Formas agresivas               BAD — Demasiado orgánico
        ▲                                   ╱╲
       ╱ ╲   triángulo dominante           ╱  ╲  blob sin estructura
      ╱   ╲                                 ╱    ╲
     ╱     ╲                               ╱      ╲
```

### 2.5 Proporción de formas por sprite

| Tipo de forma | % de la silueta total | Ejemplos |
|---|---|---|
| Cuadrados y rectángulos | **60–70%** | Cuerpo, chassis, paredes, piernas |
| Trapecios | **10–15%** | Techos, parabrisas, rampas |
| Círculos / elipses | **15–25%** | Cabeza, ruedas, copas, faros |
| Triángulos | **0%** como forma principal; **≤ 3%** como detalle mínimo | Prohibido como silueta dominante |
| Curvas libres | **≤ 5%** | Solo vegetación y detalles menores |

---

## 3. Silhouette Language por categoría

### 3.1 Niños

**Fórmula de silueta:** ○ grande + □ pequeño + ▭▭ cortos

```
        ┌─────┐
       │  ○  │     Cabeza: 45–50% de la altura total
       │     │     Forma: círculo u óvalo; ojos grandes (30% del ancho de cara)
        └─┬───┘
          │       Torso: 20–25% de la altura total
         ┌┴┐      Forma: cuadrado o rectángulo vertical corto; hombros ligeramente más anchos
         │ │      Brazos: rectángulos delgados; manos simplificadas (4 dedos)
        ▭ ▭      Piernas: 25–30% de la altura total
                   Forma: dos rectángulos cortos separados; pies pequeños (semicírculo)
```

| Atributo | Regla |
|---|---|
| **Ratio cabeza:cuerpo** | **1 : 1.2** (cabeza casi del tamaño del torso+piernas juntos) |
| **Altura total** | 1.0 u (referencia absoluta — ver ART_STYLE_GUIDE §4) |
| **Ancho de silueta** | 0.40 u máximo (silueta más alta que ancha) |
| **Postura default** | Piernas separadas, brazos visibles, peso centrado |
| **Expresión** | Ojos grandes, cejas simples, boca expresiva; emociones legibles |
| **Ropa** | Bloques de color (rectángulos); sin pliegues complejos |

**Silueta reconocible a 32 px de alto:** cabeza redonda + cuerpo compacto + piernas cortas = niño cartoon.

### 3.2 Autos (vehículos caseros)

**Fórmula de silueta:** □ + ▱ + ▭ + ○○ + elementos visibles

```
    ┌─────────────────────────┐
    │  □ parabrisas (caja)    │  ← forma cuadrada/rectangular, no aerodinámica
    ├─────────────────────────┤
    │ ▭▭ chasis (tabla/caja)  │  ← cuerpo principal = rectángulo horizontal
    │  ○ motor expuesto       │  ← pieza modular visible
    │  ▭ asiento (cartón)     │  ← pieza modular visible
    ○─┴─────────────────────┴─○  ← ruedas = círculos; pueden ser desparejadas
      ▭▭ paragolpes (madera)     ← pieza modular visible
```

| Atributo | Regla |
|---|---|
| **Forma dominante** | Rectángulo horizontal (chasis) + bloques apilados |
| **Aerodinámica** | **Ninguna.** Bordes rectos, esquinas a 90° o ligeramente redondeadas (2–4 px) |
| **Elementos visibles** | Mínimo **4 piezas modulares** identificables (ruedas, motor, asiento, paragolpe, volante, escape, etc.) |
| **Asimetría** | Permitida y deseable — transmite "hecho a mano" |
| **Altura** | 0.55–0.85 u según tamaño (small / medium / large) |
| **Ancho** | 0.90–1.50 u; siempre más ancho que alto |

**Regla de lectura:** a 64 px de ancho, se deben distinguir al menos **3 piezas modulares** distintas.

### 3.3 Casas

**Fórmula de silueta:** ▭▭ + ▱ bajo + □ ventana

```
       ▱▱▱▱▱▱▱▱▱     Techo: trapecio bajo (ángulo ≤ 25°); nunca punta alta
      ┌───────────┐
      │  □    □   │    Pared: rectángulo simple; ventanas = cuadrados
      │           │
      │    ▭      │    Puerta: rectángulo vertical
      └───────────┘
```

| Atributo | Regla |
|---|---|
| **Forma dominante** | Rectángulo vertical (pared) + trapecio bajo (techo) |
| **Techos** | Bajos, casi planos; chapa ondulada sugerida con líneas horizontales, no picos |
| **Curvas** | **Prohibidas** en estructura; esquinas isométricas exactas |
| **Ventanas** | Cuadrados o rectángulos; máximo 4 por fachada visible |
| **Detalle** | Mínimo; la personalidad viene del **color de pared** y 1–2 detalles (maceta, reja) |
| **Base** | 2×2 tiles mínimo; forma de footprint = rectángulo isométrico |

### 3.4 Vegetación

**Fórmula de silueta:** ○ grande + ▭ delgado

```
         ╭───────╮
        │   ○○   │    Copa: círculo o elipse; 2–3 tonos de verde
        │  ○  ○  │    Forma redonda, nunca cónica puntiaguda
         ╰───┬───╯
             │         Tronco: rectángulo delgado (▭)
             ▭
```

| Atributo | Regla |
|---|---|
| **Copa** | Círculo, elipse o "nube" redondeada; **prohibido** ciprés puntiagudo o pino triangular |
| **Tronco** | Rectángulo simple; 15–25% de la altura total |
| **Arbustos** | Semicírculo o elipse baja sobre suelo |
| **Flores** | Círculos pequeños de acento; tallo = línea delgada |
| **Curvas** | **Permitidas** solo en vegetación; es la excepción al lenguaje angular |

### 3.5 Props y piezas modulares

**Fórmula:** una forma primaria + un detalle identificativo

| Prop | Forma primaria | Detalle (10%) |
|---|---|---|
| Basurero | ▭ cilindro | tapa semicírculo |
| Poste de luz | ▭ alto | ○ lámpara arriba |
| Bidón | ⬭ elipse | tapa + asa |
| Caja de fruta | □ | etiqueta de color |
| Neumático | ○ | surcos (líneas) |
| Motor | □ compacto | tubo de escape (▭) |

---

## 4. Nivel de exageración

### 4.1 Escala de exageración por categoría

| Categoría | Exageración | Qué exagerar | Qué NO exagerar |
|---|---|---|---|
| **Niños** | **Alta** | Cabeza, ojos, expresiones | Longitud de piernas, tamaño de manos |
| **Vehículos** | **Media-alta** | Tamaño de ruedas, motor expuesto, asimetría | Proporciones base (debe parecer un carro, no un tanque) |
| **Casas** | **Baja** | Color de pared, inclinación de techo | Dimensiones (deben ser creíbles como vivienda) |
| **Vegetación** | **Media** | Redondez de copa, saturación de verde | Altura relativa (respetar escala §4 ART_STYLE_GUIDE) |
| **Piezas modulares** | **Media** | Material reciclado visible, cinta adhesiva | Escala (deben encajar entre sí) |
| **FX (polvo, chispas)** | **Alta** | Tamaño, cantidad, duración | — |

### 4.2 Principios de exageración

1. **Exagerar la personalidad, no la anatomía realista.** Cabeza grande sí; cuello de girafa no.
2. **Exagerar la inventiva, no el caos.** Muchas piezas visibles sí; amorphous blob de chatarra no.
3. **Exagerar la legibilidad, no el detalle.** Formas grandes y claras; no micro-texturas.
4. **Un solo elemento exagerado por sprite.** Si la cabeza es muy grande, el resto se mantiene contenido.

### 4.3 Límites numéricos de exageración

| Medida | Valor normal | Exagerado permitido | Prohibido |
|---|---|---|---|
| Cabeza / altura niño | 45–50% | hasta 55% | > 60% (parece bebé) |
| Ojos / ancho de cara | 25–30% | hasta 35% | > 40% (estilo chibi extremo) |
| Ruedas / altura vehículo | 40–50% | hasta 55% | > 60% (parece tractor) |
| Motor expuesto / largo vehículo | 15–20% | hasta 30% | > 35% (parece moto) |
| Copa / altura árbol | 60–70% | hasta 75% | > 80% (sin tronco visible) |

---

## 5. Reglas de composición

### 5.1 Regla 70 / 20 / 10

Todo sprite debe distribuir su masa visual así:

```
┌─────────────────────────────────────────────┐
│                                             │
│     ┌─────────────────────────┐             │
│     │                         │             │
│     │    70% FORMA PRINCIPAL  │             │
│     │    La silueta dominante │             │
│     │    que identifica el    │             │
│     │    objeto a distancia   │             │
│     │                         │             │
│     │  ┌──────────────────┐     │             │
│     │  │ 20% SECUNDARIA   │     │             │
│     │  │ Soporte visual;  │     │             │
│     │  │ refuerza lectura │     │             │
│     │  └──────────────────┘     │             │
│     │         ·  ·  ·           │             │
│     │      10% DETALLES         │             │
│     │   Personalidad aquí       │             │
│     └─────────────────────────┘             │
│                                             │
└─────────────────────────────────────────────┘
```

| Capa | % | Función | Ejemplos |
|---|---|---|---|
| **Forma principal** | **70%** | Identidad instantánea; la silueta que se recorta | Chasis del auto, cuerpo del niño, pared de la casa, copa del árbol |
| **Forma secundaria** | **20%** | Contexto y función; refuerza qué es el objeto | Ruedas, techo, piernas, tronco, paragolpe, ventanas |
| **Detalles** | **10%** | Personalidad, historia, ingenio | Cinta adhesiva, sticker, mancha de pintura, tuerca visible, pegatina, chapitas |

### 5.2 Aplicación por categoría

**Niño:**
- 70% = cabeza + torso (bloque superior)
- 20% = piernas + brazos
- 10% = expresión facial, accesorio (gorra, remera estampada), mancha de tierra

**Vehículo casero:**
- 70% = chasis / cuerpo principal (el bloque más grande)
- 20% = ruedas + parabrisas / estructura superior
- 10% = motor expuesto, cinta, volante, escape, calcomanía, tuerca

**Casa:**
- 70% = pared principal (rectángulo de color)
- 20% = techo + puerta
- 10% = ventanas, maceta, reja, tendedero, grafiti amistoso

**Árbol:**
- 70% = copa (círculo verde)
- 20% = tronco
- 10% = frutos, flor, nido, cinta en tronco

### 5.3 Reglas de distribución

1. **La forma principal toca al menos 2 bordes** del bounding box del sprite (ancla visual).
2. **Los detalles nunca compiten** con la forma principal en tamaño o contraste.
3. **Máximo 3 detalles** por sprite (dentro del 10%).
4. **Los detalles viven en el 10% inferior o superior** del sprite — nunca en el centro (reservado para forma principal).
5. **Contraste de detalle:** usar color de acento (máx. 2 por asset — ART_STYLE_GUIDE §5.6).

---

## 6. Legibilidad

### 6.1 Test de silueta

Todo asset debe pasar el **Silhouette Test**:

1. Rellenar el sprite de negro sobre blanco.
2. Reducir al **50%** del tamaño final en pantalla.
3. Si no se identifica la categoría en **0.5 segundos** → rediseñar.

### 6.2 Test de thumbnail

1. Reducir al **25%** (tamaño de icono en UI).
2. Debe distinguirse: niño vs vehículo vs casa vs árbol vs prop.
3. Los **3 colores dominantes** deben ser legibles.

### 6.3 Test de zoom out (mapa completo)

1. Colocar el asset en un tile de 256×128.
2. Con 10+ assets visibles simultáneamente, el objeto no debe **desaparecer** ni **dominar** la escena.
3. Props ≤ 1 tile; edificios ≥ 2 tiles; vehículos ≈ 1 tile de ancho.

### 6.4 Contraste y separación

| Regla | Especificación |
|---|---|
| **Contraste mínimo** entre forma principal y fondo | ΔL ≥ 30% (luminosidad) |
| **Separación de objetos adyacentes** | Outline 1.5–2 px o gap de 2 px mínimo |
| **Colores dominantes por sprite** | Máximo 3 (+ 2 acentos) |
| **Lectura isométrica** | Cara SE siempre la más clara; silueta no se confunde con sombra |

### 6.5 Jerarquía visual en pantalla

```
Prioridad de lectura (de mayor a menor):
1. Jugador / vehículo del jugador  →  forma principal grande + outline 2px + colores vivos
2. Otros corredores                →  outline 2px + colores distintivos
3. Obstáculos / colisionables      →  contraste alto con calzada
4. Edificios / fondo               →  outline 1.5px + colores más apagados
5. Decoración menor                →  sin outline o 1px; colores desaturados
```

---

## 7. Personalidad de los objetos

### 7.1 Principio rector

> Cada objeto tiene **dueño invisible**. Alguien del barrio lo hizo, lo usa o lo cuida.

### 7.2 Personalidad por categoría

| Categoría | Personalidad | Cómo se transmite (capa 10%) |
|---|---|---|
| **Niño protagonista** | Curioso, determinado, creativo | Gorra torcida, rodilla raspada, herramienta en mano |
| **Niño rival amistoso** | Competitivo, orgulloso de su obra | Gafas, bufanda, pegatina en casco |
| **Vehículo del protagonista** | Primera construcción, imperfecto pero querido | Cinta de colores, nombre pintado (borroso, ilegible), rueda desparejada |
| **Vehículo rival** | Más pulido pero igual de casero | Más cinta plateada, motor más grande, calcomanía |
| **Casa** | Familia, historia | Ropa tendida, maceta, mural, ventana con cortina |
| **Garaje** | Taller del barrio | Herramientas en la puerta, mancha de aceite limpia, cartel |
| **Prop reciclado** | Reutilizado con orgullo | Limpio, sin óxido excesivo, cinta o tornillo visible |

### 7.3 Vehículo ↔ Niño: conexión obligatoria

Cuando un niño tiene vehículo asignado, deben compartir **al menos 1 rasgo visual**:

| Rasgo compartido | Ejemplo |
|---|---|
| **Color de acento** | Niño con remera roja → asiento rojo en el auto |
| **Material dominante** | Niño con gorra de cartón → carrocería de cartón |
| **Detalle de cinta** | Niño con cinta en muñeca → cinta en chasis |
| **Expresión / actitud** | Niño audaz → motor expuesto grande |

**Objetivo:** que el jugador piense *"ese niño construyó ese auto"* sin leer texto.

### 7.4 Personalidad SIN basura

| Permitido (ingenio) | Prohibido (basura) |
|---|---|
| Caja de fruta limpia reutilizada | Caja rota con restos de comida |
| Bidón lavado de color vivo | Bidón sucio con manchas marrones |
| Neumático con surcos visibles | Neumático desgarrado o podrido |
| Madera con vetas y un clavo | Madera podrida con moho |
| Cinta adhesiva en unión funcional | Cinta amarillenta despegándose |
| Motor expuesto con brillo | Motor oxidado goteando aceite negro |
| Cartón doblado con intención | Cartón aplastado al azar |

---

## 8. Filosofía del reciclado creativo

### 8.1 Definición

**Reciclado creativo** = tomar un material del barrio y transformarlo en algo **limpio, funcional e ingenioso** que parece hecho con cuidado por un niño inteligente.

### 8.2 Los tres pilares

```
         ┌──────────────┐
         │   INGENIOSO   │  Se ve la idea del niño: "usé un bidón como asiento"
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───┴───┐  ┌───┴───┐  ┌───┴───┐
│ LIMPIO │  │FUNCIONAL│ │ CONECTADO │
└────────┘  └────────┘  └───────────┘
Sin suciedad  Parece que   El jugador ve
ni abandono   funciona     la relación
              de verdad    niño ↔ auto
```

| Pilar | Regla visual | Test |
|---|---|---|
| **Limpio** | Colores vivos del material; sin manchas marrones, moho, óxido dominante | ¿Lo tocarías con las manos? |
| **Funcional** | Piezas conectadas con cinta/tornillo; ruedas alineadas al suelo; asiento donde va un asiento | ¿Parece que se movería si le empujaras? |
| **Ingenioso** | Al menos 1 decisión creativa visible (bidón = tanque, cuchara = palanca) | ¿Te hace sonreír por la idea? |

### 8.3 Escala de "estado del material"

Usar esta escala al diseñar; **nunca bajar de "Usado limpio"**:

```
Nuevo ──── Usado limpio ──── Desgastado ──── ❌ Sucio / roto
  │              │               │                │
  ✓              ✓               ✓                ✗ PROHIBIDO
poco usado   reciclado del    textura visible   basura, abandono,
             barrio, lavado   pero funcional    peligro visual
```

### 8.4 Narrativa visual de construcción

Cada vehículo casero debe sugerir **cómo fue construido**:

1. **Base** (70%): un objeto grande reciclado (caja, tabla, chapa) = "empecé con esto"
2. **Conexión** (20%): cinta, clavo, soga = "lo uní así"
3. **Toque personal** (10%): calcomanía, color, accesorio = "le puse mi estilo"

---

## 9. Reglas de modularidad visual

> **Crítico:** El juego tendrá **cientos de piezas** combinables. Toda pieza modular debe encajar visual y técnicamente con cualquier otra de su categoría.

### 9.1 Categorías modulares de vehículo

| Categoría | Prefijo de asset | Cantidad estimada |
|---|---|---|
| Chassis (carrocería base) | `vehicle_chassis_` | 6–12 variantes |
| Ruedas | `wheel_` | 8–16 variantes |
| Motores | `engine_` | 6–10 variantes |
| Parachoques | `bumper_` | 6–10 variantes |
| Asientos | `seat_` | 6–10 variantes |
| Volantes | `steering_` | 4–8 variantes |
| Escapes | `exhaust_` | 4–8 variantes |
| Accesorios | `vehicle_accessory_` | 10–20 variantes |

### 9.2 Contrato visual de compatibilidad

Toda pieza modular **debe compartir**:

| Propiedad | Valor estándar | Tolerancia |
|---|---|---|
| **Escala** | Relativa al niño = 1.0 u | ±5% entre piezas de la misma categoría |
| **Perspectiva** | Isométrica 2:1, dirección SE default | 0% — exactamente igual |
| **Altura de encaje** | Ver tabla §9.3 | ±2 px |
| **Estilo de outline** | 2 px `#2A2030` | Exacto |
| **Estilo de sombreado** | Cel-shading 2–3 tonos | Exacto |
| **Fondo de generación** | `#FF00FF` | Exacto |

### 9.3 Puntos de encaje (snap points)

Cada pieza define puntos donde otras se conectan:

```
CHASSIS SMALL (vista SE, isométrico)
─────────────────────────────────────
                    [seat_snap]        ← centro superior del chasis
                         │
    [wheel_fl]───────────┼───────────[wheel_fr]
                         │
              [engine_snap]            ← frente del chasis (SE)
                         │
              [bumper_snap]            ← extremo frontal
                         │
              [exhaust_snap]           ← lateral trasero (SW)
                         │
    [wheel_rl]───────────┼───────────[wheel_rr]

    [steering_snap]                    ← interior, visible desde SE
```

| Snap point | Posición en chassis | Piezas que encajan |
|---|---|---|
| `wheel_fl` / `wheel_fr` / `wheel_rl` / `wheel_rr` | 4 esquinas inferiores | `wheel_*` |
| `engine_snap` | Frente SE, centro | `engine_*` |
| `seat_snap` | Centro superior | `seat_*` |
| `steering_snap` | Interior, offset SE | `steering_*` |
| `bumper_snap` | Extremo frontal SE | `bumper_*` |
| `exhaust_snap` | Lateral trasero SW | `exhaust_*` |

### 9.4 Tamaños de pieza

| Pieza | Tamaño (small chassis) | Tamaño (medium) | Tamaño (large) |
|---|---|---|---|
| **Chassis** | 0.90 × 0.55 × 0.70 u | 1.20 × 0.70 × 0.85 u | 1.50 × 0.85 × 1.00 u |
| **Rueda small** | Ø 0.25 u | Ø 0.25 u | — |
| **Rueda large** | — | Ø 0.30 u | Ø 0.35 u |
| **Motor small** | 0.20 × 0.15 × 0.15 u | — | — |
| **Motor medium** | — | 0.25 × 0.20 × 0.20 u | — |
| **Motor large** | — | — | 0.30 × 0.25 × 0.25 u |
| **Asiento** | 0.20 × 0.15 × 0.15 u | 0.25 × 0.18 × 0.18 u | 0.30 × 0.20 × 0.20 u |
| **Parachoques** | 0.40 × 0.10 × 0.10 u | 0.50 × 0.12 × 0.12 u | 0.60 × 0.15 × 0.15 u |
| **Volante** | Ø 0.12 u | Ø 0.14 u | Ø 0.16 u |
| **Escape** | 0.15 × 0.08 × 0.08 u | 0.20 × 0.10 × 0.10 u | 0.25 × 0.12 × 0.12 u |

### 9.5 Reglas de combinación visual

1. **Cualquier rueda encaja en cualquier snap de rueda** del mismo tamaño (small/large).
2. **Cualquier motor encaja en cualquier chassis** de su tier (small/medium/large).
3. **Las piezas no se salen del bounding box del chassis** al combinarse (salvo escape y motor "oversized" como variante especial documentada).
4. **Máximo 1 pieza por snap point.**
5. **Colores de piezas:** cada pieza usa la paleta de materiales (ART_STYLE_GUIDE §5–6); el jugador puede mezclar colores libremente.
6. **Asimetría intencional:** ruedas desparejadas (small + large) permitidas; deben verse **deliberadas**, no rotas.

### 9.6 Test de combinación

Antes de aprobar un lote de piezas modulares:

1. Combinar **chassis + 4 ruedas + motor + asiento + volante + paragolpe + escape**.
2. Verificar que no hay solapamiento visual incoherente.
3. Verificar que la silueta combinada sigue siendo > 60% rectángulos/cuadrados.
4. Verificar regla 70/20/10 en la **silueta combinada** (no solo en piezas sueltas).
5. Reducir al 50%: ¿sigue pareciendo un vehículo casero?

---

## 10. GLOBAL VISUAL RULES

> Reglas obligatorias de diseño visual. Complementan las GLOBAL ART RULES de `ART_STYLE_GUIDE.md`.

### 10.1 Shape Language

| ID | Regla |
|---|---|
| **V-001** | Formas dominantes = **cuadrados, rectángulos, trapecios**. Mínimo 60% de la silueta. |
| **V-002** | Círculos permitidos para: cabezas, ruedas, copas, faros. Máximo 25% de la silueta. |
| **V-003** | **Prohibidos triángulos puntiagudos** como forma principal. |
| **V-004** | **Prohibidas siluetas agresivas** (picos, astillas, garras, spires). |
| **V-005** | Curvas libres solo en **vegetación** y detalles menores (≤ 5%). |
| **V-006** | Esquinas redondeadas: radio 2–4 px en props; esquinas isométricas exactas en edificios. |

### 10.2 Silueta por categoría

| ID | Regla |
|---|---|
| **V-007** | Niños: **cabeza grande (○ 45–50%) + torso pequeño (□ 20–25%) + piernas cortas (▭▭ 25–30%)**. |
| **V-008** | Autos: **formas cuadradas/rectangulares + mínimo 4 piezas modulares visibles**. |
| **V-009** | Casas: **formas simples + techo bajo (trapecio ≤ 25°) + pocas curvas**. |
| **V-010** | Vegetación: **formas redondas (○) + tronco recto (▭)**. Prohibido ciprés/pino puntiagudo. |

### 10.3 Composición

| ID | Regla |
|---|---|
| **V-011** | Regla **70 / 20 / 10** obligatoria en todo sprite. |
| **V-012** | Máximo **3 detalles** por sprite (capa 10%). |
| **V-013** | Detalles en bordes superior/inferior; **nunca en el centro**. |
| **V-014** | Forma principal toca **≥ 2 bordes** del bounding box. |

### 10.4 Reciclado creativo

| ID | Regla |
|---|---|
| **V-015** | Todo material reciclado = **limpio + funcional + ingenioso**. |
| **V-016** | **Prohibido** basura sucia, moho, óxido dominante, objetos rotos/abandonados. |
| **V-017** | Estado mínimo del material: **"usado limpio"**. |
| **V-018** | Cada vehículo sugiere **cómo fue construido** (base + conexión + toque personal). |
| **V-019** | El jugador debe pensar: **"ese niño construyó ese auto"**. |

### 10.5 Modularidad

| ID | Regla |
|---|---|
| **V-020** | Piezas modulares comparten: **escala, pivote, perspectiva, altura de encaje**. |
| **V-021** | Toda pieza nueva debe combinar con **al menos 2 chassis** y **2 piezas** de otra categoría sin artefactos visuales. |
| **V-022** | Máximo **1 pieza por snap point**. |
| **V-023** | Asimetría permitida; debe verse **intencional**, no rota. |

### 10.6 Legibilidad

| ID | Regla |
|---|---|
| **V-024** | Todo asset pasa **Silhouette Test** al 50% de tamaño. |
| **V-025** | Identificación de categoría en **< 0.5 segundos** a tamaño de juego. |
| **V-026** | Máximo **3 colores dominantes** + 2 acentos por sprite. |

### 10.7 Bloque de prompt obligatorio

Incluir al final de todo prompt de diseño/generación:

```
VISUAL LANGUAGE (Carreras de Barrio v1.0):
- Shape language: squares, rectangles, trapezoids dominant; round heads/wheels/trees
- Composition: 70% primary shape, 20% secondary, 10% personality details
- Recycled = clean, functional, ingenious — never dirty trash
- Kid silhouette: big head, small torso, short legs
- Vehicle: square improvised blocks, 4+ visible modular parts
- No pointy triangles, no aggressive shapes
- Per VISUAL_LANGUAGE.md
```

---

## Apéndice A — Checklist de aprobación visual

- [ ] Silhouette Test al 50% — categoría identificable
- [ ] Thumbnail Test al 25% — distinguible en grupo
- [ ] Regla 70/20/10 respetada
- [ ] Formas dominantes = □ ▭ ▱ (≥ 60%)
- [ ] Sin triángulos puntiagudos ni siluetas agresivas
- [ ] Material reciclado = limpio, funcional, ingenioso
- [ ] Personalidad en capa 10% (máx. 3 detalles)
- [ ] Escala coherente con ART_STYLE_GUIDE §4
- [ ] Si es pieza modular: encaja con snap points §9.3
- [ ] Si es vehículo de niño: rasgo compartido niño ↔ auto §7.3

## Apéndice B — Historial de versiones

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-07-05 | Documento inicial — shape language, siluetas, composición, reciclado creativo, modularidad |

---

*Fin de VISUAL_LANGUAGE.md*
