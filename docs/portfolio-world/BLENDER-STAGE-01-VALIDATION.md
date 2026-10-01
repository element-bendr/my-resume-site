# Blender Stage 01 Validation

date: 2026-10-01  
workflow: `portfolio-world-blender-art`  
stage: `01-art-contract-bake`  
status: **BLOCKED_PENDING_REAL_BLENDER_BAKE**  
branch: `feat/blender-world-art-pipeline`  
PR: #21

## Objective

Produce and verify the first real six-zone GLB asset set from the committed Blender 4.5 LTS generator.

## Structural evidence already present

- accepted Blender/runtime authority decision;
- complete asset/export contract;
- authoring guide;
- visual/runtime certification contract;
- deterministic six-zone Blender generator;
- explicit runtime zone anchors;
- GLB byte-budget verifier;
- pinned Blender 4.5.14 Actions bake definition;
- dedicated managed ICM workflow;
- root context/handoff updated for the Blender phase;
- `main` remains untouched.

## Coordinate correction

The generator now converts intended runtime coordinates through the Blender/glTF axis boundary instead of assuming Blender depth maps directly to runtime Z.

Authoring tuple semantics:

```text
(world X, world Z, world Y)
        ↓
Blender (X, -Z, Y-up-as-Blender-Z)
        ↓
glTF exporter Y-up conversion
        ↓
runtime (X, Y, Z)
```

This correction must be included in the first bake candidate.

## Required asset outputs

Not yet produced:

- `public/world/art/command-center.glb`
- `public/world/art/build-lab.glb`
- `public/world/art/automation-lab.glb`
- `public/world/art/client-street.glb`
- `public/world/art/timeline.glb`
- `public/world/art/hobby-district.glb`

## Required Stage 01 evidence

Pending:

- Blender version output;
- successful generator exit;
- six expected files;
- per-file bytes;
- total bytes;
- SHA-256 for every GLB;
- `npm run art:verify` PASS;
- basic loader/parse proof;
- exact candidate commit.

## Current execution blocker

The current isolated shell cannot resolve external hosts, so Blender cannot be downloaded/executed locally.

The repository-side workflow exists, but connector-authored commits do not self-dispatch GitHub Actions. No successful bake run exists yet.

This is an execution-environment blocker only. It is **not** evidence that the generator or assets pass.

## Promotion state

Stage 01 remains active.

Do not:

- certify Stage 01;
- integrate Command Center GLB;
- remove the certified primitive scenery;
- make PR #21 ready for merge;
- claim production visual improvement.

## Next gate

Run the pinned Blender 4.5.14 bake from an execution environment that can execute Blender, then record the required hashes/sizes/verification result here.
