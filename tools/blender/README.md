# Blender world-art pipeline

This directory owns the authored visual layer for the gamified portfolio.

## Boundary

Blender owns scenery, forms, bevels, material intent and authored props.

React / React Three Fiber continues to own movement, walkable topology, collision constraints,
camera behavior, interaction stations, routing, accessibility, lazy loading and the no-WebGL fallback.
The generated GLBs must never become the source of truth for gameplay coordinates.

## Pinned authoring target

Blender 4.5 LTS. The initial repository lane is authored against Blender 4.5.14.

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
That gives us curved/bevelled authored forms immediately while keeping download size small.
Texture baking, KTX2/Basis compression, LODs and environment lighting belong to the next art lane.

## Integration rule

Do not replace the certified React collision/navigation meshes with GLB geometry.
Render GLB scenery above the existing topology layer and remove old decorative primitives one district
at a time only after visual QA and performance budgets pass.
