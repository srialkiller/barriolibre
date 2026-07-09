use bevy::prelude::*;

use crate::assets::registry::{AssetRegistry, TileId};
use crate::render::camera::systems::{grid_to_iso, iso_sort_key};
use crate::render::isometric::{default_tile_anchor, tile_display_size};
use crate::world::map::components::{MapRoot, MapTile};
use crate::world::map::resources::LoadedNeighborhood;

pub fn spawn_tilemap_system(
    mut commands: Commands,
    neighborhood: Res<LoadedNeighborhood>,
    registry: Res<AssetRegistry>,
    existing: Query<Entity, With<MapRoot>>,
) {
    if !existing.is_empty() {
        return;
    }

    // Exact cell size — no content-fit scaling. Upscaling by opaque bounds caused
    // subpixel seams/flicker on road dashes when the camera lerps.
    let tile_size = tile_display_size();
    let tile_anchor = default_tile_anchor();
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
                    Transform::from_xyz(position.x, position.y, z),
                ));
            });
        }
    }
}

fn warn_missing_tile(tile_id: &str) {
    tracing::warn!(tile_id, "Tile not found in AssetRegistry");
}
