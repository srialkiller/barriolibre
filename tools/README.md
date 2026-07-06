# Tools — Herramientas Internas del Estudio

Crates y scripts de **productividad interna**. No son gameplay.

**Owner:** `tools_engineer` + `build_engineer` (workspace)

## Estructura

```
tools/
├── asset_importer/      ← Import assets → Bevy-ready
├── map_validator/       ← Valida layout.json, tiles, hooks
├── manifest_builder/    ← Genera/valida manifest JSON
├── atlas_generator/     ← Texture atlases (futuro)
├── save_editor/         ← Editar saves dev (futuro)
└── debug_overlay/       ← FPS, ECS stats, asset debug
```

## Workspace

Cuando exista `Cargo.toml`, tools son **workspace members**:

```toml
[workspace]
members = [".", "tools/map_validator", "tools/debug_overlay"]
```

## Prioridad Sprint 01

1. `map_validator` — validar primer barrio JSON
2. `debug_overlay` — F3 overlay spec + crate stub
3. README stubs en el resto

## Invocación

```
@agents/tools_engineer.md Implementar map_validator
```
