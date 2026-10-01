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


## Exporter API verification

Blender 4.5 LTS documentation confirms the production exporter capabilities used by the generator:

- glTF 2.0 / GLB output;
- Selected Objects export;
- Y Up conversion;
- Apply Modifiers;
- Metal/Rough Principled-BSDF material export;
- cameras and punctual lights can be excluded.

Reference:

- <https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html>
- <https://docs.blender.org/api/main/bpy.ops.export_scene.html>

The generator also explicitly disables animation export because these district assets are static scenery.

## Required asset outputs

Not yet produced:

- `public/world/art/command-center.glb`
- `public/world/art/build-lab.glb`
- `public/world/art/automation-lab.glb`
- `public/world/art/client-street.glb`
- `public/world/art/timeline.glb`
- `public/world/art/hobby-district.glb`


## Repository structural audit

Compared with certified base `5f4de7ace37bfd843ef13f035a3b16ddb61f28d7`:

- branch is ahead only; merge base is the certified base;
- changes are limited to Blender/art source, art config/test, scoped documentation/workflow files, the Blender Actions workflow, and two package scripts;
- `src/world/world-topology.ts`: unchanged;
- `src/world/world-config.ts`: unchanged;
- player/camera/movement/interaction components: unchanged;
- Ask implementation/content registry: unchanged;
- `package-lock.json`: unchanged;
- Wrangler/production configuration: unchanged.

Workflow contract audit:

- all six stage contexts contain every required ICM section;
- no unresolved template placeholders are present;
- exactly one stage is active;
- workflow primary is `portfolio-world-blender-art`.

Source-contract hardening:

- GLB file paths and zone anchors are isolated in a pure TypeScript config;
- a Vitest contract test requires exactly one GLB per certified zone and requires each anchor to equal the zone center;
- the GLB verifier checks magic, version 2, declared file length, initial JSON chunk, per-file/total budgets, and SHA-256.

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
