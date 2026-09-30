# Stage 07 — certification and preview validation

Status: **preview and independent review PASS; formal ICM certification pending**

## Candidate and preview

- Exact runtime candidate: `27989cb13b989382df69ef2a376f6314f7b9fb6c`
- Certified Stage 06 root: `fe1d15199f06a8a6a2cae22dbc7fa623e75218f6`
- Preview Worker: `vijay-kumaran-portfolio-world-stage07-27989cb`
- Preview URL: <https://vijay-kumaran-portfolio-world-stage07-27989cb.random-planzz.workers.dev>
- Worker version: `e581366f-81ec-4ee3-b0a7-9781fdb6bf19`
- Detailed browser/API evidence: `/tmp/stage07-preview-27989cb/PREVIEW-REPORT.md`; machine-readable evidence: `results.json` and `world-extra.json` in that directory.

## Local regression

- ICM bootstrap, workflow, and strict status: PASS; Stage 00–06 remain certified and Stage 07 is active.
- Offline verification, typecheck, production build, conventional/world asset budgets, Ask disclosure, and world Ask boundary: PASS.
- Full test suite: **11 files / 66 tests PASS**.
- Critical conventional shell bundle: **89.6 KiB gzip**; total client JavaScript: **335.3 KiB gzip**.
- No runtime, dependency, package-lock, or configuration changes were made for this evidence candidate.

## Preview evidence

- Health returned HTTP 200. Grounded PCAS Ask returned `support: grounded`; unsupported revenue returned `insufficient_evidence` with no matches. The visible `/ask` grounded answer exactly matched the API answer.
- `/`, `/projects`, `/resume`, `/ask`, `/contact`, and `/play` passed at 360, 390, 768, 1024, and 1440 px (**30 route/width cases**): zero horizontal overflow, page errors, console errors, failed requests, or HTTP errors.
- Conventional routes did not load `WorldEntry`; initial `/play` did not load district chunks. All five SPA exits (header Ask/Projects/Resume, HUD Contact, Ask Terminal Open Ask) reached the expected route without page errors or failed requests.
- Map semantics/focus, 44 px touch targets, Escape/Close focus restoration, Build Lab fast travel and lazy chunk behavior, reduced motion, and forced no-WebGL fallback passed.
- Persistent zone-label portal host aligned exactly with `.world-canvas` at all target widths and after scroll/resize. Fallback exposed working Projects, Resume, Ask, and Contact links.
- One understood warning remains: `THREE.Clock` deprecation warning on world loads, previously documented in Stage 06 evidence. No application console errors were observed.

## Independent review and protected state

- Terra final Stage 07 preview review: **PASS**, no required fixes.
- `main` remains `63d25e7dbc3169cb41aaa181a513ca7af5860ba4`; production deployment/domain remain unchanged.
- Formal Stage 07 ICM certification has not yet run. This document records evidence, not certification or promotion authority.

## Next action

Run the repository's read-only exact-head Stage 07 certification check. If green, perform formal ICM certification through existing tooling. Any later merge/promotion or production deployment requires a separate explicit approval; no automatic `main` merge or deployment is authorized.
