use bevy::prelude::*;

#[derive(SystemSet, Debug, Hash, PartialEq, Eq, Clone)]
pub enum GameSet {
    Input,
    Movement,
    Interaction,
    Simulation,
    RenderPrep,
    UI,
}
