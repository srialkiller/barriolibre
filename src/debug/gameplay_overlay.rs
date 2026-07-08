use bevy::prelude::*;

#[derive(Resource, Debug, Default)]
pub struct GameplayDebugState {
    pub visible: bool,
}

#[derive(Component)]
pub struct GameplayDebugRoot;

#[derive(Component)]
pub struct GameplayDebugText;
