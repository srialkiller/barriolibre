use bevy::prelude::*;

use crate::assets::loader::{begin_asset_load_system, load_pending_tiles_system};
use crate::assets::registry::{AssetLoadState, AssetRegistry};
use crate::core::events::AssetsReady;
use crate::core::states::GameState;
use crate::world::map::systems::load_map_during_loading_system;

pub struct AssetPlugin;

impl Plugin for AssetPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<AssetRegistry>()
            .init_resource::<AssetLoadState>()
            .add_event::<AssetsReady>()
            .add_systems(
                Update,
                (
                    load_map_during_loading_system,
                    begin_asset_load_system.after(load_map_during_loading_system),
                    load_pending_tiles_system.after(begin_asset_load_system),
                )
                    .chain()
                    .run_if(in_state(GameState::Loading)),
            );
    }
}
