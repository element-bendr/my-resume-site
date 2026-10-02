from __future__ import annotations

import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from command_center_common import (
    PREVIEW_CAMERA,
    PREVIEW_PATH,
    PREVIEW_RESOLUTION,
)


def main() -> None:
    camera = bpy.data.objects.get(PREVIEW_CAMERA)
    if camera is None or camera.type != "CAMERA":
        raise RuntimeError(f"missing canonical preview camera {PREVIEW_CAMERA}")

    PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    scene.camera = camera
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = PREVIEW_RESOLUTION[0]
    scene.render.resolution_y = PREVIEW_RESOLUTION[1]
    scene.render.resolution_percentage = 100
    scene.render.filepath = str(PREVIEW_PATH)
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = 0.0

    bpy.ops.render.render(write_still=True)
    print(f"COMMAND CENTER PREVIEW: PASS output={PREVIEW_PATH}")


if __name__ == "__main__":
    main()