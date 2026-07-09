use bevy::prelude::*;

/// UI font with Latin-extended glyphs (es-AR accents, ñ, etc.).
pub const UI_FONT_ASSET: &str = "fonts/NotoSans-Regular.ttf";

#[derive(Resource, Clone)]
pub struct UiFont {
    pub regular: Handle<Font>,
}

impl UiFont {
    pub fn sized(&self, font_size: f32) -> TextFont {
        TextFont {
            font: self.regular.clone(),
            font_size,
            ..default()
        }
    }
}

pub fn load_ui_font_system(asset_server: Res<AssetServer>, mut commands: Commands) {
    commands.insert_resource(UiFont { regular: asset_server.load(UI_FONT_ASSET) });
}
