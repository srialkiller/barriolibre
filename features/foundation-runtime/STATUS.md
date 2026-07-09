# Foundation Runtime — Status

| Field | Value |
|---|---|
| **Branch** | `feature/bevy-foundation-runtime` |
| **Release** | `release/vertical-slice` |
| **Milestone** | M0 — Foundation Runtime |
| **Sprint** | Sprint_01 |
| **Lifecycle** | `complete` |
| **Started** | 2026-07-06 |
| **Completed** | 2026-07-09 |

**Current:** `complete` — M0 DoD met, merged to `develop`

## Completed

- [x] Cargo workspace + Bevy 0.15 pin
- [x] `rust-toolchain.toml`, `scripts/ci.ps1`, clippy/fmt config
- [x] `src/` structure per BEVY_ARCHITECTURE §2
- [x] Plugins: Core, Asset, Map, Camera, Sprite, Menu, Debug
- [x] GameState machine: Boot → Loading → MainMenu → Gameplay
- [x] AssetRegistry + manifest verification
- [x] `data/maps/barrio_tutorial_01/` JSON
- [x] Isometric tilemap renderer (2:1)
- [x] F3 debug overlay
- [x] `tools/map_validator` stub
- [x] `cargo build`, `cargo clippy -D warnings`, `cargo test` pass
- [x] QA DoD sign-off

## Demo criterion (M0 DoD) — verified

`cargo run` shows:
1. Isometric camera
2. Barrio from layout.json (Enter from main menu)
3. ENVIRONMENT_BASE_PACK_01 tiles
4. F3 debug overlay (FPS, state, assets)
5. Message: Foundation Runtime operativo

## Merge target

`develop` — merged 2026-07-09

## Note

Player movement, collision, and Tiled export pipeline were implemented ahead of Sprint 02 on this branch; tracked separately under M1.
