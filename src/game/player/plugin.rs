use bevy::prelude::*;

use crate::core::schedule::GameSet;
use crate::core::states::GameState;
use crate::game::player::animation_system::player_animation_system;
use crate::game::player::camera_system::player_camera_follow_system;
use crate::game::player::depth_system::player_depth_system;
use crate::game::player::interaction_system::{
    interact_with_npc_system, spawn_interaction_ui_system,
};
use crate::game::player::movement_system::player_movement_system;
use crate::game::player::events::NpcInteracted;
use crate::game::player::resources::{PlayerAssets, PlayerConfig, PlayerInteractionState};
use crate::game::player::spawn_system::{load_player_assets_system, spawn_player_system};
use crate::world::collision::resources::CollisionEditorState;

pub struct PlayerPlugin;

impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<PlayerConfig>()
            .init_resource::<PlayerAssets>()
            .init_resource::<PlayerInteractionState>()
            .add_event::<NpcInteracted>()
            .add_systems(Startup, spawn_interaction_ui_system)
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
                    .run_if(|editor: Res<CollisionEditorState>| !editor.active)
                    .in_set(GameSet::Movement),
            )
            .add_systems(
                Update,
                interact_with_npc_system
                    .run_if(in_state(GameState::Gameplay))
                    .in_set(GameSet::Interaction),
            );
    }
}
