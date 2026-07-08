use bevy::input::mouse::MouseWheel;
use bevy::prelude::*;

use super::components::IsoCamera;
use crate::render::isometric::grid_to_world;
use crate::world::map::resources::LoadedNeighborhood;

/// Default orthographic scale: higher = more of the map visible (zoomed out).
pub const DEFAULT_ZOOM: f32 = 3.5;
const MIN_ZOOM: f32 = 1.0;
const MAX_ZOOM: f32 = 9.0;
const ZOOM_KEY_SPEED: f32 = 2.5;
const ZOOM_WHEEL_STEP: f32 = 0.35;
/// Pan speed in world px/sec at scale 1.0; scaled by zoom so it feels constant.
const PAN_SPEED: f32 = 600.0;

pub fn setup_default_camera_system(mut commands: Commands) {
    commands.spawn((
        IsoCamera,
        Camera2d,
        OrthographicProjection {
            scale: DEFAULT_ZOOM,
            ..OrthographicProjection::default_2d()
        },
        Name::new("IsoCamera"),
    ));
}

pub fn focus_iso_camera_system(
    neighborhood: Res<LoadedNeighborhood>,
    mut cameras: Query<&mut Transform, With<IsoCamera>>,
) {
    let center_grid_x = neighborhood.width as f32 / 2.0 - 0.5;
    let center_grid_y = neighborhood.height as f32 / 2.0 - 0.5;
    let map_center = grid_to_world(center_grid_x as i32, center_grid_y as i32);

    for mut transform in &mut cameras {
        transform.translation = Vec3::new(map_center.x, map_center.y, 1000.0);
    }
}

/// Pan with WASD / arrow keys (debug only). Zoom with wheel or Q/E in gameplay.
pub fn camera_control_system(
    time: Res<Time>,
    keyboard: Res<ButtonInput<KeyCode>>,
    mut wheel_events: EventReader<MouseWheel>,
    mut cameras: Query<(&mut Transform, &mut OrthographicProjection), With<IsoCamera>>,
) {
    let Ok((_transform, mut projection)) = cameras.get_single_mut() else {
        return;
    };

    let mut zoom_delta = 0.0;
    for event in wheel_events.read() {
        zoom_delta -= event.y * ZOOM_WHEEL_STEP;
    }
    if keyboard.any_pressed([KeyCode::KeyQ, KeyCode::Minus, KeyCode::NumpadSubtract]) {
        zoom_delta += ZOOM_KEY_SPEED * time.delta_secs();
    }
    if keyboard.any_pressed([KeyCode::KeyE, KeyCode::Equal, KeyCode::NumpadAdd]) {
        zoom_delta -= ZOOM_KEY_SPEED * time.delta_secs();
    }
    if zoom_delta != 0.0 {
        projection.scale = (projection.scale + zoom_delta).clamp(MIN_ZOOM, MAX_ZOOM);
    }
}

/// Free camera pan — disabled during normal gameplay (WASD moves the player).
pub fn camera_pan_system(
    time: Res<Time>,
    keyboard: Res<ButtonInput<KeyCode>>,
    mut cameras: Query<(&mut Transform, &OrthographicProjection), With<IsoCamera>>,
) {
    let Ok((mut transform, projection)) = cameras.get_single_mut() else {
        return;
    };

    let mut direction = Vec2::ZERO;
    if keyboard.any_pressed([KeyCode::KeyW, KeyCode::ArrowUp]) {
        direction.y += 1.0;
    }
    if keyboard.any_pressed([KeyCode::KeyS, KeyCode::ArrowDown]) {
        direction.y -= 1.0;
    }
    if keyboard.any_pressed([KeyCode::KeyA, KeyCode::ArrowLeft]) {
        direction.x -= 1.0;
    }
    if keyboard.any_pressed([KeyCode::KeyD, KeyCode::ArrowRight]) {
        direction.x += 1.0;
    }
    if direction != Vec2::ZERO {
        let movement =
            direction.normalize() * PAN_SPEED * projection.scale * time.delta_secs();
        transform.translation.x += movement.x;
        transform.translation.y += movement.y;
    }
}

pub fn grid_to_iso(grid_x: i32, grid_y: i32) -> Vec3 {
    let world = grid_to_world(grid_x, grid_y);
    Vec3::new(world.x, world.y, 0.0)
}

pub fn iso_sort_key(grid_x: i32, grid_y: i32) -> f32 {
    crate::render::isometric::iso_sort_key(grid_x, grid_y)
}
