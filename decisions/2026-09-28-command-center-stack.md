# Decision: Command Center vertical-slice stack

date: 2026-09-28
status: accepted
owners: coordinator
supersedes: none
superseded_by: none

## Context

Stage 02 certified the conventional React/Cloudflare portfolio foundation. Stage 03 must now prove the 3D architecture without prematurely building the full world or introducing asset/physics complexity.

Current package review on 2026-09-28 found same-day patch releases in the Three/R3F ecosystem. Production-first policy favors the immediately prior stable versions with enough time in circulation while preserving React 19.3 compatibility.

## Decision

Pin exactly:
- `three` 0.186.0
- `@react-three/fiber` 9.8.0
- `@react-three/drei` 10.7.8
- `@types/three` 0.186.0

R3F 9.8.0 is selected because its release explicitly adds React 19.3 support.

The Command Center uses procedural primitives rather than external GLB/texture assets. Movement is kinematic and bounded; no physics or navmesh package is introduced.

The initial slice consists of:
- one Command Center;
- one primitive avatar;
- constrained movement;
- follow/orbit camera;
- click-to-move;
- three stations;
- accessible HTML interaction overlays;
- persistent direct portfolio navigation.

## Consequences

- renderer architecture is tested with almost no media payload;
- movement/camera bugs can be isolated from model/asset problems;
- first-load cost is dominated by code rather than art;
- later GLB/KTX2 work can be measured against a known baseline;
- new districts remain blocked until this slice certifies.

## Validation / evidence

- npm package/release data reviewed 2026-09-28;
- R3F 9.8.0 release notes explicitly cite React 19.3 compatibility;
- Drei 10.7.8 peers on R3F 9, React 19, and Three >=0.159;
- Stage 03 clean install/build evidence is still required.

## Revisit when

- frozen dependencies fail clean installation or typecheck;
- a demonstrated interaction requires a capability unavailable in the selected stack;
- Stage 03 certification is complete and Stage 04 asset/world expansion begins.
