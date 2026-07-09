use bevy::prelude::*;

use crate::core::schedule::GameSet;
use crate::core::states::GameState;
use crate::game::garage::events::GarageUnlocked;
use crate::game::garage::resources::GarageAccess;
use crate::game::garage::systems::{
    handle_garage_unlock_system, spawn_garage_ui_system, update_garage_unlock_banner_system,
    GarageUnlockBannerState,
};

pub struct GaragePlugin;

impl Plugin for GaragePlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<GarageAccess>()
            .init_resource::<GarageUnlockBannerState>()
            .add_event::<GarageUnlocked>()
            .add_systems(Startup, spawn_garage_ui_system)
            .add_systems(
                Update,
                handle_garage_unlock_system.run_if(in_state(GameState::Gameplay)),
            )
            .add_systems(
                Update,
                update_garage_unlock_banner_system
                    .run_if(in_state(GameState::Gameplay))
                    .in_set(GameSet::UI),
            );
    }
}
