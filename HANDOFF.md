# Current Handoff

## Goal
Replace the static resume site with a production-ready gamified 3D portfolio while preserving a fast conventional portfolio/resume path and keeping `main` untouched until certification.

## Phase
STAGE_00_CERTIFICATION

## Execution mode
implementation

## Authority / location
- repository: element-bendr/my-resume-site
- canonical branch: main
- working branch/worktree: feat/portfolio-world-icm-rebuild
- active workflow/stage: workflow/active/portfolio-world-rebuild / 00-bootstrap
- template source: ICM 2.1.0 @ 90322a2441539f24eafdbd2c8a36bc6392192af4

## Current state
The production baseline is untouched. Stage 00 ICM adoption and architecture work is complete and active; deterministic bootstrap/workflow/status and activation checks passed in a scoped control-surface checkout. Stage certification is the remaining gate before Stage 01.

## Canonical decisions
- `main` remains untouched until certification and explicit promotion.
- 3D is optional; conventional portfolio/resume navigation remains first-class.
- Cloudflare Workers Static Assets is the initial delivery target.
- A second Cloudflare account is not justified by the 25 MiB individual static-asset limit.
- R2/D1/KV/Durable Objects stay out until evidence demonstrates a need.
- World locomotion is guided third-person: WASD/click-to-move desktop, tap-to-move mobile, constrained navigation, context interactions, and map fast travel; no jumping/combat/falling in v1.
- WebGL 2 is the v1 production renderer; WebGPU remains architecture-ready and is evaluated only after the Command Center vertical slice; WebAssembly is permitted selectively for mature performance/codec helpers, not as the application architecture.

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
Run Stage 00 certification against the evidence candidate. If green, advance to Stage 01 content reconciliation before any React/3D implementation.

## Minimum resume context
1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-rebuild/CONTEXT.md`
5. `decisions/2026-09-28-portfolio-world-architecture.md`
