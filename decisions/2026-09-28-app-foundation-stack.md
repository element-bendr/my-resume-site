# Decision: React/Vite/Cloudflare application foundation

date: 2026-09-28
status: accepted
owners: coordinator
supersedes: none
superseded_by: none

## Context

Portfolio World needs a conventional, accessible application shell before the 3D experience is added. Cloudflare's current Workers documentation recommends its Vite plugin for React SPAs with Static Assets and an optional API Worker. The foundation must also remain small enough that Stage 03 can add Three.js without turning the first load into a shipping container.

Current stable ecosystem evidence reviewed on 2026-09-28:
- React 19.3 is the current stable React line;
- Vite 8 is stable and uses Rolldown;
- Cloudflare's Vite plugin supports SPA/static assets and Worker APIs;
- Cloudflare recommends `not_found_handling: "single-page-application"` and supports `run_worker_first: ["/api/*"]`.

## Decision

Stage 02 uses:

Runtime dependencies:
- `react` 19.3.0
- `react-dom` 19.3.0
- `react-router` 8.4.0

Development dependencies:
- `vite` 8.3.0
- `@vitejs/plugin-react` 6.1.1
- `@cloudflare/vite-plugin` 1.54.8
- `wrangler` 4.131.1
- `typescript` 7.0.2
- `vitest` 5.0.0
- `@types/react` 19.3.0
- `@types/react-dom` 19.3.0
- `@types/node` 22.20.4

Node baseline:
- Node 22.x; local reference runtime 22.16.0.

Version policy:
- exact versions in `package.json`;
- lockfile required before Stage 02 certification;
- do not automatically chase same-day package releases during an active certified build;
- dependency upgrades are deliberate changes with build/test evidence.

Cloudflare configuration:
- official `@cloudflare/vite-plugin`;
- SPA fallback through Static Assets;
- `worker/index.ts` for API routes;
- Worker-first routing restricted to `/api/*`;
- no persistence bindings in Stage 02.

React Three Fiber, Three.js, Drei, WebGPU-specific code, and Wasm-specific application code are deliberately deferred to Stage 03 or later.

## Consequences

- the ordinary portfolio can be built, tested, indexed, and used independently of 3D;
- Stage 03 receives a stable app/content/API boundary;
- package/runtime risk is isolated before introducing GPU complexity;
- exact dependency pins make later certification reproducible;
- the current no-network execution environment can author the foundation but cannot certify dependency installation/build until a lockfile and real install exist.

## Validation / evidence

- Cloudflare Workers React/Vite documentation checked 2026-09-28;
- React 19.3 stable release documentation checked 2026-09-28;
- Vite 8 stable/current package evidence checked 2026-09-28;
- exact package installation/build remains a Stage 02 gate.

## Revisit when

- package installation reveals peer/version incompatibility;
- Cloudflare Vite plugin build/preview behavior conflicts with the documented pattern;
- bundle-size evidence shows React Router or another dependency is unjustified;
- a later certified upgrade is intentionally scheduled.
