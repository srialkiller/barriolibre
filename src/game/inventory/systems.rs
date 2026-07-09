use bevy::prelude::*;

use crate::ui::UiFont;
use crate::game::inventory::components::{
    Collectible, InventoryUiRoot, InventoryUiText, PickupPromptRoot, PickupPromptText,
};
use crate::game::inventory::events::{ItemCollected, PickupCollected};
use crate::game::inventory::resources::{InventoryUiState, MaterialId, PlayerInventory};
use crate::game::player::components::Player;
use crate::game::player::interaction_system::NPC_INTERACTION_DISTANCE;
use crate::render::isometric::grid_to_world_f;
use crate::world::map::components::NeighborhoodNpc;
use crate::world::map::resources::LoadedNeighborhood;

const PICKUP_DISTANCE: f32 = 150.0;

pub fn spawn_collectibles_system(
    mut commands: Commands,
    neighborhood: Res<LoadedNeighborhood>,
    existing_collectibles: Query<Entity, With<Collectible>>,
) {
    if !existing_collectibles.is_empty() {
        return;
    }

    for pickup in &neighborhood.pickup_spawns {
        let world_position = grid_to_world_f(pickup.position[0] as f32, pickup.position[1] as f32);
        let depth = pickup.position[0] as f32 + pickup.position[1] as f32 + 0.15;
        let material_id = MaterialId::new(&pickup.material_id);

        commands.spawn((
            Collectible {
                spawn_id: pickup.id.clone(),
                material_id,
                display_name: pickup.display_name.clone(),
                quantity: pickup.quantity,
            },
            Sprite {
                color: pickup_color(&pickup.material_id),
                custom_size: Some(Vec2::splat(26.0)),
                ..default()
            },
            Transform::from_xyz(world_position.x, world_position.y, depth),
            Name::new(format!("Pickup: {}", pickup.display_name)),
        ));
    }

    tracing::info!(count = neighborhood.pickup_spawns.len(), "Collectibles spawned");
}

pub fn collect_nearby_pickup_system(
    mut commands: Commands,
    keyboard: Res<ButtonInput<KeyCode>>,
    player: Query<&Transform, With<Player>>,
    collectibles: Query<(Entity, &Transform, &Collectible)>,
    npcs: Query<&Transform, With<NeighborhoodNpc>>,
    mut inventory: ResMut<PlayerInventory>,
    mut collected_events: EventWriter<PickupCollected>,
    mut item_collected_events: EventWriter<ItemCollected>,
) {
    if !keyboard.just_pressed(KeyCode::KeyE) {
        return;
    }
    let Ok(player_transform) = player.get_single() else {
        return;
    };
    if has_nearby_npc(player_transform, npcs.iter()) {
        return;
    }
    let Some((entity, _, collectible)) = nearest_collectible(player_transform, collectibles.iter())
    else {
        return;
    };

    let new_total = inventory.add_material(
        collectible.material_id.clone(),
        &collectible.display_name,
        collectible.quantity,
    );
    collected_events.send(PickupCollected {
        material_id: collectible.material_id.clone(),
        display_name: collectible.display_name.clone(),
        amount: collectible.quantity,
        new_total,
    });
    item_collected_events.send(ItemCollected {
        material_id: collectible.material_id.clone(),
        display_name: collectible.display_name.clone(),
        amount: collectible.quantity,
        new_total,
    });
    tracing::info!(
        spawn_id = %collectible.spawn_id,
        material_id = %collectible.material_id,
        quantity = collectible.quantity,
        new_total,
        "Pickup collected"
    );
    commands.entity(entity).despawn_recursive();
}

fn nearest_collectible<'a>(
    player_transform: &Transform,
    collectibles: impl Iterator<Item = (Entity, &'a Transform, &'a Collectible)>,
) -> Option<(Entity, &'a Transform, &'a Collectible)> {
    collectibles
        .filter(|(_, transform, _)| {
            player_transform.translation.truncate().distance(transform.translation.truncate())
                <= PICKUP_DISTANCE
        })
        .min_by(|(_, left, _), (_, right, _)| {
            let player_position = player_transform.translation.truncate();
            player_position
                .distance(left.translation.truncate())
                .total_cmp(&player_position.distance(right.translation.truncate()))
        })
}

fn has_nearby_npc<'a>(
    player_transform: &Transform,
    npcs: impl Iterator<Item = &'a Transform>,
) -> bool {
    npcs.into_iter().any(|npc_transform| {
        player_transform.translation.truncate().distance(npc_transform.translation.truncate())
            <= NPC_INTERACTION_DISTANCE
    })
}

pub fn spawn_inventory_ui_system(mut commands: Commands, ui_font: Res<UiFont>) {
    commands
        .spawn((
            InventoryUiRoot,
            Node {
                position_type: PositionType::Absolute,
                top: Val::Px(48.0),
                right: Val::Px(24.0),
                width: Val::Px(300.0),
                min_height: Val::Px(180.0),
                padding: UiRect::all(Val::Px(16.0)),
                display: Display::None,
                ..default()
            },
            BackgroundColor(Color::srgba(0.04, 0.08, 0.1, 0.94)),
        ))
        .with_children(|parent| {
            parent.spawn((
                InventoryUiText,
                Text::new("Inventario"),
                ui_font.sized(20.0),
                TextColor(Color::srgb(0.92, 0.96, 0.82)),
            ));
        });

    commands
        .spawn((
            PickupPromptRoot,
            Node {
                position_type: PositionType::Absolute,
                bottom: Val::Px(24.0),
                left: Val::Px(24.0),
                padding: UiRect::all(Val::Px(10.0)),
                display: Display::None,
                ..default()
            },
            BackgroundColor(Color::srgba(0.04, 0.08, 0.1, 0.88)),
        ))
        .with_children(|parent| {
            parent.spawn((
                PickupPromptText,
                Text::new(""),
                ui_font.sized(17.0),
                TextColor(Color::srgb(0.8, 1.0, 0.74)),
            ));
        });
}

pub fn toggle_inventory_ui_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    mut ui_state: ResMut<InventoryUiState>,
    mut nodes: Query<&mut Node, With<InventoryUiRoot>>,
) {
    if keyboard.just_pressed(KeyCode::KeyI) {
        ui_state.visible = !ui_state.visible;
        for mut node in &mut nodes {
            node.display = if ui_state.visible { Display::Flex } else { Display::None };
        }
    }
}

pub fn sync_inventory_ui_system(
    ui_state: Res<InventoryUiState>,
    inventory: Res<PlayerInventory>,
    mut texts: Query<&mut Text, With<InventoryUiText>>,
) {
    if !ui_state.visible || (!inventory.is_changed() && !ui_state.is_changed()) {
        return;
    }

    let contents = if inventory.is_empty() {
        "Inventario\n\nVacío\n\n[I] Cerrar".to_string()
    } else {
        let lines = inventory
            .sorted_materials()
            .into_iter()
            .map(|(_, name, quantity)| format!("• {name} ×{quantity}"))
            .collect::<Vec<_>>()
            .join("\n");
        format!("Inventario — Materiales\n\n{lines}\n\n[I] Cerrar")
    };
    for mut text in &mut texts {
        text.0.clone_from(&contents);
    }
}

pub fn update_pickup_prompt_system(
    player: Query<&Transform, With<Player>>,
    collectibles: Query<(Entity, &Transform, &Collectible)>,
    npcs: Query<&Transform, With<NeighborhoodNpc>>,
    mut nodes: Query<&mut Node, With<PickupPromptRoot>>,
    mut texts: Query<&mut Text, With<PickupPromptText>>,
) {
    let nearest = player.get_single().ok().and_then(|player_transform| {
        (!has_nearby_npc(player_transform, npcs.iter()))
            .then(|| nearest_collectible(player_transform, collectibles.iter()))
            .flatten()
    });
    let message = nearest.map(|(_, _, collectible)| {
        format!("[E] Recoger {} ×{}", collectible.display_name, collectible.quantity)
    });

    for mut node in &mut nodes {
        node.display = if message.is_some() { Display::Flex } else { Display::None };
    }
    if let Some(message) = message {
        for mut text in &mut texts {
            text.0.clone_from(&message);
        }
    }
}

pub fn log_pickup_feedback_system(mut collected_events: EventReader<PickupCollected>) {
    for event in collected_events.read() {
        tracing::info!(
            material_id = %event.material_id,
            amount = event.amount,
            new_total = event.new_total,
            display_name = %event.display_name,
            "Inventory updated"
        );
    }
}

fn pickup_color(material_id: &str) -> Color {
    match material_id {
        "cardboard" => Color::srgb(0.72, 0.48, 0.24),
        "wire" => Color::srgb(0.34, 0.72, 0.92),
        "bottle_caps" => Color::srgb(0.92, 0.32, 0.38),
        _ => Color::srgb(0.74, 0.84, 0.42),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn npc_interaction_has_priority_inside_range() {
        let player = Transform::from_xyz(0.0, 0.0, 0.0);
        let nearby_npc = Transform::from_xyz(NPC_INTERACTION_DISTANCE - 1.0, 0.0, 0.0);
        let distant_npc = Transform::from_xyz(NPC_INTERACTION_DISTANCE + 1.0, 0.0, 0.0);

        assert!(has_nearby_npc(&player, std::iter::once(&nearby_npc)));
        assert!(!has_nearby_npc(&player, std::iter::once(&distant_npc)));
    }
}
