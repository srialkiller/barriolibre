use bevy::prelude::*;

#[derive(Resource, Debug, Default, Clone, Copy, PartialEq, Eq)]
pub struct GarageAccess {
    pub unlocked: bool,
}
