# Stage 05 — Grounded Ask Integration

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: stage05/local-integration / `.worktrees/stage05-integration`
- owner: Luna
- execution mode: implementation
- parallel-write boundaries: one implementation owner across `src/ask/**`, Worker Ask routing, `/ask`, terminal navigation, tests, and Stage 05 evidence

## Inputs

- Stage 00–04 certified state recorded in `workflow/active/portfolio-world-rebuild/state.json`
- `docs/portfolio-world/ASK-CONTRACT.md`
- `docs/portfolio-world/CONTENT-CONTRACT.md`
- `docs/portfolio-world/LOCAL-DEVELOPMENT.md`
- typed registry under `src/content/`
- existing `worker/index.ts`, `src/app/pages/AskPage.tsx`, and Command Center terminal overlay
- inherited baseline commit `fbbb08e84a9455655f3ac5fb92f496faa538f747`

## Objective

Deliver one deterministic, evidence-grounded Ask experience usable from `/ask` and the Command Center Ask Terminal, with the frozen contract in `docs/portfolio-world/ASK-CONTRACT.md`.

## In Scope

- normalized public-safe evidence registry, deterministic retrieval, and answer composition;
- `POST /api/ask` validation and stable response contract;
- accessible conventional Ask page with loading, grounded, insufficient-evidence, and error states;
- Ask Terminal navigation to the canonical `/ask` page;
- focused retrieval, answer, API, and integration tests;
- Stage 05 validation and handoff evidence.

## Out of Scope

- changing `main`, deploying, or changing production configuration;
- changing the certified movement, controller, camera, world topology, rendering, fallback, or six-zone architecture;
- adding an external LLM, credentials, persistence, analytics, visitor accounts, new dependencies, or Cloudflare storage products;
- publishing claims outside the certified public-safe content registry;
- unrelated route, design, or infrastructure refactors.

## Dependencies

- Stages 00–04 remain certified and current.
- `package-lock.json` and pinned dependencies remain authoritative.
- Only records and fields approved by `docs/portfolio-world/CONTENT-CONTRACT.md` may support answers.
- Both user entry points use the same HTTP and evidence contract.

## Process

1. Recheck the isolated worktree, branch head, and protected state.
2. Run the inherited local baseline before application changes.
3. Add deterministic evidence normalization, retrieval, and composer with focused tests.
4. Add Worker request validation and contract tests; preserve `GET /api/health`.
5. Replace the `/ask` placeholder and connect the world terminal to that route.
6. Run focused tests, then the local full gate and browser/API paths in `LOCAL-DEVELOPMENT.md`.
7. Inspect the complete diff and update validation evidence and `HANDOFF.md`.
8. Stop at the locally green candidate for independent Terra review; do not deploy or modify `main`.

## Outputs

- `docs/portfolio-world/ASK-CONTRACT.md`
- `docs/portfolio-world/LOCAL-DEVELOPMENT.md`
- `src/ask/` evidence, retrieval, and answer modules
- `worker/` Ask endpoint integrated with existing health routing
- conventional `/ask` and Command Center terminal integration
- focused Ask tests and Stage 05 validation evidence
- updated `HANDOFF.md` and `workflow/active/portfolio-world-rebuild/output/05-integration-completion-report.md`

## Acceptance

- grounded, insufficient-evidence, and invalid-request states follow the frozen schema;
- questions are normalized, bounded, validated, and never persisted or logged raw;
- retrieval order and answers are deterministic and use only public-safe evidence;
- unsupported/adversarial questions fail closed and reveal no private source data;
- `/ask` and the terminal action use the same endpoint and experience;
- the existing health endpoint and all certified Stage 00–04 behavior pass inherited and focused checks;
- local browser/API checks pass and independent Terra review is requested before certification.

## Verify

- `python3 scripts/bootstrap_check.py`
- `python3 scripts/workflow_check.py`
- `python3 scripts/workflow_status.py --strict`
- `npm run verify:offline`
- `npm run typecheck`
- focused Ask tests, then `npm test`
- `npm run build`
- `npm run verify:assets`
- `npm run verify:world-assets`
- local browser and API scenarios in `docs/portfolio-world/LOCAL-DEVELOPMENT.md`
- final diff, status, and protected-state check

## Protected State

- `main` and production deployment/domain remain unchanged;
- Stages 00–04 and their evidence remain certified and unmodified;
- six-zone world, single PlayerController/CameraRig, legal-area movement, fast travel, lazy districts, WebGL 2 path, and HTML fallback remain intact;
- no secret, private repository/source content, unsupported resume claim, or raw user question is exposed.

## Known closed decisions

- no LLM is required for the baseline Ask system;
- no persistence, account, database, KV, R2, Durable Object, or physics/navmesh dependency is authorized;
- the canonical full Ask experience is `/ask`; the world terminal navigates there;
- response fields and input limits are frozen in `docs/portfolio-world/ASK-CONTRACT.md`.

## Stop Conditions

- inherited certified baseline fails after environment/dependency diagnosis;
- an answer requires unsupported, stale, private, or contradictory evidence;
- a secret or credential appears in source/configuration;
- implementation requires a protected Stage 00–04 architecture change or dependency upgrade;
- two materially similar implementation attempts fail;
- validation cannot prove protected state remains unchanged.
