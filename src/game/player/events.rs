use bevy::prelude::*;

#[derive(Event, Debug, Clone, PartialEq, Eq)]
pub struct NpcInteracted {
    pub npc_id: String,
}
