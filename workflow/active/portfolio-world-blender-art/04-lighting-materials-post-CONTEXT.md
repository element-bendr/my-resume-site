# Stage 04 — Lighting, materials and post-processing

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: local Codex + ChatGPT coordinator
- execution mode: implementation
- parallel-write boundaries: shared world materials, textures, runtime environment/effects, quality tiers, visual evidence

## Inputs

- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified six-zone Blender integration from Stage 03
- finalized reference images
- `docs/portfolio-world/RENDERING-TECHNOLOGY.md`
- `docs/portfolio-world/ASSET-BUDGET.md`
- `docs/portfolio-world/BLENDER-QA-CERTIFICATION.md`

## Objective

Raise the already-correct six-zone geometry toward the approved concept-art quality using coherent materials, lighting, atmosphere and bounded post-processing without changing the certified spatial composition or interaction system.

Stage 04 improves presentation. It does not rescue bad massing.

## In Scope

- shared PBR material refinement;
- palette harmonization across six zones;
- texture baking where geometry alone is wasteful;
- KTX2/Basis path where measured benefit justifies decoder/transcoder cost;
- runtime environment/key/fill/rim lighting;
- sky/background/fog for floating-world depth;
- restrained bloom/ambient-occlusion/tone-mapping only after base materials read correctly;
- quality/reduced-effects tiers;
- measured LODs only where profiling demonstrates need;
- vegetation/material consistency;
- district accent tuning without color-washing entire zones.

## Out of Scope

- rebuilding district massing unless Stage 03 is explicitly reopened;
- changing topology/movement/station semantics;
- introducing WebGPU as a production requirement;
- production deploy/merge;
- unrelated portfolio/content changes.

## Material/lighting principles

- neutral architecture remains dominant;
- vegetation/landscape remains a meaningful scale cue;
- emissive accents remain secondary;
- warm/cool balance follows the finalized references;
- world must remain readable with bloom disabled;
- fog creates depth, not concealment;
- runtime lights remain runtime-owned by default;
- renderer remains WebGL 2.

## Process

1. freeze Stage 03 geometry candidate;
2. record baseline screenshots and transfer/frame measurements;
3. establish shared material palette and texture policy;
4. apply one global lighting/environment pass;
5. compare all six zones before district-specific tuning;
6. introduce textures only where they materially improve fidelity;
7. compress/atlas where justified;
8. add restrained post effects last;
9. define reduced-effects/mobile behavior;
10. recheck all six zones and the conventional fallback;
11. record exact visual/performance deltas.

If materials/lighting reveal a geometry defect, route that defect back to Stage 03 instead of hiding it with effects.

## Outputs

- shared runtime lighting/environment implementation;
- final bounded material palette;
- texture/atlas/KTX2 outputs if introduced;
- decoder/transcoder evidence if introduced;
- quality-tier/reduced-effects configuration;
- six-zone visual comparison evidence;
- updated asset/transfer measurements;
- Stage 04 completion record.

## Acceptance

- all six zones remain readable and coherent;
- finalized-reference fidelity improves materially;
- no scene depends on excessive bloom or fog;
- mobile/reduced-effects path remains usable;
- textures and decoder costs remain within approved lazy-zone budgets;
- visual effects degrade gracefully;
- WebGL 2 remains fully functional;
- no geometry/interaction regression is introduced.

## Verify

```bash
python3 scripts/workflow_status.py --strict
npm run art:verify
npm run verify:offline
npm run typecheck
npm test
npm run build
npm run verify:assets
npm run verify:world-assets
npm run verify:world-zones
```

Visual/performance evidence:

- Command Center + five districts at 1440px;
- Command Center + representative complex district at 390px;
- reduced-motion/reduced-effects view;
- bloom/effects-disabled sanity view;
- transfer size before/after textures;
- decoder/transcoder payload if introduced;
- representative frame-time/FPS comparison before/after Stage 04.

## Protected State

- `main`;
- production deployment/domain;
- verified resume/project content;
- interaction station identities/content/coordinates;
- certified movement/topology/camera/route/accessibility behavior;
- Stage 03 accepted massing unless explicitly reopened;
- user-owned `AGENTS.md`.

## Known closed decisions

- WebGL 2 remains production renderer;
- runtime lights remain runtime-owned by default;
- effects degrade gracefully;
- visual effects cannot substitute for correct massing/material response;
- KTX2/Basis/LOD additions require measured benefit.

## Stop Conditions

- two materially similar visual approaches fail;
- effect/texture cost exceeds approved budgets without measured justification;
- geometry would need to be silently changed to hide a presentation problem;
- an asset requires relaxing a certified behavior/safety boundary;
- required validation cannot be performed;
- unexpected unrelated diff appears;
- user-owned `AGENTS.md` is modified.