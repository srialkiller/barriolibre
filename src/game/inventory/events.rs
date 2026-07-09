use bevy::prelude::*;

use crate::game::inventory::resources::MaterialId;

#[derive(Event, Debug, Clone)]
pub struct PickupCollected {
    pub material_id: MaterialId,
    pub display_name: String,
    pub amount: u32,
    pub new_total: u32,
}

#[derive(Event, Debug, Clone)]
pub struct ItemCollected {
    pub material_id: MaterialId,
    pub display_name: String,
    pub amount: u32,
    pub new_total: u32,
}

impl From<PickupCollected> for ItemCollected {
    fn from(event: PickupCollected) -> Self {
        Self {
            material_id: event.material_id,
            display_name: event.display_name,
            amount: event.amount,
            new_total: event.new_total,
        }
    }
}
