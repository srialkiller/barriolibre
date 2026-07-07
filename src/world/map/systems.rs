use std::path::PathBuf;

use bevy::prelude::*;
use tracing::warn;

use crate::core::events::NeighborhoodLoaded;
use crate::core::resources::GameConfig;
use crate::world::map::resources::{
    CollisionFile, LayoutFile, LoadedNeighborhood, MapLoadState, PropsFile, SceneHooksFile,
};

pub fn load_map_during_loading_system(
    config: Res<GameConfig>,
    mut load_state: ResMut<MapLoadState>,
    mut neighborhood: ResMut<LoadedNeighborhood>,
    mut neighborhood_loaded: EventWriter<NeighborhoodLoaded>,
) {
    if load_state.requested {
        return;
    }

    let map_dir = PathBuf::from("data/maps").join(&config.default_map);
    let layout_path = map_dir.join("layout.json");
    let collision_path = map_dir.join("collision.json");
    let hooks_path = map_dir.join("scene_hooks.json");
    let props_path = map_dir.join("props.json");

    let layout_text = match std::fs::read_to_string(&layout_path) {
        Ok(text) => text,
        Err(error) => {
            warn!(?error, path = ?layout_path, "Failed to read layout.json");
            return;
        }
    };

    let layout: LayoutFile = match serde_json::from_str(&layout_text) {
        Ok(layout) => layout,
        Err(error) => {
            warn!(?error, "Invalid layout.json");
            return;
        }
    };

    neighborhood.barrio_id = layout.barrio_id.clone();
    neighborhood.display_name = if layout.display_name.is_empty() {
        layout.barrio_id.clone()
    } else {
        layout.display_name
    };
    neighborhood.width = layout.size[0];
    neighborhood.height = layout.size[1];
    neighborhood.ground_layer = layout.layers.ground;

    neighborhood.props = std::fs::read_to_string(&props_path)
        .ok()
        .and_then(|text| serde_json::from_str::<PropsFile>(&text).ok())
        .map(|file| file.props)
        .unwrap_or_default();

    neighborhood.collision_loaded = collision_path
        .exists()
        && std::fs::read_to_string(&collision_path)
            .ok()
            .and_then(|text| serde_json::from_str::<CollisionFile>(&text).ok())
            .is_some();

    if hooks_path.exists() {
        if let Ok(text) = std::fs::read_to_string(&hooks_path) {
            if let Ok(hooks) = serde_json::from_str::<SceneHooksFile>(&text) {
                neighborhood.spawn_position =
                    hooks.spawn_points.first().map(|spawn| spawn.position);
                neighborhood.hooks_loaded = true;
            }
        }
    }

    load_state.requested = true;
    load_state.loaded = true;

    tracing::info!(
        barrio = %neighborhood.barrio_id,
        width = neighborhood.width,
        height = neighborhood.height,
        "Neighborhood loaded"
    );

    neighborhood_loaded.send(NeighborhoodLoaded {
        map_id: neighborhood.barrio_id.clone(),
    });

    tracing::debug!(map_id = %neighborhood.barrio_id, "NeighborhoodLoaded event emitted");
}
