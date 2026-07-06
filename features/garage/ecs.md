# Garage — ECS

Ver [VEHICLE_DESIGN_GUIDE §9](../../docs/systems/VEHICLE_DESIGN_GUIDE.md).

## Components

```rust
#[derive(Component)]
pub struct VehicleAssembly {
    pub chassis_id: PartId,
    pub slots: HashMap<SlotId, PartId>,
}

#[derive(Component)]
pub struct VehicleStats {
    pub max_speed: f32,
    pub acceleration: f32,
    pub grip: f32,
    pub turn_rate: f32,
    pub mass: f32,
}

#[derive(Component)]
pub struct InGarage;  // marker while in garage state
```

## Resources

```rust
#[derive(Resource)]
pub struct PartsCatalog;  // from data/vehicles/parts_catalog.json
```

## Systems

| System | Trigger | Responsibility |
|---|---|---|
| `vehicle_stats_system` | `Changed<VehicleAssembly>` | Recalc stats from catalog |
| `garage_install_system` | Event `InstallPartRequest` | Validate + apply |
| `garage_ui_system` | `InGarage` + UI events | Presentation |

## Game state

`GameState::Garage` — ver [GAMEPLAY_GUIDE §7](../../docs/game/GAMEPLAY_GUIDE.md)

## Data files

- `data/vehicles/parts_catalog.json`
- `data/vehicles/default_builds.json`
