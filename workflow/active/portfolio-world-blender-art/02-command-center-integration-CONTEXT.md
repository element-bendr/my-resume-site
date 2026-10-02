# Stage 02 — Command Center authored source and integration

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: local Codex + ChatGPT coordinator
- execution mode: implementation
- parallel-write boundaries: Command Center Blender source/art, scoped R3F visual integration, validation evidence only

## Inputs

- accepted camera composition: `decisions/2026-10-02-command-center-camera-composition.md`; preview `(0,-21,10)` toward `(0,0,1.6)`, FOV 52; runtime adoption deferred to integration.
- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified Stage 01 procedural Blender/export pipeline proof
- `docs/portfolio-world/COMMAND-CENTER-BLENDER-SPEC.md`
- `docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
- `art/blender/command-center/LOCAL-CODEX-HANDOFF.md`
- `src/world/world-topology.ts`
- `src/world/world-config.ts`
- `src/world/WorldEntry.tsx`
- `src/world/CommandCenter.tsx`

## Objective

Create the first genuinely authored Command Center Blender source locally, prove it visually against the frozen authoring specification, export its production GLB, and integrate only that approved asset without changing certified interaction authority.

## In Scope

- activate Stage 02 through existing ICM tooling before implementation;
- bootstrap a local guide-only `.blend` using certified runtime constraints;
- create/edit `art/blender/command-center/source/command-center.blend`;
- author architecture beyond primitive procedural geometry;
- validate bounds, clearances, naming, triangle/material budgets and export collection;
- render `art/blender/command-center/previews/runtime.png` from the runtime-matched camera;
- visually review and refine before export;
- export the approved Command Center GLB;
- load only the approved GLB through the typed art boundary;
- preserve Ask Terminal, movement target, camera and interaction behavior.

## Out of Scope

- treating Stage 01 procedural GLBs as automatically approved final art;
- moving guide/protected zones to make scenery fit;
- claiming local Blender work before local Blender actually runs;
- unrelated portfolio content changes;
- changes to production deployment/domain;
- changes to Ask authority;
- changes to movement/topology semantics;
- rollout of the other five districts.

## Dependencies

- certified Stage 01 pipeline proof;
- frozen Command Center Blender specification;
- certified world topology/config and runtime camera contract;
- Blender 4.5 LTS available locally when execution begins.

## Process

1. Activate Stage 02 using `scripts/workflow_activate.py`.
2. Confirm Blender 4.5 LTS and the isolated branch.
3. Run `npm run art:cc:bootstrap` once to create the guide-only source.
4. Author final art only in `EXPORT_COMMAND_CENTER`.
5. Run `npm run art:cc:validate` during iteration.
6. Run `npm run art:cc:preview` and inspect the runtime-matched render.
7. Reject/block if the scene still reads as primitive/blockout quality.
8. Repeat authoring/preview until visual acceptance is PASS.
9. Run `npm run art:cc:export` only after structural and visual PASS.
10. Run GLB and repository validation.
11. Integrate only the approved Command Center GLB.
12. Validate movement, click/tap, Ask, route teardown, mobile and performance.
13. Record exact source hash, GLB hash, preview and candidate state.

## Outputs

- `art/blender/command-center/source/command-center.blend`
- `art/blender/command-center/previews/runtime.png`
- `art/blender/command-center/validation.json`
- `public/world/art/command-center.glb`
- Command Center runtime integration
- desktop/mobile screenshots
- interaction/performance evidence
- Stage 02 validation/completion record

## Acceptance

- editable Blender source exists and is traceable to the exported GLB;
- source validator passes without weakening protected clearances;
- canonical runtime preview is rendered from the same source;
- the Command Center materially exceeds Stage 01 blockout quality;
- five portal directions, hero core and Ask framing are visually legible;
- visual review is explicitly PASS before runtime replacement;
- movement/click/tap/Ask behavior passes after integration;
- no route teardown regression;
- asset and JS budgets pass.

## Verify

- `python3 scripts/workflow_status.py --strict`
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
- Ask station and interaction point.

## Known closed decisions

- Stage 01 GLBs prove Blender generation/export, not final art quality;
- local `.blend` is the creative source of truth for Stage 02;
- interaction coordinates remain React-owned;
- authored Blender source is required for final visual acceptance;
- primitive fallback remains available until this stage passes;
- runtime integration occurs only after authored visual PASS.

## Stop Conditions

- local Blender 4.5 LTS is unavailable;
- source validation requires weakening a protected runtime constraint;
- the asset remains visually blockout/primitive quality after two materially similar approaches;
- an asset requires changing certified topology to fit;
- required visual/runtime validation cannot be performed;
- unexpected unrelated diff appears.
