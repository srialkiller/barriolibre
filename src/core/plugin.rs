use bevy::prelude::*;

use super::events::GameStateChanged;
use super::resources::TimeScale;
use super::schedule::GameSet;
use super::states::GameState;
use super::systems::{boot_to_loading_system, log_state_change_system};

pub struct CorePlugin;

impl Plugin for CorePlugin {
    fn build(&self, app: &mut App) {
        app.init_state::<GameState>()
            .init_resource::<TimeScale>()
            .add_event::<GameStateChanged>()
            .configure_sets(
                Update,
                (
                    GameSet::Input,
                    GameSet::Movement,
                    GameSet::Interaction,
                    GameSet::Simulation,
                    GameSet::RenderPrep,
                    GameSet::UI,
                )
                    .chain(),
            )
            .add_systems(Update, boot_to_loading_system.run_if(in_state(GameState::Boot)))
            .add_systems(Update, log_state_change_system);
    }
}
