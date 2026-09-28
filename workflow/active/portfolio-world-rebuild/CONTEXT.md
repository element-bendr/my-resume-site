# Portfolio World Rebuild

## Authority / ownership
- repository: element-bendr/my-resume-site
- branch/worktree: feat/portfolio-world-icm-rebuild
- owner: coordinator
- execution mode: implementation
- parallel-write boundaries: single owner until explicit non-overlapping lanes are recorded

## Inputs
- baseline `main` commit 63d25e7dbc3169cb41aaa181a513ca7af5860ba4
- ICM 2.1.0 @ 90322a2441539f24eafdbd2c8a36bc6392192af4
- accepted architecture decision
- verified current portfolio/resume content, once reconciled

## Objective
Deliver a production-ready 3D portfolio/resume experience with a conventional accessible fallback, certify it on Cloudflare preview infrastructure, and only then make it eligible for promotion to `main`.

## Stages
- 00-bootstrap — adopt ICM, preserve protected state, pass bootstrap/workflow checks.
- 01-content-contract — reconcile repository vs current live portfolio content and freeze structured sources.
- 02-app-foundation — React/Vite/TypeScript/Worker scaffold, routing, fallback shell, tests/build.
- 03-command-center-slice — polished first 3D room with movement/camera, inspection, HUD, one project, Ask entry.
- 04-world-zones — Build Lab, Automation Lab, Client Street, Timeline, Hobby District with lazy loading.
- 05-integration — Ask/contact/project links/content/error/fallback behavior.
- 06-performance-accessibility — mobile, reduced motion, low-power mode, asset budgets, accessibility/performance.
- 07-certification-promotion — regression, visual inspection, Cloudflare preview, evidence, explicit promotion record.

## In Scope
ICM migration, content reconciliation, app/world implementation, structured content, Ask integration, mobile/accessibility/performance, deterministic budget checks, tests, preview certification, promotion evidence.

## Out of Scope
Changes to `main` before certification, fabricated facts, multiplayer/accounts/persistent achievements, unnecessary Cloudflare data products, unrelated repos.

## Acceptance
- `main` unchanged before promotion;
- conventional portfolio works without 3D;
- 3D world satisfies zone/interaction contract;
- asset budgets are automated/measured;
- tests/build/accessibility/visual/preview checks pass;
- promotion is explicit and evidence-backed.

## Protected State
`main`, production deployment/domain, secrets, unrelated repositories, verified resume/project claims.

## Stop Conditions
Stop if implementation would modify `main`, content provenance is ambiguous, protected state cannot be proven unchanged, a required platform capability is unsupported, asset ceiling is exceeded without exception, or a required validation gate fails.
