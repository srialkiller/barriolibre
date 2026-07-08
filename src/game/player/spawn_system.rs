use bevy::prelude::*;
use bevy::sprite::Anchor;
use tracing::warn;

use crate::game::player::components::{
    AnimState, Facing, GridPosition, Player, PlayerAnimation, PlayerSprite, PlayerVelocity,
};
use crate::game::player::resources::{PlayerAnimDefinitions, PlayerAssets, PlayerConfig};
use crate::render::isometric::grid_to_world_f;
use crate::world::map::resources::LoadedNeighborhood;

const PLAYER_TEXTURE_PATH: &str = "player/player.png";
const PLAYER_ANIM_PATH: &str = "data/characters/player_animations.json";

pub fn load_player_assets_system(
    asset_server: Res<AssetServer>,
    mut layouts: ResMut<Assets<TextureAtlasLayout>>,
    mut assets: ResMut<PlayerAssets>,
) {
    if assets.loaded {
        return;
    }

    let definitions_text = match std::fs::read_to_string(PLAYER_ANIM_PATH) {
        Ok(text) => text,
        Err(error) => {
            warn!(?error, path = PLAYER_ANIM_PATH, "Failed to read player animations");
            return;
        }
    };

    let definitions: PlayerAnimDefinitions = match serde_json::from_str(&definitions_text) {
        Ok(definitions) => definitions,
        Err(error) => {
            warn!(?error, "Invalid player_animations.json");
            return;
        }
    };

    let layout = TextureAtlasLayout::from_grid(
        UVec2::new(definitions.cell_size[0], definitions.cell_size[1]),
        definitions.columns,
        definitions.rows,
        None,
        None,
    );
    let layout_handle = layouts.add(layout);
    let texture_handle = asset_server.load(PLAYER_TEXTURE_PATH);

    *assets = PlayerAssets {
        loaded: true,
        texture: texture_handle,
        layout: layout_handle,
        definitions,
    };

    tracing::info!("Player assets queued");
}

pub fn spawn_player_system(
    mut commands: Commands,
    assets: Res<PlayerAssets>,
    config: Res<PlayerConfig>,
    neighborhood: Res<LoadedNeighborhood>,
    existing: Query<Entity, With<Player>>,
) {
    if !assets.loaded || !existing.is_empty() {
        return;
    }

    let (spawn_col, spawn_row) = neighborhood
        .spawn_position
        .map(|position| (position[0] as f32, position[1] as f32))
        .unwrap_or((12.0, 11.0));

    let world = grid_to_world_f(spawn_col, spawn_row);
    let display_height = assets.definitions.display_height_px;
    let aspect = assets.definitions.cell_size[0] as f32 / assets.definitions.cell_size[1] as f32;
    let display_width = display_height * aspect;

    commands.spawn((
        Player,
        GridPosition {
            col: spawn_col,
            row: spawn_row,
        },
        PlayerVelocity::default(),
        PlayerAnimation {
            state: AnimState::Idle,
            facing: Facing::South,
            frame_index: 0,
            timer: Timer::from_seconds(
                1.0 / assets.definitions.idle.fps.max(1.0),
                TimerMode::Repeating,
            ),
        },
        PlayerSprite,
        Sprite {
            image: assets.texture.clone(),
            texture_atlas: Some(TextureAtlas {
                layout: assets.layout.clone(),
                index: assets
                    .definitions
                    .atlas_index(AnimState::Idle, Facing::South, 0),
            }),
            custom_size: Some(Vec2::new(display_width, display_height)),
            anchor: Anchor::BottomCenter,
            ..default()
        },
        Transform::from_xyz(world.x, world.y, spawn_col + spawn_row + 0.25),
        Visibility::default(),
        Name::new("Player"),
    ));

    tracing::info!(
        col = spawn_col,
        row = spawn_row,
        zoom = config.camera_zoom,
        "Player spawned"
    );
}
