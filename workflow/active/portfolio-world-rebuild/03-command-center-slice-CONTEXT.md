# Stage 03 — Command Center Vertical Slice

## Authority / ownership

- repository: element-bendr/my-resume-site
- branch/worktree: feat/portfolio-world-icm-rebuild
- owner: coordinator
- execution mode: implementation
- stage boundary: Command Center only; no additional world districts

## Inputs

- certified Stage 00 world/movement/rendering architecture
- certified Stage 01 content authority contract
- certified Stage 02 application foundation and exact lockfile
- Stage 02 ICM validated commit: 0f2ef77df68fdd28674b50bfe83c183770adf890
- docs/portfolio-world/WORLD-SPEC.md
- docs/portfolio-world/MOVEMENT-ARCHITECTURE.md
- docs/portfolio-world/RENDERING-TECHNOLOGY.md
- docs/portfolio-world/ASSET-BUDGET.md

## Objective

Prove the complete browser-side 3D interaction architecture inside one polished Command Center before expanding the world.

The slice must demonstrate that a visitor can enter /play, understand where they are, move without game expertise, inspect meaningful portfolio objects, open accessible HTML content, and leave the 3D experience at any time.

## In Scope

- Three.js 0.186.0;
- @react-three/fiber 9.8.0;
- @react-three/drei 10.7.8;
- @types/three 0.186.0;
- WebGL 2 production path through Three/R3F;
- procedural low-poly Command Center geometry only;
- lightweight stylized avatar built from primitives;
- idle/walk visual state;
- WASD/arrow movement;
- click-to-move on the Command Center floor;
- constrained legal walkable rectangle;
- elevated third-person camera with limited orbit and follow behavior;
- three interaction stations;
- proximity/selection cues;
- one real project-detail HTML overlay;
- Ask-terminal entry overlay/placeholder that routes to the conventional Ask surface;
- world HUD exposing Map, Projects, Resume, Ask, Contact;
- reduced-motion-aware camera behavior;
- non-WebGL/direct-route escape path;
- deterministic movement/math tests;
- Stage 03 bundle/asset budget checks.

## Out of Scope

- additional world districts;
- GLB/FBX models;
- texture packs;
- physics engines;
- general navmesh/pathfinding library;
- jumping, falling, combat, crouching, sprint button, platforming;
- final character art;
- mobile virtual joystick;
- production Ask backend;
- WebGPU production path;
- audio;
- R2/D1/KV/Durable Objects;
- production deployment/promotion.

## Dependencies

- Stage 02 must remain certified;
- package-lock must remain deterministic after adding the Stage 03 dependencies;
- React Three Fiber 9.8.0 is selected specifically for React 19.3 compatibility;
- Drei 10.7.8 peer contract supports R3F 9 / React 19 / Three >=0.159.

## Process

1. Pin and install only the frozen 3D dependencies.
2. Replace the /play placeholder with a lazy-loaded WorldEntry boundary.
3. Build the procedural Command Center floor, walls, lighting, landmarks, and three stations.
4. Implement a kinematic PlayerController with a shared position reference.
5. Add camera-relative WASD movement and floor click-to-move.
6. Clamp all movement to legal Command Center bounds.
7. Add the elevated follow/orbit camera with constrained angles/zoom.
8. Add proximity/interaction resolution and HTML overlays.
9. Preserve global HUD/direct routes outside the Canvas.
10. Add deterministic tests for movement clamping, target stepping, interaction reach, and world config.
11. Run clean install, typecheck, tests, build, Stage 03 budget checks, and preview smoke.
12. Visually inspect the slice before certification.

## Outputs

- decisions/2026-09-28-command-center-stack.md
- src/world/WorldEntry.tsx
- src/world/CommandCenter.tsx
- src/world/PlayerController.tsx
- src/world/CameraRig.tsx
- src/world/InteractionStation.tsx
- src/world/world-config.ts
- src/world/movement.ts
- src/world/world.css
- src/world/WorldHud.tsx
- src/world/InteractionOverlay.tsx
- tests/movement.test.ts
- tests/world-config.test.ts
- scripts/check-world-boundary.mjs
- updated package.json/package-lock.json
- updated /play integration

## Acceptance

- /play lazy-loads the 3D slice and conventional routes remain usable without it;
- WebGL canvas renders the Command Center without external model/texture assets;
- avatar can move using WASD/arrows;
- click on legal floor produces click-to-move;
- player position never exits declared walkable bounds;
- movement is camera-relative;
- camera follows the avatar and user orbit is constrained;
- three stations can be discovered and selected;
- at least one project station opens a source-backed HTML project detail surface;
- Ask station opens a clear HTML Ask entry surface with conventional Ask route;
- movement is suspended while an overlay owns interaction;
- closing overlay restores movement;
- direct Projects/Resume/Ask/Contact navigation remains visible outside the Canvas;
- reduced-motion setting disables non-essential camera smoothing;
- no physics/navmesh dependency is present;
- no WebGPU requirement is present;
- first visible 3D code/assets stay within the frozen 3 MiB compressed target;
- TypeScript, automated tests, build, Stage 03 boundary checks, and preview smoke are green;
- main and production remain unchanged.

## Verify

- npm ci
- npm run verify:content
- npm run verify:config
- npm run verify:world
- npm run typecheck
- npm test
- npm run build
- npm run verify:assets
- preview /play and /api/health
- visual inspection desktop
- keyboard-only/direct-route escape inspection
- python3 scripts/workflow_check.py
- python3 scripts/workflow_status.py --strict

## Protected State

- main and current production deployment/domain;
- certified Stage 00/01/02 decisions and evidence;
- conventional routes and content authority;
- unresolved education/LinkedIn/client outcome fields;
- no additional district implementation before this slice certifies;
- no production WebGPU dependency.

## Known closed decisions

- procedural geometry is sufficient for this slice;
- no physics engine in Stage 03;
- no navmesh library in Stage 03; one-room legal movement is deterministic clamping;
- Three 0.186.0 / R3F 9.8.0 / Drei 10.7.8 / @types/three 0.186.0 are frozen for the slice;
- same-day Three 0.186.1, R3F 9.8.1, and Drei 10.7.9 patches are intentionally not adopted mid-build;
- substantive content remains HTML-over-3D;
- Stage 03 proves architecture, not final art fidelity.

## Stop Conditions

- Stage 02 evidence becomes stale or fails;
- peer/dependency install is incompatible with React 19.3;
- first visible 3D bundle exceeds budget without a measured explanation;
- movement can escape bounds or become trapped;
- camera can enter uncontrolled/free-flight state;
- direct portfolio routes become inaccessible;
- implementation requires physics or a new runtime capability not covered by this contract;
- protected state would change.
