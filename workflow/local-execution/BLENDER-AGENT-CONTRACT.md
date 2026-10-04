# Blender agent execution contract

Status: active for local configuration

This contract defines the machine-local interface for the real Command Center authoring loop. It does not assume a vendor-specific CLI name.

## Luna executor profile

Profile ID: `blender-luna`

The configured local command receives:

```text
--task-file <path>
```

The task file is the ICM local-runner context envelope. The command runs with the isolated candidate worktree as its current working directory.

The Luna executor must:

1. consume the task plus `icm context --compact` for the declared Stage 02 subject;
2. preserve the accepted Massing V2 composition and preview camera;
3. use Blender/Blender Python to perform detailed authoring;
4. run source validation and render the required detailed evidence before committing;
5. commit every intended candidate change and leave the worktree clean;
6. never push, merge, publish result/review records, change protected refs, or export the production GLB;
7. stop after two materially similar failed repair attempts and surface the upstream cause rather than continuing cosmetic retries.

Required committed candidate evidence:

```text
art/blender/command-center/source/command-center.blend
art/blender/command-center/previews/detail-runtime.png
art/blender/command-center/previews/detail-top.png
art/blender/command-center/previews/detail-side.png
art/blender/command-center/validation.json
art/blender/command-center/detail-review.md
```

## Terra reviewer profile

Profile ID: `blender-terra-review`

The configured local command receives:

```text
--context <review-context.json>
--output <review-decision.json>
```

It runs in a detached worktree at the exact candidate SHA.

The reviewer must not modify the candidate. It compares the three detailed views and committed review evidence against the approved references and Stage 02 acceptance contract.

The decision file must contain exactly:

```json
{
  "verdict": "pass | fix_required | stop",
  "findings": [],
  "required_fixes": [],
  "validation_summary": "..."
}
```

PASS requires no error/blocker findings and no required fixes. The reviewer identity must differ from the executor identity.

## Sol coordinator boundary

Sol does not participate in normal scene/render corrections. Sol acts when:

- task scope or architecture changes;
- protected state must change;
- the same material defect survives two comparable attempts;
- Luna/Terra evidence contradicts;
- the candidate cannot satisfy the frozen Stage 02 acceptance criteria;
- certification/promotion decisions are required.

## Read-only runner validation

The runner does not render or rewrite evidence after the executor commits. It uses:

- `blender-candidate` -> `tools/icm/validate_blender_candidate.py`;
- `icm-stage` -> `python3 scripts/workflow_status.py --strict`.

This keeps the exact candidate SHA stable through validation and independent review.
