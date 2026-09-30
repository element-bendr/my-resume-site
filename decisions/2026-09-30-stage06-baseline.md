# Decision: retain renderer; target measured Stage 06 issues

date: 2026-09-30
status: accepted for Stage 06 setup
owners: coordinator

## Context

The certified Stage 05 candidate was measured before Stage 06 work. Total client JavaScript gzip is 334.7 KiB; the optional `/play` renderer chunk is 956.38 kB raw / 254.75 KiB gzip. Conventional routes do not fetch this chunk, and districts remain lazy. The chunk consists primarily of the expected Three.js/React Three Fiber renderer baseline. Existing asset/world budgets pass.

Browser checks found persistent homepage horizontal overflow at 360/390 px and undersized controls in the world map/HUD. Keyboard opening and Escape-closing of the map worked, but the panel's dialog/disclosure semantics and focus entry require a deliberate accessibility decision.

## Decision

- Preserve the WebGL 2 / Three / React Three Fiber architecture and current route/district code-splitting boundaries.
- Do not suppress or treat the `WorldEntry` advisory as a defect absent evidence of conventional-route transfer or material runtime harm.
- Prioritize the measured homepage overflow, world control target sizes, and map overlay semantics/focus behavior.
- Perform performance changes only after a measured profile shows an actual user-facing issue or existing budget failure.

## Consequences

- Stage 06 begins with narrowly bounded layout/accessibility investigations, not a renderer rewrite or score target.
- Baseline and findings are in `docs/portfolio-world/STAGE-06-BASELINE.md`.
- No production code, dependencies, budgets, protected content, or certified behavior changes in this setup checkpoint.
