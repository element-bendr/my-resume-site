# Stage 06 — Performance, Accessibility, Mobile and Visual Hardening

## Authority / ownership

- repository: element-bendr/my-resume-site
- Stage 06 root branch: `stage06/performance-accessibility`; current bounded lane branch/worktree: `stage06/map-semantics-focus` / `.worktrees/stage06-performance`. `state.json` and `HANDOFF.md` remain authoritative for the active lane.
- owner: Sol (architecture/acceptance); Luna (bounded implementation); Terra (independent review)
- execution mode: implementation after this contract is committed and Stage 06 is activated through ICM tooling
- authority: certified feature branch `feat/portfolio-world-icm-rebuild` at `f756316c2826eede6bed2790cb81020f5f34db35`; `main` and production are protected

## Inputs

- formally certified Stages 00–05 and Stage 05 exact-head evidence/run `36568411611`
- current inherited local baseline and measurements in `docs/portfolio-world/STAGE-06-BASELINE.md`
- `docs/portfolio-world/ARCHITECTURE.md`, `ASSET-BUDGET.md`, `RENDERING-TECHNOLOGY.md`, `MOVEMENT-ARCHITECTURE.md`, and Stage 04 validation evidence
- `docs/portfolio-world/ASK-CONTRACT.md`, Stage 05 validation and completion evidence
- committed package lock and Node 22.22.x / npm 11.20.0 runtime

## Objective

Measure and harden the complete certified portfolio across loading and runtime performance, bundle/chunk behavior, accessibility, keyboard operation, reduced motion, responsive/mobile usability, visual hierarchy, fallback resilience, and browser/runtime errors. Preserve the same product, content, Ask behavior, and world architecture while making it faster, more accessible, stable, responsive, and polished. Measure before changing code; every optimization must improve user behavior or enforce a meaningful existing budget.

## In Scope

- Measured conventional-route and `/play` loading/bundle behavior; preserve world isolation and lazy district boundaries.
- World runtime profiling and only clearly evidenced unnecessary work.
- Semantic/accessibility and keyboard audit of `/`, `/projects`, `/resume`, `/ask`, and `/contact`; HTML-based accessibility for world controls and overlays.
- Reduced-motion behavior, mobile/tablet/desktop layout, touch affordances, overflow, and restrained visual hardening.
- Fallback, browser console/runtime, and network behavior; preserve all Stage 05 Ask privacy, grounding, and disclosure guarantees.
- Lane-based remediation only after this contract and baseline are frozen; targeted tests per lane, complete regression and independent Terra final audit.

## Out of Scope

- New features, projects/content, Ask capabilities, LLM/model, analytics, storage/database/persistence/accounts, new world zones or movement mechanics.
- Combat, jumping, physics, navigation engine, renderer rewrite, WebGPU production path, major navigation/design-system redesign.
- Dependency upgrades unless a demonstrated defect cannot reasonably be solved otherwise; no package-lock change without explicit approval.
- Changing certified factual behavior, movement semantics, topology, direct routes, WebGL fallback, or protected stages.
- Deploying, modifying `main`, or Stage 07 implementation.

## Dependencies

- Stages 00–05 remain certified and current; Stage 05 deterministic Ask behavior and API boundaries remain unchanged.
- Existing pinned runtime, package lock, local verification scripts, browser tools, and asset/world budgets remain authoritative.
- `main`, production, content records, world topology/controller semantics, and fallback remain protected.
- Do not begin remediation until the frozen baseline is documented and Stage 06 is formally active.

## Process

1. Reconfirm isolated branch/base, protected state, and inherited gates.
2. Measure baseline before edits: production bundle/chunks, route isolation, world/lazy chunks, responsive/browser/accessibility behavior, reduced motion, fallback, console and network.
3. Review findings and choose non-overlapping implementation lanes; use Luna for bounded changes and Terra for independent substantial-lane/final review.
4. For each lane, state evidence and acceptance, make the smallest change, run the smallest relevant check, then required broader regression. GitHub freezes the lane contract/diff; the local Stage 06 worktree may perform browser/runtime validation and bounded repairs, but must push exact-head evidence back to the lane PR before the lane is frozen.
5. Preserve conventional routes as first-class accessible HTML equivalents; do not try to make raw geometry screen-reader semantic.
6. Run complete inherited and Stage 06 regression, inspect the full diff, and update validation/completion/HANDOFF evidence.
7. Stop for Terra final audit; no deployment or `main` change.

## Outputs

- this frozen Stage 06 contract
- `docs/portfolio-world/STAGE-06-BASELINE.md` and linked decision/evidence as needed
- measured, reviewed Stage 06 implementation lanes and focused tests
- `docs/portfolio-world/STAGE-06-VALIDATION.md`
- `workflow/active/portfolio-world-rebuild/output/06-performance-accessibility-completion-report.md`
- updated `HANDOFF.md`; Terra final audit and protected-state evidence

## Acceptance

- inherited Stages 00–05 tests and checks remain green; Ask grounding, API, disclosure, and fidelity guarantees are preserved.
- conventional routes do not fetch the Three/R3F world runtime; district chunks remain lazy; existing asset and world budgets pass.
- no horizontal overflow at 360/390/768/1024/1440 target widths; essential actions have usable keyboard paths, predictable focus, semantic controls, and verified reduced-motion behavior.
- mobile world overlays/map remain usable; fallback exposes all essential routes without WebGL.
- no unexplained console errors, failed requests, or material performance regressions; measured bundle/runtime baseline and changes are recorded.
- no unnecessary production dependency; protected content/contracts/state remain intact; Terra final verdict PASS.

## Verify

- `python3 scripts/bootstrap_check.py`
- `python3 scripts/workflow_check.py`
- `python3 scripts/workflow_status.py --strict`
- `npm run verify:offline`, `npm run typecheck`, `npm test`, `npm run build`
- `npm run verify:assets`, `npm run verify:world-assets`, and Stage 05 Ask disclosure/world boundary guards
- browser matrix at 360, 390, 768, 1024, and 1440 across required conventional routes and `/play`; keyboard/focus, reduced motion, overlay/map, and forced no-WebGL fallback
- inspect route requests, console/runtime errors, output bundles, full diff, and protected state

## Protected State

- Stage 00–05 certified contracts, evidence, content records, deterministic Ask answers/disclosure, API boundaries, and package lock.
- `main` and production deployment/domain remain unchanged.
- world topology, controller/movement semantics, WebGL architecture/fallback, direct conventional routes, and district lazy boundaries.
- no secrets, private information, filesystem paths, or internal Ask provenance leak.

## Known closed decisions

- The current 956.38 kB raw / 254.75 KiB gzip WorldEntry renderer chunk is isolated to `/play`; its >500 kB advisory is not a reason to suppress it or redesign the renderer.
- Conventional routes currently avoid the world renderer; preserve route-level separation and lazy districts.
- Conventional HTML routes remain primary accessible alternatives to optional 3D; raw geometry will not receive invented screen-reader semantics.
- No arbitrary Lighthouse score gate is introduced before baseline measurement.
- No dependency upgrade or new rendering architecture is approved by this stage contract.

## Stop Conditions

- inherited baseline is red after environment diagnosis; certified Ask behavior changes; or protected content/contracts need alteration.
- a proposed fix requires a major architecture change, dependency upgrade, movement/controller/topology change, `main` modification, or deployment.
- an optimization has no measurable user benefit or an existing budget basis.
- remote feature branch moves unexpectedly; preserve local work and reconcile before proceeding.
- a required browser/runtime result cannot be established with available tools; report evidence and ask for direction rather than guessing.
