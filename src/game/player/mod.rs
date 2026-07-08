//! Playable character — locomotion, animation, camera follow (Sprint 02).

pub mod animation_system;
pub mod camera_system;
pub mod components;
pub mod depth_system;
pub mod movement_system;
pub mod plugin;
pub mod resources;
pub mod spawn_system;

pub use plugin::PlayerPlugin;
