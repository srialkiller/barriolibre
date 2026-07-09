use bevy::prelude::*;

use crate::game::garage::components::{GarageUnlockBannerRoot, GarageUnlockBannerText};
use crate::ui::UiFont;
use crate::game::garage::events::GarageUnlocked;
use crate::game::garage::resources::GarageAccess;

const BANNER_DURATION_SECONDS: f32 = 6.0;

#[derive(Resource, Debug, Default)]
pub struct GarageUnlockBannerState {
    pub remaining_seconds: f32,
}

pub fn spawn_garage_ui_system(mut commands: Commands, ui_font: Res<UiFont>) {
    commands
        .spawn((
            GarageUnlockBannerRoot,
            Node {
                position_type: PositionType::Absolute,
                top: Val::Px(96.0),
                left: Val::Percent(15.0),
                right: Val::Percent(15.0),
                padding: UiRect::all(Val::Px(14.0)),
                justify_content: JustifyContent::Center,
                display: Display::None,
                ..default()
            },
            BackgroundColor(Color::srgba(0.08, 0.12, 0.06, 0.94)),
        ))
        .with_children(|parent| {
            parent.spawn((
                GarageUnlockBannerText,
                Text::new(""),
                ui_font.sized(19.0),
                TextColor(Color::srgb(0.82, 1.0, 0.68)),
            ));
        });
}

pub fn handle_garage_unlock_system(
    mut events: EventReader<GarageUnlocked>,
    mut access: ResMut<GarageAccess>,
    mut banner: ResMut<GarageUnlockBannerState>,
) {
    for _ in events.read() {
        access.unlocked = true;
        banner.remaining_seconds = BANNER_DURATION_SECONDS;
        tracing::info!("Garage unlocked");
    }
}

pub fn update_garage_unlock_banner_system(
    time: Res<Time>,
    mut banner: ResMut<GarageUnlockBannerState>,
    access: Res<GarageAccess>,
    mut nodes: Query<&mut Node, With<GarageUnlockBannerRoot>>,
    mut texts: Query<&mut Text, With<GarageUnlockBannerText>>,
) {
    if !access.unlocked {
        return;
    }

    if banner.remaining_seconds > 0.0 {
        banner.remaining_seconds = (banner.remaining_seconds - time.delta_secs()).max(0.0);
    }

    let visible = banner.remaining_seconds > 0.0;
    let message = "Garaje desbloqueado — la fabricación llegará pronto";

    for mut node in &mut nodes {
        node.display = if visible { Display::Flex } else { Display::None };
    }
    if visible {
        for mut text in &mut texts {
            text.0 = message.to_string();
        }
    }
}
