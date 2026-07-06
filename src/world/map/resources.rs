use bevy::prelude::*;
use serde::Deserialize;

#[derive(Resource, Debug, Clone)]
pub struct LoadedNeighborhood {
    pub barrio_id: String,
    pub display_name: String,
    pub width: usize,
    pub height: usize,
    pub ground_layer: Vec<Vec<String>>,
    pub spawn_position: Option<[i32; 2]>,
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
            spawn_position: None,
            collision_loaded: false,
            hooks_loaded: false,
        }
    }
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
}

#[derive(Debug, Deserialize)]
#[allow(dead_code)]
pub struct SceneHooksFile {
    pub barrio_id: String,
    pub spawn_points: Vec<SpawnPoint>,
}

#[derive(Debug, Deserialize)]
#[allow(dead_code)]
pub struct SpawnPoint {
    pub id: String,
    pub position: [i32; 2],
}

#[derive(Resource, Debug, Default)]
pub struct MapLoadState {
    pub requested: bool,
    pub loaded: bool,
}
