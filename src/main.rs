//! Carreras de Barrio — Foundation Runtime (Sprint 01).

mod app;
mod assets;
mod core;
mod debug;
mod game;
mod network;
mod render;
mod save;
mod ui;
mod world;

use app::AppPlugin;
use bevy::prelude::*;
use tracing_subscriber::EnvFilter;

fn main() {
    tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| EnvFilter::new("info,barriolibre=debug,bevy=warn")),
        )
        .init();

    tracing::info!("Foundation Runtime operativo");

    App::new().add_plugins(AppPlugin).run();
}

#[cfg(test)]
mod tests {
    #[test]
    fn game_state_has_boot_default() {
        assert_eq!(
            format!("{:?}", super::core::states::GameState::default()),
            "Boot"
        );
    }
}
