# Stage 02 — Command Center integration

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: ChatGPT coordinator
- execution mode: implementation
- parallel-write boundaries: portfolio world Blender/art files and scoped world visual integration only

## Inputs

- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified Stage 01 art bake
- src/world/CommandCenter.tsx
- src/world/world-config.ts

## Objective

Integrate Blender scenery into the Command Center as the first production-camera vertical slice without changing interaction authority.

## In Scope

- load Command Center GLB through the typed art boundary
- place it at the certified zone anchor
- remove/disable only redundant decorative primitives
- preserve Ask Terminal, movement target and lighting behavior until replacements are proven

## Out of Scope

- unrelated portfolio content changes
- changes to production deployment/domain
- changes to Ask authority
- changes to movement/topology semantics unless separately approved

## Dependencies

- certified Stage 01 art bake
- src/world/CommandCenter.tsx
- src/world/world-config.ts

## Process

1. Inspect the exact branch diff and relevant certified runtime files.
2. Execute only the visual/art work owned by this stage.
3. Validate the smallest relevant asset/runtime gate after each meaningful change.
4. Preserve fallback behavior while a replacement is unproven.
5. Record exact evidence and candidate state.
6. Stop rather than weakening a certified behavior to make art fit.

## Outputs

- Command Center runtime integration
- desktop/mobile screenshots
- interaction/performance evidence

## Acceptance

- Command Center visibly uses authored scenery
- movement/click/tap/Ask behavior passes
- no route teardown regression
- asset and JS budgets pass

## Verify

- `${x}`
- `${x}`
- `${x}`
- `${x}`
- `${x}`

## Protected State

- `main`
- production deployment/domain
- verified resume/project content
- interaction station identities/content
- certified movement, topology, camera, route and accessibility behavior

## Known closed decisions

- interaction coordinates remain React-owned
- primitive fallback remains available until this stage passes

## Stop Conditions

- two materially similar implementation attempts fail;
- an asset requires relaxing a certified behavior or safety boundary;
- required validation cannot be performed;
- unexpected unrelated diff appears.
