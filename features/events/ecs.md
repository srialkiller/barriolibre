# Events — ECS

Orquestación sobre [RACE_DESIGN_GUIDE](../../docs/game/RACE_DESIGN_GUIDE.md) y [CLAN_SYSTEM_GUIDE §9](../../docs/game/CLAN_SYSTEM_GUIDE.md).

## Components

```rust
#[derive(Component)]
pub struct EventSlot {
    pub event_id: EventId,
    pub scheduled_day: u32,
    pub status: EventStatus,  // Locked | Open | Registered | Done
}

#[derive(Component)]
pub struct EventRegistration {
    pub event_id: EventId,
    pub participant: Entity,
    pub clan_id: Option<ClanId>,
}

#[derive(Component)]
pub struct CalendarBoard;  // marker on plaza POI
```

## Resources

```rust
#[derive(Resource)]
pub struct EventCalendar {
    pub current_day: u32,
    pub slots: Vec<EventSlotState>,
    pub active_event: Option<EventId>,
}

#[derive(Resource)]
pub struct EventCatalog;  // from data/events/event_calendar.json
```

## Events

```rust
#[derive(Event)]
pub struct EventUnlocked { pub event_id: EventId }

#[derive(Event)]
pub struct EventRegisterRequest { pub event_id: EventId, pub player: Entity }

#[derive(Event)]
pub struct EventStarted { pub event_id: EventId, pub kind: EventKind }

#[derive(Event)]
pub struct EventCompleted { pub event_id: EventId, pub rewards: EventRewards }
```

## Systems

| System | Trigger | Responsibility |
|---|---|---|
| `event_calendar_tick_system` | In-game day advance | Open/close slots |
| `event_unlock_system` | Rep/race milestones | Set slot Locked→Open |
| `event_register_system` | `EventRegisterRequest` | Fee, tag clan |
| `event_launch_system` | Scheduled time | Delegate to race/clan |
| `event_complete_system` | Race/clan done | Rewards + mark Done |

## Game state

Transición `Exploring → Racing` o `ClanHub` según `EventKind` — ver [GAMEPLAY_GUIDE §7](../../docs/game/GAMEPLAY_GUIDE.md)

## Data files

- `data/events/event_calendar.json`
- `data/events/event_rewards.json`
