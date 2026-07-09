use bevy::prelude::*;

use crate::game::player::components::{
    AnimState, GridPosition, Player, PlayerAnimation, PlayerVelocity,
};
use crate::game::player::resources::{facing_from_input, PlayerConfig};
use crate::render::isometric::world_to_grid_f;
use crate::world::collision::resources::{CollisionEditorState, CollisionGrid};

pub fn player_movement_system(
    time: Res<Time>,
    config: Res<PlayerConfig>,
    editor: Res<CollisionEditorState>,
    grid: Res<CollisionGrid>,
    keyboard: Res<ButtonInput<KeyCode>>,
    mut query: Query<(
        &mut Transform,
        &mut GridPosition,
        &mut PlayerVelocity,
        &mut PlayerAnimation,
        &Player,
    )>,
) {
    if editor.active {
        return;
    }
    let Ok((mut transform, mut grid_pos, mut velocity, mut animation, _)) = query.get_single_mut()
    else {
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
        direction = direction.normalize();
        animation.state = AnimState::Walk;
        animation.facing = facing_from_input(direction);
    } else {
        animation.state = AnimState::Idle;
    }

    velocity.0 = direction * config.move_speed;
    let delta = velocity.0 * time.delta_secs();
    let current = transform.translation.truncate();
    // ~0.2 cell collision radius so feet can't clip into prop footprints.
    const HIT_RADIUS_CELLS: f32 = 0.2;

    let after_x = current + Vec2::new(delta.x, 0.0);
    let mut next = current;
    if grid.is_walkable_world_radius(after_x, HIT_RADIUS_CELLS) {
        next.x = after_x.x;
    }

    let after_y = next + Vec2::new(0.0, delta.y);
    if grid.is_walkable_world_radius(after_y, HIT_RADIUS_CELLS) {
        next.y = after_y.y;
    }

    transform.translation.x = next.x;
    transform.translation.y = next.y;

    let (col, row) = world_to_grid_f(next);
    grid_pos.col = col;
    grid_pos.row = row;
}
