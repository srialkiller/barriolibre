use bevy::prelude::*;
use serde::Deserialize;

#[derive(Resource, Debug, Clone)]
pub struct GameConfig {
    pub title: String,
    pub default_map: String,
    pub manifest_path: String,
    pub generated_path: String,
    pub mods_directory: String,
    pub window_width: u32,
    pub window_height: u32,
    pub dev_hot_reload: bool,
    pub load_full_pack: bool,
}

impl Default for GameConfig {
    fn default() -> Self {
        Self {
            title: "Carreras de Barrio".into(),
            default_map: "barrio_tutorial_01".into(),
            manifest_path: "data/tilesets/environment_base_pack_01_manifest.json".into(),
            generated_path: "data/tilesets/environment_base_pack_01_generated.json".into(),
            mods_directory: "mods".into(),
            window_width: 1280,
            window_height: 720,
            dev_hot_reload: false,
            load_full_pack: false,
        }
    }
}

#[derive(Debug, Deserialize)]
pub struct GameConfigFile {
    pub title: String,
    pub default_map: String,
    pub manifest_path: String,
    pub generated_path: String,
    pub mods_directory: String,
    pub window_width: u32,
    pub window_height: u32,
    pub dev_hot_reload: bool,
    #[serde(default)]
    pub load_full_pack: bool,
}

impl From<GameConfigFile> for GameConfig {
    fn from(value: GameConfigFile) -> Self {
        Self {
            title: value.title,
            default_map: value.default_map,
            manifest_path: value.manifest_path,
            generated_path: value.generated_path,
            mods_directory: value.mods_directory,
            window_width: value.window_width,
            window_height: value.window_height,
            dev_hot_reload: value.dev_hot_reload,
            load_full_pack: value.load_full_pack,
        }
    }
}

#[derive(Resource, Debug, Clone, Copy)]
#[allow(dead_code)]
pub struct TimeScale {
    pub factor: f32,
}

impl Default for TimeScale {
    fn default() -> Self {
        Self { factor: 1.0 }
    }
}
