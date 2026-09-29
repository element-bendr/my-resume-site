# Local Development and Certification Loop

## Purpose

From Stage 05 onward, use local development for the fast implementation loop while keeping GitHub as the durable source of truth and certification ledger.

## Required baseline

- Node 22.22.x
- npm 11.20.0
- committed package-lock.json
- base branch: feat/portfolio-world-icm-rebuild

## Recommended worktree

```bash
git fetch origin
git worktree add -b stage05/local-integration .worktrees/stage05-integration origin/feat/portfolio-world-icm-rebuild
cd .worktrees/stage05-integration
nvm use
npm ci
```

## Baseline checks

```bash
python3 scripts/bootstrap_check.py
python3 scripts/workflow_check.py
python3 scripts/workflow_status.py --strict
npm run verify:offline
npm run typecheck
npm test
npm run build
npm run verify:assets
npm run verify:world-assets
```

## Inner loop

Use targeted local tests and browser preview after each coherent change.

```bash
npm run typecheck
npm test -- --run <relevant-test-file>
npm run dev
```

GitHub Actions should be reserved for exact-head final certification and environment-independent evidence.

## Authority rule

Local success is implementation evidence, not formal certification. Durable state must be committed to GitHub.

## Protected state

Do not modify main, the production deployment/domain, secrets, unrelated repositories, or certified Stage 00-04 contracts during local iteration.
