# Command Center neural-seed rebuild

## Decision

The two-attempt procedural reference rebuild is closed.

The next approach begins with generated 3D mesh geometry from the approved reference image rather than procedural Blender primitives.

Preferred generator: Microsoft TRELLIS.2 image-to-3D.

Primary input:

`art/blender/command-center/references/command-center-concept.png`

## Workflow

1. Verify the exact reference image and SHA-256.
2. Attempt a whole-scene image-to-3D generation.
3. Render/inspect the generated mesh from the runtime camera.
4. If the whole-scene seed is unusable, split the SAME reference into visually coherent architectural clusters and generate multiple mesh seeds.
5. Import the best seed(s) into Blender.
6. Preserve generated mesh form where it matches the reference.
7. Clean topology, repair materials, remove hidden/noisy geometry, align scale/origin, and fit around protected runtime anchors.
8. Render from the runtime camera.
9. Stop at HUMAN VISUAL REVIEW READY.

## Protected runtime anchors

- spawn;
- five bridge interfaces;
- Ask clearance;
- walkable topology;
- world scale;
- runtime camera operating envelope.

## Forbidden

- procedural plate/perimeter rebuild;
- primitive blocks as primary architecture;
- silently reverting to Massing V2;
- modifying topology to fit generated art;
- React/runtime changes;
- production GLB replacement;
- deployment.

## Seed provenance

Record for every generated mesh:

- generator/model and version/commit where available;
- source reference SHA-256;
- generation settings;
- whether full-scene or cropped/segmented input;
- output GLB SHA-256 and bytes;
- license/provenance notes;
- cleanup steps performed in Blender.

## Output

- neural seed GLB(s) under `art/blender/command-center/neural-seed/`;
- Blender source assembled from seed geometry;
- runtime/top/side review renders;
- `neural-seed-review.md`;
- `neural-seed-provenance.json`.

No production GLB export until human visual approval.
