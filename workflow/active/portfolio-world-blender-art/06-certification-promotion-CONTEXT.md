# Stage 06 — Certification and promotion

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: local Codex + ChatGPT coordinator
- execution mode: certification/promotion
- parallel-write boundaries: certification evidence, handoff/promotion records, merge-only state changes

## Inputs

- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified Stage 05 acceptance candidate
- `docs/portfolio-world/BLENDER-VALIDATION.md`
- `docs/portfolio-world/PROMOTION-RECORD.md`
- exact PR #21 head and review state

## Objective

Certify the exact Blender-world candidate, make PR #21 review-ready, merge only the proven state, and keep production deployment as a separate explicitly evidenced authority transfer.

## In Scope

- final exact-head diff review;
- protected-state audit;
- exact-head repository/browser evidence verification;
- independent final review;
- formal ICM certification;
- PR #21 readiness;
- reviewed merge to `main`;
- promotion record update;
- separate production deploy/smoke only from authenticated Cloudflare authority.

## Out of Scope

- new visual/features/content work;
- unreviewed cleanup/refactors;
- production claims without deploy/smoke evidence;
- direct mutation of `main` outside reviewed merge.

## Process

1. freeze exact Stage 05 candidate;
2. ensure working tree/index are clean except explicitly user-owned uncommitted files such as `AGENTS.md`;
3. run final repository gates against exact candidate;
4. verify Stage 05 browser/performance evidence maps to the same SHA;
5. perform final protected-state diff audit;
6. obtain independent final review;
7. run ICM certification check;
8. formally certify Stage 06 against the exact evidence candidate;
9. update completion/HANDOFF/promotion records;
10. push exact candidate to PR #21;
11. verify PR head equals certified candidate and required checks are green;
12. merge only after review/authority conditions are satisfied;
13. record resulting `main` SHA;
14. treat Cloudflare production deployment as a separate explicit step;
15. after authenticated deploy, record Worker/version/domain/smoke evidence before claiming production updated.

## Outputs

- workflow completion report;
- updated `HANDOFF.md`;
- updated Blender validation/promotion record;
- exact certified candidate SHA;
- PR #21 exact-head record;
- merge commit / resulting `main` SHA;
- separate production deployment/smoke record when executed.

## Acceptance

- exact candidate is green;
- exact candidate has independent review PASS;
- all Stage 05 evidence maps to the certified SHA;
- protected state audit passes;
- formal ICM certification passes;
- PR #21 head exactly matches the certified candidate before merge;
- `main` changes only through reviewed merge;
- production remains explicitly pending until authenticated deploy/smoke evidence exists.

## Verify

Before certification:

```bash
python3 scripts/bootstrap_check.py
python3 scripts/workflow_check.py
python3 scripts/workflow_status.py --strict
python3 scripts/workflow_certify_check.py --workflow portfolio-world-blender-art --stage 06-certification-promotion
npm run verify:offline
npm run typecheck
npm test
npm run build
npm run verify:assets
npm run verify:world-assets
npm run art:verify
npm run verify:ask-disclosure
npm run verify:world-ask
npm run verify:world-zones
```

After independent review and a clean exact candidate:

```bash
python3 scripts/workflow_certify.py \
  --workflow portfolio-world-blender-art \
  --stage 06-certification-promotion \
  --write
```

Then rerun:

```bash
python3 scripts/workflow_status.py --strict
```

PR/merge verification must additionally confirm:

- PR #21 head SHA equals the certified candidate;
- no unexpected files or user-owned `AGENTS.md` are included;
- required checks/reviews are satisfied;
- resulting `main` SHA is recorded.

Production deployment verification is separate and must record authenticated Cloudflare deployment and smoke evidence.

## Protected State

- `main` until reviewed merge;
- production deployment/domain until explicit authenticated release;
- verified resume/project content;
- interaction station identities/content;
- certified movement/topology/camera/route/accessibility behavior;
- user-owned `AGENTS.md`.

## Known closed decisions

- merge and production deploy are separate authority transfers;
- no uncertified art reaches `main`;
- a passing PR is not equivalent to a production deployment;
- Stage 06 may not introduce new visual work.

## Stop Conditions

- exact-head evidence does not match the candidate;
- independent review fails;
- formal certification fails;
- unexpected protected-state diff exists;
- PR head drifts after certification;
- merge authority is unavailable;
- production deployment authority/evidence is unavailable;
- user-owned `AGENTS.md` is modified.