# Portfolio World Blender Art Upgrade

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: ChatGPT coordinator
- execution mode: implementation
- parallel-write boundaries: Blender/art pipeline, portfolio-world art docs, world scenery integration and workflow evidence only; unrelated content/API/deployment state remains protected

## Inputs

- certified Portfolio World runtime on `main` at `5f4de7ace37bfd843ef13f035a3b16ddb61f28d7`
- `decisions/2026-10-01-blender-world-art.md`
- `docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
- `docs/portfolio-world/BLENDER-AUTHORING-GUIDE.md`
- `docs/portfolio-world/BLENDER-QA-CERTIFICATION.md`
- existing topology, movement, camera, interaction and fallback contracts

## Objective

Replace primitive-heavy scenery with reproducible Blender-authored GLB art while preserving the certified Portfolio World behavior and production fallback guarantees.

## In Scope

- Blender-authored scenery for all six zones
- deterministic GLB generation/export
- typed R3F scene-loading boundary
- district-local visual placement
- material/texture/LOD pipeline
- runtime lighting and post-processing after geometry stabilizes
- visual/performance/accessibility certification
- explicit merge/promotion evidence

## Out of Scope

- changes to resume facts/content authority
- changing world bounds to fit art
- changing interaction station coordinates to fit art
- multiplayer, physics, combat or jumping
- WebGPU production migration
- unrelated Cloudflare backend changes
- automatic production deployment

## Dependencies

- certified runtime behavior and evidence from the completed `portfolio-world-rebuild` workflow
- `src/world/world-topology.ts`
- `src/world/world-config.ts`
- `docs/portfolio-world/ASSET-BUDGET.md`
- `docs/portfolio-world/RENDERING-TECHNOLOGY.md`

## Process

1. Freeze art/runtime authority boundaries.
2. Generate and validate the six baseline GLBs.
3. Integrate Command Center as the first visual slice.
4. Validate camera, movement, interaction, mobile and performance.
5. Roll out remaining districts without changing topology authority.
6. Add lighting/post-processing/textures only after geometry is stable.
7. Run full regression and visual certification.
8. Merge only an exact green candidate; production promotion remains separate.

## Outputs

- Blender generator/source
- six bounded GLBs
- runtime loader/placement contract
- per-zone integration
- visual/performance evidence
- updated handoff and certification records

## Acceptance

- all six zones use certified Blender scenery;
- no required runtime behavior regresses;
- conventional routes/fallback remain first-class;
- asset/performance budgets pass;
- browser visual evidence demonstrates materially improved fidelity;
- exact candidate passes repository and independent review gates.

## Verify

- `npm run art:blender`
- `npm run art:verify`
- repository full verification commands in `docs/portfolio-world/BLENDER-QA-CERTIFICATION.md`
- production-build browser matrix at 360/390/768/1024/1440

## Protected State

- `main`
- current production deployment/domain
- verified portfolio content and Ask contract
- movement/topology/camera semantics
- interaction station identities and factual content
- secrets/credentials
- certified historical workflow evidence

## Known closed decisions

- Blender is the canonical authored scenery pipeline for this upgrade.
- GLBs are visual scenery, not navigation/collision authority.
- WebGL 2 remains the production renderer.
- conventional HTML remains the essential-content fallback.
- no production promotion occurs from an uncertified art candidate.

## Stop Conditions

- asset requires changing certified topology merely to fit;
- GLB budget cannot be met without an explicit architecture decision;
- visual integration breaks movement, focus, route teardown or fallback;
- two materially similar repair attempts fail;
- required evidence is unavailable or contradictory.
