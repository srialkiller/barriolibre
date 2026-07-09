use serde::Deserialize;

#[derive(Debug, Clone, Deserialize)]
pub struct QuestFile {
    pub quest_id: String,
    pub title: String,
    pub giver_npc_id: String,
    pub required_materials: Vec<RequiredMaterialDef>,
    pub dialogue: QuestDialogueDef,
    pub objectives: QuestObjectiveLabels,
}

#[derive(Debug, Clone, Deserialize)]
pub struct RequiredMaterialDef {
    pub material_id: String,
    pub quantity: u32,
}

#[derive(Debug, Clone, Deserialize)]
pub struct QuestDialogueDef {
    pub intro: String,
    pub accepted: String,
    pub in_progress: String,
    pub ready_to_return: String,
    pub completed: String,
}

#[derive(Debug, Clone, Deserialize)]
pub struct QuestObjectiveLabels {
    pub talk_intro: String,
    pub collect: String,
    #[serde(rename = "return")]
    pub return_label: String,
}

pub fn load_tutorial_quest() -> QuestFile {
    let text = std::fs::read_to_string("data/quests/tutorial_first_cart.json")
        .expect("tutorial quest manifest should exist");
    serde_json::from_str(&text).expect("tutorial quest manifest should be valid JSON")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tutorial_quest_manifest_parses() {
        let quest = load_tutorial_quest();
        assert_eq!(quest.quest_id, "tutorial_first_cart");
        assert_eq!(quest.giver_npc_id, "pedro_vecino");
        assert_eq!(quest.required_materials.len(), 3);
    }
}
