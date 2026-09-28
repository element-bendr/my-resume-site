# Current Handoff

## Goal
Replace the static resume site with a production-ready gamified 3D portfolio while preserving a fast conventional portfolio/resume path and keeping `main` untouched until certification.

## Phase
STAGE_02_APP_FOUNDATION

## Execution mode
implementation

## Authority / location
- repository: element-bendr/my-resume-site
- canonical branch: main
- working branch/worktree: feat/portfolio-world-icm-rebuild
- active workflow/stage: workflow/active/portfolio-world-rebuild / 02-app-foundation
- template source: ICM 2.1.0 @ 90322a2441539f24eafdbd2c8a36bc6392192af4

## Current state
Stages 00 and 01 are certified. Stage 02 application foundation is implemented through the offline-verifiable boundary. Content, route/renderer-boundary, Cloudflare configuration, security headers, and no-JavaScript fallback checks are green. Stage 02 remains active and uncertified because the execution environment cannot resolve the npm registry and has no cached Cloudflare Vite plugin, so the lockfile/install/build/preview gates cannot yet run.

## Canonical decisions
- `main` remains untouched until certification and explicit promotion.
- 3D is optional; conventional portfolio/resume navigation remains first-class.
- Cloudflare Workers Static Assets is the initial delivery target.
- A second Cloudflare account is not justified by the 25 MiB individual static-asset limit.
- R2/D1/KV/Durable Objects stay out until evidence demonstrates a need.
- World locomotion is guided third-person: WASD/click-to-move desktop, tap-to-move mobile, constrained navigation, context interactions, and map fast travel; no jumping/combat/falling in v1.
- WebGL 2 is the v1 production renderer; WebGPU remains architecture-ready and is evaluated only after the Command Center vertical slice; WebAssembly is permitted selectively for mature performance/codec helpers, not as the application architecture.
- Content authority is category-specific: current project evidence for technical facts, sanitized case studies for disclosure, current profile sources for positioning, structured profile content for employment history, and user approval for hobbies.

## Validation evidence
- Stage 00 certified candidate: 6b093fc74a3729018259beefd74bf16388ef98c4
- Stage 01 certified candidate: 2eb0a1dbbed64555902aa38a44a2d46bcce920fa
- Stage 02 content check: PASS (10 projects / 3 experience / 15 skills / 5 hobbies / 6 sources)
- Stage 02 renderer boundary: PASS (14 source files; 0 Three/R3F/Drei imports/dependencies)
- Stage 02 conventional routes: PASS
- Stage 02 Cloudflare/security config: PASS
- frozen package versions: publicly verified
- Node/npm baseline: 22.16.0 / 11.20.0
- package-lock generation: BLOCKED by unavailable registry/cache
- npm ci / TS7 typecheck / Vitest / production build / asset budget / Worker preview: PENDING
- Stage 02 certification: BLOCKED until those gates are green

## Protected state
- main / production baseline: UNCHANGED
- secrets/credentials: UNCHANGED
- current production deployment/domain: UNCHANGED
- unrelated repositories: UNCHANGED

## Stale / uncertain state
- education is intentionally unresolved and excluded until verified;
- LinkedIn URL is excluded until directly verified;
- client testimonials/outcome claims require evidence before inclusion;
- local package-lock/build evidence remains unavailable because this execution environment has no npm registry access/cache; remote CI is now the certification runner.
- hosted Actions remain unsuitable while account minutes are constrained.

## Next atomic action
In the first network-enabled execution environment, run `npm install --package-lock-only`, commit the lockfile, then run `npm ci && npm run verify`, `npm run preview`, and smoke `/api/health`. Fix any failures before Stage 02 certification. Do not begin Stage 03 until Stage 02 is certified.

## Minimum resume context
1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-rebuild/CONTEXT.md`
5. `decisions/2026-09-28-portfolio-world-architecture.md`
