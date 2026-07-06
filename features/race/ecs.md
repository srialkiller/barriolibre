# Race — ECS

Ver [RACE_DESIGN_GUIDE §8](../../docs/game/RACE_DESIGN_GUIDE.md) metadata.

## Components

```rust
#[derive(Component)]
pub struct RaceParticipant {
    pub race_id: RaceId,
    pub current_lap: u8,
    pub next_checkpoint: u8,
    pub finish_time: Option<f32>,
}

#[derive(Component)]
pub struct Checkpoint {
    pub index: u8,
    pub race_id: RaceId,
}

#[derive(Component)]
pub struct RivalDriver {
    pub profile_id: RivalId,
    pub behavior: RivalBehavior,
}

#[derive(Component)]
pub struct InRace;  // marker during active race
```

## Resources

```rust
#[derive(Resource)]
pub struct ActiveRace {
    pub race_id: RaceId,
    pub laps_total: u8,
    pub elapsed: f32,
    pub standings: Vec<Entity>,
}

#[derive(Resource)]
pub struct RaceCatalog;  // from data/races/*.json
```

## Events

```rust
#[derive(Event)]
pub struct RaceStarted { pub race_id: RaceId }

#[derive(Event)]
pub struct CheckpointCrossed { pub participant: Entity, pub index: u8 }

#[derive(Event)]
pub struct RaceFinished { pub participant: Entity, pub position: u8 }
```

## Systems

| System | Trigger | Responsibility |
|---|---|---|
| `race_start_system` | Register at POI | Spawn participants, countdown |
| `checkpoint_trigger_system` | Overlap | Validate order, advance lap |
| `rival_ai_system` | `InRace` | Path + atajo attempts |
| `race_reward_system` | `RaceFinished` | Drops, rep barrio |

## Game state

`GameState::Racing` — ver [GAMEPLAY_GUIDE §7](../../docs/game/GAMEPLAY_GUIDE.md)

## Data files

- `data/races/barrio_norte_circuito_01.json`
- `data/races/reward_table.json`
