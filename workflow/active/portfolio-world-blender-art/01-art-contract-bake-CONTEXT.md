# Stage 01 — Art contract and baseline bake

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: ChatGPT coordinator
- execution mode: implementation
- parallel-write boundaries: portfolio world Blender/art files and scoped world visual integration only

## Inputs

- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified main baseline 5f4de7ace37bfd843ef13f035a3b16ddb61f28d7
- decisions/2026-10-01-blender-world-art.md
- docs/portfolio-world/ASSET-BUDGET.md

## Objective

Produce a reproducible, bounded six-zone Blender asset set and freeze the source/export/runtime interface before any production scenery replacement.

## In Scope

- finalize Blender source and axis/origin rules
- generate six GLBs
- verify byte budgets and basic parse/load behavior
- keep runtime visual replacement disabled until the bake is evidenced

## Out of Scope

- unrelated portfolio content changes
- changes to production deployment/domain
- changes to Ask authority
- changes to movement/topology semantics unless separately approved

## Dependencies

- certified main baseline 5f4de7ace37bfd843ef13f035a3b16ddb61f28d7
- decisions/2026-10-01-blender-world-art.md
- docs/portfolio-world/ASSET-BUDGET.md

## Process

1. Inspect the exact branch diff and relevant certified runtime files.
2. Execute only the visual/art work owned by this stage.
3. Validate the smallest relevant asset/runtime gate after each meaningful change.
4. Preserve fallback behavior while a replacement is unproven.
5. Record exact evidence and candidate state.
6. Stop rather than weakening a certified behavior to make art fit.

## Outputs

- tools/blender/generate_world.py
- public/world/art/*.glb
- docs/portfolio-world/BLENDER-ASSET-CONTRACT.md
- asset-bake evidence

## Acceptance

- all six expected GLBs exist
- each file is within the stage budget
- total GLB payload is within budget
- source and export rules are documented
- no certified runtime behavior changed

## Verify

- `npm run art:verify`
- `npm run typecheck`
- `npm test`
- `npm run verify:offline`
- `npm run build`
- `npm run verify:assets`
- `npm run verify:world-assets`
- `npm run verify:ask-disclosure`
- `npm run verify:world-ask`

## Protected State

- `main`
- production deployment/domain
- verified resume/project content
- interaction station identities/content
- certified movement, topology, camera, route and accessibility behavior

## Known closed decisions

- GLBs are scenery only
- Blender 4.5 LTS is the authoring target

## Stop Conditions

- two materially similar implementation attempts fail;
- an asset requires relaxing a certified behavior or safety boundary;
- required validation cannot be performed;
- unexpected unrelated diff appears.
