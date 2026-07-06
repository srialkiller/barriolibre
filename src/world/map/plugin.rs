use bevy::prelude::*;

use crate::core::events::NeighborhoodLoaded;
use crate::world::map::resources::{LoadedNeighborhood, MapLoadState};

pub struct MapPlugin;

impl Plugin for MapPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<LoadedNeighborhood>()
            .init_resource::<MapLoadState>()
            .add_event::<NeighborhoodLoaded>();
    }
}
