# Foundation Runtime — QA

Sprint 01 **no mergea** hasta DoD completo.

## Proyecto
- [ ] FR-QA-P01 `cargo build` OK
- [ ] FR-QA-P02 `cargo clippy -D warnings` OK
- [ ] FR-QA-P03 `cargo test` OK
- [ ] FR-QA-P04 `cargo fmt --check` OK

## Runtime visible
- [ ] FR-QA-V01 `cargo run` opens window
- [ ] FR-QA-V02 Neighborhood tiles visible (isometric)
- [ ] FR-QA-V03 No asset load errors in log
- [ ] FR-QA-V04 FPS ≥ 30 on target hardware

## ECS
- [ ] FR-QA-E01 State transitions Boot → Loading → Gameplay work
- [ ] FR-QA-E02 Plugins load without panic

## Assets
- [ ] FR-QA-A01 ENVIRONMENT_BASE_PACK_01 tiles load
- [ ] FR-QA-A02 Manifest validation passes

## Tools
- [ ] FR-QA-T01 F3 toggles debug overlay
- [ ] FR-QA-T02 map_validator runs on barrio_tutorial_01

## POL
- [ ] POL-005 Build Engineer CI green
- [ ] POL-006 QA sign-off
- [ ] POL-007 Studio Director — visible demo confirmed
