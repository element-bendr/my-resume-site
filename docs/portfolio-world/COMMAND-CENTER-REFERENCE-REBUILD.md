# Command Center reference-driven rebuild

Status: active visual reset

## Primary visual authority

`art/blender/command-center/references/command-center-concept.png`

Secondary atmosphere references:

- `portfolio-world-concept-board.png`
- `portfolio-world-neon-hub.png`

The primary reference wins when the references disagree.

## Builder

Executor profile: `blender-codex-reference`

Codex owns the creative reconstruction loop. Existing Blender geometry is disposable unless it represents a protected runtime anchor.

## Preserve only

- player spawn;
- five bridge entrances / district connection interfaces;
- Ask interaction clearance;
- walkable topology and circulation clearances;
- world scale;
- runtime camera operating envelope;
- React-owned interaction semantics.

## Rebuild freely

- building silhouettes;
- facade systems;
- roof forms;
- civic core;
- terraces;
- platform perimeter and underside;
- structural framing;
- landscaping and vegetation;
- furniture and human-scale props;
- materials;
- glass/metal/stone separation;
- lighting fixtures and visual lighting hierarchy.

## Visual rule

Do not recreate the target primarily from cubes, cylinders, toruses, repeated slabs or emissive trim over primitive massing.

The runtime-camera render must visibly match the primary reference in:

1. silhouette;
2. foreground/midground/background depth;
3. curved versus orthogonal architectural language;
4. vertical hierarchy;
5. facade depth;
6. material separation;
7. landscape distribution;
8. human-scale detail;
9. floating-platform edge/underside;
10. lighting hierarchy.

Codex should render, compare against the reference, identify the largest visual mismatch, correct it, and repeat. Do not spend iterations polishing small details while major silhouette/depth mismatches remain.

## Required outputs

- editable `art/blender/command-center/source/command-center.blend`;
- `previews/reference-runtime.png`;
- `previews/reference-top.png`;
- `previews/reference-side.png`;
- `reference-rebuild-review.md`;
- `reference-rebuild-validation.json`;
- optional scoped Blender authoring scripts under `tools/blender/reference_*.py`.

## Stop gate

Stop at:

`REFERENCE REBUILD — HUMAN VISUAL REVIEW READY`

No GLB export.
No React integration.
No browser certification.
No deployment.

The user must visually approve the runtime-camera render before Terra final review and any subsequent export task.
