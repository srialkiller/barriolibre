use bevy::prelude::*;
use tracing::info;

use super::events::GameStateChanged;
use super::states::GameState;

pub fn boot_to_loading_system(mut next_state: ResMut<NextState<GameState>>) {
    info!("Boot → Loading");
    next_state.set(GameState::Loading);
}

pub fn log_state_change_system(
    state: Res<State<GameState>>,
    mut last_state: Local<Option<GameState>>,
    mut writer: EventWriter<GameStateChanged>,
) {
    let current = state.get().clone();
    if last_state.as_ref() != Some(&current) {
        if let Some(from) = last_state.replace(current.clone()) {
            info!(?from, ?current, "GameState transition");
            writer.send(GameStateChanged { from, to: current });
        }
    }
}
