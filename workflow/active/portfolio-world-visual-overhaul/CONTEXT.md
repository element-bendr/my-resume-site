# Portfolio World Visual Overhaul — Stage 01 Visual Foundation

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: `visual/rendering-overhaul-v1` / `.worktrees/visual-rendering-overhaul-v1`
- owner: Luna implementation; Sol visual/architecture acceptance; Terra independent review
- execution mode: implementation
- parallel-write boundaries: `src/world/**`, `docs/portfolio-world/VISUAL-OVERHAUL-V1.md`, this workflow, and `HANDOFF.md`
- baseline: `main` at `5f4de7ace37bfd843ef13f035a3b16ddb61f28d7`

## Inputs

- frozen Portfolio World architecture and topology
- frozen rendering technology and asset budgets
- certified movement/navigation/Ask/accessibility behavior from the completed `portfolio-world-rebuild` workflow
- approved generated visual reference from the controlling conversation
- `docs/portfolio-world/VISUAL-OVERHAUL-V1.md`

## Objective

Replace the prototype-grade visual presentation with a premium stylized floating-world art direction while preserving the certified movement, interaction, topology, content, fallback, accessibility, and Cloudflare architecture.

## In Scope

- global sky, fog, tone mapping, shadows, key/fill lighting;
- floating-island foundations beneath the existing semantic zones;
- bridge architecture and environmental depth;
- Command Center / Central Plaza hero-art pass;
- recognizable stylized player avatar rendered by the existing PlayerController;
- first-pass art rebuild for Build Lab, Automation Lab, Client Street, Timeline Corridor, and Hobby District;
- procedural geometry first so composition can be approved before external GLB/KTX2 asset production;
- source, build, budget, browser, responsive, reduced-motion, fallback and visual validation.

## Out of Scope

- movement speed, acceleration, click/tap/keyboard semantics;
- camera behavior changes;
- topology bounds, bridge graph, fast-travel points, station IDs, station interaction points;
- Ask behavior or factual content;
- conventional portfolio routes;
- dependency upgrades or WebGPU adoption;
- production deployment;
- photorealism or AAA concept-art density.

## Dependencies

- completed/certified `portfolio-world-rebuild` workflow;
- `docs/portfolio-world/WORLD-SPEC.md`;
- `docs/portfolio-world/ARCHITECTURE.md`;
- `docs/portfolio-world/RENDERING-TECHNOLOGY.md`;
- `docs/portfolio-world/ASSET-BUDGET.md`.

## Process

1. Activate this workflow with repository ICM tooling before further implementation.
2. Validate the current branch candidate compiles and preserves certified controller/topology invariants.
3. Run the full unit suite and world guards.
4. Build and verify conventional/world asset budgets.
5. Render browser screenshots for Command Center plus every district at desktop and 390px.
6. Compare the rendered result against the approved visual direction: readable floating hub-and-spoke world, strong Central Plaza landmark, distinct districts, environmental depth, coherent lighting, recognizable player.
7. Fix only evidenced visual/runtime issues.
8. Obtain Terra independent review.
9. Record validation and completion evidence before merge.

## Outputs

- `docs/portfolio-world/VISUAL-OVERHAUL-V1.md`
- `docs/portfolio-world/VISUAL-OVERHAUL-V1-VALIDATION.md`
- `src/world/WorldEnvironment.tsx`
- `src/world/WorldScenery.tsx`
- visual-only updates under `src/world/**`
- `workflow/active/portfolio-world-visual-overhaul/output/completion-report.md`

## Acceptance

- movement/navigation/controller semantics are unchanged;
- topology bounds/graph/fast-travel/station coordinates are unchanged;
- 66 existing tests remain green;
- world guards and Ask boundaries remain green;
- production build succeeds;
- frozen conventional and world budgets pass;
- no-WebGL fallback remains valid;
- reduced-motion remains valid;
- initial world and all five districts render without page/runtime errors or failed requests;
- 390px world route retains no horizontal overflow;
- player is visually recognizable as a stylized human/avatar;
- Command Center reads as the dominant central plaza;
- world reads as connected floating districts rather than flat slabs;
- each district has distinct visual language matching `VISUAL-OVERHAUL-V1.md`;
- no production deployment occurs from this workflow.

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
- browser screenshots / runtime inspection for Command Center + five districts at 1440px and 390px
- forced no-WebGL fallback
- reduced-motion browser pass
- exact diff against `main` proving no controller/topology/content/dependency drift
- Terra final review

## Protected State

- `main`;
- production deployment/domain;
- completed certification records from `portfolio-world-rebuild`;
- `src/world/movement.ts`;
- movement constants in `src/world/world-config.ts`;
- semantic bounds/bridge graph in `src/world/world-topology.ts`;
- station IDs/positions/interaction points;
- Ask/content/routing contracts;
- dependencies and package lock unless a separately approved blocker requires a change.

## Known closed decisions

- movement is acceptable and is not part of this redesign;
- WebGL 2 / React Three Fiber / Three.js / Drei remain the production stack;
- Cloudflare Workers serve assets/APIs; browser GPU renders the world;
- generated concept art is visual direction, not a photoreal fidelity requirement;
- first pass remains procedural to validate composition before external asset production;
- production deploy remains paused while the visual direction is being corrected.

## Stop Conditions

- controller/topology behavior changes unintentionally;
- budgets fail materially;
- visual geometry traps/intercepts navigation;
- conventional/fallback routes regress;
- a new dependency becomes necessary without explicit contract update;
- two materially similar visual attempts fail to approach the approved reference.
