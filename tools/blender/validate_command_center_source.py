from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from command_center_common import (
    ALLOWED_MATERIALS,
    CIRCULATION_INNER,
    CIRCULATION_OUTER,
    EXPORT_COLLECTION,
    GUIDE_COLLECTION,
    HEIGHT_CLEAR_MAX,
    HEIGHT_CLEAR_MIN,
    KEEP_CLEAR_WORLD,
    MATERIAL_LIMIT,
    MAX_AUTHORED_HEIGHT,
    OVERHEAD_MIN,
    PREFERRED_TRIANGLES_MAX,
    PREFERRED_TRIANGLES_MIN,
    PREVIEW_CAMERA,
    PREVIEW_COLLECTION,
    REQUIRED_EXACT_OBJECTS,
    REQUIRED_PREFIX_MINIMUMS,
    TRIANGLES_SOFT_CEILING,
    VALIDATION_PATH,
    WORLD_BOUNDS,
    world_rect_to_blender,
)


def object_bounds(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return {
        "min_x": min(p.x for p in points),
        "max_x": max(p.x for p in points),
        "min_y": min(p.y for p in points),
        "max_y": max(p.y for p in points),
        "min_z": min(p.z for p in points),
        "max_z": max(p.z for p in points),
    }


def rects_intersect(a, b):
    return not (
        a["max_x"] <= b["min_x"]
        or a["min_x"] >= b["max_x"]
        or a["max_y"] <= b["min_y"]
        or a["min_y"] >= b["max_y"]
    )


def nearest_radius(bounds):
    if bounds["min_x"] <= 0 <= bounds["max_x"]:
        x = 0.0
    else:
        x = min(abs(bounds["min_x"]), abs(bounds["max_x"]))
    if bounds["min_y"] <= 0 <= bounds["max_y"]:
        y = 0.0
    else:
        y = min(abs(bounds["min_y"]), abs(bounds["max_y"]))
    return math.hypot(x, y)


def farthest_radius(bounds):
    return max(
        math.hypot(x, y)
        for x in (bounds["min_x"], bounds["max_x"])
        for y in (bounds["min_y"], bounds["max_y"])
    )


def validate(write_report=True):
    errors = []
    warnings = []
    metrics = {}

    for name in (EXPORT_COLLECTION, GUIDE_COLLECTION, PREVIEW_COLLECTION):
        if bpy.data.collections.get(name) is None:
            errors.append(f"missing required collection {name}")

    export = bpy.data.collections.get(EXPORT_COLLECTION)
    if export is None:
        report = {"status": "FAIL", "errors": errors, "warnings": warnings, "metrics": metrics}
        return report

    objects = list(export.all_objects)
    meshes = [obj for obj in objects if obj.type == "MESH"]

    if any(obj.type in {"CAMERA", "LIGHT"} for obj in objects):
        errors.append("EXPORT_COMMAND_CENTER must not contain cameras or lights")

    names = {obj.name for obj in objects}
    for required in sorted(REQUIRED_EXACT_OBJECTS):
        if required not in names:
            errors.append(f"missing required authored object {required}")

    for prefix, minimum in REQUIRED_PREFIX_MINIMUMS.items():
        count = sum(1 for name in names if name.startswith(prefix))
        if count < minimum:
            errors.append(f"{prefix} requires at least {minimum} objects; found {count}")

    for obj in meshes:
        if not obj.name.startswith("cc_"):
            errors.append(f"export mesh {obj.name} must use cc_ naming")

    total_triangles = 0
    materials = set()
    for obj in meshes:
        mesh = obj.data
        mesh.calc_loop_triangles()
        total_triangles += len(mesh.loop_triangles)
        for slot in obj.material_slots:
            if slot.material:
                materials.add(slot.material.name)
        if any(scale <= 0 for scale in obj.scale):
            errors.append(f"{obj.name} has zero/negative scale")
        if any(abs(scale - 1.0) > 0.001 for scale in obj.scale):
            warnings.append(f"{obj.name} has unapplied scale {tuple(round(v, 4) for v in obj.scale)}")

    metrics["mesh_objects"] = len(meshes)
    metrics["triangles"] = total_triangles
    metrics["materials"] = sorted(materials)
    metrics["material_count"] = len(materials)

    if not meshes:
        errors.append("EXPORT_COMMAND_CENTER contains no mesh objects")
    if total_triangles > TRIANGLES_SOFT_CEILING:
        errors.append(
            f"triangle count {total_triangles} exceeds soft ceiling {TRIANGLES_SOFT_CEILING}"
        )
    elif total_triangles < PREFERRED_TRIANGLES_MIN:
        warnings.append(
            f"triangle count {total_triangles} is below preferred authored range "
            f"{PREFERRED_TRIANGLES_MIN}..{PREFERRED_TRIANGLES_MAX}"
        )
    elif total_triangles > PREFERRED_TRIANGLES_MAX:
        warnings.append(
            f"triangle count {total_triangles} is above preferred range "
            f"{PREFERRED_TRIANGLES_MIN}..{PREFERRED_TRIANGLES_MAX}"
        )

    if len(materials) > MATERIAL_LIMIT:
        errors.append(f"material count {len(materials)} exceeds limit {MATERIAL_LIMIT}")
    for name in sorted(materials):
        if name not in ALLOWED_MATERIALS:
            errors.append(f"unapproved production material {name}")

    min_world_x, max_world_x, min_world_z, max_world_z = WORLD_BOUNDS
    min_bl_y = -max_world_z
    max_bl_y = -min_world_z

    keep_clear = {}
    for name, world_bounds in KEEP_CLEAR_WORLD.items():
        min_x, max_x, min_y, max_y = world_rect_to_blender(world_bounds)
        keep_clear[name] = {
            "min_x": min_x,
            "max_x": max_x,
            "min_y": min_y,
            "max_y": max_y,
        }

    for obj in meshes:
        bounds = object_bounds(obj)

        if bounds["min_x"] < min_world_x - 0.10 or bounds["max_x"] > max_world_x + 0.10:
            errors.append(f"{obj.name} exceeds Command Center X bounds")
        if bounds["min_y"] < min_bl_y - 0.10 or bounds["max_y"] > max_bl_y + 0.10:
            errors.append(f"{obj.name} exceeds Command Center depth bounds")
        if bounds["min_z"] < -0.20:
            errors.append(f"{obj.name} extends too far below floor")
        if bounds["max_z"] > MAX_AUTHORED_HEIGHT + 0.05:
            errors.append(f"{obj.name} exceeds max authored height {MAX_AUTHORED_HEIGHT}")

        occupies_player_height = (
            bounds["max_z"] > HEIGHT_CLEAR_MIN
            and bounds["min_z"] < HEIGHT_CLEAR_MAX
        )
        low_floor_detail = bounds["max_z"] <= HEIGHT_CLEAR_MIN
        overhead_only = bounds["min_z"] >= OVERHEAD_MIN

        if not occupies_player_height or low_floor_detail or overhead_only:
            continue

        for region_name, region in keep_clear.items():
            if rects_intersect(bounds, region):
                errors.append(f"{obj.name} intrudes into keep-clear region {region_name}")

        min_r = nearest_radius(bounds)
        max_r = farthest_radius(bounds)
        if min_r < CIRCULATION_OUTER and max_r > CIRCULATION_INNER:
            errors.append(
                f"{obj.name} intrudes into circulation annulus "
                f"{CIRCULATION_INNER}..{CIRCULATION_OUTER}"
            )

    if bpy.data.objects.get(PREVIEW_CAMERA) is None:
        errors.append(f"missing canonical preview camera {PREVIEW_CAMERA}")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "metrics": metrics,
        "source": bpy.data.filepath,
    }

    if write_report:
        VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)
        VALIDATION_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    return report


def main() -> int:
    report = validate(write_report=True)
    print(f"COMMAND CENTER SOURCE: {report['status']}")
    print(json.dumps(report["metrics"], indent=2))
    for warning in report["warnings"]:
        print(f"WARNING: {warning}")
    for error in report["errors"]:
        print(f"ERROR: {error}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())