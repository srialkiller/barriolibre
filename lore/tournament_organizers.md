# ¿Quién organiza los torneos?

## Respuesta corta

**Los mismos chicos, con bendición informal de un adulto referente** — el encargado de la cancha, el tío del taller, o el chico más grande que ya "se graduó" de correr y ahora arbitra.

## Verdad del mundo

Un torneo del barrio no tiene federación. Tiene:

1. **Organizador joven** (16–18 en lore, NPC en juego) que armó el bracket en un cuaderno.
2. **Adulto referente** que prestó el espacio y puso una mesa con limonada.
3. **Entry fee en chapitas** que van al premio — no a un promotor.

Es fiesta de barrio: banderitas de papel, cronómetro del celular del hermano mayor, meta hecha con cinta en dos postes.

## Roles en torneos

| Rol | Quién | Función |
|---|---|---|
| Organizador | NPC `organizador_cancha` | Inscripción, bracket, premios |
| Referente adulto | Flavor / cutscene | Abre cancha, cierra a las 6 |
| Clanes | Jugadores | Inscripción clan vs clan |
| Público | NPCs ambiente | Aplausos, confetti |

## Qué NO es

- Copa corporativa con sponsors.
- Apuestas ilegales.
- Eliminatoria violenta — "eliminación suave" es cartoon (último en checkpoint fuera).

## Implicaciones de diseño

- Torneos desbloqueados por rep Corredor+ (PROGRESSION).
- Entry fee 25 chapitas → pool premio (ECONOMY).
- Hub en plaza/cancha con `scene_hook: tournament_register`.
- Victoria = rep + chapitas + reconocimiento social, no contrato profesional.

## Coherencia

Refuerza **Comunidad** e **Ingenio**. Competencia organizada por el barrio, para el barrio.
