use bevy::prelude::*;

use crate::core::states::GameState;
use crate::world::collision::resources::CollisionGrid;
use crate::world::collision::systems::build_collision_grid_system;

pub struct CollisionPlugin;

impl Plugin for CollisionPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<CollisionGrid>()
            .add_systems(OnEnter(GameState::Gameplay), build_collision_grid_system);
    }
}
