# Blender world-art pipeline

This directory owns the authored visual layer for the gamified portfolio.

## Boundary

Blender owns scenery, forms, bevels, material intent and authored props.

React / React Three Fiber continues to own movement, walkable topology, collision constraints,
camera behavior, interaction stations, routing, accessibility, lazy loading and the no-WebGL fallback.
The generated GLBs must never become the source of truth for gameplay coordinates.

## Canonical documentation

Read:

- `../../decisions/2026-10-01-blender-world-art.md`
- `../../docs/portfolio-world/BLENDER-ART-PIPELINE.md`
- `../../docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
- `../../docs/portfolio-world/BLENDER-AUTHORING-GUIDE.md`
- `../../docs/portfolio-world/BLENDER-QA-CERTIFICATION.md`

## Pinned authoring target

Blender 4.5 LTS. The initial repository lane is authored against Blender 4.5.14.

## Coordinate convention

Generator location tuples mean:

```text
(world X, world Z, world Y)
```

`world_to_blender()` converts that into Blender's Z-up coordinates before glTF export.
Do not repair axis/origin mistakes by changing React topology coordinates.

## Generate

From the repository root:

```bash
blender -b --python tools/blender/generate_world.py
npm run art:verify
```

Outputs:

```text
public/world/art/
  command-center.glb
  build-lab.glb
  automation-lab.glb
  client-street.glb
  timeline.glb
  hobby-district.glb
```

The first pass deliberately creates geometry and PBR material intent without image textures.
That gives us curved/beveled authored forms immediately while keeping download size small.
Texture baking, KTX2/Basis compression, LODs and environment lighting belong to later managed stages.

## Integration rule

Do not replace the certified React collision/navigation meshes with GLB geometry.
Render GLB scenery above the existing topology layer and remove old decorative primitives one district
at a time only after visual QA and performance budgets pass.

## CI behavior

The asset workflow is intentionally narrow. It can be started manually and contains a branch/PR path
trigger for this isolated Stage 01 lane. It downloads the pinned Blender build, bakes the six GLBs,
runs the budget gate, records SHA-256 hashes and uploads the outputs as a short-lived artifact.

A workflow definition existing in the repository is not evidence that a bake ran. Stage 01 validation
must record an actual successful execution.
