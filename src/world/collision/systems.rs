use std::path::PathBuf;

use bevy::prelude::*;
use bevy::render::render_resource::{Extent3d, TextureDimension, TextureFormat};
use bevy::window::PrimaryWindow;
use tracing::{info, warn};

use crate::render::camera::components::IsoCamera;
use crate::render::isometric::{grid_to_world, tile_display_size, world_to_grid_f};
use crate::ui::UiFont;
use crate::world::collision::resources::{
    CollisionBrushPreview, CollisionEditorHudRoot, CollisionEditorHudText, CollisionEditorState,
    CollisionFileData, CollisionGrid, CollisionOverlayAssets, CollisionOverlayCell,
    CollisionOverlayRoot, CollisionZoneRect, PropFootprints, PropFootprintsFile,
};
use crate::world::map::resources::{LoadedNeighborhood, PropInstance};

fn collision_path(barrio_id: &str) -> PathBuf {
    PathBuf::from("data/maps").join(barrio_id).join("collision.json")
}

fn footprints_path() -> PathBuf {
    PathBuf::from("data/collision/prop_footprints.json")
}

fn prop_blocks_default(prop_id: &str) -> bool {
    prop_id.starts_with("house_")
        || prop_id == "tree_01"
        || prop_id == "lamp_01"
        || prop_id == "fountain_01"
}

fn default_offsets(prop_id: &str) -> Vec<[i32; 2]> {
    if prop_id.starts_with("house_") {
        vec![[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]]
    } else if prop_id == "fountain_01" {
        vec![[0, 0], [1, 0], [0, 1], [1, 1]]
    } else if prop_id == "tree_01" || prop_id == "lamp_01" {
        vec![[0, 0]]
    } else {
        Vec::new()
    }
}

fn resolve_offsets(templates: &PropFootprints, prop_id: &str) -> Vec<[i32; 2]> {
    if let Some(offsets) = templates.offsets_for(prop_id) {
        if !offsets.is_empty() {
            return offsets.clone();
        }
    }
    if prop_blocks_default(prop_id) {
        default_offsets(prop_id)
    } else {
        Vec::new()
    }
}

fn anchor_cell(prop: &PropInstance) -> (i32, i32) {
    (prop.col.floor() as i32, prop.row.floor() as i32)
}

fn capture_max_radius(prop_id: &str) -> i32 {
    if prop_id.starts_with("house_") || prop_id == "fountain_01" {
        1
    } else {
        0
    }
}

fn mark_offsets(
    blocked: &mut [Vec<bool>],
    width: usize,
    height: usize,
    anchor_col: i32,
    anchor_row: i32,
    offsets: &[[i32; 2]],
) {
    for offset in offsets {
        let col = anchor_col + offset[0];
        let row = anchor_row + offset[1];
        if col >= 0 && row >= 0 && (col as usize) < width && (row as usize) < height {
            blocked[row as usize][col as usize] = true;
        }
    }
}

fn nearest_prop(neighborhood: &LoadedNeighborhood, col: i32, row: i32) -> Option<&PropInstance> {
    neighborhood
        .props
        .iter()
        .min_by(|left, right| {
            let left_dist = (left.col - col as f32).hypot(left.row - row as f32);
            let right_dist = (right.col - col as f32).hypot(right.row - row as f32);
            left_dist.partial_cmp(&right_dist).unwrap_or(std::cmp::Ordering::Equal)
        })
        .filter(|prop| {
            let dist = (prop.col - col as f32).hypot(prop.row - row as f32);
            dist <= 2.5
        })
}

fn capture_footprint_around(grid: &CollisionGrid, prop: &PropInstance) -> Vec<[i32; 2]> {
    let (anchor_col, anchor_row) = anchor_cell(prop);
    let max_r = capture_max_radius(&prop.prop_id);
    let mut offsets = Vec::new();

    for d_row in -max_r..=max_r {
        for d_col in -max_r..=max_r {
            let col = anchor_col + d_col;
            let row = anchor_row + d_row;
            if col < 0 || row < 0 || col >= grid.width as i32 || row >= grid.height as i32 {
                continue;
            }
            if grid.blocked[row as usize][col as usize] {
                offsets.push([d_col, d_row]);
            }
        }
    }

    if offsets.is_empty() {
        offsets.push([0, 0]);
    }
    offsets.sort_by_key(|offset| (offset[1], offset[0]));
    offsets
}

fn load_manual_cells(barrio_id: &str) -> Option<(Vec<[i32; 2]>, Vec<CollisionZoneRect>)> {
    let path = collision_path(barrio_id);
    let text = std::fs::read_to_string(&path).ok()?;
    let file: CollisionFileData = serde_json::from_str(&text).ok()?;
    if file.cells.is_empty() && file.zones.is_empty() {
        None
    } else {
        Some((file.cells, file.zones))
    }
}

fn apply_cells(blocked: &mut [Vec<bool>], width: usize, height: usize, cells: &[[i32; 2]]) {
    for cell in cells {
        let col = cell[0];
        let row = cell[1];
        if col >= 0 && row >= 0 && (col as usize) < width && (row as usize) < height {
            blocked[row as usize][col as usize] = true;
        }
    }
}

fn bake_from_templates(
    neighborhood: &LoadedNeighborhood,
    templates: &PropFootprints,
) -> Vec<Vec<bool>> {
    let width = neighborhood.width;
    let height = neighborhood.height;
    let mut blocked = vec![vec![false; width]; height];

    for prop in &neighborhood.props {
        let offsets = resolve_offsets(templates, &prop.prop_id);
        if offsets.is_empty() {
            continue;
        }
        let (anchor_col, anchor_row) = anchor_cell(prop);
        mark_offsets(&mut blocked, width, height, anchor_col, anchor_row, &offsets);
    }

    blocked
}

pub fn load_prop_footprints_system(mut templates: ResMut<PropFootprints>) {
    let path = footprints_path();
    if !path.exists() {
        info!("No prop_footprints.json — using built-in defaults");
        return;
    }
    match std::fs::read_to_string(&path) {
        Ok(text) => match serde_json::from_str::<PropFootprintsFile>(&text) {
            Ok(file) => {
                templates.footprints = file.footprints;
                info!(count = templates.footprints.len(), "Loaded prop collision footprints");
            }
            Err(error) => warn!(?error, "Invalid prop_footprints.json"),
        },
        Err(error) => warn!(?error, path = ?path, "Failed to read prop_footprints.json"),
    }
}

pub fn build_collision_grid_system(
    neighborhood: Res<LoadedNeighborhood>,
    templates: Res<PropFootprints>,
    mut grid: ResMut<CollisionGrid>,
) {
    if neighborhood.width == 0 || neighborhood.height == 0 {
        return;
    }

    let width = neighborhood.width;
    let height = neighborhood.height;

    let (blocked, zones, from_file) = if let Some((cells, zones)) =
        load_manual_cells(&neighborhood.barrio_id)
    {
        let mut blocked = vec![vec![false; width]; height];
        apply_cells(&mut blocked, width, height, &cells);
        (blocked, zones, true)
    } else {
        (bake_from_templates(&neighborhood, &templates), Vec::new(), false)
    };

    let blocked_cells = blocked.iter().flatten().filter(|cell| **cell).count();
    let zone_count = zones.len();

    *grid = CollisionGrid { width, height, blocked, zones, from_file, dirty: false };

    info!(width, height, blocked_cells, zone_count, from_file, "Collision grid built");
}

pub fn setup_collision_overlay_assets_system(
    mut images: ResMut<Assets<Image>>,
    mut assets: ResMut<CollisionOverlayAssets>,
) {
    if assets.marker != Handle::default() {
        return;
    }
    let image = Image::new(
        Extent3d { width: 1, height: 1, depth_or_array_layers: 1 },
        TextureDimension::D2,
        vec![255, 255, 255, 255],
        TextureFormat::Rgba8UnormSrgb,
        default(),
    );
    assets.marker = images.add(image);
}

pub fn spawn_collision_editor_hud_system(mut commands: Commands, ui_font: Res<UiFont>) {
    commands
        .spawn((
            CollisionEditorHudRoot,
            Node {
                position_type: PositionType::Absolute,
                bottom: Val::Px(8.0),
                left: Val::Px(8.0),
                padding: UiRect::all(Val::Px(8.0)),
                display: Display::None,
                ..default()
            },
            BackgroundColor(Color::srgba(0.05, 0.05, 0.08, 0.85)),
        ))
        .with_children(|parent| {
            parent.spawn((
                CollisionEditorHudText,
                Text::new("Collision Editor"),
                ui_font.sized(14.0),
                TextColor(Color::srgb(1.0, 0.85, 0.4)),
            ));
        });
}

pub fn toggle_collision_editor_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    neighborhood: Res<LoadedNeighborhood>,
    mut editor: ResMut<CollisionEditorState>,
    mut hud: Query<&mut Node, With<CollisionEditorHudRoot>>,
    mut cameras: Query<&mut Transform, With<IsoCamera>>,
) {
    if !keyboard.just_pressed(KeyCode::F2) {
        return;
    }
    editor.active = !editor.active;
    editor.drag_pan_active = false;
    editor.last_cursor = None;
    editor.status = if editor.active {
        "WASD/MMB pan | [ ] brush | C clear | R bake | T remember".into()
    } else {
        String::new()
    };

    if editor.active && neighborhood.width > 0 {
        let center_col = neighborhood.width as f32 / 2.0 - 0.5;
        let center_row = neighborhood.height as f32 / 2.0 - 0.5;
        let center = grid_to_world(center_col as i32, center_row as i32);
        for mut transform in &mut cameras {
            transform.translation.x = center.x;
            transform.translation.y = center.y;
        }
    }

    for mut node in &mut hud {
        node.display = if editor.active { Display::Flex } else { Display::None };
    }
}

pub fn editor_camera_drag_system(
    mut editor: ResMut<CollisionEditorState>,
    mouse: Res<ButtonInput<MouseButton>>,
    windows: Query<&Window, With<PrimaryWindow>>,
    mut cameras: Query<(&mut Transform, &OrthographicProjection), With<IsoCamera>>,
) {
    if !editor.active {
        return;
    }

    let Ok(window) = windows.get_single() else {
        return;
    };
    let cursor = window.cursor_position();

    if mouse.just_pressed(MouseButton::Middle) {
        editor.drag_pan_active = true;
        editor.last_cursor = cursor;
    }
    if mouse.just_released(MouseButton::Middle) {
        editor.drag_pan_active = false;
        editor.last_cursor = None;
    }

    if !editor.drag_pan_active {
        return;
    }

    let Some(current) = cursor else {
        return;
    };
    let Some(last) = editor.last_cursor else {
        editor.last_cursor = Some(current);
        return;
    };

    let delta = current - last;
    editor.last_cursor = Some(current);

    let Ok((mut transform, projection)) = cameras.get_single_mut() else {
        return;
    };
    let scale = projection.scale;
    transform.translation.x += delta.x * scale;
    transform.translation.y -= delta.y * scale;
}

pub fn sync_collision_overlay_system(
    mut commands: Commands,
    editor: Res<CollisionEditorState>,
    grid: Res<CollisionGrid>,
    assets: Res<CollisionOverlayAssets>,
    roots: Query<Entity, With<CollisionOverlayRoot>>,
) {
    if !editor.active {
        for entity in &roots {
            commands.entity(entity).despawn_recursive();
        }
        return;
    }

    if assets.marker == Handle::default() {
        return;
    }

    if !(grid.is_changed() || editor.is_changed() || roots.is_empty()) {
        return;
    }

    for entity in &roots {
        commands.entity(entity).despawn_recursive();
    }

    let root = commands
        .spawn((
            CollisionOverlayRoot,
            Name::new("CollisionOverlay"),
            Transform::default(),
            Visibility::default(),
        ))
        .id();

    let size = tile_display_size() * 0.92;
    for row in 0..grid.height {
        for col in 0..grid.width {
            if !grid.blocked[row][col] {
                continue;
            }
            let world = grid_to_world(col as i32, row as i32);
            commands.entity(root).with_children(|parent| {
                parent.spawn((
                    CollisionOverlayCell { col: col as i32, row: row as i32 },
                    Sprite {
                        image: assets.marker.clone(),
                        custom_size: Some(size),
                        color: Color::srgba(1.0, 0.15, 0.1, 0.45),
                        ..default()
                    },
                    Transform::from_xyz(world.x, world.y, 900.0),
                ));
            });
        }
    }
}

pub fn paint_collision_system(
    mut editor: ResMut<CollisionEditorState>,
    mut grid: ResMut<CollisionGrid>,
    mouse: Res<ButtonInput<MouseButton>>,
    neighborhood: Res<LoadedNeighborhood>,
    windows: Query<&Window, With<PrimaryWindow>>,
    camera: Query<(&Camera, &GlobalTransform), With<IsoCamera>>,
) {
    if !editor.active {
        return;
    }

    let Ok(window) = windows.get_single() else {
        return;
    };
    let Some(cursor) = window.cursor_position() else {
        return;
    };
    let Ok((camera, camera_transform)) = camera.get_single() else {
        return;
    };
    let Ok(world) = camera.viewport_to_world_2d(camera_transform, cursor) else {
        return;
    };

    let (col_f, row_f) = world_to_grid_f(world);
    let col = col_f.floor() as i32;
    let row = row_f.floor() as i32;
    editor.hover_col = col;
    editor.hover_row = row;
    editor.hover_prop_id = nearest_prop(&neighborhood, col, row).map(|prop| prop.prop_id.clone());

    let paint = mouse.pressed(MouseButton::Left);
    let erase = mouse.pressed(MouseButton::Right);
    if (paint || erase) && !editor.drag_pan_active {
        grid.paint_brush(col, row, editor.brush_radius, paint);
    }
}

pub fn sync_brush_preview_system(
    mut commands: Commands,
    editor: Res<CollisionEditorState>,
    assets: Res<CollisionOverlayAssets>,
    previews: Query<Entity, With<CollisionBrushPreview>>,
) {
    for entity in &previews {
        commands.entity(entity).despawn_recursive();
    }

    if !editor.active || assets.marker == Handle::default() {
        return;
    }

    let size = tile_display_size() * 0.92;
    let brush = editor.brush_radius;
    for d_row in -brush..=brush {
        for d_col in -brush..=brush {
            let col = editor.hover_col + d_col;
            let row = editor.hover_row + d_row;
            let world = grid_to_world(col, row);
            commands.spawn((
                CollisionBrushPreview,
                Sprite {
                    image: assets.marker.clone(),
                    custom_size: Some(size),
                    color: Color::srgba(1.0, 0.9, 0.2, 0.35),
                    ..default()
                },
                Transform::from_xyz(world.x, world.y, 950.0),
            ));
        }
    }
}

pub fn collision_editor_hotkeys_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    neighborhood: Res<LoadedNeighborhood>,
    mut editor: ResMut<CollisionEditorState>,
    mut grid: ResMut<CollisionGrid>,
    mut templates: ResMut<PropFootprints>,
    mut cameras: Query<&mut Transform, With<IsoCamera>>,
) {
    if !editor.active {
        return;
    }

    let ctrl = keyboard.pressed(KeyCode::ControlLeft) || keyboard.pressed(KeyCode::ControlRight);

    if keyboard.just_pressed(KeyCode::BracketLeft) {
        editor.brush_radius = (editor.brush_radius - 1).max(0);
        editor.status = format!(
            "Brush size: {} ({}x{} cells)",
            editor.brush_radius,
            editor.brush_radius * 2 + 1,
            editor.brush_radius * 2 + 1
        );
    }
    if keyboard.just_pressed(KeyCode::BracketRight) {
        editor.brush_radius = (editor.brush_radius + 1).min(3);
        editor.status = format!(
            "Brush size: {} ({}x{} cells)",
            editor.brush_radius,
            editor.brush_radius * 2 + 1,
            editor.brush_radius * 2 + 1
        );
    }

    if keyboard.just_pressed(KeyCode::KeyC) && !ctrl {
        grid.clear_all();
        editor.status = "Grid cleared. R to bake from templates.".into();
    }

    // G — center camera on map.
    if keyboard.just_pressed(KeyCode::KeyG) && !ctrl {
        let center_col = neighborhood.width as f32 / 2.0 - 0.5;
        let center_row = neighborhood.height as f32 / 2.0 - 0.5;
        let center = grid_to_world(center_col as i32, center_row as i32);
        for mut transform in &mut cameras {
            transform.translation.x = center.x;
            transform.translation.y = center.y;
        }
        editor.status = "Camera centered on map".into();
    }

    // R — rebuild map collisions from remembered prop footprints.
    if keyboard.just_pressed(KeyCode::KeyR) && !ctrl {
        grid.blocked = bake_from_templates(&neighborhood, &templates);
        grid.from_file = false;
        grid.dirty = true;
        editor.status = format!(
            "Baked from prop templates ({} cells). Ctrl+S to save map.",
            grid.blocked_count()
        );
    }

    // T — capture current painting around nearest prop as that prop's template.
    if keyboard.just_pressed(KeyCode::KeyT) && !ctrl {
        if let Some(prop_id) = editor.hover_prop_id.clone() {
            if let Some(prop) = neighborhood.props.iter().find(|prop| prop.prop_id == prop_id) {
                // Prefer the nearest instance to the cursor as the capture anchor.
                let nearest =
                    nearest_prop(&neighborhood, editor.hover_col, editor.hover_row).unwrap_or(prop);
                let offsets = capture_footprint_around(&grid, nearest);
                let count = offsets.len();
                templates.set_offsets(nearest.prop_id.clone(), offsets);
                editor.status = format!(
                    "Remembered {} cells for '{}'. Press R to bake all instances, Ctrl+Shift+S to save templates.",
                    count, nearest.prop_id
                );
            }
        } else {
            editor.status =
                "Hover a prop cell, paint its blocked tiles, then press T to remember.".into();
        }
    }

    // Ctrl+S — save this map's collision.json.
    if ctrl
        && keyboard.just_pressed(KeyCode::KeyS)
        && !keyboard.pressed(KeyCode::ShiftLeft)
        && !keyboard.pressed(KeyCode::ShiftRight)
    {
        match save_collision_file(&neighborhood.barrio_id, &grid) {
            Ok(count) => {
                grid.dirty = false;
                grid.from_file = true;
                editor.status = format!("Saved {count} blocked cells to collision.json");
                info!(count, "Collision grid saved");
            }
            Err(error) => {
                editor.status = format!("Save failed: {error}");
                warn!(?error, "Failed to save collision.json");
            }
        }
    }

    // Ctrl+Shift+S — save remembered prop footprints globally.
    if ctrl
        && (keyboard.pressed(KeyCode::ShiftLeft) || keyboard.pressed(KeyCode::ShiftRight))
        && keyboard.just_pressed(KeyCode::KeyS)
    {
        match save_prop_footprints(&templates) {
            Ok(count) => {
                editor.status = format!("Saved {count} prop footprints to prop_footprints.json");
                info!(count, "Prop footprints saved");
            }
            Err(error) => {
                editor.status = format!("Template save failed: {error}");
                warn!(?error, "Failed to save prop_footprints.json");
            }
        }
    }
}

pub fn update_collision_editor_hud_system(
    editor: Res<CollisionEditorState>,
    grid: Res<CollisionGrid>,
    templates: Res<PropFootprints>,
    mut text_query: Query<&mut Text, With<CollisionEditorHudText>>,
) {
    if !editor.active {
        return;
    }

    let dirty = if grid.dirty { " *" } else { "" };
    let source = if grid.from_file { "file" } else { "templates" };
    let hover = editor.hover_prop_id.as_deref().unwrap_or("(no prop under cursor)");
    let remembered = templates.footprints.len();
    let brush_cells = editor.brush_radius * 2 + 1;
    let message = format!(
        "Collision Editor [F2]{dirty}\n\
Blocked: {} ({source}) | Templates: {remembered} | Brush: {brush_cells}x{brush_cells}\n\
Hover: {hover} @ ({}, {})\n\
LMB paint | RMB erase | [ ] brush | C clear\n\
WASD/MMB drag pan | G center | R bake | T remember\n\
Ctrl+S map | Ctrl+Shift+S templates\n\
{}",
        grid.blocked_count(),
        editor.hover_col,
        editor.hover_row,
        editor.status
    );
    for mut text in &mut text_query {
        text.0 = message.clone();
    }
}

fn save_collision_file(barrio_id: &str, grid: &CollisionGrid) -> Result<usize, String> {
    let path = collision_path(barrio_id);
    if let Some(parent) = path.parent() {
        std::fs::create_dir_all(parent).map_err(|error| error.to_string())?;
    }
    let cells = grid.to_cells();
    let count = cells.len();
    let payload = CollisionFileData {
        barrio_id: barrio_id.to_owned(),
        version: 1,
        cells,
        zones: grid.zones.clone(),
    };
    let json = serde_json::to_string_pretty(&payload).map_err(|error| error.to_string())?;
    std::fs::write(&path, json + "\n").map_err(|error| error.to_string())?;
    Ok(count)
}

fn save_prop_footprints(templates: &PropFootprints) -> Result<usize, String> {
    let path = footprints_path();
    if let Some(parent) = path.parent() {
        std::fs::create_dir_all(parent).map_err(|error| error.to_string())?;
    }
    let count = templates.footprints.len();
    let payload = PropFootprintsFile { version: 1, footprints: templates.footprints.clone() };
    let json = serde_json::to_string_pretty(&payload).map_err(|error| error.to_string())?;
    std::fs::write(&path, json + "\n").map_err(|error| error.to_string())?;
    Ok(count)
}
