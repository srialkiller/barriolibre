use bevy::prelude::*;

use crate::game::player::components::{AnimState, PlayerAnimation, PlayerSprite};
use crate::game::player::resources::PlayerAssets;

pub fn player_animation_system(
    time: Res<Time>,
    assets: Res<PlayerAssets>,
    mut query: Query<(&mut PlayerAnimation, &mut Sprite), With<PlayerSprite>>,
) {
    if !assets.loaded {
        return;
    }

    for (mut animation, mut sprite) in &mut query {
        let fps = match animation.state {
            AnimState::Idle => assets.definitions.idle.fps,
            AnimState::Walk => assets.definitions.walk.fps,
        };
        animation.timer.tick(time.delta());
        if animation.timer.just_finished() {
            let frame_count = match animation.state {
                AnimState::Idle => assets.definitions.idle.frames as usize,
                AnimState::Walk => assets.definitions.walk.frames_per_direction as usize,
            };
            animation.frame_index = (animation.frame_index + 1) % frame_count.max(1);
            animation.timer = Timer::from_seconds(1.0 / fps.max(1.0), TimerMode::Repeating);
        }

        let index = assets.definitions.atlas_index(
            animation.state,
            animation.facing,
            animation.frame_index,
        );
        if let Some(atlas) = sprite.texture_atlas.as_mut() {
            atlas.index = index;
        }
    }
}
