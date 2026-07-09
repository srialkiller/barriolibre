# Quest — ECS

## Plugin

`QuestPlugin` (`src/game/quest/`)

## Resources

| Resource | Owner | Descripción |
|---|---|---|
| `TutorialQuestState` | QuestPlugin | Definición JSON + `QuestStage` |
| `NpcDialogueOverrides` | QuestPlugin | Líneas de diálogo por `npc_id` |
| `ActiveQuestHud` | QuestPlugin | Título y objetivo para UI |

## Events (consumidos)

| Event | Productor | Uso |
|---|---|---|
| `NpcInteracted` | PlayerPlugin | Aceptar / completar misión |
| `ItemCollected` | InventoryPlugin | Avanzar recolección |

## Events (emitidos)

| Event | Consumidor | Uso |
|---|---|---|
| `QuestCompleted` | (futuro save/UI) | Misión tutorial terminada |
| `GarageUnlocked` | GaragePlugin | Desbloquear garaje |

## Stages

```
NotStarted → Accepted → ReadyToReturn → Completed
                ↑ ItemCollected (3/3 materiales)
NotStarted → Accepted  (NpcInteracted con Pedro)
ReadyToReturn → Completed (NpcInteracted con Pedro)
```

## UI components

- `QuestHudRoot` / `QuestHudText` — panel objetivo activo
