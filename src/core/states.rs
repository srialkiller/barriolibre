use bevy::prelude::*;

#[derive(States, Clone, Eq, PartialEq, Debug, Hash, Default)]
#[allow(dead_code)]
pub enum GameState {
    #[default]
    Boot,
    Loading,
    MainMenu,
    Gameplay,
    Paused,
    Debug,
}
