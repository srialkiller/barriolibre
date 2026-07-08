use bevy::prelude::*;

#[derive(Component, Debug)]
pub struct Player;

#[derive(Component, Debug, Clone, Copy)]
pub struct GridPosition {
    pub col: f32,
    pub row: f32,
}

#[derive(Component, Debug, Clone, Copy, Default)]
pub struct PlayerVelocity(pub Vec2);

#[derive(Component, Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Facing {
    North,
    East,
    South,
    West,
}

#[derive(Component, Debug, Clone, Copy, PartialEq, Eq)]
pub enum AnimState {
    Idle,
    Walk,
}

#[derive(Component, Debug)]
pub struct PlayerAnimation {
    pub state: AnimState,
    pub facing: Facing,
    pub frame_index: usize,
    pub timer: Timer,
}

#[derive(Component, Debug)]
pub struct PlayerSprite;
