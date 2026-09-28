# Decision: Use guided third-person movement with constrained navigation

date: 2026-09-28
status: accepted
owners: coordinator
supersedes: none
superseded_by: none

## Context

The 3D portfolio needs to feel explorable without turning professional information into a game-skill test. The visitor may be a gamer, recruiter, client, mobile user, keyboard user, pointer-only user, or someone running a reduced-motion/low-power environment.

A fully free physics-driven character introduces avoidable risks: falling, collision traps, expensive simulation, camera disorientation, and mobile control complexity. A purely fixed camera or slideshow would lose the desired sense of inhabiting the portfolio world.

## Decision

Use a hybrid guided third-person controller:
- elevated trailing camera;
- WASD/arrow movement;
- desktop click-to-move;
- mobile tap-to-move;
- constrained navmesh/navigation graph;
- context-sensitive interaction points;
- map-based fast travel;
- automatic interaction positioning;
- HTML overlays for substantive content.

Do not implement jumping, combat, platforming, falling, free-flight camera control, or a mandatory physics engine for v1 movement.

The map and conventional HTML routes are permanent escape hatches from physical traversal.

## Consequences

- the visitor experiences a spatial portfolio without needing game expertise;
- navigation remains deterministic and testable;
- mobile control is simpler;
- geometry can be visually dramatic without becoming collision complexity;
- zone connectors can also serve as lazy-load/prefetch boundaries;
- interaction design remains compatible with accessible HTML content.

## Validation / evidence

Implementation is governed by:
- `docs/portfolio-world/WORLD-SPEC.md`;
- `docs/portfolio-world/MOVEMENT-ARCHITECTURE.md`;
- `docs/portfolio-world/ASSET-BUDGET.md`.

The command-center vertical slice must prove the movement contract before world expansion.

## Revisit when

- usability testing shows the camera or movement model is materially confusing;
- mobile tap navigation cannot provide reliable target selection;
- a new interaction genuinely requires physics or another locomotion state;
- performance measurements show the selected navigation implementation is unsuitable.
