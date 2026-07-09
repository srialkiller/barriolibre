use bevy::diagnostic::{DiagnosticsStore, FrameTimeDiagnosticsPlugin};
use bevy::prelude::*;

use crate::assets::registry::AssetRegistry;
use crate::core::states::GameState;
use crate::ui::UiFont;
use crate::debug::gameplay_overlay::{GameplayDebugRoot, GameplayDebugState, GameplayDebugText};
use crate::debug::overlay::{DebugOverlayRoot, DebugOverlayState, DebugOverlayText};
use crate::game::player::components::{GridPosition, PlayerVelocity};
use crate::render::isometric::world_to_grid_f;

pub struct DebugPlugin;

impl Plugin for DebugPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<DebugOverlayState>()
            .init_resource::<GameplayDebugState>()
            .add_plugins(FrameTimeDiagnosticsPlugin)
            .add_systems(Startup, (spawn_debug_overlay_system, spawn_gameplay_debug_system))
            .add_systems(
                Update,
                (
                    toggle_debug_overlay_system,
                    update_debug_overlay_system,
                    toggle_gameplay_debug_system,
                    update_gameplay_debug_system,
                ),
            );
    }
}

fn spawn_debug_overlay_system(mut commands: Commands, ui_font: Res<UiFont>) {
    commands
        .spawn((
            DebugOverlayRoot,
            Node {
                position_type: PositionType::Absolute,
                top: Val::Px(8.0),
                left: Val::Px(8.0),
                padding: UiRect::all(Val::Px(8.0)),
                display: Display::None,
                ..default()
            },
            BackgroundColor(Color::srgba(0.0, 0.0, 0.0, 0.75)),
        ))
        .with_children(|parent| {
            parent.spawn((
                DebugOverlayText,
                Text::new("Debug Overlay"),
                ui_font.sized(16.0),
                TextColor(Color::srgb(0.9, 0.95, 1.0)),
            ));
        });
}

fn spawn_gameplay_debug_system(mut commands: Commands, ui_font: Res<UiFont>) {
    commands
        .spawn((
            GameplayDebugRoot,
            Node {
                position_type: PositionType::Absolute,
                top: Val::Px(8.0),
                right: Val::Px(8.0),
                padding: UiRect::all(Val::Px(8.0)),
                display: Display::None,
                ..default()
            },
            BackgroundColor(Color::srgba(0.0, 0.0, 0.0, 0.75)),
        ))
        .with_children(|parent| {
            parent.spawn((
                GameplayDebugText,
                Text::new("Gameplay Debug"),
                ui_font.sized(16.0),
                TextColor(Color::srgb(0.85, 1.0, 0.85)),
            ));
        });
}

fn toggle_debug_overlay_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    mut overlay_state: ResMut<DebugOverlayState>,
    mut nodes: Query<&mut Node, With<DebugOverlayRoot>>,
) {
    if keyboard.just_pressed(KeyCode::F3) {
        overlay_state.visible = !overlay_state.visible;
        for mut node in &mut nodes {
            node.display = if overlay_state.visible { Display::Flex } else { Display::None };
        }
    }
}

fn toggle_gameplay_debug_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    state: Res<State<GameState>>,
    mut overlay_state: ResMut<GameplayDebugState>,
    mut nodes: Query<&mut Node, With<GameplayDebugRoot>>,
) {
    if state.get() != &GameState::Gameplay {
        return;
    }
    if keyboard.just_pressed(KeyCode::F1) {
        overlay_state.visible = !overlay_state.visible;
        for mut node in &mut nodes {
            node.display = if overlay_state.visible { Display::Flex } else { Display::None };
        }
    }
}

fn update_debug_overlay_system(
    overlay_state: Res<DebugOverlayState>,
    state: Res<State<GameState>>,
    registry: Res<AssetRegistry>,
    diagnostics: Res<DiagnosticsStore>,
    mut text_query: Query<&mut Text, With<DebugOverlayText>>,
) {
    if !overlay_state.visible {
        return;
    }

    let fps = diagnostics
        .get(&FrameTimeDiagnosticsPlugin::FPS)
        .and_then(|diagnostic| diagnostic.smoothed())
        .unwrap_or(0.0);

    let message = format!(
        "FPS: {fps:.1}\nGameState: {:?}\nAssets: {}",
        state.get(),
        registry.total_registered()
    );

    for mut text in &mut text_query {
        text.0 = message.clone();
    }
}

fn update_gameplay_debug_system(
    overlay_state: Res<GameplayDebugState>,
    state: Res<State<GameState>>,
    diagnostics: Res<DiagnosticsStore>,
    player: Query<(&Transform, &GridPosition, &PlayerVelocity)>,
    mut text_query: Query<&mut Text, With<GameplayDebugText>>,
) {
    if state.get() != &GameState::Gameplay || !overlay_state.visible {
        return;
    }

    let fps = diagnostics
        .get(&FrameTimeDiagnosticsPlugin::FPS)
        .and_then(|diagnostic| diagnostic.smoothed())
        .unwrap_or(0.0);

    let message = if let Ok((transform, grid_pos, velocity)) = player.get_single() {
        let world = transform.translation.truncate();
        let (tile_col, tile_row) = world_to_grid_f(world);
        format!(
            "FPS: {fps:.1}\nPos: ({:.1}, {:.1})\nTile: ({:.1}, {:.1})\nGrid: ({:.2}, {:.2})\nSpeed: {:.1} px/s",
            world.x,
            world.y,
            tile_col.floor(),
            tile_row.floor(),
            grid_pos.col,
            grid_pos.row,
            velocity.0.length()
        )
    } else {
        format!("FPS: {fps:.1}\nPlayer: not spawned")
    };

    for mut text in &mut text_query {
        text.0 = message.clone();
    }
}
