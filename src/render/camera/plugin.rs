use bevy::prelude::*;

use crate::core::states::GameState;
use crate::render::camera::systems::{
    camera_control_system, camera_pan_system, focus_iso_camera_system, setup_default_camera_system,
};
use crate::world::collision::resources::CollisionEditorState;

pub struct CameraPlugin;

impl Plugin for CameraPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup_default_camera_system)
            .add_systems(OnEnter(GameState::Gameplay), focus_iso_camera_system)
            .add_systems(
                Update,
                (
                    camera_control_system,
                    camera_pan_system.run_if(
                        in_state(GameState::Debug)
                            .or(|editor: Res<CollisionEditorState>| editor.active),
                    ),
                )
                    .run_if(in_state(GameState::Gameplay).or(in_state(GameState::Debug))),
            );
    }
}
