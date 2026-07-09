use bevy::prelude::*;

use crate::core::events::NeighborhoodLoaded;
use crate::core::states::GameState;
use crate::world::map::resources::{LoadedNeighborhood, MapLoadState};
use crate::world::map::spawn_system::spawn_neighborhood_npcs_system;

pub struct MapPlugin;

impl Plugin for MapPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<LoadedNeighborhood>()
            .init_resource::<MapLoadState>()
            .add_event::<NeighborhoodLoaded>()
            .add_systems(OnEnter(GameState::Gameplay), spawn_neighborhood_npcs_system);
    }
}
