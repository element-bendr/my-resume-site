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

The six production GLB binaries are now vendored and hash-verified from GitHub bake run `36815004861` using Blender 4.5.14 LTS. `npm run art:verify` and basic GLB parsing pass; exact sizes and hashes are recorded in `docs/portfolio-world/BLENDER-STAGE-01-VALIDATION.md`. Terra independently reviewed documentation head `f27c70b6e45e0770e12789fde523f023ffdd8d85` against artifact candidate `94f0ec5976778d8abf80bad35aa7a743526cf1d7` and returned PASS with no required fixes. Runtime scenery replacement has **not** begun. Stage 01 remains active pending remote bake/CI confirmation and formal certification; PR #21 is not yet ready to merge.

The prior certified `main` production deployment/smoke record remains pending. This Blender branch does not silently resolve or overwrite that release state.

## Validation evidence

- GitHub bake run `36815004861`: Blender 4.5.14 LTS artifact PASS.
- Six GLB SHA-256/size checks and `npm run art:verify`: PASS.
- Basic GLB version/JSON/node/mesh/material parse proof: PASS.
- Full inherited repository gates are rerunning for the exact evidence candidate.
- Detailed sizes, hashes, and stage evidence: `docs/portfolio-world/BLENDER-STAGE-01-VALIDATION.md`.

## Protected state

- `main`: unchanged.
- production/deployment: unchanged.
- runtime scenery integration: not started.
- movement, topology, camera, routes, Ask, content, dependencies: unchanged.

## Stale / uncertain state

- Stage 01 is not formally certified yet.
- Stage 02 remains pending and inactive.
- Browser/runtime visual acceptance is deferred until the Stage 01 artifact is independently reviewed and certified.

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
- six binary GLB outputs are present under `public/world/art/`;
- bake artifact and SHA-256 verification pass;
- basic GLB loader/parse proof passes;
- Terra independent Stage 01 review: PASS; no required fixes;
- runtime/browser scenery validation is intentionally deferred until Stage 02.

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

Immediate technical gate: push PR #21 at reviewed head `f27c70b6e45e0770e12789fde523f023ffdd8d85`, confirm GitHub bake/CI against that exact head, then formally certify Stage 01 before any runtime scenery integration.

## Next atomic action

1. push PR #21 exact head `f27c70b6e45e0770e12789fde523f023ffdd8d85`;
2. confirm GitHub bake/CI against that exact head and formally certify Stage 01;
3. only then activate Stage 02 Command Center runtime integration.

## Minimum resume context

1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-blender-art/CONTEXT.md`
5. `workflow/active/portfolio-world-blender-art/01-art-contract-bake-CONTEXT.md`
6. `decisions/2026-10-01-blender-world-art.md`
7. `docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
