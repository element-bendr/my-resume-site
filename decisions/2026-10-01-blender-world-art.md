# Decision: Blender-authored scenery is the canonical 3D art pipeline

date: 2026-10-01
status: accepted
owners: portfolio-world-blender-art
supersedes: none
superseded_by: none

## Context

The certified Portfolio World runtime proves navigation, interaction, routing, accessibility, fallback behavior and Cloudflare delivery, but its scenery is intentionally primitive-heavy. The visual target is materially richer than what should be maintained as hand-authored React Three Fiber boxes, cylinders and toruses.

The art upgrade must improve visual fidelity without invalidating the certified interaction contracts or turning Blender geometry into a second gameplay/navigation authority.

## Decision

Blender 4.5 LTS is the canonical authoring tool for district scenery and static visual props.

The browser runtime remains React + TypeScript + React Three Fiber / Three.js. Blender exports one GLB per district. GLBs are visual scenery only.

React remains authoritative for:

- world topology and walkable bounds;
- movement and click/tap targets;
- interaction station coordinates;
- camera behavior;
- route behavior;
- content authority;
- accessibility;
- fallback behavior.

Blender remains authoritative for:

- authored geometry;
- bevels and curved forms;
- scene-local prop placement;
- material intent;
- UVs and baked texture inputs;
- LOD source geometry when introduced.

No interaction coordinate may be derived from an exported mesh at runtime.

The generated concept/reference art is art direction, not executable geometry and not a factual content source.

## Consequences

- Visual scenery can evolve without rewriting movement/navigation code.
- Each district can be lazy-loaded and replaced independently.
- A failed or missing GLB must not make Resume, Projects, Ask or Contact unreachable.
- Art files and textures are subject to explicit transfer, decode and frame-time budgets.
- Blender source must be reproducible through committed scripts or committed source files; opaque one-off binary editing is insufficient for a production dependency.
- Runtime lighting/post-processing changes remain separate from the geometry-authoring lane.
- The existing certified primitive scenery remains the rollback/fallback reference until each GLB lane passes visual and performance certification.

## Validation / evidence

- Certified runtime baseline: `main` at `5f4de7ace37bfd843ef13f035a3b16ddb61f28d7`.
- Existing primitive-heavy scenery is located in `src/world/CommandCenter.tsx` and `src/world/districts/*`.
- Blender pipeline implementation is isolated in draft PR #21 on `feat/blender-world-art-pipeline`.
- Asset generation is defined by `tools/blender/generate_world.py`.
- Runtime loading boundary is `src/world/art/BlenderDistrictArt.tsx`.

## Revisit when

- a different DCC/asset pipeline produces materially better output with equal or better reproducibility;
- GLB delivery/decode cost cannot meet the production budgets;
- runtime-generated procedural geometry proves measurably superior for a specific asset class;
- WebGPU adoption changes the asset/material contract.
