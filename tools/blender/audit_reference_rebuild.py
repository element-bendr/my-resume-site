from __future__ import annotations

import json
import sys

import bpy

LEGACY_PREFIXES = (
    "cc_facade_",
    "cc_civic_arch_",
    "cc_lateral_",
    "cc_core_structural_",
    "cc_core_crown_",
    "cc_foreground_",
    "cc_floating_",
    "cc_landscape_",
    "cc_terrace_",
    "cc_underside_",
)

collection = bpy.data.collections.get("EXPORT_COMMAND_CENTER")
if collection is None:
    raise SystemExit("REFERENCE REBUILD AUDIT: FAIL missing EXPORT_COMMAND_CENTER")

meshes = [obj for obj in collection.all_objects if obj.type == "MESH"]
if not meshes:
    raise SystemExit("REFERENCE REBUILD AUDIT: FAIL no export meshes")

legacy = sorted(obj.name for obj in meshes if obj.name.startswith(LEGACY_PREFIXES))
if legacy:
    raise SystemExit(
        "REFERENCE REBUILD AUDIT: FAIL legacy detail geometry still present: "
        + ", ".join(legacy[:20])
    )

simple = 0
substantial = 0
for obj in meshes:
    verts = len(obj.data.vertices)
    polys = len(obj.data.polygons)
    if verts <= 24 and polys <= 24:
        simple += 1
    if verts >= 96 or polys >= 96:
        substantial += 1

simple_ratio = simple / len(meshes)
if simple_ratio > 0.55:
    raise SystemExit(
        f"REFERENCE REBUILD AUDIT: FAIL primitive-like mesh ratio {simple_ratio:.2%} > 55%"
    )
if substantial < 8:
    raise SystemExit(
        f"REFERENCE REBUILD AUDIT: FAIL only {substantial} substantial meshes; expected >= 8"
    )

result = {
    "status": "PASS",
    "mesh_objects": len(meshes),
    "primitive_like_meshes": simple,
    "primitive_like_ratio": round(simple_ratio, 4),
    "substantial_meshes": substantial,
    "legacy_prefix_matches": 0,
}
print("REFERENCE_REBUILD_GEOMETRY=" + json.dumps(result, sort_keys=True))
