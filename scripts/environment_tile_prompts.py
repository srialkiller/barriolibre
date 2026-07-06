"""Prompt templates for ENVIRONMENT_BASE_PACK_01 — Carreras de Barrio."""

BASE_PROMPT = """
=== CARRERAS DE BARRIO — ENVIRONMENT_BASE_PACK_01 ===
GAME ART BIBLE + ART_STYLE_GUIDE + VISUAL_LANGUAGE + ASSET_PIPELINE compliant.

Single isometric ground tile for a Latin American neighborhood racing game.
Clean HD hand-painted cartoon game art. NOT pixel art. NOT photorealistic.
Modern casual game tileset style with smooth soft textures, low noise.

CAMERA: isometric 2:1 dimetric diamond tile, 30 degree elevation, 45 degree azimuth NE.
LIGHTING: mid-morning sunny, light from NE (55 deg), warm #FFF5E6.
Shadows toward SW at 35% opacity tint #3A3A5C on surface edges.
No outline on terrain tiles. No text. No labels. No UI.

CANVAS: exactly one diamond-shaped isometric tile filling the center.
Tile aspect ratio 2:1 (width twice height). Seamless tileable edges where specified.
Background OUTSIDE the diamond: 100% solid flat magenta #FF00FF, no gradients.

MATERIAL RULES: clean, cared-for neighborhood. No trash, no grime, no post-apocalyptic.
No buildings, no trees, no people, no vehicles, no objects. Ground infrastructure ONLY.
""".strip()

TILE_SPECS: dict[str, str] = {
    "road_straight_h": """
TILE: asphalt road straight horizontal (runs east-west on isometric diamond).
Dark warm gray asphalt #6B6860 base, #4A4840 shadow on SW edge, #858278 highlight on NE edge.
Road surface spans full tile with road on east and west diamond edges for seamless connection.
Subtle cartoon tire wear texture, very subtle. Center of tile is flat road.
Variant differences: change subtle cracks, patch marks, or wear patterns only.
""",
    "road_straight_v": """
TILE: asphalt road straight vertical (runs north-south on isometric diamond).
Same asphalt palette #6B6860/#4A4840/#858278. Road connects on north and south diamond edges.
Seamless tileable north-south. Subtle warm cartoon asphalt texture.
""",
    "road_corner_ne": """
TILE: asphalt road corner connecting NORTH and EAST edges of isometric diamond.
Road surface turns 90 degrees on the diamond. Same asphalt palette.
Clean cartoon style, seamless on north and east edges.
""",
    "road_corner_nw": """
TILE: asphalt road corner connecting NORTH and WEST edges of isometric diamond.
Same asphalt palette, seamless north and west edges.
""",
    "road_corner_se": """
TILE: asphalt road corner connecting SOUTH and EAST edges of isometric diamond.
Same asphalt palette, seamless south and east edges.
""",
    "road_corner_sw": """
TILE: asphalt road corner connecting SOUTH and WEST edges of isometric diamond.
Same asphalt palette, seamless south and west edges.
""",
    "road_cross": """
TILE: asphalt road four-way cross intersection. Road on all four diamond edges N S E W.
Same asphalt palette. Intersection center slightly lighter.
""",
    "road_deadend": """
TILE: asphalt road dead end. Road enters from SOUTH edge only, ends with curved cap toward north.
Same asphalt palette. Rounded end cap, no exit on other edges (grass or dirt on other edges).
""",
    "road_tjunction_n": """
TILE: asphalt T-junction. Road on NORTH, EAST, WEST edges. South edge is grass #6AAF4A.
Same asphalt palette for road arms.
""",
    "road_tjunction_s": """
TILE: asphalt T-junction. Road on SOUTH, EAST, WEST edges. North edge is grass.
""",
    "road_tjunction_e": """
TILE: asphalt T-junction. Road on EAST, NORTH, SOUTH edges. West edge is grass.
""",
    "road_tjunction_w": """
TILE: asphalt T-junction. Road on WEST, NORTH, SOUTH edges. East edge is grass.
""",
    "road_narrow": """
TILE: narrow asphalt road straight horizontal, thinner lane than standard, east-west connection.
Same palette but road band is 60% normal width centered on tile.
""",
    "road_wide": """
TILE: wide asphalt road straight horizontal, wider lane, east-west connection.
Same palette but road band is 140% normal width.
""",
    "road_damaged": """
TILE: damaged asphalt road straight horizontal east-west. Same base palette but visible cracks,
small pothole patches in cartoon style (not dangerous looking). Still clean and cared-for.
""",
    "road_patched": """
TILE: patched asphalt road straight horizontal east-west. Lighter gray patch rectangles
#858278 on #6B6860 base showing recent repair. Cared-for neighborhood feel.
""",
    "sidewalk_straight": """
TILE: concrete sidewalk straight, cement #B8B0A4 base, #8A8278 SW shadow, #D4CCC0 NE highlight.
Sidewalk connects east-west edges. Slightly raised curb lip visible on south edge as thin line.
Clean well-maintained Latin American neighborhood sidewalk.
""",
    "sidewalk_corner": """
TILE: concrete sidewalk corner connecting north and east edges. Cement palette #B8B0A4.
""",
    "sidewalk_inner_corner": """
TILE: concrete sidewalk inner corner, north and west edges connected. Cement palette.
""",
    "sidewalk_outer_corner": """
TILE: concrete sidewalk outer corner, south and east edges. Cement palette.
""",
    "sidewalk_crossing": """
TILE: sidewalk cross junction, cement on all four edges N S E W.
""",
    "sidewalk_ramp": """
TILE: sidewalk ramp straight east-west, gentle slope indicated by shading, accessible curb cut.
Cement palette, seamless east-west.
""",
    "curb_straight": """
TILE: curb strip straight east-west. Thin raised edge between sidewalk (north) and road (south).
Concrete #B8B0A4 curb top, asphalt #6B6860 visible south. Seamless east-west.
""",
    "curb_corner": """
TILE: curb corner north-east. Thin raised curb line turning 90 degrees.
""",
    "curb_ramp": """
TILE: curb ramp with lowered curb cut for accessibility, east-west seamless.
""",
    "grass_clean": """
TILE: clean healthy grass fill tile. Green #6AAF4A base, #4A8830 shadow SW, #82C860 highlight NE.
Full diamond fill, seamless all edges for tiling. Soft cartoon grass tufts suggestion, no flowers.
Variant: vary tuft density and slight color shift within palette only.
""",
    "grass_dry": """
TILE: dry summer grass fill. Slightly yellow-green #78A040 base, warmer tones, still clean and healthy.
Full diamond seamless fill.
""",
    "dirt_compact": """
TILE: compact dirt ground #A08058 base, #705840 shadow. Full diamond seamless fill.
Smooth packed earth, clean barrio vacant lot feel, not muddy.
""",
    "dirt_soft": """
TILE: soft dirt ground slightly lighter #B89868, loose soil texture suggested softly.
Full diamond seamless fill.
""",
    "concrete_clean": """
TILE: clean concrete pavement #B8B0A4, full diamond fill, seamless edges.
Smooth well-maintained surface, plaza or driveway feel.
""",
    "concrete_old": """
TILE: older concrete #989088 with subtle hairline cracks (cartoon, not broken).
Still clean and functional. Full diamond seamless fill.
""",
    "gravel": """
TILE: gravel ripio surface #C8B898 base, #988868 shadow. Small pebble suggestion softly.
Full diamond seamless fill. Parking area or unpaved lane feel.
""",
    "marking_manhole": """
TILE OVERLAY: round metal manhole cover centered on asphalt #6B6860 road base.
Dark gray circle #505050 with simple radial line pattern, no readable text. Cartoon style.
""",
    "marking_storm_drain": """
TILE OVERLAY: storm drain grate on asphalt, rectangular slotted grate near south edge of tile.
Dark gray #505050 slots on #6B6860 asphalt.
""",
    "marking_crack_small": """
TILE OVERLAY: small hairline crack on asphalt road base #6B6860. Thin dark line #4A4840, subtle.
""",
    "marking_crack_large": """
TILE OVERLAY: larger cartoon crack on asphalt, branching thin lines, still clean not destructive.
""",
    "marking_repair_asphalt": """
TILE OVERLAY: fresh asphalt repair patch, lighter gray rectangle #858278 on road #6B6860.
""",
    "marking_paint_straight": """
TILE OVERLAY: white road lane marking dashed line #F0F0E8 running east-west center of asphalt tile.
""",
    "marking_paint_stop": """
TILE OVERLAY: white stop line bar #F0F0E8 across road near north edge on asphalt base.
""",
    "marking_paint_crosswalk": """
TILE OVERLAY: zebra crosswalk white stripes #F0F0E8 across asphalt road, cartoon style.
""",
    "marking_paint_arrow": """
TILE OVERLAY: white direction arrow #F0F0E8 painted on asphalt pointing east.
""",
    "transition_road_dirt": """
TILE: transition half asphalt road #6B6860 north half, half compact dirt #A08058 south half.
Clean straight boundary between materials on east-west axis. Seamless on all edges.
""",
    "transition_road_grass": """
TILE: transition half asphalt north, half grass #6AAF4A south. Clean material boundary.
""",
    "transition_sidewalk_grass": """
TILE: transition half cement sidewalk #B8B0A4 north, half grass south.
""",
    "transition_concrete_grass": """
TILE: transition half concrete #B8B0A4 north, half grass south.
""",
    "transition_concrete_dirt": """
TILE: transition half concrete north, half dirt #A08058 south.
""",
    "transition_grass_dirt": """
TILE: transition half grass #6AAF4A north, half dirt #A08058 south.
""",
}


def build_prompt(tile_key: str, variant: int = 1, reference_note: str = "") -> str:
    spec = TILE_SPECS.get(tile_key, "")
    variant_note = f"VARIANT {variant}: change subtle texture, cracks, patches, or color within palette. Same silhouette and connections."
    ref = f"\n{reference_note}" if reference_note else ""
    return f"{BASE_PROMPT}\n\n{spec}\n\n{variant_note}{ref}\n\nMANDATORY: solid #FF00FF outside diamond. One tile only. 256x128 isometric diamond."
