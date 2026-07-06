# Foundation Runtime — ECS

Implementación detallada: [BEVY_ARCHITECTURE.md](../../docs/systems/BEVY_ARCHITECTURE.md).

## GameState

```rust
#[derive(States, Clone, Eq, PartialEq, Debug, Hash, Default)]
pub enum GameState {
    #[default]
    Boot,
    Loading,
    MainMenu,
    Gameplay,
    Paused,
    Debug,
}
```

## Plugins (Sprint 01 — ver BEVY_ARCHITECTURE §4)

| Plugin | Module |
|---|---|
| `CorePlugin` | `core/` |
| `AssetPlugin` | `assets/` |
| `MapPlugin` | `world/map/` |
| `CameraPlugin` | `render/camera/` |
| `SpritePlugin` | `render/sprites/` |
| `MenuPlugin` | `ui/menus/` (stub) |
| `DebugPlugin` | `debug/` |

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
