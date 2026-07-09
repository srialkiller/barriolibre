# map_validator

Valida `data/maps/*/layout.json` contra tile manifest, scene_hooks, collision y props.

**Status:** ✅ Sprint 01 — operational  
**Owner:** tools_engineer

## Checks

- Tile IDs exist in generated manifest (or PNG on disk)
- Layout dimensions consistent with ground layer
- `scene_hooks.json`: barrio_id, spawn/NPC/pickup positions in bounds
- NPCs require name + dialogue; pickups require material ID, display name and quantity
- `collision.json`: barrio_id, cells in bounds (optional file)
- `props.json`: barrio_id, prop PNGs exist, positions in bounds

## Usage

```bash
cargo run -p map_validator -- data/maps/barrio_tutorial_01
```

Also runs as part of `scripts/ci.ps1`.

## Exit codes

- `0` — all checks passed
- `1` — validation errors (printed to stderr)
