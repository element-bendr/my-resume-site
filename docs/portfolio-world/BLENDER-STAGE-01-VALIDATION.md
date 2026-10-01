# Blender Stage 01 Validation

date: 2026-10-01  
workflow: `portfolio-world-blender-art`  
stage: `01-art-contract-bake`  
status: **BAKE_VALIDATED_PENDING_STAGE_CERTIFICATION**
branch: `feat/blender-world-art-pipeline`
PR: #21

## Exact bake evidence

- GitHub bake run: `36815004861`
- Blender artifact: `/tmp/pr21-blender-artifact`
- Blender version: 4.5.14 LTS
- artifact SHA/size verification: PASS against `public/world/art/SHA256SUMS.txt`
- exact candidate commit: pending this evidence commit; runtime integration remains disabled

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

All six outputs are present under `public/world/art/` and match the independent
artifact hashes:

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| `command-center.glb` | 432,336 | `31d750fc9bf8da5fb6cb28d3fc47b651ac874565731bec5a813086c842e1065a` |
| `build-lab.glb` | 311,848 | `c04531432535e6b9a480a9a02a2540fdec03a183e774d14f1793a7f9791ae879` |
| `automation-lab.glb` | 400,088 | `784285daac1b576fd1eec2955bc08c9bf24f3d513de234832580d6ace1577d2e` |
| `client-street.glb` | 305,952 | `970010d41b53fbd41e9549da44cb589ea9c374d6327785bfce69d270b643c778` |
| `timeline.glb` | 259,308 | `84cc312d02042292e24bf65e27b3728ee80dd2409a4cac6e1270ad4d41de36b5` |
| `hobby-district.glb` | 231,812 | `8b2139dc7f8e7a777fd3c22181d68b30bd401fdd5ae3b130ef361d0cd7b8dd01` |

Total GLB payload: 1,941,344 bytes (1,895.8 KiB).


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

- Blender 4.5.14 LTS artifact bake: PASS, run `36815004861`;
- six expected files and SHA-256/size checks: PASS;
- `npm run art:verify`: PASS, six files, 1,895.8 KiB total;
- GLB parse proof: PASS; all six files are GLB version 2 with valid JSON chunks
  and parsed node/mesh/material tables;
- runtime integration remains intentionally disabled pending Stage 02.

## Current execution status

The pinned remote bake artifact has been independently hash-checked and copied
without modification. Local structural verification and GLB parse proof pass.
No runtime scenery replacement has been enabled.

## Promotion state

Stage 01 remains active.

Do not:

- certify Stage 01;
- integrate Command Center GLB;
- remove the certified primitive scenery;
- make PR #21 ready for merge;
- claim production visual improvement.

## Next gate

Complete the Stage 01 evidence commit and independent review. Do not activate
Stage 02 or integrate the GLBs into runtime scenery until Stage 01 is formally
certified.
