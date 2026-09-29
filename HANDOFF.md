# Current Handoff

## Goal
Replace the static resume site with a production-ready gamified 3D portfolio while preserving a fast conventional portfolio/resume path and keeping `main` untouched until certification.

## Phase
STAGE_04_WORLD_ZONES

## Execution mode
implementation

## Authority / location
- repository: element-bendr/my-resume-site
- canonical branch: main
- working branch/worktree: feat/portfolio-world-icm-rebuild
- active workflow/stage: workflow/active/portfolio-world-rebuild / 04-world-zones
- template source: ICM 2.1.0 @ 90322a2441539f24eafdbd2c8a36bc6392192af4

## Current state
Stages 00-03 are formally certified. Stage 04 is blocked awaiting activation with its world-zone contract now frozen. The next implementation expands the certified Command Center controller into Build Lab, Automation Lab, Client Street, Timeline Corridor, and Hobby District using one shared topology and lazy district modules.

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
- Stage 02 application candidate: 62df9c82a1e4860de777803bfdc259b8ab65b3af
- Stage 02 app CI run 36423770301: PASS
- Stage 02 ICM candidate: 0f2ef77df68fdd28674b50bfe83c183770adf890
- Stage 02 ICM run 36424566049: PASS
- Stage 03 contract/activation: ACTIVE
- Stage 03 application candidate: 30740ed443f6f20d0432d0d07d530ebdab2fe321
- Stage 03 exact-head CI run 36444089676: PASS (6 test files / 21 tests, build, budgets, browser fallback, WebGL screenshot)

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
- Stage 03 Command Center is certified. Stage 04 may expand topology but must preserve the certified controller, browser fallback, and direct-route behavior.

## Next atomic action
Activate Stage 04, generalize movement to the legal-area union, add world topology + fast travel, then implement district modules and content interactions. Do not begin Stage 05 Ask/backend integration.

## Minimum resume context
1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-rebuild/CONTEXT.md`
5. `decisions/2026-09-28-portfolio-world-architecture.md`
