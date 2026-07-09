use bevy::prelude::*;

use crate::core::schedule::GameSet;
use crate::core::states::GameState;
use crate::game::inventory::events::{ItemCollected, PickupCollected};
use crate::game::inventory::resources::{InventoryUiState, PlayerInventory};
use crate::game::inventory::systems::{
    collect_nearby_pickup_system, log_pickup_feedback_system, spawn_collectibles_system,
    spawn_inventory_ui_system, sync_inventory_ui_system, toggle_inventory_ui_system,
    update_pickup_prompt_system,
};

pub struct InventoryPlugin;

impl Plugin for InventoryPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<PlayerInventory>()
            .init_resource::<InventoryUiState>()
            .add_event::<PickupCollected>()
            .add_event::<ItemCollected>()
            .add_systems(Startup, spawn_inventory_ui_system)
            .add_systems(OnEnter(GameState::Gameplay), spawn_collectibles_system)
            .add_systems(
                Update,
                toggle_inventory_ui_system
                    .run_if(in_state(GameState::Gameplay))
                    .in_set(GameSet::Input),
            )
            .add_systems(
                Update,
                (collect_nearby_pickup_system, update_pickup_prompt_system)
                    .chain()
                    .run_if(in_state(GameState::Gameplay))
                    .in_set(GameSet::Interaction),
            )
            .add_systems(
                Update,
                (sync_inventory_ui_system, log_pickup_feedback_system)
                    .run_if(in_state(GameState::Gameplay))
                    .in_set(GameSet::UI),
            );
    }
}
