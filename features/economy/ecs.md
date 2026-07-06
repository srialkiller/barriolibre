# Economy — ECS

Ver [ECONOMY_GUIDE §11](../../docs/systems/ECONOMY_GUIDE.md).

## Components

```rust
#[derive(Component)]
pub struct EconomyOwner;  // marker on player

#[derive(Component)]
pub struct RepThreshold {
    pub track: RepTrack,
    pub required: u32,
    pub unlock_id: UnlockId,
}
```

## Resources

```rust
#[derive(Resource)]
pub struct PlayerEconomy {
    pub chapitas: u32,
    pub materials: HashMap<MaterialId, u32>,
    pub reputation: HashMap<RepTrack, u32>,
    pub unlocked_recipes: HashSet<RecipeId>,
}

#[derive(Resource)]
pub struct PriceTable;  // from data/economy/price_table.json
```

## Events

```rust
#[derive(Event)]
pub struct EconomyTransaction {
    pub kind: TransactionKind,  // Credit | Debit
    pub chapitas: i32,
    pub materials: HashMap<MaterialId, i32>,
    pub reason: TransactionReason,
}

#[derive(Event)]
pub struct ReputationChanged {
    pub track: RepTrack,
    pub new_value: u32,
    pub delta: i32,
}
```

## Systems

| System | Trigger | Responsibility |
|---|---|---|
| `economy_apply_system` | `EconomyTransaction` | Validate + apply balances |
| `rep_unlock_system` | `ReputationChanged` | Unlock recipes, circuits |
| `economy_hud_system` | Changed balances | Update HUD |
| `economy_persist_system` | Save | Serialize PlayerEconomy |

## Game state

Economy activa en todos los estados excepto menú — ver [GAMEPLAY_GUIDE §7](../../docs/game/GAMEPLAY_GUIDE.md)

## Data files

- `data/economy/price_table.json`
- `data/economy/material_defs.json`
- `data/economy/rep_thresholds.json`
