use bevy::prelude::*;

use crate::core::states::GameState;
use crate::render::props::systems::spawn_props_system;

pub struct PropPlugin;

impl Plugin for PropPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(OnEnter(GameState::Gameplay), spawn_props_system);
    }
}
