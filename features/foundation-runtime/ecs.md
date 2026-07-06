# Foundation Runtime — ECS

## GameState

```rust
#[derive(States, Clone, Eq, PartialEq, Debug, Hash, Default)]
pub enum GameState {
    #[default]
    Boot,
    Loading,
    MainMenu,
    Gameplay,
}
```

## Plugins (planned crates/modules)

| Plugin | Responsibility |
|---|---|
| `CorePlugin` | State machine, events, config |
| `AssetPlugin` | AssetManager, manifest verify, hot reload |
| `RenderPlugin` | Isometric camera, tilemap |
| `WorldPlugin` | layout.json, scene_hooks, collision load |

## Resources

```rust
#[derive(Resource)]
pub struct GameConfig { /* paths, dev flags */ }

#[derive(Resource)]
pub struct LoadedNeighborhood { /* layout + hooks */ }
```

## Events

```rust
pub struct AssetsReady;
pub struct NeighborhoodLoaded { pub map_id: String };
```

## Data paths

```
data/config/game.toml
data/maps/barrio_tutorial_01/layout.json
data/maps/barrio_tutorial_01/collision.json
data/maps/barrio_tutorial_01/scene_hooks.json
data/tilesets/environment_base_pack_01_manifest.json
assets/environment/
mods/   (empty, future)
```
