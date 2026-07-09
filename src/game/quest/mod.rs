//! Quest domain — tutorial mission flow driven by gameplay events.

pub mod components;
pub mod data;
pub mod events;
pub mod plugin;
pub mod resources;
pub mod systems;

pub use plugin::QuestPlugin;
pub use resources::NpcDialogueOverrides;
