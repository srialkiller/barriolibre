use bevy::prelude::*;

#[derive(Component, Debug)]
#[allow(dead_code)]
pub struct MapTile {
    pub grid_x: i32,
    pub grid_y: i32,
    pub tile_id: String,
}

#[derive(Component, Debug)]
pub struct MapRoot;

#[derive(Component, Debug)]
pub struct PropRoot;

#[derive(Component, Debug)]
#[allow(dead_code)]
pub struct MapProp {
    pub prop_id: String,
    pub col: f32,
    pub row: f32,
}

#[derive(Component, Debug)]
pub struct NeighborhoodNpc {
    pub npc_id: String,
    pub display_name: String,
    pub dialogue: String,
}
