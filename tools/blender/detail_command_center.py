"""Add the bounded authored detail pass and render canonical review views."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "art/blender/command-center"
SOURCE = ART / "source/command-center.blend"
PREVIEWS = ART / "previews"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from command_center_common import aim_object_at, select_eevee_engine  # noqa: E402

export = bpy.data.collections["EXPORT_COMMAND_CENTER"]
preview = bpy.data.collections["PREVIEW_DO_NOT_EXPORT"]

# Make the bounded recipe rerunnable after a structural validation correction.
detail_prefixes = (
    "cc_facade_", "cc_civic_arch_", "cc_lateral_", "cc_core_structural_",
    "cc_core_crown_outer", "cc_core_crown_inner", "cc_foreground_",
    "cc_floating_", "cc_landscape_",
)
for obj in list(export.objects):
    if obj.name.startswith(detail_prefixes):
        bpy.data.objects.remove(obj, do_unlink=True)


def material(name, color, metallic=0.0, roughness=0.6, emission=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Emission Color"].default_value = (*color, 1)
    bsdf.inputs["Emission Strength"].default_value = emission
    return mat


stone = bpy.data.materials.get("CC_SoftMetal")
dark = bpy.data.materials.get("CC_Graphite")
teal = bpy.data.materials.get("CC_Teal")
cyan = material("CC_Cyan", (0.04, 0.36, 0.42), 0.35, 0.35, 0.3)
glass = material("CC_DarkGlass", (0.025, 0.08, 0.11), 0.65, 0.2, 0.05)


def finish(obj, name, mat, collection=export, bevel=0.0):
    obj.name = name
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    collection.objects.link(obj)
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new("Detail edge", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        bpy.ops.object.modifier_apply(modifier=mod.name)
    obj.select_set(False)
    return obj


def box(name, loc, size, mat=stone, collection=export, bevel=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.scale = size
    return finish(obj, name, mat, collection, bevel)


def cylinder(name, loc, radius, depth, mat=stone, collection=export, vertices=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    return finish(bpy.context.object, name, mat, collection, 0.025)


def torus(name, loc, major, minor, mat=stone, collection=export, rotate=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major, minor_radius=minor, major_segments=32, minor_segments=8,
        location=loc, rotation=rotate,
    )
    obj = bpy.context.object
    obj.scale = scale
    return finish(obj, name, mat, collection)


def arc(name, center, radius, start, end, z, tube, mat=stone, collection=export):
    verts = []
    faces = []
    segments = 20
    for i in range(segments + 1):
        a = start + (end - start) * i / segments
        for dz in (-tube, tube):
            verts.append((center[0] + radius * math.cos(a), center[1] + radius * math.sin(a), z + dz))
    for i in range(segments):
        j = i + 1
        faces.append((2 * i, 2 * j, 2 * j + 1, 2 * i + 1))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    return finish(bpy.data.objects.new(name, mesh), name, mat, collection, 0.025)


# Facade depth: layered window bays make the background civic hall read as occupied architecture.
for side, x in enumerate((-2.45, 2.45)):
    for level in range(4):
        z = 0.95 + level * 0.92
        box(f"cc_facade_{side}_bay_{level}", (x, 4.56, z), (0.54, 0.10, 0.52), glass, bevel=0.025)
        for fin in (-0.36, 0.36):
            box(f"cc_facade_{side}_mullion_{level}_{fin}", (x + fin * 0.42, 4.47, z), (0.07, 0.18, 0.64), dark, bevel=0.02)
    for level in range(3):
        box(f"cc_facade_{side}_ledge_{level}", (x, 4.50, 1.45 + level * 1.1), (1.08, 0.18, 0.10), stone, bevel=0.025)
    arc(f"cc_civic_arch_{side}", (x, 4.32), 0.72, math.radians(200), math.radians(340), 4.72, 0.09, stone)

# Curved civic canopies frame the two lateral destinations without entering the circulation annulus.
for side, x in enumerate((-6.35, 6.35)):
    for level in (1.25, 2.05, 2.85):
        torus(f"cc_lateral_terrace_ring_{side}_{level}", (x, -2.8, level), 1.05, 0.07, dark, rotate=(math.pi / 2, 0, 0))
    arc(f"cc_lateral_canopy_{side}", (x, -2.8), 1.45, math.radians(205), math.radians(335), 3.25, 0.11, stone)
    for y in (-3.65, -2.8, -1.95):
        box(f"cc_lateral_screen_{side}_{y}", (x + (-0.82 if side == 0 else 0.82), y, 1.8), (0.08, 0.42, 2.6), glass, bevel=0.02)

# Hero civic core gets a restrained layered crown and four structural ribs.
for i, angle in enumerate((0, math.pi / 2, math.pi, 3 * math.pi / 2)):
    x, y = 1.12 * math.cos(angle), 1.12 * math.sin(angle)
    box(f"cc_core_structural_rib_{i}", (x, y, 2.0), (0.10, 0.22, 2.2), cyan, bevel=0.025).rotation_euler.z = angle
torus("cc_core_crown_outer", (0, 0, 2.48), 1.20, 0.075, cyan)
torus("cc_core_crown_inner", (0, 0, 2.62), 0.82, 0.05, dark)

# Foreground human-scale furnishing and planting make the player zone legible at runtime scale.
for i, x in enumerate((-2.7, 2.7)):
    for j in range(3):
        y = -5.38 + j * 0.38
        box(f"cc_foreground_seat_{i}_{j}", (x, y, 0.68 + 0.12 * i), (1.0, 0.16, 0.18), stone, bevel=0.04)
    for j in range(3):
        cylinder(f"cc_foreground_lamp_{i}_{j}", (x + (-0.52 if j % 2 else 0.52), -5.45 + j * 0.35, 1.25), 0.045, 1.35, cyan, vertices=12)
        torus(f"cc_foreground_lamp_ring_{i}_{j}", (x + (-0.52 if j % 2 else 0.52), -5.45 + j * 0.35, 1.94), 0.13, 0.025, cyan)

# Terraced platform edging and a visible suspended underside make the island read as floating.
for level, radius in enumerate((7.35, 6.85, 6.25)):
    torus(f"cc_floating_edge_ring_{level}", (0, 0, -0.05 - level * 0.02), radius, 0.07, dark, scale=(1, 0.72, 1))
for side in (-1, 1):
    for y in (-3.0, -1.5, 0.0, 1.5, 3.0):
        x = side * (7.25 - abs(y) * 0.10)
        box(f"cc_floating_edge_brace_{side}_{y}", (x, y, 0.0), (0.18, 0.12, 0.16), cyan, bevel=0.025)

# Low perimeter planters supply a second material/shape language without blocking protected routes.
for i, (x, y) in enumerate(((-6.45, -4.0), (6.45, -4.0), (-6.95, 3.55), (6.95, 3.55))):
    box(f"cc_landscape_planter_{i}", (x, y, 0.28), (0.9, 0.72, 0.42), dark, bevel=0.10)
    for j in range(3):
        cylinder(f"cc_landscape_stem_{i}_{j}", (x - 0.25 + j * 0.25, y, 0.85), 0.045, 0.8, dark, vertices=12)
        torus(f"cc_landscape_leaf_{i}_{j}", (x - 0.25 + j * 0.25, y, 1.30), 0.16, 0.04, teal, rotate=(math.pi / 2, 0, 0))


def render_view(name, location, target):
    camera = bpy.data.objects["PREVIEW_RUNTIME"]
    camera.location = location
    aim_object_at(camera, target)
    camera.data.angle = math.radians(52)
    scene = bpy.context.scene
    scene.camera = camera
    scene.render.engine = select_eevee_engine(scene.render)
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(PREVIEWS / name)
    bpy.ops.render.render(write_still=True)


# Keep the approved runtime camera as the saved source state after review renders.
render_view("detail-runtime.png", (0, -21, 10), (0, 0, 1.6))
render_view("detail-top.png", (0, 0, 22), (0, 0, 0))
render_view("detail-side.png", (21, 0, 7), (0, 0, 1.6))
camera = bpy.data.objects["PREVIEW_RUNTIME"]
camera.location = (0, -21, 10)
aim_object_at(camera, (0, 0, 1.6))
camera.data.angle = math.radians(52)
bpy.context.scene.camera = camera
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
print("DETAIL COMMAND CENTER: saved source and canonical review renders")
