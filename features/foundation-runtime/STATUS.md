# Foundation Runtime — Status

| Field | Value |
|---|---|
| **Branch** | `feature/bevy-foundation-runtime` |
| **Release** | `release/vertical-slice` |
| **Milestone** | M0 — Foundation Runtime |
| **Sprint** | Sprint_01 |
| **Lifecycle** | `in_progress` |
| **Started** | 2026-07-06 |

**Current:** `in_progress` — Build Engineer + Technical Director step 1 complete

## Completed (step 1)

- [x] Cargo workspace + Bevy 0.15 pin
- [x] `rust-toolchain.toml`, `scripts/ci.ps1`, clippy/fmt config
- [x] `src/` structure per BEVY_ARCHITECTURE §2
- [x] Plugins: Core, Asset, Map, Camera, Sprite, Menu, Debug
- [x] GameState machine: Boot → Loading → MainMenu → Gameplay
- [x] AssetRegistry + manifest verification (187 tiles)
- [x] `data/maps/barrio_tutorial_01/` JSON
- [x] Isometric tilemap renderer (2:1)
- [x] F3 debug overlay
- [x] `cargo build`, `cargo clippy -D warnings`, `cargo test` pass

## Pending (next agents)

- [ ] Tools Engineer: map_validator stub
- [ ] QA Director: full DoD sign-off
- [ ] Release Manager: merge to develop

## Demo criterion (M0 DoD)

`cargo run` must show:
1. Isometric camera
2. Barrio from layout.json
3. ENVIRONMENT_BASE_PACK_01 tiles
4. F3 debug overlay (FPS, state, assets)
5. Message: Foundation Runtime operativo

## Merge target

`develop`
