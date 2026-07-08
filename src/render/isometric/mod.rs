//! Isometric 2:1 math — ASSET_PIPELINE §10.5 + manifest tile specs.

use bevy::prelude::*;
use bevy::sprite::Anchor;

/// Pixel size of environment tiles (`size_pixels` in `.meta.json`).
pub const TILE_PX_WIDTH: f32 = 256.0;
pub const TILE_PX_HEIGHT: f32 = 128.0;

/// World footprint (`size_units` in `.meta.json`).
pub const TILE_WORLD_WIDTH: f32 = 1.0;
pub const TILE_WORLD_HEIGHT: f32 = 0.5;

/// Pixels per world unit (256 px / 1.0 u).
pub const PIXELS_PER_UNIT: f32 = TILE_PX_WIDTH / TILE_WORLD_WIDTH;

/// Grid snap pivot for floor tiles (center of diamond).
pub const TILE_PIVOT: Vec2 = Vec2::new(0.5, 0.5);

/// Converts grid indices to world position (Bevy 2D, Y-up).
pub fn grid_to_world(grid_x: i32, grid_y: i32) -> Vec2 {
    let world_x =
        (grid_x - grid_y) as f32 * TILE_WORLD_WIDTH * 0.5 * PIXELS_PER_UNIT;
    let world_y =
        -((grid_x + grid_y) as f32 * TILE_WORLD_HEIGHT * 0.5 * PIXELS_PER_UNIT);
    Vec2::new(world_x, world_y)
}

/// Converts fractional grid coordinates to world position (Bevy 2D, Y-up).
///
/// Used for props, which can sit on non-integer cells (e.g. a fountain
/// centred between four tiles).
pub fn grid_to_world_f(col: f32, row: f32) -> Vec2 {
    let world_x = (col - row) * TILE_WORLD_WIDTH * 0.5 * PIXELS_PER_UNIT;
    let world_y = -((col + row) * TILE_WORLD_HEIGHT * 0.5 * PIXELS_PER_UNIT);
    Vec2::new(world_x, world_y)
}

/// Inverse of [`grid_to_world_f`] — world feet position to fractional grid coords.
pub fn world_to_grid_f(world: Vec2) -> (f32, f32) {
    let half_width = TILE_WORLD_WIDTH * 0.5 * PIXELS_PER_UNIT;
    let half_height = TILE_WORLD_HEIGHT * 0.5 * PIXELS_PER_UNIT;
    let col = (world.x / half_width - world.y / half_height) * 0.5;
    let row = (-world.y / half_height - world.x / half_width) * 0.5;
    (col, row)
}

/// Depth sort key for pseudo-3D draw order.
pub fn iso_sort_key(grid_x: i32, grid_y: i32) -> f32 {
    (grid_x + grid_y) as f32
}

/// Display size for loaded tile sprites (native pixel dimensions).
pub fn tile_display_size() -> Vec2 {
    Vec2::new(
        TILE_WORLD_WIDTH * PIXELS_PER_UNIT,
        TILE_WORLD_HEIGHT * PIXELS_PER_UNIT,
    )
}

/// Anchor from ASSET_PIPELINE pivot.
///
/// Pivot is in image space (top-left origin, Y-down, range `[0, 1]`).
/// Bevy `Anchor::Custom` is an offset from the sprite center in range
/// `[-0.5, 0.5]` with Y-up, so a `(0.5, 0.5)` pivot must map to the
/// center `(0.0, 0.0)`.
pub fn tile_anchor_from_pivot(pivot_x: f32, pivot_y: f32) -> Anchor {
    Anchor::Custom(Vec2::new(pivot_x - 0.5, 0.5 - pivot_y))
}

pub fn default_tile_anchor() -> Anchor {
    tile_anchor_from_pivot(TILE_PIVOT.x, TILE_PIVOT.y)
}

/// Alpha bounding box of a tile's visible content, in image pixels.
///
/// Returns `(min, max)` where `min` is the top-left and `max` is the
/// bottom-right (exclusive) of the opaque region. `None` when the image
/// is empty, fully transparent, or not RGBA8.
pub fn content_bounds(image: &Image, alpha_threshold: u8) -> Option<(Vec2, Vec2)> {
    let size = image.size();
    let width = size.x as usize;
    let height = size.y as usize;
    if width == 0 || height == 0 {
        return None;
    }

    let data = &image.data;
    let bytes_per_pixel = data.len() / (width * height);
    if bytes_per_pixel < 4 {
        return None;
    }

    let mut min_x = width;
    let mut min_y = height;
    let mut max_x = 0usize;
    let mut max_y = 0usize;
    let mut found_opaque = false;

    for pixel_y in 0..height {
        for pixel_x in 0..width {
            let alpha = data[(pixel_y * width + pixel_x) * bytes_per_pixel + 3];
            if alpha > alpha_threshold {
                found_opaque = true;
                min_x = min_x.min(pixel_x);
                min_y = min_y.min(pixel_y);
                max_x = max_x.max(pixel_x);
                max_y = max_y.max(pixel_y);
            }
        }
    }

    if !found_opaque {
        return None;
    }

    Some((
        Vec2::new(min_x as f32, min_y as f32),
        Vec2::new((max_x + 1) as f32, (max_y + 1) as f32),
    ))
}

/// Fits a tile's content bounds into a full iso cell.
///
/// Returns the sprite `custom_size` (frame scaled up so the opaque
/// content covers the `256x128` cell) and the world-space offset to add
/// to the tile transform so the content center lands on the grid
/// position (Bevy Y-up; image Y is flipped).
pub fn fit_content_to_cell(min: Vec2, max: Vec2) -> (Vec2, Vec2) {
    let content = max - min;
    if content.x <= 0.0 || content.y <= 0.0 {
        return (tile_display_size(), Vec2::ZERO);
    }

    let scale =
        (TILE_PX_WIDTH / content.x).max(TILE_PX_HEIGHT / content.y);
    let custom_size = Vec2::new(TILE_PX_WIDTH * scale, TILE_PX_HEIGHT * scale);

    let content_center = (min + max) * 0.5;
    let frame_center = Vec2::new(TILE_PX_WIDTH * 0.5, TILE_PX_HEIGHT * 0.5);
    let world_offset = Vec2::new(
        -(content_center.x - frame_center.x) * scale,
        (content_center.y - frame_center.y) * scale,
    );

    (custom_size, world_offset)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn origin_tile_at_zero() {
        assert_eq!(grid_to_world(0, 0), Vec2::ZERO);
    }

    #[test]
    fn neighbor_spacing_matches_tile_size() {
        assert_eq!(grid_to_world(1, 0).x, TILE_PX_WIDTH * 0.5);
        assert_eq!(grid_to_world(0, 1).x, -TILE_PX_WIDTH * 0.5);
        assert_eq!(grid_to_world(0, 1).y, -TILE_PX_HEIGHT * 0.5);
    }

    #[test]
    fn world_grid_roundtrip() {
        let world = grid_to_world_f(12.5, 11.25);
        let (col, row) = world_to_grid_f(world);
        assert!((col - 12.5).abs() < 0.01);
        assert!((row - 11.25).abs() < 0.01);
    }
}
