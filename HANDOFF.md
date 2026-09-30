# Current Handoff

## Goal
Finish Stage 06 performance/accessibility hardening through a GitHub↔local feedback loop: GitHub freezes each bounded lane and review trail; the local Stage 06 worktree executes browser/runtime validation, fixes only evidenced failures, and writes results back before Stage 06 certification. Preserve Stages 00–05 and keep `main` and production untouched.

## Phase
STAGE_06_CANVAS_ROUTE_TEARDOWN_BLOCKED

## Execution mode
implementation

## Authority / location
- repository: element-bendr/my-resume-site
- canonical branch: main
- working branch/worktree: stage06/canvas-route-teardown / .worktrees/stage06-performance
- application candidate: feat/portfolio-world-icm-rebuild @ d36e5fb65d40a669e9d260e8356962f4413d922b
- active workflow/stage: workflow/active/portfolio-world-rebuild / 06-performance-accessibility
- template source: ICM 2.1.0 @ 90322a2441539f24eafdbd2c8a36bc6392192af4

## Current state
Stages 00–05 are formally certified. Stage 05 application candidate `d36e5fb65d40a669e9d260e8356962f4413d922b` passed exact-head GitHub Actions run [36568411611](https://github.com/element-bendr/my-resume-site/actions/runs/36568411611); final Terra review passed; formal ICM certification passed in run [36569532413](https://github.com/element-bendr/my-resume-site/actions/runs/36569532413). Certification state commit is `f756316c2826eede6bed2790cb81020f5f34db35`. Stage 06 contract and measured baseline were committed as `c0507383025ca191264df1f31b42410624fb259b`; Stage 06 was activated using `scripts/workflow_activate.py`.

Stage 06 lanes 1–4 are frozen through merged PR #9. Failed final-audit evidence from PR #10 is persisted in the Stage 06 root at `42f6820072cbc82abda32b10d1ad938eae191273`. Lane 5 on `stage06/canvas-route-teardown` reproduced the `/play` SPA-exit React DOM `removeChild` failure at pickup `ecce3e529eee7c3d1fdb7b0e8e699cdbe9ac9163`. Two bounded manual R3F unmount attempts (`unmountComponentAtNode`, then the same under `flushSync`) both failed and were reverted. Terra confirmed the stop rule; there is no promotable runtime candidate on PR #11. Stage 06 remains active; certification was not run. The next materially different repair is a persistent `SiteShell`-owned Drei `Html portal` host outside the routed `Outlet`. Stage 07 remains pending.

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
- Stage 05 application candidate: `d36e5fb65d40a669e9d260e8356962f4413d922b`
- Stage 05 exact-head run [36568411611](https://github.com/element-bendr/my-resume-site/actions/runs/36568411611): success; 11 files / 66 tests; build, guards, budgets, HTTP, Ask UI, terminal route, and fallback checks PASS
- Stage 05 independent Terra review: PASS; protected Stage 00–04 state: PASS
- Stage 05 formal ICM certification run [36569532413](https://github.com/element-bendr/my-resume-site/actions/runs/36569532413): PASS; certification state commit: `f756316c2826eede6bed2790cb81020f5f34db35`
- Stage 00–05: certified; Stage 06: active; Stage 07: pending
- Stage 06 contract/baseline commit: `c0507383025ca191264df1f31b42410624fb259b`
- Stage 06 activation: completed using existing ICM tooling; active stage 06, Stage 07 pending
- Stage 06 lane 1 PR #6: `stage06/performance-accessibility` @ `61900faf6e7510b8cd99db0e5d39a77d850c3b8e`; homepage overflow lane PASS
- Stage 06 lane 2 PR #7: MERGED into `stage06/performance-accessibility` at `16ae381aa1bbf7f04da1873993dbf8378bc0be7d`; local runtime/browser certification PASS; Terra PASS; protected state intact
- Stage 06 lane 3 PR #8: MERGED into `stage06/performance-accessibility` at `6067c3203186819d92dfacfbb4b028aa8655d834`; local validation PASS; Terra PASS; protected state intact
- Stage 06 lane 4 PR #9: MERGED into `stage06/performance-accessibility` at `04dfec1a24de9a86cc5f73ec1e3e4f23418e2579`; local validation PASS; Terra PASS; protected state intact
- Stage 06 final audit pickup: `stage06/final-acceptance-audit` @ `79ccc4f3210e2bdb71b3867484578ae7928da437`
- Stage 06 final audit non-browser gates: PASS; ICM checks, offline verification, typecheck, 66/66 tests, build, budgets, Ask disclosure, and world Ask boundary guard
- Stage 06 final audit browser matrix: PASS for 360/390/768/1024/1440 route overflow, conventional-route world isolation, initial `/play` district laziness, Ask overlay focus/Escape/movement resume, and route rendering
- Stage 06 final audit blocker: SPA exits from `/play` via header Ask/Projects/Resume, world HUD Contact, and Ask Terminal Open Ask reach their destination but emit `NotFoundError: Failed to execute 'removeChild' on 'Node'`; instrumentation isolated the stale removal to a disconnected Drei `Html` world-label portal during full Canvas teardown
- Stage 06 final Terra audit: **FAIL**; certification blocked; failed-audit evidence merged by PR #10 at `42f6820072cbc82abda32b10d1ad938eae191273`
- Stage 06 lane 5 PR #11: `stage06/canvas-route-teardown`; BLOCKED at pickup `ecce3e529eee7c3d1fdb7b0e8e699cdbe9ac9163`; two manual R3F unmount approaches failed/reverted; Terra confirmed stop rule; no runtime candidate
- Stage 06 certification: NOT RUN; Stage 06 remains active and Stage 07 remains pending
- Feedback-loop rule: GitHub is canonical contract/review state; local `.worktrees/stage06-performance` executes exact-head validation and bounded repairs; results are committed/pushed back to the current active lane PR before further Stage 06 work
- Superseded workflow-order run [36568111222](https://github.com/element-bendr/my-resume-site/actions/runs/36568111222): failure because disclosure scan ran before build; corrected run 36568411611 passed

## Protected state
- main / production baseline: UNCHANGED
- secrets/credentials: UNCHANGED
- current production deployment/domain: UNCHANGED
- unrelated repositories: UNCHANGED

## Stale / uncertain state
- education is intentionally unresolved and excluded until verified;
- LinkedIn URL is excluded until directly verified;
- client testimonials/outcome claims require evidence before inclusion;
- Stage 03 Command Center and Stage 04 six-zone world are certified. Stage 05 must preserve the certified controller, browser fallback, direct-route behavior, and shared world architecture.

## Next atomic action
Freeze PR #11 as diagnostic evidence only; do not treat it as a successful repair. Then open a materially different Stage 06 lane using Drei's public `Html portal` API with a persistent host owned by `SiteShell` outside the routed `Outlet`.

The next lane must:
- create one dedicated DOM host whose lifetime is the persistent `SiteShell`, not the routed `/play` subtree;
- expose that host to the lazy world through the smallest typed React context/ref bridge;
- pass the persistent host ref only to the zone-label Drei `Html` instances in `WorldTopology`;
- preserve the existing PR #9 rule that non-Command-Center label portals remain mounted during fast travel and hide the current label with `visibility`;
- keep the portal host non-interactive/decorative and prevent it from disturbing page layout, stacking, focus order, or accessibility;
- preserve all dependencies and renderer architecture.

First prove in-world label projection, positioning, visibility, z-order, and resizing at desktop and 390px. Then prove all five `/play` SPA exits have zero runtime/page errors and zero failed requests. Re-run fast travel, map focus, lazy districts, route isolation, touch sizing, overflow, full repository gates, and Terra.

If that candidate fails, stop and return evidence rather than layering another teardown workaround. Do not certify Stage 06, activate Stage 07, touch `main`, or deploy.

## Minimum resume context
1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-rebuild/06-performance-accessibility-CONTEXT.md`
5. `docs/portfolio-world/STAGE-06-BASELINE.md`
6. `docs/portfolio-world/ASK-CONTRACT.md`
7. `decisions/2026-09-28-portfolio-world-architecture.md`
8. PR #7 (`stage06/world-map-touch-targets`) exact-head diff and local validation evidence

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
- `07b7253`: connected Ask Terminal to `/ask` with a dedicated accessible overlay action; added typed legal-area/essential-route assertions and `npm run verify:world-ask` boundary guard (22 world source files, no Ask API/client coupling). Focused world/routes/WebGL tests PASS (14); typecheck, bootstrap/workflow/strict status, offline checks, full suite (11 files / 66 tests), build, conventional/world asset budgets, and Ask disclosure scan PASS. Browser: desktop station activation, Escape close/resumed movement/reopen, Open Ask navigation, direct `/ask`, and exact equality between visible PCAS answer and raw API response PASS; at 390×844 dialog/action remained visible. Forced WebGL context failure preserved the conventional fallback with Ask route. Browser artifacts are in `/tmp/.playwright-cli/`.
- blockers: none; no deploy or push performed
- protected state: `main`, production, and certified Stage 00–04 stage records unchanged


## Stage 04 evidence
- application candidate: f404ce032000e3d7c86f5e29748a9e1b634df3a1
- GitHub Actions run: 36521705441
- tests: 7 files / 31 tests PASS
- total client JS: 333.3 KiB gzip
- browser proof: Command Center + five districts + non-WebGL fallback PASS
