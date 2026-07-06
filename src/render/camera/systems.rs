use bevy::prelude::*;

use super::components::IsoCamera;
use crate::render::isometric::grid_to_world;
use crate::world::map::resources::LoadedNeighborhood;

pub fn setup_default_camera_system(mut commands: Commands) {
    commands.spawn((IsoCamera, Camera2d, Name::new("IsoCamera")));
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

pub fn grid_to_iso(grid_x: i32, grid_y: i32) -> Vec3 {
    let world = grid_to_world(grid_x, grid_y);
    Vec3::new(world.x, world.y, 0.0)
}

pub fn iso_sort_key(grid_x: i32, grid_y: i32) -> f32 {
    crate::render::isometric::iso_sort_key(grid_x, grid_y)
}
