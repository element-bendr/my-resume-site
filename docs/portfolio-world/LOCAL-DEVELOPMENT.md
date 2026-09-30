# Local Development and Certification Loop

## Purpose

From Stage 05 onward, use local development for the fast implementation loop while keeping GitHub as the durable source of truth and certification ledger.

## Required baseline

- Node 22.22.x
- npm 11.20.0
- committed package-lock.json
- base branch: feat/portfolio-world-icm-rebuild

## Recommended worktree

Run from the repository root. Fetch before choosing the base and verify the actual remote head. If the worktree or branch already exists, inspect its status and reuse it; do not overwrite or delete it.

```bash
git fetch origin --prune
git status --short --branch
git branch --show-current
git log -1 --oneline origin/feat/portfolio-world-icm-rebuild
git worktree add -b stage05/local-integration .worktrees/stage05-integration origin/feat/portfolio-world-icm-rebuild
cd .worktrees/stage05-integration
nvm use
node --version
npm --version
npm ci
```

Use Node 22.22.x and npm 11.20.0. If npm differs, install the pinned npm version before `npm ci`. Do not use dependency-changing `npm install` for the project; `package-lock.json` is authoritative.

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

Use the smallest relevant test first, then inspect the affected UI/API path in the local browser. For Ask work, keep the request/response contract in `ASK-CONTRACT.md` authoritative for both entry points.

```bash
npm run typecheck
npm test -- --run <relevant-test-file>
npm run dev
```

For Stage 05, exercise `/`, `/play`, `/play?zone=command-center`, `/ask`, `/projects`, `/resume`, and `/api/health`. Check grounded project/experience/skill questions, unsupported and adversarial questions, invalid JSON, wrong method/content type, empty input, and a question over 500 normalized Unicode code points. Confirm the terminal's `Open Ask` action reaches `/ask` and the non-WebGL fallback remains available.

GitHub Actions should be reserved for exact-head final certification and environment-independent evidence.

## Authority rule

Local success is implementation evidence, not formal certification. Durable state must be committed to GitHub.

Use local commands for ordinary editing and verification. Reserve GitHub Actions for final exact-commit certification or evidence that cannot reasonably be produced locally. Do not deploy during Stage 05.

## Protected state

Do not modify main, the production deployment/domain, secrets, unrelated repositories, or certified Stage 00-04 contracts during local iteration.
