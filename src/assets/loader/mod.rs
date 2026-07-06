use bevy::prelude::*;
use bevy::render::render_resource::{Extent3d, TextureDimension, TextureFormat};
use tracing::warn;

use crate::assets::manifest::{
    collect_map_tile_ids, read_layout_tile_ids, resolve_tile_path, tile_file_exists,
};
use crate::assets::registry::{AssetLoadState, AssetRegistry, GeneratedManifest, PackManifest, TileId};
use crate::core::events::AssetsReady;
use crate::core::resources::GameConfig;
use crate::core::states::GameState;
use crate::world::map::resources::{LoadedNeighborhood, MapLoadState};

pub fn begin_asset_load_system(
    config: Res<GameConfig>,
    map_load_state: Res<MapLoadState>,
    neighborhood: Res<LoadedNeighborhood>,
    mut load_state: ResMut<AssetLoadState>,
) {
    if load_state.finished || !load_state.pending_ids.is_empty() {
        return;
    }

    if !map_load_state.loaded && neighborhood.ground_layer.is_empty() {
        return;
    }

    let manifest_text = match std::fs::read_to_string(&config.manifest_path) {
        Ok(text) => text,
        Err(error) => {
            warn!(?error, "Failed to read manifest");
            return;
        }
    };

    let pack: PackManifest = match serde_json::from_str(&manifest_text) {
        Ok(pack) => pack,
        Err(error) => {
            warn!(?error, "Invalid pack manifest JSON");
            return;
        }
    };

    let pending_ids = if config.load_full_pack {
        let generated_text = match std::fs::read_to_string(&config.generated_path) {
            Ok(text) => text,
            Err(error) => {
                warn!(?error, "Failed to read generated manifest");
                return;
            }
        };

        let generated: GeneratedManifest = match serde_json::from_str(&generated_text) {
            Ok(generated) => generated,
            Err(error) => {
                warn!(?error, "Invalid generated manifest JSON");
                return;
            }
        };

        generated.generated.into_iter().map(TileId::new).collect()
    } else if !neighborhood.ground_layer.is_empty() {
        collect_map_tile_ids(&neighborhood)
    } else {
        read_layout_tile_ids(&config.default_map).unwrap_or_default()
    };

    if pending_ids.is_empty() {
        warn!("No tile IDs resolved for loading");
        return;
    }

    load_state.manifest_verified = true;
    load_state.pack_id = pack.pack_id;
    load_state.pending_ids = pending_ids;

    tracing::info!(
        pack = %load_state.pack_id,
        version = %pack.version,
        base_path = %pack.base_path,
        tiles = load_state.pending_ids.len(),
        load_full_pack = config.load_full_pack,
        "Manifest verified — loading tiles"
    );
}

pub fn load_pending_tiles_system(
    config: Res<GameConfig>,
    asset_server: Res<AssetServer>,
    mut images: ResMut<Assets<Image>>,
    mut load_state: ResMut<AssetLoadState>,
    mut registry: ResMut<AssetRegistry>,
    mut assets_ready: EventWriter<AssetsReady>,
    mut next_state: ResMut<NextState<GameState>>,
) {
    if load_state.finished || load_state.pending_ids.is_empty() {
        return;
    }

    let pending: Vec<TileId> = load_state.pending_ids.drain(..).collect();

    for tile_id in pending {
        if tile_file_exists(&tile_id) {
            let path = resolve_tile_path(&tile_id);
            let handle = asset_server.load(path);
            registry.register_tile(tile_id, handle);
        } else {
            let handle = images.add(placeholder_image_for_tile(&tile_id));
            registry.register_tile(tile_id, handle);
            registry.register_missing();
        }
    }

    load_state.finished = true;
    assets_ready.send(AssetsReady);
    tracing::info!(
        pack = %load_state.pack_id,
        dev_hot_reload = config.dev_hot_reload,
        mods = %config.mods_directory,
        loaded = registry.loaded_count(),
        missing = registry.missing_count(),
        "Assets ready"
    );
    next_state.set(GameState::MainMenu);
}

fn placeholder_image_for_tile(tile_id: &TileId) -> Image {
    let (red, green, blue) = placeholder_color(&tile_id.0);
    let width = crate::render::isometric::TILE_PX_WIDTH as u32;
    let height = crate::render::isometric::TILE_PX_HEIGHT as u32;
    let mut data = vec![0_u8; (width * height * 4) as usize];

    for pixel in data.chunks_mut(4) {
        pixel[0] = red;
        pixel[1] = green;
        pixel[2] = blue;
        pixel[3] = 255;
    }

    let mut image = Image::new(
        Extent3d {
            width,
            height,
            depth_or_array_layers: 1,
        },
        TextureDimension::D2,
        data,
        TextureFormat::Rgba8UnormSrgb,
        default(),
    );
    image.sampler = default();
    image
}

fn placeholder_color(tile_id: &str) -> (u8, u8, u8) {
    if tile_id.starts_with("road_") {
        (70, 70, 75)
    } else if tile_id.starts_with("sidewalk_") {
        (180, 175, 165)
    } else if tile_id.starts_with("grass_") {
        (90, 150, 70)
    } else if tile_id.starts_with("curb_") {
        (120, 120, 125)
    } else {
        (100, 100, 110)
    }
}
