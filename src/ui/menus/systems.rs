use bevy::prelude::*;

use crate::core::states::GameState;
use crate::world::map::resources::LoadedNeighborhood;

#[derive(Component)]
pub struct MainMenuRoot;

pub fn setup_main_menu_system(
    mut commands: Commands,
    neighborhood: Res<LoadedNeighborhood>,
) {
    commands.spawn((
        MainMenuRoot,
        Node {
            width: Val::Percent(100.0),
            height: Val::Percent(100.0),
            justify_content: JustifyContent::Center,
            align_items: AlignItems::Center,
            flex_direction: FlexDirection::Column,
            row_gap: Val::Px(12.0),
            ..default()
        },
    ))
    .with_children(|parent| {
        parent.spawn((
            Text::new("Foundation Runtime operativo"),
            TextFont {
                font_size: 28.0,
                ..default()
            },
            TextColor(Color::srgb(1.0, 0.85, 0.2)),
        ));
        parent.spawn((
            Text::new(format!("Barrio: {}", neighborhood.display_name)),
            TextFont {
                font_size: 20.0,
                ..default()
            },
            TextColor(Color::srgb(0.9, 0.9, 0.95)),
        ));
        parent.spawn((
            Text::new("Presiona Enter para explorar el barrio"),
            TextFont {
                font_size: 18.0,
                ..default()
            },
            TextColor(Color::srgb(0.75, 0.85, 1.0)),
        ));
    });
}

pub fn teardown_main_menu_system(
    mut commands: Commands,
    query: Query<Entity, With<MainMenuRoot>>,
) {
    for entity in &query {
        commands.entity(entity).despawn_recursive();
    }
}

pub fn handle_menu_input_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    mut next_state: ResMut<NextState<GameState>>,
) {
    if keyboard.just_pressed(KeyCode::Enter) || keyboard.just_pressed(KeyCode::NumpadEnter) {
        next_state.set(GameState::Gameplay);
    }
}
