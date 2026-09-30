# Portfolio World Rebuild

## Authority / ownership
- repository: element-bendr/my-resume-site
- branch/worktree: feat/portfolio-world-icm-rebuild
- owner: coordinator
- execution mode: implementation
- parallel-write boundaries: single owner until explicit non-overlapping lanes are recorded

## Inputs
- baseline `main` commit `63d25e7dbc3169cb41aaa181a513ca7af5860ba4`
- ICM 2.1.0 @ `90322a2441539f24eafdbd2c8a36bc6392192af4`
- accepted architecture decision in `decisions/2026-09-28-portfolio-world-architecture.md`
- verified portfolio/resume content, once stage 01 reconciles its source of truth

## Objective
Deliver a production-ready 3D portfolio/resume experience with a conventional accessible fallback, certify it on Cloudflare preview infrastructure, and only then make it eligible for promotion to `main`.

## In Scope
- ICM migration and durable project contract
- content reconciliation
- React/Vite/TypeScript/Worker application scaffold
- 3D command-center vertical slice
- navigation/HUD and accessible fallback routes
- remaining professional and personal zones
- Ask terminal integration
- mobile/low-power/reduced-motion behavior
- automated asset-budget enforcement
- tests, build, visual, accessibility, performance, preview, and promotion evidence

## Out of Scope
- modifications to `main` before certification
- fabricated resume/project facts
- multiplayer, accounts, or persistent achievements
- unnecessary Cloudflare data products
- changes to unrelated repositories

## Dependencies
- stage 00 depends on the current `main` baseline and pinned ICM template source
- each later stage depends on certification/evidence from the prior stage
- current public portfolio content may be imported only after stage 01 resolves provenance

## Process
1. Inspect current repository state and relevant diff.
2. Load only context needed for the active stage.
3. Confirm execution mode, protected state, and ownership.
4. Execute only work allowed by the active stage.
5. Validate at meaningful checkpoints.
6. Inspect final diff/status.
7. Update handoff and completion evidence.
8. Advance only after acceptance conditions are satisfied.

## Outputs
- production application source
- structured portfolio content
- optimized 3D assets
- tests and deterministic asset-budget checks
- Cloudflare configuration
- retained certification and promotion evidence

## Acceptance
- `main` remains unchanged before promotion
- conventional portfolio works without 3D
- 3D world satisfies the frozen zone and interaction contract
- no fabricated content enters production
- asset/performance budgets are measured automatically
- tests/build/accessibility/visual/preview gates pass
- production promotion is explicit and evidence-backed

## Verify
- `python3 scripts/bootstrap_check.py`
- `python3 scripts/workflow_check.py`
- `python3 scripts/workflow_status.py --strict`
- stage-specific TypeScript/build/test checks once the app exists
- automated asset-size manifest/budget check
- accessibility checks
- desktop/mobile visual inspection
- Cloudflare preview smoke test
- final diff/protected-state audit

## Protected State
- `main`
- current production deployment/domain
- credentials and secrets
- unrelated repositories
- verified resume/project claims

## Known closed decisions
- no second Cloudflare account solely for the 25 MiB individual asset limit
- 3D is optional and never the only navigation path
- no persistent multiplayer backend in v1
- R2/D1/KV/Durable Objects require measured justification

## Stop Conditions
- implementation would modify `main` before certification
- content provenance is ambiguous
- protected state cannot be proven unchanged
- a required dependency exceeds the accepted platform/budget contract
- an asset exceeds the 10 MiB internal ceiling without an accepted exception
- a required validation gate fails

## Stage plan
- 00-bootstrap — adopt ICM, preserve protected state, pass bootstrap/workflow checks
- 01-content-contract — reconcile repository vs current live portfolio content and freeze structured sources
- 02-app-foundation — React/Vite/TypeScript/Worker scaffold, routing, fallback shell, tests/build
- 03-command-center-slice — polished first 3D room with movement/camera, inspection, HUD, one project, Ask entry
- 04-world-zones — Build Lab, Automation Lab, Client Street, Timeline, Hobby District with lazy loading
- 05-integration — Ask/contact/project links/content/error/fallback behavior
- 06-performance-accessibility — mobile, reduced motion, low-power mode, asset budgets, accessibility/performance
- 07-certification-promotion — regression, visual inspection, Cloudflare preview, evidence, explicit promotion record
