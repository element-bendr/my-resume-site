# Portfolio World Art v2 — Asset-Based Hero Scene

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: `visual/world-art-v2-reference-match` / `.worktrees/visual-world-art-v2-reference-match`
- owner: Luna implementation; Sol visual acceptance; Terra independent review
- execution mode: implementation
- baseline: PR #17 certified visual foundation at `3399ab48e392cbf33b79ad22440075777b12f082`
- user visual verdict on v1: REJECTED

## Inputs

- approved generated floating-world reference
- `docs/portfolio-world/VISUAL-REFERENCE-CONTRACT.md` as the canonical implementation translation of that image
- user-supplied screenshot proving v1 mismatch
- `docs/portfolio-world/VISUAL-OVERHAUL-V2.md`
- `docs/portfolio-world/VISUAL-ASSET-SOURCES.md`
- certified movement/navigation/content/runtime from prior workflows

## Objective

Produce one Central Plaza hero scene that materially approaches the approved visual reference using curated real modular glTF assets, PBR materials, vegetation/props, stronger vertical architecture and cinematic composition, while preserving controller/topology/content behavior.

## In Scope

- curate a small CC0 glTF asset subset from approved sources;
- vendor only selected assets needed for the hero scene;
- record source/license/size for every asset;
- use GLTFLoader/useGLTF through Drei for render assets;
- separate simple walkable/collision surfaces from render geometry;
- Central Plaza architecture, one bridge and distant district silhouettes;
- vegetation and scale props;
- lighting/material refinement;
- visual camera composition tuning without changing movement/input semantics;
- proper low-poly player GLB if a suitable CC0 asset fits budget, otherwise retain current player temporarily.

## Out of Scope

- rebuilding all five districts before hero-scene visual approval;
- movement algorithm/constants changes;
- topology graph/bounds/fast-travel changes;
- station behavior/content/Ask/routing changes;
- WebGPU;
- production deployment;
- importing entire asset packs.

## Dependencies

- Quaternius Modular Sci-Fi MegaKit, CC0, glTF;
- Kenney City Kit Industrial, CC0;
- Kenney City Kit Commercial, CC0;
- frozen repository asset budgets.

## Process

1. Activate this workflow through ICM tooling.
2. Download approved asset packs locally outside the repository.
3. Inspect asset names/thumbnails and curate the minimum hero-scene subset.
4. Copy only selected glTF/GLB + required textures into `public/world/assets/v2/`.
5. Record every vendored file in `docs/portfolio-world/VISUAL-ASSET-MANIFEST.md`.
6. Implement a Central Plaza asset scene with one bridge and distant silhouettes.
7. Tune camera composition and lighting for the hero screenshot without modifying controller math.
8. Run typecheck/tests/build/budgets/guards.
9. Capture 1440px and 390px hero screenshots.
10. Compare the 1440px hero screenshot line-by-line against `VISUAL-REFERENCE-CONTRACT.md`.
11. Stop for user visual acceptance before district propagation.
12. Terra reviews technical/protected-state quality after visual acceptance candidate exists.

## Outputs

- `docs/portfolio-world/VISUAL-ASSET-MANIFEST.md`
- `docs/portfolio-world/VISUAL-OVERHAUL-V2-VALIDATION.md`
- curated assets under `public/world/assets/v2/`
- hero-scene implementation under `src/world/**`
- `workflow/active/portfolio-world-art-v2/output/completion-report.md`

## Acceptance

Visual:
- spawn view reads as a premium floating sci-fi place rather than a primitive blockout;
- Central Plaza contains layered architecture with meaningful vertical scale;
- player is grounded within the environment;
- one bridge and at least three distant district silhouettes are readable;
- vegetation/props create human scale;
- warm/cool lighting and atmospheric depth are visible;
- user explicitly accepts the hero direction before district work continues.

Technical:
- movement/input semantics unchanged;
- topology/station/content/Ask unchanged;
- no page/runtime errors or failed requests;
- typecheck, 66 tests, build and all guards PASS;
- frozen asset budgets PASS;
- 390px remains usable;
- reduced-motion/no-WebGL behavior remains valid.

## Verify

- ICM bootstrap/workflow/strict checks
- `npm run typecheck`
- `npm test`
- `npm run build`
- `npm run verify:assets`
- `npm run verify:world-assets`
- `npm run verify:ask-disclosure`
- `npm run verify:world-ask`
- browser screenshot/runtime inspection at 1440px and 390px
- exact diff against v1 certified base for protected-state review

## Protected State

- movement.ts and movement constants
- semantic topology graph/bounds/fast-travel
- station IDs/positions/interaction points
- Ask/content/routes
- main and production
- prior certification evidence

## Known closed decisions

- PR #17 visual output is rejected and must not be merged;
- primitive-only environment construction is not an acceptable final art strategy;
- real curated modular assets are required;
- user visual acceptance is a hard gate before district propagation.

## Stop Conditions

- hero scene remains dominated by primitives;
- asset subset violates budget;
- asset license/source cannot be proven;
- navigation becomes obstructed;
- controller/topology/content drift occurs;
- second materially similar hero attempt is visually rejected.


## Active bounded repair — asset dependency closure

Stage 01 is currently blocked by incomplete glTF packaging, not by a proved failure of the asset-based art direction.

Repair constraints:
- do not push local failed commits `abec3eb` or `e36d08f`;
- prove one selected Quaternius glTF end-to-end before expanding;
- enumerate and vendor every external `buffers[].uri` and `images[].uri` dependency;
- preserve or intentionally rewrite relative paths so browser fetches resolve;
- add a deterministic repository check for missing glTF dependencies;
- require zero asset 404s/failed requests and visible browser geometry/material output;
- do not compensate for missing assets with new procedural stand-ins;
- do not continue district production until the Central Plaza hero asset set visibly renders.


## Reference-match lane override

The approved generated world image is the primary visual authority. Asset-library defaults, current procedural screenshots, and prior blockouts must not determine composition.

The current lane must satisfy `docs/portfolio-world/VISUAL-REFERENCE-CONTRACT.md` before Stage 01 can pass. In particular:
- lower/elevated third-person framing with horizon visible;
- player in lower third;
- Central Plaza as layered architecture rather than a slab;
- at least three district silhouettes visible from spawn;
- one finished bridge;
- vegetation/scale props;
- warm/cool lighting;
- 70–80% of visible hero architecture asset-driven or deliberately authored equivalent;
- no dominant primitive pillars/boxes.

A green test suite or Terra PASS cannot override failed user visual acceptance.
