use bevy::prelude::*;

use crate::core::schedule::GameSet;
use crate::core::states::GameState;
use crate::game::player::animation_system::player_animation_system;
use crate::game::player::camera_system::player_camera_follow_system;
use crate::game::player::depth_system::player_depth_system;
use crate::game::player::movement_system::player_movement_system;
use crate::game::player::resources::{PlayerAssets, PlayerConfig};
use crate::game::player::spawn_system::{load_player_assets_system, spawn_player_system};

pub struct PlayerPlugin;

impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<PlayerConfig>()
            .init_resource::<PlayerAssets>()
            .add_systems(
                OnEnter(GameState::Gameplay),
                (load_player_assets_system, spawn_player_system).chain(),
            )
            .add_systems(
                Update,
                (
                    player_movement_system,
                    player_animation_system,
                    player_depth_system,
                    player_camera_follow_system,
                )
                    .chain()
                    .run_if(in_state(GameState::Gameplay))
                    .in_set(GameSet::Movement),
            );
    }
}
