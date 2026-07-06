# GITFLOW_GUIDE.md
## Carreras de Barrio — Git como Pipeline del Estudio Virtual

**Versión:** 1.0  
**Owner:** `release_manager` + `studio_director`  
**Estado:** Norma oficial — **ninguna tarea comienza sin rama registrada**

---

> Este documento **no explica Git genérico**. Define **cómo trabaja el estudio virtual** con Git como parte del pipeline de producción.

---

## Tabla de contenidos

1. [Filosofía](#1-filosofía)
2. [Ramas permanentes](#2-ramas-permanentes)
3. [Ramas de trabajo](#3-ramas-de-trabajo)
4. [Naming conventions](#4-naming-conventions)
5. [Estados de rama/feature](#5-estados-de-ramafeature)
6. [Flujo del estudio](#6-flujo-del-estudio)
7. [Sprint = Release branch](#7-sprint--release-branch)
8. [Políticas del estudio](#8-políticas-del-estudio)
9. [Registro de ramas](#9-registro-de-ramas)
10. [Quién puede hacer qué con Git](#10-quién-puede-hacer-qué-con-git)
11. [Merge review](#11-merge-review)
12. [GLOBAL GIT RULES](#12-global-git-rules)

---

## 1. Filosofía

Git **no es una herramienta aparte** — es el sistema de tracking del estudio virtual.

| Principio | Regla |
|---|---|
| **Una feature = una rama** | Nunca trabajo genérico en `main` |
| **Release Manager único** | Solo él ejecuta comandos git |
| **Estado visible** | `features/<name>/STATUS.md` + `production/branches/registry.json` |
| **QA antes de merge** | POL-003 — sin excepciones |
| **Metrics gate** | POL-004 — blockers críticos bloquean merge |

---

## 2. Ramas permanentes

```
main          ← Producción estable (tags de release)
    ↑
release/*     ← Candidatos a ship (vertical-slice, mvp, alpha…)
    ↑
develop       ← Integración continua del estudio
    ↑
feature/*     ← Trabajo diario (una por feature/task)
```

| Rama | Propósito | Quién mergea |
|---|---|---|
| `main` | Builds estables, demos externas | Release Manager (post human approval) |
| `release/vertical-slice` | MVP loop jugable | Release Manager |
| `release/mvp` | Post playtest MVP | Release Manager |
| `develop` | Integración de features aprobadas | Release Manager |

**Estado inicial del repo:** solo `main`. Sprint 01 crea `develop` + `release/vertical-slice` + primera feature branch.

---

## 3. Ramas de trabajo

### Prefijos obligatorios

| Prefijo | Uso | Ejemplo |
|---|---|---|
| `feature/` | Gameplay, sistemas, código | `feature/bevy-scaffold` |
| `bugfix/` | Corrección de bugs | `bugfix/inventory-null` |
| `art/` | Assets, packs visuales | `art/environment-pack-02` |
| `docs/` | Documentación | `docs/gitflow-guide` |
| `research/` | Spike, prototipo, evaluación | `research/bevy-networking` |
| `hotfix/` | Fix urgente en main | `hotfix/savegame-crash` |

### Reglas de naming

- **kebab-case** siempre
- **Específico**, nunca genérico: `feature/garage-ui` ✅ · `feature/work` ❌
- Mapear 1:1 a carpeta `features/<name>/` cuando aplique
- Registrar en `production/branches/registry.json` antes de checkout

---

## 4. Naming conventions — catálogo

### Features (gameplay)

```
feature/bevy-scaffold
feature/environment-loader
feature/player-controller
feature/inventory
feature/crafting-system
feature/garage
feature/garage-ui
feature/race-ai
feature/tutorial
feature/camera
feature/audio-system
```

### Bugfixes

```
bugfix/inventory-null
bugfix/race-checkpoints
bugfix/player-collision
bugfix/savegame
```

### Arte

```
art/environment-pack-02
art/player-pack-01
art/garage-pack
art/tree-pack
art/vfx-pack
```

### Documentación

```
docs/gameplay-guide
docs/economy
docs/lore-update
docs/neighborhood-v2
docs/gitflow-guide
```

### Research

```
research/bevy-networking
research/ecs-vehicles
research/steamdeck
research/ai-racers
```

---

## 5. Estados de rama/feature

Cada feature/rama progresa por estos estados (documentados en `features/<name>/STATUS.md`):

```
Draft
    ↓
In Design          ← Creative + especialistas definen
    ↓
Implementation     ← Technical Director (código) / Art (assets)
    ↓
QA                 ← QA Director aprueba
    ↓
Ready to Merge     ← Release Manager valida políticas
    ↓
Merged             ← En develop o release/*
    ↓
Released           ← En main con tag
```

| Estado | Quién avanza | Criterio |
|---|---|---|
| Draft | Studio Director | Feature detectada, rama creada |
| In Design | Especialistas | design.md / spec completo |
| Implementation | Tech / Art | TASKS.md items done |
| QA | QA Director | QA.md criteria met |
| Ready to Merge | Release Manager | POL-001–007 ✅ |
| Merged | Release Manager | git merge ejecutado |
| Released | Release Manager | tag en main |

---

## 6. Flujo del estudio

```
Tú (prompt)
    ↓
Studio Director           ← Detecta tipo, asigna agentes
    ↓
Release Manager           ← Crea rama, registra, checkout
    ↓
Creative Director         ← Gate identidad (si feature nueva)
    ↓
Especialista(s)           ← Diseño / implementación / arte
    ↓
QA Director               ← Aprobación
    ↓
Release Manager           ← Merge review + merge
    ↓
Studio Director           ← Actualiza roadmap + metrics
    ↓
develop / release/*
```

### Ejemplo: "Agregar garage"

```
Studio Director:
  Feature detectada: garage
  Tipo: gameplay
  Rama: feature/garage
  Cadena: Creative → Vehicle → Game → Technical → QA

Release Manager:
  git switch -c feature/garage develop
  registry.json ← entry
  features/garage/STATUS.md ← Draft → In Design

[... trabajo especialistas ...]

Release Manager:
  STATUS → Ready to Merge
  POL check ✅
  git merge feature/garage → develop
  STATUS → Merged
  studio_scan.py
```

---

## 7. Sprint = Release branch

Los sprints del roadmap **viven dentro de una release branch**, no en ramas genéricas.

### Vertical Slice (actual)

**Release branch:** `release/vertical-slice`

| Feature branch | Sprint | Status |
|---|---|---|
| `feature/bevy-scaffold` | Sprint 01 | ⬜ |
| `feature/environment-loader` | Sprint 01 | ⬜ |
| `feature/player-controller` | Sprint 02 | ⬜ |
| `feature/inventory` | Sprint 02 | ⬜ |
| `feature/crafting-system` | Sprint 03 | ⬜ |
| `feature/garage` | Sprint 03 | ⬜ |
| `feature/race-ai` | Sprint 03 | ⬜ |
| `feature/tutorial` | Sprint 03 | ⬜ |

### Flujo de cierre

```
Todas las feature branches → QA ✅
    ↓
Merge a develop
    ↓
release/vertical-slice integrada
    ↓
Playtest MVP
    ↓
release/mvp → main (tag v0.1.0-mvp)
```

Ver [production/branches/README.md](../../production/branches/README.md).

---

## 8. Políticas del estudio

| ID | Política |
|---|---|
| **POL-001** | **Nunca trabajar sobre `main`** directamente. |
| **POL-002** | **Toda feature requiere rama propia** registrada en registry. |
| **POL-003** | **Toda rama requiere QA aprobado** antes de merge. |
| **POL-004** | **No merge si `metrics/project_state.json` tiene blockers `critical`**. |
| **POL-005** | **Technical Director aprueba compilación** (`cargo check` / `cargo test`). |
| **POL-006** | **QA Director aprueba arte** (score A/B) y funcionalidad. |
| **POL-007** | **Studio Director aprueba integración** (roadmap + features sync). |

Excepciones → ADR nuevo + aprobación humana.

---

## 9. Registro de ramas

**Fuente de verdad:** `production/branches/registry.json`

```json
{
  "branch": "feature/garage",
  "type": "feature",
  "feature": "garage",
  "release": "release/vertical-slice",
  "status": "In Design",
  "created": "2026-07-06",
  "agents": ["vehicle_designer", "game_designer", "technical_director"],
  "merged_to": null
}
```

Release Manager **crea y actualiza** entradas. Studio Director **lee** para orquestar.

---

## 10. Quién puede hacer qué con Git

| Comando | Release Manager | Otros agentes | Humano |
|---|---|---|---|
| `git switch -c` | ✅ | ❌ | ✅ (con registro) |
| `git checkout` | ✅ | ❌ | ✅ |
| `git merge` | ✅ | ❌ | ⚠️ emergencia |
| `git tag` | ✅ | ❌ | ✅ |
| `git commit` | ✅ | ❌* | ✅ |
| `git push` | ✅ | ❌ | ✅ |

\*Especialistas **proponen** cambios; Release Manager o humano commitea en la rama correcta. En práctica con Cursor, el humano commitea — Release Manager valida rama y mensaje.

---

## 11. Merge review

Checklist obligatorio antes de merge (Release Manager):

- [ ] `features/<name>/STATUS.md` = `Ready to Merge`
- [ ] `features/<name>/QA.md` criteria ✅
- [ ] POL-001–007 satisfied
- [ ] `cargo check` pass (si hay Rust) — POL-005
- [ ] No conflictos con `develop`
- [ ] CHANGELOG.md updated
- [ ] Studio Director sign-off — POL-007
- [ ] `python scripts/studio_scan.py` post-merge

---

## 12. GLOBAL GIT RULES

| ID | Regla |
|---|---|
| **GIT-001** | Ninguna tarea inicia sin Release Manager + rama registrada. |
| **GIT-002** | Studio Director siempre precede a Release Manager en el pipeline. |
| **GIT-003** | Una rama = un propósito. No mezclar garage + inventory en misma rama. |
| **GIT-004** | Merge solo a `develop` o `release/*` — nunca directo a `main` (except hotfix). |
| **GIT-005** | Hotfix: `hotfix/*` desde `main` → merge main + develop. |
| **GIT-006** | Tags semver en main: `v0.1.0-mvp`, `v0.2.0-alpha`. |
| **GIT-007** | IA nunca improvisa nombre de rama — usar convención §4. |

---

## Referencias

- [agents/release_manager.md](../../agents/release_manager.md)
- [agents/studio_director.md](../../agents/studio_director.md)
- [production/branches/README.md](../../production/branches/README.md)
- [features/README.md](../../features/README.md)

---

*Fin de GITFLOW_GUIDE.md*
