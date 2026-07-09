use bevy::prelude::*;

use crate::game::player::components::Player;
use crate::game::player::resources::PlayerConfig;
use crate::render::camera::components::IsoCamera;

#[allow(clippy::type_complexity)]
pub fn player_camera_follow_system(
    time: Res<Time>,
    config: Res<PlayerConfig>,
    player: Query<&Transform, With<Player>>,
    mut cameras: Query<
        (&mut Transform, &OrthographicProjection),
        (With<IsoCamera>, Without<Player>),
    >,
) {
    let Ok(player_transform) = player.get_single() else {
        return;
    };
    let Ok((mut camera_transform, projection)) = cameras.get_single_mut() else {
        return;
    };

    let target = Vec3::new(
        player_transform.translation.x,
        player_transform.translation.y,
        camera_transform.translation.z,
    );
    let alpha = (config.camera_lerp * time.delta_secs()).clamp(0.0, 1.0);
    let lerped = camera_transform.translation.lerp(target, alpha);

    // Snap to world pixel under the current zoom so neighboring tiles don't
    // sample across seams while following the player.
    let pixel = projection.scale.max(0.001);
    camera_transform.translation.x = (lerped.x / pixel).round() * pixel;
    camera_transform.translation.y = (lerped.y / pixel).round() * pixel;
}
