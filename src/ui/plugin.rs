use bevy::prelude::*;

use crate::ui::font::load_ui_font_system;

pub struct UiPlugin;

impl Plugin for UiPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(PreStartup, load_ui_font_system);
    }
}
