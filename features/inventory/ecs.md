# Inventory — ECS

Ver [ECONOMY_GUIDE §11](../../docs/systems/ECONOMY_GUIDE.md).

## Components

```rust
#[derive(Component)]
pub struct Collectible {
    pub spawn_id: String,
    pub material_id: MaterialId,
    pub display_name: String,
    pub quantity: u32,
}
```

## Resources

```rust
#[derive(Resource)]
pub struct PlayerInventory {
    pub materials: HashMap<MaterialId, u32>,
}
```

## Events

```rust
#[derive(Event)]
pub struct PickupCollected {
    pub material_id: MaterialId,
    pub display_name: String,
    pub amount: u32,
    pub new_total: u32,
}
```

## Systems

| System | Trigger | Responsibility |
|---|---|---|
| `spawn_collectibles_system` | `OnEnter(Gameplay)` | Crear pickups desde scene hooks |
| `collect_nearby_pickup_system` | Tecla `E` | Transferir a PlayerInventory y despawn |
| `update_pickup_prompt_system` | Proximidad | Mostrar prompt de recolección |
| `toggle_inventory_ui_system` | Tecla `I` | Abrir/cerrar panel |
| `sync_inventory_ui_system` | Resource changed | Renderizar stacks |

## Game state

Pickup activo en `GameState::Gameplay`.

## Data files

- `data/maps/barrio_tutorial_01/scene_hooks.json`
- Fuente editable: Object Layer `pickups` en `barrio_tutorial_01.tmx`
