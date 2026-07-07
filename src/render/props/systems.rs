use bevy::prelude::*;
use bevy::sprite::Anchor;

use crate::assets::registry::AssetRegistry;
use crate::render::isometric::grid_to_world_f;
use crate::world::map::components::{MapProp, PropRoot};
use crate::world::map::resources::LoadedNeighborhood;

/// Spawns upright props (houses, trees, plaza furniture) from `props.json`.
///
/// Each prop is anchored bottom-centre on its cell and depth-sorted by
/// `col + row` (isometric back-to-front) so nearer props occlude farther ones
/// and every prop draws above the ground tiles it stands on.
pub fn spawn_props_system(
    mut commands: Commands,
    neighborhood: Res<LoadedNeighborhood>,
    registry: Res<AssetRegistry>,
    existing: Query<Entity, With<PropRoot>>,
) {
    if !existing.is_empty() {
        return;
    }

    let root = commands
        .spawn((
            PropRoot,
            Name::new("PropRoot"),
            Transform::default(),
            Visibility::default(),
        ))
        .id();

    let mut spawned = 0_usize;
    for prop in &neighborhood.props {
        let Some(handle) = registry.prop(&prop.prop_id).cloned() else {
            tracing::warn!(prop_id = %prop.prop_id, "Prop not in AssetRegistry");
            continue;
        };

        let world = grid_to_world_f(prop.col, prop.row);
        // +0.5 lifts the prop above the ground tile on its own cell; the tiny
        // row term breaks ties within a diagonal for stable ordering.
        let depth = prop.col + prop.row + prop.row * 0.001 + 0.5;

        commands.entity(root).with_children(|parent| {
            parent.spawn((
                MapProp {
                    prop_id: prop.prop_id.clone(),
                    col: prop.col,
                    row: prop.row,
                },
                Sprite {
                    image: handle,
                    custom_size: Some(Vec2::new(prop.width_px, prop.height_px)),
                    anchor: Anchor::BottomCenter,
                    ..default()
                },
                Transform::from_xyz(world.x, world.y, depth),
            ));
        });
        spawned += 1;
    }

    tracing::info!(spawned, total = neighborhood.props.len(), "Props spawned");
}
