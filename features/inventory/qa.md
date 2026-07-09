# Inventory — QA

## Criterios de aceptación

| ID | Criterio | Prioridad |
|---|---|---|
| I-QA-01 | Pickup material incrementa stack correcto | P0 |
| I-QA-02 | Inventario muestra cantidades actuales | P0 |
| I-QA-03 | Jugador aparece en SpawnPoint exportado desde Tiled | P0 |
| I-QA-04 | Movimiento y colisión no tienen regresiones | P0 |
| I-QA-05 | NPC muestra diálogo al presionar `E` | P0 |
| I-QA-06 | Los tres pickups se pueden recoger una sola vez | P0 |
| I-QA-07 | Inventario abre/cierra con `I` sin detener el runtime | P0 |
| I-QA-08 | Craft, vehículos, carreras y save avanzado no se incluyen | P1 |

## Verificación automatizada

- [x] `cargo fmt --all -- --check`
- [x] `cargo clippy --all-targets --features dev_fast -- -D warnings`
- [x] `cargo test --workspace --features dev_fast` — 11 tests
- [x] `cargo run -p map_validator -- data/maps/barrio_tutorial_01`
- [x] `cargo run --features dev_fast` inicia sin errores de aplicación

## Playtest manual

- [ ] Entrar al barrio y confirmar spawn `[13, 13]`
- [ ] Caminar hasta Tomás y abrir/cerrar diálogo con `E`
- [ ] Recoger Cartón limpio, Alambre y Chapitas con `E`
- [ ] Abrir inventario con `I` y confirmar cantidad `×1` para cada material

## Visual (Art Director)

- [ ] Pickup legible sobre el mapa isométrico
- [ ] Prompts de NPC y pickup no se superponen
- [ ] Panel de inventario legible a 1280×720

## Regresión

- [x] Stack de material suma cantidades en unit test
- [x] Inventario vacío no crashea ni oculta el mapa permanentemente
