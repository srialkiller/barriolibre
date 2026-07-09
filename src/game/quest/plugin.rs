use bevy::prelude::*;

use crate::core::schedule::GameSet;
use crate::core::states::GameState;
use crate::game::quest::events::QuestCompleted;
use crate::game::quest::systems::{
    handle_item_collected_quest_system, handle_npc_interacted_quest_system,
    init_tutorial_quest_system, spawn_quest_ui_system, sync_quest_presentations_system,
    sync_quest_ui_system,
};

pub struct QuestPlugin;

impl Plugin for QuestPlugin {
    fn build(&self, app: &mut App) {
        app.add_event::<QuestCompleted>()
            .add_systems(Startup, (init_tutorial_quest_system, spawn_quest_ui_system))
            .add_systems(
                Update,
                (
                    handle_npc_interacted_quest_system,
                    handle_item_collected_quest_system,
                    sync_quest_presentations_system,
                )
                    .chain()
                    .run_if(in_state(GameState::Gameplay)),
            )
            .add_systems(
                Update,
                sync_quest_ui_system
                    .run_if(in_state(GameState::Gameplay))
                    .in_set(GameSet::UI),
            );
    }
}
