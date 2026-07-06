use bevy::prelude::*;

use super::states::GameState;

#[derive(Event, Debug, Clone)]
pub struct AssetsReady;

#[derive(Event, Debug, Clone)]
#[allow(dead_code)]
pub struct NeighborhoodLoaded {
    pub map_id: String,
}

#[derive(Event, Debug, Clone)]
#[allow(dead_code)]
pub struct GameStateChanged {
    pub from: GameState,
    pub to: GameState,
}
