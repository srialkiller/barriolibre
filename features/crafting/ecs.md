# Crafting — ECS

Ver [ECONOMY_GUIDE §11](../../docs/systems/ECONOMY_GUIDE.md).

## Components

```rust
#[derive(Component)]
pub struct CraftStation;  // marker on garage POI entity

#[derive(Component)]
pub struct UnlockedRecipes {
    pub recipe_ids: HashSet<RecipeId>,
}
```

## Resources

```rust
#[derive(Resource)]
pub struct RecipeCatalog;  // from data/economy/recipe_table.json

#[derive(Resource)]
pub struct CraftSession {
    pub selected_recipe: Option<RecipeId>,
}
```

## Events

```rust
#[derive(Event)]
pub struct CraftRequest {
    pub recipe_id: RecipeId,
    pub player: Entity,
}

#[derive(Event)]
pub struct CraftCompleted {
    pub recipe_id: RecipeId,
    pub output_part: PartId,
}
```

## Systems

| System | Trigger | Responsibility |
|---|---|---|
| `craft_validate_system` | `CraftRequest` | Check materials, chapitas, unlock |
| `craft_execute_system` | After validate OK | Consume resources, add part |
| `craft_ui_system` | `CraftStation` + UI | List recipes, fire request |

## Game state

Craft ocurre en `GameState::Garage` — ver [GAMEPLAY_GUIDE §7](../../docs/game/GAMEPLAY_GUIDE.md)

## Data files

- `data/economy/recipe_table.json`
- `data/economy/material_defs.json`
