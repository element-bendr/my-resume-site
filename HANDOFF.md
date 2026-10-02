# Current Handoff

## Goal

Upgrade the certified Portfolio World from primitive-heavy Three.js scenery to genuinely authored Blender scenery exported as GLB while preserving all certified runtime, content, accessibility and fallback contracts.

## Phase

BLENDER_ART_STAGE_02_AUTHORED_PASS_01_VISUAL_BLOCKED

## Execution mode

implementation

## Authority / location

- repository: `element-bendr/my-resume-site`
- canonical branch: `main`
- protected baseline: `5f4de7ace37bfd843ef13f035a3b16ddb61f28d7`
- implementation branch: `feat/blender-world-art-pipeline`
- draft PR: #21
- primary workflow: `workflow/active/portfolio-world-blender-art`
- active stage: `02-command-center-integration`
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

The six production GLB binaries are now vendored and hash-verified from GitHub bake run `36815004861` using Blender 4.5.14 LTS. `npm run art:verify` and basic GLB parsing pass; exact sizes and hashes are recorded in `docs/portfolio-world/BLENDER-STAGE-01-VALIDATION.md`. Terra independently reviewed documentation head `f27c70b6e45e0770e12789fde523f023ffdd8d85` against artifact candidate `94f0ec5976778d8abf80bad35aa7a743526cf1d7` and returned PASS with no required fixes. Exact-head GitHub bake/CI run `36816140894` passed against pushed candidate `549d35838ddc4d048af83102001a9be00d3e66f1`. Stage 01 is formally certified by state commit `eca3c550d1af9c55cf13ec76b19f723d976b9d1e`.

Stage 02 is active. User-authorized local Blender is 5.2.1 LTS; the repository target remains 4.5.14. The first editable Command Center pass is saved and structurally validates: 260 meshes, 97,580 triangles, six materials, zero textures. Its canonical preview is visually FAIL: floor-dominant, hero cropped, skyline outside the frame, foreground Timeline lintel obscuring the plaza. The exact prescribed camera is unchanged. Evidence and exact next action are in `art/blender/command-center/visual-pass-01.md`. No export or runtime integration occurred.

The prior certified `main` production deployment/smoke record remains pending. This Blender branch does not silently resolve or overwrite that release state.

## Validation evidence

- GitHub bake run `36815004861`: Blender 4.5.14 LTS artifact PASS.
- exact-head GitHub bake/CI run `36816140894`: PASS against `549d35838ddc4d048af83102001a9be00d3e66f1`.
- Stage 02 activation: PASS via existing workflow tooling; active stage is `02-command-center-integration`.
- `npm run art:cc:bootstrap`: PASS under Blender 5.2.1 after compatibility fix.
- Existing validation entrypoint via the single MCP Blender instance: PASS, zero errors; triangles exceed preferred range but remain below the soft ceiling.
- Existing preview entrypoint via the same MCP Blender instance: PASS; canonical 1600 x 900 image saved. Visual outcome: FAIL / camera-composition conflict.
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

- Stage 01 certification state is recorded at `eca3c550d1af9c55cf13ec76b19f723d976b9d1e`.
- Stage 02 is active; authored source and preview are saved. Visual acceptance is blocked.
- Stage 02 now has a frozen authored-scene specification, local bootstrap/validator/render/export scripts, and a local Codex handoff.
- Visual review must resolve canonical-camera framing before a second authored pass. Browser/runtime integration has not begun.

## Canonical decisions

- Blender 4.5 LTS remains the repository's canonical 3D asset/export target. User-authorized Blender 5.2.1 LTS is the current local execution environment; this is a tooling-version deviation only and does not change target contracts.
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

Stage 01 certification remains intact; Stage 02 is not certified.

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

Current blocker: the first canonical preview fails visual composition. The fixed camera excludes skyline/horizon and crops the hero. A separately recorded camera/composition decision is needed before another pass. Structural validation is green; no export or runtime integration is claimed.

## Next atomic action

1. independently review the saved first-pass source and `previews/runtime.png`;
2. record a decision resolving camera-visible composition while preserving protected runtime authority;
3. reconsider foreground portal silhouette and massing before a second pass;
4. retain the single MCP Blender instance and open bead `stage05-integration-dsq`;
5. export/integrate only after explicit visual PASS.

## Minimum resume context

1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-blender-art/CONTEXT.md`
5. `workflow/active/portfolio-world-blender-art/01-art-contract-bake-CONTEXT.md`
6. `decisions/2026-10-01-blender-world-art.md`
7. `docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
8. `docs/portfolio-world/COMMAND-CENTER-BLENDER-SPEC.md`
9. `art/blender/command-center/LOCAL-CODEX-HANDOFF.md`
