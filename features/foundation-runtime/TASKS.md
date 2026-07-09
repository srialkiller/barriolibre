# Foundation Runtime — Tasks

> Branch: `feature/bevy-foundation-runtime` — **complete**, merged to `develop`

## Build Engineer
- [x] **S1-BE-001** Cargo workspace + Bevy 0.15 pin + profiles
- [x] **S1-BE-002** `scripts/ci.ps1` — fmt, clippy -D warnings, test, map_validator
- [x] **S1-BE-003** `rust-toolchain.toml`

## Technical Director
- [x] **S1-TD-001** App + states: Boot, Loading, MainMenu, Gameplay
- [x] **S1-TD-002** Plugins: CorePlugin, AssetPlugin, RenderPlugin, WorldPlugin
- [x] **S1-TD-003** Global resources + event bus
- [x] **S1-TD-004** AssetManager + manifest verification
- [x] **S1-TD-005** Hot reload (dev feature via `cargo run-hot`)
- [x] **S1-TD-006** Isometric camera 2:1
- [x] **S1-TD-007** Tilemap renderer
- [x] **S1-TD-008** Load layout.json + scene_hooks.json + collision.json
- [x] **S1-TD-009** tracing logging + GameConfig
- [x] **S1-TD-010** mods/ directory scaffold

## Tools Engineer
- [x] **S1-TE-001** tools/map_validator stub
- [x] **S1-TE-002** F3 debug_overlay (FPS, state, asset count)

## World Designer
- [x] **S1-WD-001** data/maps/barrio_tutorial_01/layout.json

## QA
- [x] **S1-QA-001** Full DoD from Sprint_01.md
