use bevy::diagnostic::{DiagnosticsStore, FrameTimeDiagnosticsPlugin};
use bevy::prelude::*;

use crate::assets::registry::AssetRegistry;
use crate::core::states::GameState;
use crate::debug::overlay::{DebugOverlayRoot, DebugOverlayState, DebugOverlayText};

pub struct DebugPlugin;

impl Plugin for DebugPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<DebugOverlayState>()
            .add_plugins(FrameTimeDiagnosticsPlugin)
            .add_systems(Startup, spawn_debug_overlay_system)
            .add_systems(
                Update,
                (
                    toggle_debug_overlay_system,
                    update_debug_overlay_system,
                ),
            );
    }
}

fn spawn_debug_overlay_system(mut commands: Commands) {
    commands.spawn((
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
            TextFont {
                font_size: 16.0,
                ..default()
            },
            TextColor(Color::srgb(0.9, 0.95, 1.0)),
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
            node.display = if overlay_state.visible {
                Display::Flex
            } else {
                Display::None
            };
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
