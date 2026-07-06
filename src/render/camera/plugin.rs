use bevy::prelude::*;

use crate::core::states::GameState;
use crate::render::camera::systems::{focus_iso_camera_system, setup_default_camera_system};

pub struct CameraPlugin;

impl Plugin for CameraPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup_default_camera_system)
            .add_systems(
                OnEnter(GameState::Gameplay),
                focus_iso_camera_system,
            );
    }
}
