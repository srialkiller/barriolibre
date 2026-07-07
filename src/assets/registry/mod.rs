use std::collections::HashMap;
use std::fmt;

use bevy::prelude::*;
use serde::Deserialize;

#[derive(Clone, Debug, Hash, PartialEq, Eq, PartialOrd, Ord)]
pub struct TileId(pub String);

impl TileId {
    pub fn new(value: impl Into<String>) -> Self {
        Self(value.into())
    }
}

impl fmt::Display for TileId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}", self.0)
    }
}

impl From<&str> for TileId {
    fn from(value: &str) -> Self {
        Self(value.to_owned())
    }
}

#[derive(Resource, Debug, Default)]
pub struct AssetRegistry {
    tiles: HashMap<TileId, Handle<Image>>,
    props: HashMap<String, Handle<Image>>,
    loaded_count: usize,
    missing_count: usize,
}

impl AssetRegistry {
    pub fn tile(&self, id: &TileId) -> Option<&Handle<Image>> {
        self.tiles.get(id)
    }

    pub fn register_tile(&mut self, id: TileId, handle: Handle<Image>) {
        self.tiles.insert(id, handle);
        self.loaded_count += 1;
    }

    pub fn prop(&self, prop_id: &str) -> Option<&Handle<Image>> {
        self.props.get(prop_id)
    }

    pub fn register_prop(&mut self, prop_id: String, handle: Handle<Image>) {
        self.props.insert(prop_id, handle);
        self.loaded_count += 1;
    }

    pub fn prop_count(&self) -> usize {
        self.props.len()
    }

    pub fn register_missing(&mut self) {
        self.missing_count += 1;
    }

    pub fn loaded_count(&self) -> usize {
        self.loaded_count
    }

    pub fn missing_count(&self) -> usize {
        self.missing_count
    }

    pub fn total_registered(&self) -> usize {
        self.tiles.len()
    }
}

#[derive(Debug, Deserialize)]
pub struct GeneratedManifest {
    pub generated: Vec<String>,
}

#[derive(Debug, Deserialize)]
pub struct PackManifest {
    pub pack_id: String,
    pub version: String,
    pub base_path: String,
}

#[derive(Resource, Debug, Default)]
pub struct AssetLoadState {
    pub manifest_verified: bool,
    pub pack_id: String,
    pub pending_ids: Vec<TileId>,
    pub finished: bool,
}
