"""Generate the portfolio world's authored 3D art as deterministic GLB assets.

Run from the repository root:
  blender -b --python tools/blender/generate_world.py

Blender 4.5 LTS is the pinned authoring target.
The exported meshes are scenery only. Navigation, collisions, interaction points,
routing and accessibility remain owned by the React application.
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public" / "world" / "art"
OUT.mkdir(parents=True, exist_ok=True)

ZONE_FILES = {
    "command-center": "command-center.glb",
    "build-lab": "build-lab.glb",
    "automation-lab": "automation-lab.glb",
    "client-street": "client-street.glb",
    "timeline": "timeline.glb",
    "hobby-district": "hobby-district.glb",
}


def reset_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
        # Materials are recreated per scene because every GLB is exported independently.
        if datablocks == bpy.data.materials:
            continue


def mat(name: str, base: tuple[float, float, float, float], *, metallic=0.0, rough=0.5,
        emissive: tuple[float, float, float, float] | None = None, emission_strength=0.0):
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = base
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    if emissive is not None:
        bsdf.inputs["Emission Color"].default_value = emissive
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return material


def finish(obj, material=None, bevel=0.0, smooth=False):
    if material:
        obj.data.materials.append(material)
    if bevel > 0:
        modifier = obj.modifiers.new("soft_edges", "BEVEL")
        modifier.width = bevel
        modifier.segments = 3
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    if smooth and hasattr(obj.data, "polygons"):
        for face in obj.data.polygons:
            face.use_smooth = True
    return obj


def world_to_blender(location):
    """Convert runtime-authored (world X, world Z, world Y) into Blender (X, Y, Z).

    Blender is Z-up while glTF is Y-up. Using this convention keeps intended
    runtime depth stable after Blender's glTF coordinate conversion.
    """
    world_x, world_z, world_y = location
    return (world_x, -world_z, world_y)


def box(name, location, scale, material, bevel=0.08):
    bpy.ops.mesh.primitive_cube_add(location=world_to_blender(location))
    obj = bpy.context.object
    obj.name = name
    obj.scale = (scale[0] / 2, scale[1] / 2, scale[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(obj, material, bevel)


def cyl(name, location, radius, depth, material, vertices=48, bevel=0.05):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=world_to_blender(location),
    )
    obj = bpy.context.object
    obj.name = name
    return finish(obj, material, bevel, smooth=True)


def torus(name, location, major, minor, material, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=64,
        minor_segments=12,
        location=world_to_blender(location),
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    return finish(obj, material, 0.0, smooth=True)


def sphere(name, location, radius, material):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2,
        radius=radius,
        location=world_to_blender(location),
    )
    obj = bpy.context.object
    obj.name = name
    return finish(obj, material, 0.0, smooth=True)


def palette(accent=(0.19, 0.64, 1.0, 1.0)):
    return {
        "floor": mat("Floor", (0.018, 0.035, 0.060, 1), metallic=0.45, rough=0.48),
        "shell": mat("Shell", (0.040, 0.070, 0.105, 1), metallic=0.62, rough=0.33),
        "panel": mat("Panel", (0.075, 0.105, 0.155, 1), metallic=0.40, rough=0.38),
        "dark": mat("Dark", (0.010, 0.018, 0.032, 1), metallic=0.22, rough=0.70),
        "glass": mat("GlassLike", (0.055, 0.145, 0.190, 1), metallic=0.20, rough=0.18),
        "accent": mat("Accent", accent, metallic=0.15, rough=0.28, emissive=accent, emission_strength=5.0),
        "warm": mat("WarmAccent", (1.0, 0.49, 0.18, 1), metallic=0.05, rough=0.32,
                    emissive=(1.0, 0.26, 0.06, 1), emission_strength=4.0),
    }


def base_platform(p, width, depth):
    box("platform", (0, 0, -0.18), (width, depth, 0.28), p["floor"], 0.16)
    # inset floor avoids the flat slab look while keeping the collision plane in React.
    box("inset", (0, 0, -0.025), (width - 0.5, depth - 0.5, 0.05), p["dark"], 0.04)


def build_command_center():
    p = palette((0.18, 0.72, 1.0, 1.0))
    base_platform(p, 15.4, 11.4)
    cyl("core_dais", (0, 0, 0.16), 1.75, 0.34, p["shell"], vertices=64, bevel=0.10)
    cyl("core_step", (0, 0, 0.39), 1.32, 0.15, p["panel"], vertices=64, bevel=0.05)
    for radius, height in ((1.15, 1.25), (0.82, 1.72), (0.48, 2.10)):
        torus("holo_ring", (0, 0, height), radius, 0.035, p["accent"], rotation=(math.pi / 2, 0, 0))
    sphere("holo_core", (0, 0, 1.72), 0.26, p["accent"])
    for angle in range(0, 360, 45):
        a = math.radians(angle)
        x, y = math.cos(a) * 4.6, math.sin(a) * 3.5
        box("radial_console", (x, y, 0.55), (1.25, 0.72, 1.02), p["shell"], 0.16)
        box("console_light", (x, y, 1.08), (0.72, 0.08, 0.22), p["accent"], 0.035)
    for x in (-6.7, 6.7):
        for y in (-4.7, 4.7):
            cyl("corner_pylon", (x, y, 0.75), 0.24, 1.5, p["panel"], vertices=24, bevel=0.04)
            sphere("pylon_light", (x, y, 1.55), 0.12, p["accent"])
    return p


def build_build_lab():
    p = palette((0.48, 0.37, 1.0, 1.0))
    base_platform(p, 11.4, 9.4)
    box("rear_wall", (0, -4.1, 1.55), (10.6, 0.38, 3.2), p["shell"], 0.18)
    for x in (-3.9, -1.3, 1.3, 3.9):
        box("archive_bay", (x, -3.65, 1.05), (2.05, 0.62, 1.8), p["panel"], 0.12)
        box("archive_screen", (x, -3.31, 1.25), (1.18, 0.05, 0.56), p["accent"], 0.025)
        box("archive_trim", (x, -3.28, 0.48), (1.48, 0.04, 0.08), p["accent"], 0.02)
    cyl("review_table", (0, 1.5, 0.38), 1.6, 0.70, p["shell"], vertices=48, bevel=0.10)
    torus("review_holo", (0, 1.5, 1.45), 0.76, 0.045, p["accent"], rotation=(math.pi / 2, 0, 0))
    sphere("review_core", (0, 1.5, 1.45), 0.32, p["accent"])
    for x in (-4.7, 4.7):
        box("side_column", (x, -0.5, 1.45), (0.46, 5.8, 2.9), p["dark"], 0.13)
        box("column_light", (x * 0.995, -0.5, 1.48), (0.08, 4.8, 0.08), p["accent"], 0.02)
    return p


def build_automation_lab():
    p = palette((0.18, 0.95, 0.67, 1.0))
    base_platform(p, 11.4, 9.4)
    for x in (-4.2, -1.4, 1.4, 4.2):
        cyl("agent_pod", (x, -2.65, 0.62), 0.55, 1.18, p["shell"], vertices=32, bevel=0.09)
        sphere("agent_orb", (x, -2.65, 1.58), 0.25, p["accent"])
        torus("agent_ring", (x, -2.65, 1.58), 0.45, 0.027, p["accent"], rotation=(math.pi / 2, 0, 0))
    for y in (-0.35, 1.0, 2.35):
        box("data_rail", (0, y, 0.16), (9.3, 0.18, 0.15), p["panel"], 0.045)
        for x in (-3.9, -1.3, 1.3, 3.9):
            sphere("rail_node", (x, y, 0.38), 0.105, p["accent"])
    box("runtime_wall", (0, 4.05, 1.35), (10.0, 0.4, 2.8), p["shell"], 0.18)
    for x in (-3.2, -1.05, 1.05, 3.2):
        box("runtime_panel", (x, 3.82, 1.45), (1.55, 0.05, 1.05), p["glass"], 0.08)
        box("runtime_glyph", (x, 3.78, 1.45), (0.78, 0.03, 0.06), p["accent"], 0.02)
    return p


def build_client_street():
    p = palette((1.0, 0.46, 0.20, 1.0))
    base_platform(p, 9.4, 11.4)
    box("street", (1.35, 0, 0.035), (2.5, 10.4, 0.08), p["dark"], 0.04)
    for y in (-4.1, -1.35, 1.4, 4.15):
        box("shop_shell", (-2.65, y, 1.45), (3.2, 2.25, 2.9), p["shell"], 0.20)
        box("shop_window", (-0.99, y, 1.42), (0.06, 1.34, 1.38), p["glass"], 0.03)
        box("shop_sign", (-0.94, y, 2.25), (0.05, 1.34, 0.28), p["accent"], 0.03)
        box("awning", (-0.74, y, 2.02), (0.62, 1.9, 0.12), p["panel"], 0.05)
    for y in (-4.7, -2.35, 0, 2.35, 4.7):
        cyl("bollard", (3.7, y, 0.4), 0.11, 0.8, p["panel"], vertices=20, bevel=0.03)
        sphere("bollard_light", (3.7, y, 0.86), 0.08, p["accent"])
    return p


def build_timeline():
    p = palette((1.0, 0.75, 0.18, 1.0))
    base_platform(p, 13.4, 9.4)
    box("timeline_rail", (0, 0, 0.12), (11.9, 0.26, 0.18), p["accent"], 0.05)
    for x, year in ((-4.6, "2014"), (0, "2009"), (4.6, "2007")):
        cyl("timeline_pillar", (x, 0, 1.3), 0.22, 2.6, p["shell"], vertices=28, bevel=0.05)
        torus("timeline_crown", (x, 0, 2.75), 0.62, 0.045, p["accent"], rotation=(math.pi / 2, 0, 0))
        box("timeline_plaque", (x, -0.28, 1.45), (1.6, 0.08, 0.82), p["glass"], 0.08)
    for x in (-6.0, -3.0, 3.0, 6.0):
        box("side_fin", (x, 3.75, 1.25), (0.24, 0.48, 2.5), p["panel"], 0.08)
    return p


def build_hobby():
    p = palette((1.0, 0.30, 0.72, 1.0))
    base_platform(p, 9.4, 11.4)
    cyl("hobby_stage", (0, 0, 0.20), 2.45, 0.35, p["shell"], vertices=64, bevel=0.12)
    torus("stage_light", (0, 0, 0.42), 2.05, 0.045, p["accent"], rotation=(math.pi / 2, 0, 0))
    # Gaming cabinet.
    box("arcade", (-2.7, -3.3, 0.95), (1.28, 0.9, 1.9), p["panel"], 0.18)
    box("arcade_screen", (-2.7, -2.82, 1.18), (0.82, 0.05, 0.62), p["accent"], 0.04)
    # Kettlebell silhouette.
    sphere("kettlebell_body", (2.8, -3.1, 0.55), 0.52, p["shell"])
    torus("kettlebell_handle", (2.8, -3.1, 1.18), 0.42, 0.11, p["accent"], rotation=(math.pi / 2, 0, 0))
    # Anime/display wall and philosophy monoliths.
    box("display_wall", (-3.4, 3.4, 1.3), (2.7, 0.36, 2.6), p["shell"], 0.16)
    box("display_panel", (-3.4, 3.18, 1.4), (1.9, 0.05, 1.45), p["glass"], 0.08)
    for x in (1.8, 3.1):
        box("monolith", (x, 3.35, 1.05), (0.78, 0.7, 2.1), p["panel"], 0.14)
        box("monolith_light", (x, 2.96, 1.05), (0.36, 0.04, 1.1), p["accent"], 0.03)
    return p


BUILDERS = {
    "command-center": build_command_center,
    "build-lab": build_build_lab,
    "automation-lab": build_automation_lab,
    "client-street": build_client_street,
    "timeline": build_timeline,
    "hobby-district": build_hobby,
}


def export_zone(zone: str) -> None:
    reset_scene()
    # Purge materials so every exported file is self-contained and deterministic.
    for material in list(bpy.data.materials):
        bpy.data.materials.remove(material)
    BUILDERS[zone]()
    bpy.ops.object.select_all(action="SELECT")
    path = OUT / ZONE_FILES[zone]
    bpy.ops.export_scene.gltf(
        filepath=str(path),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_materials="EXPORT",
        export_yup=True,
        export_cameras=False,
        export_lights=False,
        export_extras=False,
        export_animations=False,
    )
    print(f"[portfolio-art] exported {zone}: {path}")


for zone_name in ZONE_FILES:
    export_zone(zone_name)

print("[portfolio-art] Blender asset generation complete")
