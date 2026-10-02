from __future__ import annotations

import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from command_center_common import EXPORT_COLLECTION, GLB_PATH
from validate_command_center_source import validate


def main() -> None:
    report = validate(write_report=True)
    if report["status"] != "PASS":
        raise RuntimeError(
            "Command Center source validation failed; refusing production export"
        )

    collection = bpy.data.collections.get(EXPORT_COLLECTION)
    if collection is None:
        raise RuntimeError(f"missing {EXPORT_COLLECTION}")

    bpy.ops.object.select_all(action="DESELECT")
    export_objects = list(collection.all_objects)
    if not export_objects:
        raise RuntimeError(f"{EXPORT_COLLECTION} is empty")

    for obj in export_objects:
        obj.select_set(True)

    GLB_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(GLB_PATH),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_cameras=False,
        export_lights=False,
        export_extras=False,
        export_animations=False,
    )
    print(f"COMMAND CENTER EXPORT: PASS output={GLB_PATH}")


if __name__ == "__main__":
    main()