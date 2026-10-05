# Command Center authored pass 01

## Outcome

Structural validation: PASS. Canonical preview rendering: PASS.
Visual acceptance: FAIL / blocked on camera-composition conflict.
No production export or runtime integration is authorized by this record.

The editable source contains a segmented plaza, layered geodesic core,
perimeter towers with recessed glazing/louvers, five overhead portal directions,
Ask framing, eight planted trees, benches, lamps and kiosks. All protected
guide objects remain present. This is a saved first review checkpoint, not
completion of Stage 02.

## Execution

- Local environment: Blender 5.2.1 LTS, user-authorized existing MCP instance.
- `tools/blender/author_command_center.py` was loaded in the existing MCP
  session; `plaza`, `core`, `architecture` and `props` authored native editable
  meshes. No second Blender process was launched.
- Existing `validate_command_center_source.validate()` entrypoint ran inside
  that same session: PASS, zero errors, one preferred-range warning.
- Existing `render_command_center_preview.main()` entrypoint ran inside
  that same session: PASS, 1600 x 900, Eevee, AgX, exposure 0.
- `python3 scripts/workflow_check.py`: PASS.
- `python3 scripts/workflow_status.py --strict`: PASS; Stage 02 active.
- No production GLB was generated or replaced.

The npm validation/preview wrappers were not launched because they start a
second Blender process. Their existing Python entrypoints were used directly
through MCP to respect the user's one-instance requirement.

## Metrics and hashes

- Export mesh objects: 260.
- Triangles: 97,580 (above preferred 90,000, below soft ceiling 120,000).
- Materials: 6: CC_Cyan, CC_DarkGlass, CC_Graphite, CC_Gunmetal,
  CC_SoftMetal, CC_Teal.
- Image textures: 0.
- Source: `source/command-center.blend`, SHA-256
  `4e9c4e2ef71a3bdd5518a424e3f2923ba17ab53ba5212bc5ab733060d477b24b`.
- Preview: `previews/runtime.png`, SHA-256
  `911f50443413b461a948a94b63368c9b99ac0243bef6c7741f17da7c4168939f`.
- Validation report: `validation.json`, SHA-256
  `3348a87c4589dde23bbef06002c3f10c727e95bbb79abcc161dcea905b421902`.
- GLB bytes/hash: not applicable; export gate not reached.
- Parent commit before this checkpoint: `9fb6bbbadf9027c8d152a2683157e4f8203452e4`.
  The Git commit containing this record identifies this checkpoint exactly.

## Visual findings

The canonical preview is floor-dominant. The hero's upper geometry is cropped,
the back skyline is outside the image, and the foreground Timeline lintel
occludes the plaza. Vegetation and panel detail are visible, but the image does
not materially approach the reference composition. A structural PASS does not
resolve these visual failures.

The camera was checked against the prescribed values: position
`(0, -10.2, 6.4)`, target `(0, -3.5, 1)`, horizontal FOV 52 degrees.
It remains unchanged. This downward view cannot frame the rear vertical
massing/horizon requested by the visual brief with the current geometry.
Changing camera behavior is outside this lane's authority.

The current validator also limits all exported underside geometry to
`Z >= -0.20` and accepts only seven material names. The pass respects those
limits; floating-world depth and richer landscape color remain limited.
The first pass uses provisional neutral/foliage shader values within that
vocabulary and still needs palette review against the art specification.

## Exact next action

Independent review of this saved source and canonical image, followed by a
recorded decision resolving the fixed-camera framing conflict. Reconsider the
foreground portal silhouette and camera-visible massing before a second art
pass. Do not export, integrate React, or start district production until an
explicit visual PASS is obtained. Keep the bead open.
