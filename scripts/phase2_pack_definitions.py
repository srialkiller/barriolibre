#!/usr/bin/env python3
"""Phase 2 batch definitions — explicit tile IDs and grid sizes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GridPack:
    raw_name: str
    category: str
    tile_base: str
    tile_ids: list[str]
    rows: int
    cols: int


def v(base: str, nums: list[int]) -> list[str]:
    return [f"{base}_{n:02d}" for n in nums]


GRID_PACKS: list[GridPack] = [
    # Roads — variants 02-03 only (1x2 strips)
    GridPack("phase2_road_straight_v_raw.png", "roads", "road_straight_v", v("road_straight_v", [2, 3]), 1, 2),
    GridPack("phase2_road_corner_ne_raw.png", "roads", "road_corner_ne", v("road_corner_ne", [2, 3]), 1, 2),
    GridPack("phase2_road_corner_nw_raw.png", "roads", "road_corner_nw", v("road_corner_nw", [2, 3]), 1, 2),
    GridPack("phase2_road_corner_se_raw.png", "roads", "road_corner_se", v("road_corner_se", [2, 3]), 1, 2),
    GridPack("phase2_road_corner_sw_raw.png", "roads", "road_corner_sw", v("road_corner_sw", [2, 3]), 1, 2),
    GridPack("phase2_road_tjunction_n_raw.png", "roads", "road_tjunction_n", v("road_tjunction_n", [2, 3]), 1, 2),
    GridPack("phase2_road_tjunction_s_raw.png", "roads", "road_tjunction_s", v("road_tjunction_s", [2, 3]), 1, 2),
    GridPack("phase2_road_tjunction_e_raw.png", "roads", "road_tjunction_e", v("road_tjunction_e", [1, 2, 3]), 1, 3),
    GridPack("phase2_road_tjunction_w_raw.png", "roads", "road_tjunction_w", v("road_tjunction_w", [1, 2, 3]), 1, 3),
    GridPack("phase2_road_cross_raw.png", "roads", "road_cross", v("road_cross", [2, 3]), 1, 2),
    GridPack("phase2_road_deadend_raw.png", "roads", "road_deadend", v("road_deadend", [2, 3]), 1, 2),
    GridPack("phase2_road_narrow_raw.png", "roads", "road_narrow", v("road_narrow", [2, 3]), 1, 2),
    GridPack("phase2_road_wide_raw.png", "roads", "road_wide", v("road_wide", [2, 3]), 1, 2),
    GridPack("phase2_road_damaged_raw.png", "roads", "road_damaged", v("road_damaged", [2, 3]), 1, 2),
    GridPack("phase2_road_patched_raw.png", "roads", "road_patched", v("road_patched", [2, 3]), 1, 2),
    # Sidewalks — new types (1x3)
    GridPack("phase2_sidewalk_corner_raw.png", "sidewalks", "sidewalk_corner", v("sidewalk_corner", [1, 2, 3]), 1, 3),
    GridPack("phase2_sidewalk_inner_corner_raw.png", "sidewalks", "sidewalk_inner_corner", v("sidewalk_inner_corner", [1, 2, 3]), 1, 3),
    GridPack("phase2_sidewalk_outer_corner_raw.png", "sidewalks", "sidewalk_outer_corner", v("sidewalk_outer_corner", [1, 2, 3]), 1, 3),
    GridPack("phase2_sidewalk_crossing_raw.png", "sidewalks", "sidewalk_crossing", v("sidewalk_crossing", [1, 2, 3]), 1, 3),
    GridPack("phase2_sidewalk_ramp_raw.png", "sidewalks", "sidewalk_ramp", v("sidewalk_ramp", [1, 2, 3]), 1, 3),
    # Curbs
    GridPack("phase2_curb_straight_raw.png", "curbs", "curb_straight", v("curb_straight", [2, 3]), 1, 2),
    GridPack("phase2_curb_corner_raw.png", "curbs", "curb_corner", v("curb_corner", [1, 2, 3]), 1, 3),
    GridPack("phase2_curb_ramp_raw.png", "curbs", "curb_ramp", v("curb_ramp", [1, 2, 3]), 1, 3),
    # Terrain — 5 variants (2x3 grid, use 5 cells left-to-right top row then 2 bottom)
    GridPack("phase2_dirt_soft_raw.png", "terrain", "dirt_soft", v("dirt_soft", [1, 2, 3, 4, 5]), 2, 3),
    GridPack("phase2_concrete_old_raw.png", "terrain", "concrete_old", v("concrete_old", [1, 2, 3, 4, 5]), 2, 3),
    # Markings
    GridPack("phase2_marking_manhole_raw.png", "markings", "marking_manhole", v("marking_manhole", [2, 3]), 1, 2),
    GridPack("phase2_marking_storm_drain_raw.png", "markings", "marking_storm_drain", v("marking_storm_drain", [1, 2, 3]), 1, 3),
    GridPack("phase2_marking_crack_small_raw.png", "markings", "marking_crack_small", v("marking_crack_small", [1, 2, 3]), 1, 3),
    GridPack("phase2_marking_crack_large_raw.png", "markings", "marking_crack_large", v("marking_crack_large", [1, 2, 3]), 1, 3),
    GridPack("phase2_marking_repair_raw.png", "markings", "marking_repair_asphalt", v("marking_repair_asphalt", [1, 2, 3]), 1, 3),
    GridPack("phase2_marking_paint_straight_raw.png", "markings", "marking_paint_straight", v("marking_paint_straight", [2, 3]), 1, 2),
    GridPack("phase2_marking_paint_stop_raw.png", "markings", "marking_paint_stop", v("marking_paint_stop", [1, 2, 3]), 1, 3),
    GridPack("phase2_marking_paint_crosswalk_raw.png", "markings", "marking_paint_crosswalk", v("marking_paint_crosswalk", [1, 2, 3]), 1, 3),
    GridPack("phase2_marking_paint_arrow_raw.png", "markings", "marking_paint_arrow", v("marking_paint_arrow", [1, 2, 3]), 1, 3),
    # Transitions
    GridPack("phase2_transition_road_dirt_raw.png", "transitions", "transition_road_dirt", v("transition_road_dirt", [2, 3]), 1, 2),
    GridPack("phase2_transition_road_grass_raw.png", "transitions", "transition_road_grass", v("transition_road_grass", [2, 3]), 1, 2),
    GridPack("phase2_transition_sidewalk_grass_raw.png", "transitions", "transition_sidewalk_grass", v("transition_sidewalk_grass", [1, 2, 3]), 1, 3),
    GridPack("phase2_transition_concrete_grass_raw.png", "transitions", "transition_concrete_grass", v("transition_concrete_grass", [1, 2, 3]), 1, 3),
    GridPack("phase2_transition_concrete_dirt_raw.png", "transitions", "transition_concrete_dirt", v("transition_concrete_dirt", [1, 2, 3]), 1, 3),
    GridPack("phase2_transition_grass_dirt_raw.png", "transitions", "transition_grass_dirt", v("transition_grass_dirt", [2, 3]), 1, 2),
]

CONNECTIONS: dict[str, dict] = {
    "road_straight_v": {"north": "road", "south": "road"},
    "road_corner_ne": {"north": "road", "east": "road"},
    "road_corner_nw": {"north": "road", "west": "road"},
    "road_corner_se": {"south": "road", "east": "road"},
    "road_corner_sw": {"south": "road", "west": "road"},
    "road_tjunction_n": {"north": "road", "east": "road", "west": "road"},
    "road_tjunction_s": {"south": "road", "east": "road", "west": "road"},
    "road_tjunction_e": {"east": "road", "north": "road", "south": "road"},
    "road_tjunction_w": {"west": "road", "north": "road", "south": "road"},
    "road_cross": {"north": "road", "south": "road", "east": "road", "west": "road"},
    "road_deadend": {"south": "road"},
    "road_narrow": {"east": "road", "west": "road"},
    "road_wide": {"east": "road", "west": "road"},
    "road_damaged": {"east": "road", "west": "road"},
    "road_patched": {"east": "road", "west": "road"},
    "sidewalk_corner": {"north": "sidewalk", "east": "sidewalk"},
    "sidewalk_inner_corner": {"north": "sidewalk", "west": "sidewalk"},
    "sidewalk_outer_corner": {"south": "sidewalk", "east": "sidewalk"},
    "sidewalk_crossing": {"north": "sidewalk", "south": "sidewalk", "east": "sidewalk", "west": "sidewalk"},
    "sidewalk_ramp": {"east": "sidewalk", "west": "sidewalk"},
    "curb_straight": {"east": "curb", "west": "curb"},
    "curb_corner": {"north": "curb", "east": "curb"},
    "curb_ramp": {"east": "curb", "west": "curb"},
    "dirt_soft": {"fill": "dirt"},
    "concrete_old": {"fill": "concrete"},
    "marking_manhole": {},
    "marking_storm_drain": {},
    "marking_crack_small": {},
    "marking_crack_large": {},
    "marking_repair_asphalt": {},
    "marking_paint_straight": {},
    "marking_paint_stop": {},
    "marking_paint_crosswalk": {},
    "marking_paint_arrow": {},
    "transition_road_dirt": {"north": "road", "south": "dirt"},
    "transition_road_grass": {"north": "road", "south": "grass"},
    "transition_sidewalk_grass": {"north": "sidewalk", "south": "grass"},
    "transition_concrete_grass": {"north": "concrete", "south": "grass"},
    "transition_concrete_dirt": {"north": "concrete", "south": "dirt"},
    "transition_grass_dirt": {"north": "grass", "south": "dirt"},
}
