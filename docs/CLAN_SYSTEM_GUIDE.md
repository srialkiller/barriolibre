# CLAN_SYSTEM_GUIDE.md
## Carreras de Barrio — Guía de Clanes del Barrio

**Equipo:** GAMEPLAY (Equipo 3)  
**ADN:** [GAME_IDENTITY.md](./GAME_IDENTITY.md) — pilar "Pertenencia"  
**Relacionado:** [ECONOMY_GUIDE.md](./ECONOMY_GUIDE.md), [PROGRESSION_GUIDE.md](./PROGRESSION_GUIDE.md), [RACE_DESIGN_GUIDE.md](./RACE_DESIGN_GUIDE.md)  
**Versión:** 1.0

---

> Los clanes no son guilds de MMO. Son **grupos de chicos del barrio** que compiten juntos, comparten materiales y se reconocen por banderas y eventos. Cooperación sana, infantil, sin toxicidad.

---

## Tabla de contenidos

1. [Filosofía del clan](#1-filosofía-del-clan)
2. [Estructura y roles](#2-estructura-y-roles)
3. [Creación y membresía](#3-creación-y-membresía)
4. [Identidad visual](#4-identidad-visual)
5. [Economía del clan](#5-economía-del-clan)
6. [Eventos de clan](#6-eventos-de-clan)
7. [Ranking y reputación](#7-ranking-y-reputación)
8. [Integración con carreras](#8-integración-con-carreras)
9. [Bevy ECS](#9-bevy-ecs)
10. [GLOBAL CLAN RULES](#10-global-clan-rules)

---

## 1. Filosofía del clan

| Principio | Regla |
|---|---|
| **Amistad, no jerarquía tóxica** | Líder = organizador, no dictador |
| **Cooperación visible** | Proyectos colectivos con recompensa compartida |
| **Identidad del barrio** | Nombre, bandera y colores propios |
| **Competencia sana** | Torneos entre clanes, no PvP agresivo |
| **Opcional pero valioso** | Jugar solo es viable; clan acelera progresión social |

**Filtro GAME_IDENTITY:** Si una mecánica de clan fomenta exclusión, bullying o pay-to-win → no pertenece.

---

## 2. Estructura y roles

| Rol | Cantidad | Permisos |
|---|---|---|
| **Fundador** | 1 | Crear clan, disolver, transferir liderazgo |
| **Capitán** | 0–2 | Invitar, expulsar, iniciar eventos |
| **Miembro** | 3–12 | Donar, participar, intercambiar |
| **Invitado** | — | Solo en eventos abiertos del barrio |

**Tamaño máximo:** 12 miembros (barrio pequeño, íntimo).

---

## 3. Creación y membresía

### 3.1 Crear clan

| Requisito | Valor |
|---|---|
| Reputación barrio | ≥ Corredor (150 rep) |
| Chapitas | 100 (sumidero) |
| Ubicación | Plaza o cancha (POI social) |

### 3.2 Unirse

- Invitación directa de capitán/fundador
- Solicitud + aprobación
- Un jugador = **1 clan activo** a la vez
- Cooldown salida: 24 h antes de unirse a otro

### 3.3 Disolución

- Fundador puede disolver si ≤2 miembros
- Inactivo 30 días → clan archivado (datos conservados 7 días)

---

## 4. Identidad visual

| Elemento | Sistema | Arte |
|---|---|---|
| **Nombre** | 3–20 chars, filtro palabras | UI |
| **Bandera** | Slot `special: flag_clan` en vehículo | VISUAL_LANGUAGE § vehículos |
| **Colores** | 2 colores primarios (paleta restringida) | ART_STYLE paleta |
| **Emblema** | 1 de 12 iconos predefinidos v1 | Asset pack futuro |

La bandera del clan es visible en carreras y en el hub del clan — refuerza pertenencia sin paywall.

---

## 5. Economía del clan

Ver [ECONOMY_GUIDE.md §9](./ECONOMY_GUIDE.md#9-clanes-y-economía).

| Mecánica | Descripción |
|---|---|
| **Banco clan** | Chapitas + materiales donados por miembros |
| **Proyecto clan** | Meta colectiva (ej. 500 cartón) → desbloquea pieza especial |
| **Intercambio** | Miembros intercambian piezas/materiales sin coste |
| **Entry fee torneo** | 25 chapitas/miembro → premio pool distribuido |

**Regla:** donaciones son voluntarias; nunca obligatorias para progresar solo.

---

## 6. Eventos de clan

| Evento | Frecuencia | Descripción |
|---|---|---|
| **Carrera clan vs clan** | Semanal | 4v4 en circuito del barrio |
| **Proyecto colectivo** | Continuo | Donar materiales → pieza clan |
| **Exploración grupal** | Bajo demanda | Bonus rep si 3+ miembros en mismo POI |
| **Torneo del barrio** | Mensual | Clanes compiten; premio reputación + chapitas |
| **Fiesta post-torneo** | Tras torneo | Hub social, confetti, sin gameplay |

### 6.1 Carrera clan vs clan

```
Preparación (build + inscripción)
    ↓
Clasificación (tiempos individuales suman)
    ↓
Final (top 2 clanes)
    ↓
Premios (pool chapitas + rep_clan)
    ↓
Reputación clan actualizada
```

---

## 7. Ranking y reputación

| Métrica | ID | Uso |
|---|---|---|
| **Rep clan** | `rep_clan_*` | Desbloqueos, torneos |
| **Ranking barrio** | `rank_clan_barrio_*` | Tabla en plaza |
| **Victorias torneo** | `stat_clan_wins` | Logro, cosmético |

**Rep clan sube por:** eventos, donaciones, victorias, proyectos completados.  
**No baja** por derrotas — solo estagna (competencia sana).

---

## 8. Integración con carreras

| Modo | Clan |
|---|---|
| Carrera libre | Bandera visible; sin bonus |
| Carrera clan | +5% chapitas si 2+ miembros en misma carrera |
| Torneo | Obligatorio tag clan; ranking afecta seed |
| Rival NPC | Rivales pueden ser "clan vecino" narrativo |

Hooks: `scene_hook: clan_hub`, `scene_hook: clan_race_register`

---

## 9. Bevy ECS

```rust
#[derive(Resource)]
pub struct ClanRegistry {
    pub clans: HashMap<ClanId, ClanData>,
}

#[derive(Component)]
pub struct ClanMembership {
    pub clan_id: ClanId,
    pub role: ClanRole,
    pub joined_at: u64,
}

#[derive(Component)]
pub struct ClanBank {
    pub chapitas: u32,
    pub materials: HashMap<MaterialId, u32>,
    pub active_project: Option<ClanProjectId>,
}
```

Datos: `data/clans/clan_config.json`, `data/clans/clan_projects.json`

---

## 10. GLOBAL CLAN RULES

| ID | Regla |
|---|---|
| **CL-001** | Máximo 12 miembros — barrio íntimo, no MMO. |
| **CL-002** | Un jugador, un clan activo. |
| **CL-003** | Cooperación > competencia interna. |
| **CL-004** | Sin chat tóxico: filtros + report (futuro). |
| **CL-005** | Proyectos clan = contenido exclusivo cooperativo, no P2W. |
| **CL-006** | Bandera clan = identidad, no stat boost en PvE solo. |
| **CL-007** | Toda mecánica clan pasa filtro GAME_IDENTITY §7. |

---

*Fin de CLAN_SYSTEM_GUIDE.md*
