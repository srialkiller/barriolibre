use bevy::prelude::*;
use serde::Deserialize;

#[derive(Resource, Debug, Clone)]
pub struct LoadedNeighborhood {
    pub barrio_id: String,
    pub display_name: String,
    pub width: usize,
    pub height: usize,
    pub ground_layer: Vec<Vec<String>>,
    pub props: Vec<PropInstance>,
    pub spawn_position: Option<[i32; 2]>,
    pub spawn_facing: Option<String>,
    pub npc_spawns: Vec<NpcSpawn>,
    pub pickup_spawns: Vec<PickupSpawn>,
    pub collision_loaded: bool,
    pub hooks_loaded: bool,
}

impl Default for LoadedNeighborhood {
    fn default() -> Self {
        Self {
            barrio_id: String::new(),
            display_name: String::new(),
            width: 0,
            height: 0,
            ground_layer: Vec::new(),
            props: Vec::new(),
            spawn_position: None,
            spawn_facing: None,
            npc_spawns: Vec::new(),
            pickup_spawns: Vec::new(),
            collision_loaded: false,
            hooks_loaded: false,
        }
    }
}

/// One placed prop (house, tree, lamp, ...) read from `props.json`.
///
/// `col`/`row` are fractional grid coordinates of the cell the prop stands on;
/// `width_px`/`height_px` are the proportional on-screen size (same pixel space
/// as tiles, where one tile is 256x128).
#[derive(Debug, Clone, Deserialize)]
pub struct PropInstance {
    pub prop_id: String,
    pub col: f32,
    pub row: f32,
    pub width_px: f32,
    pub height_px: f32,
}

#[derive(Debug, Deserialize)]
pub struct PropsFile {
    #[serde(default)]
    pub props: Vec<PropInstance>,
}

#[derive(Debug, Deserialize)]
pub struct LayoutFile {
    pub barrio_id: String,
    #[serde(default)]
    pub display_name: String,
    pub size: [usize; 2],
    pub layers: LayoutLayers,
}

#[derive(Debug, Deserialize)]
#[allow(dead_code)]
pub struct LayoutLayers {
    pub ground: Vec<Vec<String>>,
    #[serde(default)]
    pub markings: Vec<Vec<String>>,
    #[serde(default)]
    pub overlay: Vec<Vec<String>>,
}

#[derive(Debug, Deserialize)]
#[allow(dead_code)]
pub struct CollisionFile {
    pub barrio_id: String,
    #[serde(default)]
    pub version: u32,
    #[serde(default)]
    pub cells: Vec<[i32; 2]>,
}

#[derive(Debug, Deserialize)]
#[allow(dead_code)]
pub struct SceneHooksFile {
    pub barrio_id: String,
    #[serde(default)]
    pub spawn_points: Vec<SpawnPoint>,
    #[serde(default)]
    pub npcs: Vec<NpcSpawn>,
    #[serde(default)]
    pub pickups: Vec<PickupSpawn>,
}

#[derive(Debug, Deserialize)]
#[allow(dead_code)]
pub struct SpawnPoint {
    pub id: String,
    pub position: [i32; 2],
    #[serde(default)]
    pub facing: Option<String>,
}

#[derive(Debug, Clone, Deserialize)]
pub struct NpcSpawn {
    pub id: String,
    pub name: String,
    pub dialogue: String,
    pub position: [i32; 2],
}

#[derive(Debug, Clone, Deserialize)]
pub struct PickupSpawn {
    pub id: String,
    pub material_id: String,
    pub display_name: String,
    #[serde(default = "default_pickup_quantity")]
    pub quantity: u32,
    pub position: [i32; 2],
}

fn default_pickup_quantity() -> u32 {
    1
}

#[derive(Resource, Debug, Default)]
pub struct MapLoadState {
    pub requested: bool,
    pub loaded: bool,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tutorial_scene_hooks_define_exploration_loop() {
        let hooks_text = std::fs::read_to_string("data/maps/barrio_tutorial_01/scene_hooks.json")
            .expect("tutorial scene hooks should exist");
        let hooks: SceneHooksFile =
            serde_json::from_str(&hooks_text).expect("tutorial scene hooks should be valid");

        assert_eq!(hooks.spawn_points.first().map(|spawn| spawn.position), Some([13, 13]));
        assert_eq!(hooks.npcs.first().map(|npc| npc.id.as_str()), Some("pedro_vecino"));
        assert_eq!(hooks.pickups.len(), 3);
        assert!(hooks
            .pickups
            .iter()
            .all(|pickup| pickup.position != hooks.spawn_points[0].position));
    }
}
