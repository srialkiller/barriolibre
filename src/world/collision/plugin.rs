use bevy::prelude::*;

use crate::core::states::GameState;
use crate::world::collision::resources::{
    CollisionEditorState, CollisionGrid, CollisionOverlayAssets, PropFootprints,
};
use crate::world::collision::systems::{
    build_collision_grid_system, collision_editor_hotkeys_system, editor_camera_drag_system,
    load_prop_footprints_system, paint_collision_system, setup_collision_overlay_assets_system,
    spawn_collision_editor_hud_system, sync_brush_preview_system, sync_collision_overlay_system,
    toggle_collision_editor_system, update_collision_editor_hud_system,
};

pub struct CollisionPlugin;

impl Plugin for CollisionPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<CollisionGrid>()
            .init_resource::<CollisionEditorState>()
            .init_resource::<CollisionOverlayAssets>()
            .init_resource::<PropFootprints>()
            .add_systems(
                Startup,
                (
                    load_prop_footprints_system,
                    setup_collision_overlay_assets_system,
                    spawn_collision_editor_hud_system,
                ),
            )
            .add_systems(OnEnter(GameState::Gameplay), build_collision_grid_system)
            .add_systems(
                Update,
                (
                    toggle_collision_editor_system,
                    editor_camera_drag_system,
                    paint_collision_system,
                    collision_editor_hotkeys_system,
                    sync_collision_overlay_system,
                    sync_brush_preview_system,
                    update_collision_editor_hud_system,
                )
                    .chain()
                    .run_if(in_state(GameState::Gameplay)),
            );
    }
}
