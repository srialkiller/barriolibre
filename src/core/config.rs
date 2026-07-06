use std::fs;

use tracing::warn;

use super::resources::{GameConfig, GameConfigFile};

const CONFIG_PATH: &str = "data/config/game.toml";

pub fn load_game_config() -> GameConfig {
    match fs::read_to_string(CONFIG_PATH) {
        Ok(contents) => match toml::from_str::<GameConfigFile>(&contents) {
            Ok(file) => file.into(),
            Err(error) => {
                warn!(?error, "Invalid game.toml — using defaults");
                GameConfig::default()
            }
        },
        Err(error) => {
            warn!(?error, "Missing game.toml — using defaults");
            GameConfig::default()
        }
    }
}
