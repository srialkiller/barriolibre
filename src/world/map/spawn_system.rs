use bevy::prelude::*;

use crate::render::isometric::grid_to_world_f;
use crate::world::map::components::NeighborhoodNpc;
use crate::world::map::resources::LoadedNeighborhood;

pub fn spawn_neighborhood_npcs_system(
    mut commands: Commands,
    neighborhood: Res<LoadedNeighborhood>,
    existing_npcs: Query<Entity, With<NeighborhoodNpc>>,
) {
    if !existing_npcs.is_empty() {
        return;
    }

    for npc_spawn in &neighborhood.npc_spawns {
        let world_position =
            grid_to_world_f(npc_spawn.position[0] as f32, npc_spawn.position[1] as f32);
        let depth = npc_spawn.position[0] as f32 + npc_spawn.position[1] as f32 + 0.2;

        commands.spawn((
            NeighborhoodNpc {
                npc_id: npc_spawn.id.clone(),
                display_name: npc_spawn.name.clone(),
                dialogue: npc_spawn.dialogue.clone(),
            },
            Sprite {
                color: Color::srgb(0.95, 0.62, 0.22),
                custom_size: Some(Vec2::new(34.0, 68.0)),
                anchor: bevy::sprite::Anchor::BottomCenter,
                ..default()
            },
            Transform::from_xyz(world_position.x, world_position.y, depth),
            Name::new(format!("NPC: {}", npc_spawn.name)),
        ));
    }

    tracing::info!(count = neighborhood.npc_spawns.len(), "Neighborhood NPCs spawned");
}
