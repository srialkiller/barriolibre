use std::collections::HashMap;
use std::fmt;

use bevy::prelude::*;

#[derive(Debug, Clone, Hash, PartialEq, Eq, PartialOrd, Ord)]
pub struct MaterialId(String);

impl MaterialId {
    pub fn new(value: impl Into<String>) -> Self {
        Self(value.into())
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for MaterialId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.0)
    }
}

#[derive(Resource, Debug, Default)]
pub struct PlayerInventory {
    materials: HashMap<MaterialId, u32>,
    display_names: HashMap<MaterialId, String>,
}

impl PlayerInventory {
    pub fn add_material(
        &mut self,
        material_id: MaterialId,
        display_name: impl Into<String>,
        quantity: u32,
    ) -> u32 {
        self.display_names.insert(material_id.clone(), display_name.into());
        let total = self.materials.entry(material_id).or_default();
        *total = total.saturating_add(quantity);
        *total
    }

    pub fn quantity(&self, material_id: &MaterialId) -> u32 {
        self.materials.get(material_id).copied().unwrap_or_default()
    }

    pub fn sorted_materials(&self) -> Vec<(&MaterialId, &str, u32)> {
        let mut materials = self
            .materials
            .keys()
            .map(|material_id| {
                let display_name = self
                    .display_names
                    .get(material_id)
                    .map_or_else(|| material_id.as_str(), String::as_str);
                (material_id, display_name, self.quantity(material_id))
            })
            .collect::<Vec<_>>();
        materials.sort_by(|left, right| left.0.cmp(right.0));
        materials
    }

    pub fn is_empty(&self) -> bool {
        self.materials.is_empty()
    }
}

#[derive(Resource, Debug, Default)]
pub struct InventoryUiState {
    pub visible: bool,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn add_material_stacks_quantities() {
        let mut inventory = PlayerInventory::default();
        let cardboard_id = MaterialId::new("cardboard");

        inventory.add_material(cardboard_id.clone(), "Cartón", 1);
        let total = inventory.add_material(cardboard_id.clone(), "Cartón", 2);

        assert_eq!(total, 3);
        assert_eq!(inventory.quantity(&cardboard_id), 3);
    }

    #[test]
    fn missing_material_has_zero_quantity() {
        let inventory = PlayerInventory::default();
        assert_eq!(inventory.quantity(&MaterialId::new("wire")), 0);
    }
}
