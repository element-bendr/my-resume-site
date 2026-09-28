# Current Handoff

## Goal
Replace the static resume site with a production-ready gamified 3D portfolio while preserving a fast conventional portfolio/resume path and keeping `main` untouched until certification.

## Phase
ICM_ADOPTION_AND_ARCHITECTURE

## Execution mode
implementation

## Authority / location
- repository: element-bendr/my-resume-site
- canonical branch: main
- working branch/worktree: feat/portfolio-world-icm-rebuild
- active workflow/stage: workflow/active/portfolio-world-rebuild / 00-bootstrap
- template source: ICM 2.1.0 @ 90322a2441539f24eafdbd2c8a36bc6392192af4

## Current state
The production baseline is untouched. ICM 2.1.0 project canon is being adopted before application implementation.

## Canonical decisions
- `main` remains untouched until certification and explicit promotion.
- 3D is optional; conventional portfolio/resume navigation remains first-class.
- Cloudflare Workers Static Assets is the initial delivery target.
- A second Cloudflare account is not justified by the 25 MiB individual static-asset limit.
- R2/D1/KV/Durable Objects stay out until evidence demonstrates a need.

## Validation evidence
- branch base: 63d25e7dbc3169cb41aaa181a513ca7af5860ba4
- bootstrap validation: PENDING
- workflow validation: PENDING
- validated commit: not yet certified

## Protected state
- main / production baseline: UNCHANGED
- secrets/credentials: UNCHANGED
- current production deployment/domain: UNCHANGED
- unrelated repositories: UNCHANGED

## Stale / uncertain state
- This repo is an older static portfolio baseline; current deployed Ask-site content must be reconciled explicitly before implementation.
- Hosted Actions may remain unavailable until minutes reset; deterministic local certification may be used where the workflow contract permits it.

## Next atomic action
Run the three deterministic Python ICM checks in a real checkout. If green, activate stage 00 and advance to the content-source contract before scaffolding the application.

## Minimum resume context
1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-rebuild/CONTEXT.md`
5. `decisions/2026-09-28-portfolio-world-architecture.md`
