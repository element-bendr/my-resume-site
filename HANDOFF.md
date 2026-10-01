# Current Handoff

## Goal

Upgrade the certified Portfolio World from primitive-heavy Three.js scenery to Blender-authored GLB scenery while preserving all certified runtime, content, accessibility and fallback contracts.

## Phase

BLENDER_ART_STAGE_01_ACTIVE

## Execution mode

implementation

## Authority / location

- repository: `element-bendr/my-resume-site`
- canonical branch: `main`
- protected baseline: `5f4de7ace37bfd843ef13f035a3b16ddb61f28d7`
- implementation branch: `feat/blender-world-art-pipeline`
- draft PR: #21
- primary workflow: `workflow/active/portfolio-world-blender-art`
- active stage: `01-art-contract-bake`
- template: ICM 2.1.0 @ `90322a2441539f24eafdbd2c8a36bc6392192af4`

## Current state

The certified React/R3F world is already on `main`. The visual upgrade is isolated from it.

Implemented on the Blender branch:

- deterministic Blender source generator for six zones;
- typed R3F GLB loader boundary;
- manual-only pinned Blender asset workflow;
- GLB byte-budget gate;
- accepted Blender/runtime authority decision;
- Blender asset contract;
- authoring guide;
- visual/runtime certification checklist;
- dedicated six-stage ICM workflow.

The six production GLB binaries have **not** yet been generated or certified. Runtime scenery replacement has **not** begun. Therefore Stage 01 is still active and PR #21 remains draft.

The prior certified `main` production deployment/smoke record remains pending. This Blender branch does not silently resolve or overwrite that release state.

## Canonical decisions

- Blender 4.5 LTS is the canonical authored scenery pipeline for this upgrade.
- GLBs are visual scenery only.
- React remains authoritative for topology, movement, station positions, camera, routes, content, accessibility and fallback.
- WebGL 2 remains the production renderer.
- conventional HTML remains first-class and complete for essential portfolio access.
- one GLB is produced per world zone.
- production lights remain runtime-owned by default.
- assets are integrated and certified incrementally, starting with Command Center.
- no uncertified art reaches `main` or production.

## Documentation map

- architecture decision: `decisions/2026-10-01-blender-world-art.md`
- high-level pipeline: `docs/portfolio-world/BLENDER-ART-PIPELINE.md`
- hard asset interface: `docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
- modeling/export workflow: `docs/portfolio-world/BLENDER-AUTHORING-GUIDE.md`
- visual/runtime gates: `docs/portfolio-world/BLENDER-QA-CERTIFICATION.md`
- global transfer budgets: `docs/portfolio-world/ASSET-BUDGET.md`
- renderer policy: `docs/portfolio-world/RENDERING-TECHNOLOGY.md`

## Validation

No Stage 01 certification exists yet.

Current proof is structural only:

- source and contracts are committed on the isolated branch;
- all managed stage contracts pass required-section/placeholder checks;
- pure config tests lock GLB names and art anchors to the certified six-zone topology;
- protected runtime/content/deployment files are absent from the branch diff;
- the GLB verifier now validates binary GLB structure, budgets and SHA-256;
- `main` has not been modified;
- binary GLB output has not yet been produced;
- no real Blender bake has run yet;
- full repository/browser validation is intentionally deferred until an actual asset candidate exists.

Do not describe the Blender world as complete, integrated, or production-ready yet.

## Protected-state status

Expected intact:

- `main`;
- production deployment/domain;
- content and Ask contracts;
- topology/movement/camera behavior;
- interaction station data;
- historical workflow evidence.

## Blockers

No architectural blocker.

Immediate technical gate: normalize intended runtime X/Y/Z placement through Blender Z-up → glTF Y-up export, then produce the first real six-GLB bake and measure it.

## Next atomic action

1. finalize coordinate conversion in `tools/blender/generate_world.py`;
2. bake all six GLBs with Blender 4.5.14;
3. run `npm run art:verify`;
4. record hashes/sizes and Stage 01 evidence;
5. only then begin Command Center runtime integration.

## Minimum resume context

1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-blender-art/CONTEXT.md`
5. `workflow/active/portfolio-world-blender-art/01-art-contract-bake-CONTEXT.md`
6. `decisions/2026-10-01-blender-world-art.md`
7. `docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
