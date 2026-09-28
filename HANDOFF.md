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
Stages 00 and 01 are certified. Stage 02 application foundation is functionally complete and exact-head CI is green at `62df9c82a1e4860de777803bfdc259b8ab65b3af`: deterministic lockfile, npm ci, content/boundary/config checks, TypeScript, 10/10 tests, production build, 87.0 KiB critical gzip, and Cloudflare preview /api/health all pass. Only the repository ICM certification transition remains before Stage 03.

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
- Stage 02 exact application candidate: 62df9c82a1e4860de777803bfdc259b8ab65b3af
- Stage 02 CI run 36423770301: PASS
- deterministic lockfile / npm ci: PASS
- content/boundary/config gates: PASS
- TypeScript typecheck: PASS
- Vitest: 10/10 PASS
- production build: PASS
- asset budget: PASS; critical shell 87.0 KiB gzip
- Cloudflare preview /api/health: PASS
- Stage 02 ICM certification: PENDING

## Protected state
- main / production baseline: UNCHANGED
- secrets/credentials: UNCHANGED
- current production deployment/domain: UNCHANGED
- unrelated repositories: UNCHANGED

## Stale / uncertain state
- education is intentionally unresolved and excluded until verified;
- LinkedIn URL is excluded until directly verified;
- client testimonials/outcome claims require evidence before inclusion;
- Ask backend remains deferred to Stage 05;
- 3D renderer/world behavior remains deferred to Stage 03.

## Next atomic action
Run Stage 02 ICM certification. If green, mark Stage 02 certified, activate Stage 03, freeze the Command Center vertical-slice contract, then add the stable Three.js / React Three Fiber stack.

## Minimum resume context
1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-rebuild/CONTEXT.md`
5. `decisions/2026-09-28-portfolio-world-architecture.md`
