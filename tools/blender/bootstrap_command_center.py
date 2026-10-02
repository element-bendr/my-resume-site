from __future__ import annotations

import os
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from command_center_common import (
    EXPORT_COLLECTION,
    GUIDE_COLLECTION,
    KEEP_CLEAR_WORLD,
    PREVIEW_CAMERA,
    PREVIEW_CAMERA_POSITION,
    PREVIEW_COLLECTION,
    PREVIEW_FOV_DEGREES,
    PREVIEW_RESOLUTION,
    PREVIEW_TARGET,
    RUNTIME_POINTS,
    SOURCE_PATH,
    WORLD_BOUNDS,
    aim_object_at,
    world_rect_to_blender,
    world_to_blender,
)


def reset_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in list(bpy.data.collections):
        bpy.data.collections.remove(collection)


def new_collection(name: str):
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    return collection


def move_to_collection(obj, collection) -> None:
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def guide_box(collection, name: str, world_bounds, z_min=0.35, z_max=2.15):
    min_x, max_x, min_y, max_y = world_rect_to_blender(world_bounds)
    bpy.ops.mesh.primitive_cube_add(
        location=((min_x + max_x) / 2, (min_y + max_y) / 2, (z_min + z_max) / 2)
    )
    obj = bpy.context.object
    obj.name = f"GUIDE_{name}"
    obj.dimensions = (max_x - min_x, max_y - min_y, z_max - z_min)
    obj.display_type = "WIRE"
    obj.show_in_front = True
    obj.hide_render = True
    obj["portfolio_guide"] = True
    move_to_collection(obj, collection)
    return obj


def guide_circle(collection, name: str, radius: float):
    bpy.ops.mesh.primitive_circle_add(vertices=96, radius=radius, fill_type="NOTHING", location=(0, 0, 0.025))
    obj = bpy.context.object
    obj.name = f"GUIDE_{name}"
    obj.display_type = "WIRE"
    obj.show_in_front = True
    obj.hide_render = True
    obj["portfolio_guide"] = True
    move_to_collection(obj, collection)
    return obj


def guide_empty(collection, name: str, runtime_point):
    x, z, y = runtime_point
    obj = bpy.data.objects.new(f"GUIDE_{name}", None)
    obj.location = world_to_blender(x, z, y)
    obj.empty_display_type = "CIRCLE"
    obj.empty_display_size = 0.35
    obj.show_in_front = True
    obj.hide_render = True
    obj["portfolio_guide"] = True
    collection.objects.link(obj)
    return obj


def add_preview_camera(collection):
    camera_data = bpy.data.cameras.new(PREVIEW_CAMERA)
    camera_data.angle = __import__("math").radians(PREVIEW_FOV_DEGREES)
    camera = bpy.data.objects.new(PREVIEW_CAMERA, camera_data)
    camera.location = PREVIEW_CAMERA_POSITION
    collection.objects.link(camera)
    aim_object_at(camera, PREVIEW_TARGET)
    bpy.context.scene.camera = camera
    return camera


def add_preview_light(collection, name, light_type, location, color, energy):
    data = bpy.data.lights.new(name=name, type=light_type)
    data.color = color
    data.energy = energy
    obj = bpy.data.objects.new(name, data)
    obj.location = location
    collection.objects.link(obj)
    if light_type == "SUN":
        aim_object_at(obj, (0, 0, 0.8))
    return obj


def configure_scene():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = PREVIEW_RESOLUTION[0]
    scene.render.resolution_y = PREVIEW_RESOLUTION[1]
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = 0.0

    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.0015, 0.0033, 0.0070, 1.0)
        bg.inputs["Strength"].default_value = 0.22

    scene["portfolio_world_stage"] = "02-command-center-integration"
    scene["authoring_spec"] = "docs/portfolio-world/COMMAND-CENTER-BLENDER-SPEC.md"
    scene["runtime_anchor"] = "[0,0,0]"


def main() -> None:
    force = os.environ.get("FORCE_COMMAND_CENTER_BOOTSTRAP") == "1"
    if SOURCE_PATH.exists() and not force:
        raise RuntimeError(
            f"{SOURCE_PATH} already exists. Refusing to overwrite authored work. "
            "Set FORCE_COMMAND_CENTER_BOOTSTRAP=1 only if destruction is intentional."
        )

    SOURCE_PATH.parent.mkdir(parents=True, exist_ok=True)

    reset_scene()
    configure_scene()

    new_collection(EXPORT_COLLECTION)
    guides = new_collection(GUIDE_COLLECTION)
    preview = new_collection(PREVIEW_COLLECTION)

    min_x, max_x, min_z, max_z = WORLD_BOUNDS
    guide_box(guides, "ZONE_BOUNDS", (min_x, max_x, min_z, max_z), z_min=-0.05, z_max=0.05)

    for name, bounds in KEEP_CLEAR_WORLD.items():
        guide_box(guides, f"KEEP_CLEAR_{name.upper()}", bounds)

    guide_circle(guides, "CIRCULATION_INNER", 1.75)
    guide_circle(guides, "CIRCULATION_OUTER", 4.70)

    for name, point in RUNTIME_POINTS.items():
        guide_empty(guides, name.upper(), point)

    add_preview_camera(preview)
    add_preview_light(preview, "PREVIEW_Key", "SUN", (5, -5, 9), (0.80, 0.92, 1.0), 2.0)
    add_preview_light(preview, "PREVIEW_Cyan", "POINT", (0, 1, 4), (0.345, 0.843, 1.0), 900)
    add_preview_light(preview, "PREVIEW_Teal", "POINT", (5, 3, 2.5), (0.459, 0.949, 0.784), 500)

    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE_PATH))
    print(f"COMMAND CENTER BOOTSTRAP: PASS source={SOURCE_PATH}")


if __name__ == "__main__":
    main()