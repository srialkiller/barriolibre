use bevy::prelude::*;

use crate::ui::UiFont;

use crate::game::garage::events::GarageUnlocked;
use crate::game::inventory::events::ItemCollected;
use crate::game::inventory::resources::PlayerInventory;
use crate::game::player::events::NpcInteracted;
use crate::game::quest::components::{QuestHudRoot, QuestHudText};
use crate::game::quest::data::load_tutorial_quest;
use crate::game::quest::events::QuestCompleted;
use crate::game::quest::resources::{
    dialogue_for_stage, materials_complete, materials_progress, next_stage_after_npc_interact,
    objective_for_stage, ActiveQuestHud, NpcDialogueOverrides, QuestStage, TutorialQuestState,
};

pub fn init_tutorial_quest_system(mut commands: Commands) {
    let definition = load_tutorial_quest();
    let mut overrides = NpcDialogueOverrides::default();
    overrides
        .lines
        .insert(definition.giver_npc_id.clone(), definition.dialogue.intro.clone());

    let hud = ActiveQuestHud {
        visible: true,
        title: definition.title.clone(),
        objective: definition.objectives.talk_intro.clone(),
    };

    commands.insert_resource(TutorialQuestState::new(definition));
    commands.insert_resource(overrides);
    commands.insert_resource(hud);
}

pub fn spawn_quest_ui_system(mut commands: Commands, ui_font: Res<UiFont>) {
    commands
        .spawn((
            QuestHudRoot,
            Node {
                position_type: PositionType::Absolute,
                top: Val::Px(24.0),
                left: Val::Px(24.0),
                width: Val::Px(360.0),
                padding: UiRect::all(Val::Px(14.0)),
                display: Display::Flex,
                flex_direction: FlexDirection::Column,
                row_gap: Val::Px(6.0),
                ..default()
            },
            BackgroundColor(Color::srgba(0.05, 0.07, 0.1, 0.92)),
        ))
        .with_children(|parent| {
            parent.spawn((
                QuestHudText,
                Text::new(""),
                ui_font.sized(18.0),
                TextColor(Color::srgb(0.92, 0.96, 0.82)),
            ));
        });
}

pub fn handle_npc_interacted_quest_system(
    mut events: EventReader<NpcInteracted>,
    mut quest: ResMut<TutorialQuestState>,
    mut completed_events: EventWriter<QuestCompleted>,
    mut garage_events: EventWriter<GarageUnlocked>,
) {
    for event in events.read() {
        let previous = quest.stage;
        quest.stage = next_stage_after_npc_interact(
            quest.stage,
            &event.npc_id,
            &quest.definition.giver_npc_id,
        );

        if previous == QuestStage::ReadyToReturn && quest.stage == QuestStage::Completed {
            completed_events.send(QuestCompleted {
                quest_id: quest.definition.quest_id.clone(),
            });
            garage_events.send(GarageUnlocked);
            tracing::info!(quest_id = %quest.definition.quest_id, "Tutorial quest completed");
        } else if previous == QuestStage::NotStarted && quest.stage == QuestStage::Accepted {
            tracing::info!(quest_id = %quest.definition.quest_id, "Tutorial quest accepted");
        }
    }
}

pub fn handle_item_collected_quest_system(
    mut events: EventReader<ItemCollected>,
    mut quest: ResMut<TutorialQuestState>,
    inventory: Res<PlayerInventory>,
) {
    for event in events.read() {
        tracing::debug!(
            material_id = %event.material_id,
            display_name = %event.display_name,
            amount = event.amount,
            new_total = event.new_total,
            "Quest received item collected"
        );

        if quest.stage != QuestStage::Accepted {
            continue;
        }

        let required = quest.required_materials();
        if materials_complete(&inventory, &required) {
            quest.stage = QuestStage::ReadyToReturn;
            tracing::info!(
                quest_id = %quest.definition.quest_id,
                material_id = %event.material_id,
                "All materials collected"
            );
            break;
        }
    }
}

pub fn sync_quest_presentations_system(
    quest: Res<TutorialQuestState>,
    inventory: Res<PlayerInventory>,
    mut overrides: ResMut<NpcDialogueOverrides>,
    mut hud: ResMut<ActiveQuestHud>,
) {
    if !quest.is_changed() && !inventory.is_changed() {
        return;
    }

    let required = quest.required_materials();
    let (collected, total) = materials_progress(&inventory, &required);

    let dialogue = dialogue_for_stage(quest.stage, collected, &quest.definition.dialogue);
    overrides.lines.insert(quest.definition.giver_npc_id.clone(), dialogue.to_string());

    hud.visible = quest.stage != QuestStage::Completed;
    hud.title = quest.definition.title.clone();
    hud.objective =
        objective_for_stage(quest.stage, collected, total, &quest.definition.objectives);
}

pub fn sync_quest_ui_system(
    hud: Res<ActiveQuestHud>,
    mut nodes: Query<&mut Node, With<QuestHudRoot>>,
    mut texts: Query<&mut Text, With<QuestHudText>>,
) {
    let message = format!("{}\n\n> {}", hud.title, hud.objective);
    for mut node in &mut nodes {
        node.display = if hud.visible { Display::Flex } else { Display::None };
    }
    for mut text in &mut texts {
        if text.0 != message {
            text.0.clone_from(&message);
        }
    }
}
