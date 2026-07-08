use bevy::prelude::*;

use crate::game::player::components::Player;
use crate::game::player::resources::PlayerConfig;
use crate::render::camera::components::IsoCamera;

pub fn player_camera_follow_system(
    time: Res<Time>,
    config: Res<PlayerConfig>,
    player: Query<&Transform, With<Player>>,
    mut cameras: Query<&mut Transform, (With<IsoCamera>, Without<Player>)>,
) {
    let Ok(player_transform) = player.get_single() else {
        return;
    };
    let Ok(mut camera_transform) = cameras.get_single_mut() else {
        return;
    };

    let target = Vec3::new(
        player_transform.translation.x,
        player_transform.translation.y,
        camera_transform.translation.z,
    );
    let alpha = (config.camera_lerp * time.delta_secs()).clamp(0.0, 1.0);
    camera_transform.translation = camera_transform.translation.lerp(target, alpha);
}
