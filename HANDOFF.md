# Current Handoff

## Goal
Implement Stage 05 integration: one grounded Ask experience shared by `/ask` and the in-world Command Center terminal, preserving all certified Stage 00–04 behavior and keeping `main` untouched.

## Phase
STAGE_05_INTEGRATION

## Execution mode
implementation

## Authority / location
- repository: element-bendr/my-resume-site
- canonical branch: main
- working branch/worktree: stage05/local-integration / .worktrees/stage05-integration
- active workflow/stage: workflow/active/portfolio-world-rebuild / 05-integration
- template source: ICM 2.1.0 @ 90322a2441539f24eafdbd2c8a36bc6392192af4

## Current state
Stages 00–04 are certified in the fetched integration state. Stage 05 contract is frozen in `docs/portfolio-world/ASK-CONTRACT.md` and `workflow/active/portfolio-world-rebuild/05-integration-CONTEXT.md`; local-first runbook is updated in `docs/portfolio-world/LOCAL-DEVELOPMENT.md`. The deterministic public-safe evidence registry, retrieval, and evidence-only answer composer are implemented in `src/ask/`. `POST /api/ask` is implemented in `worker/ask.ts` and routed beside the preserved health endpoint. The conventional `/ask` UI now calls the shared API and shows answers, evidence, and public source labels; the world terminal integration remains pending. Inherited baseline passed on `fbbb08e84a9455655f3ac5fb92f496faa538f747` before documentation changes.

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
- the Command Center Ask Terminal still needs to link to the canonical `/ask` experience;
- Stage 03 Command Center and Stage 04 six-zone world are certified. Stage 05 must preserve the certified controller, browser fallback, direct-route behavior, and shared world architecture.

## Next atomic action
Connect the Command Center Ask Terminal to the canonical `/ask` experience. Keep world state independent of API availability; do not add an LLM or storage dependency. After both entry points, rerun the final browser/API checks and request independent Terra review.

## Minimum resume context
1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-rebuild/05-integration-CONTEXT.md`
5. `docs/portfolio-world/ASK-CONTRACT.md`
6. `decisions/2026-09-28-portfolio-world-architecture.md`

## Stage 05 setup / validation
- remote integration head fetched: `fbbb08e84a9455655f3ac5fb92f496faa538f747`
- latest local contract commit: `dbadd02f47d99687a3712374ffd07a7b2132ec45` (stable transport error codes; workflow check and strict status PASS)
- local runtime: Node 22.22.0, npm 11.20.0; `npm ci` PASS
- inherited baseline: bootstrap, workflow check/status, offline verification, typecheck, tests (7 files / 31 tests), build, conventional asset budget, and world asset budget all PASS
- `49f81c37992700c2a74803efba5f5c81833a218f`: deterministic public-safe evidence registry, normalization, retrieval, and evidence-only answer composer; focused Ask tests, typecheck, and full test suite PASS (9 files / 42 tests)
- retrieval uses certified technology phrases with maximal-phrase filtering, so a nested generic term cannot broaden exact project-tech matching
- `5a32eb210da5a23a86c17cd22aac109906408d5a`: added explicit public-safe/fact invariants, verified source-reference shape, conservative unsupported-intent fail-closed gate, hobby-category scoping, and exact project status composition; focused Ask tests PASS (14), typecheck PASS, full suite PASS (9 files / 45 tests)
- `974842d6b30be532465ae9f00b66d09167d46e2a`: source validator now enforces the existing visibility enum and hobby evidence requires exact `user-approved` provenance; malformed-value regression tests added. Focused Ask tests PASS (14), typecheck PASS, full suite PASS (9 files / 45 tests)
- `3af9ddf8bac017c722152aee690e4d8d03584a93`: added bounded, non-logging `POST /api/ask` transport with stable error envelope/codes, 500-code-point and 4096-byte limits, strict JSON shape/content type, method handling, and no-store/security headers; health and unknown API routes preserved. Worker tests PASS (15), Ask tests PASS (29), typecheck PASS, full suite PASS (9 files / 58 tests), offline/workflow checks PASS, build and both asset budgets PASS. Local Vite/Worker HTTP smoke PASS for health, grounded, insufficient-evidence, malformed JSON, oversized body, wrong method, and unknown API route.
- `b389a666d1ffc2eac0cf2423925628931b980e80`: built the accessible conventional Ask UI and typed client; shared API limits/error types live in `src/ask/types.ts`. The client validates the frozen response envelope, bounds normalized question length, and preserves aborts. `/ask` presents loading/error/insufficient states, grounded answers, matched evidence, and public source labels only. Focused client/Worker tests PASS (21); typecheck PASS; full suite PASS (10 files / 64 tests); workflow/bootstrap/offline checks, production build, and both asset budgets PASS. Browser matrix PASS for PCAS, Cloudflare Workers projects, HCL experience, Python, hobbies, metric, AWS certifications, prompt injection, oversized local input, and network-offline error. Browser-side strict comparison confirmed the visible PCAS answer equals `POST /api/ask` answer exactly. `/ask` has no horizontal overflow at 1440, 768, and 390 px. Shared mobile header containment was fixed with a two-rule media-query change; `/projects` and `/resume` remain 390 px wide without overflow. `/` retains an unrelated pre-existing 34 px hero-heading overflow at 390 px; left out of scope.
- `98a6b07`: addressed Terra's Ask disclosure/accessibility findings. `/ask` now imports a browser-safe map containing only approved public source labels and uses a neutral label for other refs. The unused content `sourceIds` export was removed so the full source registry is tree-shaken from client JS. Added `npm run verify:ask-disclosure` to reject internal labels and `internal-reference` in built client bundles. Error alert has a stable ID conditionally included in the textarea description. Ask/Worker/content tests PASS (27), typecheck/build PASS, disclosure scan PASS (8 client bundles). Browser smoke at 390 px confirmed no horizontal overflow, matching `aria-describedby`/alert association, and neutral labeling for an internal-only hobby source.
- blockers: none; no deploy or push performed
- protected state: `main`, production, and certified Stage 00–04 stage records unchanged


## Stage 04 evidence
- application candidate: f404ce032000e3d7c86f5e29748a9e1b634df3a1
- GitHub Actions run: 36521705441
- tests: 7 files / 31 tests PASS
- total client JS: 333.3 KiB gzip
- browser proof: Command Center + five districts + non-WebGL fallback PASS
