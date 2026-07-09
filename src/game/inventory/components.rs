use bevy::prelude::*;

use crate::game::inventory::resources::MaterialId;

#[derive(Component, Debug)]
pub struct Collectible {
    pub spawn_id: String,
    pub material_id: MaterialId,
    pub display_name: String,
    pub quantity: u32,
}

#[derive(Component)]
pub struct InventoryUiRoot;

#[derive(Component)]
pub struct InventoryUiText;

#[derive(Component)]
pub struct PickupPromptRoot;

#[derive(Component)]
pub struct PickupPromptText;
