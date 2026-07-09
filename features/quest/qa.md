# Quest — QA

## Pre-requisitos

- Rama `feature/quest`
- `cargo run --features dev_fast`

## Checklist — Flujo tutorial

- [ ] El jugador aparece en el barrio (spawn 13,13)
- [ ] HUD muestra misión **El primer carrito** y objetivo **Hablá con Pedro**
- [ ] `[E]` con Pedro abre diálogo de intro y acepta la misión
- [ ] Objetivo cambia a recoger materiales con contador `(0/3)`
- [ ] Recoger cartón, alambre y chapitas incrementa contador e inventario `[I]`
- [ ] Al tener los 3 materiales, objetivo cambia a **Volvé con Pedro**
- [ ] Segunda conversación con Pedro completa la misión
- [ ] Aparece banner **Garaje desbloqueado**
- [ ] HUD de misión se oculta al completar

## Regresión

- [ ] NPC tiene prioridad sobre pickup cuando ambos están cerca
- [ ] Movimiento WASD y cámara sin cambios
- [ ] `cargo clippy --features dev_fast -- -D warnings`
- [ ] `cargo test --workspace --features dev_fast`
