# Inventory — Changelog

## [Unreleased] — feature/inventory

### Added
- PlayerInventory resource
- InventoryPlugin with pickup collection events
- Minimal inventory panel toggled with `I`
- Three tutorial pickups exported from Tiled
- Basic neighborhood NPC interaction
- Tiled `npcs` and `pickups` Object Layer export
- Reference-map generator preserves Sprint 02 object layers
- Map validation for NPC and pickup hooks

### Changed
- Camera zoom-in no longer uses `E`; `E` is reserved for world interaction
- NPC interaction takes priority when an NPC and pickup are both nearby
