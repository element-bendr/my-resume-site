# Stage 02 — Command Center authored source and integration

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: local Codex + ChatGPT coordinator
- execution mode: implementation
- parallel-write boundaries: Command Center Blender source/art, scoped visual evidence, and only later scoped R3F integration after visual PASS

## Inputs

- accepted camera composition: `decisions/2026-10-02-command-center-camera-composition.md`; preview `(0,-21,10)` toward `(0,0,1.6)`, FOV 52; runtime adoption deferred to integration.
- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified Stage 01 procedural Blender/export pipeline proof
- `docs/portfolio-world/COMMAND-CENTER-BLENDER-SPEC.md`
- `docs/portfolio-world/COMMAND-CENTER-MASSING-V2.md`
- `docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
- `art/blender/command-center/MASSING-V2-HANDOFF.md`
- `src/world/world-topology.ts`
- `src/world/world-config.ts`
- `src/world/WorldEntry.tsx`
- `src/world/CommandCenter.tsx`\n- `decisions/2026-10-04-blender-icm-autonomous-execution.md`\n- `docs/portfolio-world/BLENDER-AUTONOMOUS-EXECUTION.md`

## Objective

Develop the human-approved Massing V2 civic-hub composition into a detailed authored Command Center.

Current phase: **DETAILED_COMMAND_CENTER_AUTHORING_ACTIVE**. Human composition PASS at `dbc8d7c18fdf7b6d6761e79dbcff329f33ccda5f` is recorded in PR #21 comment [5956821330](https://github.com/element-bendr/my-resume-site/pull/21#issuecomment-5956821330). The Massing V2 composition gate is CLOSED; preserve its spatial foundation. Stage 02 remains ACTIVE, not complete/certified.

Detailed authoring is now authorized. Production GLB export remains blocked until a later detailed visual PASS and exact-source validation; React integration requires validated production export. Stage 03, merge and deployment remain blocked.

## Historical failure state

Local authoring evidence supplied by the Stage 02 session:

- camera decision: `79ea3fc`
- second-pass checkpoint: `e948434`
- structural validation: PASS
- scene size: 296 meshes
- triangles: 105,600
- materials: 6
- Terra visual review: FAIL
- failure reason: flat diorama rather than referenced floating civic hub
- evidence path: `/mnt/shared/projects/mixed/Resume-gamified/.worktrees/blender-world-art/art/blender/command-center/visual-pass-02.md`
- mandatory two-attempt stop rule: triggered

No GLB export, React integration, push, merge, deployment, or `main` change occurred from those local attempts.

The user-owned `AGENTS.md` remains protected and must not be changed.

## In Scope

- evolve the approved Massing V2 with curved/terraced civic architecture, facade depth, structural framing, landscape, human-scale detail and floating edge/underside treatment;
- improve foreground player-scale readability and lateral direction cues without moving spawn or changing the approved preview camera;
- render canonical runtime, top/plan, side/elevation and useful oblique views for detailed visual review;
- record source counts, review-only geometry separation, limitations and protected-state proof;
- preserve the two failed authored attempts as evidence;
- create a new massing/composition plan before any further detail work;
- work from the finalized reference images and frozen runtime constraints;
- create a materially different low-cost Massing V2 greybox;
- prove foreground / midground / background depth;
- prove multi-level civic-plaza hierarchy;
- prove floating-platform edge/void and visible horizon;
- prove at least three outward destination directions from the runtime view;
- prove at least one convincing bridge/bridge mouth;
- validate bounds and protected clearances;
- render top, runtime-camera, and side/elevation massing views;
- obtain explicit visual review before detailed authoring resumes.

## Out of Scope

- a third incremental polish pass on the failed scene;
- production materials/textures;
- detailed greebling;
- production GLB export before Massing V2 visual PASS;
- React/R3F integration before Massing V2 visual PASS;
- Stage 03 district rollout;
- moving protected guides/coordinates to make art fit;
- unrelated portfolio content changes;
- production deployment or `main` changes.

## Dependencies

- certified Stage 01 pipeline proof;
- frozen Command Center Blender specification;
- finalized visual references available to the local Blender lane;
- `docs/portfolio-world/COMMAND-CENTER-MASSING-V2.md`;
- certified topology/config/camera contracts;
- Blender 4.5 LTS available locally.

## Process

Current entry point: Massing V2 human composition gate has PASSED. Preserve the approved source and prior failure evidence; continue at detailed authoring step 11 below, then stop for independent detailed visual review. Exact-source validation must prove export collection, clearances, circulation, bounds, naming, budgets and `PREVIEW_DO_NOT_EXPORT` separation before eventual production export.

1. Read the prior FAIL evidence and do not continue the failed silhouette incrementally.
2. Read `COMMAND-CENTER-MASSING-V2.md`.
3. Preserve current failed source/checkpoints as evidence.
4. Create a materially different greybox massing plan.
5. Keep the Massing V2 greybox cheap:
   - preferred 20k–40k triangles;
   - soft ceiling 50k;
   - 1–3 simple review materials;
   - no production textures required.
6. Render:
   - `massing-v2-top.png`
   - `massing-v2-runtime.png`
   - `massing-v2-side.png`
7. Run protected-clearance/source validation.
8. Write `massing-v2-review.md` comparing the greybox with the finalized references.
9. Stop at `MASSING V2 GREYBOX — REVIEW READY`.
10. Obtain explicit visual PASS.
11. Only after PASS, resume detailed authored modeling.
12. Only after later authored visual PASS, export the production GLB.
13. Only after production GLB validation, integrate into React and run runtime tests.

## Execution model — graph-bounded visual loop

For detailed authoring, substantial work should run through the pinned graph-backed ICM runtime. Luna is the bounded Blender executor; Terra supplies visual critique and detached independent review; Sol remains coordinator/architecture escalation rather than participating in every render correction.

A bounded authoring task may iterate scene -> render -> critique -> correction while its objective and protected-state assumptions remain unchanged. Each iteration must preserve compact evidence. If the same material defect survives two materially similar attempts, stop and correct the upstream scene rule, reference interpretation, or task/stage contract before resuming.

The formal reviewer remains independent of the executor. Production GLB export, React integration and promotion remain governed by the existing Stage 02 gates.

## Outputs

Immediate required outputs:

- `docs/portfolio-world/COMMAND-CENTER-MASSING-V2.md`
- `art/blender/command-center/MASSING-V2-HANDOFF.md`
- `art/blender/command-center/previews/massing-v2-top.png`
- `art/blender/command-center/previews/massing-v2-runtime.png`
- `art/blender/command-center/previews/massing-v2-side.png`
- `art/blender/command-center/massing-v2-review.md`
- source validation evidence for the Massing V2 candidate

Current detailed-authoring outputs:

- final authored `command-center.blend`
- canonical final runtime preview
- top/plan and side/elevation detailed previews
- concise detailed review document with exact source validation, counts, review-only separation and known limitations

Deferred until detailed visual PASS and source/export validation:

- production `command-center.glb`
- React Command Center integration
- runtime/browser evidence

## Acceptance

Massing V2 visual PASS requires:

- scene reads as a floating civic hub before detail/material polish;
- clear foreground / midground / background separation;
- visible sky/horizon;
- multi-level plaza composition;
- meaningful vertical skyline;
- at least three outward destination directions visible from runtime view;
- at least one convincing bridge/bridge mouth;
- hero core proportionate to the overall architecture;
- human-scale cues visible;
- no large empty floor area dominating the frame;
- protected movement, entrance, spawn, and Ask clearances intact.

Stage 02 final acceptance still additionally requires:

- editable Blender source traceable to production GLB;
- final visual PASS;
- GLB structural/budget PASS;
- movement/click/tap/Ask behavior PASS after integration;
- no route teardown regression;
- asset/JS budgets PASS.

## Verify

For the current Massing V2 gate:

- `python3 scripts/workflow_status.py --strict`\n- after canonical graph initialization: `python3 scripts/icm.py --json validate`\n- bounded runtime context: `python3 scripts/icm.py --json context --compact --subject stage.portfolio-world-blender-art-02-command-center-integration`
- `npm run art:cc:validate` when compatible with the active source
- inspect `massing-v2-top.png`
- inspect `massing-v2-runtime.png`
- inspect `massing-v2-side.png`
- review `massing-v2-review.md`

Do **not** run `npm run art:cc:export` as part of the current gate.

After later visual PASS, the production verification sequence remains:

- `npm run art:cc:validate`
- `npm run art:cc:preview`
- `npm run art:cc:export`
- `npm run art:verify`
- `npm run typecheck`
- `npm test`
- `npm run build`
- `npm run verify:world-assets`

## Protected State

- `main`;
- production deployment/domain;
- verified resume/project content;
- interaction station identities/content;
- certified movement, topology, camera, route and accessibility behavior;
- five bridge entrances;
- player spawn;
- Ask station and interaction point;
- user-owned `AGENTS.md`.

## Known closed decisions

- human Massing V2 composition PASS: `dbc8d7c18fdf7b6d6761e79dbcff329f33ccda5f`, PR comment `5956821330`;
- the approved composition may not be redesigned without a new blocking visual finding;
- Stage 01 GLBs prove Blender generation/export, not final art quality;
- local `.blend` is the creative source of truth for Stage 02;
- interaction coordinates remain React-owned;
- two materially similar failed visual attempts trigger a mandatory composition reset;
- a third incremental pass on the failed massing is prohibited;
- Massing V2 must pass in greybox form before detailed modeling resumes;
- production GLB export and runtime integration remain blocked until visual PASS.

## Stop Conditions

- Massing V2 still reads as a flat diorama;
- source validation requires weakening a protected runtime constraint;
- a proposed fix mainly adds detail/materials without materially changing massing;
- an asset requires changing certified topology to fit;
- required visual validation cannot be performed;
- unexpected unrelated diff appears;
- user-owned `AGENTS.md` is modified.
