use std::collections::HashMap;

use bevy::prelude::*;

use crate::assets::registry::{AssetRegistry, TileId};
use crate::render::camera::systems::{grid_to_iso, iso_sort_key};
use crate::render::isometric::{
    content_bounds, default_tile_anchor, fit_content_to_cell, tile_display_size,
};
use crate::world::map::components::{MapRoot, MapTile};
use crate::world::map::resources::LoadedNeighborhood;

const CONTENT_ALPHA_THRESHOLD: u8 = 8;

pub fn spawn_tilemap_system(
    mut commands: Commands,
    neighborhood: Res<LoadedNeighborhood>,
    registry: Res<AssetRegistry>,
    images: Res<Assets<Image>>,
    existing: Query<Entity, With<MapRoot>>,
) {
    if !existing.is_empty() {
        return;
    }

    let default_size = tile_display_size();
    let tile_anchor = default_tile_anchor();
    let mut fit_cache: HashMap<String, (Vec2, Vec2)> = HashMap::new();
    let root = commands
        .spawn((
            MapRoot,
            Name::new("MapRoot"),
            Transform::default(),
            Visibility::default(),
        ))
        .id();

    for (row_index, row) in neighborhood.ground_layer.iter().enumerate() {
        for (col_index, tile_id) in row.iter().enumerate() {
            let grid_x = col_index as i32;
            let grid_y = row_index as i32;
            let position = grid_to_iso(grid_x, grid_y);
            let z = iso_sort_key(grid_x, grid_y);

            let handle = registry
                .tile(&TileId::new(tile_id.clone()))
                .cloned()
                .unwrap_or_else(|| {
                    warn_missing_tile(tile_id);
                    Handle::default()
                });

            let (tile_size, offset) =
                *fit_cache.entry(tile_id.clone()).or_insert_with(|| {
                    images
                        .get(&handle)
                        .and_then(|image| {
                            content_bounds(image, CONTENT_ALPHA_THRESHOLD)
                        })
                        .map(|(min, max)| fit_content_to_cell(min, max))
                        .unwrap_or((default_size, Vec2::ZERO))
                });

            commands.entity(root).with_children(|parent| {
                parent.spawn((
                    MapTile {
                        grid_x,
                        grid_y,
                        tile_id: tile_id.clone(),
                    },
                    Sprite {
                        image: handle,
                        custom_size: Some(tile_size),
                        anchor: tile_anchor,
                        ..default()
                    },
                    Transform::from_xyz(
                        position.x + offset.x,
                        position.y + offset.y,
                        z,
                    ),
                ));
            });
        }
    }
}

fn warn_missing_tile(tile_id: &str) {
    tracing::warn!(tile_id, "Tile not found in AssetRegistry");
}
