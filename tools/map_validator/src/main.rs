//! Validates `data/maps/<barrio>/` JSON against manifests and asset files.
//!
//! Usage:
//!   cargo run -p map_validator -- data/maps/barrio_tutorial_01

use std::collections::HashSet;
use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::process;

use serde::Deserialize;

const DEFAULT_MANIFEST: &str = "data/tilesets/environment_base_pack_01_generated.json";

fn main() {
    let map_dir = env::args()
        .nth(1)
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from("data/maps/barrio_tutorial_01"));

    let manifest_path =
        env::args().nth(2).map(PathBuf::from).unwrap_or_else(|| PathBuf::from(DEFAULT_MANIFEST));

    match validate_map(&map_dir, &manifest_path) {
        Ok(summary) => {
            println!("OK: {}", summary);
        }
        Err(errors) => {
            eprintln!("map_validator: {} error(s) in {}", errors.len(), map_dir.display());
            for error in &errors {
                eprintln!("  - {error}");
            }
            process::exit(1);
        }
    }
}

fn validate_map(map_dir: &Path, manifest_path: &Path) -> Result<String, Vec<String>> {
    let mut errors = Vec::new();

    let layout_path = map_dir.join("layout.json");
    let layout_text = read_file(&layout_path, &mut errors);
    let layout: Option<LayoutFile> =
        layout_text.as_ref().and_then(|text| parse_json(text, &layout_path, &mut errors).ok());

    let known_tiles = load_tile_manifest(manifest_path, &mut errors);

    if let Some(layout) = &layout {
        validate_layout_dimensions(layout, &mut errors);
        validate_tile_ids(layout, &known_tiles, &mut errors);
    }

    let barrio_id = layout.as_ref().map(|file| file.barrio_id.as_str());

    let hooks_path = map_dir.join("scene_hooks.json");
    if hooks_path.exists() {
        if let Ok(text) = fs::read_to_string(&hooks_path) {
            if let Ok(hooks) = parse_json::<SceneHooksFile>(&text, &hooks_path, &mut errors) {
                validate_scene_hooks(&hooks, barrio_id, layout.as_ref(), &mut errors);
            }
        }
    }

    let collision_path = map_dir.join("collision.json");
    if collision_path.exists() {
        if let Ok(text) = fs::read_to_string(&collision_path) {
            if let Ok(collision) = parse_json::<CollisionFile>(&text, &collision_path, &mut errors)
            {
                validate_collision(&collision, barrio_id, layout.as_ref(), &mut errors);
            }
        }
    }

    let props_path = map_dir.join("props.json");
    if props_path.exists() {
        if let Ok(text) = fs::read_to_string(&props_path) {
            if let Ok(props_file) = parse_json::<PropsFile>(&text, &props_path, &mut errors) {
                validate_props(&props_file, barrio_id, layout.as_ref(), &mut errors);
            }
        }
    }

    if errors.is_empty() {
        let width = layout.as_ref().map(|file| file.size[0]).unwrap_or(0);
        let height = layout.as_ref().map(|file| file.size[1]).unwrap_or(0);
        Ok(format!(
            "{} ({width}x{height}) — layout, hooks, collision, props validated",
            map_dir.display()
        ))
    } else {
        Err(errors)
    }
}

fn read_file(path: &Path, errors: &mut Vec<String>) -> Option<String> {
    match fs::read_to_string(path) {
        Ok(text) => Some(text),
        Err(error) => {
            errors.push(format!("missing or unreadable {}: {error}", path.display()));
            None
        }
    }
}

fn parse_json<T: for<'de> Deserialize<'de>>(
    text: &str,
    path: &Path,
    errors: &mut Vec<String>,
) -> Result<T, ()> {
    serde_json::from_str(text).map_err(|error| {
        errors.push(format!("invalid JSON in {}: {error}", path.display()));
    })
}

fn load_tile_manifest(manifest_path: &Path, errors: &mut Vec<String>) -> HashSet<String> {
    let text = match fs::read_to_string(manifest_path) {
        Ok(text) => text,
        Err(error) => {
            errors.push(format!(
                "missing or unreadable manifest {}: {error}",
                manifest_path.display()
            ));
            return HashSet::new();
        }
    };

    match serde_json::from_str::<GeneratedManifest>(&text) {
        Ok(manifest) => manifest.generated.into_iter().collect(),
        Err(error) => {
            errors.push(format!("invalid manifest JSON in {}: {error}", manifest_path.display()));
            HashSet::new()
        }
    }
}

fn validate_layout_dimensions(layout: &LayoutFile, errors: &mut Vec<String>) {
    let [width, height] = layout.size;
    let ground_height = layout.layers.ground.len();
    if ground_height != height {
        errors.push(format!("layout size height ({height}) != ground rows ({ground_height})"));
    }

    for (row_index, row) in layout.layers.ground.iter().enumerate() {
        if row.len() != width {
            errors.push(format!(
                "ground row {row_index} has {} columns, expected {width}",
                row.len()
            ));
        }
    }
}

fn validate_tile_ids(layout: &LayoutFile, known_tiles: &HashSet<String>, errors: &mut Vec<String>) {
    if known_tiles.is_empty() {
        return;
    }

    let mut missing = HashSet::new();
    for row in &layout.layers.ground {
        for tile_id in row {
            if !known_tiles.contains(tile_id) && !tile_png_exists(tile_id) {
                missing.insert(tile_id.clone());
            }
        }
    }

    for tile_id in missing {
        errors.push(format!("unknown tile id '{tile_id}' (not in manifest and no PNG)"));
    }
}

fn validate_scene_hooks(
    hooks: &SceneHooksFile,
    barrio_id: Option<&str>,
    layout: Option<&LayoutFile>,
    errors: &mut Vec<String>,
) {
    if let Some(expected) = barrio_id {
        if hooks.barrio_id != expected {
            errors.push(format!(
                "scene_hooks barrio_id '{}' != layout '{}'",
                hooks.barrio_id, expected
            ));
        }
    }

    if hooks.spawn_points.is_empty() {
        errors.push("scene_hooks has no spawn_points".to_string());
    }

    if let Some(layout) = layout {
        let [width, height] = layout.size;
        for spawn in &hooks.spawn_points {
            if spawn.id.is_empty() {
                errors.push("spawn_point with empty id".to_string());
            }
            let [col, row] = spawn.position;
            if col < 0 || row < 0 || col as usize >= width || row as usize >= height {
                errors.push(format!(
                    "spawn '{}' position [{col},{row}] outside map {width}x{height}",
                    spawn.id
                ));
            }
        }
    }
}

fn validate_collision(
    collision: &CollisionFile,
    barrio_id: Option<&str>,
    layout: Option<&LayoutFile>,
    errors: &mut Vec<String>,
) {
    if let Some(expected) = barrio_id {
        if collision.barrio_id != expected {
            errors.push(format!(
                "collision barrio_id '{}' != layout '{}'",
                collision.barrio_id, expected
            ));
        }
    }

    if let Some(layout) = layout {
        let [width, height] = layout.size;
        for [col, row] in &collision.cells {
            if *col < 0 || *row < 0 || *col as usize >= width || *row as usize >= height {
                errors.push(format!("collision cell [{col},{row}] outside map {width}x{height}"));
            }
        }
    }
}

fn validate_props(
    props_file: &PropsFile,
    barrio_id: Option<&str>,
    layout: Option<&LayoutFile>,
    errors: &mut Vec<String>,
) {
    if let Some(expected) = barrio_id {
        if props_file.barrio_id != expected {
            errors.push(format!(
                "props barrio_id '{}' != layout '{}'",
                props_file.barrio_id, expected
            ));
        }
    }

    if let Some(layout) = layout {
        let [width, height] = layout.size;
        for prop in &props_file.props {
            if prop.prop_id.is_empty() {
                errors.push("prop with empty prop_id".to_string());
                continue;
            }
            if !prop_png_exists(&prop.prop_id) {
                errors.push(format!("missing prop PNG for '{}'", prop.prop_id));
            }
            if prop.col < 0.0
                || prop.row < 0.0
                || prop.col as usize >= width
                || prop.row as usize >= height
            {
                errors.push(format!(
                    "prop '{}' at ({},{}) outside map {width}x{height}",
                    prop.prop_id, prop.col, prop.row
                ));
            }
        }
    }
}

fn tile_png_exists(tile_id: &str) -> bool {
    let category = if tile_id.starts_with("road_") {
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
    };
    Path::new("assets").join(format!("environment/{category}/{tile_id}.png")).exists()
}

fn prop_png_exists(prop_id: &str) -> bool {
    Path::new("assets").join(format!("environment/props/{prop_id}.png")).exists()
}

#[derive(Debug, Deserialize)]
struct GeneratedManifest {
    generated: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct LayoutFile {
    barrio_id: String,
    size: [usize; 2],
    layers: LayoutLayers,
}

#[derive(Debug, Deserialize)]
struct LayoutLayers {
    ground: Vec<Vec<String>>,
}

#[derive(Debug, Deserialize)]
struct SceneHooksFile {
    barrio_id: String,
    spawn_points: Vec<SpawnPoint>,
}

#[derive(Debug, Deserialize)]
struct SpawnPoint {
    id: String,
    position: [i32; 2],
}

#[derive(Debug, Deserialize)]
struct CollisionFile {
    barrio_id: String,
    cells: Vec<[i32; 2]>,
}

#[derive(Debug, Deserialize)]
struct PropsFile {
    barrio_id: String,
    props: Vec<PropInstance>,
}

#[derive(Debug, Deserialize)]
struct PropInstance {
    prop_id: String,
    col: f32,
    row: f32,
}
