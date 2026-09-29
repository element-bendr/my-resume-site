# Stage 04 — World Zones

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/portfolio-world-icm-rebuild
- owner: coordinator
- execution mode: implementation
- stage boundary: world districts/topology only; backend Ask integration remains Stage 05

## Inputs

- certified Stage 00 world/movement/rendering architecture
- certified Stage 01 content authority
- certified Stage 02 application foundation
- certified Stage 03 Command Center controller and browser proof
- Stage 03 ICM validated commit: 32d43aed13a91815007a0d29f384a31fe2246974
- docs/portfolio-world/WORLD-SPEC.md
- docs/portfolio-world/MOVEMENT-ARCHITECTURE.md
- docs/portfolio-world/RENDERING-TECHNOLOGY.md
- docs/portfolio-world/STAGE-03-VALIDATION.md

## Objective

Expand the certified Command Center into the complete explorable Portfolio World without changing the proven locomotion, renderer, accessibility, or content-authority contracts.

The world must gain five real districts:
- Build Lab
- Automation Lab
- Client Street
- Timeline Corridor
- Hobby District

The Ask Terminal remains in the Command Center for Stage 04.

## In Scope

- one global coordinate system;
- one shared PlayerController and CameraRig;
- multiple rectangular walkable platforms connected by walkable bridge/corridor areas;
- union-of-walkable-areas movement constraints;
- district identification from player position;
- map-based fast travel to every major district;
- persistent zone name in the HUD;
- lightweight always-present world topology;
- district-specific procedural geometry;
- per-district dynamic/lazy module boundaries;
- project stations sourced from typed project content;
- timeline stations sourced from structured experience content;
- hobby stations sourced from user-approved hobby content;
- HTML interaction overlays for project, experience, and hobby records;
- deterministic topology/reachability/fast-travel tests;
- Stage 04 asset/bundle budget checks;
- desktop browser screenshot evidence.

## Out of Scope

- Ask backend/model integration;
- production contact form backend;
- external GLB/FBX character/environment packs;
- audio;
- multiplayer;
- physics engine;
- general third-party navmesh/pathfinding dependency;
- WebGPU production renderer;
- final art polish;
- production deployment.

## World topology

The coordinate layout is deterministic and intentionally compact.

- Command Center: central hub
- Client Street: west
- Hobby District: east
- Timeline Corridor: north
- Build Lab: south-west
- Automation Lab: south-east

Each district is joined to the Command Center through a legal bridge/corridor area. The walkable union, not visible decorative geometry, is movement authority.

## Loading model

The topology floor/bridges and zone beacons are always lightweight and present.

District detail is a separate dynamic module. A district detail module loads when:
- the visitor enters that district;
- the visitor chooses that district via fast travel;
- the district has already been visited in the current session.

No external model/texture assets are introduced in this stage, so the lazy boundary proves architecture without manufacturing asset weight.

## Fast travel

Map fast travel:
1. selects a valid district;
2. marks the target district detail as loaded;
3. clears pending click/interact state;
4. moves the avatar to the district fast-travel spawn;
5. updates current-zone state;
6. closes the map;
7. lets the certified camera rig settle around the new avatar position.

Reduced-motion users receive the same destination without any additional cinematic camera behavior.

## Process

1. Freeze world-zone topology and data contracts.
2. Generalize movement from one rectangle to the union of legal walkable areas.
3. Add zone detection and fast-travel spawn configuration.
4. Add lightweight topology/bridge geometry.
5. Add district lazy boundaries.
6. Implement Build Lab and Automation Lab project stations.
7. Implement Client Street project storefront/stations.
8. Implement Timeline Corridor experience stations.
9. Implement Hobby District user-approved stations.
10. Extend HTML interaction overlays by content kind.
11. Extend HUD/map to real district travel.
12. Add deterministic tests and CI/budget/browser evidence.
13. Visually inspect world composition before certification.

## Outputs

- decisions/2026-09-29-world-zones.md
- src/world/world-topology.ts
- src/world/WorldTopology.tsx
- src/world/WorldDistricts.tsx
- src/world/districts/BuildLab.tsx
- src/world/districts/AutomationLab.tsx
- src/world/districts/ClientStreet.tsx
- src/world/districts/TimelineCorridor.tsx
- src/world/districts/HobbyDistrict.tsx
- generalized world-config / movement / PlayerController / HUD / overlay
- tests/world-topology.test.ts
- Stage 04 world validation/budget checks
- Stage 04 certification workflow and browser evidence

## Acceptance

- all six major zones resolve to deterministic bounds and fast-travel spawns;
- every district is reachable from Command Center through legal walkable areas;
- player cannot move into the void between zones/bridges;
- the Stage 03 controller remains the only player controller;
- map fast travel reaches every district;
- current zone updates as the player traverses or fast-travels;
- each district has a distinct readable visual identity;
- Build/Automation/Client project stations open typed project content;
- Timeline opens structured experience content;
- Hobby opens user-approved hobby content;
- direct Projects/Resume/Ask/Contact routes remain available;
- WebGL failure fallback remains green;
- district modules are dynamically split;
- no external 3D asset pack is required;
- no physics/navmesh package is introduced;
- tests/typecheck/build/budgets/browser proof are green;
- main and production remain unchanged.

## Verify

- npm ci
- npm run verify:content
- npm run verify:config
- npm run verify:world
- npm run verify:world-zones
- npm run typecheck
- npm test
- npm run build
- npm run verify:assets
- npm run verify:world-assets
- preview /play and /api/health
- browser fallback proof
- desktop world screenshot inspection
- python3 scripts/workflow_check.py
- python3 scripts/workflow_status.py --strict

## Protected State

- main / production deployment/domain;
- certified Stage 00-03 contracts and evidence;
- Stage 03 movement/camera semantics;
- content-source/disclosure authority;
- conventional route availability;
- Ask backend remains Stage 05;
- no final-art/external-asset scope creep.

## Known closed decisions

- one shared world/controller, not per-zone controller instances;
- legal movement is a deterministic union of rectangles/bridges in Stage 04;
- district detail is lazy/dynamic even though procedural assets remain small;
- map fast travel is first-class and does not require walking;
- Command Center remains the spawn/home hub;
- Ask Terminal remains in Command Center;
- Stage 04 proves complete world topology, not final art fidelity.

## Stop Conditions

- Stage 03 certification becomes stale;
- movement can cross non-walkable voids;
- a district requires a second movement/camera architecture;
- district loading breaks interaction/content reachability;
- bundle/asset budgets regress beyond frozen limits without evidence;
- direct professional routes become inaccessible;
- protected state would change.
