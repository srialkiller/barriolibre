# Inventory — ECS

Ver [ECONOMY_GUIDE §11](../../docs/systems/ECONOMY_GUIDE.md).

## Components

```rust
#[derive(Component)]
pub struct Collectible {
    pub item_kind: ItemKind,
    pub quantity: u32,
}

#[derive(Component)]
pub struct InventoryOwner;  // marker on player entity

#[derive(Component)]
pub struct PickupPending;   // anti double-pickup frame
```

## Resources

```rust
#[derive(Resource)]
pub struct PlayerInventory {
    pub materials: HashMap<MaterialId, u32>,
    pub parts: Vec<PartInstance>,
    pub blueprints: HashSet<BlueprintId>,
}

#[derive(Resource)]
pub struct ItemDefs;  // from data/economy/material_defs.json
```

## Events

```rust
#[derive(Event)]
pub struct PickupItemRequest {
    pub collector: Entity,
    pub collectible: Entity,
}

#[derive(Event)]
pub struct InventoryChanged {
    pub owner: Entity,
}
```

## Systems

| System | Trigger | Responsibility |
|---|---|---|
| `pickup_system` | `PickupItemRequest` | Transfer to PlayerInventory |
| `collectible_highlight_system` | Proximity to player | Visual feedback |
| `inventory_ui_system` | UI open | Render stacks |
| `inventory_persist_system` | Save event | Serialize state |

## Game state

Pickup activo en `GameState::Exploring` — ver [GAMEPLAY_GUIDE §7](../../docs/game/GAMEPLAY_GUIDE.md)

## Data files

- `data/economy/material_defs.json`
- `data/world/collectible_spawns_tutorial.json`
