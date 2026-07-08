use std::path::Path;

use bevy::prelude::*;
use serde::Deserialize;
use tracing::warn;

use crate::world::collision::resources::CollisionGrid;
use crate::world::map::resources::LoadedNeighborhood;

#[derive(Debug, Deserialize)]
struct PropMetaCollision {
    #[serde(default)]
    blocks_movement: bool,
}

#[derive(Debug, Deserialize)]
struct PropMetaFile {
    #[serde(default)]
    collision: Option<PropMetaCollision>,
}

fn prop_blocks_movement(prop_id: &str) -> bool {
    let meta_path = Path::new("assets")
        .join("environment")
        .join("props")
        .join(format!("{prop_id}.meta.json"));

    if meta_path.exists() {
        if let Ok(text) = std::fs::read_to_string(&meta_path) {
            if let Ok(meta) = serde_json::from_str::<PropMetaFile>(&text) {
                if let Some(collision) = meta.collision {
                    return collision.blocks_movement;
                }
            }
        }
    }

    prop_id.starts_with("house_")
        || prop_id == "tree_01"
        || prop_id == "lamp_01"
        || prop_id == "fountain_01"
}

pub fn build_collision_grid_system(
    neighborhood: Res<LoadedNeighborhood>,
    mut grid: ResMut<CollisionGrid>,
) {
    if neighborhood.width == 0 || neighborhood.height == 0 {
        return;
    }

    let width = neighborhood.width;
    let height = neighborhood.height;
    let mut blocked = vec![vec![false; width]; height];

    for prop in &neighborhood.props {
        if !prop_blocks_movement(&prop.prop_id) {
            continue;
        }
        let col = prop.col.floor() as i32;
        let row = prop.row.floor() as i32;
        if col >= 0 && row >= 0 && (col as usize) < width && (row as usize) < height {
            blocked[row as usize][col as usize] = true;
        } else {
            warn!(
                prop_id = %prop.prop_id,
                col,
                row,
                "Prop collision cell outside map bounds"
            );
        }
    }

    let blocked_cells = blocked
        .iter()
        .flatten()
        .filter(|cell| **cell)
        .count();

    *grid = CollisionGrid {
        width,
        height,
        blocked,
    };

    tracing::info!(
        width,
        height,
        blocked_cells,
        "Collision grid built"
    );
}
