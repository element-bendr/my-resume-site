# Stage 04 — Lighting, materials and post-processing

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: ChatGPT coordinator
- execution mode: implementation
- parallel-write boundaries: portfolio world Blender/art files and scoped world visual integration only

## Inputs

- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified six-zone Blender integration
- docs/portfolio-world/RENDERING-TECHNOLOGY.md
- docs/portfolio-world/ASSET-BUDGET.md

## Objective

Raise the integrated authored geometry toward the approved concept-art quality using bounded materials, lighting, textures and post-processing.

## In Scope

- runtime environment/key/rim lighting
- restrained bloom/ambient occlusion/tone mapping where measured
- texture baking and KTX2/Basis path where justified
- quality tiers and LODs only from measurements

## Out of Scope

- unrelated portfolio content changes
- changes to production deployment/domain
- changes to Ask authority
- changes to movement/topology semantics unless separately approved

## Dependencies

- certified six-zone Blender integration
- docs/portfolio-world/RENDERING-TECHNOLOGY.md
- docs/portfolio-world/ASSET-BUDGET.md

## Process

1. Inspect the exact branch diff and relevant certified runtime files.
2. Execute only the visual/art work owned by this stage.
3. Validate the smallest relevant asset/runtime gate after each meaningful change.
4. Preserve fallback behavior while a replacement is unproven.
5. Record exact evidence and candidate state.
6. Stop rather than weakening a certified behavior to make art fit.

## Outputs

- lighting/material implementation
- compressed texture outputs if introduced
- quality-tier configuration
- visual/performance evidence

## Acceptance

- visual fidelity improves without unreadable bloom/fog
- mobile remains usable
- reduced-effects path exists where needed
- asset budgets remain within approved thresholds

## Verify

- `${x}`
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

- WebGL 2 remains production renderer
- lights are runtime-owned by default
- effects degrade gracefully

## Stop Conditions

- two materially similar implementation attempts fail;
- an asset requires relaxing a certified behavior or safety boundary;
- required validation cannot be performed;
- unexpected unrelated diff appears.
