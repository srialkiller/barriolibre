use bevy::prelude::*;

use crate::core::states::GameState;
use crate::ui::menus::systems::{
    handle_menu_input_system, setup_main_menu_system, teardown_main_menu_system,
};

pub struct MenuPlugin;

impl Plugin for MenuPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(OnEnter(GameState::MainMenu), setup_main_menu_system)
            .add_systems(OnExit(GameState::MainMenu), teardown_main_menu_system)
            .add_systems(
                Update,
                handle_menu_input_system.run_if(in_state(GameState::MainMenu)),
            );
    }
}
