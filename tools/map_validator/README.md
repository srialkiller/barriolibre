# map_validator

Valida `data/maps/*/layout.json` contra tile manifest y scene_hooks.

**Status:** stub — Sprint 01  
**Owner:** tools_engineer

## Checks (planned)

- Tile IDs exist in manifest
- Dimensions consistent
- scene_hooks reference valid POI ids
- collision.json schema valid (optional use)

## Usage (planned)

```bash
cargo run -p map_validator -- data/maps/barrio_tutorial_01/
```
