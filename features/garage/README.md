# Feature: Garage / Taller

**Status:** spec  
**Phase:** vertical_slice  
**Owner:** `vehicle_designer` + `technical_director`  
**Docs:** [VEHICLE_DESIGN_GUIDE](../../docs/systems/VEHICLE_DESIGN_GUIDE.md), [GAMEPLAY_GUIDE §3](../../docs/game/GAMEPLAY_GUIDE.md)

## Resumen

UI y lógica del taller donde el jugador **ensambla, cambia y mejora** piezas del vehículo. Corazón del pilar Creatividad.

## MVP scope

- [ ] Abrir taller en POI `poi_garage`
- [ ] Ver slots: chasis, motor, ruedas (mínimo 3)
- [ ] Instalar/desinstalar pieza del inventario
- [ ] Preview stats en tiempo real
- [ ] Salir al barrio con vehículo actualizado

## Out of scope (v1)

- Slot especial, escape, cosméticos avanzados
- Animación craft (instant craft en otra feature)

## Dependencias

- `inventory` — piezas en inventario
- `crafting` — obtener piezas iniciales
- Assets: vehicle parts pack (placeholder OK en vertical slice)
