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
- active workflow/stage: workflow/active/portfolio-world-rebuild / 00-bootstrap
- template source: ICM 2.1.0 @ 90322a2441539f24eafdbd2c8a36bc6392192af4

## Current state
Stage 00 is certified. Stage 01 is active. Content sources have been reconciled into a category-specific authority model: project repos/certification for technical facts, sanitized case studies for public disclosure, current profile repos for positioning, structured profile content for employment history, and direct user approval for hobbies. The legacy resume site is historical input only.

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
- branch base: 63d25e7dbc3169cb41aaa181a513ca7af5860ba4
- `python3 scripts/bootstrap_check.py`: PASS
- `python3 scripts/workflow_check.py`: PASS
- `python3 scripts/workflow_status.py --strict`: PASS
- `workflow_activate.py` dry-run/write: PASS
- post-activation workflow/status checks: PASS
- remote Stage 00 output existence: PASS
- full-tree clean clone proof: NOT CLAIMED; scoped checkout limitation retained
- validated commit: pending Stage 00 certification

## Protected state
- main / production baseline: UNCHANGED
- secrets/credentials: UNCHANGED
- current production deployment/domain: UNCHANGED
- unrelated repositories: UNCHANGED

## Stale / uncertain state
- This repo is an older static portfolio baseline; current deployed Ask-site content must be reconciled explicitly before implementation.
- Hosted Actions may remain unavailable until minutes reset; deterministic local certification may be used where the workflow contract permits it.

## Next atomic action
Validate the Stage 01 content contract against the pinned sources and certification requirements. If green, certify Stage 01 and advance to Stage 02 application foundation.

## Minimum resume context
1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-rebuild/CONTEXT.md`
5. `decisions/2026-09-28-portfolio-world-architecture.md`
