# Current Handoff

## Goal
Replace the static resume site with a production-ready gamified 3D portfolio while preserving a fast conventional portfolio/resume path and keeping `main` untouched until certification.

## Phase
STAGE_01_CONTENT_CONTRACT

## Execution mode
implementation

## Authority / location
- repository: element-bendr/my-resume-site
- canonical branch: main
- working branch/worktree: feat/portfolio-world-icm-rebuild
- active workflow/stage: workflow/active/portfolio-world-rebuild / 01-content-contract
- template source: ICM 2.1.0 @ 90322a2441539f24eafdbd2c8a36bc6392192af4

## Current state
Stage 00 is certified. Stage 01 content reconciliation is complete pending certification. The content authority model is frozen: project evidence governs technical facts, sanitized case studies govern disclosure, current profile sources govern positioning, structured profile content governs employment history, and legacy resume HTML is historical input only.

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
- Stage 00 bootstrap/workflow/status/activation/certification: PASS
- Stage 01 source snapshot resolution: PASS
- Stage 01 category-specific authority reconciliation: PASS
- Stage 01 legacy preserve/replace/reject classification: PASS
- Stage 01 protected-state review: PASS
- Stage 01 certification: PENDING

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
Certify Stage 01 against its completion evidence. If green, activate Stage 02 application foundation and create the typed content + React/Vite/Worker shell while preserving the legacy main branch.

## Minimum resume context
1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-rebuild/CONTEXT.md`
5. `decisions/2026-09-28-portfolio-world-architecture.md`
