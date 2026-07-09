# Quest — Status

| Field | Value |
|---|---|
| **Branch** | `feature/quest` |
| **Release** | `release/vertical-slice` |
| **Lifecycle** | `qa` |
| **Sprint** | Sprint_03 |
| **Started** | 2026-07-09 |

**Current:** `qa` — primer flujo jugable del tutorial implementado; pendiente playtest manual.

## Implementado

- [x] `QuestPlugin` con `TutorialQuestState` y manifest JSON
- [x] Objetivos reactivos a `NpcInteracted` e `ItemCollected`
- [x] Diálogos de Pedro por fase (intro, aceptada, en progreso, entrega, completada)
- [x] HUD de misión activa con progreso de materiales
- [x] Completar misión emite `QuestCompleted` y `GarageUnlocked`
- [x] NPC renombrado a Pedro; pickups fuera del spawn
- [x] `cargo clippy`, `cargo test` verificados

## Pendiente de QA manual

- [ ] Completar flujo sin reiniciar: Pedro → 3 materiales → Pedro → banner garaje
- [ ] Verificar que el HUD desaparece al completar
- [ ] Confirmar que el garaje queda desbloqueado (`GarageAccess.unlocked`)
