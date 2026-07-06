use std::collections::HashSet;
use std::path::{Path, PathBuf};

use crate::assets::registry::TileId;
use crate::world::map::resources::LoadedNeighborhood;

pub fn resolve_tile_path(tile_id: &TileId) -> String {
    let category = category_for_tile_id(&tile_id.0);
    format!("environment/{category}/{id}.png", id = tile_id.0)
}

pub fn category_for_tile_id(tile_id: &str) -> &'static str {
    if tile_id.starts_with("road_") {
        "roads"
    } else if tile_id.starts_with("sidewalk_") {
        "sidewalks"
    } else if tile_id.starts_with("curb_") {
        "curbs"
    } else if tile_id.starts_with("marking_") {
        "markings"
    } else if tile_id.starts_with("transition_") {
        "transitions"
    } else {
        "terrain"
    }
}

pub fn tile_file_exists(tile_id: &TileId) -> bool {
    Path::new("assets").join(resolve_tile_path(tile_id)).exists()
}

pub fn collect_map_tile_ids(neighborhood: &LoadedNeighborhood) -> Vec<TileId> {
    let mut unique_ids = HashSet::new();

    for row in &neighborhood.ground_layer {
        for tile_id in row {
            unique_ids.insert(tile_id.clone());
        }
    }

    let mut tile_ids: Vec<TileId> = unique_ids.into_iter().map(TileId::new).collect();
    tile_ids.sort_by(|left, right| left.0.cmp(&right.0));
    tile_ids
}

pub fn read_layout_tile_ids(map_id: &str) -> Option<Vec<TileId>> {
    let layout_path = PathBuf::from("data/maps").join(map_id).join("layout.json");
    let layout_text = std::fs::read_to_string(&layout_path).ok()?;
    let layout: serde_json::Value = serde_json::from_str(&layout_text).ok()?;
    let ground = layout.get("layers")?.get("ground")?.as_array()?;

    let mut unique_ids = HashSet::new();
    for row in ground {
        let columns = row.as_array()?;
        for tile_id in columns {
            unique_ids.insert(tile_id.as_str()?.to_owned());
        }
    }

    let mut tile_ids: Vec<TileId> = unique_ids.into_iter().map(TileId::new).collect();
    tile_ids.sort_by(|left, right| left.0.cmp(&right.0));
    Some(tile_ids)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reads_tutorial_map_tile_ids() {
        let ids = read_layout_tile_ids("barrio_tutorial_01").expect("layout");
        assert!(ids.len() < 50, "map-only load should be a small subset of the pack");
        assert!(ids.iter().any(|id| id.0.contains("grass_clean")));
    }

    #[test]
    fn resolves_road_category() {
        let path = resolve_tile_path(&TileId::new("road_straight_h_01"));
        assert_eq!(path, "environment/roads/road_straight_h_01.png");
    }

    #[test]
    fn resolves_terrain_category() {
        let path = resolve_tile_path(&TileId::new("grass_clean_01"));
        assert_eq!(path, "environment/terrain/grass_clean_01.png");
    }
}
