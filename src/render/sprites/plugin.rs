use bevy::prelude::*;

use crate::core::states::GameState;
use crate::render::sprites::systems::spawn_tilemap_system;

pub struct SpritePlugin;

impl Plugin for SpritePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(OnEnter(GameState::Gameplay), spawn_tilemap_system);
    }
}
