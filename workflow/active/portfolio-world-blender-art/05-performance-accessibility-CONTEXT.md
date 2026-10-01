# Stage 05 — Performance and accessibility certification

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: ChatGPT coordinator
- execution mode: implementation
- parallel-write boundaries: portfolio world Blender/art files and scoped world visual integration only

## Inputs

- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified Stage 04 visual candidate
- docs/portfolio-world/BLENDER-QA-CERTIFICATION.md

## Objective

Prove the complete Blender world remains performant, accessible and failure-tolerant across the production viewport/capability matrix.

## In Scope

- 360/390/768/1024/1440 browser matrix
- movement/fast-travel/station regression
- route exit/focus/reduced-motion checks
- forced WebGL/asset failure checks
- transfer/decode/frame-time review

## Out of Scope

- unrelated portfolio content changes
- changes to production deployment/domain
- changes to Ask authority
- changes to movement/topology semantics unless separately approved

## Dependencies

- certified Stage 04 visual candidate
- docs/portfolio-world/BLENDER-QA-CERTIFICATION.md

## Process

1. Inspect the exact branch diff and relevant certified runtime files.
2. Execute only the visual/art work owned by this stage.
3. Validate the smallest relevant asset/runtime gate after each meaningful change.
4. Preserve fallback behavior while a replacement is unproven.
5. Record exact evidence and candidate state.
6. Stop rather than weakening a certified behavior to make art fit.

## Outputs

- docs/portfolio-world/BLENDER-VALIDATION.md
- exact candidate evidence
- independent review findings

## Acceptance

- all repository gates pass
- all browser/runtime gates pass
- no material performance regression remains unresolved
- fallback and conventional routes remain complete

## Verify

- `${x}`
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

- visual polish cannot override accessibility/fallback
- performance exceptions require evidence and explicit decision

## Stop Conditions

- two materially similar implementation attempts fail;
- an asset requires relaxing a certified behavior or safety boundary;
- required validation cannot be performed;
- unexpected unrelated diff appears.
