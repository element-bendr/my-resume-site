# Stage 07 — Certification and Promotion

## Authority / ownership

- repository: element-bendr/my-resume-site
- Stage 07 branch/worktree: `stage07/certification-promotion` / `.worktrees/stage07-certification-promotion`
- Stage 06 certified root: `fe1d15199f06a8a6a2cae22dbc7fa623e75218f6`
- owner: Sol (promotion acceptance); Luna (local execution); Terra (independent review)
- execution mode: certification
- `main`, production deployment, production domain, credentials, and secrets remain protected until explicit Stage 07 promotion gates pass

## Inputs

- formally certified Stage 06 state and completion evidence
- certified Stage 06 candidate `96a944dba45ea4fe36c9e580eedaa980d4c8d32e`
- integrated Stage 06 root `fe1d15199f06a8a6a2cae22dbc7fa623e75218f6`
- existing Cloudflare Worker/static-assets configuration
- current production baseline on `main`
- all Stage 00–06 contracts, decisions, validation records, and completion reports

## Objective

Prove the complete certified portfolio world on Cloudflare preview infrastructure, preserve all certified behavior and protected state, create explicit promotion evidence, and make the certified application eligible for deliberate promotion to `main` and production only after every Stage 07 gate passes.

## In Scope

- activate Stage 07 through repository ICM tooling
- integrate the certified Stage 06 root into the portfolio rebuild integration branch without altering certified runtime behavior
- produce a Cloudflare preview build/deployment using non-production configuration
- run final regression, browser, visual, accessibility, fallback, route, network, and asset-budget checks against preview
- compare preview behavior with certified local evidence
- verify conventional routes remain first-class and 3D remains optional
- inspect final repository diff and promotion provenance
- produce Stage 07 validation evidence, completion report, and explicit promotion record
- after all gates and independent review pass, prepare a separate explicit promotion step for `main` and production

## Out of Scope

- new features, content, redesigns, dependency upgrades, renderer changes, Ask/model changes, or topology/controller changes
- silent merge to `main`
- production deployment before explicit promotion approval/evidence
- changing Cloudflare production credentials, domain, or account configuration merely to make preview pass
- weakening tests, budgets, accessibility, fallback, route isolation, or certified guards
- deleting historical failed-audit evidence

## Dependencies

- Stages 00–06 must remain certified and non-stale
- Stage 06 root must carry the formal certification state
- Cloudflare preview must use existing repository configuration and non-production deployment semantics
- any external preview/deployment identifier must be recorded as evidence rather than inferred

## Process

1. Activate Stage 07 with `python3 scripts/workflow_activate.py --workflow portfolio-world-rebuild --write`.
2. Confirm strict workflow state and clean worktree before promotion work.
3. Compare the Stage 06 root with the rebuild integration branch and integrate only certified Stage 06 changes.
4. Run local repository gates again on the exact integration candidate.
5. Build and deploy to Cloudflare preview only; record exact commit, preview URL/identifier, and deployment evidence.
6. Run final browser/visual/accessibility/regression checks on preview at 360, 390, 768, 1024, and 1440 px.
7. Verify all conventional routes, `/play`, Ask, map/focus, fast travel, reduced motion, no-WebGL fallback, SPA exits, portal alignment, route isolation, lazy districts, console/network state, and budgets.
8. Compare preview evidence to Stage 06 certified evidence and investigate any drift.
9. Run protected-state and final diff audit.
10. Obtain independent Terra review on the exact promotion candidate and evidence.
11. Write Stage 07 validation evidence, completion report, and explicit promotion record.
12. Only after Stage 07 certification may a separate, explicit promotion action merge to `main` and deploy production.

## Outputs

- `docs/portfolio-world/STAGE-07-VALIDATION.md`
- `docs/portfolio-world/PROMOTION-RECORD.md`
- `workflow/active/portfolio-world-rebuild/output/07-certification-promotion-completion-report.md`
- updated `HANDOFF.md`
- updated workflow certification state
- Cloudflare preview evidence referencing the exact candidate

## Acceptance

- Stage 07 activation occurs through repository ICM tooling
- Stages 00–06 remain certified and non-stale
- certified Stage 06 runtime behavior is unchanged by integration
- local full gates pass on the exact promotion candidate
- Cloudflare preview deploy succeeds without touching production
- preview browser matrix passes at 360/390/768/1024/1440
- conventional routes remain isolated from optional world runtime
- `/play` and all five SPA exits remain zero-error
- keyboard/focus, map, fast travel, touch targets, reduced motion, fallback, portal alignment, and lazy district behavior remain correct
- no unexplained console errors, page errors, failed requests, or unexpected HTTP failures
- asset/world budgets and Ask guards pass
- final diff/protected-state audit is PASS
- Terra independently returns PASS on the exact promotion candidate
- promotion record identifies the exact candidate, preview evidence, protected-state status, and explicit next promotion action
- `main` and production remain unchanged until that explicit next action

## Verify

- `python3 scripts/bootstrap_check.py`
- `python3 scripts/workflow_check.py`
- `python3 scripts/workflow_status.py --strict`
- `npm run verify:offline`
- `npm run typecheck`
- `npm test`
- `npm run build`
- `npm run verify:assets`
- `npm run verify:world-assets`
- `npm run verify:ask-disclosure`
- `npm run verify:world-ask`
- exact-commit Cloudflare preview deploy and smoke checks
- 360/390/768/1024/1440 preview browser matrix
- keyboard/focus and coarse-pointer checks
- reduced-motion and forced no-WebGL checks
- route/network/console inspection
- final git diff and protected-state audit
- Terra final review
- repository certification check/write before promotion eligibility

## Protected State

- `main`
- current production deployment and production domain
- Cloudflare production credentials/secrets
- certified Stage 00–06 records and runtime behavior
- verified portfolio/resume content
- Ask grounding/API contract
- movement/controller semantics and world topology
- dependency lockfile unless a separately justified Stage 07 blocker requires change

## Known closed decisions

- 3D remains optional and never the only navigation path
- Cloudflare Workers Static Assets remains the initial delivery target
- no second Cloudflare account is required for the current asset contract
- persistent zone-label output uses the SiteShell-owned portal host
- no teardown suppression, hard-reload workaround, or renderer rewrite is permitted
- Stage 07 is evidence/promotion work, not a product-feature stage
- production promotion is a separate explicit action after Stage 07 certification

## Stop Conditions

- any Stage 00–06 certification becomes stale
- local or preview regression fails
- preview differs materially from certified Stage 06 behavior
- protected `main` or production state changes before explicit promotion
- preview deploy requires unsafe credential/config changes
- asset, accessibility, route isolation, Ask, fallback, or browser gates fail
- Terra reports a required fix
- exact promotion candidate/provenance cannot be established
