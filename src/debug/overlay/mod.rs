use bevy::prelude::*;

#[derive(Resource, Debug, Default)]
pub struct DebugOverlayState {
    pub visible: bool,
}

#[derive(Component)]
pub struct DebugOverlayRoot;

#[derive(Component)]
pub struct DebugOverlayText;
