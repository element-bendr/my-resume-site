# Production Command Center export contract

Status: active after a certified detailed-authoring candidate exists.

## Source authority

Production export must start from an exact ICM candidate ref whose durable result and independent review both PASS and agree on the candidate SHA.

For the current export:

- source task: `command-center-detail-002`
- source ref: `refs/heads/icm/candidates/command-center-detail-002`
- source SHA: `0a5e3ea05ad1b1e5d2986a786bb7a33c531565c1`

The export task must not first merge this candidate into `feat/blender-world-art-pipeline`.

## Executor behavior

The export executor is intentionally non-creative. It must:

1. verify HEAD equals the task base SHA;
2. verify `art/blender/command-center/validation.json` remains PASS;
3. run the existing deterministic Blender export:
   `npm run art:cc:export`;
4. run `node scripts/check-blender-assets.mjs`;
5. record export evidence containing source SHA, GLB SHA-256, byte size, and validation outcomes;
6. commit only the production GLB and declared export evidence;
7. leave the candidate worktree clean.

No geometry, material, camera, preview, Blender source, React, routing, runtime integration, workflow contract, or deployment change is authorized.

## Validation

Runner validation is read-only:

- `blender-assets` -> `node scripts/check-blender-assets.mjs`
- `icm-stage` -> `python3 scripts/workflow_status.py --strict`

The existing GLB checker verifies GLB v2 structure, declared length, JSON chunk presence, per-file 900 KiB ceiling, and total staged GLB budget.

## Independent review

Terra reviews exact candidate state, not an uncommitted export directory.

PASS requires:

- source candidate SHA matches the certified detailed candidate;
- only authorized export paths changed;
- GLB validation passes;
- export evidence hash/size agrees with the committed GLB;
- protected Blender source and website/runtime state remain unchanged;
- no required fixes remain.

A passing export does not authorize React integration, merge, or deployment.
