use bevy::prelude::*;

use crate::core::config::load_game_config;
use crate::assets::AssetPlugin;
use crate::core::CorePlugin;
use crate::debug::DebugPlugin;
use crate::render::camera::CameraPlugin;
use crate::render::sprites::SpritePlugin;
use crate::ui::menus::MenuPlugin;
use crate::world::map::MapPlugin;

pub struct AppPlugin;

impl Plugin for AppPlugin {
    fn build(&self, app: &mut App) {
        let game_config = load_game_config();

        app.insert_resource(game_config.clone())
            .add_plugins(
                DefaultPlugins
                    .set(WindowPlugin {
                        primary_window: Some(Window {
                            title: game_config.title.clone(),
                            resolution: (
                                game_config.window_width as f32,
                                game_config.window_height as f32,
                            )
                                .into(),
                            ..default()
                        }),
                        ..default()
                    })
                    .set(ImagePlugin::default_nearest())
                    .disable::<bevy::log::LogPlugin>()
                    .disable::<bevy::audio::AudioPlugin>()
                    .disable::<bevy::gilrs::GilrsPlugin>()
                    .disable::<bevy::pbr::PbrPlugin>()
                    .disable::<bevy::gltf::GltfPlugin>()
                    .disable::<bevy::animation::AnimationPlugin>(),
            )
            .add_plugins(CorePlugin)
            .add_plugins(AssetPlugin)
            .add_plugins(MapPlugin)
            .add_plugins(CameraPlugin)
            .add_plugins(SpritePlugin)
            .add_plugins(MenuPlugin)
            .add_plugins(DebugPlugin);
    }
}
