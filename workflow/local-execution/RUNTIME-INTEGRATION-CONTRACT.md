# Command Center React/runtime integration contract

Status: active after certified production export.

## Source authority

The integration source is the evidence-normalized certified export candidate:

- source task: `command-center-export-evidence-001`
- source ref: `refs/heads/icm/candidates/command-center-export-evidence-001`
- source SHA: `890f584306b6a44c4bf5d325591cb7e9ee1bf718`
- production GLB SHA-256: `72008b693cf0fc889aea7cf8af94ec2876cc0e3a7807b430e6e483fe275d7496`
- production GLB bytes: `845512`

The integration task must start from that exact candidate and must not rewrite the GLB.

## Ownership boundary

Blender owns decorative Command Center scenery only.

React remains authoritative for:

- world topology and walkable bounds;
- player spawn and movement;
- bridges and zone connectivity;
- camera rig;
- interaction stations and resume/content data;
- Ask behavior;
- HUD/map;
- click/tap/keyboard movement;
- no-WebGL/conventional-route fallback.

The runtime must not infer any of those contracts from GLB meshes or object names.

## Integration seam

The existing asset registry is authoritative:

`BLENDER_ART_ASSETS["command-center"] === "/world/art/command-center.glb"`

and:

`BLENDER_ART_PLACEMENTS["command-center"] === [0, 0, 0]`

Integration should use this registry instead of introducing a duplicate literal asset path or transform.

The current procedural Command Center scenery may be reduced/replaced only where the certified GLB supplies equivalent decorative scenery. Interaction stations, movement target marker, lighting/fog needed by the runtime, and React-owned interaction behavior remain intact.

Loading must be bounded by React Suspense and retain a local decorative fallback so an asset load failure does not destroy navigation authority or conventional routes.

## Required behavior

After integration:

- Command Center GLB renders at its certified origin;
- GLB is decorative only;
- Ask Terminal remains at its existing React-owned station coordinates;
- player spawn remains unchanged;
- movement/topology remain unchanged;
- camera semantics remain unchanged;
- click/tap/keyboard movement remains unchanged;
- other districts retain current behavior and lazy loading;
- conventional routes still do not require the GLB;
- WebGL fallback remains available;
- production GLB bytes are unchanged.

## Validation

The runner uses:

- `blender-assets` -> existing GLB structural/budget validation;
- `runtime-integration` -> `npm run verify`;
- `icm-stage` -> strict workflow-state validation.

`npm run verify` already covers offline world checks, tests, production build, conventional asset budget and world JS budget.

## Independent review

Terra reviews the exact integration candidate and must verify:

- the source export candidate is exact;
- GLB bytes/hash are unchanged;
- asset path/placement come from the existing Blender art registry;
- no topology/config/interaction content authority moved into the GLB;
- React-owned spawn, Ask, camera and bridges remain unchanged;
- conventional fallback and route isolation remain intact;
- only declared runtime/test/evidence paths changed;
- all runner validations pass.

A PASS integration candidate does not authorize merge to `main` or deployment. Browser/visual certification is a separate governed task.
