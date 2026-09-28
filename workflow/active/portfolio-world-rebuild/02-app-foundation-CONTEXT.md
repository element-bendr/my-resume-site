# Stage 02 — Application Foundation

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/portfolio-world-icm-rebuild
- owner: coordinator
- execution mode: implementation
- parallel-write boundaries: foundation/config/content only; no Three.js world implementation

## Inputs

- certified Stage 00 architecture/bootstrap candidate `6b093fc74a3729018259beefd74bf16388ef98c4`
- certified Stage 01 content-contract candidate `2eb0a1dbbed64555902aa38a44a2d46bcce920fa`
- `docs/portfolio-world/CONTENT-CONTRACT.md`
- `docs/portfolio-world/CONTENT-SOURCES.json`
- `docs/portfolio-world/ARCHITECTURE.md`
- `docs/portfolio-world/ASSET-BUDGET.md`
- Cloudflare React/Vite/Static Assets guidance current on 2026-09-28

## Objective

Create a production-oriented React/TypeScript/Vite application foundation with typed, source-referenced portfolio content, conventional accessible routes, a minimal Cloudflare API Worker, deterministic validation scripts, and no 3D world code yet.

## In Scope

- React SPA shell and conventional navigation;
- routes for Home, Play placeholder, Projects, Resume, Ask placeholder, and Contact;
- typed presentation content derived only from the Stage 01 contract;
- Cloudflare Vite plugin and Workers Static Assets configuration;
- a minimal `/api/health` Worker endpoint;
- TypeScript project references for client, tooling, and Worker;
- deterministic content/route/asset-budget validation;
- package manifest with exact dependency versions;
- package-lock generation when registry access is available;
- basic responsive/accessibility structure and semantic HTML;
- preserving the old static files as historical branch content until deliberate cleanup.

## Out of Scope

- Three.js / React Three Fiber;
- 3D geometry, character controller, camera, navmesh, animation;
- Ask-model integration;
- contact submission backend;
- D1, KV, R2, Durable Objects;
- production deployment;
- rewriting unresolved education/LinkedIn/client outcome claims.

## Dependencies

- Stage 01 must remain certified and current;
- package installation/build requires registry access unavailable in the current execution container;
- Cloudflare platform configuration follows the official Vite plugin React SPA + Worker pattern.

## Process

1. Freeze package/runtime choices in a durable decision.
2. Scaffold the React/TypeScript/Vite/Worker foundation.
3. Materialize typed content from the Stage 01 authority contract.
4. Add conventional accessible routes and navigation.
5. Add deterministic content and asset-budget checks.
6. Generate a package lock and install dependencies in a network-enabled environment.
7. Run typecheck, tests, build, Worker preview/smoke, and budget checks.
8. Inspect diff/protected state.
9. Record completion evidence only after all required checks are green.

## Outputs

- package/runtime decision;
- package manifest and lockfile;
- React/TypeScript application shell;
- conventional routes;
- typed content registry;
- Worker and Wrangler configuration;
- Vite/TypeScript configuration;
- deterministic tests and verification scripts.

## Acceptance

- package versions are exact and documented;
- `package-lock.json` exists and matches `package.json`;
- `npm ci` succeeds;
- TypeScript checks succeed;
- deterministic tests succeed;
- Vite/Cloudflare build succeeds;
- `/api/health` returns expected JSON under Worker preview;
- Home/Projects/Resume/Ask/Contact/Play routes resolve;
- essential navigation is usable without WebGL;
- no Three.js/R3F dependency or import exists yet;
- content tests reject skill percentages and unresolved education;
- critical built shell remains within the Stage 00 budget;
- `main` remains unchanged.

## Verify

- `npm ci`
- `npm run typecheck`
- `npm test`
- `npm run build`
- `npm run verify:content`
- `npm run verify:assets`
- `npm run preview` plus `/api/health` smoke check
- `python3 scripts/workflow_check.py`
- `python3 scripts/workflow_status.py --strict`
- final protected-state diff

## Protected State

- `main` and current production deployment/domain;
- certified Stage 00/01 decisions and content authority;
- unresolved education/LinkedIn/client outcome fields;
- private source/client data and credentials;
- no 3D implementation before Stage 03.

## Known closed decisions

- WebGL 2 remains the v1 production 3D renderer, but no renderer is installed in Stage 02;
- Cloudflare official Vite integration is the application/deployment foundation;
- conventional HTML/React portfolio routes are first-class;
- no Cloudflare persistence products are introduced;
- dependency versions are pinned exactly, not floating ranges.

## Stop Conditions

- package/runtime incompatibility is discovered;
- package-lock cannot be generated and verified;
- build/typecheck/tests fail;
- content requires an unresolved or private claim;
- the foundation introduces 3D or storage scope early;
- protected `main` or production state would change.
