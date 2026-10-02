from __future__ import annotations

import math
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMAND_CENTER_ROOT = REPO_ROOT / "art" / "blender" / "command-center"
SOURCE_PATH = COMMAND_CENTER_ROOT / "source" / "command-center.blend"
PREVIEW_PATH = COMMAND_CENTER_ROOT / "previews" / "runtime.png"
VALIDATION_PATH = COMMAND_CENTER_ROOT / "validation.json"
GLB_PATH = REPO_ROOT / "public" / "world" / "art" / "command-center.glb"

EXPORT_COLLECTION = "EXPORT_COMMAND_CENTER"
GUIDE_COLLECTION = "GUIDES_DO_NOT_EXPORT"
PREVIEW_COLLECTION = "PREVIEW_DO_NOT_EXPORT"
PREVIEW_CAMERA = "PREVIEW_RUNTIME"

WORLD_BOUNDS = (-8.0, 8.0, -6.0, 6.0)
HEIGHT_CLEAR_MIN = 0.35
HEIGHT_CLEAR_MAX = 2.15
OVERHEAD_MIN = 2.25
CIRCULATION_INNER = 1.75
CIRCULATION_OUTER = 4.70
MAX_AUTHORED_HEIGHT = 5.20

KEEP_CLEAR_WORLD = {
    "client_entrance": (-8.0, -5.8, -1.6, 1.6),
    "hobby_entrance": (5.8, 8.0, -1.6, 1.6),
    "timeline_entrance": (-1.6, 1.6, 3.8, 6.0),
    "build_entrance": (-6.5, -3.5, -6.0, -3.8),
    "automation_entrance": (3.5, 6.5, -6.0, -3.8),
    "spawn": (-1.30, 1.30, 2.20, 4.80),
    "ask_approach": (2.70, 5.10, -3.50, -0.50),
}

RUNTIME_POINTS = {
    "spawn": (0.0, 3.5, 0.0),
    "ask_station": (4.35, -2.70, 0.0),
    "ask_interaction": (3.55, -1.45, 0.0),
    "portal_client": (-8.0, 0.0, 0.0),
    "portal_hobby": (8.0, 0.0, 0.0),
    "portal_timeline": (0.0, 6.0, 0.0),
    "portal_build": (-5.0, -6.0, 0.0),
    "portal_automation": (5.0, -6.0, 0.0),
}

REQUIRED_EXACT_OBJECTS = {
    "cc_core_dais",
    "cc_ask_frame",
    "cc_arch_client",
    "cc_arch_hobby",
    "cc_arch_timeline",
    "cc_arch_build",
    "cc_arch_automation",
}

REQUIRED_PREFIX_MINIMUMS = {
    "cc_floor_": 1,
    "cc_core_": 3,
    "cc_shell_": 3,
    "cc_pylon_": 3,
    "cc_portal_": 5,
    "cc_console_": 3,
}

ALLOWED_MATERIALS = {
    "CC_Graphite",
    "CC_Gunmetal",
    "CC_SoftMetal",
    "CC_Cyan",
    "CC_Teal",
    "CC_Violet",
    "CC_DarkGlass",
}

PREFERRED_TRIANGLES_MIN = 35_000
PREFERRED_TRIANGLES_MAX = 90_000
TRIANGLES_SOFT_CEILING = 120_000
MATERIAL_LIMIT = 10

PREVIEW_CAMERA_POSITION = (0.0, -21.0, 10.0)
PREVIEW_TARGET = (0.0, 0.0, 1.6)
PREVIEW_FOV_DEGREES = 52.0
PREVIEW_RESOLUTION = (1600, 900)


def select_eevee_engine(render_settings) -> str:
    available = {
        item.identifier
        for item in render_settings.bl_rna.properties["engine"].enum_items
    }
    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        if engine in available:
            return engine
    raise RuntimeError(
        "Blender does not provide a supported Eevee engine; "
        f"available engines: {sorted(available)}"
    )


def world_to_blender(x: float, z: float, y: float = 0.0) -> tuple[float, float, float]:
    return (x, -z, y)


def world_rect_to_blender(bounds: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    min_x, max_x, min_z, max_z = bounds
    return (min_x, max_x, -max_z, -min_z)


def aim_object_at(obj, target: tuple[float, float, float]) -> None:
    from mathutils import Vector

    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def fov_radians() -> float:
    return math.radians(PREVIEW_FOV_DEGREES)
