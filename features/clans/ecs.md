# Clans — ECS

Ver [CLAN_SYSTEM_GUIDE §9](../../docs/game/CLAN_SYSTEM_GUIDE.md).

## Components

```rust
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

#[derive(Component)]
pub struct ClanFlag {
    pub colors: [Color; 3],
    pub emblem_id: EmblemId,
}

#[derive(Component)]
pub struct ClanHub;  // marker on POI entity
```

## Resources

```rust
#[derive(Resource)]
pub struct ClanRegistry {
    pub clans: HashMap<ClanId, ClanData>,
}

#[derive(Resource)]
pub struct ClanProjectCatalog;  // from data/clans/clan_projects.json
```

## Events

```rust
#[derive(Event)]
pub struct ClanCreated { pub clan_id: ClanId, pub founder: Entity }

#[derive(Event)]
pub struct ClanDonation {
    pub donor: Entity,
    pub clan_id: ClanId,
    pub chapitas: u32,
    pub materials: HashMap<MaterialId, u32>,
}

#[derive(Event)]
pub struct ClanProjectCompleted { pub clan_id: ClanId, pub project_id: ClanProjectId }
```

## Systems

| System | Trigger | Responsibility |
|---|---|---|
| `clan_create_system` | UI request | Validate name, spawn clan |
| `clan_join_system` | Invite accept | Add membership |
| `clan_bank_system` | `ClanDonation` | Transfer player → bank |
| `clan_project_system` | Donation / threshold | Progress + complete |
| `clan_flag_render_system` | `InRace` + membership | Show flag on vehicle |

## Game state

`GameState::ClanHub` — ver [GAMEPLAY_GUIDE §7](../../docs/game/GAMEPLAY_GUIDE.md)

## Data files

- `data/clans/clan_config.json`
- `data/clans/clan_projects.json`
