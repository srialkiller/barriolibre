# ADR-005: Nombre Comercial del Juego

**Status:** Proposed — **pendiente decisión humana post-prototipo**

> **Gate intencional:** No cerrar hasta tener (1) prototipo jugable, (2) dirección artística consolidada en vertical slice, (3) primer circuito funcionando. Ahí el nombre será evidente.  
**Date:** 2026-07-06  
**Deciders:** Creative Director (+ stakeholder humano)

---

## Context

Existen dos nombres en circulación:

| Nombre | Dónde aparece |
|---|---|
| **barriolibre** | Repositorio GitHub, carpeta del proyecto |
| **Carreras de Barrio** | Documentación, GAME_IDENTITY, concepto del juego |

Antes de UI, logotipo, Steam, itch.io y redes sociales, debemos **unificar la marca**.

## Opciones evaluadas

| Nombre | Pros | Contras |
|---|---|---|
| **Carreras de Barrio** | Claro, descriptivo, español nativo, ya en docs | Largo; dominio .com probablemente tomado |
| **Garage de Barrio** | Enfatiza craft/taller | Suena más estático, menos carrera |
| **Barrio Libre Racing** | Bilingüe, energía | "Racing" aleja del público LATAM infantil |
| **Barrio GP** | Corto, memorable | Pierde identidad craft/reciclaje |
| **Patio Racers** | Tierno, único | "Patio" limita escala del mundo |
| **Racers del Barrio** | Social, claro | Genérico |
| **Chatarra GP** | Muy identidad reciclaje | Puede sonar negativo para padres |
| **Garage Kids** | Inglés, marketable | Pierde barrio latinoamericano |
| **Barrio Torque** | Moderno | "Torque" suena adulto/mecánico |
| **barriolibre** | Repo ya existe; evoca libertad del barrio | No comunica carreras ni craft |

## Recomendación del Creative Director (no final)

**Nombre comercial:** `Carreras de Barrio`  
**Slug / repo / handles:** `barriolibre` o `carrerasdebarrio` (verificar disponibilidad)

**Rationale:** El ADN dice que no trata sobre autos sino creatividad — pero "Carreras" comunica el gancho jugable mientras "de Barrio" ancla identidad cultural. `barriolibre` funciona como **marca paraguas** del estudio/proyecto.

```
Marca paraguas:  Barrio Libre (estudio)
Juego:           Carreras de Barrio
Repo:            barriolibre (puede mantenerse)
```

## Decision

**PENDIENTE** — requiere confirmación humana antes de:

- [ ] Logo y UI
- [ ] Página Steam / itch.io
- [ ] Handles redes sociales
- [ ] Renombrar repo (opcional)

## Consequences (cuando se cierre)

Documentar decisión final aquí y actualizar:

- `README.md`
- `docs/game/GAME_IDENTITY.md` (si cambia nombre)
- Splash screen, metadata Bevy

## Referencias

- `docs/game/GAME_IDENTITY.md`
- `agents/creative_director.md`
