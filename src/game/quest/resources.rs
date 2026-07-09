use bevy::prelude::*;
use std::collections::HashMap;

use crate::game::inventory::resources::MaterialId;
use crate::game::inventory::resources::PlayerInventory;
use crate::game::quest::data::QuestFile;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum QuestStage {
    NotStarted,
    Accepted,
    ReadyToReturn,
    Completed,
}

#[derive(Resource, Debug)]
pub struct TutorialQuestState {
    pub definition: QuestFile,
    pub stage: QuestStage,
}

impl TutorialQuestState {
    pub fn new(definition: QuestFile) -> Self {
        Self { definition, stage: QuestStage::NotStarted }
    }

    pub fn required_materials(&self) -> Vec<(MaterialId, u32)> {
        self.definition
            .required_materials
            .iter()
            .map(|material| (MaterialId::new(&material.material_id), material.quantity))
            .collect()
    }
}

#[derive(Resource, Debug, Default)]
pub struct NpcDialogueOverrides {
    pub lines: HashMap<String, String>,
}

#[derive(Resource, Debug, Default, Clone)]
pub struct ActiveQuestHud {
    pub visible: bool,
    pub title: String,
    pub objective: String,
}

pub fn materials_progress(
    inventory: &PlayerInventory,
    required: &[(MaterialId, u32)],
) -> (u32, u32) {
    let total = required.len() as u32;
    let collected = required
        .iter()
        .filter(|(material_id, quantity)| inventory.quantity(material_id) >= *quantity)
        .count() as u32;
    (collected, total)
}

pub fn materials_complete(inventory: &PlayerInventory, required: &[(MaterialId, u32)]) -> bool {
    required
        .iter()
        .all(|(material_id, quantity)| inventory.quantity(material_id) >= *quantity)
}

pub fn next_stage_after_npc_interact(
    stage: QuestStage,
    npc_id: &str,
    giver_npc_id: &str,
) -> QuestStage {
    if npc_id != giver_npc_id {
        return stage;
    }

    match stage {
        QuestStage::NotStarted => QuestStage::Accepted,
        QuestStage::ReadyToReturn => QuestStage::Completed,
        _ => stage,
    }
}

pub fn dialogue_for_stage(
    stage: QuestStage,
    collected: u32,
    dialogue: &crate::game::quest::data::QuestDialogueDef,
) -> &str {
    match stage {
        QuestStage::NotStarted => &dialogue.intro,
        QuestStage::Accepted if collected == 0 => &dialogue.accepted,
        QuestStage::Accepted => &dialogue.in_progress,
        QuestStage::ReadyToReturn => &dialogue.ready_to_return,
        QuestStage::Completed => &dialogue.completed,
    }
}

pub fn objective_for_stage(
    stage: QuestStage,
    collected: u32,
    total: u32,
    labels: &crate::game::quest::data::QuestObjectiveLabels,
) -> String {
    match stage {
        QuestStage::NotStarted => labels.talk_intro.clone(),
        QuestStage::Accepted => format!("{} ({collected}/{total})", labels.collect),
        QuestStage::ReadyToReturn => labels.return_label.clone(),
        QuestStage::Completed => "Misión completada".to_string(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::game::quest::data::load_tutorial_quest;

    #[test]
    fn first_pedro_talk_accepts_quest() {
        let next =
            next_stage_after_npc_interact(QuestStage::NotStarted, "pedro_vecino", "pedro_vecino");
        assert_eq!(next, QuestStage::Accepted);
    }

    #[test]
    fn unrelated_npc_does_not_advance_quest() {
        let next =
            next_stage_after_npc_interact(QuestStage::NotStarted, "other_npc", "pedro_vecino");
        assert_eq!(next, QuestStage::NotStarted);
    }

    #[test]
    fn return_talk_completes_quest() {
        let next =
            next_stage_after_npc_interact(QuestStage::ReadyToReturn, "pedro_vecino", "pedro_vecino");
        assert_eq!(next, QuestStage::Completed);
    }

    #[test]
    fn inventory_tracks_required_materials() {
        let quest = load_tutorial_quest();
        let required = quest
            .required_materials
            .iter()
            .map(|material| (MaterialId::new(&material.material_id), material.quantity))
            .collect::<Vec<_>>();

        let mut inventory = PlayerInventory::default();
        assert!(!materials_complete(&inventory, &required));

        inventory.add_material(MaterialId::new("cardboard"), "Cartón", 1);
        inventory.add_material(MaterialId::new("wire"), "Alambre", 1);
        inventory.add_material(MaterialId::new("bottle_caps"), "Chapitas", 1);

        assert!(materials_complete(&inventory, &required));
        assert_eq!(materials_progress(&inventory, &required), (3, 3));
    }
}
