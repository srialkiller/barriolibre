use bevy::prelude::*;

use crate::game::player::components::{GridPosition, Player};

pub fn player_depth_system(mut query: Query<(&GridPosition, &mut Transform), With<Player>>) {
    for (grid_pos, mut transform) in &mut query {
        // Continuous col+row (not floored) so depth tracks the player's feet while
        // moving; flooring caused the sprite to sort behind forward tiles.
        transform.translation.z = grid_pos.col + grid_pos.row + 0.25;
    }
}
