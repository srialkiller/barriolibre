use bevy::prelude::*;
use serde::Deserialize;

use crate::game::player::components::{AnimState, Facing};
use crate::render::camera::systems::DEFAULT_ZOOM;

#[derive(Resource, Debug, Clone)]
pub struct PlayerConfig {
    /// World pixels per second at `PIXELS_PER_UNIT` scale.
    pub move_speed: f32,
    pub camera_lerp: f32,
    pub camera_zoom: f32,
}

impl Default for PlayerConfig {
    fn default() -> Self {
        Self { move_speed: 220.0, camera_lerp: 6.0, camera_zoom: DEFAULT_ZOOM }
    }
}

#[derive(Resource, Debug)]
pub struct PlayerAssets {
    pub loaded: bool,
    pub texture: Handle<Image>,
    pub layout: Handle<TextureAtlasLayout>,
    pub definitions: PlayerAnimDefinitions,
}

impl Default for PlayerAssets {
    fn default() -> Self {
        Self {
            loaded: false,
            texture: Handle::default(),
            layout: Handle::default(),
            definitions: PlayerAnimDefinitions::default(),
        }
    }
}

#[derive(Debug, Clone, Deserialize, Default)]
pub struct PlayerAnimDefinitions {
    pub cell_size: [u32; 2],
    pub columns: u32,
    pub rows: u32,
    pub display_height_px: f32,
    pub idle: IdleAnimDef,
    pub walk: WalkAnimDef,
}

#[derive(Debug, Clone, Deserialize, Default)]
pub struct IdleAnimDef {
    pub frame_start: u32,
    pub frames: u32,
    pub fps: f32,
}

#[derive(Debug, Clone, Deserialize, Default)]
pub struct WalkAnimDef {
    pub frames_per_direction: u32,
    pub fps: f32,
    pub direction_rows: WalkDirectionRows,
}

#[derive(Debug, Clone, Deserialize, Default)]
pub struct WalkDirectionRows {
    pub north: u32,
    pub east: u32,
    pub south: u32,
    pub west: u32,
}

impl PlayerAnimDefinitions {
    pub fn atlas_index(&self, state: AnimState, facing: Facing, frame: usize) -> usize {
        match state {
            AnimState::Idle => {
                let start = self.idle.frame_start as usize;
                start + (frame % self.idle.frames as usize)
            }
            AnimState::Walk => {
                let row = match facing {
                    Facing::North => self.walk.direction_rows.north,
                    Facing::East => self.walk.direction_rows.east,
                    Facing::South => self.walk.direction_rows.south,
                    Facing::West => self.walk.direction_rows.west,
                } as usize;
                let col = frame % self.walk.frames_per_direction as usize;
                row * self.columns as usize + col
            }
        }
    }
}

pub fn facing_from_input(direction: Vec2) -> Facing {
    if direction.length_squared() < f32::EPSILON {
        return Facing::South;
    }
    if direction.x.abs() >= direction.y.abs() {
        if direction.x >= 0.0 {
            Facing::East
        } else {
            Facing::West
        }
    } else if direction.y >= 0.0 {
        Facing::North
    } else {
        Facing::South
    }
}
