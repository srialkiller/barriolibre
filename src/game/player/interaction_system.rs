use bevy::prelude::*;

use crate::game::player::components::Player;
use crate::ui::UiFont;
use crate::game::player::events::NpcInteracted;
use crate::game::player::resources::PlayerInteractionState;
use crate::game::quest::NpcDialogueOverrides;
use crate::world::map::components::NeighborhoodNpc;

pub const NPC_INTERACTION_DISTANCE: f32 = 190.0;

#[derive(Component)]
pub struct InteractionUiRoot;

#[derive(Component)]
pub struct InteractionUiText;

pub fn spawn_interaction_ui_system(mut commands: Commands, ui_font: Res<UiFont>) {
    commands
        .spawn((
            InteractionUiRoot,
            Node {
                position_type: PositionType::Absolute,
                bottom: Val::Px(24.0),
                left: Val::Percent(20.0),
                right: Val::Percent(20.0),
                padding: UiRect::all(Val::Px(12.0)),
                justify_content: JustifyContent::Center,
                display: Display::None,
                ..default()
            },
            BackgroundColor(Color::srgba(0.05, 0.04, 0.08, 0.9)),
        ))
        .with_children(|parent| {
            parent.spawn((
                InteractionUiText,
                Text::new(""),
                ui_font.sized(18.0),
                TextColor(Color::srgb(1.0, 0.94, 0.78)),
            ));
        });
}

pub fn interact_with_npc_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    player: Query<&Transform, With<Player>>,
    npcs: Query<(&Transform, &NeighborhoodNpc)>,
    mut interaction_state: ResMut<PlayerInteractionState>,
    dialogue_overrides: Option<Res<NpcDialogueOverrides>>,
    mut npc_interacted_events: EventWriter<NpcInteracted>,
    mut ui_nodes: Query<&mut Node, With<InteractionUiRoot>>,
    mut ui_texts: Query<&mut Text, With<InteractionUiText>>,
) {
    let Ok(player_transform) = player.get_single() else {
        return;
    };

    let nearest_npc = npcs
        .iter()
        .filter_map(|(transform, npc)| {
            let distance =
                player_transform.translation.truncate().distance(transform.translation.truncate());
            (distance <= NPC_INTERACTION_DISTANCE).then_some((distance, npc))
        })
        .min_by(|(left_distance, _), (right_distance, _)| left_distance.total_cmp(right_distance));

    let Some((_, npc)) = nearest_npc else {
        interaction_state.active_npc_id = None;
        interaction_state.dialogue_open = false;
        set_interaction_ui(&mut ui_nodes, &mut ui_texts, None);
        return;
    };

    if interaction_state.active_npc_id.as_deref() != Some(&npc.npc_id) {
        interaction_state.active_npc_id = Some(npc.npc_id.clone());
        interaction_state.dialogue_open = false;
    }

    if keyboard.just_pressed(KeyCode::KeyE) {
        let was_open = interaction_state.dialogue_open;
        interaction_state.dialogue_open = !interaction_state.dialogue_open;
        if !was_open && interaction_state.dialogue_open {
            npc_interacted_events.send(NpcInteracted { npc_id: npc.npc_id.clone() });
        }
    }

    let dialogue_text = dialogue_overrides
        .as_ref()
        .and_then(|overrides| overrides.lines.get(&npc.npc_id))
        .map(String::as_str)
        .unwrap_or(&npc.dialogue);

    let message = if interaction_state.dialogue_open {
        format!("{}: {}\n[E] Cerrar", npc.display_name, dialogue_text)
    } else {
        format!("[E] Hablar con {}", npc.display_name)
    };
    set_interaction_ui(&mut ui_nodes, &mut ui_texts, Some(message));
}

fn set_interaction_ui(
    ui_nodes: &mut Query<&mut Node, With<InteractionUiRoot>>,
    ui_texts: &mut Query<&mut Text, With<InteractionUiText>>,
    message: Option<String>,
) {
    let is_visible = message.is_some();
    for mut node in ui_nodes.iter_mut() {
        node.display = if is_visible { Display::Flex } else { Display::None };
    }
    if let Some(message) = message {
        for mut text in ui_texts.iter_mut() {
            text.0.clone_from(&message);
        }
    }
}
