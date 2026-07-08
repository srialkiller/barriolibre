use bevy::prelude::*;

use crate::game::player::components::{GridPosition, Player};
use crate::render::isometric::iso_sort_key;

pub fn player_depth_system(
    mut query: Query<(&GridPosition, &mut Transform), With<Player>>,
) {
    for (grid_pos, mut transform) in &mut query {
        let col = grid_pos.col.floor() as i32;
        let row = grid_pos.row.floor() as i32;
        transform.translation.z = iso_sort_key(col, row) + 0.25;
    }
}
