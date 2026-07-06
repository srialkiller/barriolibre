# Foundation Runtime — Design

## Architecture

```
cargo run
    ↓
Boot → Loading (assets + map) → MainMenu → Gameplay
    ↓
Render isometric tilemap from layout.json
```

## Asset pipeline runtime

1. Load manifest JSON
2. Verify PNGs exist for referenced tiles
3. Register in AssetManager
4. Hot reload watches `assets/` in dev

## Render

- ADR-002: 2:1 isometric, NE light reference
- Sorting by Y for pseudo-depth
- Style anchor tile: `road_straight_h_01`

## Out of scope Sprint 01

- Player movement
- Pickups, garage, race
- Audio

## Vertical Slice alignment

This runtime is **step 1** toward 15 min playable loop (see MVP.md).
