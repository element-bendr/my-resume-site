# Stage 03 — District rollout

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/blender-world-art-pipeline
- owner: local Codex + ChatGPT coordinator
- execution mode: implementation
- parallel-write boundaries: district Blender/art sources, district visual evidence, scoped district runtime integration only

## Inputs

- `workflow/active/portfolio-world-blender-art/CONTEXT.md`
- certified Stage 02 Command Center source + runtime integration
- approved Command Center visual language / reusable kit
- finalized world reference images
- `src/world/WorldDistricts.tsx`
- `src/world/districts/DistrictStations.tsx`
- `src/world/world-topology.ts`
- `src/world/world-config.ts`
- `docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
- `docs/portfolio-world/BLENDER-QA-CERTIFICATION.md`
- `docs/portfolio-world/ASSET-BUDGET.md`

## Objective

Author and integrate the five remaining world districts one at a time, using the certified Command Center as the visual-system reference while preserving each district's distinct resume function and the existing lazy-loading/runtime boundaries.

## Fixed rollout order

Unless an explicit recorded decision changes it:

1. Build Lab
2. Automation Lab
3. Client Street
4. Timeline Corridor
5. Hobby District

Rationale:

- Build Lab and Automation Lab establish the reusable technical/industrial module family first;
- Client Street then tests a warmer commercial variation;
- Timeline tests monumental/archive language;
- Hobby District tests the most playful/organic variation last.

Do not build all five in parallel before validating the shared visual system.

## District identity targets

### Build Lab

- violet technical/industrial accent;
- fabrication/research/workbench language;
- strong vertical machinery/structure;
- readable Memory OS / Mnemos / Palimpsest station relationships.

### Automation Lab

- emerald/cyan operations accent;
- data/operations/system architecture;
- denser control-room/automation language;
- preserve PCAS / Newsharness / ChronoQuill / Content OS / Governed Runtime station readability.

### Client Street

- warm amber/commercial accent;
- civic/commercial street frontage;
- recognizable entrances/facades;
- Trifecta/KPDC and SteelMade stations remain legible.

### Timeline Corridor

- blue/gold archive accent;
- chronological/monumental promenade;
- strong directional sequence;
- V-Infinity / HCL / NIIT remain distinct without altering station data.

### Hobby District

- magenta/playful garden-studio accent;
- more vegetation/organic forms;
- lighter recreational/studio feel;
- Gaming / Anime / Kettlebells / Philosophy / Tinkering remain readable.

District colors are accents, not full-scene washes.

## In Scope

For each district:

- create governed editable Blender source;
- create a cheap massing/greybox checkpoint when the district composition is non-trivial;
- preserve certified zone bounds and station/fast-travel points;
- produce runtime-camera visual evidence;
- export one production GLB for the zone only after visual PASS;
- integrate through the existing lazy district boundary;
- preserve `DistrictStations`;
- disable decorative scenery raycasts where needed;
- remove redundant primitive decoration only after the Blender replacement passes;
- record source/export hashes and asset/performance evidence.

## Out of Scope

- changing district content/station identity;
- changing topology/fast-travel semantics;
- changing production deployment/domain;
- global lighting/post-processing polish that belongs to Stage 04;
- global performance tuning that belongs to Stage 05;
- merging or deploying before later certification stages.

## Dependencies

- Stage 02 certified;
- Command Center visual language accepted;
- `WorldDistricts.tsx` lazy-loading contract intact;
- `DistrictStations.tsx` station ownership intact.

## Process

For each district, complete the entire sequence before starting the next:

1. inspect certified bounds, stations, fast-travel point and bridge arrival;
2. define local authoring source/reference/preview paths;
3. establish massing first where needed;
4. visually review the greybox from the runtime/arrival view;
5. author final district geometry/material assignments;
6. validate source bounds/budgets;
7. export the district GLB;
8. run `npm run art:verify`;
9. integrate only that district GLB into its existing lazy module;
10. keep station React components unchanged;
11. validate fast travel, keyboard, click/tap movement and all station interactions;
12. capture desktop/mobile screenshots;
13. record exact candidate/evidence;
14. certify that district slice before continuing.

If a shared kit or design rule proves wrong, stop and correct it before propagating the defect to later districts.

## Outputs

For each of five districts:

- editable Blender source;
- runtime preview(s);
- source validation evidence;
- production GLB;
- scoped runtime integration;
- desktop/mobile evidence;
- source/GLB hashes and byte counts;
- per-zone visual/runtime verdict.

Repository-wide Stage 03 outputs:

- five certified lazy district integrations;
- updated art manifest;
- updated asset/performance measurements;
- Stage 03 completion record.

## Acceptance

Stage 03 passes only when:

- all five districts use accepted authored Blender scenery;
- each district remains visually distinct but belongs to the same world;
- `WorldDistricts.tsx` lazy imports remain intact;
- `DistrictStations.tsx` remains React-owned;
- fast travel arrives correctly in every zone;
- all station interactions remain unchanged;
- decorative meshes do not steal pointer events;
- no zone causes unexpected asset/network/runtime failures;
- per-zone asset packs remain within approved budgets or have explicit measured exceptions;
- no district reaches the next one with an unresolved visual/runtime FAIL.

## Verify

After each district integration:

```bash
python3 scripts/workflow_status.py --strict
npm run art:verify
npm run verify:world-zones
npm run typecheck
npm test
npm run build
npm run verify:world-assets
```

Browser evidence per district:

- 1440px desktop arrival/runtime view;
- 390px mobile arrival/runtime view;
- fast travel into the district;
- keyboard movement;
- click/tap movement;
- every station interaction in that district;
- clean route/overlay exit;
- console/network check for failed asset requests.

At Stage 03 completion also run:

```bash
npm run verify:offline
npm run verify:assets
npm run verify:ask-disclosure
npm run verify:world-ask
```

## Protected State

- `main`;
- production deployment/domain;
- verified resume/project content;
- station IDs, content, positions and interaction points;
- certified movement/topology/camera/route/accessibility behavior;
- `WorldDistricts.tsx` lazy-loading semantics;
- `DistrictStations.tsx` interaction ownership;
- user-owned `AGENTS.md`.

## Known closed decisions

- district content/station identity is unchanged;
- topology remains authoritative outside Blender;
- one GLB is delivered per world zone;
- district rollout is sequential, not bulk;
- the certified Command Center supplies the shared visual-system language, not identical district styling.

## Stop Conditions

- two materially similar visual/implementation attempts fail for a district;
- a shared design rule is discovered to be wrong;
- an asset requires relaxing a certified behavior or safety boundary;
- required validation cannot be performed;
- unexpected unrelated diff appears;
- user-owned `AGENTS.md` is modified.
