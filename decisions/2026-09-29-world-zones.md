# Decision: Expand Portfolio World as one shared topology with lazy district modules

date: 2026-09-29
status: accepted
owners: coordinator
supersedes: none
superseded_by: none

## Context

Stage 03 certified one procedural Command Center and one movement/camera/interaction architecture. Stage 04 must expand the world without duplicating controllers or introducing a heavyweight navmesh/physics dependency.

The world also needs to preserve the previously frozen rule that zones are independent loading boundaries.

## Decision

Use one global world coordinate system with:
- a central Command Center;
- five district platforms;
- deterministic bridge/corridor walkable rectangles;
- a union-of-walkable-areas constraint;
- one PlayerController;
- one CameraRig;
- one global interaction registry;
- one global HUD/map.

District detail is code-split by district and loads when entered, fast-travelled to, or already visited.

Always-present topology is intentionally lightweight:
- floors;
- bridges;
- district beacons/labels.

District modules provide the visual and content detail.

No external GLB/texture pack is required in Stage 04.

## District responsibilities

- Build Lab: Memory OS, Mnemos, Palimpsest and build-system motifs.
- Automation Lab: PCAS, Newsharness, ChronoQuill, ArtSports Content OS, Governed Runtime.
- Client Street: Trifecta/KPDC, SteelMade, and later public-safe client cards.
- Timeline Corridor: structured V-Infinity, HCL Comnet, and NIIT experience.
- Hobby District: Gaming, Anime, Kettlebells, Philosophy, Tinkering.
- Command Center: identity/home hub and Ask Terminal.

## Movement consequence

The Stage 03 `COMMAND_CENTER_BOUNDS` clamp becomes a generalized legal-area constraint.

A proposed movement point:
- remains unchanged when inside any legal platform/bridge;
- otherwise projects to the nearest point in the legal-area union.

Because legal bridge rectangles overlap their source/destination platforms, normal small-step movement can cross between zones without teleporting over voids.

## Fast travel consequence

Fast travel is a state transition, not simulated walking:
- validate zone;
- load target detail;
- place avatar at zone spawn;
- clear pending movement/interaction;
- update current zone.

## Loading consequence

The world can retain visited district modules for the session to avoid repeated code/module churn.

No R2, Worker storage, or persistence is needed.

## Revisit when

- polygonal walkable geometry becomes necessary for final art;
- external GLB/texture assets create measured memory/load pressure;
- the rectangle-union model materially limits the final world composition;
- a navmesh library offers a demonstrated benefit that outweighs complexity.
