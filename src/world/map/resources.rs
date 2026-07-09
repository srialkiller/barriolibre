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
