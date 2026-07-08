use bevy::prelude::*;

use crate::render::isometric::world_to_grid_f;

/// Tile walkability for player movement (row-major `[row][col]`).
#[derive(Resource, Debug, Clone)]
pub struct CollisionGrid {
    pub width: usize,
    pub height: usize,
    pub blocked: Vec<Vec<bool>>,
}

impl Default for CollisionGrid {
    fn default() -> Self {
        Self {
            width: 0,
            height: 0,
            blocked: Vec::new(),
        }
    }
}

impl CollisionGrid {
    pub fn is_walkable_cell(&self, col: i32, row: i32) -> bool {
        if col < 0 || row < 0 || col >= self.width as i32 || row >= self.height as i32 {
            return false;
        }
        !self.blocked[row as usize][col as usize]
    }

    pub fn is_walkable_f(&self, col: f32, row: f32) -> bool {
        self.is_walkable_cell(col.floor() as i32, row.floor() as i32)
    }

    pub fn is_walkable_world(&self, world: Vec2) -> bool {
        let (col, row) = world_to_grid_f(world);
        self.is_walkable_f(col, row)
    }
}
