use bevy::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

use crate::render::isometric::world_to_grid_f;

/// Sub-tile collision rectangle in grid coordinates (col, row are fractional;
/// width/height are in cells). A point (pc, pr) is blocked if it falls inside
/// any zone: col <= pc < col+width AND row <= pr < row+height.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CollisionZoneRect {
    pub col: f32,
    pub row: f32,
    pub width: f32,
    pub height: f32,
}

/// Tile walkability for player movement (row-major `[row][col]`).
#[derive(Resource, Debug, Clone)]
pub struct CollisionGrid {
    pub width: usize,
    pub height: usize,
    pub blocked: Vec<Vec<bool>>,
    /// Sub-tile rectangles for fine-grained prop collisions (trees, lamps, etc.)
    pub zones: Vec<CollisionZoneRect>,
    pub from_file: bool,
    pub dirty: bool,
}

impl Default for CollisionGrid {
    fn default() -> Self {
        Self {
            width: 0,
            height: 0,
            blocked: Vec::new(),
            zones: Vec::new(),
            from_file: false,
            dirty: false,
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
        if !self.is_walkable_cell(col.floor() as i32, row.floor() as i32) {
            return false;
        }
        self.zones.iter().all(|z| !point_in_zone(col, row, z))
    }

    pub fn is_walkable_world_radius(&self, world: Vec2, radius_cells: f32) -> bool {
        let (col, row) = world_to_grid_f(world);
        let samples = [
            (col, row),
            (col + radius_cells, row),
            (col - radius_cells, row),
            (col, row + radius_cells),
            (col, row - radius_cells),
        ];
        samples.iter().all(|(sc, sr)| self.is_walkable_f(*sc, *sr))
    }

    pub fn set_blocked(&mut self, col: i32, row: i32, blocked: bool) -> bool {
        if col < 0 || row < 0 || col >= self.width as i32 || row >= self.height as i32 {
            return false;
        }
        let cell = &mut self.blocked[row as usize][col as usize];
        if *cell == blocked {
            return false;
        }
        *cell = blocked;
        self.dirty = true;
        true
    }

    pub fn blocked_count(&self) -> usize {
        self.blocked.iter().flatten().filter(|cell| **cell).count()
    }

    pub fn clear_all(&mut self) {
        for row in &mut self.blocked {
            row.fill(false);
        }
        self.dirty = true;
    }

    pub fn paint_brush(&mut self, center_col: i32, center_row: i32, radius: i32, blocked: bool) {
        for d_row in -radius..=radius {
            for d_col in -radius..=radius {
                let _ = self.set_blocked(center_col + d_col, center_row + d_row, blocked);
            }
        }
    }

    pub fn to_cells(&self) -> Vec<[i32; 2]> {
        let mut cells = Vec::new();
        for (row, row_data) in self.blocked.iter().enumerate() {
            for (col, blocked) in row_data.iter().enumerate() {
                if *blocked {
                    cells.push([col as i32, row as i32]);
                }
            }
        }
        cells
    }
}

#[derive(Resource, Debug)]
pub struct CollisionEditorState {
    pub active: bool,
    pub status: String,
    pub hover_prop_id: Option<String>,
    pub hover_col: i32,
    pub hover_row: i32,
    /// Brush radius in cells (0 = 1 cell, 1 = 3x3, 2 = 5x5).
    pub brush_radius: i32,
    pub drag_pan_active: bool,
    pub last_cursor: Option<Vec2>,
}

impl Default for CollisionEditorState {
    fn default() -> Self {
        Self {
            active: false,
            status: String::new(),
            hover_prop_id: None,
            hover_col: 0,
            hover_row: 0,
            brush_radius: 0,
            drag_pan_active: false,
            last_cursor: None,
        }
    }
}

pub fn point_in_zone(col: f32, row: f32, zone: &CollisionZoneRect) -> bool {
    col >= zone.col
        && col < zone.col + zone.width
        && row >= zone.row
        && row < zone.row + zone.height
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CollisionFileData {
    pub barrio_id: String,
    #[serde(default = "default_collision_version")]
    pub version: u32,
    #[serde(default)]
    pub cells: Vec<[i32; 2]>,
    #[serde(default)]
    pub zones: Vec<CollisionZoneRect>,
}

fn default_collision_version() -> u32 {
    1
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct PropFootprintsFile {
    #[serde(default = "default_collision_version")]
    pub version: u32,
    #[serde(default)]
    pub footprints: HashMap<String, Vec<[i32; 2]>>,
}

#[derive(Resource, Debug, Clone, Default)]
pub struct PropFootprints {
    pub footprints: HashMap<String, Vec<[i32; 2]>>,
}

impl PropFootprints {
    pub fn offsets_for(&self, prop_id: &str) -> Option<&Vec<[i32; 2]>> {
        self.footprints.get(prop_id)
    }

    pub fn set_offsets(&mut self, prop_id: String, offsets: Vec<[i32; 2]>) {
        self.footprints.insert(prop_id, offsets);
    }
}

#[derive(Component)]
pub struct CollisionOverlayRoot;

#[derive(Component)]
#[allow(dead_code)]
pub struct CollisionOverlayCell {
    pub col: i32,
    pub row: i32,
}

#[derive(Component)]
pub struct CollisionEditorHudRoot;

#[derive(Component)]
pub struct CollisionEditorHudText;

#[derive(Component)]
pub struct CollisionBrushPreview;

#[derive(Resource, Debug, Default)]
pub struct CollisionOverlayAssets {
    pub marker: Handle<Image>,
}
