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
Stages 00 and 01 are certified. Stage 02 is blocked only for contract activation. The next implementation is the conventional React/TypeScript/Vite/Cloudflare foundation and typed content layer; Three.js remains explicitly deferred to Stage 03.

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
- Stage 01 ICM certification: PASS
- Stage 02 Cloudflare/React/Vite architecture research: COMPLETE
- Stage 02 dependency installation/build: PENDING network-enabled environment
- Stage 02 certification: PENDING

## Protected state
- main / production baseline: UNCHANGED
- secrets/credentials: UNCHANGED
- current production deployment/domain: UNCHANGED
- unrelated repositories: UNCHANGED

## Stale / uncertain state
- education is intentionally unresolved and excluded until verified;
- LinkedIn URL is excluded until directly verified;
- client testimonials/outcome claims require evidence before inclusion;
- hosted Actions confirmation remains optional/deferred while account minutes are constrained.

## Next atomic action
Activate the Stage 02 contract, scaffold the typed React/Vite/Cloudflare foundation, and run all deterministic checks available without registry access. Do not certify Stage 02 until package-lock, npm ci, typecheck, tests, build, preview/API smoke, and asset-budget checks are green.

## Minimum resume context
1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-rebuild/CONTEXT.md`
5. `decisions/2026-09-28-portfolio-world-architecture.md`
