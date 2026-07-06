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
