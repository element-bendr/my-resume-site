# Stage 05 — Performance and accessibility certification

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: local Codex + ChatGPT coordinator
- execution mode: certification
- parallel-write boundaries: validation fixes/evidence only; no discretionary visual redesign

## Inputs

- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified Stage 04 visual candidate
- `docs/portfolio-world/BLENDER-QA-CERTIFICATION.md`
- `docs/portfolio-world/ASSET-BUDGET.md`
- `docs/portfolio-world/RENDERING-TECHNOLOGY.md`

## Objective

Prove the complete six-zone Blender world remains performant, accessible, failure-tolerant and usable across the production viewport/capability matrix before promotion.

## In Scope

- 360/390/768/1024/1440 viewport matrix;
- movement/fast-travel/station regressions;
- route exit/focus checks;
- reduced-motion/reduced-effects behavior;
- touch/coarse-pointer behavior;
- forced no-WebGL fallback;
- forced GLB/asset failure behavior;
- transfer/decode/frame-time review;
- memory/leak sanity while travelling between zones;
- console/network error review;
- conventional Resume/Projects/Ask/Contact route regression;
- narrowly scoped fixes for certification failures.

## Out of Scope

- discretionary visual redesign;
- new districts/features;
- production deployment/domain changes;
- content/Ask changes;
- topology/movement changes unless fixing a proven regression through a separately reviewed decision.

## Dependencies

- certified Stage 04 visual candidate
- `docs/portfolio-world/BLENDER-QA-CERTIFICATION.md`

## Process

1. freeze the exact Stage 04 candidate;
2. run all repository gates;
3. run the full viewport/browser matrix;
4. traverse every zone through fast travel and normal movement;
5. exercise every station class and Ask interaction;
6. force reduced motion;
7. force no-WebGL;
8. force at least one GLB failure path;
9. record transfer/decode/frame-time evidence;
10. inspect console/network for errors/404 loops;
11. fix only evidenced certification failures;
12. rerun the affected gate and the full final gate set;
13. obtain independent review on the exact candidate.

## Outputs

- `docs/portfolio-world/BLENDER-VALIDATION.md`
- exact candidate SHA/evidence
- viewport/browser matrix evidence
- performance/transfer measurements
- fallback/failure evidence
- independent review findings
- Stage 05 completion record.

## Acceptance

- all repository gates pass;
- all browser/runtime gates pass;
- conventional routes remain complete;
- keyboard/focus/touch/reduced-motion remain usable;
- forced no-WebGL and GLB-failure paths remain non-blank and useful;
- no unresolved console/network errors;
- no unresolved material performance regression;
- lazy district behavior remains intact;
- exact candidate has independent review PASS.

## Verify

Repository gates:

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
npm run art:verify
npm run verify:ask-disclosure
npm run verify:world-ask
npm run verify:world-zones
```

Browser/runtime matrix:

- 360px
- 390px
- 768px
- 1024px
- 1440px

Required scenarios:

- `/play` initial load;
- Command Center movement/Ask;
- all five district fast-travel destinations;
- keyboard movement;
- click/tap movement;
- district station interactions;
- map open/close and focus behavior;
- route exits;
- reduced motion/effects;
- forced no-WebGL;
- forced GLB failure;
- repeated district travel for memory/resource sanity;
- network/console review.

## Protected State

- `main`;
- production deployment/domain;
- verified resume/project content;
- certified interaction/topology/movement/camera semantics;
- Stage 04 accepted visual direction except for fixes required by certification;
- user-owned `AGENTS.md`.

## Known closed decisions

- visual polish cannot override accessibility/fallback;
- performance exceptions require evidence and explicit decision;
- Stage 05 fixes are certification-driven, not feature work;
- a technically green repo without browser/failure evidence is not certified.

## Stop Conditions

- two materially similar fixes fail to resolve a certification defect;
- a proposed fix weakens accessibility/fallback to recover performance;
- required browser/performance validation cannot be performed;
- unexpected unrelated diff appears;
- user-owned `AGENTS.md` is modified.
