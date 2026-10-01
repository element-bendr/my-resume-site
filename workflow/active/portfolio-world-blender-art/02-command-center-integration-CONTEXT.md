# Stage 02 — Command Center authored source and integration

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: ChatGPT coordinator
- execution mode: implementation
- parallel-write boundaries: Command Center Blender source/art, scoped R3F visual integration, validation evidence only

## Inputs

- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified Stage 01 procedural Blender/export pipeline proof
- approved concept/reference image
- `src/world/CommandCenter.tsx`
- `src/world/world-config.ts`

## Objective

Produce an editable, genuinely authored Command Center Blender source that materially approaches the approved visual reference, export it to GLB, visually approve it, and only then integrate it as the first production-camera slice without changing interaction authority.

## In Scope

- create or obtain editable Command Center `.blend` source;
- model/refine architecture beyond primitive procedural geometry;
- establish authored materials/UVs as needed;
- render review images from the same Blender source;
- export the approved Command Center GLB;
- load the approved GLB through the typed art boundary;
- preserve Ask Terminal, movement target, camera and interaction behavior.

## Out of Scope

- treating Stage 01 procedural GLBs as automatically approved final art;
- claiming a local Blender connection when none occurred;
- unrelated portfolio content changes;
- changes to production deployment/domain;
- changes to Ask authority;
- changes to movement/topology semantics;
- rollout of the other five districts.

## Dependencies

- certified Stage 01 pipeline proof;
- approved concept/reference image;
- editable Blender source for the Command Center;
- `src/world/CommandCenter.tsx`;
- `src/world/world-config.ts`.

## Process

1. Preserve the Stage 01 procedural GLB as pipeline evidence only.
2. Create/obtain editable Command Center Blender source.
3. Render desktop/isometric review images directly from that source.
4. Compare the render against the approved visual reference.
5. Reject/block if the asset still reads as primitive/blockout quality.
6. Export the approved source to GLB and run structural/budget validation.
7. Integrate only the Command Center GLB.
8. Validate movement, click/tap, Ask, route teardown, mobile and performance.
9. Record exact source hash, GLB hash and visual evidence.

## Outputs

- editable Command Center Blender source;
- rendered visual-review images;
- approved Command Center GLB;
- Command Center runtime integration;
- desktop/mobile screenshots;
- interaction/performance evidence.

## Acceptance

- an editable Blender source exists and is traceable to the exported GLB;
- the Command Center materially approaches the approved concept rather than the Stage 01 blockout;
- visual review is explicitly PASS before runtime replacement;
- movement/click/tap/Ask behavior passes;
- no route teardown regression;
- asset and JS budgets pass.

## Verify

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
- certified movement, topology, camera, route and accessibility behavior.

## Known closed decisions

- Stage 01 GLBs prove Blender generation/export, not final art quality;
- interaction coordinates remain React-owned;
- authored Blender source is required for final visual acceptance;
- primitive fallback remains available until this stage passes.

## Stop Conditions

- no editable Blender source is available;
- the asset remains visually blockout/primitive quality;
- two materially similar implementation attempts fail;
- an asset requires relaxing a certified behavior or safety boundary;
- required validation cannot be performed;
- unexpected unrelated diff appears.
