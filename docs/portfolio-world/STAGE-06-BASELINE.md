# Stage 06 baseline — 2026-09-30

## Candidate and environment

- certified feature base: `f756316c2826eede6bed2790cb81020f5f34db35`
- isolated branch: `stage06/performance-accessibility`
- runtime: Node `v22.22.0`, npm `11.20.0`; `npm ci` completed using committed lockfile (145 packages)
- `nvm use` could not run because nvm is not installed in this shell; the active runtime exactly matches `.nvmrc` and project npm requirement.
- npm audit reports 4 existing advisories (3 moderate, 1 high); no dependency changes were made.

## Inherited baseline

| Check | Result |
| --- | --- |
| `python3 scripts/bootstrap_check.py` | PASS |
| `python3 scripts/workflow_check.py` | PASS |
| `python3 scripts/workflow_status.py --strict` | PASS; Stages 00–05 certified, Stage 06 blocked awaiting activation, Stage 07 pending |
| `npm run verify:offline` | PASS |
| `npm run typecheck` | PASS |
| `npm test` | PASS; 11 files, 66 tests |
| `npm run build` | PASS |
| `npm run verify:assets` | PASS; critical gzip 89.2 KiB |
| `npm run verify:world-assets` | PASS; total client JS gzip 334.7 KiB |
| `npm run verify:ask-disclosure` | PASS; 8 built JS bundles scanned |
| `npm run verify:world-ask` | PASS; 22 world files, no API/client coupling |

## Bundle and route-loading measurements

- Build output: conventional `index` chunk 277.5 kB raw; `WorldEntry` 956.38 kB raw / 254.75 KiB gzip. Build emits its existing >500 kB chunk advisory for `WorldEntry`.
- Source-map composition attributes the large chunk primarily to Three.js (~2.12M source chars) and React Three Fiber (~713K); Drei contributes ~17K. This is renderer/library weight, not accidental inclusion of district application code.
- `/`, `/projects`, `/resume`, `/ask`, and `/contact` load the conventional index JS/CSS and do not request the WorldEntry/Three/R3F runtime.
- `/play` alone requests WorldEntry and its stylesheet on initial entry. District details remain separate dynamic chunks and were not requested on initial `/play`.
- The heavy chunk is therefore expected for the current optional WebGL renderer and stays within the existing 3 MiB compressed first-visible-3D budget. Do not suppress the warning or rewrite rendering architecture on this evidence alone.

## Browser matrix and concrete findings

Production preview tested at widths 360, 390, 768, 1024, and 1440 px (height 844), across `/`, `/projects`, `/resume`, `/ask`, `/contact`, and `/play`.

1. **Homepage mobile overflow persists.** At 390 px, document width is 424 px (+34); at 360 px it is 392 px (+32). The primary Contact nav link extends to x=392 at 390 px. Other tested routes have no horizontal overflow at 390 px; route matrix showed no overflow at 768/1024/1440.
2. **World map touch targets are small.** At 390 px, the Map button is 49×33 px and Close map is 32×32 px. Both are keyboard-operable buttons; improve touch size/spacing without changing map behavior.
3. **World navigation touch targets are slightly short.** At 390 px the shared header links are 43 px tall; the Command Center overlay Projects/Resume/Contact links are 52×15, 53×15, and 51×15 px. Review mobile touch affordance while preserving compact visual direction.
4. **Map overlay semantics/focus need review.** Opening the map by keyboard works and Escape closes it, returning focus to the Map trigger. The visible map panel has no `role=dialog`/`aria-modal` and keyboard focus remains on the trigger rather than moving into the panel; assess whether it is a dialog or non-modal disclosure and make semantics/focus consistent. No movement regression was assessed by this setup-only pass.

No missing accessible names were found among tested native controls; `/ask` textarea has associated “Your question” label and hint/count description. Main/header/nav/footer landmarks were present on tested conventional routes. This is an exploratory DOM/browser baseline, not a formal WCAG conformance audit; contrast and assistive-technology review remain Stage 06 work.

## Motion, fallback, console, and network

- With `prefers-reduced-motion: reduce`, browser reports the preference active and document scroll behavior is `auto`; Stage 06 should verify world camera/decorative motion in addition to this conventional-page observation.
- Forced failure of WebGL context creation on `/play` rendered the `3D UNAVAILABLE` fallback with Projects, Resume, Ask, and Contact links. No fallback defect found.
- Browser route matrix produced no failed requests and zero console errors. `/play` logged a Three.js `Clock` deprecation warning and headless Chromium/GL `ReadPixels` GPU stall warnings; no app call site for `Clock` was found. Record and reassess in a normal target browser; GPU messages are environment-sensitive.
- Conventional route request inspection showed no duplicate renderer transfer or unexpected API request. No broken fonts/images/scripts were observed.

## Baseline decision

Retain the existing renderer and district split. Prioritize the evidenced homepage overflow and mobile world-control/focus review. Broader performance changes require profiling that demonstrates a material user-facing gain; do not chase synthetic scores or the existing expected world chunk advisory.
