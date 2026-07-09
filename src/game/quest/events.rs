use bevy::prelude::*;

#[derive(Event, Debug, Clone, PartialEq, Eq)]
pub struct QuestCompleted {
    pub quest_id: String,
}
